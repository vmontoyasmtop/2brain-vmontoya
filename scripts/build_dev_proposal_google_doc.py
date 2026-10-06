#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys, json, time, urllib.request, urllib.parse

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

GDOCS_DIR = os.path.expanduser(r"~\.gdocs-trabajo-mcp")
TOKEN_PATH = os.path.join(GDOCS_DIR, "token.json")
CREDENTIALS_PATH = os.path.join(GDOCS_DIR, "credentials.json")
if not os.path.exists(CREDENTIALS_PATH):
    CREDENTIALS_PATH = os.path.expanduser(r"~\.gcal-trabajo-mcp\credentials.json")

TEMPLATE_FILE_ID = "1zuxw18nflYFJVw0WnZRbzVvJHNJtJF1t-WUVtu967tE"

def safe_urlopen(req, retries=5, delay=2):
    for attempt in range(retries):
        try:
            return urllib.request.urlopen(req, timeout=45)
        except Exception as e:
            if attempt == retries - 1:
                raise e
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

def build_dev_proposal_doc(access_token):
    doc_title = "🤝 PROPUESTA TÉCNICA DESARROLLADOR: Módulo de Finanzas (finance-ms) — $500/Sprint"
    copy_body = json.dumps({"name": doc_title}).encode("utf-8")
    
    req_copy = urllib.request.Request(
        f"https://www.googleapis.com/drive/v3/files/{TEMPLATE_FILE_ID}/copy",
        data=copy_body,
        headers={"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    )
    resp_copy = safe_urlopen(req_copy)
    cloned_file = json.loads(resp_copy.read().decode("utf-8"))
    new_doc_id = cloned_file["id"]

    req_get = urllib.request.Request(
        f"https://docs.googleapis.com/v1/documents/{new_doc_id}",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    resp_get = safe_urlopen(req_get)
    doc = json.loads(resp_get.read().decode("utf-8"))
    end_index = doc.get("body", {}).get("content", [])[-1].get("endIndex", 1) - 1

    if end_index > 1:
        clean_requests = [{"deleteContentRange": {"range": {"startIndex": 1, "endIndex": end_index}}}]
        req_clean = urllib.request.Request(
            f"https://docs.googleapis.com/v1/documents/{new_doc_id}:batchUpdate",
            data=json.dumps({"requests": clean_requests}).encode("utf-8"),
            headers={"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
        )
        safe_urlopen(req_clean)

    doc_content = """PROPUESTA DE COLABORACIÓN TÉCNICA: DESARROLLO MÓDULO DE FINANZAS
MasterHub — Microservicio finance-ms ($500.00 USD por Sprint)

DATOS DEL ACUERDO
• Proyecto: MasterHub — Módulo de Finanzas, Facturación, SENIAT & Conciliación
• Rol: Desarrollador Co-Piloto / Fullstack UI & API Integration (Next.js / TypeScript)
• Líder Técnico: Ing. Víctor Montoya
• Esquema de Pago: $500.00 USD por Sprint liquidado contra entregable en Staging
• Total Proyecto: $2,000.00 USD (4 Sprints / 6 a 8 Semanas)


1. RESUMEN DE HITOS Y ESQUEMA DE PAGOS
"""

    insert_req = [{"insertText": {"location": {"index": 1}, "text": doc_content}}]
    req_ins = urllib.request.Request(
        f"https://docs.googleapis.com/v1/documents/{new_doc_id}:batchUpdate",
        data=json.dumps({"requests": insert_req}).encode("utf-8"),
        headers={"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    )
    safe_urlopen(req_ins)

    req_get2 = urllib.request.Request(
        f"https://docs.googleapis.com/v1/documents/{new_doc_id}",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    resp_get2 = safe_urlopen(req_get2)
    doc2 = json.loads(resp_get2.read().decode("utf-8"))
    end_doc_index = doc2.get("body", {}).get("content", [])[-1].get("endIndex", 1) - 1

    table_req = [{"insertTable": {"rows": 5, "columns": 4, "location": {"index": end_doc_index}}}]
    req_table = urllib.request.Request(
        f"https://docs.googleapis.com/v1/documents/{new_doc_id}:batchUpdate",
        data=json.dumps({"requests": table_req}).encode("utf-8"),
        headers={"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    )
    safe_urlopen(req_table)

    req_get3 = urllib.request.Request(
        f"https://docs.googleapis.com/v1/documents/{new_doc_id}",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    resp_get3 = safe_urlopen(req_get3)
    doc3 = json.loads(resp_get3.read().decode("utf-8"))

    sprint_table_data = [
        ["Sprint / Hito", "Duración", "Entregable Principal UI & Consumo API", "Pago por Hito"],
        ["Sprint 1: CxP & Retenciones", "1.5 – 2 sem", "Formularios de facturas, cálculo visual de IVA/ISLR SENIAT y tabla CxP.", "$500.00 USD"],
        ["Sprint 2: Egresos & Bancos", "1.5 – 2 sem", "Enrutamiento de cuentas, generador TXT (BNC/Provincial) y soportes S3.", "$500.00 USD"],
        ["Sprint 3: CxC & Conciliación", "1.5 – 2 sem", "Parser de extractos bancarios CSV, calculadora POS y estados de cuenta.", "$500.00 USD"],
        ["Sprint 4: Caja Chica & Release", "1.5 – 2 sem", "Arqueo de caja chica por sucursal, dashboard de métricas y pulido final.", "$500.00 USD"]
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
                        cell_requests.append({"index": start_c, "text": text_val})
                break

    cell_requests.sort(key=lambda x: x["index"], reverse=True)
    batch_cell_requests = [{"insertText": {"location": {"index": item["index"]}, "text": item["text"]}} for item in cell_requests]

    req_batch_cells = urllib.request.Request(
        f"https://docs.googleapis.com/v1/documents/{new_doc_id}:batchUpdate",
        data=json.dumps({"requests": batch_cell_requests}).encode("utf-8"),
        headers={"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    )
    safe_urlopen(req_batch_cells)

    req_get4 = urllib.request.Request(
        f"https://docs.googleapis.com/v1/documents/{new_doc_id}",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    resp_get4 = safe_urlopen(req_get4)
    doc4 = json.loads(resp_get4.read().decode("utf-8"))
    end_doc_index2 = doc4.get("body", {}).get("content", [])[-1].get("endIndex", 1) - 1

    detail_content = """

2. TÉRMINOS Y CONDICIONES DEL SERVICIO
• Pago Contra Entrega: Cada pago de $500.00 USD se libera inmediatamente tras la revisión y aprobación de las vistas funcionales en el entorno de Staging.
• Soporte y Arquitectura: El Líder Técnico (Ing. Víctor Montoya) proveerá los contratos de API, base de datos PostgreSQL, modelos Prisma y apoyo diario.
• Control de Versiones: El código se entregará a través de Pull Requests en ramas de feature organizadas en GitHub.
• Garantía: Período de 15 días posteriores al cierre de cada sprint para correcciones menores o ajustes de interfaz.


3. CONFORMIDAD Y ACEPTACIÓN

Desarrollador Colaborador:
Nombre: _____________________________________________
C.I. / ID: __________________________________________
Firma: ___________________________ Fecha: ___/___/2026

Líder Técnico MasterHub:
Ing. Víctor Montoya — Master Group VE
"""

    insert_req2 = [{"insertText": {"location": {"index": end_doc_index2}, "text": detail_content}}]
    req_ins2 = urllib.request.Request(
        f"https://docs.googleapis.com/v1/documents/{new_doc_id}:batchUpdate",
        data=json.dumps({"requests": insert_req2}).encode("utf-8"),
        headers={"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    )
    safe_urlopen(req_ins2)

    try:
        perm_req = urllib.request.Request(
            f"https://www.googleapis.com/drive/v3/files/{new_doc_id}/permissions",
            data=json.dumps({"role": "reader", "type": "anyone"}).encode("utf-8"),
            headers={"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
        )
        safe_urlopen(perm_req)
    except Exception as pe:
        pass

    final_url = f"https://docs.google.com/document/d/{new_doc_id}/edit"
    return final_url, new_doc_id

if __name__ == "__main__":
    token = get_access_token()
    url, doc_id = build_dev_proposal_doc(token)
    print(f"GOOGLE_DOC_URL={url}")
