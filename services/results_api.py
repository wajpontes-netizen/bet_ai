import requests
import os

API_KEY = os.getenv("API_KEY")  # sua chave
BASE_URL = "https://api-football-v1.p.rapidapi.com/v3/fixtures"

HEADERS = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
}

def get_result(fixture_id):

    try:
        url = f"{BASE_URL}?id={fixture_id}"
        res = requests.get(url, headers=HEADERS)
        data = res.json()

        response = data.get("response", [])
        if not response:
            return None

        goals_home = response[0]["goals"]["home"]
        goals_away = response[0]["goals"]["away"]

        return goals_home, goals_away

    except:
        return None