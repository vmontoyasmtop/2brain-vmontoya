#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Google Stitch Cloud Deployment & Sync — EL CUADRE MARCHADOR MOBILE (US-19)
==========================================================================
Diseñadora: 🦋 Konan (El Ángel de Papel — Akatsuki Design Labs)
Propósito: Verificar, completar y descargar desde Google Stitch Cloud
           las 4 pantallas móviles nativas de 'El Cuadre Marchador Mobile' (US-19)
           en el proyecto 'El Cuadre POS' (ID: 15301442243370859300).
"""

import os
import sys
import json
import time
import base64
import urllib.request
import urllib.error

if sys.platform == "win32":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

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
    os.environ.get("GOOGLE_STITCH_API_KEY")
    or os.environ.get("STITCH_API_KEY")
    or config.get("GOOGLE_STITCH_API_KEY")
    or config.get("STITCH_API_KEY")
    or ""
)

BASE_URL = f"https://stitch.googleapis.com/mcp?key={API_KEY}"
PROJECT_ID = "15301442243370859300"

SCREENS_SPEC = [
    {
        "slug": "stitch_el_cuadre_marchador_escaner",
        "keywords": ["escaner", "escáner", "scanner", "pasillo", "camera", "harina"],
        "title_hint": "El Cuadre Marchador — Escáner por Cámara & Buscador de Pasillo",
        "prompt": (
            "Design a native mobile app screen (Flutter iOS/Android) for 'EL CUADRE MARCHADOR — ESCÁNER & PASILLO'. "
            "Theme: Dark Slate Criollo (#020617 deep background, #0F172A card surfaces, #1E293B borders, "
            "#10B981 emerald green primary accents, #F59E0B BCV amber gold accents). "
            "Top App Bar: Compact brand header 'EL CUADRE MARCHADOR', LAN Wi-Fi connection status pill "
            "('🟢 Conectado Caja Principal 192.168.1.100 | SQLite Sync'), and live exchange rate badge ('Tasa BCV: Bs. 45.00 / $'). "
            "Upper Half (Live Camera Barcode Scanner): Real-time camera viewfinder with a glowing emerald green (#10B981) laser reticle "
            "targeting an EAN-13 / Code-128 barcode, flashlight toggle button, and floating voice/text search bar ('Buscar producto o código...'). "
            "Lower Half (Draggable Instant Result Bottom Sheet <100ms): Scanned product card for 'Harina P.A.N. Maíz Blanco 1Kg' with product thumbnail, "
            "SKU badge '7591001234567', Stock pill ('Stock: 48 und'), Cost ('Costo: $0.95'), and highlighted dual Selling Price "
            "('$1.40 USD / Bs. 63.00 BCV'). Three large tactile quick-action buttons: 'Marcar Precio', 'Sumar Stock', and '+ Cola Etiqueta'. "
            "Bottom Navigation Bar with 4 tabs: 'Escáner' (active emerald), 'Marcado $/Bs', 'Conteo/Recepción', 'Etiquetas'."
        ),
    },
    {
        "slug": "stitch_el_cuadre_marchador_marcado",
        "keywords": ["marcado", "bimoneda", "margen", "margin"],
        "title_hint": "El Cuadre Marchador — Ficha de Marcado Bimoneda ($/Bs) & Editor de Margen",
        "prompt": (
            "Design a native mobile app screen (Flutter iOS/Android) for 'EL CUADRE MARCHADOR — MARCADO BIMONEDA ($/Bs) & MARGEN'. "
            "Theme: Dark Slate Criollo (#020617 background, #0F172A elevated cards, #10B981 emerald green for USD, #F59E0B amber for Bolívares BCV). "
            "Product Header Card: Thumbnail photo of 'Aceite de Maíz Mazeite 1L', EAN-13 barcode '7592009876543', category pill 'Víveres Secos', "
            "and green sync badge ('Sincronizado con Caja'). "
            "Cost & Dual-Currency Margin Card: Editable Purchase Cost input ('Costo Compra: $2.10 USD'), interactive profit margin selector pills "
            "('+20%', '+30%', '+35% [Activo]', '+50%', 'Manual'), large prominent Selling Price in USD ('$2.85 USD') styled in bold Space Grotesk emerald (#10B981), "
            "and automatic live conversion to Bolívares ('Bs. 128.25') in glowing amber (#F59E0B) at 'Tasa BCV: Bs. 45.00/$'. "
            "Highlighted Tactile Toggle Switch card: '🏷️ Enviar automáticamente a Cola de Habladores / Etiquetas' switched ON. "
            "Compact quick numeric keypad at the bottom and full-width primary emerald CTA button: 'Guardar y Sincronizar con Caja'."
        ),
    },
    {
        "slug": "stitch_el_cuadre_marchador_conteo",
        "keywords": ["recepción", "recepcion", "depósito", "deposito", "conteo", "offline"],
        "title_hint": "El Cuadre Marchador — Recepción Exprés en Depósito & Conteo Offline-First",
        "prompt": (
            "Design a native mobile app screen (Flutter iOS/Android) for 'EL CUADRE MARCHADOR — RECEPCIÓN EN DEPÓSITO & CONTEO OFFLINE-FIRST'. "
            "Theme: Dark Slate Criollo (#020617 background, #0F172A cards, #F59E0B amber offline indicators, #10B981 emerald actions). "
            "Top Offline-First Status Banner: High-visibility amber/slate banner '⚡ Modo Depósito SQLite: 4 cambios pendientes por sincronizar' "
            "with compact action button 'Sincronizar Lote'. "
            "Top Segmented Tabs: 'Conteo Físico Rápido' (active) vs 'Alta Exprés Nuevo Producto'. "
            "Agile Warehouse Form: Product photo capture box with camera icon, 'Generar Código Interno Code-128' button, "
            "unit type toggle ('UNIDAD' vs 'PESO Kg'), and large tactile physical count stepper buttons ('-10', '-1', '+1', '+10', '+Caja x24'). "
            "Stock Comparison Card: 'Stock Sistema: 36 und' vs 'Stock Físico Contado: 60 und' with highlighted discrepancy badge ('+24 und Entrada de Caja'). "
            "Compact Cost ($0.95) and Selling Price ($1.40 / Bs. 63.00) inputs, and primary bottom button: 'Registrar en Lote Local (SQLite)'."
        ),
    },
    {
        "slug": "stitch_el_cuadre_marchador_etiquetas",
        "keywords": ["habladores", "impresión", "impresion", "bluetooth", "50x30", "cola de habladores", "cola de etiquetas"],
        "title_hint": "El Cuadre Marchador — Cola de Habladores & Impresión Térmica Bluetooth 50x30mm",
        "prompt": (
            "Design a native mobile app screen (Flutter iOS/Android) for 'EL CUADRE MARCHADOR — COLA DE HABLADORES & IMPRESIÓN BLUETOOTH 50x30mm'. "
            "Theme: Dark Slate Criollo (#020617 background, #0F172A cards, #10B981 emerald accents, #F59E0B amber BCV highlights). "
            "Top Printer Status Bar: Connected thermal printer pill '🖨️ Bluetooth: Xprinter XP-P300 Conectada — Batería 85%' with toggle to '🖥️ Cola PC Mostrador'. "
            "Format Selector Tabs: 'Etiqueta Adhesiva Térmica 50x30mm (Code-128)' vs 'Hablador de Anaquel Criollo ($ / Bs BCV)'. "
            "Realistic Live Label Preview Card: Crisp white thermal label mockup (50x30mm ratio) showing product name 'HARINA P.A.N. 1KG', "
            "bold dual price '$1.40 / Bs. 63.00', date '04/11/2026', and scannable Code-128 barcode bars. "
            "Print Queue List ('15 Productos Marcados en Cola'): Scrollable item cards with product name, updated dual price, and copy count selector pills "
            "('x1', 'x2', 'x5'). "
            "Floating Bottom Primary CTA Button: '🖨️ Imprimir Lote Ahora (24 etiquetas)' in glowing emerald green."
        ),
    },
]


def call_tool(name: str, arguments: dict, timeout_sec: int = 300) -> dict:
    payload = {
        "jsonrpc": "2.0",
        "id": int(time.time() * 1000),
        "method": "tools/call",
        "params": {"name": name, "arguments": arguments},
    }
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        BASE_URL,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout_sec) as res:
        data = json.loads(res.read().decode("utf-8"))
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


def find_screens_in_response(obj) -> list:
    """Busca recursivamente objetos screen válidos (que tengan htmlCode o deviceType o name con screens/)."""
    found = []
    if isinstance(obj, dict):
        name = str(obj.get("name", ""))
        if "screens/" in name and ("htmlCode" in obj or "html_code" in obj or "screenshot" in obj):
            found.append(obj)
        for v in obj.values():
            found.extend(find_screens_in_response(v))
    elif isinstance(obj, list):
        for item in obj:
            found.extend(find_screens_in_response(item))
    return found


def download_screen_files(screen_obj: dict, slug: str, assets_dir: str, protos_dir: str):
    img_out = os.path.join(assets_dir, f"{slug}.png")
    html_out = os.path.join(protos_dir, f"{slug}.html")

    # Screenshot
    screenshot_obj = screen_obj.get("screenshot", {})
    screenshot_name = screenshot_obj.get("name", "") if isinstance(screenshot_obj, dict) else ""
    if screenshot_name:
        res_img = call_tool("download_file", {"name": screenshot_name})
        img_b64 = res_img.get("image") or res_img.get("content") or res_img.get("data") or ""
        if img_b64:
            with open(img_out, "wb") as f_img:
                f_img.write(base64.b64decode(img_b64))
            print(f"   🖼️ PNG guardado ({os.path.getsize(img_out) // 1024} KB): {img_out}")

    # HTML
    html_obj = screen_obj.get("htmlCode", {}) or screen_obj.get("html_code", {})
    html_name = html_obj.get("name", "") if isinstance(html_obj, dict) else ""
    if html_name:
        res_html = call_tool("download_file", {"name": html_name})
        raw_html = res_html.get("html") or res_html.get("content") or res_html.get("data") or ""
        if raw_html:
            try:
                if not raw_html.lstrip().startswith("<"):
                    html_text = base64.b64decode(raw_html).decode("utf-8")
                else:
                    html_text = raw_html
            except Exception:
                html_text = raw_html
            with open(html_out, "w", encoding="utf-8") as f_html:
                f_html.write(html_text)
            print(f"   💻 HTML guardado ({len(html_text)} chars): {html_out}")


def main():
    assets_dir = os.path.join(BASE_DIR, "wiki", "proyectos", "assets")
    protos_dir = os.path.join(BASE_DIR, "wiki", "proyectos", "prototipos")
    os.makedirs(assets_dir, exist_ok=True)
    os.makedirs(protos_dir, exist_ok=True)

    print("🦋 Konan (UI/UX Stitch): Listando pantallas en Google Stitch Cloud...")
    all_screens = call_tool("list_screens", {"projectId": PROJECT_ID}).get("screens", [])
    print(f"📋 Total objetos en list_screens: {len(all_screens)}")

    valid_screens = []
    for s in all_screens:
        sid = s.get("name", "").split("/")[-1]
        title = s.get("title", "")
        has_html = bool(s.get("htmlCode") or s.get("html_code"))
        has_img = bool(s.get("screenshot"))
        dtype = s.get("deviceType", "")
        print(f"  - ID: {sid} | html={has_html} | img={has_img} | type={dtype} | Title: {title}")
        if has_html:
            valid_screens.append(s)

    results_summary = []
    used_ids = set()

    for idx, spec in enumerate(SCREENS_SPEC, start=1):
        slug = spec["slug"]
        matched_screen = None

        # Buscar entre las pantallas válidas con HTML que hablen de "Marchador" o coincidan con keywords
        for s in valid_screens:
            sid = s.get("name", "").split("/")[-1]
            if sid in used_ids:
                continue
            title_low = s.get("title", "").lower()
            if "marchador" in title_low and any(kw in title_low for kw in spec["keywords"]):
                matched_screen = s
                break

        if matched_screen:
            sid = matched_screen.get("name", "").split("/")[-1]
            used_ids.add(sid)
            print(f"\n[{idx}/4] ✅ Pantalla ya existente en Stitch para {slug}: {matched_screen.get('title')} ({sid})")
        else:
            print(f"\n[{idx}/4] 🎨 Generando en Stitch pantalla móvil: {slug}...")
            before_html_ids = {s.get("name", "").split("/")[-1] for s in valid_screens}
            gen_resp = call_tool(
                "generate_screen_from_text",
                {
                    "projectId": PROJECT_ID,
                    "prompt": spec["prompt"],
                    "deviceType": "MOBILE",
                    "modelId": "GEMINI_3_8_FLASH",
                },
                timeout_sec=300,
            )
            # Buscar primero dentro de gen_resp
            embedded = [s for s in find_screens_in_response(gen_resp) if s.get("htmlCode") or s.get("html_code")]
            if embedded:
                matched_screen = embedded[0]
            else:
                # Poll list_screens hasta 3 veces esperando que aparezca la pantalla con htmlCode
                for attempt in range(4):
                    time.sleep(3)
                    refreshed = call_tool("list_screens", {"projectId": PROJECT_ID}).get("screens", [])
                    valid_screens = [s for s in refreshed if s.get("htmlCode") or s.get("html_code")]
                    new_candidates = [
                        s for s in valid_screens
                        if s.get("name", "").split("/")[-1] not in before_html_ids
                        and s.get("name", "").split("/")[-1] not in used_ids
                    ]
                    if new_candidates:
                        matched_screen = new_candidates[0]
                        break

            if matched_screen:
                sid = matched_screen.get("name", "").split("/")[-1]
                used_ids.add(sid)
                print(f"   ✅ Generada: {matched_screen.get('title')} ({sid})")
            else:
                print(f"   ⚠️ No se pudo localizar el objeto screen con HTML para {slug}. Respuesta keys: {list(gen_resp.keys())}")
                continue

        download_screen_files(matched_screen, slug, assets_dir, protos_dir)
        results_summary.append(
            {
                "index": idx,
                "slug": slug,
                "title": matched_screen.get("title", spec["title_hint"]),
                "screen_id": matched_screen.get("name", "").split("/")[-1],
                "resource_name": matched_screen.get("name", ""),
                "png_path": os.path.join(assets_dir, f"{slug}.png"),
                "html_path": os.path.join(protos_dir, f"{slug}.html"),
            }
        )

    summary_path = os.path.join(BASE_DIR, "scripts", "marchador_stitch_results.json")
    with open(summary_path, "w", encoding="utf-8") as f_sum:
        json.dump(results_summary, f_sum, indent=2, ensure_ascii=False)

    print("\n" + "=" * 70)
    print("🚀 RESUMEN FINAL DE LAS 4 PANTALLAS EN GOOGLE STITCH:")
    for item in results_summary:
        print(f"  {item['index']}. {item['slug']} -> Screen ID: {item['screen_id']} | {item['title']}")
    print("=" * 70)


if __name__ == "__main__":
    main()
