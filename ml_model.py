from sklearn.ensemble import RandomForestClassifier
import pandas as pd

model = RandomForestClassifier(n_estimators=100)

def train():
    df = pd.read_csv("data/historico.csv")

    X = df[["xg_total", "odd"]]
    y = df["resultado"]

    model.fit(X, y)

def predict_bet(xg, odd):
    try:
        return model.predict_proba([[xg, odd]])[0][1]
    except:
        return 0.5