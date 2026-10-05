#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script Oficial ALFRED / Docs Expert:
Creación del Documento Oficial de Google Docs del Sermón 4 (Estudio + Prédica con Puntos y Textos Claros).
Cuenta Personal / Ministerial: vmontoya.smartopsve@gmail.com
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
PERSONAL_EMAIL = "vmontoya.smartopsve@gmail.com"

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

def create_google_doc(access_token):
    title = "⛪ SERMÓN 4: De Aprendiz a Multiplicador — Estudio Bíblico & Guía de Púlpito"
    
    # 1. Crear documento vacío en Google Docs
    req_create = urllib.request.Request(
        "https://docs.googleapis.com/v1/documents",
        data=json.dumps({"title": title}).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
    )
    resp_create = safe_urlopen(req_create)
    doc_data = json.loads(resp_create.read().decode("utf-8"))
    doc_id = doc_data["documentId"]
    print(f"📄 Documento creado en Google Docs. ID: {doc_id}")

    # 2. Cargar contenido consolidado
    md_estudio = r"C:\Users\vmontoyaMG\Desktop\2brain\wiki\ministerial\sermon-4-de-aprendiz-a-multiplicador-estudio.md"
    md_predica = r"C:\Users\vmontoyaMG\Desktop\2brain\wiki\ministerial\sermon-4-de-aprendiz-a-multiplicador-predica.md"
    
    with open(md_estudio, "r", encoding="utf-8") as f:
        text_estudio = f.read()
    with open(md_predica, "r", encoding="utf-8") as f:
        text_predica = f.read()

    def clean_md(text):
        lines = text.splitlines()
        cleaned = []
        frontmatter = 0
        for l in lines:
            if l.strip() == "---":
                frontmatter += 1
                if frontmatter <= 2:
                    continue
            if frontmatter < 2:
                continue
            cleaned.append(l)
        res = "\n".join(cleaned).strip()
        res = res.replace("```markdown", "").replace("```", "")
        res = res.replace("`[PAUSA - SILENCIO]`", "[PAUSA - SILENCIO]")
        res = res.replace("`[VOZ CERCANA]`", "[VOZ CERCANA]")
        res = res.replace("`[ÉNFASIS FIRME]`", "[ÉNFASIS FIRME]")
        res = res.replace("`[INTERACCIÓN]`", "[INTERACCIÓN]")
        res = res.replace("`[ANOTAR EN EL CUADERNO]`", "[ANOTAR EN EL CUADERNO]")
        return res

    full_text = f"""================================================================================
SERMÓN 4: DE APRENDIZ A MULTIPLICADOR (EL CICLO DE LA VIDA)
Serie de Sermones: Caminando Juntos — De Creyentes a Discípulos
Documento Oficial de Púlpito & Estudio Exegético
================================================================================

PASAJES BASE:
• 2 Timoteo 2:1-2
• Hebreos 5:11-14
• 1 Corintios 11:1
(Con Mateo 28:18-20 y Mateo 5:14-16)

IDEA CENTRAL (PROPOSICIÓN HOMILÉTICA):
"La verdadera madurez espiritual jamás se mide por cuánta Biblia cabe en tu cabeza, sino por cuántas vidas estás alimentando con el amor de Cristo: el discipulado bíblico no concluye cuando aprendes a seguir a Jesús, sino cuando enseñas a otros a seguirle."

================================================================================
PARTE I: GUÍA Y MANUSCRITO DE PÚLPITO (CON PUNTOS Y TEXTOS CLAROS)
================================================================================

{clean_md(text_predica)}

================================================================================
PARTE II: ESTUDIO EXEGÉTICO, LINGÜÍSTICO Y TEOLÓGICO DE RESPALDO
================================================================================

{clean_md(text_estudio)}
"""

    # 3. Insertar texto en el documento
    requests = [{
        "insertText": {
            "location": {"index": 1},
            "text": full_text
        }
    }]

    req_update = urllib.request.Request(
        f"https://docs.googleapis.com/v1/documents/{doc_id}:batchUpdate",
        data=json.dumps({"requests": requests}).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
    )
    safe_urlopen(req_update)
    print("✅ Contenido insertado con éxito en el documento.")

    # 4. Otorgar permisos a la cuenta personal (vmontoya.smartopsve@gmail.com) como editor y a cualquiera con el link como lector
    try:
        perm_personal = urllib.request.Request(
            f"https://www.googleapis.com/drive/v3/files/{doc_id}/permissions?sendNotificationEmail=false",
            data=json.dumps({
                "role": "writer",
                "type": "user",
                "emailAddress": PERSONAL_EMAIL
            }).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
        )
        safe_urlopen(perm_personal)
        print(f"👤 Permiso de edición otorgado a la cuenta personal: {PERSONAL_EMAIL}")
    except Exception as e:
        print(f"⚠️ Nota permiso personal: {e}")

    try:
        perm_anyone = urllib.request.Request(
            f"https://www.googleapis.com/drive/v3/files/{doc_id}/permissions",
            data=json.dumps({"role": "reader", "type": "anyone"}).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
        )
        safe_urlopen(perm_anyone)
        print("🌍 Permiso de lectura pública por enlace habilitado.")
    except Exception as e:
        print(f"⚠️ Nota permiso público: {e}")

    doc_url = f"https://docs.google.com/document/d/{doc_id}/edit"
    print(f"👉 URL Oficial: {doc_url}")
    return doc_url, doc_id

if __name__ == "__main__":
    token = get_access_token()
    url, doc_id = create_google_doc(token)
    print(f"DOC_URL={url}")
