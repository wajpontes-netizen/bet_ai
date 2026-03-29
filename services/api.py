import requests
from datetime import datetime
from config import API_KEY

def get_games():
    headers = {
        "x-apisports-key": API_KEY
    }

    # tenta jogos ao vivo
    url = "https://v3.football.api-sports.io/fixtures?live=all"
    res = requests.get(url, headers=headers)
    data = res.json()

    # fallback: jogos do dia
    if not data.get("response"):
        today = datetime.now().strftime("%Y-%m-%d")
        url = f"https://v3.football.api-sports.io/fixtures?date={today}"
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
                "home_xg": 1.4,
                "away_xg": 1.2,
                "corners_mean": 9.5,
                "odds": {"over25": 1.85}
            })

        except:
            continue

    return games