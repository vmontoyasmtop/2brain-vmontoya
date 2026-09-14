#!/usr/bin/env python3
"""
Bot de Telegram de Ingesta ALFRED 2brain (Costo $0)
Escucha mensajes de Telegram (notas de texto, enlaces de YouTube/NotebookLM, archivos)
y los guarda en raw/inbox/ para sintetizarlos en 2brain.

Configuración:
1. Cree su bot en Telegram buscando a @BotFather y enviando /newbot
2. Guarde su TOKEN en el archivo scripts/.env o variable de entorno TELEGRAM_BOT_TOKEN
3. Ejecute: python scripts/telegram_bot.py
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
ENV_FILE = os.path.join(BASE_DIR, "scripts", ".env")

os.makedirs(INBOX_DIR, exist_ok=True)

def get_token():
    # 1. Variable de entorno
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if token:
        return token.strip()
        
    # 2. Archivo scripts/.env
    if os.path.exists(ENV_FILE):
        with open(ENV_FILE, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("TELEGRAM_BOT_TOKEN="):
                    return line.split("=", 1)[1].strip()
    return None

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

def process_message(token, message):
    chat_id = message.get("chat", {}).get("id")
    text = message.get("text", "")
    date = message.get("date")
    sender = message.get("from", {}).get("first_name", "Usuario")
    
    timestamp_str = datetime.datetime.fromtimestamp(date).strftime("%Y-%m-%d %H:%M:%S") if date else datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 1. Manejo de Enlaces o Texto
    if text:
        filename = f"telegram_note_{file_timestamp}.md"
        target_path = os.path.join(INBOX_DIR, filename)
        
        content = f"""---
title: "Nota / Enlace desde Telegram"
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

---
*Ingerido automáticamente por ALFRED 2brain Bot.*
"""
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(content)
            
        print(f"📥 Captura guardada en: {target_path}")
        
        # Confirmación por Telegram
        reply_text = f"✅ ¡Recibido y guardado en 2brain!\n📄 Archivo: {filename}\n🕒 {timestamp_str}\n\nALFRED lo procesará en breve."
        telegram_api(token, "sendMessage", {"chat_id": chat_id, "text": reply_text})
        
    # 2. Manejo de Documentos / Archivos
    elif "document" in message:
        doc = message["document"]
        file_name = doc.get("file_name", f"doc_{file_timestamp}")
        target_path = os.path.join(INBOX_DIR, file_name)
        file_id = doc.get("file_id")
        
        # Obtener URL de descarga del archivo desde Telegram
        file_info = telegram_api(token, "getFile", {"file_id": file_id})
        if file_info and file_info.get("ok"):
            file_path_tg = file_info["result"].get("file_path")
            download_url = f"https://api.telegram.org/file/bot{token}/{file_path_tg}"
            
            try:
                urllib.request.urlretrieve(download_url, target_path)
                print(f"📥 Documento descargado en: {target_path}")
                reply_text = f"✅ Documento '{file_name}' descargado en 2brain raw/inbox."
                telegram_api(token, "sendMessage", {"chat_id": chat_id, "text": reply_text})
            except Exception as ex:
                print(f"❌ Error al descargar documento: {ex}")

def main():
    print("========================================================")
    print("   ALFRED 2brain - Listener Bot de Telegram (Costo $0)")
    print("========================================================")
    
    token = get_token()
    if not token or token == "TU_TOKEN_AQUI":
        print("❌ Error: No se encontró el TOKEN del Bot de Telegram.")
        print("📌 Instrucciones:")
        print(" 1. Habla con @BotFather en Telegram y escribe /newbot")
        print(f" 2. Guarda tu token en: {ENV_FILE}")
        print("    Ejemplo de contenido en .env:")
        print("    TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz")
        sys.exit(1)
        
    print(f"🤖 Bot conectado con token: {token[:10]}...")
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
                        process_message(token, update["message"])
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n👋 Listener de Telegram detenido por el usuario.")

if __name__ == "__main__":
    main()
