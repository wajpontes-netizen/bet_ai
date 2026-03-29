import random

def get_extra_stats(game):

    # simulação (depois liga com API real)
    return {
        "home_goals_avg": random.uniform(1, 2.5),
        "away_goals_avg": random.uniform(1, 2.5),
        "home_conceded_avg": random.uniform(0.8, 2),
        "away_conceded_avg": random.uniform(0.8, 2),
        "home_form": random.uniform(0.3, 0.9),
        "away_form": random.uniform(0.3, 0.9),
        "shots_home": random.randint(8, 18),
        "shots_away": random.randint(8, 18),
    }