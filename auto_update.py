import pandas as pd
import os

DATASET_PATH = "dataset.csv"
PENDING_PATH = "pending_bets.csv"

def update_dataset():
    print("📊 Atualizando dataset...")

    # Verifica se arquivo existe
    if not os.path.exists(PENDING_PATH):
        print("⚠️ pending_bets não existe")
        return

    # Verifica se está vazio
    if os.stat(PENDING_PATH).st_size == 0:
        print("⚠️ pending_bets vazio")
        return

    try:
        df_pending = pd.read_csv(PENDING_PATH)

        if df_pending.empty:
            print("⚠️ Sem dados no pending")
            return

        # Criar dataset se não existir
        if not os.path.exists(DATASET_PATH):
            df_pending.to_csv(DATASET_PATH, index=False)
        else:
            df_dataset = pd.read_csv(DATASET_PATH)
            df_final = pd.concat([df_dataset, df_pending])
            df_final.to_csv(DATASET_PATH, index=False)

        # Limpa pending
        open(PENDING_PATH, "w").close()

        print("✅ Dataset atualizado")

    except Exception as e:
        print("Erro ao atualizar dataset:", e)