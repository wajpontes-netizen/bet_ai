import requests
from config import API_KEY

def get_games():
    url = "https://v3.football.api-sports.io/fixtures?live=all"

    headers = {
        "x-apisports-key": API_KEY
    }

    res = requests.get(url, headers=headers)
    data = res.json()

    games = []

    for item in data.get("response", []):
        try:
            home = item["teams"]["home"]["name"]
            away = item["teams"]["away"]["name"]
            league = item["league"]["name"]

            games.append({
                "match": f"{home} vs {away}",
                "league": league,
                "home_xg": 1.5,
                "away_xg": 1.3,
                "corners_mean": 9.5,
                "odds": {"over25": 1.90}
            })

        except:
            continue

    return games