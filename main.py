import time
from datetime import datetime
from services.aggregator import get_games

MIN_PROB = 0.60
MIN_VALUE = 0.02

def calcular_probabilidade():
    # Simulação IA (depois ligamos com ML real)
    import random
    return round(random.uniform(0.55, 0.75), 2)

def analisar_jogo(jogo):
    home = jogo.get("home")
    away = jogo.get("away")
    league = jogo.get("league")
    date = jogo.get("date")

    try:
        dt = datetime.fromisoformat(date)
        horario = dt.strftime("%d/%m %H:%M")
    except:
        horario = "N/A"

    print(f"\n🔎 {home} vs {away} ({league}) - {horario}")

    mercados = [
        {"nome": "Over 2.5 Gols", "odd": 1.85},
        {"nome": "Over 9.5 Cantos", "odd": 1.90}
    ]

    for mercado in mercados:
        prob = calcular_probabilidade()
        odd = mercado["odd"]

        value = round((prob * odd) - 1, 3)

        print(f"➡️ {mercado['nome']} | Prob: {prob} | Odd: {odd} | Value: {value}")

        if prob >= MIN_PROB and value >= MIN_VALUE:
            print("✅ APOSTA BOA")

            print(f"""
🔥 OPORTUNIDADE

🏆 {league}
⚽ {home} vs {away}
🕒 {horario}

📊 Mercado: {mercado['nome']}
📈 Probabilidade: {int(prob*100)}%
💰 Odd: {odd}
📊 Value: {value}

🚀 Entrada recomendada
""")
        else:
            print("❌ Filtro rejeitou")

def main():
    print("🚀 Iniciando sistema profissional...")

    while True:
        jogos = get_games()

        print(f"\n📊 Jogos encontrados: {len(jogos)}")

        if not jogos:
            print("⚠️ Nenhum jogo disponível")
        else:
            for jogo in jogos:
                analisar_jogo(jogo)

        print("\n⏳ Aguardando 1 hora...\n")
        time.sleep(3600)

if __name__ == "__main__":
    main()