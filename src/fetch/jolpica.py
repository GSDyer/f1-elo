import requests

BASE_URL = "https://api.jolpi.ca/ergast/f1/"

def get_drivers(season: int):
    """
    Fetch drivers from given season from Jolpica API
    """
    url = f"{BASE_URL}{season}/results/"
    response = requests.get(url)
    response.raise_for_status()
    
    data = response.json()
    # drivers_raw = data["MRData"]["DriverTable"]["Drivers"]
    # drivers = []
    # for d in drivers_raw:
    #     driver_id = d.get("driverId")
    #     full_name = f"{d.get("givenName", " ")}{d.get("familyName", " ")}".strip()
    #     driver_code = d.get("code")
    #     drivers.append({"driver_id": driver_id,
    #                     "full_name": full_name,
    #                     "driver_code": driver_code
    #                     })
    return data