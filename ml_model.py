import pandas as pd
from xgboost import XGBClassifier
import os

MODEL_PATH = "model.pkl"
DATA_PATH = "data/historico.csv"

# -----------------------------
# TREINAR MODELO
# -----------------------------
def train_model():
    if not os.path.exists(DATA_PATH):
        print("⚠️ Sem histórico para treinar IA")
        return None

    df = pd.read_csv(DATA_PATH)

    if len(df) < 20:
        print("⚠️ Poucos dados para treinar IA")
        return None

    X = df[["home_xg", "away_xg", "corners_mean", "odd"]]
    y = df["resultado"]

    model = XGBClassifier(
        n_estimators=100,
        max_depth=3,
        learning_rate=0.1,
        use_label_encoder=False,
        eval_metric="logloss"
    )

    model.fit(X, y)

    return model

# -----------------------------
# CARREGAR OU TREINAR
# -----------------------------
_model = None

def get_model():
    global _model

    if _model is None:
        _model = train_model()

    return _model

# -----------------------------
# PREVISÃO
# -----------------------------
def predict_bet(home_xg, away_xg, corners_mean, odd):
    model = get_model()

    if model is None:
        return 0.5  # fallback neutro

    X = pd.DataFrame([{
        "home_xg": home_xg,
        "away_xg": away_xg,
        "corners_mean": corners_mean,
        "odd": odd
    }])

    prob = model.predict_proba(X)[0][1]

    return float(prob)