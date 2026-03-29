def filtro_profissional(prob, odd, liga):

    # evita ligas ruins
    ligas_ruins = ["Friendly", "Youth", "Reserve"]

    if any(l in liga for l in ligas_ruins):
        return False

    # probabilidade mínima
    if prob < 0.55:
        return False

    # odd mínima
    if odd < 1.40 or odd > 3.50:
        return False

    # VALUE mínimo (CRÍTICO)
    value = prob - (1 / odd)

    if value < 0.03:
        return False

    return True