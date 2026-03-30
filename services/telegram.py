import requests
import os

# =========================
# CONFIG
# =========================
TOKEN = os.getenv("8705713589:AAFdMxxFRHFrAB-3c_JQgnR96shxrnN3CqM")
CHAT_ID = os.getenv("1209904852")

# =========================
# ENVIAR MENSAGEM
# =========================
def enviar_telegram(mensagem):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

        payload = {
            "chat_id": CHAT_ID,
            "text": mensagem,
            "parse_mode": "HTML"
        }

        response = requests.post(url, json=payload)

        if response.status_code != 200:
            print("❌ Erro Telegram:", response.text)
        else:
            print("✅ Enviado para Telegram")

    except Exception as e:
        print("❌ Falha ao enviar:", e)