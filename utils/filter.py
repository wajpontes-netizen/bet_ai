def apply_filters(game, prob, odd):

    if prob < 0.52:
        return False

    if odd < 1.50 or odd > 3.00:
        return False

    return True