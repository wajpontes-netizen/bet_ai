def apply_filters(game, prob, odd):

    # Probabilidade mínima
    if prob < 0.55:
        return False

    # Odds dentro do intervalo ideal
    if odd < 1.70 or odd > 2.50:
        return False

    return True