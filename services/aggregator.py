from services.api_football import get_games as api_football_games

def get_games():
    try:
        games = api_football_games()

        if not games:
            print("⚠️ Nenhum jogo da API")
            return []

        return games

    except Exception as e:
        print("Erro aggregator:", e)
        return []