def estimate_xg(goals_for, goals_against):
    attack = goals_for * 0.6
    defense = goals_against * 0.4
    return attack + defense