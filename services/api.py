import requests
from config import API_KEY

def get_games():
    url = "https://v3.football.api-sports.io/fixtures?next=10"

    headers = {
        "x-apisports-key": API_KEY
    }

    try:
        res = requests.get(url, headers=headers)
        data = res.json()
    except:
        return []

    games = []

    for item in data.get("response", []):
        try:
            home = item["teams"]["home"]["name"]
            away = item["teams"]["away"]["name"]
            league = item["league"]["name"]

            # dados simples (garantidos)
            home_xg = 1.4
            away_xg = 1.2
            corners_mean = 9.5

            # odds fallback (temporário)
            odds = 1.85

            games.append({
                "match": f"{home} vs {away}",
                "league": league,
                "home_xg": home_xg,
                "away_xg": away_xg,
                "corners_mean": corners_mean,
                "odds": {"over25": odds}
            })

        except:
            continue

    return games