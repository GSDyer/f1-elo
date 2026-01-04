import pandas as pd

RACE_RESULTS_CSV = "data/processed/race_results.csv"

def expected_score(rating_a, rating_b):
    """
    Calculates probability that A beats B, to be used in ELO calculation
    """
    return (1 / (1 + 10 ** ((rating_b - rating_a) / 400)))

def calc_elo_change(rating_a, rating_b, score_a, k=20):
    """
    Calculates the change in ELO for A and B based on their current ELO and who won in matchup
    
    :param rating_a: Current ELO for A
    :param rating_b: Current ELO for B
    :param score_a: 1 if A wins matchup, 0 if A lost matchup
    :param k: k value to define how much ELO changes per matchup
    """
    expected_a = expected_score(rating_a, rating_b)
    expected_b = 1 - expected_a

    new_a = rating_a + (k * (score_a - expected_a))
    new_b = rating_b + (k * ((1 - score_a) - expected_b))

    return new_a, new_b

def process_single_race(race_df, elos):
    """
    Updates ELO ratings for drivers after a single race
    """
    race_df = race_df.sort_values("position")
    drivers = race_df["driver_id"].tolist()

    for driver in drivers:
        elos.setdefault(driver, 1500)

    pre_race_elos = {d: elos[d] for d in drivers}

    deltas = {d: 0.0 for d in drivers}

    for i, driver_a in enumerate(drivers):
        for driver_b in drivers[i + 1:]:
            rating_a = pre_race_elos[driver_a]
            rating_b = pre_race_elos[driver_b]

            new_a, new_b = calc_elo_change(rating_a, rating_b, score_a=1)
            deltas[driver_a] += (new_a - rating_a) / (len(drivers) - 1)
            deltas[driver_b] += (new_b - rating_b) / (len(drivers) - 1)
    
    for driver in drivers:
        elos[driver] += deltas[driver]
    

def compute_elo_history():

    df = pd.read_csv(RACE_RESULTS_CSV)

    df = df.sort_values(["season", "round", "position"]).reset_index(drop=True)

    elos = {}
    history_rows = []

    for (season, round_num), race_df in df.groupby(["season", "round"]):
        race_name = race_df["race_name"].iloc[0]

        process_single_race(race_df, elos)

        for driver_id in race_df["driver_id"]:
            history_rows.append({
                "season": season,
                "round": round_num,
                "race_name": race_name,
                "driver_id": driver_id,
                "elo": elos[driver_id]
            }) 
    history_df = pd.DataFrame(history_rows)
    return history_df

if __name__ == "__main__":
    elo_history = compute_elo_history()
    print(elo_history.head())
    elo_history.to_csv("data/elo_scores/elo_history.csv", index=False)