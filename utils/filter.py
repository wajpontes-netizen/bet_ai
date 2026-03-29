def apply_filters(game, prob, odd):

    if prob < 0.50:
        return False

    if odd < 1.40 or odd > 3.20:
        return False

    return True