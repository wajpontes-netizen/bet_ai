import pandas as pd
import os

PENDING_PATH = "data/pending_bets.csv"
RESULTS_PATH = "data/results.csv"

def update_dataset():

    if not os.path.exists(PENDING_PATH):
        print("⚠️ Nenhuma aposta pendente")
        return

    try:
        df = pd.read_csv(PENDING_PATH)
    except:
        print("⚠️ Erro ao ler pending_bets")
        return

    if df.empty:
        print("⚠️ Arquivo vazio")
        return

    results = []

    for _, row in df.iterrows():

        # 🔥 SIMULAÇÃO (substituir depois por API real)
        import random
        result = random.choice(["WIN", "LOSS"])

        profit = (row["odd"] - 1) if result == "WIN" else -1

        results.append({
            **row,
            "result": result,
            "profit": profit
        })

    df_results = pd.DataFrame(results)

    # salvar histórico
    if os.path.exists(RESULTS_PATH):
        df_results.to_csv(RESULTS_PATH, mode='a', header=False, index=False)
    else:
        df_results.to_csv(RESULTS_PATH, index=False)

    # limpar pendentes
    os.remove(PENDING_PATH)

    print("✅ Resultados atualizados")


if __name__ == "__main__":
    update_dataset()