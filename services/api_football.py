import requests

API_KEY = "92e513a4009536a16df3603b9fff54d0"

def get_games():
    url = "https://v3.football.api-sports.io/fixtures?next=20"

    headers = {
        "x-apisports-key": API_KEY
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)

        print("🌐 Status:", response.status_code)
        print("📦 Resposta RAW:", response.text[:500])  # DEBUG REAL

        if response.status_code != 200:
            print("❌ Erro na API")
            return fallback_games()

        data = response.json()

        if not data.get("response"):
            print("⚠️ API retornou vazio")
            return fallback_games()

        jogos = []

        for item in data["response"]:
            try:
                jogo = {
                    "home": item["teams"]["home"]["name"],
                    "away": item["teams"]["away"]["name"],
                    "league": item["league"]["name"],
                    "date": item["fixture"]["date"]
                }
                jogos.append(jogo)
            except Exception as e:
                print("⚠️ Erro ao processar jogo:", e)
                continue

        print(f"✅ {len(jogos)} jogos carregados")

        return jogos

    except Exception as e:
        print("❌ Erro geral API:", e)
        return fallback_games()


# 🔥 FALLBACK (nunca deixa o sistema parar)
def fallback_games():
    print("⚠️ Usando fallback de jogos")

    return [
        {
            "home": "Flamengo",
            "away": "Palmeiras",
            "league": "Brasileirão",
            "date": "2026-03-29T16:30:00"
        },
        {
            "home": "Barcelona",
            "away": "Real Madrid",
            "league": "La Liga",
            "date": "2026-03-29T18:00:00"
        },
        {
            "home": "Manchester City",
            "away": "Liverpool",
            "league": "Premier League",
            "date": "2026-03-29T17:00:00"
        }
    ]