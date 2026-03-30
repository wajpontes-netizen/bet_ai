import time
from datetime import datetime

from services.aggregator import get_games

# ==============================
# FILTRO INTELIGENTE PROFISSIONAL
# ==============================

def avaliar_aposta(prob, odd):
    value = prob * odd - 1

    if prob >= 0.63 and value >= 0.15:
        return "PREMIUM", value

    elif prob >= 0.57 and value >= 0.08:
        return "BOA", value

    elif prob >= 0.53 and value >= 0.03:
        return "RISCO", value

    return None, value

# ==============================
# SIMULAÇÃO DE IA (MELHORAR DEPOIS)
# ==============================

def calcular_probabilidade(jogo, mercado):
    # Aqui depois você liga com sua IA real
    base = 0.55

    if mercado == "over_gols":
        return base + 0.10
    elif mercado == "over_cantos":
        return base + 0.08

    return base

# ==============================
# LOOP PRINCIPAL
# ==============================

def main():
    print("🚀 Iniciando sistema profissional...")

    while True:
        jogos = get_games()

        print(f"\n📊 Jogos encontrados: {len(jogos)}")

        if not jogos:
            print("⚠️ Nenhum jogo disponível")
            print("⏳ Aguardando 1 hora...")
            time.sleep(3600)
            continue

        for jogo in jogos:
            try:
                time_str = jogo.get("time", "--:--")
                date_str = jogo.get("date", "--/--")
                home = jogo.get("home", "Time A")
                away = jogo.get("away", "Time B")
                league = jogo.get("league", "Liga")

                print(f"\n🔎 {home} vs {away} ({league}) - {date_str} {time_str}")

                # ==============================
                # MERCADOS
                # ==============================
                mercados = [
                    ("Over 2.5 Gols", "over_gols", 1.85),
                    ("Over 9.5 Cantos", "over_cantos", 1.90)
                ]

                for nome, key, odd in mercados:
                    prob = calcular_probabilidade(jogo, key)
                    tipo, value = avaliar_aposta(prob, odd)

                    print(f"➡️ {nome} | Prob: {prob:.2f} | Odd: {odd} | Value: {value:.3f}")

                    if tipo:
                        print(f"🔥 {tipo}")
                        print("🚀 Entrada recomendada")
                        print(f"🏆 {league}")
                        print(f"⚽ {home} vs {away}")
                        print(f"🕒 {date_str} {time_str}")
                        print(f"📊 Mercado: {nome}")
                        print(f"📈 Probabilidade: {int(prob*100)}%")
                        print(f"💰 Odd: {odd}")
                        print(f"📊 Value: {value:.3f}")
                    else:
                        print("❌ Filtro rejeitou")

            except Exception as e:
                print(f"Erro ao analisar jogo: {e}")

        print("\n⏳ Aguardando 1 hora...")
        time.sleep(3600)


if __name__ == "__main__":
    main()
