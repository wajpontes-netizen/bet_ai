import requests
from config import API_KEY

def get_games():
    url = "https://v3.football.api-sports.io/fixtures?next=10"

    headers = {
        "x-apisports-key": API_KEY
    }

    res = requests.get(url, headers=headers)
    data = res.json()

    games = []

    for item in data["response"]:
        try:
            home = item["teams"]["home"]["name"]
            away = item["teams"]["away"]["name"]
            league = item["league"]["name"]

            # ⚠️ ainda precisamos melhorar dados depois
            home_xg = 1.5
            away_xg = 1.3

            odds = {
                "over25": 1.90  # depois vamos puxar real
            }

            games.append({
                "match": f"{home} vs {away}",
                "league": league,
                "home_xg": home_xg,
                "away_xg": away_xg,
                "corners_mean": 9.5,
                "odds": odds
            })

        except:
            continue

    return games