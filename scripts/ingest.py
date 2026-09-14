#!/usr/bin/env python3
"""
Script de Ingesta Rápida ALFRED 2brain
Uso:
  python scripts/ingest.py <ruta_archivo_o_url> [area]

Áreas disponibles:
  trabajo, programacion, proyectos, ministerial, familiar, finanzas
"""

import os
import sys
import datetime
import shutil
import urllib.request
import json

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "raw")
INBOX_DIR = os.path.join(RAW_DIR, "inbox")

os.makedirs(INBOX_DIR, exist_ok=True)

def ingest_file(source_path, area="inbox"):
    if not os.path.exists(source_path):
        print(f"❌ Error: El archivo '{source_path}' no existe.")
        return False
    
    filename = os.path.basename(source_path)
    target_area_dir = os.path.join(RAW_DIR, area) if area != "inbox" else INBOX_DIR
    os.makedirs(target_area_dir, exist_ok=True)
    
    target_path = os.path.join(target_area_dir, filename)
    shutil.copy2(source_path, target_path)
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"✅ Archivo ingerido exitosamente en: {target_path}")
    print(f"🕒 Timestamp: {timestamp}")
    print(f"📌 Pendiente de síntesis por ALFRED en wiki/{area}/")
    return True

def ingest_url(url, area="inbox"):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"url_ingest_{timestamp}.md"
    target_area_dir = os.path.join(RAW_DIR, area) if area != "inbox" else INBOX_DIR
    os.makedirs(target_area_dir, exist_ok=True)
    target_path = os.path.join(target_area_dir, filename)
    
    content = f"""---
title: "Ingesta de URL"
url: "{url}"
created: {datetime.datetime.now().strftime("%Y-%m-%d")}
area: "{area}"
status: "pending_synthesis"
---

# Enlace Ingerido

**URL**: {url}  
**Fecha de Captura**: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

> [!NOTE]
> Pendiente de lectura y síntesis por ALFRED en la base de conocimiento 2brain.
"""
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(content)
        
    print(f"✅ URL registrada exitosamente en: {target_path}")
    return True

def main():
    if len(sys.argv) < 2:
        print("Uso: python scripts/ingest.py <ruta_archivo_o_url> [area]")
        print("Ejemplo: python scripts/ingest.py https://youtube.com/watch?v=12345 ministerial")
        sys.exit(1)
        
    target = sys.argv[1]
    area = sys.argv[2] if len(sys.argv) > 2 else "inbox"
    
    if target.startswith("http://") or target.startswith("https://"):
        ingest_url(target, area)
    else:
        ingest_file(target, area)

if __name__ == "__main__":
    main()
