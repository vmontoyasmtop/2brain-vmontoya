#!/usr/bin/env python3
"""
Script helper para registrar o eliminar el Webhook de ALFRED en Telegram.

Uso:
  python manage_webhook.py set <URL_DEL_WORKER>
  python manage_webhook.py info
  python manage_webhook.py delete
"""

import sys
import os
import json
import urllib.request

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENV_FILE = os.path.join(BASE_DIR, "scripts", ".env")

def load_token():
    if os.path.exists(ENV_FILE):
        with open(ENV_FILE, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("TELEGRAM_BOT_TOKEN="):
                    return line.split("=", 1)[1].strip()
    return os.environ.get("TELEGRAM_BOT_TOKEN")

def call_tg(token, method, data=None):
    url = f"https://api.telegram.org/bot{token}/{method}"
    if data:
        req = urllib.request.Request(url, data=json.dumps(data).encode("utf-8"), headers={"Content-Type": "application/json"})
    else:
        req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))

def main():
    token = load_token()
    if not token or token == "TU_TELEGRAM_TOKEN_AQUI":
        print("❌ Error: No se encontró TELEGRAM_BOT_TOKEN en scripts/.env")
        sys.exit(1)

    cmd = sys.argv[1] if len(sys.argv) > 1 else "info"

    if cmd == "set":
        if len(sys.argv) < 3:
            print("Uso: python manage_webhook.py set https://alfred-2brain-bot.<tu-subdominio>.workers.dev")
            sys.exit(1)
        webhook_url = sys.argv[2]
        res = call_tg(token, "setWebhook", {"url": webhook_url, "allowed_updates": ["message"]})
        print(f"🔗 Registrando Webhook ({webhook_url}):", res)
    elif cmd == "delete":
        res = call_tg(token, "deleteWebhook")
        print("🗑️ Webhook Eliminado (Modo Polling activo):", res)
    else:
        res = call_tg(token, "getWebhookInfo")
        print("ℹ️ Estado del Webhook:", json.dumps(res, indent=2))

if __name__ == "__main__":
    main()
