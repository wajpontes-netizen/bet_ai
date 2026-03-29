import numpy as np
from scipy.stats import poisson
import os
import time
import pandas as pd

from config import VALUE_THRESHOLD
from services.api import get_games
from utils.filter import apply_filters
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
    return sum(matrix[i][j] for i in range(len(matrix)) for j in range(len(matrix)) if i + j > 2.5)

def corners_over(mean, line):
    return 1 - poisson.cdf(line, mean)

def value(prob, odd):
    return prob - (1 / odd)

# -----------------------------
# EXECUÇÃO
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

            linha_cantos = max(7.5, round(g["corners_mean"]) - 0.5)
            corners = corners_over(g["corners_mean"], linha_cantos)

            bets = {
                "Over 2.5 Gols": (over, g["odds"].get("over25", 0)),
                f"Over {linha_cantos} Cantos": (corners, 1.90)
            }

            for name, (prob_modelo, odd) in bets.items():

                if odd == 0:
                    continue

                try:
                    ml_prob_raw = predict_bet(
                        g["home_xg"],
                        g["away_xg"],
                        g["corners_mean"],
                        odd
                    )
                except:
                    ml_prob_raw = 0.5

                ml_prob = (prob_modelo * 0.8) + (ml_prob_raw * 0.2)

                val = value(ml_prob, odd)

                print(f"📊 Prob: {round(ml_prob,2)} | Odd: {odd} | Value: {round(val,3)}")

                if val > 0.005 and ml_prob > 0.50:

                    print("✅ Aposta aprovada")

                    # salva aposta
                    new_row = pd.DataFrame([{
                        "match": g["match"],
                        "league": g["league"],
                        "home_xg": g["home_xg"],
                        "away_xg": g["away_xg"],
                        "corners_mean": g["corners_mean"],
                        "odd": odd,
                        "date": g.get("date", ""),
                        "market": name
                    }])

                    if os.path.exists(PENDING_PATH):
                        new_row.to_csv(PENDING_PATH, mode='a', header=False, index=False)
                    else:
                        new_row.to_csv(PENDING_PATH, index=False)

                    all_bets.append({
                        "jogo": g["match"],
                        "liga": g["league"],
                        "mercado": name,
                        "prob": ml_prob,
                        "odd": odd,
                        "value": val,
                        "data": g.get("date", "N/A")
                    })

        except Exception as e:
            print(f"Erro: {e}")
            continue

    if not all_bets:
        print("\n⚠️ Nenhuma aposta encontrada")
    else:
        all_bets = sorted(all_bets, key=lambda x: x["value"], reverse=True)[:5]

        for bet in all_bets:
            msg = f"""
🔥 VALUE BET

🏆 {bet['jogo']}
🕒 {bet['data']}
📊 {bet['mercado']}
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


# LOOP
if __name__ == "__main__":
    while True:
        print("\n🚀 Rodando...")
        run()
        time.sleep(3600)