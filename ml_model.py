import os
import joblib
import numpy as np

MODEL_PATH = "model.pkl"

# -----------------------------
# PREVISÃO
# -----------------------------
def predict_bet(home_xg, away_xg, corners_mean, odd, extra):

    try:
        model = joblib.load(MODEL_PATH)

        X = np.array([[home_xg, away_xg, corners_mean, odd]])
        prob = model.predict_proba(X)[0][1]

        return float(prob)

    except:
        # fallback inteligente (melhor que aleatório)
        base = (home_xg + away_xg) / 3

        # ajuste por cantos
        base += (corners_mean - 9) * 0.02

        # ajuste por odd
        if odd > 2:
            base += 0.03

        return min(max(base, 0.45), 0.70)


# -----------------------------
# FILTRO ANTI-RED (ESSENCIAL)
# -----------------------------
def risk_filter(prob, odd):

    # probabilidade mínima real
    if prob < 0.50:
        return False

    # odds ruins
    if odd < 1.75 or odd > 3.20:
        return False

    # valor esperado forte
    val = prob - (1 / odd)

    if val < 0.05:
        return False

    return True


# -----------------------------
# TREINAMENTO AUTOMÁTICO
# -----------------------------
def retrain():

    import pandas as pd

    if not os.path.exists("data/results.csv"):
        print("⚠️ Sem dados para treinar")
        return

    df = pd.read_csv("data/results.csv")

    if len(df) < 50:
        print("⚠️ Poucos dados para treinar IA")
        return

    X = df[["home_xg", "away_xg", "corners_mean", "odd"]]
    y = df["result"].apply(lambda x: 1 if x == "WIN" else 0)

    # peso maior para odds boas
    df["weight"] = df["odd"].apply(lambda x: 1.3 if x > 2 else 1)

    from xgboost import XGBClassifier

    model = XGBClassifier(
        n_estimators=150,
        max_depth=4,
        learning_rate=0.05,
        subsample=0.8
    )

    model.fit(X, y, sample_weight=df["weight"])

    joblib.dump(model, MODEL_PATH)

    print("🧠 IA treinada com dados reais")