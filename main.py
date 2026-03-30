import time
from datetime import datetime
from services.aggregator import get_games

# =========================
# CONFIG
# =========================
MIN_VALUE = 0.05
MIN_PROB = 0.54
TOP_N = 20

# =========================
# FORMATAR DATA
# =========================
def formatar_data(data_iso):
    try:
        dt = datetime.fromisoformat(data_iso.replace("Z", "+00:00"))
        return dt.strftime("%d/%m %H:%M")
    except:
        return data_iso

# =========================
# CALCULAR VALUE
# =========================
def calcular_value(prob, odd):
    return (prob * odd) - 1

# =========================
# CLASSIFICAR APOSTA
# =========================
def classificar_aposta(prob, value):
    if prob >= 0.62 and value >= 0.12:
        return "🔥 PREMIUM"
    elif prob >= 0.58 and value >= 0.08:
        return "✅ BOA"
    else:
        return "⚡ VALUE"

# =========================
# IA SIMPLES (placeholder)
# =========================
def prever_probabilidade():
    import random
    return round(random.uniform(0.54, 0.66), 2)

# =========================
# LOOP PRINCIPAL
# =========================
def run():
    print("🚀 Iniciando sistema profissional...")

    jogos_processados = set()

    while True:
        jogos = get_games()

        print(f"\n📊 Jogos encontrados: {len(jogos)}")

        if not jogos:
            print("⚠️ Nenhum jogo disponível")
            time.sleep(3600)
            continue

        apostas_boas = []

        for jogo in jogos:
            home = jogo["home"]
            away = jogo["away"]
            league = jogo["league"]
            date_str = jogo["date"]

            id_jogo = f"{home}_{away}_{date_str}"

            # 🚫 evitar duplicados
            if id_jogo in jogos_processados:
                continue
            jogos_processados.add(id_jogo)

            data_formatada = formatar_data(date_str)

            # =========================
            # MERCADOS (MAIS VOLUME)
            # =========================
            mercados = [
                ("Over 2.5 Gols", 1.85),
                ("Over 1.5 Gols", 1.35),
                ("Ambas Marcam", 1.75),
                ("Over 9.5 Cantos", 1.90)
            ]

            for nome, odd in mercados:
                prob = prever_probabilidade()
                value = calcular_value(prob, odd)

                print(f"➡️ {nome} | Prob: {prob} | Odd: {odd} | Value: {round(value,3)}")

                # ✅ FILTRO REAL (AGORA FUNCIONA)
                if prob >= MIN_PROB and value >= MIN_VALUE:
                    tipo = classificar_aposta(prob, value)

                    apostas_boas.append({
                        "liga": league,
                        "home": home,
                        "away": away,
                        "data": data_formatada,
                        "mercado": nome,
                        "prob": prob,
                        "odd": odd,
                        "value": value,
                        "tipo": tipo
                    })

        # =========================
        # TOP PICKS
        # =========================
        apostas_boas = sorted(apostas_boas, key=lambda x: x["value"], reverse=True)
        top_apostas = apostas_boas[:TOP_N]

        if not top_apostas:
            print("\n⚠️ Nenhuma aposta encontrada")
        else:
            print("\n🔥 TOP ENTRADAS DO DIA:\n")

            for aposta in top_apostas:
                print("🚀 OPORTUNIDADE")
                print(f"{aposta['tipo']}")
                print(f"🏆 {aposta['liga']}")
                print(f"⚽ {aposta['home']} vs {aposta['away']}")
                print(f"🕒 {aposta['data']}")
                print(f"📊 {aposta['mercado']}")
                print(f"📈 Probabilidade: {int(aposta['prob']*100)}%")
                print(f"💰 Odd: {aposta['odd']}")
                print(f"📊 Value: {round(aposta['value'],3)}")
                print("-" * 30)

        print("\n⏳ Aguardando 1 hora...\n")
        time.sleep(3600)

# =========================
# START
# =========================
if __name__ == "__main__":
    run()