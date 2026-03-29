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

    for item in data.get("response", []):
        try:
            fixture_id = item["fixture"]["id"]

            # buscar odds do jogo
            odds_url = f"https://v3.football.api-sports.io/odds?fixture={fixture_id}"
            odds_res = requests.get(odds_url, headers=headers).json()

            over25 = 0

            for book in odds_res.get("response", []):
                for bet in book.get("bookmakers", []):
                    for market in bet.get("bets", []):
                        if market["name"] == "Goals Over/Under":
                            for value in market["values"]:
                                if value["value"] == "Over 2.5":
                                    over25 = float(value["odd"])

            if over25 == 0:
                continue

            games.append({
                "match": f"{item['teams']['home']['name']} vs {item['teams']['away']['name']}",
                "league": item["league"]["name"],
                "home_xg": 1.5,
                "away_xg": 1.3,
                "corners_mean": 9.5,
                "odds": {"over25": over25}
            })

        except:
            continue

    return games