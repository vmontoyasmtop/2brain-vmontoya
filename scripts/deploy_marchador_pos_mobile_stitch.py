#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Google Stitch Cloud Deployment — EL CUADRE MARCHADOR: MODO POS MÓVIL (VENTA & DESPACHO EN PASILLO)
==================================================================================================
Diseñadora: 🦋 Konan (El Ángel de Papel — Akatsuki Design Labs)
Propósito: Desplegar en Google Stitch Cloud (stitch.withgoogle.com) las 4 pantallas
           del Punto de Venta Móvil (Mobile POS — "Cómo se marcha y vende desde el celular")
           dentro del proyecto 'El Cuadre POS' (ID: 15301442243370859300).
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

POS_MOBILE_SCREENS = [
    {
        "slug": "stitch_el_cuadre_marchador_pos_catalogo",
        "keywords": ["pos móvil", "pos movil", "catálogo", "catalogo", "venta en pasillo", "marchar pedido"],
        "title_hint": "El Cuadre Marchador POS — Venta en Pasillo & Catálogo Táctil Mobile",
        "prompt": (
            "Design a native mobile POS screen (Flutter iOS/Android) for 'EL CUADRE MARCHADOR POS — VENTA EN PASILLO'. "
            "Theme: Dark Slate Criollo (#020617 background, #0F172A product cards, #10B981 emerald green for USD prices and primary buttons, "
            "#F59E0B amber gold for Bolívares BCV prices). "
            "Top Header: Brand title 'EL CUADRE POS MÓVIL', active seller badge 'Marchador: Carlos (Pasillo 2)', "
            "and live exchange rate pill 'Tasa BCV: Bs. 45.00 / $'. "
            "Search & Scanner Row: Instant search bar 'Buscar o escanear producto...' with integrated green camera barcode scanner icon button and voice mic button. "
            "Category Filter Pills (Horizontal scroll): '🔥 Frecuentes', '🥑 Frutas/Verduras Kg', '🧀 Charcutería', '📦 Víveres', '🥩 Carnicería'. "
            "2-Column Touch Product Grid: High-contrast product cards with photos, stock badges, quick '+' add button, and dual pricing: "
            "1) 'Harina P.A.N. 1Kg' ($1.40 / Bs. 63.00), 2) 'Queso Blanco Duro' ($5.80/Kg / Bs. 261.00), "
            "3) 'Tomate Perita' ($1.80/Kg / Bs. 81.00), 4) 'Aceite Mazeite 1L' ($2.85 / Bs. 128.25). "
            "Floating Bottom Sticky Cart Bar (Elevated glassmorphic emerald/slate panel): Shows active order '🧾 Pedido #ORD-204 • 5 Artículos', "
            "Total '$12.40 USD | Bs. 558.00', and two prominent action buttons side-by-side: "
            "amber button '🚀 Marchar a Caja' and emerald button '💳 Cobrar Aquí'."
        ),
    },
    {
        "slug": "stitch_el_cuadre_marchador_pos_pesaje",
        "keywords": ["pesaje en pasillo", "charcutería", "charcuteria", "dame bs", "calculadora de gramos"],
        "title_hint": "El Cuadre Marchador POS — Pesaje Rápido & Modo Criollo 'Dame X Bs/$'",
        "prompt": (
            "Design a native mobile POS bottom-sheet modal screen (Flutter iOS/Android) for 'EL CUADRE MARCHADOR POS — PESAJE EN PASILLO & CHARCUTERÍA'. "
            "Theme: Dark Slate Criollo (#020617 background, #0F172A modal surface, #10B981 emerald green, #F59E0B BCV amber, #38BDF8 cyan weight badges). "
            "Product Header inside Modal: '🧀 Queso Blanco Duro Llanero' with unit price '$5.80 / Kg (Bs. 261.00 / Kg)' and live scale connection badge "
            "'⚖️ Balanza Wi-Fi Pasillo #1 Conectada'. "
            "Digital Weight & Dual Price LCD Display: Large glowing digital readout showing '0.650 Kg (650g)' on the left, "
            "and live calculated total '$3.77 USD / Bs. 169.65' on the right. "
            "Quick Criollo Weight Presets (4 tactile buttons): '1/4 Kg (250g)', '1/2 Kg (500g)', '3/4 Kg (750g)', '1 Kg'. "
            "Special Venezuelan 'Modo Criollo: Dame por Monto ($ o Bs)' Card: Highlighted interactive input where the customer says "
            "'Dame Bs. 150 de queso' or 'Dame $3.00', automatically calculating the exact weight to cut ('Cortar exactamente: 0.575 Kg'). "
            "Compact numeric keypad and full-width emerald CTA button: '✅ Agregar 0.650 Kg al Pedido ($3.77 / Bs. 169.65)'."
        ),
    },
    {
        "slug": "stitch_el_cuadre_marchador_pos_ticket",
        "keywords": ["comanda", "marchar a caja", "orden #204", "cola cero", "ticket del marchador"],
        "title_hint": "El Cuadre Marchador POS — Ticket Activo & Despacho 'Marchar a Caja' (Cola Cero)",
        "prompt": (
            "Design a native mobile POS order review and dispatch screen (Flutter iOS/Android) for 'EL CUADRE MARCHADOR POS — TICKET & MARCHAR A CAJA'. "
            "Theme: Dark Slate Criollo (#020617 background, #0F172A cards, #10B981 emerald USD, #F59E0B amber Bs BCV). "
            "Top Order Header: '🧾 Pedido en Pasillo #ORD-204' with customer identifier input pill '👤 Cliente: Doña Carmen (Cesta Roja #04)' "
            "and LAN status '🟢 Sincronizado con Caja 01'. "
            "Scrollable Order Items List with tactile +/- quantity steppers: "
            "1) 'Queso Blanco Duro (0.650 Kg)' -> '$3.77 / Bs. 169.65', "
            "2) 'Harina P.A.N. 1Kg (x3 und)' -> '$4.20 / Bs. 189.00', "
            "3) 'Tomate Perita (1.200 Kg)' -> '$2.16 / Bs. 97.20', "
            "4) 'Café Amanecer 250g (x1 und)' -> '$2.27 / Bs. 102.15'. "
            "Bi-Monetary Summary Box: Subtotal '$12.40 USD', Tasa BCV 'Bs. 45.00/$', Giant Dual Total: '$12.40 USD' (emerald) and 'Bs. 558.00' (amber). "
            "QR Pre-Ticket Preview Badge: Small scannable QR code card 'Ticket Rápido Cola-Cero para escanear en Taquilla'. "
            "Dual Bottom Action Buttons: "
            "1) Primary prominent Amber-Gold button: '🚀 MARCHAR PEDIDO A CAJA PRINCIPAL (Enviar a Taquilla + Imprimir Pre-Ticket)' "
            "2) Secondary Emerald button: '💳 Cobrar Directo Aquí en el Móvil'."
        ),
    },
    {
        "slug": "stitch_el_cuadre_marchador_pos_cobro",
        "keywords": ["cobro móvil", "cobro movil", "pago móvil qr", "pago movil qr", "vuelto mixto"],
        "title_hint": "El Cuadre Marchador POS — Cobro Móvil Bimoneda (Pago Móvil QR, Mixto $/Bs & Fiado)",
        "prompt": (
            "Design a native mobile POS checkout and payment screen (Flutter iOS/Android) for 'EL CUADRE MARCHADOR POS — COBRO MÓVIL EN SITIO'. "
            "Theme: Dark Slate Criollo (#020617 background, #0F172A cards, #10B981 emerald green, #F59E0B amber BCV). "
            "Top Total Banner: Prominent dual-currency total due: 'TOTAL A COBRAR: $12.40 USD  |  Bs. 558.00 (BCV 45.00)'. "
            "Payment Method Selector Pills (2x2 or horizontal): '📲 Pago Móvil QR (Activo)', '💵 Efectivo Mixto $/Bs', '💳 Punto Inalámbrico', '📓 Anotar Fiado'. "
            "Interactive Pago Móvil & Mixed Payment Card: "
            "- Scannable Dynamic Venezuelan Pago Móvil QR Code on screen so the customer scans directly from the seller's phone, showing 'Banco Mercantil 0105 • RIF J-41234567-8 • Monto exacto: Bs. 333.00'. "
            "- Mixed Payment Breakdown: 'Recibido en Efectivo USD: $5.00' + 'Restante en Pago Móvil / Bs: Bs. 333.00 ($7.40)'. "
            "- Quick 4-digit Reference Input: 'Últimos 4 dígitos Ref: [ 8492 ]' with 'Verificar Pago' badge. "
            "- Automatic Change Calculator (Vuelto): 'Vuelto a entregar: $0.00 / Bs. 0.00 (Cuadre Exacto ✅)'. "
            "Bottom Floating Primary Emerald CTA: '✅ Completar Venta & Imprimir Ticket Bluetooth (58mm)' + WhatsApp receipt button."
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

    screenshot_obj = screen_obj.get("screenshot", {})
    screenshot_name = screenshot_obj.get("name", "") if isinstance(screenshot_obj, dict) else ""
    if screenshot_name:
        res_img = call_tool("download_file", {"name": screenshot_name})
        img_b64 = res_img.get("image") or res_img.get("content") or res_img.get("data") or ""
        if img_b64:
            with open(img_out, "wb") as f_img:
                f_img.write(base64.b64decode(img_b64))
            print(f"   🖼️ PNG guardado ({os.path.getsize(img_out) // 1024} KB): {img_out}")

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

    print("🦋 Konan (UI/UX Stitch): Desplegando las 4 pantallas de MODO POS MÓVIL (Marchar & Vender)...")
    all_screens = call_tool("list_screens", {"projectId": PROJECT_ID}).get("screens", [])
    valid_screens = [s for s in all_screens if s.get("htmlCode") or s.get("html_code")]
    used_ids = {s.get("name", "").split("/")[-1] for s in valid_screens}
    print(f"📋 Pantallas con HTML actuales en el proyecto: {len(valid_screens)}")

    results_summary = []

    for idx, spec in enumerate(POS_MOBILE_SCREENS, start=1):
        slug = spec["slug"]
        print(f"\n[{idx}/4] 🎨 Generando en Stitch pantalla POS Móvil: {slug}...")
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

        matched_screen = None
        embedded = [s for s in find_screens_in_response(gen_resp) if s.get("htmlCode") or s.get("html_code")]
        if embedded:
            matched_screen = embedded[0]
        else:
            for _ in range(5):
                time.sleep(3)
                refreshed = call_tool("list_screens", {"projectId": PROJECT_ID}).get("screens", [])
                valid_now = [s for s in refreshed if s.get("htmlCode") or s.get("html_code")]
                new_candidates = [
                    s for s in valid_now
                    if s.get("name", "").split("/")[-1] not in used_ids
                ]
                if new_candidates:
                    matched_screen = new_candidates[0]
                    break

        if matched_screen:
            sid = matched_screen.get("name", "").split("/")[-1]
            used_ids.add(sid)
            title = matched_screen.get("title", spec["title_hint"])
            print(f"   ✅ Generada: {title} ({sid})")
            download_screen_files(matched_screen, slug, assets_dir, protos_dir)
            results_summary.append(
                {
                    "index": idx,
                    "slug": slug,
                    "title": title,
                    "screen_id": sid,
                    "resource_name": matched_screen.get("name", ""),
                    "png_path": os.path.join(assets_dir, f"{slug}.png"),
                    "html_path": os.path.join(protos_dir, f"{slug}.html"),
                }
            )
        else:
            print(f"   ⚠️ No se pudo obtener el screen para {slug}")

    summary_path = os.path.join(BASE_DIR, "scripts", "marchador_pos_mobile_stitch_results.json")
    with open(summary_path, "w", encoding="utf-8") as f_sum:
        json.dump(results_summary, f_sum, indent=2, ensure_ascii=False)

    print("\n" + "=" * 70)
    print("🚀 RESUMEN DE LAS 4 PANTALLAS POS MÓVIL (MARCHAR & VENDER) EN STITCH:")
    for item in results_summary:
        print(f"  {item['index']}. {item['slug']} -> Screen ID: {item['screen_id']} | {item['title']}")
    print("=" * 70)


if __name__ == "__main__":
    main()
