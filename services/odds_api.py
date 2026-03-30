import requests

API_KEY = "c97416b1578113973cfa128a685cb6d1"

def get_odds(match_name):

    url = f"https://api.the-odds-api.com/v4/sports/soccer/odds/?apiKey={API_KEY}&regions=eu&markets=totals"

    try:
        res = requests.get(url)
        data = res.json()

        for game in data:
            if match_name.lower() in game["home_team"].lower():

                for bookmaker in game["bookmakers"]:
                    for market in bookmaker["markets"]:
                        if market["key"] == "totals":

                            for outcome in market["outcomes"]:
                                if outcome["name"] == "Over" and outcome["point"] == 2.5:
                                    return outcome["price"]

    except:
        pass

    return None