#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Descargador oficial de Google Stitch para SmartOps VE
"""

import os
import sys
import json
import base64
import urllib.request

if sys.platform == "win32":
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8')

API_KEY = os.environ.get("STITCH_API_KEY", "")
BASE_URL = f"https://stitch.googleapis.com/mcp?key={API_KEY}"
PROJECT_ID = "6994536314139933854"

def call_tool(name: str, arguments: dict) -> dict:
    body = json.dumps({
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": name,
            "arguments": arguments
        }
    }).encode("utf-8")
    
    req = urllib.request.Request(
        BASE_URL,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=120) as res:
        data = json.loads(res.read().decode())
        content = data["result"]["content"][0]["text"]
        return json.loads(content)

def main():
    print(f"🦋 Conectando a Stitch para Proyecto {PROJECT_ID}...")
    
    # 1. Generar Pantalla 2 (Dashboard Administrativo) si no existe
    screens = call_tool("list_screens", {"projectId": PROJECT_ID}).get("screens", [])
    print(f"Pantallas actuales en Stitch: {len(screens)}")
    
    has_dashboard = any("Dashboard" in s.get("title", "") for s in screens)
    if not has_dashboard:
        print("📌 Generando Pantalla 2: Dashboard Administrativo & Kanban...")
        prompt_p2 = (
            "Design an executive multi-tenant administrative dashboard for 'SmartOps VE' professionals to manage appointments, "
            "AI leads, and e-commerce orders. Desktop widescreen view (1440px), dark obsidian theme (#0B132B), glassmorphic panels (#161F38), "
            "bright electric blue accents (#0072FF), and cyan glowing metrics (#00E5FF). "
            "Left Sidebar with logo, Command Bar shortcut (Ctrl+K), and navigation links. "
            "Top bar with live Google Calendar sync status pill and 'Ver Perfil Público' action. "
            "AI Morning Briefing full-width glowing hero box with WhatsApp confirmation CTA. "
            "Bento Metrics Grid with 4 cards: Ingresos del Mes ($1,480 USD), Citas Completadas (38), Conversión Agente IA (41.5%), Pases Wallet/NFC (142). "
            "Interactive 4-column Appointments Kanban Board: Confirmadas, En Espera, En Curso, Completadas with appointment cards and Google Meet badges. "
            "AI Agent Training Console section for master prompt and WhatsApp Cloud API toggles."
        )
        s2 = call_tool("generate_screen_from_text", {
            "projectId": PROJECT_ID,
            "prompt": prompt_p2,
            "deviceType": "DESKTOP",
            "modelId": "GEMINI_3_8_FLASH"
        })
        print(f"✓ Pantalla 2 generada: {s2.get('title')}")
        screens = call_tool("list_screens", {"projectId": PROJECT_ID}).get("screens", [])

    wiki_assets = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "wiki", "proyectos", "assets")
    wiki_prototipos = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "wiki", "proyectos", "prototipos")

    # 2. Descargar archivos para cada pantalla
    for s in screens:
        screen_id = s.get("name", "").split("/")[-1]
        screen_title = s.get("title", "Screen")
        slug = "profile_booking" if "Profile" in screen_title or "Storefront" in screen_title else "admin_dashboard"
        print(f"\n📥 Procesando: {screen_title} ({screen_id})...")
        
        # HTML
        html_name = s.get("htmlCode", {}).get("name")
        if html_name:
            print(f"  Descargando HTML ({html_name})...")
            res_html = call_tool("download_file", {"name": html_name})
            html_content = res_html.get("html", "")
            if html_content:
                out_path = os.path.join(wiki_prototipos, f"stitch_smartops_{slug}_official.html")
                with open(out_path, "w", encoding="utf-8") as f:
                    f.write(html_content)
                print(f"  ✓ Guardado: {out_path}")
        
        # Screenshot
        img_name = s.get("screenshot", {}).get("name")
        if img_name:
            print(f"  Descargando Screenshot ({img_name})...")
            res_img = call_tool("download_file", {"name": img_name})
            img_b64 = res_img.get("image", "")
            if img_b64:
                img_bytes = base64.b64decode(img_b64)
                out_img = os.path.join(wiki_assets, f"stitch_smartops_{slug}.png")
                with open(out_img, "wb") as f:
                    f.write(img_bytes)
                print(f"  ✓ Guardado: {out_img}")

    print("\n🎉 ¡Descarga oficial completa desde Google Stitch!")

if __name__ == "__main__":
    main()
