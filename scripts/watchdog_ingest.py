#!/usr/bin/env python3
"""
Watchdog de Ingesta Automática ALFRED 2brain
Monitorea la carpeta raw/inbox/ y notifica/registra nuevos archivos capturados.
Ejecución: python scripts/watchdog_ingest.py
"""

import os
import sys
import time
import datetime
import json

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "raw")
INBOX_DIR = os.path.join(RAW_DIR, "inbox")
QUEUE_FILE = os.path.join(BASE_DIR, "scripts", ".ingest_queue.json")

os.makedirs(INBOX_DIR, exist_ok=True)

def load_processed_files():
    if os.path.exists(QUEUE_FILE):
        try:
            with open(QUEUE_FILE, "r", encoding="utf-8") as f:
                return set(json.load(f))
        except Exception:
            return set()
    return set()

def save_processed_files(processed):
    with open(QUEUE_FILE, "w", encoding="utf-8") as f:
        json.dump(list(processed), f, indent=2)

def scan_inbox():
    processed = load_processed_files()
    current_files = []
    
    for root, _, files in os.walk(INBOX_DIR):
        for file in files:
            if not file.startswith("."):
                full_path = os.path.abspath(os.path.join(root, file))
                current_files.append(full_path)
                
    new_files = [f for f in current_files if f not in processed]
    
    if new_files:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n🔔 [{timestamp}] ¡Se detectaron {len(new_files)} nuevo(s) archivo(s) en inbox!")
        for file_path in new_files:
            rel_path = os.path.relpath(file_path, BASE_DIR)
            print(f"  📄 Nuevo elemento: {rel_path}")
            processed.add(file_path)
        save_processed_files(processed)
        print("  💡 Ejecute 'ALFRED' o '/ingest' para procesar los elementos con los subagentes.")
        
def main():
    print("========================================================")
    print("   ALFRED 2brain - Watchdog de Ingesta Automática")
    print("========================================================")
    print(f"📁 Monitoreando carpeta: {INBOX_DIR}")
    print("Press Ctrl+C para detener.\n")
    
    try:
        while True:
            scan_inbox()
            time.sleep(5)
    except KeyboardInterrupt:
        print("\n👋 Watchdog detenido por el usuario.")

if __name__ == "__main__":
    main()
