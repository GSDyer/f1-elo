from src.fetch.jolpica import get_drivers


def main():
    drivers = get_drivers(season=2025)
    print(f"Fetched {len(drivers)} drivers")

if __name__ == "__main__":
    main()