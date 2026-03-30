import pandas as pd
import os

PENDING_PATH = "data/pending_bets.csv"

def update_dataset():
    if not os.path.exists(PENDING_PATH):
        print("⚠️ Arquivo não existe")
        return

    if os.stat(PENDING_PATH).st_size == 0:
        print("⚠️ Arquivo vazio")
        return

    try:
        df = pd.read_csv(PENDING_PATH)

        if df.empty:
            print("⚠️ Sem dados")
            return

        print("📊 Atualizando dataset...")

    except Exception as e:
        print("Erro:", e)


if __name__ == "__main__":
    update_dataset()