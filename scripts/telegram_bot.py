#!/usr/bin/env python3
"""
Bot de Telegram ALFRED 2brain (Chat & Ingesta - Costo $0)
Permite:
1. Conversar con ALFRED en vivo desde Telegram usando la API de Gemini (gratuita).
2. Guardar archivos, enlaces de YouTube/NotebookLM, notas y NOTAS DE VOZ directamente en raw/inbox/.
3. Procesamiento avanzado de audio: validación MIME, detección de magic bytes, resguardo binario y sidecar Markdown.
4. Alta resiliencia con fallbacks de modelo (gemini-3.6-flash, gemini-3.5-flash, gemini-2.5-flash, gemini-1.5-flash) y reintentos ante timeouts de socket.

Configuración (.env):
TELEGRAM_BOT_TOKEN=123456789:ABCdef...
GEMINI_API_KEY=AIzaSy... (Obtenla gratis en https://aistudio.google.com)
"""

import os
import sys
import time
import json
import socket
import urllib.request
import urllib.parse
import urllib.error
import datetime

# Timeout por defecto para sockets globales (60 segundos)
socket.setdefaulttimeout(60)

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

# MIME types de audio soportados oficialmente por Gemini API
ALLOWED_AUDIO_MIMES = {
    "audio/ogg": ".ogg",
    "audio/mp3": ".mp3",
    "audio/mpeg": ".mp3",
    "audio/wav": ".wav",
    "audio/aac": ".aac",
    "audio/flac": ".flac",
    "audio/m4a": ".m4a",
    "audio/opus": ".ogg",
    "audio/webm": ".webm"
}

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
            
        with urllib.request.urlopen(req, timeout=60) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            return result
    except Exception as e:
        print(f"⚠️ Error en llamada API Telegram ({method}): {e}")
        return None

def detect_audio_format(raw_bytes, default_mime="audio/ogg"):
    """
    Inspecciona magic bytes del buffer de audio para validar y normalizar MIME type y extensión.
    """
    if not raw_bytes or len(raw_bytes) < 4:
        return default_mime, ".ogg"

    # Magic byte matching
    if raw_bytes.startswith(b"OggS"):
        return "audio/ogg", ".ogg"
    elif raw_bytes.startswith(b"RIFF") and raw_bytes[8:12] == b"WAVE":
        return "audio/wav", ".wav"
    elif raw_bytes.startswith(b"ID3") or raw_bytes[:2] in (b"\xff\xfb", b"\xff\xf3", b"\xff\xf2"):
        return "audio/mp3", ".mp3"
    elif raw_bytes.startswith(b"fLaC"):
        return "audio/flac", ".flac"
    elif raw_bytes[4:8] == b"ftyp" or raw_bytes.startswith(b"\xff\xf1") or raw_bytes.startswith(b"\xff\xf9"):
        return "audio/m4a", ".m4a"

    # Fallback normalizando default_mime
    clean_mime = default_mime.split(";")[0].strip().lower() if default_mime else "audio/ogg"
    
    mime_mapping = {
        "audio/oga": ("audio/ogg", ".ogg"),
        "audio/opus": ("audio/ogg", ".ogg"),
        "audio/mpeg": ("audio/mp3", ".mp3"),
        "audio/x-wav": ("audio/wav", ".wav"),
        "audio/wave": ("audio/wav", ".wav"),
        "audio/mp4": ("audio/m4a", ".m4a"),
        "audio/x-m4a": ("audio/m4a", ".m4a"),
    }
    
    if clean_mime in mime_mapping:
        return mime_mapping[clean_mime]
        
    ext = ALLOWED_AUDIO_MIMES.get(clean_mime, ".ogg")
    return clean_mime if clean_mime in ALLOWED_AUDIO_MIMES else "audio/ogg", ext

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

def call_gemini_alfred(gemini_key, user_text, audio_bytes=None, mime_type="audio/ogg"):
    dashboard_ctx = read_dashboard_summary()
    system_prompt = f"""Tu nombre es ALFRED. Eres el Mayordomo de Vida y Asistente Ejecutivo Personal del usuario en su sistema 2brain.
Te diriges al usuario con el trato de 'Señor', actuando con máxima cortesía, profesionalismo, elegancia y eficiencia.

Conocimiento del 2brain del usuario (Resumen Dashboard):
{dashboard_ctx}

Instrucciones para Notas de Voz y Audio:
- Si el mensaje contiene un archivo de audio o nota de voz, realiza una comprensión auditiva integral.
- Si el Señor solicita registrar una tarea, recordatorio o idea, confirma los detalles recibidos con total claridad.
- Mantén tus respuestas estructuradas, concisas y elegantes en español formal."""

    parts = []
    if audio_bytes:
        import base64
        b64_data = base64.b64encode(audio_bytes).decode("utf-8")
        parts.append({
            "inline_data": {
                "mime_type": mime_type,
                "data": b64_data
            }
        })
    
    if audio_bytes:
        if user_text:
            prompt_text = f"El Señor ha enviado una nota de voz acompañada del siguiente mensaje: '{user_text}'. Escuche el audio atentamente y responda a su solicitud con total elegancia y eficiencia."
        else:
            prompt_text = "Escuche con atención la nota de voz enviada por el Señor, identifique su consulta, orden o pensamiento, y responda con máxima cortesía y precisión como su fiel mayordomo ALFRED."
    else:
        prompt_text = user_text if user_text else "A sus órdenes, Señor."
        
    parts.append({"text": prompt_text})

    payload = {
        "system_instruction": {
            "parts": [{"text": system_prompt}]
        },
        "contents": [
            {
                "role": "user",
                "parts": parts
            }
        ]
    }

    # Modelos candidatos con fallback progresivo y reintentos resiliencia ante errores 500/503/429 y Socket Timeout
    candidate_models = ["gemini-3.6-flash", "gemini-3.5-flash", "gemini-2.5-flash", "gemini-1.5-flash"]
    last_error = None

    for model_name in candidate_models:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={gemini_key}"
        for attempt in range(3):
            try:
                req = urllib.request.Request(
                    url,
                    data=json.dumps(payload).encode("utf-8"),
                    headers={"Content-Type": "application/json"}
                )
                with urllib.request.urlopen(req, timeout=45) as resp:
                    res = json.loads(resp.read().decode("utf-8"))
                    candidates = res.get("candidates", [])
                    if candidates:
                        res_parts = candidates[0].get("content", {}).get("parts", [])
                        if res_parts:
                            return res_parts[0].get("text", "A su servicio, Señor.")
            except urllib.error.HTTPError as http_err:
                last_error = f"HTTP {http_err.code}: {http_err.reason}"
                print(f"⚠️ Reintento {attempt+1}/3 con modelo {model_name} debido a error HTTP ({http_err.code})")
                if http_err.code in (429, 404):
                    # Salta al siguiente modelo si es 429 (quota limit) o 404 (modelo no encontrado)
                    break
                time.sleep(1.5 * (attempt + 1))
            except (socket.timeout, urllib.error.URLError) as net_err:
                last_error = f"Timeout/Red: {net_err}"
                print(f"⚠️ Reintento {attempt+1}/3 con modelo {model_name} por socket timeout o problema de red")
                time.sleep(2.0 * (attempt + 1))
            except Exception as e:
                last_error = str(e)
                print(f"⚠️ Reintento {attempt+1}/3 con modelo {model_name} debido a: {e}")
                time.sleep(1.5 * (attempt + 1))
        
    return f"Disculpe la molestia, Señor. Ocurrió una saturación o inconformidad temporal en las llamadas a los modelos de Google Gemini: {last_error}"

def process_message(config, message):
    token = config.get("TELEGRAM_BOT_TOKEN")
    gemini_key = config.get("GEMINI_API_KEY")
    
    chat_id = message.get("chat", {}).get("id")
    text = message.get("text", "").strip()
    date = message.get("date")
    sender = message.get("from", {}).get("first_name", "Señor")
    
    timestamp_str = datetime.datetime.fromtimestamp(date).strftime("%Y-%m-%d %H:%M:%S") if date else datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    has_voice = "voice" in message
    has_audio = "audio" in message

    if not text and "document" not in message and not has_voice and not has_audio:
        return

    # Procesamiento de Notas de Voz / Audio con Gemini Multimodal
    if (has_voice or has_audio) and gemini_key and gemini_key != "TU_GEMINI_KEY_AQUI":
        audio_item = message.get("voice") or message.get("audio")
        file_id = audio_item.get("file_id")
        raw_mime = audio_item.get("mime_type", "audio/ogg" if has_voice else "audio/mp3")
        duration = audio_item.get("duration", 0)
        caption = message.get("caption", "").strip()
        
        telegram_api(token, "sendChatAction", {"chat_id": chat_id, "action": "record_voice"})
        
        file_info = telegram_api(token, "getFile", {"file_id": file_id})
        if file_info and file_info.get("ok"):
            file_path_tg = file_info["result"].get("file_path")
            download_url = f"https://api.telegram.org/file/bot{token}/{file_path_tg}"
            
            raw_audio = None
            for dl_attempt in range(3):
                try:
                    req_down = urllib.request.Request(download_url)
                    with urllib.request.urlopen(req_down, timeout=60) as resp_down:
                        raw_audio = resp_down.read()
                    break
                except Exception as dl_err:
                    print(f"⚠️ Reintento descarga de audio {dl_attempt+1}/3 debido a: {dl_err}")
                    time.sleep(1.5 * (dl_attempt + 1))
            
            if not raw_audio or len(raw_audio) == 0:
                telegram_api(token, "sendMessage", {"chat_id": chat_id, "text": "❌ Disculpe Señor, el archivo de audio recibido está vacío o expiró el tiempo de espera al descargarlo de Telegram."})
                return

            # Validar y normalizar MIME type y extensión con inspección de Magic Bytes
            clean_mime, file_ext = detect_audio_format(raw_audio, default_mime=raw_mime)
            
            try:
                # 1. Resguardo de archivo binario en raw/inbox
                prefix = "voice" if has_voice else "audio"
                audio_filename = f"{prefix}_{file_timestamp}{file_ext}"
                audio_full_path = os.path.join(INBOX_DIR, audio_filename)
                with open(audio_full_path, "wb") as f_aud:
                    f_aud.write(raw_audio)
                
                # 2. Procesar respuesta con Gemini Multimodal
                response = call_gemini_alfred(gemini_key, caption, audio_bytes=raw_audio, mime_type=clean_mime)
                
                # 3. Guardar nota sidecar de ingesta en raw/inbox
                markdown_filename = f"{prefix}_{file_timestamp}.md"
                markdown_full_path = os.path.join(INBOX_DIR, markdown_filename)
                sidecar_content = f"""---
title: "Nota de Voz ({sender})"
source: "Telegram (@Alfred_2brain_bot)"
sender: "{sender}"
created: "{timestamp_str}"
audio_file: "{audio_filename}"
mime_type: "{clean_mime}"
file_size_bytes: {len(raw_audio)}
duration_seconds: {duration}
status: "processed"
---

# Nota de Voz / Audio Ingestada

**Fecha**: {timestamp_str}  
**Remitente**: {sender}  
**Archivo**: `{audio_filename}` ({len(raw_audio)} bytes, {duration}s)  
**MIME Type**: `{clean_mime}`  

### Texto / Comentario Adjunto:
{caption if caption else "*(Sin comentario adjunto)*"}

### Respuesta de ALFRED:
{response}
"""
                with open(markdown_full_path, "w", encoding="utf-8") as f_md:
                    f_md.write(sidecar_content)

                # 4. Enviar respuesta al usuario por Telegram
                telegram_api(token, "sendMessage", {"chat_id": chat_id, "text": response})
                return
            except Exception as ex:
                telegram_api(token, "sendMessage", {"chat_id": chat_id, "text": f"❌ Disculpe Señor, ocurrió una incidencia al procesar la nota de voz: {ex}"})
                return

    # Comando /ticket o /helpdesk
    if text.startswith("/ticket") or text.startswith("/helpdesk"):
        parts = text.split(maxsplit=1)
        subcommand = parts[1] if len(parts) > 1 else ""
        
        if subcommand.startswith("create"):
            # /ticket create Título del ticket | Descripción
            ticket_data = subcommand.replace("create", "", 1).strip()
            title = ticket_data
            desc = "Registrado desde Telegram por " + sender
            if "|" in ticket_data:
                title, desc = ticket_data.split("|", 1)
                
            from masterhub_helpdesk import create_ticket
            create_ticket(title.strip(), desc.strip())
            reply = f"🛠️ *Ticket de Helpdesk Creado*, Señor:\n📌 *Título*: {title.strip()}\n📝 *Descripción*: {desc.strip()}"
            telegram_api(token, "sendMessage", {"chat_id": chat_id, "text": reply, "parse_mode": "Markdown"})
            return
        else:
            # Listar o consultar por defecto
            from masterhub_helpdesk import make_request
            res = make_request("tickets?limit=5")
            if res and isinstance(res, list):
                ticket_lines = [f"• *[{t.get('status')}]* #{t.get('id')[:6]}: {t.get('title')}" for t in res[:5]]
                reply = "🛠️ *Últimos Tickets en MasterHub Helpdesk*:\n\n" + "\n".join(ticket_lines)
            elif res and isinstance(res, dict) and "items" in res:
                ticket_lines = [f"• *[{t.get('status')}]* #{t.get('id')[:6]}: {t.get('title')}" for t in res.get("items", [])[:5]]
                reply = "🛠️ *Últimos Tickets en MasterHub Helpdesk*:\n\n" + "\n".join(ticket_lines)
            else:
                reply = "🛠️ *MasterHub Helpdesk*: Servidor local no detectado en `http://localhost:3000`. Inicie el proyecto en `Desktop/MasterHub` para consultar tickets."
                
            telegram_api(token, "sendMessage", {"chat_id": chat_id, "text": reply, "parse_mode": "Markdown"})
            return

    # Comando /start o /help
    if text.startswith("/start") or text.startswith("/help"):
        help_msg = (
            "🎩 *ALFRED — Mayordomo Ejecutivo 2brain*\n\n"
            "¡A sus órdenes, Señor! Estoy listo para asistirlo. Puede utilizarme de las siguientes maneras:\n\n"
            "💬 *1. Conversación y Notas de Voz*:\n"
            "• Escríbame cualquier mensaje de texto o **envíeme notas de voz directamente**.\n"
            "• Escucharé y responderé sus solicitudes de voz en tiempo real con resguardo automático en `raw/inbox/`.\n\n"
            "🛠️ *2. Gestión de Tickets Helpdesk*:\n"
            "• `/ticket` — Ver últimos tickets de MasterHub.\n"
            "• `/ticket create Título | Descripción` — Crear nuevo ticket en Helpdesk.\n\n"
            "📥 *3. Ingesta a 2brain*:\n"
            "• Envíeme cualquier enlace (YouTube, NotebookLM, artículos) o archivo.\n"
            "• Use el comando `/ingest <texto o url>` para guardado directo."
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
