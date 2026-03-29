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

            # 🎯 linha dinâmica de cantos
            linha_cantos = max(7.5, round(g["corners_mean"]) - 0.5)
            corners = corners_over(g["corners_mean"], linha_cantos)

            bets = {
                "Over 2.5 Gols": (over, g["odds"].get("over25", 0)),
                f"Over {linha_cantos} Cantos": (corners, 1.90)
            }

            for name, (prob_modelo, odd) in bets.items():

                print(f"\n➡️ Testando mercado: {name}")

                if odd == 0:
                    print("❌ Odd zerada")
                    continue

                # IA real (sem boost fake)
                try:
                    ml_prob_raw = predict_bet(
                        g["home_xg"] + g["away_xg"],
                        odd
                    )
                except Exception as e:
                    print(f"Erro na IA: {e}")
                    ml_prob_raw = 0.5

                # 🔥 combinação real
                ml_prob = (prob_modelo * 0.8) + (ml_prob_raw * 0.2)

                val = value(ml_prob, odd)

                print(f"📊 Prob Final: {round(ml_prob,2)} | Odd: {odd} | Value: {round(val,3)}")

                # FILTRO
                try:
                    if not apply_filters(g, ml_prob, odd):
                        print("⛔ Reprovado no filtro")
                        continue
                except Exception as e:
                    print(f"Erro no filtro: {e}")
                    continue

                # DECISÃO MAIS PROFISSIONAL
                if val > 0.02 and ml_prob > 0.52:
                    print("✅ Aposta aprovada")

                    all_bets.append({
                        "jogo": g["match"],
                        "liga": g["league"],
                        "mercado": name,
                        "prob": ml_prob,
                        "odd": odd,
                        "value": val,
                        "data": g.get("date", "N/A")
                    })
                else:
                    print("❌ Sem valor suficiente")

        except Exception as e:
            print(f"Erro geral: {e}")
            continue

    # -----------------------------
    # RESULTADOS
    # -----------------------------
    if not all_bets:
        print("\n⚠️ Nenhuma aposta encontrada")
    else:
        all_bets = sorted(all_bets, key=lambda x: x["value"], reverse=True)

        # 🔥 só TOP 5 (qualidade)
        all_bets = all_bets[:5]

        print("\n🔥 TOP APOSTAS:\n")

        for bet in all_bets:

            msg = f"""
🔥 VALUE BET

🏆 {bet['jogo']}
🕒 Horário: {bet['data']}
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

    # -----------------------------
    # AUTO UPDATE
    # -----------------------------
    print("\n🔄 Atualizando base...")
    os.system("python auto_update.py")


# -----------------------------
# LOOP 24H
# -----------------------------
if __name__ == "__main__":
    while True:
        print("\n🚀 Iniciando análise...")
        run()
        print("\n⏳ Aguardando 1 hora...")
        time.sleep(3600)