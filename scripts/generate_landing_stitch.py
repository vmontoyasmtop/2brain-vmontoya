#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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

def call(name, args):
    body = json.dumps({'jsonrpc': '2.0', 'id': 1, 'method': 'tools/call', 'params': {'name': name, 'arguments': args}}).encode('utf-8')
    req = urllib.request.Request(BASE_URL, data=body, headers={'Content-Type': 'application/json'}, method='POST')
    with urllib.request.urlopen(req, timeout=180) as r:
        d = json.loads(r.read().decode())
        return json.loads(d['result']['content'][0]['text'])

prompt = """Design a hyper-modern 2026 SaaS landing page for 'SmartOps VE' - The All-in-One Autonomous Business Hub for Professionals & Retail.
Theme & Style:
- Deep luxury obsidian background (#0B132B), glowing cyan accent lights (#00E5FF), electric blue primary (#0072FF), and frosted glass cards (#161F38 with 1px cyan border rgba(0,229,255,0.15)).
- Fonts: Montserrat bold headlines, Inter for UI text and metrics.

Page Structure:
1. Navigation Header: SmartOps VE logo with glowing 'VE' badge, links to 'Soluciones', 'Booking & IA', 'Tienda', 'Precios', and 'Iniciar Sesión / Comenzar Gratis' button.
2. Hero Section:
   - Floating badge: '⚡ Nueva Era SmartOps 2026 • Agentes IA & Booking Nativo'
   - Headline: 'Vende Más, Trabaja Menos. Tu Negocio en Piloto Automático.'
   - Subtitle: 'Transforma tu presencia en un Hub Comercial autónomo: Citas en tiempo real sincronizadas con Google Calendar, Doble Digital con IA en WhatsApp, Tienda y Tarjetas Inteligentes NFC.'
   - Dual CTAs: 'Crear Mi Hub Gratis' (glowing cyan) and 'Ver Demostración en Vivo'.
   - 3D Interactive Mockup Showcase: A central floating widescreen laptop showing the SmartOps Admin Kanban dashboard, flanked by a mobile phone displaying the public booking profile and a sleek matte black NFC smart card.
3. Live Interactive Feature Bento Grid (4 Core Pillars):
   - Card 1 (Booking & Google Meet): Real-time calendar slot selector with zero-conflict scheduling and WhatsApp reminders.
   - Card 2 (Doble Digital IA): Floating chatbot bubble showing an AI agent qualifying leads and closing appointments 24/7.
   - Card 3 (Storefront & Quick Pay): Bi-monetary checkout widget ($ USD & Pago Móvil QR) for instant product/service billing.
   - Card 4 (NFC & Digital Wallet): Apple Wallet & Google Wallet pass with live dynamic updates.
4. ROI & Automation Metrics:
   - +40% aumento en conversión de leads, -8h semanales en atención manual, 99.8% reducción en inasistencias.
5. Interactive Pricing Tier Section:
   - 3 Plans: Starter ($15/mo), Profesional ($35/mo - Popular Glow), and Enterprise Retail ($75/mo).
6. Final CTA & Footer with copyright, legal and social channels.
"""

def main():
    print("🦋 Konan: Generando nueva Landing Web en Google Stitch...")
    res = call('generate_screen_from_text', {
        'projectId': PROJECT_ID,
        'prompt': prompt,
        'deviceType': 'DESKTOP',
        'modelId': 'GEMINI_3_8_FLASH'
    })
    screen_name = res.get('name')
    print(f"Pantalla Landing Web generada con exito: {screen_name}")

    s = call('get_screen', {'name': screen_name})
    html_name = s.get('htmlCode', {}).get('name')
    img_name = s.get('screenshot', {}).get('name')

    wiki_prototipos = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "wiki", "proyectos", "prototipos")
    wiki_assets = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "wiki", "proyectos", "assets")

    if html_name:
        h = call('download_file', {'name': html_name})
        out_html = os.path.join(wiki_prototipos, "stitch_smartops_landing_web_official.html")
        with open(out_html, 'w', encoding='utf-8') as f:
            f.write(h.get('html', ''))
        print(f"HTML guardado en {out_html}")

    if img_name:
        i = call('download_file', {'name': img_name})
        out_png = os.path.join(wiki_assets, "stitch_smartops_landing_web.png")
        with open(out_png, 'wb') as f:
            f.write(base64.b64decode(i.get('image', '')))
        print(f"Screenshot PNG guardado en {out_png}")

    print("Landing Web completada en Google Stitch!")

if __name__ == "__main__":
    main()
