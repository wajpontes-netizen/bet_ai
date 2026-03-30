import requests
from datetime import datetime
import os

API_KEY = os.getenv("c97416b1578113973cfa128a685cb6d1")

def get_games():
    url = "https://v3.football.api-sports.io/fixtures"

    today = datetime.utcnow().strftime("%Y-%m-%d")

    headers = {
        "x-apisports-key": API_KEY
    }

    params = {
        "date": today  # plano free
    }

    try:
        response = requests.get(url, headers=headers, params=params)

        print(f"🌐 Status: {response.status_code}")

        data = response.json()

        if "response" not in data or not data["response"]:
            print("⚠️ API sem jogos hoje")
            return []

        jogos = []

        for item in data["response"]:
            try:
                jogos.append({
                    "home": item["teams"]["home"]["name"],
                    "away": item["teams"]["away"]["name"],
                    "league": item["league"]["name"],
                    "date": item["fixture"]["date"]
                })
            except:
                continue

        return jogos

    except Exception as e:
        print("❌ Erro API:", e)
        return []