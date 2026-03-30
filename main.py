import time
from datetime import datetime
from services.aggregator import get_games
from services.telegram import enviar_telegram  # IMPORTANTE

# =========================
# CONFIG
# =========================
MIN_VALUE = 0.10
MIN_PROB = 0.58
TOP_MIN = 15
TOP_MAX = 20

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
# CLASSIFICAÇÃO
# =========================
def classificar_aposta(prob, value):
    if prob >= 0.63 and value >= 0.12:
        return "🔥 PREMIUM"
    elif prob >= 0.58 and value >= 0.10:
        return "✅ BOA"
    return None

# =========================
# IA SIMPLES
# =========================
def prever_probabilidade():
    import random
    return round(random.uniform(0.56, 0.66), 2)

# =========================
# LOOP PRINCIPAL
# =========================
def run():
    print("🚀 Sistema iniciado...")

    enviados = set()

    while True:
        jogos = get_games()
        print(f"📊 Jogos encontrados: {len(jogos)}")

        if not jogos:
            print("⚠️ Sem jogos")
            time.sleep(3600)
            continue

        apostas = []

        for jogo in jogos:
            home = jogo["home"]
            away = jogo["away"]
            league = jogo["league"]
            data = formatar_data(jogo["date"])

            jogo_id = f"{home}_{away}_{data}"

            if jogo_id in enviados:
                continue

            mercados = [
                ("Over 2.5 Gols", 1.85),
                ("Over 9.5 Cantos", 1.90)
            ]

            for nome, odd in mercados:
                prob = prever_probabilidade()
                value = calcular_value(prob, odd)

                if prob < MIN_PROB or value < MIN_VALUE:
                    continue  # 🔥 FILTRA ANTES (ESSENCIAL)

                tipo = classificar_aposta(prob, value)

                aposta = {
                    "id": jogo_id,
                    "liga": league,
                    "home": home,
                    "away": away,
                    "data": data,
                    "mercado": nome,
                    "prob": prob,
                    "odd": odd,
                    "value": value,
                    "tipo": tipo
                }

                apostas.append(aposta)

        # 🔥 ORDENA MELHORES
        apostas = sorted(apostas, key=lambda x: x["value"], reverse=True)

        # 🔥 LIMITA ENTRE 15 E 20
        apostas = apostas[:TOP_MAX]

        if len(apostas) < TOP_MIN:
            print("⚠️ Poucas apostas boas")
            time.sleep(3600)
            continue

        print(f"🔥 Enviando {len(apostas)} apostas...")

        for aposta in apostas:
            msg = f"""
🚀 OPORTUNIDADE
{aposta['tipo']}

🏆 {aposta['liga']}
⚽ {aposta['home']} vs {aposta['away']}
🕒 {aposta['data']}

📊 {aposta['mercado']}
📈 Prob: {int(aposta['prob']*100)}%
💰 Odd: {aposta['odd']}
📊 Value: {round(aposta['value'],3)}
"""

            enviar_telegram(msg)
            enviados.add(aposta["id"])

            time.sleep(2)  # evita flood

        print("⏳ Aguardando 1 hora...\n")
        time.sleep(3600)

# =========================
# START
# =========================
if __name__ == "__main__":
    run()