from src.fetch.jolpica import get_season_results


def main():
    for season in range(1950,2026):
        get_season_results(season)

if __name__ == "__main__":
    main()