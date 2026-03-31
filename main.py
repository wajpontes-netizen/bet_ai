import time
from datetime import datetime, timedelta
from services.aggregator import get_games
from services.telegram import enviar_telegram

# =========================
# CONFIG
# =========================
TOP_MIN = 15
TOP_MAX = 20

LIGAS_BOAS = [
    "Premier League",
    "La Liga",
    "Serie A",
    "Bundesliga",
    "Ligue 1",
    "Brasileirão",
    "UEFA Champions League",
    "UEFA Europa League"
    "Sul-amaricano"
    "Libertadores"
]

# =========================
# FORMATAR DATA (MANAUS)
# =========================
def formatar_data(data_iso):
    try:
        dt = datetime.fromisoformat(data_iso.replace("Z", "+00:00"))

        # ajuste -4h (Manaus)
        dt = dt - timedelta(hours=4)

        return dt.strftime("%d/%m %H:%M")
    except:
        return data_iso

# =========================
# FILTRO TEMPO
# =========================
def jogo_valido(data_iso):
    try:
        dt = datetime.fromisoformat(data_iso.replace("Z", "+00:00"))
        agora = datetime.utcnow()

        minutos = (dt - agora).total_seconds() / 60

        return 20 <= minutos <= 300  # 20min até 5h
    except:
        return False

# =========================
# IA PROFISSIONAL
# =========================
def calcular_probabilidade_real(odd, league):
    prob = 1 / odd

    if league in LIGAS_BOAS:
        prob += 0.05
    else:
        prob -= 0.02

    if odd <= 1.85:
        prob += 0.03

    return round(min(max(prob, 0.50), 0.80), 2)

def calcular_value(prob, odd):
    return round((prob * odd) - 1, 3)

def calcular_score(prob, value):
    return round((prob * 0.7) + (value * 0.3), 3)

# =========================
# CLASSIFICAÇÃO
# =========================
def classificar_aposta(prob, value):
    if prob >= 0.65 and value >= 0.12:
        return "🔥 PREMIUM"
    elif prob >= 0.60 and value >= 0.08:
        return "✅ BOA"
    return "📊 PADRÃO"

# =========================
# LOOP PRINCIPAL
# =========================
def run():
    print("🚀 Sistema profissional iniciado...")

    enviados = set()

    while True:
        jogos = get_games()
        print(f"📊 Jogos encontrados: {len(jogos)}")

        if not jogos:
            print("⚠️ Sem jogos... tentando novamente em 30 min\n")
            time.sleep(1800)
            continue

        apostas = []

        for jogo in jogos:

            # 🔥 filtro de tempo
            if not jogo_valido(jogo["date"]):
                continue

            home = jogo["home"]
            away = jogo["away"]
            league = jogo["league"]
            data_formatada = formatar_data(jogo["date"])

            jogo_id = f"{home}_{away}_{data_formatada}"

            if jogo_id in enviados:
                continue

            mercados = [
                ("Over 2.5 Gols", 1.85),
                ("Over 9.5 Cantos", 1.90)
            ]

            for nome, odd in mercados:

                prob = calcular_probabilidade_real(odd, league)
                value = calcular_value(prob, odd)
                score = calcular_score(prob, value)

                # 🔥 filtro profissional
                if prob < 0.57:
                    continue

                if value < 0.05:
                    continue

                tipo = classificar_aposta(prob, value)

                apostas.append({
                    "id": jogo_id,
                    "liga": league,
                    "home": home,
                    "away": away,
                    "data": data_formatada,
                    "mercado": nome,
                    "prob": prob,
                    "odd": odd,
                    "value": value,
                    "score": score,
                    "tipo": tipo
                })

        # 🔥 ordena por score (IA)
        apostas = sorted(apostas, key=lambda x: x["score"], reverse=True)

        # 🔥 limita entre 15 e 20
        apostas = apostas[:TOP_MAX]

        if not apostas:
            print("⚠️ Nenhuma aposta encontrada\n")
            time.sleep(1800)
            continue

        if len(apostas) < TOP_MIN:
            print("⚠️ Poucas apostas, enviando mesmo assim...\n")

        print(f"🔥 Enviando {len(apostas)} apostas...\n")

        for aposta in apostas:
            msg = f"""
🚀 <b>OPORTUNIDADE</b>
{aposta['tipo']}

🏆 {aposta['liga']}
⚽ {aposta['home']} vs {aposta['away']}
🕒 {aposta['data']}

📊 {aposta['mercado']}
📈 Prob: {int(aposta['prob']*100)}%
💰 Odd: {aposta['odd']}
📊 Value: {aposta['value']}
"""

            enviar_telegram(msg)
            enviados.add(aposta["id"])
            time.sleep(2)

        print("⏳ Aguardando 1 hora...\n")
        time.sleep(3600)

# =========================
# START
# =========================
if __name__ == "__main__":
    run()