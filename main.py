import numpy as np
from scipy.stats import poisson
import os
import time

from config import BANKROLL, VALUE_THRESHOLD
from services.api import get_games
from utils.filter import apply_filters
from ml_model import predict_bet
from services.telegram import send

MAX_GOALS = 6

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
    return sum(matrix[i][j] for i in range(len(matrix)) for j in range(len(matrix)) if i + j > 2.5)

def corners_over(mean, line=9.5):
    return 1 - poisson.cdf(line, mean)

def value(prob, odd):
    return prob - (1 / odd)

def kelly(prob, odd):
    return ((prob * odd) - 1) / (odd - 1)

# -----------------------------
# FUNÇÃO PRINCIPAL
# -----------------------------
def run():
    games = get_games()

    print(f"\n📊 Jogos encontrados: {len(games)}")

    all_bets = []

    for g in games:
        try:
            print(f"\n🔎 Analisando: {g['match']} ({g['league']})")

            matrix = score_matrix(g["home_xg"], g["away_xg"])

            over = over25(matrix)
            corners = corners_over(g["corners_mean"])

            bets = {
                "Over 2.5 Gols": (over, g["odds"].get("over25", 0)),
                "Over Cantos": (corners, 1.90)
            }

            for name, (prob, odd) in bets.items():

                if odd == 0:
                    continue

                ml_prob = predict_bet(
                    g["home_xg"] + g["away_xg"],
                    odd
                )

                if not apply_filters(g, ml_prob, odd):
                    continue

                val = value(ml_prob, odd)

                if val > VALUE_THRESHOLD:
                    all_bets.append({
                        "jogo": g["match"],
                        "liga": g["league"],
                        "mercado": name,
                        "prob": ml_prob,
                        "odd": odd,
                        "value": val
                    })

        except Exception as e:
            print(f"Erro: {e}")
            continue

    # -----------------------------
    # RESULTADO
    # -----------------------------
    if not all_bets:
        print("\n⚠️ Nenhuma aposta encontrada")
    else:
        all_bets = sorted(all_bets, key=lambda x: x["value"], reverse=True)

        print("\n🔥 TOP APOSTAS:\n")

        for bet in all_bets[:5]:
            stake = kelly(bet["prob"], bet["odd"]) * BANKROLL * 0.25

            msg = f"""
🔥 VALUE BET

🏆 {bet['jogo']}
🏆 Liga: {bet['liga']}
📊 Mercado: {bet['mercado']}
📈 Prob IA: {round(bet['prob'],2)}
💰 Odd: {bet['odd']}
💎 Value: {round(bet['value'],2)}
💵 Stake: R${round(stake,2)}
"""

            print(msg)

            try:
                send(msg)
            except:
                pass

    # -----------------------------
    # AUTO-APRENDIZADO
    # -----------------------------
    print("\n🔄 Atualizando base...")
    os.system("python auto_update.py")


# -----------------------------
# LOOP 24H (NÚVEM)
# -----------------------------
if __name__ == "__main__":
    while True:
        print("\n🚀 Iniciando análise...")
        run()
        print("\n⏳ Aguardando 1 hora...")
        time.sleep(3600)