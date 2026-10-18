#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script Oficial ALFRED:
Creación del Documento Ejecutivo / Propuesta de Inversión Hardware, Software y Modelo Recurrente
Proyecto: Meniox Market (POS & Gestión de Tiendas)
Destinatario: vmontoya.smartopsve@gmail.com (Cuenta Personal SmartOps)
Tarifa de Desarrollo: $8.00 USD / hora
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
            return urllib.request.urlopen(req, timeout=35)
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

def build_presentation_text():
    return """================================================================================
PROPUESTA DE INVERSIÓN & MODELO DE NEGOCIO: MENIOX MARKET
Punto de Venta (POS) & Gestión para Fruterías, Minimarkets y Víveres
================================================================================

DATOS DEL PROYECTO
• Solución: Meniox Market (Arquitectura Local-First On-Premise & Red LAN)
• Titular & Líder Técnico: Ing. Víctor Montoya (SmartOps VE)
• Correo de Gestión: vmontoya.smartopsve@gmail.com
• Tarifa de Ingeniería / Programación: $8.00 USD / hora
• Objetivo: Transformar pequeños comercios sin conocimientos tecnológicos,
  generando un flujo de ingresos por implementación + suscripción mensual recurrente.

================================================================================
1. RESUMEN EJECUTIVO: LA PROPUESTA DE VALOR
================================================================================
Meniox Market es una solución tecnológica diseñada a la medida de la realidad
comercial venezolana:
1. Funciona 100% sin internet (tolerancia total a fallas de conectividad).
2. Permite cobrar en red local (LAN) desde múltiples teléfonos o tablets sin licencias por asiento.
3. Interfaz ultra simple: pesaje de frutas/verduras en 2 toques sin calculadora.
4. Desacoplado del hardware fiscal (emisión en tickera térmica de $25 USD o fiscal si lo requiere).

================================================================================
2. ESTRUCTURA DE COSTOS DE SOFTWARE (DESARROLLO A $8.00 USD / HORA)
================================================================================
El desarrollo se estructura en 4 módulos operativos (Sprints) aprovechando el
núcleo preexistente de Meniox y adaptándolo a la modalidad Local-First:

--------------------------------------------------------------------------------
MÓDULO 1: CORE POS TÁCTIL, CATÁLOGO BIMONETARIO & PESAJE GRANEL (25 Horas)
--------------------------------------------------------------------------------
• Pantalla dividida de alta visibilidad para mostrador.
• Malla táctil con fotos grandes para frutas y verduras.
• Modal de pesaje rápido asistido con botones directos (1/4 Kg, 1/2 Kg, 1 Kg, 2 Kg).
• Buscador predictivo (3 letras) y soporte para lector de código de barras USB.
• Actualización en vivo de precios según Tasa Oficial BCV o tasa personalizada.
• Base de datos local SQLite con Prisma ORM (WAL mode, resistente a apagones).
>> Inversión de Programación: 25 horas × $8.00/h = $200.00 USD

--------------------------------------------------------------------------------
MÓDULO 2: PASARELA DE COBRO BIMONETARIA, CIERRE & ARQUEO DE CAJA (20 Horas)
--------------------------------------------------------------------------------
• Pantalla única de cobro: Punto de Débito (Voucher), Pago Móvil (QR dinámico),
  Efectivo ($ y Bs.) y Pagos Mixtos en un solo ticket.
• Calculador automático de vuelto exacto en $ o Bs. para evitar descuadres.
• Cierre de Turno y Arqueo Ciego en 2 minutos contra Lote del punto físico.
• Reporte de caja diario exportable o enviado por WhatsApp al dueño.
>> Inversión de Programación: 20 horas × $8.00/h = $160.00 USD

--------------------------------------------------------------------------------
MÓDULO 3: LIBRO DE FIADOS (CUENTAS POR COBRAR) & MERMAS (15 Horas)
--------------------------------------------------------------------------------
• Directorio de clientes de confianza con saldo adeudado y límite de crédito.
• Registro de abonos parciales o totales con comprobante por WhatsApp.
• Módulo de Merma Orgánica: baja de frutas/verduras dañadas en 2 clics.
>> Inversión de Programación: 15 horas × $8.00/h = $120.00 USD

--------------------------------------------------------------------------------
MÓDULO 4: EMPAQUETADO STANDALONE LAN, PWA & SERVICIO TÉRMICO (15 Horas)
--------------------------------------------------------------------------------
• Configuración del servidor local autónomo en puerto 3000 (red LAN multi-dispositivo).
• Instalación como PWA en modo pantalla completa (Kiosk Mode) en Windows.
• Módulo de impresión ESC/POS para tickeras térmicas USB de 58mm/80mm y pulso a gaveta.
• Script de auto-arranque con Windows (enciende la PC y el sistema queda listo).
>> Inversión de Programación: 15 horas × $8.00/h = $120.00 USD

--------------------------------------------------------------------------------
TOTAL INVERSIÓN BASE EN SOFTWARE (DESARROLLO COMPLETO):
75 Horas de Ingeniería × $8.00 USD/h = $600.00 USD
--------------------------------------------------------------------------------

================================================================================
3. INVERSIÓN DE HARDWARE (VALORES REALES DE MERCADO EN VENEZUELA)
================================================================================

A. EQUIPOS DE MOSTRADOR / PERIFÉRICOS (PRECIOS REALES CARACAS):
• Impresora Térmica 58mm USB + RJ11 (Xprinter / POS-58):          $25.00 USD
• Balanza Comercial Digital 40 Kg c/ Batería Recargable (Camry):   $38.00 USD
• Lector de Código de Barras USB Láser c/ Base Manos Libres:      $22.00 USD
• Gaveta de Dinero Metálica c/ Conexión RJ11 (4/5 Billetes):       $45.00 USD
• Mini UPS DC para Router de Internet (Respaldo 4-6h apagones):    $28.00 USD
Subtotal Periféricos de Caja:                                     $158.00 USD

B. OPCIONES DE COMPUTADORA EN VENEZUELA (SEGÚN PRESUPUESTO DEL CLIENTE):
1. Opción "Reutilización": El cliente ya posee laptop o PC en tienda:    $0.00 USD
2. Opción "Estándar Comercial": CPU Dell OptiPlex SFF + Monitor 19":   $230.00 USD
3. Opción "Mini PC Tiny Reacondicionada": HP/Dell Mini + Monitor:     $250.00 USD
4. Opción "Mini PC Nueva de Vitrina": GMKtec / Intel N95 + Monitor:   $350.00 USD

================================================================================
4. PROPUESTA ECONÓMICA INTEGRAL PARA EL CLIENTE FINAL (PACKS COMERCIALES)
================================================================================

--------------------------------------------------------------------------------
PACK 1: "ACTIVACIÓN DIGITAL" (Para comercios que ya tienen PC o Laptop)
--------------------------------------------------------------------------------
• Hardware Incluido: Balanza Digital 40 Kg + Impresora Térmica 58mm + Lector USB.
• Software: Instalación de Meniox Market, configuración LAN, carga inicial de catálogo
  y capacitación presencial de 1 hora.
• Inversión Hardware:                                             $85.00 USD
• Implementación & Licencia Software:                            $135.00 USD
TOTAL INVERSIÓN INICIAL CLIENTE:                                 $220.00 USD
+ Mensualidad de Servicio Cloud & Soporte:                       $15.00 USD / mes

--------------------------------------------------------------------------------
PACK 2: "PUESTO DE CAJA COMPLETO" (El más vendido / Todo incluido)
--------------------------------------------------------------------------------
• Hardware Incluido: CPU Dell OptiPlex SFF (8GB RAM, SSD) + Monitor 19" +
  Balanza 40 Kg + Tickera 58mm + Gaveta Metálica RJ11 + Lector Láser USB.
• Software: Instalación completa, red Wi-Fi LAN en teléfonos/tablets, carga de productos
  y capacitación operativa.
• Inversión Hardware (Todo el puesto):                           $360.00 USD
• Implementación & Licencia Software:                            $140.00 USD
TOTAL INVERSIÓN INICIAL CLIENTE:                                 $500.00 USD
+ Mensualidad de Servicio Cloud & Soporte:                       $15.00 USD / mes

--------------------------------------------------------------------------------
PACK 3: "PREMIUM COMPACTO" (Con Mini-PC Nueva Sellada)
--------------------------------------------------------------------------------
• Hardware: Mini-PC Nueva + Monitor 19" + Balanza + Tickera + Gaveta + Lector + Mini UPS.
• Software: Paquete completo de configuración, catálogo y soporte prioritario.
TOTAL INVERSIÓN INICIAL CLIENTE:                                 $650.00 USD
+ Mensualidad de Servicio Cloud & Soporte:                       $20.00 USD / mes

================================================================================
5. EL MODELO DE INGRESOS RECURRENTES (SUSCRIPCIÓN MENSUAL SaaS)
================================================================================
¿Por qué el cliente paga gustosamente la mensualidad de $15.00 a $20.00 USD?
1. Sincronización Automática de Tasa BCV: Precios actualizados diariamente sin que
   el dueño tenga que modificar producto por producto.
2. Respaldo Diario en la Nube (Cloud Backup): Si la computadora de la tienda sufre
   un daño físico, se recupera toda la información de ventas y fiados en minutos.
3. Soporte Técnico Directo por WhatsApp: Asistencia inmediata para resolver dudas
   de cajeros o problemas de impresión.
4. Reportes Ejecutivos Semanales: Envío de consolidado de ventas y cuentas por cobrar
   al WhatsApp del propietario.

PROYECCIÓN DE INGRESOS RECURRENTES (MRR):
• Con 5 comercios activos:    $75.00 USD / mes ($900.00 USD / año)
• Con 15 comercios activos:  $225.00 USD / mes ($2,700.00 USD / año)
• Con 30 comercios activos:  $450.00 USD / mes ($5,400.00 USD / año)
• Con 50 comercios activos:  $750.00 USD / mes ($9,000.00 USD / año)

================================================================================
6. RENTABILIDAD DEL DESARROLLO INICIAL ($600.00 USD A $8/H)
================================================================================
• El desarrollo del software ($600 USD de costo de horas) se amortiza y recupera
  completamente con las primeras 4 a 5 ventas del software ($135-$140 USD de cobro inicial).
• A partir del cliente N° 6, el 100% del cobro de instalación es ganancia neta directa.
• La cartera de suscripción mensual queda generando un flujo pasivo acumulativo mensual
  en dólares para SmartOps VE.
================================================================================
"""

def create_google_doc(access_token):
    title = "📊 PROPUESTA EJECUTIVA & PLAN DE INVERSIÓN: Meniox Market ($8/h + Mensualidad)"
    
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

    content = build_presentation_text()
    requests = [{
        "insertText": {
            "location": {"index": 1},
            "text": content
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
