#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Google Stitch Cloud Deployment — EL CUADRE POS (Fashion & Footwear Edition)
==========================================================================
Diseñadora: 🦋 Konan (El Ángel de Papel — Akatsuki Design Labs)
Propósito: Desplegar en la nube de Google Stitch (stitch.withgoogle.com)
           la pantalla oficial para tiendas de ropa y calzado en el proyecto
           oficial 'El Cuadre POS - Caja, Viveres y Abasto Criollo' (ID: 15301442243370859300).
"""

import os
import sys
import json
import time
import base64
import urllib.request
import urllib.parse
import urllib.error

if sys.platform == "win32":
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_FILE = os.path.join(BASE_DIR, "scripts", ".env")

config = {}
if os.path.exists(ENV_FILE):
    with open(ENV_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                config[k.strip()] = v.strip()

API_KEY = (
    os.environ.get("GOOGLE_STITCH_API_KEY") or
    os.environ.get("STITCH_API_KEY") or
    config.get("GOOGLE_STITCH_API_KEY") or
    config.get("STITCH_API_KEY")
)

if not API_KEY:
    print("❌ Error: No se encontró STITCH_API_KEY en scripts/.env")
    sys.exit(1)

BASE_URL = f"https://stitch.googleapis.com/mcp?key={API_KEY}"
PROJECT_ID = "15301442243370859300"

def call_tool(name: str, arguments: dict, timeout_sec: int = 240) -> dict:
    payload = {
        "jsonrpc": "2.0",
        "id": int(time.time() * 1000),
        "method": "tools/call",
        "params": {
            "name": name,
            "arguments": arguments
        }
    }
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        BASE_URL,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    
    with urllib.request.urlopen(req, timeout=timeout_sec) as res:
        data = json.loads(res.read().decode())
        if "error" in data:
            raise RuntimeError(f"RPC Error ({name}): {data['error']}")
        
        result = data.get("result", {})
        if result.get("isError"):
            err_text = result.get("content", [{}])[0].get("text", "")
            raise RuntimeError(f"Tool Error ({name}): {err_text}")
        
        content_items = result.get("content", [])
        if not content_items:
            return {}
        
        text = content_items[0].get("text", "")
        try:
            return json.loads(text)
        except Exception:
            return {"raw_text": text}

def main():
    print("🦋 Konan (UI/UX Stitch): Conectando a Google Stitch (stitch.withgoogle.com)...")
    print(f"🎯 Proyecto Destino: 'El Cuadre POS' (ID: {PROJECT_ID})")
    
    # 1. Verificar pantallas existentes
    screens_resp = call_tool("list_screens", {"projectId": PROJECT_ID})
    screens = screens_resp.get("screens", [])
    print(f"📋 Pantallas actuales en Stitch para este proyecto: {len(screens)}")
    for s in screens:
        print(f"   - {s.get('title')} (ID: {s.get('name', '').split('/')[-1]})")

    # 2. Generar pantalla con generate_screen_from_text
    print("\n🎨 Generando pantalla en Google Stitch Cloud vía Gemini 3.8 Flash...")
    prompt_fashion = (
        "Design a modern touch-screen POS terminal for an apparel and footwear boutique named 'EL CUADRE POS — FASHION & FOOTWEAR EDITION'. "
        "Widescreen 1080p desktop layout. "
        "Theme: Obsidian Atelier Luxury Dark Mode (#0B0F17 dark slate background, #131D2D elevated surfaces, #1E293B border accents, #3B82F6 electric cobalt blue primary action, #F43F5E fashion coral badge, #F59E0B gold accents). "
        "Header: Left side has boutique logo 'EL CUADRE FASHION' with gold hangtag icon, department toggle button (Ropa y Calzado / Viveres y Market). Center has live BCV exchange rate pill ('Tasa BCV: Bs. 44.50 / $') with green sync dot, quick action buttons for 'Canje / Devolución' and 'Etiquetas Térmicas 50x30mm'. Right side has Cashier profile and PIN Lock. "
        "Main Catalog Area (68% width): Top search input with USB barcode scanner icon. Horizontal department pills (Todos, Calzado Caballero, Calzado Dama, Camisas y Franelas, Pantalones Jeans, Vestidos, Accesorios). Product grid displaying footwear (sneakers, oxfords, stilettos) and apparel cards with high-res photos, dual pricing ($ USD and Bs. BCV), and size availability indicators. "
        "Variant Selector Modal: Centered touch modal with large size buttons (36, 37, 38, 39, 40, 41, 42, 43, 44) showing color-coded stock (Green: in stock, Amber: last pair, Gray: sold out), color swatches (Negro Onix, Blanco Puro, Rojo), and add to ticket button. "
        "Cart & Checkout Panel (32% width): Active ticket items with explicit [TALLA: 42] and [COLOR: Negro] badges, plus/minus quantity steppers, subtotal, 16% IVA SENIAT tax, grand total in USD ($) and Bolívares (Bs.), and Venezuelan payment method buttons (Efectivo $, Pago Móvil QR, Punto de Venta, Zelle)."
    )

    gen_resp = call_tool("generate_screen_from_text", {
        "projectId": PROJECT_ID,
        "prompt": prompt_fashion,
        "deviceType": "DESKTOP",
        "modelId": "GEMINI_3_8_FLASH"
    }, timeout_sec=240)

    print("\n✨ ¡Respuesta de generación recibida de Google Stitch!")
    print(json.dumps(gen_resp, indent=2, ensure_ascii=False)[:500] + "...")

    # Extraer el screen name generado
    # La respuesta suele traer el objeto screen o lista de screens generadas
    new_screen = gen_resp if "name" in gen_resp else gen_resp.get("screen", {})
    screen_name = new_screen.get("name", "")
    
    if not screen_name:
        # Volver a listar pantallas para ubicar la nueva
        time.sleep(2)
        refreshed = call_tool("list_screens", {"projectId": PROJECT_ID}).get("screens", [])
        if refreshed:
            new_screen = refreshed[-1]
            screen_name = new_screen.get("name", "")

    screen_id = screen_name.split("/")[-1] if screen_name else "generated"
    screen_title = new_screen.get("title", "Caja Táctica POS — Fashion & Footwear Edition")
    
    print(f"\n✅ Pantalla Generada en Google Stitch:")
    print(f"   • Título: {screen_title}")
    print(f"   • Screen ID: {screen_id}")
    print(f"   • Recurso: {screen_name}")

    # Descargar screenshot si está disponible
    screenshot_obj = new_screen.get("screenshot", {})
    screenshot_file_name = screenshot_obj.get("name", "") if isinstance(screenshot_obj, dict) else ""
    
    if screenshot_file_name:
        print(f"\n📸 Descargando captura oficial desde Google Stitch ({screenshot_file_name})...")
        try:
            file_resp = call_tool("download_file", {"name": screenshot_file_name})
            img_b64 = file_resp.get("content", "") or file_resp.get("data", "")
            if img_b64:
                img_path = os.path.join(BASE_DIR, "wiki", "proyectos", "assets", "stitch_el_cuadre_fashion_pos.png")
                with open(img_path, "wb") as f_img:
                    f_img.write(base64.b64decode(img_b64))
                print(f"✅ Captura guardada en: {img_path}")
        except Exception as e:
            print(f"⚠️ Nota al descargar captura: {e}")

    # Descargar HTML code si está disponible
    html_obj = new_screen.get("htmlCode", {}) or new_screen.get("html_code", {})
    html_file_name = html_obj.get("name", "") if isinstance(html_obj, dict) else ""
    
    if html_file_name:
        print(f"\n💻 Descargando código HTML oficial desde Google Stitch ({html_file_name})...")
        try:
            html_resp = call_tool("download_file", {"name": html_file_name})
            html_content = html_resp.get("content", "")
            if html_content:
                # Decodificar si viene en base64
                try:
                    html_text = base64.b64decode(html_content).decode("utf-8")
                except Exception:
                    html_text = html_content
                html_path = os.path.join(BASE_DIR, "wiki", "proyectos", "prototipos", "stitch_el_cuadre_fashion_pos_stitch_cloud.html")
                with open(html_path, "w", encoding="utf-8") as f_html:
                    f_html.write(html_text)
                print(f"✅ HTML guardado en: {html_path}")
        except Exception as e:
            print(f"⚠️ Nota al descargar HTML: {e}")

    # Enlace Web directo para El Señor
    stitch_url = f"https://stitch.withgoogle.com/projects/{PROJECT_ID}"
    print(f"\n" + "="*70)
    print(f"🚀 ¡YA ESTÁ DISPONIBLE EN GOOGLE STITCH!")
    print(f"🔗 Enlace directo del proyecto: {stitch_url}")
    if screen_id:
        print(f"🖼️ Screen ID: {screen_id}")
    print(f"="*70)

if __name__ == "__main__":
    main()
