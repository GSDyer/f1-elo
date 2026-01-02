import json
import os
import requests
import time

BASE_URL = "https://api.jolpi.ca/ergast/f1/"
RAW_DATA_DIR = os.path.join("data", "raw", "jolpica")

def get_season_results(season: int):
    """
    Queries Jolpica API for all race results from a specific season, and saves it as a JSON in data/raw/jolpica
    Will skip if the season JSON already exists
    """
    output_file = output_file = os.path.join(RAW_DATA_DIR, f"{season}_season_results.json")
    if os.path.exists(output_file):
        print(f"Raw data for season {season} already exists: Skipping API call")
        return
    
    all_races = []
    race_lookup = {}
    limit = 100
    offset = 0

    while True:
        print(f"Fetching season: {season} with offset: {offset}")
        url = f"{BASE_URL}{season}/results/?limit={limit}&offset={offset}"
        response = requests.get(url)

        data = response.json()
        races = data["MRData"]["RaceTable"]["Races"]
        for race in races:
            key = (race["season"], race["round"])
            #Check if previous API request stopped partway through a races results
            if key not in race_lookup:
                all_races.append(race)
                race_lookup[key] = race
            else:
                existing_race = race_lookup[key]
                existing_driver_ids = {d["Driver"]["driverId"] for d in existing_race.get("Results", [])}
                for d in race.get("Results", []):
                    if d["Driver"]["driverId"] not in existing_driver_ids:
                        existing_race.setdefault("Results", []).append(d)

        total = int(data["MRData"]["total"])
        offset += limit
        if offset >= total:
            break
        time.sleep(0.5)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump({"Races": all_races}, f, ensure_ascii=False, indent=2)
