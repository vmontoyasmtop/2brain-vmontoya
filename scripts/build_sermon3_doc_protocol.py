#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script Oficial ALFRED / Docs Expert:
Actualización del Documento Oficial de Google Docs del Sermón 3 con el nuevo enfoque:
Los Tres Enemigos Mortales del Discipulado (Historias bíblicas en paralelo, exégesis y versos de soporte).
Documento ID: 1_odcEAt0dLERg5ePizpzuSKBrcfzUOo4C6Bh9zJnYOs
"""

import os
import sys
import json
import time
import urllib.request
import urllib.parse

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GDOCS_DIR = os.path.expanduser(r"~\.gdocs-trabajo-mcp")
TOKEN_PATH = os.path.join(GDOCS_DIR, "token.json")
CREDENTIALS_PATH = os.path.join(GDOCS_DIR, "credentials.json")
TARGET_DOC_ID = "1_odcEAt0dLERg5ePizpzuSKBrcfzUOo4C6Bh9zJnYOs"

def safe_urlopen(req, retries=5, delay=2):
    for attempt in range(retries):
        try:
            return urllib.request.urlopen(req, timeout=30)
        except Exception as e:
            if attempt == retries - 1:
                raise e
            time.sleep(delay * (attempt + 1))

def get_access_token():
    with open(CREDENTIALS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    web = data.get("web", {})
    client_id = web.get("client_id")
    client_secret = web.get("client_secret")

    with open(TOKEN_PATH, "r", encoding="utf-8") as f:
        tdata = json.load(f)

    req = urllib.request.Request(
        "https://oauth2.googleapis.com/token",
        data=urllib.parse.urlencode({
            "client_id": client_id,
            "client_secret": client_secret,
            "refresh_token": tdata["refresh_token"],
            "grant_type": "refresh_token"
        }).encode("utf-8")
    )
    resp = safe_urlopen(req)
    res = json.loads(resp.read().decode("utf-8"))
    return res["access_token"]

def update_google_doc(access_token):
    md_path = r"C:\Users\vmontoyaMG\Desktop\2brain\wiki\ministerial\sermon-3-un-corazon-ensenable-predica.md"
    with open(md_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    # Preparamos el texto limpio para Google Docs suprimiendo frontmatter y marcas markdown toscas
    lines = md_text.splitlines()
    cleaned = []
    frontmatter_count = 0
    for line in lines:
        if line.strip() == "---":
            frontmatter_count += 1
            if frontmatter_count <= 2:
                continue
        if frontmatter_count < 2:
            continue
        cleaned.append(line)

    content = "\n".join(cleaned).strip()

    # Limpiamos marcas markdown para garantizar lectura nativa pulcra
    content = content.replace("```markdown", "").replace("```", "")
    content = content.replace("`[PAUSA - SILENCIO]`", "[PAUSA - SILENCIO]")
    content = content.replace("`[VOZ CERCANA]`", "[VOZ CERCANA]")
    content = content.replace("`[ÉNFASIS FIRME]`", "[ÉNFASIS FIRME]")
    content = content.replace("`[INTERACCIÓN]`", "[INTERACCIÓN]")

    # 1. Obtener longitud actual del documento
    req_get = urllib.request.Request(
        f"https://docs.googleapis.com/v1/documents/{TARGET_DOC_ID}",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    resp_get = safe_urlopen(req_get)
    doc = json.loads(resp_get.read().decode("utf-8"))
    end_index = doc.get("body", {}).get("content", [])[-1].get("endIndex", 1) - 1

    # 2. Limpiar contenido viejo e insertar el nuevo texto estructurado
    requests = []
    if end_index > 1:
        requests.append({
            "deleteContentRange": {
                "range": {
                    "startIndex": 1,
                    "endIndex": end_index
                }
            }
        })
    requests.append({
        "insertText": {
            "location": {"index": 1},
            "text": content
        }
    })

    req_update = urllib.request.Request(
        f"https://docs.googleapis.com/v1/documents/{TARGET_DOC_ID}:batchUpdate",
        data=json.dumps({"requests": requests}).encode("utf-8"),
        headers={"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    )
    safe_urlopen(req_update)
    print(f"✅ Google Doc actualizado exitosamente con el enfoque de Los Tres Enemigos Mortales.")
    print(f"👉 URL: https://docs.google.com/document/d/{TARGET_DOC_ID}/edit")

if __name__ == "__main__":
    token = get_access_token()
    update_google_doc(token)
