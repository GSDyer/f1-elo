import json
import os
import csv

RAW_DATA_DIR = os.path.join("data", "raw", "jolpica")
PROCESSED_DATA_DIR = os.path.join("data", "processed")

OUTPUT_FILE = os.path.join(PROCESSED_DATA_DIR, "race_results.csv")


def load_season_file(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def extract_race_results(season_data: dict) -> list[dict]:
    rows = []

    for race in season_data["Races"]:
        season = int(race["season"])
        round_num = int(race["round"])
        race_name = race["raceName"]

        for result in race.get("Results", []):
            rows.append({
                "season": season,
                "round": round_num,
                "race_name": race_name,
                "driver_id": result["Driver"]["driverId"],
                "driver_name": result["Driver"]["givenName"] + " " + result["Driver"]["familyName"],
                "position": int(result["position"]),
                "status": result.get("status", ""),
            })
    
    return rows

def process_all_seasons() -> list[dict]:
    all_rows = []

    for filename in sorted(os.listdir(RAW_DATA_DIR)):
        if not filename.endswith("_season_results.json"):
            continue
        path = os.path.join(RAW_DATA_DIR, filename)
        season_data = load_season_file(path)
        rows = extract_race_results(season_data)
        all_rows.extend(rows)

    return all_rows

def write_csv(rows: list[dict], output_path: str):
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)


def main():
    rows = process_all_seasons()
    write_csv(rows, OUTPUT_FILE)
    print(f"Wrote {len(rows)} rows to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()