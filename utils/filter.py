def apply_filters(game, prob, odd):

    # evitar jogos ruins
    if prob < 0.57:
        return False

    # evitar odds ruins
    if odd < 1.70 or odd > 2.20:
        return False

    # evitar jogos com pouco gol esperado
    if (game["home_xg"] + game["away_xg"]) < 2.4:
        return False

    return True