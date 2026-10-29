#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pain (PM) — Script de Inicialización de Proyecto ClickUp: SmartOps VE
"""

import sys
import os
import json
import urllib.request
import urllib.error

if sys.platform == "win32":
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8')

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import scripts.clickup_api as cu

TEAM_ID = "90141555783"

def main():
    print("☁️ Pain (Project Manager): Inicializando espacio de trabajo en ClickUp...")
    
    # 1. Comprobar si ya existe el espacio o crearlo
    spaces = cu.get_spaces(TEAM_ID).get("spaces", [])
    target_space = None
    for s in spaces:
        if "smartops" in s["name"].lower():
            target_space = s
            break
            
    if not target_space:
        print("📌 Creando Space: '🚀 SMARTOPS VE — Core Refactor 2026'...")
        payload = {
            "name": "🚀 SMARTOPS VE — Core Refactor 2026",
            "multiple_assignees": True,
            "features": {
                "due_dates": {"enabled": True, "start_date": True, "reminders": True},
                "time_tracking": {"enabled": True},
                "tags": {"enabled": True},
                "checklists": {"enabled": True},
                "custom_fields": {"enabled": True}
            }
        }
        target_space = cu.clickup_request(f"/team/{TEAM_ID}/space", method="POST", data=payload)
        print(f"✓ Space Creado: ID {target_space['id']}")
    else:
        print(f"✓ Space existente encontrado: {target_space['name']} (ID {target_space['id']})")
        
    space_id = target_space["id"]
    
    # 2. Crear Lista del Backlog
    lists = cu.get_lists(space_id, is_space=True).get("lists", [])
    target_list = None
    for l in lists:
        if "backlog" in l["name"].lower() or "smartops" in l["name"].lower():
            target_list = l
            break
            
    if not target_list:
        print("📌 Creando Lista: '⚡ Backlog Akatsuki — Booking, E-commerce & IA'...")
        payload = {
            "name": "⚡ Backlog Akatsuki — Booking, E-commerce & IA",
            "content": "Espacio de trabajo oficial para la reactivación y transformación de SmartOps VE en un Hub de Negocio Autónomo."
        }
        target_list = cu.clickup_request(f"/space/{space_id}/list", method="POST", data=payload)
        print(f"✓ Lista Creada: ID {target_list['id']}")
    else:
        print(f"✓ Lista existente encontrada: {target_list['name']} (ID {target_list['id']})")
        
    list_id = target_list["id"]
    
    # 3. User Stories en Gherkin
    user_stories = [
        {
            "name": "US-01 [UI/UX & Design] Reingeniería Visual de Landing, Perfil & Dashboard en Google Stitch",
            "priority": 1, # Urgente
            "tags": ["ui-ux", "stitch", "konan", "sai"],
            "description": """## 🦋 US-01: Reingeniería Visual & Prototipado en Google Stitch

**Responsables**: 🦋 Konan (UI/UX Designer) & 🎨 Sai (Arte Gráfico)  
**Story Points**: 5 SP  
**Herramienta**: Google Stitch Cloud (`projects/6994536314139933854`)

### 📋 Criterios de Aceptación (Gherkin)
- **Escenario 1: Navegación de Landing y Perfil**
  - **Dado que** un cliente o profesional accede a la plataforma SmartOps,
  - **Cuando** visualiza el perfil o la landing page,
  - **Entonces** debe renderizarse bajo el sistema de diseño *SmartOps Obsidian Glow* (#0B132B, #00E5FF, #0072FF) con Bento Grid y tarjetas Glassmorphism.

- **Escenario 2: Interacción con el Motor de Booking**
  - **Dado que** el usuario desea agendar una cita,
  - **Cuando** selecciona servicio, día y hora disponible,
  - **Entonces** se despliega el modal de confirmación con sincronización a Google Calendar y Google Meet.

### 📦 Entregables
- Prototipos oficiales 4K y HTML generados por Gemini 3.8 Flash en Google Stitch.
"""
        },
        {
            "name": "US-02 [Frontend Web] Setup de Next.js 15 App Router & Migración a Tailwind v4",
            "priority": 2, # Alta
            "tags": ["frontend", "nextjs15", "itachi"],
            "description": """## 👁️ US-02: Setup de Next.js 15 App Router & Migración a Tailwind v4

**Responsable**: 👁️ Itachi (Frontend Lead)  
**Story Points**: 8 SP  
**Repositorio**: `Website_smartopsve`

### 📋 Criterios de Aceptación (Gherkin)
- **Escenario 1: Limpieza de Librerías Redundantes**
  - **Dado que** el repositorio anterior mezclaba Material UI (@mui) con Tailwind 3.4 y Radix UI,
  - **Cuando** se refactoriza la arquitectura del layout base,
  - **Entonces** se elimina Material UI reduciendo el peso del bundle en >60% y se estandariza con Shadcn UI + Tailwind v4.

- **Escenario 2: Renderizado Rápido y Web Vitals**
  - **Dado que** se despliega la web en Google Cloud Run,
  - **Cuando** se audita con Lighthouse,
  - **Entonces** el LCP (Largest Contentful Paint) debe ser inferior a 1.0s.
"""
        },
        {
            "name": "US-03 [Backend & Engine] Motor de Booking & Sincronización Bidireccional Google Calendar",
            "priority": 2, # Alta
            "tags": ["backend", "booking", "kakuzu", "api"],
            "description": """## 🖤 US-03: Motor de Booking & Sincronización Google Calendar

**Responsable**: 🖤 Kakuzu (Backend & DB Architect)  
**Story Points**: 8 SP  
**Repositorio**: `API_V3` / Endpoints `/api/booking`

### 📋 Criterios de Aceptación (Gherkin)
- **Escenario 1: Disponibilidad de Horarios en Tiempo Real**
  - **Dado que** un cliente consulta los horarios libres de un profesional,
  - **Cuando** el endpoint `/api/booking/slots` evalúa la agenda,
  - **Entonces** devuelve únicamente los slots sin solapamiento con Google Calendar y citas previas.

- **Escenario 2: Confirmación y Creación de Enlace Meet**
  - **Dado que** se completa la reserva de una cita virtual,
  - **Cuando** se persiste la reserva en MongoDB,
  - **Entonces** se emite el evento a Google Calendar API y se genera el enlace de Google Meet para ambos participantes.
"""
        },
        {
            "name": "US-04 [AI Agents] Agente Conversacional Autónomo 'Doble Digital' (Web & WhatsApp)",
            "priority": 2, # Alta
            "tags": ["ai-agents", "rag", "gemini", "kakuzu", "itachi"],
            "description": """## 🤖 US-04: Agente Conversacional Autónomo 'Doble Digital'

**Responsables**: 🖤 Kakuzu (RAG Engine) & 👁️ Itachi (Chat Widget)  
**Story Points**: 8 SP  
**Tecnología**: Gemini API / LangChain + WhatsApp Cloud API

### 📋 Criterios de Aceptación (Gherkin)
- **Escenario 1: Atención y Cotización de Tarifas**
  - **Dado que** un prospecto consulta el precio de un servicio en el perfil público,
  - **Cuando** envía su consulta al widget flotante de IA,
  - **Entonces** el agente responde al instante con las tarifas exactas y los beneficios del servicio.

- **Escenario 2: Agendamiento por Lenguaje Natural**
  - **Dado que** el cliente dice: '¿Víctor tiene espacio este viernes en la tarde?',
  - **Cuando** el agente procesa la intención,
  - **Entonces** consulta el motor de booking y ofrece directamente los botones de los slots disponibles.
"""
        },
        {
            "name": "US-05 [E-commerce] Checkout Exprés Bimonetario & Pasarela Pago Móvil QR",
            "priority": 3, # Normal
            "tags": ["ecommerce", "payments", "kakuzu"],
            "description": """## 🛒 US-05: Checkout Exprés Bimonetario & Pago Móvil QR

**Responsable**: 🖤 Kakuzu (Finanzas & Transacciones)  
**Story Points**: 5 SP  

### 📋 Criterios de Aceptación (Gherkin)
- **Escenario 1: Cobro Bimonetario Dinámico**
  - **Dado que** un cliente adquiere un producto (Licencia POS, Tarjeta NFC o Asesoría),
  - **Cuando** visualiza el total en pantalla,
  - **Entonces** el sistema muestra el valor en USD y el equivalente en Bolívares a tasa oficial BCV en tiempo real.

- **Escenario 2: Generación de QR de Pago Móvil**
  - **Dado que** el cliente elige Pago Móvil,
  - **Cuando** presiona pagar,
  - **Entonces** se renderiza el código QR dinámico con teléfono, RIF y monto exacto listo para escanear desde la app bancaria.
"""
        },
        {
            "name": "US-06 [DevOps & Cloud] CI/CD Docker Multi-Stage & Cloud Run Zero-Downtime",
            "priority": 3, # Normal
            "tags": ["devops", "cloud-run", "docker", "orochimaru"],
            "description": """## 🐍 US-06: CI/CD Docker Multi-Stage & Cloud Run Zero-Downtime

**Responsable**: 🐍 Orochimaru (Cloud Architect & DevOps)  
**Story Points**: 5 SP  

### 📋 Criterios de Aceptación (Gherkin)
- **Escenario 1: Construcción de Contenedor Liviano**
  - **Dado que** se efectúa un push a la rama `main`,
  - **Cuando** corre el Dockerfile multi-stage,
  - **Entonces** la imagen final no excede los 180MB y no contiene dependencias de desarrollo.

- **Escenario 2: Despliegue Zero-Downtime**
  - **Dado que** Cloud Run recibe la nueva versión,
  - **Cuando** pasa las pruebas de salud (`health check`),
  - **Entonces** conmuta el 100% del tráfico sin interrumpir las sesiones activas de usuarios.
"""
        },
        {
            "name": "US-07 [QA & Ciberseguridad] Pruebas de Estrés de Concurrencia & Pentesting OWASP",
            "priority": 2, # Alta
            "tags": ["qa", "security", "hidan", "deidara", "sasori"],
            "description": """## 💀 US-07: Pruebas de Estrés de Concurrencia & Pentesting OWASP

**Responsables**: 💀 Hidan (QA Lead), 💣 Deidara (Red Team) & 🦂 Sasori (Blue Team)  
**Story Points**: 5 SP  

### 📋 Criterios de Aceptación (Gherkin)
- **Escenario 1: Concurrencia en Reserva Simultánea**
  - **Dado que** dos clientes intentan reservar exactamente el mismo slot de horario en el mismo milisegundo,
  - **Cuando** se ejecuta la transacción en la base de datos,
  - **Entonces** solo uno es confirmado con éxito y el segundo recibe una notificación amigable de 'Horario recién ocupado'.

- **Escenario 2: Auditoría OWASP de Endpoints Públicos**
  - **Dado que** el agente conversacional y el booking son de acceso público,
  - **Cuando** Deidara ejecuta inyecciones de prompts y flood de requests,
  - **Entonces** el sistema aplica rate-limiting y sanitización estricta sin filtrar variables de entorno ni claves de API.
"""
        }
    ]
    
    # 4. Crear las tareas en ClickUp
    print(f"\n📌 Creando las 7 Historias de Usuario en ClickUp (Lista: {list_id})...")
    created_tasks = []
    for us in user_stories:
        t = cu.create_task(
            list_id=list_id,
            name=us["name"],
            description=us["description"],
            priority=us["priority"],
            tags=us["tags"]
        )
        task_id = t.get("id")
        task_url = t.get("url")
        print(f"  ✓ {us['name'][:50]}... -> ID: {task_id} ({task_url})")
        created_tasks.append({"id": task_id, "name": us["name"], "url": task_url})
        
    print(f"\n🎉 ¡Backlog de SmartOps VE creado exitosamente en ClickUp!")
    print(f"   Space: {target_space['name']} ({space_id})")
    print(f"   List URL: https://app.clickup.com/{TEAM_ID}/v/li/{list_id}")

if __name__ == "__main__":
    main()
