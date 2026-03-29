import requests

def get_extra_stats(game):

    # fallback seguro
    try:
        return {
            "home_goals_avg": game.get("home_goals_avg", game["home_xg"]),
            "away_goals_avg": game.get("away_goals_avg", game["away_xg"]),
            "home_conceded_avg": game.get("away_xg", 1),
            "away_conceded_avg": game.get("home_xg", 1),
            "home_form": 0.6,
            "away_form": 0.5,
            "shots_home": 12,
            "shots_away": 10,
        }
    except:
        return {
            "home_goals_avg": 1.2,
            "away_goals_avg": 1.2,
            "home_conceded_avg": 1,
            "away_conceded_avg": 1,
            "home_form": 0.5,
            "away_form": 0.5,
            "shots_home": 10,
            "shots_away": 10,
        }