#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Google Stitch Generator para SmartOps VE (Konan & Akatsuki)
===========================================================
Interactúa directamente con https://stitch.googleapis.com/mcp?key=...
para crear proyecto, design system y pantallas oficiales en Stitch.
"""

import os
import sys
import json
import time
import urllib.request
import urllib.parse
import urllib.error

if sys.platform == "win32":
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8')

API_KEY = os.environ.get("STITCH_API_KEY", "")
BASE_URL = f"https://stitch.googleapis.com/mcp?key={API_KEY}"

def call_mcp_tool(name: str, arguments: dict) -> dict:
    body = json.dumps({
        "jsonrpc": "2.0",
        "id": int(time.time() * 1000),
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
    
    try:
        with urllib.request.urlopen(req, timeout=120) as res:
            resp_data = json.loads(res.read().decode())
            if "error" in resp_data:
                raise RuntimeError(f"MCP RPC Error: {resp_data['error']}")
            
            result = resp_data.get("result", {})
            if result.get("isError"):
                content = result.get("content", [{}])[0].get("text", "")
                raise RuntimeError(f"Tool Error ({name}): {content}")
            
            # Content suele ser JSON en string dentro de result.content[0].text
            content_text = result.get("content", [{}])[0].get("text", "")
            try:
                return json.loads(content_text)
            except Exception:
                return {"raw_text": content_text}
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode()
        raise RuntimeError(f"HTTP {e.code} Error calling {name}: {err_msg}")

def main():
    print("🦋 Konan (UI/UX Designer): Iniciando despliegue de SmartOps VE en Google Stitch...")
    
    # 1. Crear Proyecto
    print("📌 1. Creando Proyecto en Google Stitch...")
    proj_resp = call_mcp_tool("create_project", {
        "title": "SmartOps VE — Next-Gen Business Hub"
    })
    proj_name = proj_resp.get("name", "")
    proj_id = proj_name.replace("projects/", "")
    print(f"✅ Proyecto Creado: {proj_name} (ID: {proj_id})")
    
    # 2. Crear Design System
    print("📌 2. Configurando Design System 'SmartOps Obsidian Glow'...")
    ds_resp = call_mcp_tool("create_design_system", {
        "projectId": proj_id,
        "designSystem": {
            "displayName": "SmartOps Obsidian Glow",
            "theme": {
                "colorMode": "DARK",
                "headlineFont": "MONTSERRAT",
                "bodyFont": "INTER",
                "roundness": "ROUND_TWELVE",
                "customColor": "#00e5ff",
                "overridePrimaryColor": "#0072ff",
                "overrideSecondaryColor": "#00e5ff",
                "overrideNeutralColor": "#0b132b"
            }
        }
    })
    ds_id = ds_resp.get("name", "") or ds_resp.get("id", "")
    print(f"✅ Design System Registrado: {ds_id}")
    
    # 3. Generar Pantalla 1: Perfil Público & Booking Storefront
    print("📌 3. Generando Pantalla 1: 'Perfil Inteligente & Booking Storefront'...")
    prompt_p1 = (
        "Design a hyper-modern 2026 digital business profile and service booking storefront for 'SmartOps VE' "
        "(professional brand for cloud architect & retail consultant Ing. Víctor Montoya). "
        "Dark luxury aesthetic: Deep Obsidian background (#0B132B) with subtle cyan glowing atmospheric backdrops (#00E5FF) "
        "and glassmorphism cards (#161F38 with 16px backdrop-blur and border of rgba(0,229,255,0.15)). "
        "Sections: Top Sticky Navbar with SmartOps VE logo, Bento Grid Hero with verified avatar and green pulse 'Available Today', "
        "direct WhatsApp and Add to Wallet (NFC) buttons. Segmented Navigation: 'Agendar Cita (Booking)' and 'Servicios & Tienda'. "
        "Real-time Booking Engine with 3 selectable service cards ($30 USD), 5-day horizon selector, and available time slots grid "
        "(09:30 AM, 11:00 AM, 02:30 PM, 04:15 PM) synced with Google Calendar. Floating AI Copilot widget on bottom-right."
    )
    
    screen1_resp = call_mcp_tool("generate_screen_from_text", {
        "projectId": proj_id,
        "prompt": prompt_p1,
        "deviceType": "DESKTOP",
        "modelId": "GEMINI_3_8_FLASH"
    })
    screen1_name = screen1_resp.get("name", "")
    print(f"✅ Pantalla 1 Generada: {screen1_name}")
    
    # 4. Generar Pantalla 2: Dashboard Administrativo & Kanban
    print("📌 4. Generando Pantalla 2: 'Dashboard Administrativo & Kanban de Citas'...")
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
    
    screen2_resp = call_mcp_tool("generate_screen_from_text", {
        "projectId": proj_id,
        "prompt": prompt_p2,
        "deviceType": "DESKTOP",
        "modelId": "GEMINI_3_8_FLASH"
    })
    screen2_name = screen2_resp.get("name", "")
    print(f"✅ Pantalla 2 Generada: {screen2_name}")
    
    # 5. Descargar archivos y capturas
    print("📌 5. Descargando código HTML y capturas oficiales de Stitch...")
    wiki_assets = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "wiki", "proyectos", "assets")
    wiki_prototipos = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "wiki", "proyectos", "prototipos")
    os.makedirs(wiki_assets, exist_ok=True)
    os.makedirs(wiki_prototipos, exist_ok=True)
    
    # Listar pantallas para obtener archivos
    screens_list = call_mcp_tool("list_screens", {"projectId": proj_id})
    screens = screens_list.get("screens", [])
    print(f"Total pantallas encontradas: {len(screens)}")
    
    for idx, screen in enumerate(screens, 1):
        s_name = screen.get("name", "")
        s_title = screen.get("title", f"screen_{idx}")
        print(f"Descargando archivos para {s_name} ({s_title})...")
        
        # Descargar HTML
        try:
            html_data = call_mcp_tool("download_file", {
                "name": f"{s_name}/code.html"
            })
            html_content = html_data.get("content", "") or html_data.get("raw_text", "")
            if html_content:
                out_html = os.path.join(wiki_prototipos, f"stitch_smartops_screen_{idx}.html")
                with open(out_html, "w", encoding="utf-8") as f:
                    f.write(html_content)
                print(f"  ✓ HTML guardado en {out_html}")
        except Exception as e:
            print(f"  ⚠️ Error descargando HTML: {e}")
            
        # Descargar Screenshot
        try:
            png_data = call_mcp_tool("download_file", {
                "name": f"{s_name}/screenshot.png"
            })
            img_url = png_data.get("downloadUrl", "")
            if img_url:
                out_png = os.path.join(wiki_assets, f"stitch_smartops_screen_{idx}.png")
                urllib.request.urlretrieve(img_url, out_png)
                print(f"  ✓ Captura PNG guardada en {out_png}")
        except Exception as e:
            print(f"  ⚠️ Error descargando Screenshot: {e}")
            
    print(f"\n🎉 ¡Misión cumplida! Proyecto disponible en: https://stitch.withgoogle.com/")
    print(f"   Project ID: {proj_id}")

if __name__ == "__main__":
    main()
