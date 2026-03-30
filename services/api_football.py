import requests
from datetime import datetime

API_KEY = "92e513a4009536a16df3603b9fff54d0"

def get_games():
    url = "https://v3.football.api-sports.io/fixtures"

    today = datetime.now().strftime("%Y-%m-%d")

    headers = {
        "x-apisports-key": API_KEY
    }

    params = {
        "date": today
    }

    try:
        response = requests.get(url, headers=headers, params=params)

        print("🌐 Status:", response.status_code)
        data = response.json()

        if not data.get("response"):
            print("⚠️ API retornou vazio")
            return []

        games = []

        for item in data["response"]:
            fixture = item["fixture"]
            teams = item["teams"]
            league = item["league"]

            games.append({
                "home": teams["home"]["name"],
                "away": teams["away"]["name"],
                "league": league["name"],
                "date": fixture["date"]
            })

        return games

    except Exception as e:
        print("❌ Erro API:", e)
        return []