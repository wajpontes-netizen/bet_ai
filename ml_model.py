import numpy as np
import joblib
import os

MODEL_PATH = "model.pkl"

def predict_bet(home_xg, away_xg, corners, odd, extra):

    if not os.path.exists(MODEL_PATH):
        return 0.5

    try:
        model = joblib.load(MODEL_PATH)

        features = np.array([[
            home_xg,
            away_xg,
            corners,
            odd
        ]])

        prob = model.predict_proba(features)[0][1]

        return prob

    except:
        return 0.5