import pandas as pd
import os
import random

PENDING_PATH = "data/pending_bets.csv"
HIST_PATH = "data/historico.csv"

# -----------------------------
# RESULTADO (TEMPORÁRIO)
# -----------------------------
def get_result():
    # ⚠️ depois vamos trocar por API real
    return random.choice([0, 1])

# -----------------------------
# ATUALIZAR DATASET
# -----------------------------
def update_dataset():

    # arquivo não existe
    if not os.path.exists(PENDING_PATH):
        print("📭 Sem apostas pendentes")
        return

    # tenta ler
    try:
        df = pd.read_csv(PENDING_PATH)
    except Exception as e:
        print(f"⚠️ Erro ao ler arquivo: {e}")
        return

    # arquivo vazio
    if df.empty:
        print("⚠️ Nenhuma aposta para atualizar")
        return

    print(f"📊 Atualizando {len(df)} apostas...")

    results = []

    for _, row in df.iterrows():
        try:
            result = get_result()

            results.append({
                "home_xg": row.get("home_xg", 0),
                "away_xg": row.get("away_xg", 0),
                "corners_mean": row.get("corners_mean", 0),
                "odd": row.get("odd", 0),
                "resultado": result
            })

        except Exception as e:
            print(f"Erro ao processar linha: {e}")
            continue

    # nada processado
    if not results:
        print("⚠️ Nenhum resultado gerado")
        return

    new_data = pd.DataFrame(results)

    # salva histórico
    try:
        if os.path.exists(HIST_PATH):
            new_data.to_csv(HIST_PATH, mode='a', header=False, index=False)
        else:
            new_data.to_csv(HIST_PATH, index=False)
    except Exception as e:
        print(f"Erro ao salvar histórico: {e}")
        return

    # remove pendentes
    try:
        os.remove(PENDING_PATH)
    except:
        pass

    print("✅ Histórico atualizado com sucesso!")

# -----------------------------
# EXECUÇÃO
# -----------------------------
if __name__ == "__main__":
    update_dataset()