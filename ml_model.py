import numpy as np
from xgboost import XGBClassifier

# modelo simples (depois vamos treinar melhor)
model = XGBClassifier()

def predict_bet(home_xg, away_xg, corners, odd, extra):

    try:
        features = np.array([[
            home_xg,
            away_xg,
            corners,

            extra["home_goals_avg"],
            extra["away_goals_avg"],
            extra["home_conceded_avg"],
            extra["away_conceded_avg"],
            extra["home_form"],
            extra["away_form"],
            extra["shots_home"],
            extra["shots_away"],

            odd
        ]])

        prob = model.predict_proba(features)[0][1]

    except:
        prob = 0.5

    return prob