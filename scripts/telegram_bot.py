#!/usr/bin/env python3
"""
Bot de Telegram ALFRED 2brain (Chat & Ingesta - Costo $0)
Permite:
1. Conversar con ALFRED en vivo desde Telegram usando la API de Gemini (gratuita).
2. Guardar archivos, enlaces de YouTube/NotebookLM y notas directamente en raw/inbox/.

Configuración (.env):
TELEGRAM_BOT_TOKEN=123456789:ABCdef...
GEMINI_API_KEY=AIzaSy... (Obtenla gratis en https://aistudio.google.com)
"""

import os
import sys
import time
import json
import urllib.request
import urllib.parse
import datetime

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "raw")
INBOX_DIR = os.path.join(RAW_DIR, "inbox")
WIKI_DIR = os.path.join(BASE_DIR, "wiki")
ENV_FILE = os.path.join(BASE_DIR, "scripts", ".env")

os.makedirs(INBOX_DIR, exist_ok=True)

def load_env():
    config = {}
    if os.path.exists(ENV_FILE):
        with open(ENV_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    config[key.strip()] = val.strip()
                    
    # Override con vars de entorno
    if os.environ.get("TELEGRAM_BOT_TOKEN"):
        config["TELEGRAM_BOT_TOKEN"] = os.environ.get("TELEGRAM_BOT_TOKEN")
    if os.environ.get("GEMINI_API_KEY"):
        config["GEMINI_API_KEY"] = os.environ.get("GEMINI_API_KEY")
        
    return config

def telegram_api(token, method, data=None):
    url = f"https://api.telegram.org/bot{token}/{method}"
    try:
        if data:
            encoded_data = json.dumps(data).encode("utf-8")
            req = urllib.request.Request(url, data=encoded_data, headers={"Content-Type": "application/json"})
        else:
            req = urllib.request.Request(url)
            
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            return result
    except Exception as e:
        print(f"⚠️ Error en llamada API Telegram ({method}): {e}")
        return None

def read_dashboard_summary():
    dash_path = os.path.join(WIKI_DIR, "life-dashboard.md")
    if os.path.exists(dash_path):
        try:
            with open(dash_path, "r", encoding="utf-8") as f:
                content = f.read()
                return content[:2000] # Primeros 2000 caracteres del dashboard
        except Exception:
            pass
    return "Dashboard de Vida disponible en el sistema 2brain."

def call_gemini_alfred(gemini_key, user_text):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={gemini_key}"
    
    dashboard_ctx = read_dashboard_summary()
    system_prompt = f"""Tu nombre es ALFRED. Eres el Mayordomo de Vida y Asistente Ejecutivo Personal del usuario en su sistema 2brain.
Te diriges al usuario con el trato de 'Señor', actuando con máxima cortesía, profesionalismo, elegancia y eficiencia.

Conocimiento del 2brain del usuario (Resumen Dashboard):
{dashboard_ctx}

Responde de forma concisa, profesional y formal en español, como el fiel mayordomo ALFRED."""

    payload = {
        "system_instruction": {
            "parts": [{"text": system_prompt}]
        },
        "contents": [
            {
                "role": "user",
                "parts": [{"text": user_text}]
            }
        ]
    }

    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            res = json.loads(resp.read().decode("utf-8"))
            candidates = res.get("candidates", [])
            if candidates:
                parts = candidates[0].get("content", {}).get("parts", [])
                if parts:
                    return parts[0].get("text", "A su servicio, Señor.")
    except Exception as e:
        print(f"⚠️ Error al llamar a Gemini API: {e}")
        return f"Disculpe la molestia, Señor. Ocurrió una incidencia técnica conectando con el motor Gemini: {e}"
        
    return "A la orden, Señor. ¿En qué más puedo asistirle?"

def process_message(config, message):
    token = config.get("TELEGRAM_BOT_TOKEN")
    gemini_key = config.get("GEMINI_API_KEY")
    
    chat_id = message.get("chat", {}).get("id")
    text = message.get("text", "").strip()
    date = message.get("date")
    sender = message.get("from", {}).get("first_name", "Señor")
    
    timestamp_str = datetime.datetime.fromtimestamp(date).strftime("%Y-%m-%d %H:%M:%S") if date else datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if not text and "document" not in message:
        return

    # Comando /start o /help
    if text.startswith("/start") or text.startswith("/help"):
        help_msg = (
            "🎩 *ALFRED — Mayordomo Ejecutivo 2brain*\n\n"
            "¡A sus órdenes, Señor! Estoy listo para asistirlo. Puede utilizarme de dos maneras:\n\n"
            "💬 *1. Conversación y Consultas*:\n"
            "Simplemente escríbame cualquier pregunta, duda de su agenda, sermones o tareas y responderé como su asistente ejecutivo.\n\n"
            "📥 *2. Ingesta a 2brain*:\n"
            "• Envíeme cualquier enlace (YouTube, NotebookLM, artículos) o archivo.\n"
            "• Use el comando `/ingest <texto o url>` para forzar el guardado directo en su base de conocimiento."
        )
        telegram_api(token, "sendMessage", {"chat_id": chat_id, "text": help_msg, "parse_mode": "Markdown"})
        return

    # Ingesta forzada con /ingest
    is_explicit_ingest = text.startswith("/ingest")
    if is_explicit_ingest:
        text = text.replace("/ingest", "").strip()

    # Si es un enlace explícito (http:// o https://) o comando /ingest -> GUARDAR EN 2BRAIN
    if is_explicit_ingest or text.startswith("http://") or text.startswith("https://") or "document" in message:
        if "document" in message:
            doc = message["document"]
            file_name = doc.get("file_name", f"doc_{file_timestamp}")
            target_path = os.path.join(INBOX_DIR, file_name)
            file_id = doc.get("file_id")
            
            file_info = telegram_api(token, "getFile", {"file_id": file_id})
            if file_info and file_info.get("ok"):
                file_path_tg = file_info["result"].get("file_path")
                download_url = f"https://api.telegram.org/file/bot{token}/{file_path_tg}"
                try:
                    urllib.request.urlretrieve(download_url, target_path)
                    reply = f"✅ *Documento recibido*, Señor.\n📄 Guardado en `raw/inbox/{file_name}`."
                    telegram_api(token, "sendMessage", {"chat_id": chat_id, "text": reply, "parse_mode": "Markdown"})
                except Exception as ex:
                    telegram_api(token, "sendMessage", {"chat_id": chat_id, "text": f"❌ Error al descargar documento: {ex}"})
            return
            
        # Enlace o Nota de Ingesta
        filename = f"telegram_ingest_{file_timestamp}.md"
        target_path = os.path.join(INBOX_DIR, filename)
        
        content = f"""---
title: "Captura Telegram"
source: "Telegram (@Alfred_2brain_bot)"
sender: "{sender}"
created: "{timestamp_str}"
status: "pending_synthesis"
---

# Captura desde Telegram

**Fecha**: {timestamp_str}  
**Remitente**: {sender}  

### Contenido Capturado:
{text}
"""
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(content)
            
        reply = f"📥 *Guardado en 2brain*, Señor.\n📄 `raw/inbox/{filename}`\n🕒 {timestamp_str}"
        telegram_api(token, "sendMessage", {"chat_id": chat_id, "text": reply, "parse_mode": "Markdown"})
        return

    # De lo contrario -> MODO CONVERSACIÓN CON ALFRED (GEMINI API)
    if gemini_key and gemini_key != "TU_GEMINI_KEY_AQUI":
        # Indicar que ALFRED está escribiendo...
        telegram_api(token, "sendChatAction", {"chat_id": chat_id, "action": "typing"})
        response = call_gemini_alfred(gemini_key, text)
        telegram_api(token, "sendMessage", {"chat_id": chat_id, "text": response})
    else:
        # Fallback sin Gemini API Key
        reply = (
            f"A sus órdenes, Señor {sender}. He recibido su mensaje:\n\n"
            f"'{text}'\n\n"
            "💡 *Nota de ALFRED*: Para activar mis respuestas inteligentes completas por Telegram, por favor coloque su `GEMINI_API_KEY` en el archivo `scripts/.env` (es 100% gratuita en https://aistudio.google.com)."
        )
        telegram_api(token, "sendMessage", {"chat_id": chat_id, "text": reply, "parse_mode": "Markdown"})

def main():
    print("========================================================")
    print("   ALFRED 2brain - Bot de Telegram (Chat & Ingesta)")
    print("========================================================")
    
    config = load_env()
    token = config.get("TELEGRAM_BOT_TOKEN")
    gemini_key = config.get("GEMINI_API_KEY")
    
    if not token or token == "TU_TOKEN_AQUI":
        print("❌ Error: No se encontró el TELEGRAM_BOT_TOKEN.")
        print(f"📌 Por favor configúrelo en: {ENV_FILE}")
        sys.exit(1)
        
    print(f"🤖 Bot de Telegram activo con token: {token[:10]}...")
    if gemini_key and gemini_key != "TU_GEMINI_KEY_AQUI":
        print("🧠 Integración con Gemini API (Chat de ALFRED): ACTIVADA")
    else:
        print("ℹ️ Integración con Gemini API: Pendiente (Agregue GEMINI_API_KEY en .env)")
        
    print("📡 Escuchando mensajes entrantes en tiempo real... (Ctrl+C para salir)\n")
    
    offset = None
    try:
        while True:
            params = {"timeout": 20}
            if offset:
                params["offset"] = offset
                
            updates = telegram_api(token, "getUpdates", params)
            if updates and updates.get("ok"):
                for update in updates.get("result", []):
                    offset = update["update_id"] + 1
                    if "message" in update:
                        process_message(config, update["message"])
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n👋 Bot de Telegram detenido por el usuario.")

if __name__ == "__main__":
    main()
