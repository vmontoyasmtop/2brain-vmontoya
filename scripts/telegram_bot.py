#!/usr/bin/env python3
"""
Bot de Telegram ALFRED 2brain (Chat & Ingesta - Costo $0)
Permite:
1. Conversar con ALFRED en vivo desde Telegram usando la API de Gemini (gratuita).
2. Guardar archivos, enlaces de YouTube/NotebookLM, notas y NOTAS DE VOZ directamente en raw/inbox/.
3. Procesamiento avanzado de audio: validación MIME, detección de magic bytes, resguardo binario y sidecar Markdown.
4. Alta resiliencia con fallbacks de modelo (gemini-3.6-flash, gemini-3.5-flash, gemini-2.5-flash, gemini-1.5-flash) y reintentos ante timeouts de socket.
5. Módulo ligero de Notificaciones Push Proactivas (Notification Worker): captura persistente de TELEGRAM_CHAT_ID, resumen matutino 07:30 AM y alertas 15 min antes de eventos agendados en life-dashboard.md.

Configuración (.env):
TELEGRAM_BOT_TOKEN=123456789:ABCdef...
GEMINI_API_KEY=AIzaSy... (Obtenla gratis en https://aistudio.google.com)
TELEGRAM_CHAT_ID=... (Capturado automáticamente)
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
import re
import threading

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

# Lock para escrituras seguras en .env desde hilos
env_lock = threading.Lock()

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

MONTH_MAP = {
    "ene": 1, "jan": 1,
    "feb": 2,
    "mar": 3,
    "abr": 4, "apr": 4,
    "may": 5,
    "jun": 6,
    "jul": 7,
    "ago": 8, "aug": 8,
    "sep": 9,
    "oct": 10,
    "nov": 11,
    "dic": 12, "dec": 12
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
    if os.environ.get("TELEGRAM_CHAT_ID"):
        config["TELEGRAM_CHAT_ID"] = os.environ.get("TELEGRAM_CHAT_ID")
        
    return config

def save_chat_id(chat_id, config):
    """
    Captura y guarda de forma persistente el TELEGRAM_CHAT_ID en .env al recibir cualquier mensaje o nota de voz.
    """
    if not chat_id:
        return
    str_chat_id = str(chat_id)
    if config.get("TELEGRAM_CHAT_ID") == str_chat_id:
        return
        
    config["TELEGRAM_CHAT_ID"] = str_chat_id
    
    with env_lock:
        lines = []
        found = False
        if os.path.exists(ENV_FILE):
            with open(ENV_FILE, "r", encoding="utf-8") as f:
                lines = f.readlines()
                
        new_lines = []
        for line in lines:
            if line.strip().startswith("TELEGRAM_CHAT_ID="):
                new_lines.append(f"TELEGRAM_CHAT_ID={str_chat_id}\n")
                found = True
            else:
                new_lines.append(line)
                
        if not found:
            if new_lines and not new_lines[-1].endswith("\n"):
                new_lines.append("\n")
            new_lines.append(f"# ID de chat capturado automáticamente para notificaciones push\nTELEGRAM_CHAT_ID={str_chat_id}\n")
            
        try:
            with open(ENV_FILE, "w", encoding="utf-8") as f:
                f.writelines(new_lines)
            print(f"✅ TELEGRAM_CHAT_ID={str_chat_id} capturado y guardado de forma persistente en {ENV_FILE}")
        except Exception as e:
            print(f"⚠️ Error al guardar TELEGRAM_CHAT_ID en .env: {e}")

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

def parse_upcoming_events_from_dashboard():
    """
    Parsea prioridades y eventos agendados con horario desde life-dashboard.md.
    """
    dash_path = os.path.join(WIKI_DIR, "life-dashboard.md")
    if not os.path.exists(dash_path):
        return []
        
    events = []
    now = datetime.datetime.now()
    current_year = now.year
    
    try:
        with open(dash_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            
        current_section = "General"
        for line in lines:
            line_str = line.strip()
            if line_str.startswith("### "):
                current_section = line_str.replace("### ", "").strip()
                continue
                
            if not line_str or line_str.startswith("---") or line_str.startswith("```"):
                continue

            # Evento con fecha específica: ej. 17-Sep 12:30 – 13:30 PM o 17-Sep 09:00 AM
            m_date = re.search(r'(\d{1,2})-(Ene|Feb|Mar|Abr|May|Jun|Jul|Ago|Sep|Oct|Nov|Dic|Jan|Apr|Aug|Dec)\s+(\d{1,2}):(\d{2})(?:\s*(?:–|-|a)\s*\d{1,2}:\d{2})?\s*(AM|PM)?', line_str, re.IGNORECASE)
            if m_date:
                day = int(m_date.group(1))
                mon_str = m_date.group(2).lower()
                month = MONTH_MAP.get(mon_str, now.month)
                hour = int(m_date.group(3))
                minute = int(m_date.group(4))
                ampm = m_date.group(5)
                
                if ampm:
                    ampm_upper = ampm.upper()
                    if ampm_upper == "PM" and hour < 12:
                        hour += 12
                    elif ampm_upper == "AM" and hour == 12:
                        hour = 0
                
                try:
                    event_dt = datetime.datetime(current_year, month, day, hour, minute)
                    clean_title = re.sub(r'^-?\s*\[[ xX]\]\s*', '', line_str)
                    clean_title = clean_title.replace("**", "").replace("[[", "").replace("]]", "")
                    
                    event_id = f"{event_dt.strftime('%Y%m%d_%H%M')}_{abs(hash(clean_title[:30]))}"
                    events.append({
                        "id": event_id,
                        "title": clean_title,
                        "datetime": event_dt,
                        "raw_time": f"{hour:02d}:{minute:02d}",
                        "section": current_section
                    })
                except ValueError:
                    pass
                continue

            # Bloque de tiempo recurrente (ej. 18:30 - 20:30 o 08:30 PM)
            m_time = re.search(r'(\d{1,2}):(\d{2})\s*(AM|PM)?', line_str, re.IGNORECASE)
            if m_time and any(k in line_str.lower() for k in ["desconexión", "deep work", "lunes a viernes", "sábados y domingos"]):
                hour = int(m_time.group(1))
                minute = int(m_time.group(2))
                ampm = m_time.group(3)
                if ampm:
                    ampm_upper = ampm.upper()
                    if ampm_upper == "PM" and hour < 12:
                        hour += 12
                    elif ampm_upper == "AM" and hour == 12:
                        hour = 0
                
                if "lunes a viernes" in line_str.lower() and now.weekday() >= 5:
                    continue
                if "sábados y domingos" in line_str.lower() and now.weekday() < 5:
                    continue

                event_dt = datetime.datetime(now.year, now.month, now.day, hour, minute)
                clean_title = re.sub(r'^-?\s*\[[ xX]\]\s*', '', line_str)
                clean_title = clean_title.replace("**", "").replace("[[", "").replace("]]", "")
                
                event_id = f"{event_dt.strftime('%Y%m%d_%H%M')}_{abs(hash(clean_title[:30]))}"
                events.append({
                    "id": event_id,
                    "title": clean_title,
                    "datetime": event_dt,
                    "raw_time": f"{hour:02d}:{minute:02d}",
                    "section": current_section
                })

    except Exception as e:
        print(f"⚠️ Error al parsear eventos de life-dashboard.md: {e}")

    return events

def read_latest_handover_from_log():
    """
    Lee el último registro de cierre/handover o la sección de actividad más reciente en wiki/log.md.
    """
    log_path = os.path.join(WIKI_DIR, "log.md")
    if not os.path.exists(log_path):
        return None
    try:
        with open(log_path, "r", encoding="utf-8") as f:
            content = f.read()

        sections = content.split("\n## ")
        if len(sections) > 1:
            for sec in reversed(sections[1:]):
                sec_lower = sec.lower()
                if "handover" in sec_lower or "cierre" in sec_lower or "resumen de logros" in sec_lower or "acciones realizadas" in sec_lower:
                    lines = sec.strip().split("\n")
                    header = lines[0].strip()
                    points = []
                    for l in lines[1:]:
                        l_str = l.strip()
                        if (l_str.startswith("- ") or l_str.startswith("* ")) and not l_str.startswith("- **Área"):
                            clean_l = re.sub(r'^[-\*\s]+', '', l_str)
                            clean_l = re.sub(r'\[\[([^\|\]]+\|)?([^\]]+)\]\]', r'\2', clean_l)
                            clean_l = clean_l.replace("**", "").strip()
                            if clean_l and not clean_l.startswith("Agentes Responsables"):
                                points.append(clean_l)
                        if len(points) >= 5:
                            break
                    if points:
                        return header, points
    except Exception as e:
        print(f"⚠️ Error leyendo cierre desde log.md: {e}")
    return None

def build_daily_morning_summary():
    """
    Construye el resumen ejecutivo diario de las 07:30 AM integrando el cierre anterior (log.md) y la agenda/prioridades (life-dashboard.md).
    """
    dash_path = os.path.join(WIKI_DIR, "life-dashboard.md")
    if not os.path.exists(dash_path):
        return "🎩 *ALFRED*: Buenos días, Señor. Hoy no se encontró el archivo Dashboard de Vida."

    sections = {}
    current_sec = "General"

    try:
        with open(dash_path, "r", encoding="utf-8") as f:
            for line in f:
                line_str = line.strip()
                if line_str.startswith("### "):
                    current_sec = line_str.replace("### ", "").strip()
                    if current_sec not in sections:
                        sections[current_sec] = []
                    continue
                    
                if line_str.startswith("- [ ]") or line_str.startswith("- [x]"):
                    is_pending = line_str.startswith("- [ ]")
                    clean_item = line_str[5:].strip()
                    clean_item = re.sub(r'\[\[([^\|\]]+\|)?([^\]]+)\]\]', r'\2', clean_item)
                    clean_item = clean_item.replace("**", "")
                    
                    if is_pending:
                        if current_sec not in sections:
                            sections[current_sec] = []
                        sections[current_sec].append(clean_item)

        msg_lines = [
            "🎩 *ALFRED — Informe Matutino Ejecutivos (07:30 AM)*\n",
            "¡Buenos días, Señor! A sus órdenes. Le presento la síntesis de apertura de jornada:\n"
        ]

        # 1. Cierre de la Jornada Anterior
        handover_data = read_latest_handover_from_log()
        if handover_data:
            header, points = handover_data
            msg_lines.append(f"🌙 *Resumen del Cierre Anterior ({header})*:")
            for p in points:
                msg_lines.append(f"• {p}")
            msg_lines.append("")

        # 2. Agenda y Prioridades de Hoy
        msg_lines.append("☀️ *Agenda & Prioridades Activas para Hoy*:")
        total_pending = 0
        for sec_name, items in sections.items():
            if items:
                msg_lines.append(f"📌 *{sec_name}*:")
                for item in items[:4]:
                    msg_lines.append(f"• {item}")
                msg_lines.append("")
                total_pending += len(items)

        if total_pending == 0:
            msg_lines.append("🎉 *Todas las prioridades del dashboard se encuentran al día.*")

        msg_lines.append("✨ *Que tenga una jornada de máxima excelencia y productividad, Señor.*")
        return "\n".join(msg_lines)

    except Exception as e:
        print(f"⚠️ Error construyendo resumen matutino: {e}")
        return "🎩 *ALFRED*: Buenos días, Señor. Ocurrió un inconveniente al generar el resumen de prioridades."

def notification_worker(config):
    """
    Hilo recurrente (Notification Worker) para notificaciones proactivas Push vía Telegram.
    Revisa a las 07:30 AM el resumen matutino y 15 minutos antes los eventos agendados en life-dashboard.md.
    """
    sent_daily = set()
    sent_events = set()

    print("🔔 Notification Worker activo en segundo plano.")

    while True:
        try:
            latest_config = load_env()
            token = latest_config.get("TELEGRAM_BOT_TOKEN")
            chat_id = latest_config.get("TELEGRAM_CHAT_ID") or config.get("TELEGRAM_CHAT_ID")

            if token and chat_id:
                now = datetime.datetime.now()
                today_str = now.strftime("%Y-%m-%d")

                # 1. Notificación matutina a las 07:30 AM
                if now.hour == 7 and now.minute == 30 and today_str not in sent_daily:
                    summary_text = build_daily_morning_summary()
                    res = telegram_api(token, "sendMessage", {
                        "chat_id": chat_id,
                        "text": summary_text,
                        "parse_mode": "Markdown"
                    })
                    if res and res.get("ok"):
                        sent_daily.add(today_str)
                        print(f"🔔 Notificación Push matutina (07:30 AM) enviada con éxito a Chat ID: {chat_id}")

                # 2. Notificaciones 15 minutos antes de eventos clave
                events = parse_upcoming_events_from_dashboard()
                for event in events:
                    event_dt = event["datetime"]
                    diff_seconds = (event_dt - now).total_seconds()

                    # Si el evento ocurre en los próximos 15 minutos (0 <= diff <= 900) y no se ha notificado
                    if 0 <= diff_seconds <= 900 and event["id"] not in sent_events:
                        mins_left = max(1, int(diff_seconds // 60))
                        event_text = (
                            f"⏰ *RECORDATORIO DE EVENTO PRÓXIMO* (en {mins_left} min)\n\n"
                            f"📌 *Compromiso*: {event['title']}\n"
                            f"🕒 *Horario*: `{event['raw_time']}`\n"
                            f"📂 *Sección*: {event['section']}\n\n"
                            f"🎩 *ALFRED*: A sus órdenes, Señor. Le recuerdo estar preparado para esta actividad."
                        )
                        res = telegram_api(token, "sendMessage", {
                            "chat_id": chat_id,
                            "text": event_text,
                            "parse_mode": "Markdown"
                        })
                        if res and res.get("ok"):
                            sent_events.add(event["id"])
                            print(f"🔔 Notificación Push de evento enviada ({event['title']}) a Chat ID: {chat_id}")

        except Exception as e:
            print(f"⚠️ Error en Notification Worker: {e}")

        time.sleep(30)

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
    if chat_id:
        save_chat_id(chat_id, config)

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
            "🔔 *2. Notificaciones Push Proactivas*:\n"
            "• Captura automática de su `TELEGRAM_CHAT_ID`.\n"
            "• Resumen diario de prioridades a las 07:30 AM.\n"
            "• Alertas 15 minutos antes de eventos clave de `life-dashboard.md`.\n\n"
            "🛠️ *3. Gestión de Tickets Helpdesk*:\n"
            "• `/ticket` — Ver últimos tickets de MasterHub.\n"
            "• `/ticket create Título | Descripción` — Crear nuevo ticket en Helpdesk.\n\n"
            "📥 *4. Ingesta a 2brain*:\n"
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
        telegram_api(token, "sendChatAction", {"chat_id": chat_id, "action": "typing"})
        response = call_gemini_alfred(gemini_key, text)
        telegram_api(token, "sendMessage", {"chat_id": chat_id, "text": response})
    else:
        reply = (
            f"A sus órdenes, Señor {sender}. He recibido su mensaje:\n\n"
            f"'{text}'\n\n"
            "💡 *Nota de ALFRED*: Para activar mis respuestas inteligentes completas por Telegram, por favor coloque su `GEMINI_API_KEY` en el archivo `scripts/.env` (es 100% gratuita en https://aistudio.google.com)."
        )
        telegram_api(token, "sendMessage", {"chat_id": chat_id, "text": reply, "parse_mode": "Markdown"})

def main():
    print("========================================================")
    print("   ALFRED 2brain - Bot de Telegram (Chat & Push Worker)")
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
        
    # Iniciar Hilo Recurrente de Notificaciones Push (Notification Worker)
    worker_thread = threading.Thread(target=notification_worker, args=(config,), daemon=True)
    worker_thread.start()
    print("🔔 Módulo de Notificaciones Push en segundo plano (Notification Worker): ACTIVADO")

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
