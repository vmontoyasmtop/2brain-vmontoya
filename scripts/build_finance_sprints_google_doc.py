#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script Oficial ALFRED:
Creación y Maquetación de Documento Corporativo en Google Docs
"PLANIFICACIÓN DE SPRINTS & BACKLOG SCRUM: MÓDULO DE FINANZAS (finance-ms)"
Master Group VE & MasterHub
"""

import os
import sys
import json
import time
import urllib.request
import urllib.parse
import urllib.error

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GDOCS_DIR = os.path.expanduser(r"~\.gdocs-trabajo-mcp")
TOKEN_PATH = os.path.join(GDOCS_DIR, "token.json")
CREDENTIALS_PATH = os.path.join(GDOCS_DIR, "credentials.json")
if not os.path.exists(CREDENTIALS_PATH):
    CREDENTIALS_PATH = os.path.expanduser(r"~\.gcal-trabajo-mcp\credentials.json")

TEMPLATE_FILE_ID = "1zuxw18nflYFJVw0WnZRbzVvJHNJtJF1t-WUVtu967tE" # Master Template Oficial con Banner

def safe_urlopen(req, retries=5, delay=2):
    for attempt in range(retries):
        try:
            return urllib.request.urlopen(req, timeout=45)
        except Exception as e:
            if attempt == retries - 1:
                raise e
            print(f"⚠️ Reintento de red {attempt+1}/{retries} debido a: {e}", flush=True)
            time.sleep(delay * (attempt + 1))

def get_oauth_credentials():
    with open(CREDENTIALS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    web = data.get("web", {})
    return web.get("client_id"), web.get("client_secret")

def get_access_token():
    client_id, client_secret = get_oauth_credentials()
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

def build_finance_doc(access_token):
    doc_title = "📋 PLANIFICACIÓN DE SPRINTS & BACKLOG SCRUM: Módulo de Finanzas (finance-ms) — MasterHub"
    copy_body = json.dumps({"name": doc_title}).encode("utf-8")
    
    print("1. Clonando plantilla oficial corporativa de Master Group...")
    req_copy = urllib.request.Request(
        f"https://www.googleapis.com/drive/v3/files/{TEMPLATE_FILE_ID}/copy",
        data=copy_body,
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
    )
    resp_copy = safe_urlopen(req_copy)
    cloned_file = json.loads(resp_copy.read().decode("utf-8"))
    new_doc_id = cloned_file["id"]
    print(f"✅ Plantilla clonada exitosamente en Google Drive. ID: {new_doc_id}")

    # Obtener contenido actual para vaciar el cuerpo viejo preservando el header
    req_get = urllib.request.Request(
        f"https://docs.googleapis.com/v1/documents/{new_doc_id}",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    resp_get = safe_urlopen(req_get)
    doc = json.loads(resp_get.read().decode("utf-8"))
    end_index = doc.get("body", {}).get("content", [])[-1].get("endIndex", 1) - 1

    clean_requests = []
    if end_index > 1:
        clean_requests.append({
            "deleteContentRange": {
                "range": {
                    "startIndex": 1,
                    "endIndex": end_index
                }
            }
        })
        req_clean = urllib.request.Request(
            f"https://docs.googleapis.com/v1/documents/{new_doc_id}:batchUpdate",
            data=json.dumps({"requests": clean_requests}).encode("utf-8"),
            headers={"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
        )
        safe_urlopen(req_clean)
        print("✅ Cuerpo anterior limpiado preservando encabezado y banner corporativo.")

    doc_content = """PLANIFICACIÓN DE SPRINTS & BACKLOG SCRUM: MÓDULO DE FINANZAS (finance-ms)
Plan de Trabajo Ágil Acelerado (Plan B Exprés Fast-Track) — MasterHub

DATOS DE IDENTIFICACIÓN CORPORATIVA
• Empresa / Plataforma: Master Group VE — MasterHub
• Módulo: Finanzas & Gestión Fiscal (finance-ms)
• Responsable Técnico: Ing. Víctor Montoya (Analista IT & Desarrollador Principal)
• Modalidad: Plan B Exprés por Premura (Fast-Track) — 4 Sprints Timeboxed (6 Semanas Totales)
• Presupuesto & Hitos: 67 Story Points (SP) | Inversión: $6,000.00 USD ($1,500.00 USD por Hito de Sprint)
• Trazabilidad ClickUp: Espacio MasterHub / 1er Fase (Tarea Padre ID: MS-FINANZAS #86bb7qxde)


1. RESUMEN EJECUTIVO & CRONOGRAMA DE SPRINTS
El presente documento define la planificación técnica detallada para el desarrollo e implementación del Módulo de Finanzas (finance-ms) de MasterHub.

La metodología seleccionada es Scrum Fast-Track, organizada en 4 Sprints iterativos de 1.5 semanas de duración cada uno, garantizando la puesta en marcha progresiva y la entrega de valor funcional inmediato en cuentas por pagar, cálculo fiscal SENIAT, pagos bancarios masivos, conciliación de ventas y control de caja chica.


2. MATRIZ DE CRONOGRAMA POR SPRINT E HITOS FINANCIEROS
"""

    print("2. Insertando texto maestro inicial...")
    insert_req = [{
        "insertText": {
            "location": {"index": 1},
            "text": doc_content
        }
    }]
    req_ins = urllib.request.Request(
        f"https://docs.googleapis.com/v1/documents/{new_doc_id}:batchUpdate",
        data=json.dumps({"requests": insert_req}).encode("utf-8"),
        headers={"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    )
    safe_urlopen(req_ins)
    print("✅ Texto inicial insertado.")

    # 3. Obtener el índice final para insertar la tabla de Sprints
    req_get2 = urllib.request.Request(
        f"https://docs.googleapis.com/v1/documents/{new_doc_id}",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    resp_get2 = safe_urlopen(req_get2)
    doc2 = json.loads(resp_get2.read().decode("utf-8"))
    end_doc_index = doc2.get("body", {}).get("content", [])[-1].get("endIndex", 1) - 1

    print("3. Insertando tabla nativa para el Cronograma de Sprints (5 filas x 6 columnas)...")
    table_req = [{
        "insertTable": {
            "rows": 5,
            "columns": 6,
            "location": {"index": end_doc_index}
        }
    }]
    req_table = urllib.request.Request(
        f"https://docs.googleapis.com/v1/documents/{new_doc_id}:batchUpdate",
        data=json.dumps({"requests": table_req}).encode("utf-8"),
        headers={"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    )
    safe_urlopen(req_table)
    print("✅ Tabla de Sprints creada.")

    # 4. Poblar celdas de la tabla de Sprints
    req_get3 = urllib.request.Request(
        f"https://docs.googleapis.com/v1/documents/{new_doc_id}",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    resp_get3 = safe_urlopen(req_get3)
    doc3 = json.loads(resp_get3.read().decode("utf-8"))

    sprint_table_data = [
        ["Sprint", "Fechas de Ejecución", "Duración", "Story Points", "Entregable Clave", "Hito Financiero"],
        ["Sprint 1", "17/09 – 27/09/2026", "1.5 sem", "21 SP", "MVP CxP, Motor Fiscal SENIAT, Tasa BCV & Propuesta Pago PDF", "$1,500.00 USD"],
        ["Sprint 2", "28/09 – 08/10/2026", "1.5 sem", "18 SP", "Egresos, Enrutamiento BNC/Provincial, TXT Bancario & MinIO S3", "$1,500.00 USD"],
        ["Sprint 3", "09/10 – 19/10/2026", "1.5 sem", "15 SP", "CxC, Conciliación Masiva CSV & Calculadora Comisiones POS", "$1,500.00 USD"],
        ["Sprint 4", "20/10 – 30/10/2026", "1.5 sem", "13 SP", "Caja Chica, Cuota Marketing 4%, Audit Logs SENIAT & Release", "$1,500.00 USD"]
    ]

    cell_requests = []
    for elem in doc3.get("body", {}).get("content", []):
        if "table" in elem:
            tbl = elem["table"]
            rows = tbl.get("tableRows", [])
            if len(rows) == 5:
                for r_idx, row in enumerate(rows):
                    cells = row.get("tableCells", [])
                    for c_idx, cell in enumerate(cells):
                        start_c = cell.get("content", [])[0].get("startIndex")
                        text_val = sprint_table_data[r_idx][c_idx]
                        cell_requests.append({
                            "index": start_c,
                            "text": text_val
                        })
                break

    cell_requests.sort(key=lambda x: x["index"], reverse=True)
    batch_cell_requests = [{
        "insertText": {
            "location": {"index": item["index"]},
            "text": item["text"]
        }
    } for item in cell_requests]

    print("4. Poblando celdas de la tabla de Sprints...")
    req_batch_cells = urllib.request.Request(
        f"https://docs.googleapis.com/v1/documents/{new_doc_id}:batchUpdate",
        data=json.dumps({"requests": batch_cell_requests}).encode("utf-8"),
        headers={"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    )
    safe_urlopen(req_batch_cells)
    print("✅ Celdas de tabla de Sprints pobladas.")

    # 5. Insertar el desglose detallado de historias de usuario tras la tabla
    req_get4 = urllib.request.Request(
        f"https://docs.googleapis.com/v1/documents/{new_doc_id}",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    resp_get4 = safe_urlopen(req_get4)
    doc4 = json.loads(resp_get4.read().decode("utf-8"))
    end_doc_index2 = doc4.get("body", {}).get("content", [])[-1].get("endIndex", 1) - 1

    stories_content = """

3. DESGLOSE DETALLADO DE HISTORIAS DE USUARIO POR SPRINT

3.1. SPRINT 1: MVP Cuentas por Pagar (CxP) & Motor Fiscal SENIAT
• Fechas & Esfuerzo: 17/09/2026 – 27/09/2026 | 1.5 Semanas | 21 Story Points | Hito: $1,500.00 USD
• Tarea ClickUp: ID #86bc224z8
• Objetivo del Sprint: Automatizar la recepción de facturas, cálculo fiscal SENIAT y generación del reporte PDF de propuesta de pago semanal los martes a las 5:00 PM.

Historias de Usuario:
• US 1.1: Modelado Prisma ORM & Base de Datos (4h | 3 SP)
  Crear el esquema de base de datos relacional con Prisma ORM para entidades Supplier, AccountPayable, TaxRetention y PaymentProposal, garantizando integridad referencial y trazabilidad.
• US 1.2: API CxP & Sincronización Tasa Oficial BCV (6h | 5 SP)
  Desarrollar API para registro de facturas multimoneda (USD/Bs) y consulta automatizada de la tasa oficial del Banco Central de Venezuela (BCV), congelando el monto en bolívares a la fecha de emisión.
• US 1.3: Motor Fiscal SENIAT — Retenciones de IVA e ISLR (6h | 5 SP)
  Implementar la lógica tributaria que aplica retenciones del 75% o 100% de IVA y deducciones de ISLR según la categoría fiscal del proveedor, emitiendo automáticamente el comprobante oficial de 14 dígitos (YYYYMMXXXXXXXX).
• US 1.4: Cronjob de Propuesta Semanal de Pago en PDF (6h | 5 SP)
  Configurar servicio programado que genera todos los martes a las 5:00 PM un documento PDF consolidado con las facturas listas para aprobación de pago por parte de Dirección General.
• US 1.5: UI React / Next.js para Carga y Aprobación de Facturas (8h | 3 SP)
  Construir interfaces de usuario modernas en MasterHub con tablas interactivas, filtros por sucursal y modales de aprobación de lotes de pago.


3.2. SPRINT 2: Egresos, Enrutamiento Bancario & Archivos TXT
• Fechas & Esfuerzo: 28/09/2026 – 08/10/2026 | 1.5 Semanas | 18 Story Points | Hito: $1,500.00 USD
• Tarea ClickUp: ID #86bc2251g
• Objetivo del Sprint: Automatizar la emisión de pagos masivos mediante enrutamiento de cuentas (BNC / Banco Provincial) y generación de lotes TXT estructurados.

Historias de Usuario:
• US 2.1: Enrutamiento Inteligente de Cuentas Bancarias (8h | 5 SP)
  Asociar dinámicamente cuentas bancarias origen y destino por sucursal y banco emisor para optimizar transferencias y minimizar comisiones interbancarias.
• US 2.2: Generador de Lotes TXT Bancarios BNC & Provincial (8h | 5 SP)
  Exportar lotes de pago estructurados en formato TXT oficial conforme a los manuales técnicos de Banco Nacional de Crédito (BNC) y Banco Provincial para su carga directa en banca en línea.
• US 2.3: Gestión de Soportes Digitales en MinIO S3 (8h | 5 SP)
  Implementar repositorio seguro de valija digital (comprobantes de transferencia y facturas PDF/JPG) alojado en MinIO (S3 compatible), vinculado a cada egreso.
• US 2.4: Módulo de Conciliación Manual de Egresos (6h | 3 SP)
  Permitir el marcado de pagos como liquidados con registro del número de referencia bancaria para cierre de ciclo de egresos.


3.3. SPRINT 3: Cuentas por Cobrar (CxC) & Conciliación Masiva CSV
• Fechas & Esfuerzo: 09/10/2026 – 19/10/2026 | 1.5 Semanas | 15 Story Points | Hito: $1,500.00 USD
• Tarea ClickUp: ID #86bc22532
• Objetivo del Sprint: Cruzar automáticamente extractos bancarios CSV con las ventas de Xetux, calculando comisiones POS (0.30%) y retención ISLR TC (2%).

Historias de Usuario:
• US 3.1: Parser de Extractos Bancarios CSV & Conciliación Masiva (10h | 5 SP)
  Módulo de carga y procesamiento de extractos bancarios en CSV para cruce automatizado contra ventas diarias por fecha, lote y monto.
• US 3.2: Calculadora de Comisiones POS (0.30%) y Retención ISLR TC (2%) (10h | 5 SP)
  Deducción automática de comisiones bancarias por punto de venta y retenciones fiscales en tarjetas de débito/crédito para el cálculo exacto del ingreso neto.
• US 3.3: Estado de Cuenta de Clientes & Reclamaciones CxC (10h | 5 SP)
  Visualización unificada de saldos pendientes, notas de crédito y seguimiento de cobranzas para clientes corporativos.


3.4. SPRINT 4: Caja Chica, Cuota Marketing (4%), Audit Logs & Release
• Fechas & Esfuerzo: 20/10/2026 – 30/10/2026 | 1.5 Semanas | 13 Story Points | Hito: $1,500.00 USD
• Tarea ClickUp: ID #86bc225cr
• Objetivo del Sprint: Arqueo de caja chica por sucursal, automatización de la cuota de marketing (4%), trazabilidad SENIAT y despliegue final en producción.

Historias de Usuario:
• US 4.1: Arqueo e Inspección de Caja Chica Semanal (8h | 3 SP)
  Registro de gastos menores, vales provisionales y solicitud de reposición de fondo fijo semanal por sucursal con validación de comprobantes.
• US 4.2: Deducción Automática de Cuota de Marketing (4%) (6h | 3 SP)
  Cálculo y deducción automática del 4% sobre ventas brutas de cada sede destinado al fondo corporativo de mercadeo y publicidad.
• US 4.3: Audit Logs & Trazabilidad Fiscal SENIAT (10h | 5 SP)
  Historial inalterable de auditoría con registro de usuario, timestamp, IP y acción en comprobantes de retención para garantizar cumplimiento normativo.
• US 4.4: Despliegue en Staging / Producción & Cierre (6h | 2 SP)
  Ejecución de migraciones finales en bases de datos PostgreSQL, configuración en Hetzner Cloud con Coolify y puesta en marcha 100% operativa.


4. CONFORMIDAD Y APROBACIÓN EJECUTIVA

Desarrollador / Líder Técnico IT:
Ing. Víctor Montoya — MasterHub / Xetux

Aprobación Dirección General / Administración:
Dirección General — Master Group VE
"""

    print("5. Insertando detalle de historias de usuario y conformidad...")
    insert_req2 = [{
        "insertText": {
            "location": {"index": end_doc_index2},
            "text": stories_content
        }
    }]
    req_ins2 = urllib.request.Request(
        f"https://docs.googleapis.com/v1/documents/{new_doc_id}:batchUpdate",
        data=json.dumps({"requests": insert_req2}).encode("utf-8"),
        headers={"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    )
    safe_urlopen(req_ins2)
    print("✅ Detalle de historias de usuario insertado con éxito.")

    # 6. Aplicar estilos nativos (TITLE, SUBTITLE, HEADING_1, HEADING_2, HEADING_3)
    print("6. Aplicando estilos y jerarquías tipográficas nativas de Google Docs...")
    req_get5 = urllib.request.Request(
        f"https://docs.googleapis.com/v1/documents/{new_doc_id}",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    resp_get5 = safe_urlopen(req_get5)
    doc5 = json.loads(resp_get5.read().decode("utf-8"))

    style_requests = []
    for elem in doc5.get("body", {}).get("content", []):
        if "paragraph" in elem:
            p = elem["paragraph"]
            p_text = ""
            for pe in p.get("elements", []):
                p_text += pe.get("textRun", {}).get("content", "")
            
            p_clean = p_text.strip()
            p_start = elem.get("startIndex")
            p_end = elem.get("endIndex")

            if p_clean.startswith("PLANIFICACIÓN DE SPRINTS & BACKLOG SCRUM: MÓDULO DE FINANZAS"):
                style_requests.append({
                    "updateParagraphStyle": {
                        "range": {"startIndex": p_start, "endIndex": p_end},
                        "paragraphStyle": {"namedStyleType": "TITLE"},
                        "fields": "namedStyleType"
                    }
                })
            elif p_clean.startswith("Plan de Trabajo Ágil Acelerado"):
                style_requests.append({
                    "updateParagraphStyle": {
                        "range": {"startIndex": p_start, "endIndex": p_end},
                        "paragraphStyle": {"namedStyleType": "SUBTITLE"},
                        "fields": "namedStyleType"
                    }
                })
            elif any(p_clean.startswith(prefix) for prefix in [
                "1. RESUMEN EJECUTIVO",
                "2. MATRIZ DE CRONOGRAMA",
                "3. DESGLOSE DETALLADO",
                "4. CONFORMIDAD Y APROBACIÓN"
            ]):
                style_requests.append({
                    "updateParagraphStyle": {
                        "range": {"startIndex": p_start, "endIndex": p_end},
                        "paragraphStyle": {"namedStyleType": "HEADING_1"},
                        "fields": "namedStyleType"
                    }
                })
            elif any(p_clean.startswith(prefix) for prefix in [
                "3.1. SPRINT 1",
                "3.2. SPRINT 2",
                "3.3. SPRINT 3",
                "3.4. SPRINT 4"
            ]):
                style_requests.append({
                    "updateParagraphStyle": {
                        "range": {"startIndex": p_start, "endIndex": p_end},
                        "paragraphStyle": {"namedStyleType": "HEADING_2"},
                        "fields": "namedStyleType"
                    }
                })

    if style_requests:
        req_styles = urllib.request.Request(
            f"https://docs.googleapis.com/v1/documents/{new_doc_id}:batchUpdate",
            data=json.dumps({"requests": style_requests}).encode("utf-8"),
            headers={"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
        )
        safe_urlopen(req_styles)
        print(f"✅ {len(style_requests)} estilos nativos aplicados.")

    # 7. Configurar permisos de lectura en Google Drive
    print("7. Configurando permisos en Google Drive...")
    try:
        perm_req = urllib.request.Request(
            f"https://www.googleapis.com/drive/v3/files/{new_doc_id}/permissions",
            data=json.dumps({"role": "reader", "type": "anyone"}).encode("utf-8"),
            headers={"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
        )
        safe_urlopen(perm_req)
        print("✅ Permiso de lectura pública ('anyone'/'reader') configurado.")
    except Exception as pe:
        print(f"⚠️ Permiso Drive: {pe}")

    final_url = f"https://docs.google.com/document/d/{new_doc_id}/edit"
    print(f"\n🎉 GOOGLE DOC OFICIAL GENERADO EXITOSAMENTE:\n👉 {final_url}\n")
    return final_url, new_doc_id

if __name__ == "__main__":
    token = get_access_token()
    url, doc_id = build_finance_doc(token)
    print(f"RESULT_URL={url}")
    print(f"DOC_ID={doc_id}")
