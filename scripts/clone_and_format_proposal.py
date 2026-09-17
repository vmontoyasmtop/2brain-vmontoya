#!/usr/bin/env python3
import os
import sys
import json
import urllib.request
import urllib.parse

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
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode("utf-8"))
        return res["access_token"]

def delete_file(access_token, file_id):
    try:
        req = urllib.request.Request(
            f"https://www.googleapis.com/drive/v3/files/{file_id}",
            method="DELETE",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        with urllib.request.urlopen(req) as resp:
            print(f"🗑️ Documento borrado de Drive: {file_id}")
    except Exception as e:
        print(f"⚠️ Nota borrando documento: {e}")

def clone_and_build_proposal(access_token):
    # 1. Clonar el documento plantilla "Documento con Banner" usando Drive API files.copy
    new_title = "📋 PROPUESTA EMPRESARIAL: Presupuesto de Servidores MasterHub y Planes de IA [PROP-MGH-2026-004]"
    copy_body = json.dumps({"name": new_title}).encode("utf-8")
    
    req_copy = urllib.request.Request(
        f"https://www.googleapis.com/drive/v3/files/{TEMPLATE_FILE_ID}/copy",
        data=copy_body,
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
    )
    with urllib.request.urlopen(req_copy) as resp:
        cloned_file = json.loads(resp.read().decode("utf-8"))
        new_doc_id = cloned_file["id"]

    print(f"📋 Plantilla clonada con éxito! Nuevo Documento ID: {new_doc_id}")

    # 2. Leer contenido actual del documento clonado para reemplazar secciones conservando el banner y diseño
    req_get = urllib.request.Request(
        f"https://docs.googleapis.com/v1/documents/{new_doc_id}",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    with urllib.request.urlopen(req_get) as resp:
        doc = json.loads(resp.read().decode("utf-8"))

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
PARA: Sr. Emiliano — Dirección General, Master Group VE
DE: Ing. Víctor Montoya — Analista IT & Líder de Arquitectura
ASUNTO: Análisis Comparativo de Servidores Cloud para MasterHub (MGH) y Presupuesto Operativo de Inteligencia Artificial (IA)

1. RESUMEN EJECUTIVO
El presente documento expone la evaluación técnica y económica para el despliegue en producción de la plataforma MasterHub (MGH) —suite multimicroservicio que integra los módulos de Autenticación, Helpdesk, Inventario, Recursos Humanos y Finanzas— así como la estructura de costos para la integración de modelos de Inteligencia Artificial (IA) para automatizaciones operativas.

Cifra Consolidada de Inversión Sugerida:
• Infraestructura de Servidor Nube (MasterHub MGH): $20.00 USD / mes
• Consumo Operativo de Inteligencia Artificial (Gemini 3.6 Flash): $0.00 a $5.00 USD / mes
• INVERSIÓN TOTAL MENSUAL ESTIMADA: ~$20.00 – $25.00 USD / mes ($240.00 – $300.00 USD / año)

2. FOOTPRINT TÉCNICO DE MASTERHUB (MGH)
Para garantizar un rendimiento óptimo de la plataforma sin interrupciones ni cuellos de botella, la infraestructura hospedará los siguientes componentes activos:
• 7 Contenedores Docker Activos: frontend-ui-dashboard (Next.js 16), api-gateway (NestJS), auth-ms, inventory-ms, helpdesk-ms, hr-ms, finance-ms.
• Bases de Datos Relacionales PostgreSQL: Bases de datos aisladas y respaldadas automáticamente.
• Almacenamiento de Archivos S3 (MinIO): Para guardar comprobantes, valijas digitales, documentos de RRHH y facturas del SENIAT.

3. CUADRO COMPARATIVO DE OPCIONES DE SERVIDOR (HOSTING CLOUD)
Se auditaron 4 alternativas de mercado comparando precio, rendimiento de hardware y nivel de control:

4. ANÁLISIS DE COSTOS DE MODELOS Y PLANES DE INTELIGENCIA ARTIFICIAL (IA)
Se evaluaron las principales opciones de IA del mercado para dar soporte tanto a los asistentes de automatización corporativa (Bot ALFRED) como al procesamiento inteligente de datos en MasterHub:

5. PRESUPUESTO CONSOLIDADO FINAL PARA APROBACIÓN
1. Servidor Cloud Hetzner Dedicated vCPU (MasterHub MGH): $ 20.00 USD / mes
2. Licencia / API de Inteligencia Artificial (Google Gemini 3.6 Flash): $ 0.00 USD / mes
3. Resguardo & Copias de Seguridad Automáticas (S3 Object Storage): $ 3.00 USD / mes
----------------------------------------------------------------------------------
TOTAL INVERSIÓN MENSUAL ESTIMADA: $ 23.00 USD / mes
TOTAL INVERSIÓN ANUAL PROYECTADA: $ 276.00 USD / año
----------------------------------------------------------------------------------

Métrica de Ahorro para Master Group VE:
• Costo de Software ERP Comercial Tradicional (Profit / Odoo / SAP): $5,000.00 - $12,000.00 USD / año
• Costo de Solución Propia MasterHub (Servidor + IA): $276.00 USD / año
• AHORRO ESTIMADO PARA LA EMPRESA: > 95% de reducción de costos operativos en TI

6. PRÓXIMOS PASOS RECOMENDADOS
1. Aprobación de la Opción 1 (Hetzner Cloud) para la creación de la cuenta corporativa de servidores.
2. Configuración del Servidor VPS CPX31 y despliegue del orquestador Coolify.
3. Migración del entorno de MasterHub a producción bajo el dominio corporativo de Master Group.

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
    with urllib.request.urlopen(req_batch) as resp:
        pass

    req_get2 = urllib.request.Request(
        f"https://docs.googleapis.com/v1/documents/{new_doc_id}",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    with urllib.request.urlopen(req_get2) as resp:
        doc2 = json.loads(resp.read().decode("utf-8"))

    full_t = ""
    for elem in doc2.get("body", {}).get("content", []):
        if "paragraph" in elem:
            for p_elem in elem["paragraph"].get("elements", []):
                full_t += p_elem.get("textRun", {}).get("content", "")

    s3_idx = full_t.find("Se auditaron 4 alternativas de mercado comparando precio, rendimiento de hardware y nivel de control:")

    table_reqs = []
    if s3_idx != -1:
        pos3 = s3_idx + len("Se auditaron 4 alternativas de mercado comparando precio, rendimiento de hardware y nivel de control:") + 2
        table_reqs.append({
            "insertTable": {
                "rows": 5,
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
        with urllib.request.urlopen(req_batch_t) as resp:
            pass

    req_get3 = urllib.request.Request(
        f"https://docs.googleapis.com/v1/documents/{new_doc_id}",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    with urllib.request.urlopen(req_get3) as resp:
        doc3 = json.loads(resp.read().decode("utf-8"))

    cell_reqs = []
    table_servidores = [
        ["Opción de Proveedor", "Especificación de Hardware", "Costo Mensual", "Costo Anual", "Ventajas Competitivas"],
        ["🏆 Opción 1: Hetzner Cloud + Coolify (RECOMENDADA)", "CPX31: 4 vCPU AMD EPYC, 8 GB RAM, 160 GB NVMe SSD", "$15 – $25 USD", "$180 – $300 USD", "Costo 100% Fijo. Desempeño NVMe. Despliegue automático directo desde GitHub."],
        ["Opción 2: Híbrido PaaS (Railway / Render + Aiven)", "Microservicios Serverless + Base de datos administrada Aiven", "$35 – $65 USD", "$420 – $780 USD", "Cero gestión de Linux. Mayor costo por contenedor activo 24/7."],
        ["Opción 3: DigitalOcean", "App Platform + Managed DB + Spaces S3", "$48 – $85 USD", "$576 – $1,020 USD", "Panel de administración empresarial."],
        ["Opción 4: AWS (Amazon Web Services)", "App Runner / ECS Fargate + RDS PostgreSQL + S3", "$70 – $130 USD", "$840 – $1,560 USD", "Infraestructura tradicional. Alta complejidad y sobrecosto por ancho de banda."]
    ]

    for elem in doc3.get("body", {}).get("content", []):
        if "table" in elem:
            tbl = elem["table"]
            rows = tbl.get("tableRows", [])
            if len(rows) == 5:
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
        with urllib.request.urlopen(req_batch_c) as resp:
            pass

    try:
        perm_req = urllib.request.Request(
            f"https://www.googleapis.com/drive/v3/files/{new_doc_id}/permissions",
            data=json.dumps({"role": "reader", "type": "anyone"}).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
        )
        with urllib.request.urlopen(perm_req) as p_resp:
            pass
    except Exception as pe:
        print(f"⚠️ Permiso drive: {pe}")

    cloned_url = f"https://docs.google.com/document/d/{new_doc_id}/edit"
    print(f"✨ DOCUMENTO CLONADO Y FORMATEADO CON ÉXITO: {cloned_url}")
    return cloned_url

if __name__ == "__main__":
    token = get_access_token()
    final_url = clone_and_build_proposal(token)
    print(f"DOCUMENT_URL={final_url}")
