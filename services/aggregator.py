from services.api_football import get_games as api_football_games

def get_games():
    try:
        jogos = api_football_games()

        if not jogos:
            print("⚠️ API retornou vazio")
            return fallback_games()

        return jogos

    except Exception as e:
        print("Erro aggregator:", e)
        return fallback_games()


def fallback_games():
    print("⚠️ Usando fallback")

    return [
        {
            "home": "Flamengo",
            "away": "Palmeiras",
            "league": "Brasileirão",
            "date": "2026-03-29T16:30:00+00:00"
        },
        {
            "home": "Barcelona",
            "away": "Real Madrid",
            "league": "La Liga",
            "date": "2026-03-29T18:00:00+00:00"
        }
    ]