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

            home = item["teams"]["home"]["name"]
            away = item["teams"]["away"]["name"]
            league = item["league"]["name"]

            # -----------------------------
            # ODDS REAIS
            # -----------------------------
            odds_url = f"https://v3.football.api-sports.io/odds?fixture={fixture_id}"
            odds_res = requests.get(odds_url, headers=headers).json()

            over25 = 0

            for book in odds_res.get("response", []):
                for bookmaker in book.get("bookmakers", []):
                    for market in bookmaker.get("bets", []):
                        if market["name"] == "Goals Over/Under":
                            for val in market["values"]:
                                if val["value"] == "Over 2.5":
                                    over25 = float(val["odd"])

            if over25 == 0:
                continue

            # -----------------------------
            # ESTATÍSTICAS REAIS (simplificado)
            # -----------------------------
            stats_url = f"https://v3.football.api-sports.io/fixtures/statistics?fixture={fixture_id}"
            stats_res = requests.get(stats_url, headers=headers).json()

            home_shots = 10
            away_shots = 10

            try:
                for team in stats_res["response"]:
                    for stat in team["statistics"]:
                        if stat["type"] == "Total Shots":
                            if team["team"]["name"] == home:
                                home_shots = int(stat["value"] or 10)
                            else:
                                away_shots = int(stat["value"] or 10)
            except:
                pass

            # -----------------------------
            # xG APROXIMADO REALISTA
            # -----------------------------
            home_xg = home_shots * 0.1
            away_xg = away_shots * 0.1

            corners_mean = 9 + (home_shots + away_shots) * 0.05

            games.append({
                "match": f"{home} vs {away}",
                "league": league,
                "home_xg": home_xg,
                "away_xg": away_xg,
                "corners_mean": corners_mean,
                "odds": {"over25": over25}
            })

        except Exception as e:
            print(f"Erro API: {e}")
            continue

    return games