import pandas as pd
import random

def update_dataset():
    df = pd.read_csv("data/historico.csv")

    # simulação (depois você troca por resultados reais)
    new_data = {
        "xg_total": round(random.uniform(2.0, 3.5), 2),
        "odds": round(random.uniform(1.8, 2.1), 2),
        "result": random.choice([0, 1])
    }

    df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
    df.to_csv("data/historico.csv", index=False)

    print("Dataset atualizado!")

if __name__ == "__main__":
    update_dataset()