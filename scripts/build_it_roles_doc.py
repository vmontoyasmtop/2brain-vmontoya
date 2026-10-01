#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script Oficial ALFRED:
Creación y Maquetación de Documento Corporativo en Google Docs
"MANUAL ORGANIZACIONAL Y DESCRIPTIVO DE CARGOS DEL DEPARTAMENTO DE IT"
Master Group VE & Xetux
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

TEMPLATE_FILE_ID = "1zuxw18nflYFJVw0WnZRbzVvJHNJtJF1t-WUVtu967tE" # Master Template con Banner

def safe_urlopen(req, retries=5, delay=2):
    for attempt in range(retries):
        try:
            return urllib.request.urlopen(req, timeout=45)
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

def build_document(access_token):
    doc_title = "📋 MANUAL ORGANIZACIONAL: Descriptivo de Cargos del Departamento de IT (Líder IT, Devs, QA, Soporte N1)"
    copy_body = json.dumps({"name": doc_title}).encode("utf-8")
    
    print("1. Clonando plantilla oficial corporativa...")
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
    print(f"✅ Plantilla clonada exitosamente. ID: {new_doc_id}")

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
        print("✅ Cuerpo anterior limpiado preservando encabezado oficial.")

    # Construcción del texto maestro sin marcas Markdown crudas
    doc_content = """MANUAL ORGANIZACIONAL Y DESCRIPTIVO DE CARGOS DEL DEPARTAMENTO DE IT
Estructura Operativa, Perfiles de Cargo, Matriz de Responsabilidades y KPIs

DATOS DE IDENTIFICACIÓN CORPORATIVA
• Empresa: Master Group VE
• Departamento: Tecnología, Desarrollo e Infraestructura IT
• Autor y Líder del Área: Ing. Víctor Montoya
• Aprobación: Dirección General (Sr. Emiliano) & Recursos Humanos
• Versión: 1.0 Oficial (Septiembre 2026)


1. PROPÓSITO GENERAL Y JUSTIFICACIÓN DEL DOCUMENTO
El presente manual tiene por objeto formalizar la arquitectura de roles, responsabilidades, dependencias jerárquicas e indicadores clave de gestión (KPIs) del Departamento de Tecnología de Master Group VE.

1.1. Diagnóstico de Eficiencia y Separación de Enfoques (Context Switching)
En la etapa inicial, la concentración simultánea de desarrollo estratégico de software corporativo (MasterHub) y de soporte técnico reactivo de campo (asistencia telefónica a cajeros de Xetux, cambio de consumibles, reparación de impresoras y cableado) en una misma figura técnica generaba una severa penalización cognitiva por cambio constante de contexto.

Para maximizar el retorno de inversión en tecnología y garantizar la estabilidad total de la empresa, el departamento se divide en dos alas de trabajo complementarias:
a) Ala de Ingeniería y Calidad de Software: Enfocada en innovación, desarrollo continuo de MasterHub (Finanzas, RRHH, Helpdesk, Inventario) y aseguramiento de calidad previa a producción.
b) Ala de Soporte Operativo e Infraestructura de Campo: Enfocada en la continuidad ininterrumpida de puestos de trabajo, atención inmediata en tiendas Xetux y auditoría física semanal de inventario.


2. ESTRUCTURA ORGANIGRAFICA DEL DEPARTAMENTO DE IT
Dirección General (Sr. Emiliano)
    └── Líder de IT & Arquitectura Tecnológica (Ing. Víctor Montoya)
            ├── Ala de Ingeniería de Software & Calidad
            │       ├── Desarrolladores de Software (Fullstack / Backend / Frontend)
            │       └── Analista de Aseguramiento de Calidad (QA / Software Tester)
            └── Ala de Operaciones & Infraestructura
                    └── Soporte Técnico IT Jr. (Nivel 1 / Campo & Xetux)


3. DESCRIPTIVOS DETALLADOS DE CARGOS

3.1. CARGO: LÍDER DE IT & ARQUITECTURA TECNOLÓGICA
• Área: Tecnología, Desarrollo e Infraestructura IT
• Reporta a: Dirección General (Sr. Emiliano)
• Supervisa a: Desarrolladores de Software, Analista QA y Soporte Técnico IT Jr.
• Nivel Jerárquico: Táctico - Estratégico / Jefatura de Área
• Modalidad: Presencial / Híbrida

A. Propósito y Misión del Cargo:
Liderar la estrategia tecnológica, diseñar la arquitectura modular de software propietario (MasterHub), administrar servidores cloud y redes locales, y coordinar al equipo técnico garantizando continuidad operativa, seguridad de datos y alta productividad de la empresa.

B. Responsabilidades y Funciones Principales:
1. Arquitectura y Gobernanza de Software:
   - Diseñar y gobernar la arquitectura de microservicios y módulos de MasterHub (auth-ms, hr-ms, finance-ms, helpdesk-sm, inventory-sm).
   - Definir estándares de bases de datos relacionales (Prisma ORM, PostgreSQL), migraciones seguras y políticas de borrado lógico (Soft Delete).
   - Realizar revisión técnica de código (Pull Requests) y autorizar pases a producción.
2. Gestión de Servidores, Redes y Cloud:
   - Administrar servidores VPS (Linode, Hetzner, Coolify, Docker) garantizando alta disponibilidad.
   - Diseñar y supervisar la política de respaldos automatizados de bases de datos (locales y remotos) y planes de recuperación (DRP).
   - Administrar la seguridad de redes corporativas, accesos remotos y esquemas de permisos basados en roles (RBAC).
3. Gestión del Backlog y Dirección del Equipo:
   - Traducir requerimientos de Dirección y áreas funcionales en tareas técnicas estructuradas.
   - Asignar cargas de trabajo a desarrolladores y coordinar con QA los ciclos de pruebas y liberaciones.
   - Supervisar el cumplimiento de los Acuerdos de Nivel de Servicio (SLAs) del área de Soporte Técnico.
4. Relación Ejecutiva y Presupuesto:
   - Evaluar costos de infraestructura, herramientas de IA y licencias, presentando balances periódicos y propuestas de ahorro a Dirección General.

C. Perfil del Cargo y Requisitos:
• Formación Académica: Ingeniero en Sistemas, Computación, Informática o carrera afín.
• Experiencia Previa: Mínimo 3 a 5 años en roles combinados de desarrollo de software, análisis de sistemas y coordinación técnica.
• Competencias Técnicas: TypeScript, Node.js, Python, React/Next.js, REST APIs, bases de datos SQL, Docker, Linux, redes empresariales y arquitectura de software.
• Competencias Blandas: Pensamiento estratégico, visión de negocio, capacidad de priorización, liderazgo de equipos y comunicación asertiva con Dirección.

D. Indicadores Clave de Desempeño (KPIs):
• Disponibilidad de Sistemas Críticos (Uptime Servidores y Bases de Datos): Mayor o igual al 99.5%
• Cumplimiento de Entregables del Roadmap de Software: Mayor o igual al 85% de funcionalidades en fecha
• Ejecución Exitosa de Respaldos de Bases de Datos: 100% de respaldos automatizados validados


3.2. CARGO: DESARROLLADOR DE SOFTWARE (FULLSTACK / BACKEND / FRONTEND)
• Área: Tecnología, Desarrollo e Infraestructura IT
• Reporta a: Líder de IT & Arquitectura Tecnológica
• Supervisa a: No aplica
• Nivel Jerárquico: Especialista Técnico / Operativo de Desarrollo
• Modalidad: Presencial / Híbrida con seguimiento ágil

A. Propósito y Misión del Cargo:
Construir, mantener y optimizar los módulos, servicios, endpoints e interfaces de usuario del ecosistema MasterHub y herramientas satélites de Master Group, siguiendo los lineamientos de arquitectura y código limpio.

B. Responsabilidades y Funciones Principales:
1. Desarrollo de Funcionalidades y Módulos:
   - Escribir código limpio, modular y tipado en los módulos asignados de MasterHub (Finanzas, RRHH, Helpdesk, etc.).
   - Desarrollar e integrar APIs RESTful, endpoints de autenticación y lógica de negocio.
   - Construir interfaces web receptivas, modernas y de fácil navegación para usuarios corporativos.
2. Calidad de Código y Pruebas Unitarias:
   - Elaborar pruebas unitarias y de integración para validar la lógica crítica antes de transferir a QA.
   - Ejecutar refactorizaciones controladas para mitigar deuda técnica y optimizar consumo de memoria.
3. Control de Versiones y Trabajo Ágil:
   - Administrar ramas de Git (feature branches), redactar commits descriptivos y atender observaciones de Pull Requests.
   - Corregir de forma ágil los defectos reportados por QA dentro del ciclo de sprint.
   - Utilizar herramientas de desarrollo asistido autorizadas (Antigravity CLI/IDE).

C. Perfil del Cargo y Requisitos:
• Formación Académica: TSU o Ingeniero en Sistemas, Informática, Computación o experiencia comprobada en programación.
• Experiencia Previa: Mínimo 1 a 2 años en desarrollo activo de aplicaciones web (Fullstack, Backend o Frontend).
• Competencias Técnicas: TypeScript / JavaScript moderno, Node.js, frameworks frontend (React/Next.js o Vue), SQL, ORMs (Prisma), Git y APIs REST.
• Competencias Blandas: Orientación a resultados, disciplina analítica, proactividad y disposición para el trabajo en equipo y revisión de código.

D. Indicadores Clave de Desempeño (KPIs):
• Cumplimiento de Tareas / Historias de Usuario Asignadas: Mayor o igual al 90% por sprint
• Tasa de Defectos Devueltos por QA: Menor al 10% de entregables rechazados por fallas críticas
• Tiempo Promedio de Corrección de Bugs (Bug Fix Turnaround): Menor a 24 horas en severidad alta


3.3. CARGO: ANALISTA DE ASEGURAMIENTO DE CALIDAD (QA / SOFTWARE TESTER)
• Área: Tecnología, Desarrollo e Infraestructura IT
• Reporta a: Líder de IT & Arquitectura Tecnológica
• Supervisa a: No aplica
• Nivel Jerárquico: Especialista Técnico / Aseguramiento Operativo
• Modalidad: Presencial / Híbrida

A. Propósito y Misión del Cargo:
Garantizar que todo incremento de software, módulo o corrección implementada en MasterHub cumpla con los requerimientos funcionales, de negocio, de seguridad y sin regresiones antes de su despliegue en producción.

B. Responsabilidades y Funciones Principales:
1. Diseño y Ejecución de Matrices de Pruebas:
   - Analizar requerimientos y redactar casos de prueba (Test Cases), escenarios de borde y matrices de aceptación.
   - Ejecutar pruebas manuales funcionales, de integración, interfaz (UI/UX) y regresión.
   - Validar exhaustivamente flujos críticos de negocio: cálculos de retención SENIAT (75%/100%), emisión de comprobantes, pagos bancarios e inventario.
2. Detección y Seguimiento de Defectos (Bug Tracking):
   - Documentar defectos con pasos reproducibles exactos, capturas, respuestas de APIs y niveles de severidad.
   - Dar seguimiento al ciclo de vida del defecto, retestear correcciones y certificar el cierre de incidencias.
3. Certificación de Calidad y Testing de APIs:
   - Realizar pruebas de APIs mediante Postman u otras herramientas para validar esquemas de datos y códigos de estado.
   - Emitir la certificación formal de calidad (Sign-Off) que autoriza el paso a producción.

C. Perfil del Cargo y Requisitos:
• Formación Académica: TSU o Ingeniero en Sistemas, Informática o formación certificada en Testing de Software (ISTQB deseable).
• Experiencia Previa: Mínimo 1 año en pruebas funcionales de software web y consumo de APIs.
• Competencias Técnicas: Diseño de planes de prueba, manejo de Postman, uso de Chrome DevTools (Consola, Red, Storage), SQL básico y nociones de metodologías ágiles.
• Competencias Blandas: Minuciosidad, atención al detalle, pensamiento analítico, comunicación constructiva y asertividad técnica con desarrolladores.

D. Indicadores Clave de Desempeño (KPIs):
• Eficacia de Detección de Defectos (DDE en pruebas): Mayor o igual al 95% de bugs detectados antes de producción
• Tasa de Escape de Defectos a Producción: Menor al 5% de incidencias reportadas tras release
• Precisión y Reproducibilidad en Reportes de Bugs: 100% de tickets con evidencias completas


3.4. CARGO: SOPORTE TÉCNICO IT JR. (NIVEL 1 / CAMPO & XETUX)
• Área: Tecnología, Desarrollo e Infraestructura IT
• Reporta a: Líder de IT & Arquitectura Tecnológica
• Supervisa a: No aplica
• Nivel Jerárquico: Operativo / Asistencia de Campo
• Modalidad: Presencial en Sedes y Oficinas Centrales

A. Propósito y Misión del Cargo:
Brindar soporte técnico preventivo y reactivo de primer nivel a usuarios administrativos y sucursales comerciales (Xetux), velando por la operatividad de puestos de trabajo, periféricos y conectividad, además de ejecutar la auditoría física y etiquetado semanal del inventario tecnológico.

B. Responsabilidades y Funciones Principales:
1. Mesa de Ayuda Helpdesk (Nivel 1):
   - Atender, categorizar y solucionar los tickets de nivel 1 ingresados en la plataforma MasterHub Helpdesk.
   - Formatear, configurar e instalar laptops y computadores de escritorio (Windows 10/11, antivirus, utilitarios de oficina).
   - Realizar mantenimiento preventivo y correctivo de impresoras (toner, atascos, rodillos, configuración de spooler) y periféricos.
2. Soporte a Sucursales y Puntos de Venta (Xetux):
   - Asistir ágilmente por vía telefónica o remota a cajeros ante fallas en puntos de venta (bloqueo de terminales, impresoras de tickets, visores).
   - Diagnosticar cableado de red RJ45, switches locales y puntos de acceso Wi-Fi en tiendas.
   - Escalar al Líder de IT fallas de infraestructura mayor (caídas de enlace troncal o fallos centrales de base de datos).
3. Control Físico Semanal de Inventario:
   - Cumplir las jornadas programadas de visita a sedes para realizar la toma física de equipos y periféricos.
   - Etiquetar nuevos activos tecnológicos con códigos identificadores y asentar las actas de entrega/devolución.
   - Mantener el orden y control del stock físico de piezas y repuestos.

C. Perfil del Cargo y Requisitos:
• Formación Académica: Técnico Medio en Informática, TSU o estudiante de los primeros ciclos universitarios en Sistemas o Informática.
• Experiencia Previa: Mínimo 6 meses a 1 año en soporte a usuarios, ensamblaje de hardware o Helpdesk.
• Competencias Técnicas: Hardware de PC, Windows 10/11, configuración de impresoras de red/USB, crimpado de cables UTP RJ45, herramientas de control remoto (AnyDesk, TeamViewer) y manejo de Helpdesk.
• Competencias Blandas: Vocación de servicio al usuario, paciencia y empatía, disciplina para seguir procedimientos (SOPs), puntualidad y alto orden físico.

D. Indicadores Clave de Desempeño (KPIs):
• Tiempo de Primera Respuesta en Cajas de Sucursales: Menor a 15 minutos en horario comercial
• Tasa de Resolución en Nivel 1 (First Contact Resolution): Mayor o igual al 70% sin requerir escalamiento
• Cumplimiento de Cronograma de Toma Física de Inventario: 100% de sedes y equipos asignados
• Satisfacción del Usuario Interno (CSAT): Mayor o igual al 90% de valoraciones positivas


4. CICLO DE VIDA INTEGRADO DE DESARROLLO Y SOPORTE (SDLC + HELPDESK)
El departamento opera bajo un flujo estructurado de comunicación para evitar interrupciones innecesarias:
Paso 1: El usuario o cajero de sucursal registra la incidencia en el Helpdesk de MasterHub.
Paso 2: Soporte N1 diagnostica el caso. Si es operativo (hardware, tóner, Windows, punto de venta), lo resuelve de inmediato.
Paso 3: Si se detecta un error de software o se solicita una nueva función, Soporte N1 escala el ticket documentado al Líder de IT.
Paso 4: El Líder de IT prioriza la tarea en el Backlog y la asigna al Desarrollador correspondiente.
Paso 5: El Desarrollador construye la solución, realiza pruebas unitarias y genera un Pull Request.
Paso 6: El Analista QA despliega en ambiente de prueba y ejecuta la matriz de testing funcional y de regresión.
Paso 7: Si QA aprueba (Sign-Off), el Líder de IT autoriza y ejecuta el pase a producción en los servidores cloud.
Paso 8: Se notifica al usuario final y se cierra el ticket formalmente en MasterHub.


5. MATRIZ DE RESPONSABILIDADES RACI CORPORATIVA
A continuación se detalla la matriz de asignación de responsabilidades:
(R = Responsable de Ejecutar | A = Aprobador Final / Rendición de Cuentas | C = Consultado | I = Informado)
"""

    print("2. Insertando texto maestro estructurado...")
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
    print("✅ Texto insertado exitosamente.")

    # 3. Obtener el índice final para insertar la tabla RACI
    req_get2 = urllib.request.Request(
        f"https://docs.googleapis.com/v1/documents/{new_doc_id}",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    resp_get2 = safe_urlopen(req_get2)
    doc2 = json.loads(resp_get2.read().decode("utf-8"))
    
    end_doc_index = doc2.get("body", {}).get("content", [])[-1].get("endIndex", 1) - 1
    
    print("3. Insertando tabla nativa para la Matriz RACI...")
    table_req = [{
        "insertTable": {
            "rows": 11,
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
    print("✅ Tabla RACI de 11 filas x 6 columnas creada.")

    # 4. Poblar celdas de la tabla RACI
    req_get3 = urllib.request.Request(
        f"https://docs.googleapis.com/v1/documents/{new_doc_id}",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    resp_get3 = safe_urlopen(req_get3)
    doc3 = json.loads(resp_get3.read().decode("utf-8"))

    raci_data = [
        ["Proceso / Actividad Clave", "Dirección", "Líder IT", "Desarrollador", "Analista QA", "Soporte N1"],
        ["Definición de Estrategia y Presupuesto IT", "Aprobador (A)", "Responsable (R)", "Informado (I)", "Informado (I)", "Informado (I)"],
        ["Arquitectura de Software y Modelado DB", "Informado (I)", "A / R", "Consultado (C)", "Consultado (C)", "Informado (I)"],
        ["Desarrollo de Código y Módulos MasterHub", "Informado (I)", "Aprobador (A)", "Responsable (R)", "Consultado (C)", "Informado (I)"],
        ["Diseño y Ejecución de Casos de Prueba QA", "Informado (I)", "Aprobador (A)", "Consultado (C)", "Responsable (R)", "Informado (I)"],
        ["Certificación de Calidad (Sign-Off Release)", "Informado (I)", "Aprobador (A)", "Informado (I)", "Responsable (R)", "Informado (I)"],
        ["Pase a Producción en Servidores Cloud", "Informado (I)", "A / R", "Consultado (C)", "Informado (I)", "Informado (I)"],
        ["Atención Tickets Helpdesk y Sucursales Xetux", "Informado (I)", "Aprobador (A)", "Informado (I)", "Informado (I)", "Responsable (R)"],
        ["Mantenimiento Físico de PCs e Impresoras", "Informado (I)", "Aprobador (A)", "Informado (I)", "Informado (I)", "Responsable (R)"],
        ["Toma Física Semanal y Etiquetado de Activos", "Informado (I)", "Aprobador (A)", "Informado (I)", "Informado (I)", "Responsable (R)"],
        ["Administración de Backups y Seguridad", "Informado (I)", "A / R", "Informado (I)", "Informado (I)", "Informado (I)"]
    ]

    cell_requests = []
    for elem in doc3.get("body", {}).get("content", []):
        if "table" in elem:
            tbl = elem["table"]
            rows = tbl.get("tableRows", [])
            if len(rows) == 11:
                # Recorremos celdas
                for r_idx, row in enumerate(rows):
                    cells = row.get("tableCells", [])
                    for c_idx, cell in enumerate(cells):
                        start_c = cell.get("content", [])[0].get("startIndex")
                        text_val = raci_data[r_idx][c_idx]
                        cell_requests.append({
                            "index": start_c,
                            "text": text_val
                        })
                break

    # Para evitar desfase de índices, ordenamos las inserciones de celdas en orden DESCENDENTE por índice
    cell_requests.sort(key=lambda x: x["index"], reverse=True)
    batch_cell_requests = [{
        "insertText": {
            "location": {"index": item["index"]},
            "text": item["text"]
        }
    } for item in cell_requests]

    print("4. Poblando celdas de la tabla RACI...")
    req_batch_cells = urllib.request.Request(
        f"https://docs.googleapis.com/v1/documents/{new_doc_id}:batchUpdate",
        data=json.dumps({"requests": batch_cell_requests}).encode("utf-8"),
        headers={"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    )
    safe_urlopen(req_batch_cells)
    print("✅ Celdas de la tabla RACI pobladas con éxito.")

    # 5. Aplicar formato y jerarquía de párrafos nativos (TITLE, HEADING_1, HEADING_2)
    print("5. Aplicando estilos nativos (TITLE, HEADING_1, HEADING_2)...")
    req_get4 = urllib.request.Request(
        f"https://docs.googleapis.com/v1/documents/{new_doc_id}",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    resp_get4 = safe_urlopen(req_get4)
    doc4 = json.loads(resp_get4.read().decode("utf-8"))

    style_requests = []
    for elem in doc4.get("body", {}).get("content", []):
        if "paragraph" in elem:
            p = elem["paragraph"]
            p_text = ""
            for pe in p.get("elements", []):
                p_text += pe.get("textRun", {}).get("content", "")
            
            p_clean = p_text.strip()
            p_start = elem.get("startIndex")
            p_end = elem.get("endIndex")

            if p_clean == "MANUAL ORGANIZACIONAL Y DESCRIPTIVO DE CARGOS DEL DEPARTAMENTO DE IT":
                style_requests.append({
                    "updateParagraphStyle": {
                        "range": {"startIndex": p_start, "endIndex": p_end},
                        "paragraphStyle": {"namedStyleType": "TITLE"},
                        "fields": "namedStyleType"
                    }
                })
            elif p_clean == "Estructura Operativa, Perfiles de Cargo, Matriz de Responsabilidades y KPIs":
                style_requests.append({
                    "updateParagraphStyle": {
                        "range": {"startIndex": p_start, "endIndex": p_end},
                        "paragraphStyle": {"namedStyleType": "SUBTITLE"},
                        "fields": "namedStyleType"
                    }
                })
            elif any(p_clean.startswith(prefix) for prefix in [
                "1. PROPÓSITO GENERAL Y JUSTIFICACIÓN",
                "2. ESTRUCTURA ORGANIGRAFICA",
                "3. DESCRIPTIVOS DETALLADOS",
                "4. CICLO DE VIDA INTEGRADO",
                "5. MATRIZ DE RESPONSABILIDADES"
            ]):
                style_requests.append({
                    "updateParagraphStyle": {
                        "range": {"startIndex": p_start, "endIndex": p_end},
                        "paragraphStyle": {"namedStyleType": "HEADING_1"},
                        "fields": "namedStyleType"
                    }
                })
            elif any(p_clean.startswith(prefix) for prefix in [
                "1.1. Diagnóstico de Eficiencia",
                "3.1. CARGO: LÍDER DE IT",
                "3.2. CARGO: DESARROLLADOR DE SOFTWARE",
                "3.3. CARGO: ANALISTA DE ASEGURAMIENTO DE CALIDAD",
                "3.4. CARGO: SOPORTE TÉCNICO IT JR."
            ]):
                style_requests.append({
                    "updateParagraphStyle": {
                        "range": {"startIndex": p_start, "endIndex": p_end},
                        "paragraphStyle": {"namedStyleType": "HEADING_2"},
                        "fields": "namedStyleType"
                    }
                })
            elif any(p_clean.startswith(prefix) for prefix in [
                "A. Propósito y Misión",
                "B. Responsabilidades y Funciones",
                "C. Perfil del Cargo",
                "D. Indicadores Clave de Desempeño"
            ]):
                style_requests.append({
                    "updateParagraphStyle": {
                        "range": {"startIndex": p_start, "endIndex": p_end},
                        "paragraphStyle": {"namedStyleType": "HEADING_3"},
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
        print(f"✅ {len(style_requests)} estilos nativos aplicados con éxito.")

    # 6. Asignar permisos públicos de lectura
    print("6. Configurando permisos públicos de lectura en Google Drive...")
    try:
        perm_req = urllib.request.Request(
            f"https://www.googleapis.com/drive/v3/files/{new_doc_id}/permissions",
            data=json.dumps({"role": "reader", "type": "anyone"}).encode("utf-8"),
            headers={"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
        )
        safe_urlopen(perm_req)
        print("✅ Permiso de lectura pública ('anyone'/'reader') configurado.")
    except Exception as pe:
        print(f"⚠️ Nota sobre permisos de Drive: {pe}")

    final_url = f"https://docs.google.com/document/d/{new_doc_id}/edit"
    print(f"\n🎉 DOCUMENTO OFICIAL GENERADO EXITOSAMENTE:\n👉 {final_url}\n")
    return final_url

if __name__ == "__main__":
    token = get_access_token()
    url = build_document(token)
    print(f"RESULT_URL={url}")
