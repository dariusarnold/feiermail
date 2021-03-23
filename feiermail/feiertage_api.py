import requests
from holiday import Holiday


def get_holiday_json(year: int, bundesland: str):
    response = requests.get(f"https://feiertage-api.de/api/?jahr={year}&nur_land={bundesland}")
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Request failed with status code {response.status_code}")
        return None


def parse_json(json_holidays):
    """
    Ein Json Element enthält den Namen des Feiertags als Key, als Value ein weiteres dict mit den keys "datum"
    und "hinweis".
    Datum ist im YYYY-MM-DD Format.
    :param json_holidays:
    :return:
    """
    holidays = []
    for name_holiday in json_holidays:
        holidays.append(Holiday(name_holiday, json_holidays[name_holiday]["datum"]))
    return holidays