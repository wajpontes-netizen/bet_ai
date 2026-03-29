import random

bank = 1000
bets = 100

roi = 0

for i in range(bets):

    prob = random.uniform(0.55, 0.65)
    odd = random.uniform(1.80, 2.10)

    value = prob - (1 / odd)

    if value > 0.05:
        stake = bank * 0.02

        win = random.random() < prob

        if win:
            profit = stake * (odd - 1)
            bank += profit
            roi += profit
        else:
            bank -= stake
            roi -= stake

print(f"Banca final: {round(bank,2)}")
print(f"Lucro: {round(roi,2)}")