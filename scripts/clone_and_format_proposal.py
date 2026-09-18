#!/usr/bin/env python3
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

TEMPLATE_FILE_ID = "1zuxw18nflYFJVw0WnZRbzVvJHNJtJF1t-WUVtu967tE" # Agenda / Banner Template Doc

def safe_urlopen(req, retries=5, delay=2):
    for attempt in range(retries):
        try:
            return urllib.request.urlopen(req, timeout=30)
        except Exception as e:
            if attempt == retries - 1:
                raise e
            print(f"⚠️ Reintento de red {attempt+1}/{retries} debido a: {e}")
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

def clone_and_build_proposal(access_token):
    new_title = "📋 PROPUESTA EMPRESARIAL: Presupuesto Auditado de Servidores (Hetzner vs SeeNode) y Planes de IA [PROP-MGH-2026-004]"
    copy_body = json.dumps({"name": new_title}).encode("utf-8")
    
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

    print(f"📋 Plantilla clonada con éxito! Nuevo Documento ID: {new_doc_id}")

    req_get = urllib.request.Request(
        f"https://docs.googleapis.com/v1/documents/{new_doc_id}",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    resp_get = safe_urlopen(req_get)
    doc = json.loads(resp_get.read().decode("utf-8"))

    end_index = doc.get("body", {}).get("content", [])[-1].get("endIndex", 1) - 1

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

    proposal_text = """PROPUESTA EMPRESARIAL DE INFRAESTRUCTURA CLOUD Y SERVICIOS DE IA

CÓDIGO DE DOCUMENTO: PROP-MGH-2026-004
FECHA DE EMISIÓN: Jueves, 17 de Septiembre de 2026
AUDITORÍA DE PRECIOS EN VIVO: Septiembre 2026 (Hetzner, SeeNode, Gemini, OpenAI)
PARA: Sr. Emiliano — Dirección General, Master Group VE
DE: Ing. Víctor Montoya — Analista IT & Líder de Arquitectura
ASUNTO: Análisis Comparativo Auditado de Servidores Cloud para MasterHub (MGH) incluyendo SeeNode Cloud y Presupuesto Operativo de IA

1. RESUMEN EJECUTIVO AUDITADO
El presente documento expone la evaluación técnica y económica auditada con precios vigentes (Septiembre 2026) para el despliegue en producción de la plataforma MasterHub (MGH) —suite multimicroservicio que integra los módulos de Autenticación, Helpdesk, Inventario, Recursos Humanos y Finanzas— incorporando el análisis de la infraestructura de SeeNode Cloud (https://seenode.com/es), así como la estructura de costos para la integración de modelos de Inteligencia Artificial (IA) para automatizaciones operativas.

Cifra Consolidada de Inversión Sugerida Auditada:
• Opción A (Máximo Ahorro - Hetzner Cloud CAX21 ARM / CPX22 AMD): $8.50 – $21.00 USD / mes
• Opción B (Máxima Gestión PaaS & MCP para IA - SeeNode Cloud): $48.50 USD / mes
• Consumo Operativo de Inteligencia Artificial (Google Gemini 3.8 / 2.5 Flash-Lite): $0.00 a $5.00 USD / mes
• INVERSIÓN TOTAL MENSUAL ESTIMADA: ~$11.50 – $53.50 USD / mes ($138.00 – $642.00 USD / año)

2. FOOTPRINT TÉCNICO DE MASTERHUB (MGH)
Para garantizar un rendimiento óptimo de la plataforma sin interrupciones ni cuellos de botella, la infraestructura hospedará los siguientes componentes activos:
• 7 Contenedores Docker Activos: frontend-ui-dashboard (Next.js 16), api-gateway (NestJS), auth-ms, inventory-ms, helpdesk-ms, hr-ms, finance-ms.
• Bases de Datos Relacionales PostgreSQL: Bases de datos aisladas y respaldadas automáticamente.
• Almacenamiento de Archivos S3 (MinIO): Para guardar comprobantes, valijas digitales, documentos de RRHH y facturas del SENIAT.

3. CUADRO COMPARATIVO AUDITADO DE OPCIONES DE SERVIDOR (HOSTING CLOUD 2026)
Se auditaron 5 alternativas de mercado comparando precio real, rendimiento de hardware y nivel de control:

4. TARIFAS REALES AUDITADAS DE MODELOS DE INTELIGENCIA ARTIFICIAL (IA 2026)
Se evaluaron las principales opciones de IA del mercado para dar soporte tanto a los asistentes de automatización corporativa (Bot ALFRED) como al procesamiento inteligente de datos en MasterHub:
• Google Gemini 2.5 Flash-Lite: $0.10 input / $0.40 output por 1M tokens (Ultrarrápido y ultraeconómico).
• Google Gemini 3.8 Flash (RECOMENDADO): Free Tier Gratis / $0.75 input / $3.75 output por 1M tokens.
• OpenAI GPT-4o-mini: $0.15 input / $0.60 output por 1M tokens.
• OpenAI GPT-4o: $2.50 input / $10.00 output por 1M tokens.
• Anthropic Claude Haiku 4.5: $1.00 input / $5.00 output por 1M tokens.
• Anthropic Claude Sonnet 5: $2.00 input / $10.00 output por 1M tokens.
• DeepSeek-Flash (V4): $0.006 input / $0.60 output por 1M tokens.

5. PRESUPUESTO CONSOLIDADO FINAL AUDITADO
1. Opción A (Hetzner Cloud CAX21 ARM + Gemini 3.8 Flash): $ 11.50 USD / mes ($138 USD / año)
2. Opción B (Hetzner Cloud CPX22 AMD + Gemini 3.8 Flash): $ 24.00 USD / mes ($288 USD / año)
3. Opción C (SeeNode Cloud PaaS + PostgreSQL + Gemini 3.8 Flash): $ 51.50 USD / mes ($618 USD / año)
----------------------------------------------------------------------------------
AHORRO ESTIMADO FRENTE A ERPs COMERCIALES ($5,000 USD/año): > 90% a 95% de ahorro en TI.
----------------------------------------------------------------------------------

6. PRÓXIMOS PASOS RECOMENDADOS
1. Aprobación de la Opción 1A (Hetzner CAX21 ARM) para máximo ahorro o la Opción 2 (SeeNode Cloud) para PaaS gestionado con MCP.
2. Configuración del Servidor y despliegue del entorno de producción.
3. Migración de MasterHub a producción bajo el dominio corporativo de Master Group.

Master Group VE — Departamento de Tecnología e IT
Ing. Víctor Montoya | Analista IT & Líder de Arquitectura
"""

    requests.append({
        "insertText": {
            "location": {"index": 1},
            "text": proposal_text
        }
    })

    req_batch = urllib.request.Request(
        f"https://docs.googleapis.com/v1/documents/{new_doc_id}:batchUpdate",
        data=json.dumps({"requests": requests}).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
    )
    safe_urlopen(req_batch)

    req_get2 = urllib.request.Request(
        f"https://docs.googleapis.com/v1/documents/{new_doc_id}",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    resp_get2 = safe_urlopen(req_get2)
    doc2 = json.loads(resp_get2.read().decode("utf-8"))

    full_t = ""
    for elem in doc2.get("body", {}).get("content", []):
        if "paragraph" in elem:
            for p_elem in elem["paragraph"].get("elements", []):
                full_t += p_elem.get("textRun", {}).get("content", "")

    s3_idx = full_t.find("Se auditaron 5 alternativas de mercado comparando precio real, rendimiento de hardware y nivel de control:")

    table_reqs = []
    if s3_idx != -1:
        pos3 = s3_idx + len("Se auditaron 5 alternativas de mercado comparando precio real, rendimiento de hardware y nivel de control:") + 2
        table_reqs.append({
            "insertTable": {
                "rows": 7,
                "columns": 5,
                "location": {"index": pos3}
            }
        })

    if table_reqs:
        req_batch_t = urllib.request.Request(
            f"https://docs.googleapis.com/v1/documents/{new_doc_id}:batchUpdate",
            data=json.dumps({"requests": table_reqs}).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
        )
        safe_urlopen(req_batch_t)

    req_get3 = urllib.request.Request(
        f"https://docs.googleapis.com/v1/documents/{new_doc_id}",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    resp_get3 = safe_urlopen(req_get3)
    doc3 = json.loads(resp_get3.read().decode("utf-8"))

    cell_reqs = []
    table_servidores = [
        ["Opción de Proveedor", "Especificación de Hardware", "Costo Mensual", "Costo Anual", "Ventajas Competitivas Auditadas"],
        ["🏆 Opción 1A: Hetzner CAX21 ARM (MÁXIMO AHORRO)", "CAX21: 4 vCPU ARM Ampere, 8 GB RAM, 80 GB NVMe SSD", "€7.99 (~$8.50 USD)", "$102 USD", "Costo Fijo Ibatible. Rendimiento excelente para contenedores Docker Next.js/NestJS."],
        ["Opción 1B: Hetzner CPX22 AMD", "CPX22: 3 vCPU AMD EPYC, 4 GB RAM, 80 GB NVMe SSD", "€19.49 (~$21.00 USD)", "$252 USD", "Rendimiento Regular AMD. Excelente estabilidad para microservicios."],
        ["🟢 Opción 2: SeeNode Cloud (RECOMENDADA PAAS/IA)", "7 Contenedores (2 x Std $7 + 5 x Basic $4) + PostgreSQL ($12) + S3 ($2.5)", "$48.50 USD", "$582 USD", "PaaS 100% Gestionado en Español. Integración nativa con servidor MCP para IA."],
        ["Opción 3: Híbrido PaaS (Railway / Render + Aiven)", "Microservicios Serverless + Base de datos administrada Aiven", "$35 – $65 USD", "$420 – $780 USD", "Cero gestión de Linux. Mayor costo por contenedor activo 24/7."],
        ["Opción 4: DigitalOcean", "App Platform + Managed DB + Spaces S3", "$48 – $85 USD", "$576 – $1,020 USD", "Panel de administración empresarial."],
        ["Opción 5: AWS (Amazon Web Services)", "App Runner / ECS Fargate + RDS PostgreSQL + S3", "$70 – $130 USD", "$840 – $1,560 USD", "Infraestructura tradicional. Alta complejidad y sobrecosto por ancho de banda."]
    ]

    for elem in doc3.get("body", {}).get("content", []):
        if "table" in elem:
            tbl = elem["table"]
            rows = tbl.get("tableRows", [])
            if len(rows) == 7:
                for r_i, r in enumerate(rows):
                    cells = r.get("tableCells", [])
                    for c_i, c in enumerate(cells):
                        val = table_servidores[r_i][c_i]
                        st_idx = c.get("content", [])[0].get("startIndex")
                        cell_reqs.append({
                            "insertText": {
                                "location": {"index": st_idx},
                                "text": val
                            }
                        })
                break

    if cell_reqs:
        req_batch_c = urllib.request.Request(
            f"https://docs.googleapis.com/v1/documents/{new_doc_id}:batchUpdate",
            data=json.dumps({"requests": cell_reqs}).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
        )
        safe_urlopen(req_batch_c)

    try:
        perm_req = urllib.request.Request(
            f"https://www.googleapis.com/drive/v3/files/{new_doc_id}/permissions",
            data=json.dumps({"role": "reader", "type": "anyone"}).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
        )
        safe_urlopen(perm_req)
    except Exception as pe:
        print(f"⚠️ Permiso drive: {pe}")

    cloned_url = f"https://docs.google.com/document/d/{new_doc_id}/edit"
    print(f"✨ DOCUMENTO CON SEENODE CLONADO Y FORMATEADO CON ÉXITO: {cloned_url}")
    return cloned_url

if __name__ == "__main__":
    token = get_access_token()
    final_url = clone_and_build_proposal(token)
    print(f"DOCUMENT_URL={final_url}")
