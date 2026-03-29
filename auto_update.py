import pandas as pd
import os
import random

PENDING_PATH = "data/pending_bets.csv"
HIST_PATH = "data/historico.csv"

def get_result():
    # TEMPORÁRIO (depois vamos usar API real)
    return random.choice([0, 1])

def update_dataset():

    if not os.path.exists(PENDING_PATH):
        print("Sem apostas pendentes")
        return

    df = pd.read_csv(PENDING_PATH)

    if df.empty:
        print("Nada para atualizar")
        return

    results = []

    for _, row in df.iterrows():
        result = get_result()

        results.append({
            "home_xg": row["home_xg"],
            "away_xg": row["away_xg"],
            "corners_mean": row["corners_mean"],
            "odd": row["odd"],
            "resultado": result
        })

    new_data = pd.DataFrame(results)

    if os.path.exists(HIST_PATH):
        new_data.to_csv(HIST_PATH, mode='a', header=False, index=False)
    else:
        new_data.to_csv(HIST_PATH, index=False)

    os.remove(PENDING_PATH)

    print("✅ Histórico atualizado!")

if __name__ == "__main__":
    update_dataset()