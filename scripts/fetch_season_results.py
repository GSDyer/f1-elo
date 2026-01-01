from src.fetch.jolpica import get_season_results


def main():
    get_season_results(season=2025)
    print("2025 data complete")

if __name__ == "__main__":
    main()