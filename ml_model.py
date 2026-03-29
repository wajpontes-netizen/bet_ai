import pandas as pd
from xgboost import XGBClassifier
import os

MODEL_FILE = "model.json"
DATA_FILE = "data/historico.csv"

def train_model():
    df = pd.read_csv(DATA_FILE)

    X = df[["xg_total", "odds"]]
    y = df["result"]

    model = XGBClassifier(use_label_encoder=False, eval_metric='logloss')
    model.fit(X, y)

    model.save_model(MODEL_FILE)

    return model

def load_model():
    model = XGBClassifier()
    model.load_model(MODEL_FILE)
    return model

def get_model():
    if not os.path.exists(MODEL_FILE):
        return train_model()
    return load_model()

def predict_bet(xg_total, odd):
    model = get_model()

    df = pd.DataFrame([[xg_total, odd]], columns=["xg_total", "odds"])
    prob = model.predict_proba(df)[0][1]

    return prob