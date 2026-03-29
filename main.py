import numpy as np
from scipy.stats import poisson
import os
import time
import pandas as pd

from services.api import get_games
from services.stats import get_extra_stats
from ml_model import predict_bet
from services.telegram import send

MAX_GOALS = 6
PENDING_PATH = "data/pending_bets.csv"

# -----------------------------
# MODELOS
# -----------------------------
def score_matrix(home_xg, away_xg):
    matrix = np.zeros((MAX_GOALS, MAX_GOALS))
    for i in range(MAX_GOALS):
        for j in range(MAX_GOALS):
            matrix[i][j] = poisson.pmf(i, home_xg) * poisson.pmf(j, away_xg)
    return matrix

def over25(matrix):
    return sum(
        matrix[i][j]
        for i in range(len(matrix))
        for j in range(len(matrix))
        if i + j > 2.5
    )

def corners_over(mean, line):
    return 1 - poisson.cdf(line, mean)

def value(prob, odd):
    return prob - (1 / odd)

# -----------------------------
# FILTRO PROFISSIONAL
# -----------------------------
def filtro_profissional(prob, odd, liga):

    ligas_ruins = ["Friendly", "Youth", "Reserve"]

    if any(l in liga for l in ligas_ruins):
        return False

    if prob < 0.55:
        return False

    if odd < 1.70 or odd > 3.50:
        return False

    val = prob - (1 / odd)

    if val < 0.03:
        return False

    return True

# -----------------------------
# EXECUÇÃO
# -----------------------------
def run():
    print("\n🚀 Iniciando análise...")

    games = get_games()
    print(f"📊 Jogos encontrados: {len(games)}")

    all_bets = []

    for g in games:
        try:
            print(f"\n🔎 Analisando: {g['match']} ({g['league']})")

            # EXTRA DATA (multi-api futuro)
            extra = get_extra_stats(g)

            matrix = score_matrix(g["home_xg"], g["away_xg"])
            prob_over = over25(matrix)

            linha_cantos = max(7.5, round(g["corners_mean"]) - 0.5)
            prob_cantos = corners_over(g["corners_mean"], linha_cantos)

            mercados = {
                "Over 2.5 Gols": (prob_over, g["odds"].get("over25", 0)),
                f"Over {linha_cantos} Cantos": (prob_cantos, 1.90)
            }

            for nome, (prob_modelo, odd) in mercados.items():

                if odd == 0:
                    continue

                # IA AVANÇADA
                ml_prob = predict_bet(
                    g["home_xg"],
                    g["away_xg"],
                    g["corners_mean"],
                    odd,
                    extra
                )

                # COMBINAÇÃO FINAL
                prob_final = (prob_modelo * 0.6) + (ml_prob * 0.4)

                val = value(prob_final, odd)

                print(f"📊 Prob: {round(prob_final,2)} | Odd: {odd} | Value: {round(val,3)}")

                if not filtro_profissional(prob_final, odd, g["league"]):
                    print("⛔ Reprovado no filtro")
                    continue

                print("💰 VALUE BET ENCONTRADA")

                # SALVAR PARA IA
                new_row = pd.DataFrame([{
                    "match": g["match"],
                    "league": g["league"],
                    "home_xg": g["home_xg"],
                    "away_xg": g["away_xg"],
                    "corners_mean": g["corners_mean"],
                    "odd": odd,
                    "date": g.get("date", ""),
                    "market": nome
                }])

                if os.path.exists(PENDING_PATH):
                    new_row.to_csv(PENDING_PATH, mode='a', header=False, index=False)
                else:
                    new_row.to_csv(PENDING_PATH, index=False)

                all_bets.append({
                    "jogo": g["match"],
                    "liga": g["league"],
                    "mercado": nome,
                    "prob": prob_final,
                    "odd": odd,
                    "value": val,
                    "data": g.get("date", "")
                })

        except Exception as e:
            print(f"Erro: {e}")
            continue

    # -----------------------------
    # RESULTADO FINAL
    # -----------------------------
    if not all_bets:
        print("\n⚠️ Nenhuma aposta encontrada")
    else:
        all_bets = sorted(all_bets, key=lambda x: x["value"], reverse=True)

        print("\n🔥 TOP APOSTAS:\n")

        for bet in all_bets[:3]:
            msg = f"""
🔥 VALUE BET

🏆 {bet['jogo']}
🕒 {bet['data']}
🏆 Liga: {bet['liga']}
📊 Mercado: {bet['mercado']}
📈 Prob: {round(bet['prob'],2)}
💰 Odd: {bet['odd']}
💎 Value: {round(bet['value'],2)}
"""
            print(msg)

            try:
                send(msg)
            except:
                pass

    print("\n🔄 Atualizando base...")
    os.system("python auto_update.py")

# -----------------------------
# LOOP
# -----------------------------
if __name__ == "__main__":
    while True:
        run()
        print("\n⏳ Aguardando 1 hora...")
        time.sleep(3600)