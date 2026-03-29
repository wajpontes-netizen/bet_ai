import pandas as pd
import os
from xgboost import XGBClassifier
import joblib

PENDING_PATH = "data/pending_bets.csv"
DATASET_PATH = "data/dataset.csv"
MODEL_PATH = "model.pkl"

def update_dataset():

    if not os.path.exists(PENDING_PATH):
        print("⚠️ Sem dados novos")
        return

    try:
        df = pd.read_csv(PENDING_PATH)
    except:
        print("⚠️ Arquivo vazio")
        return

    if df.empty:
        print("⚠️ Sem linhas")
        return

    # SIMULA RESULTADO (depois ligamos API real)
    df["result"] = df["home_xg"] + df["away_xg"] > 2.5

    if os.path.exists(DATASET_PATH):
        old = pd.read_csv(DATASET_PATH)
        df = pd.concat([old, df])

    df.to_csv(DATASET_PATH, index=False)

    os.remove(PENDING_PATH)

    print("✅ Dataset atualizado")

def train_model():

    if not os.path.exists(DATASET_PATH):
        print("⚠️ Sem dataset")
        return

    df = pd.read_csv(DATASET_PATH)

    if len(df) < 50:
        print("⚠️ Poucos dados para treinar IA")
        return

    X = df[[
        "home_xg",
        "away_xg",
        "corners_mean",
        "odd"
    ]]

    y = df["result"]

    model = XGBClassifier()
    model.fit(X, y)

    joblib.dump(model, MODEL_PATH)

    print("🧠 IA treinada com sucesso")

# EXECUÇÃO
update_dataset()
train_model()