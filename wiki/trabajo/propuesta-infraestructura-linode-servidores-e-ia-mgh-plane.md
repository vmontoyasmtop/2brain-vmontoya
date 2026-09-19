---
title: "Propuesta Técnica y Financiera: Infraestructura Linode y Planes de IA (MGH & Plane.so)"
type: "guide"
area: "trabajo"
created: 2026-09-18
updated: 2026-09-18
tags:
  - 
---

# 📋 Documento Técnico y Financiero: Infraestructura Linode & Planes de IA

*Propuesta de coexistencia en servidor VPS Linode (Akamai Cloud) para MasterHub (MGH) y Plane.so, junto a la evaluación comparativa de asistentes de programación con IA.*

**Enlace a Google Docs Corporativo**: [📋 Propuesta Infraestructura Linode - MGH & Plane.so](https://docs.google.com/document/d/1NHxfBLv0ZtdD0C8e_KZXvcyx_yst0MF9UmDjJghFvvU/edit)

---

## 🔍 1. Contexto y Justificación del Stack por Proyecto

### A. Proyecto Plane.so
- **Propósito**: Plataforma *open-source* de gestión de proyectos, Sprints, backlog e incidencias (alternativa autohospedada a Jira/Linear).
- **Stack Tecnológico**: Django (Python) + Next.js + PostgreSQL + Redis/Valkey + MinIO (S3).
- **Justificación**:
  - **Backend Django (Python)**: Manejo de reglas de negocio complejas, permisos y colas asíncronas con Celery (notificaciones y reportes).
  - **Frontend Next.js**: Interfaz SPA/SSR de alto rendimiento.
  - **MinIO**: Almacenamiento de archivos y adjuntos S3.
  - **Redis / Valkey**: Caché en memoria y broker de mensajes Celery.

### B. Proyecto MasterHub (MGH)
- **Propósito**: Plataforma web y API central del ecosistema MGH.
- **Stack Tecnológico**: Next.js (React) + NestJS (Node.js / TypeScript).
- **Justificación**:
  - **Backend NestJS (Node.js)**: Arquitectura empresarial modular basada en TypeScript, orientada a APIs I/O no bloqueantes (REST/TCP).
  - **Frontend Next.js**: Renderizado SSR para máximo SEO y rendimiento.

---

## 🖥️ 2. Arquitectura de Servidor Compartido en Linode (Akamai Cloud)

### ¿Por qué un único VPS compartido?
1. **Eficiencia Financiera**: Un solo VPS de 16 GB RAM en Linode cuesta **$96.00 USD/mes**, reduciendo más del 60% frente a servicios PaaS gestionados ($250–$400+/mes).
2. **Aislamiento con Docker**: Docker empaqueta Python/Django y Node.js/NestJS en contenedores independientes, evitando conflictos en el SO.
3. **Centralización**: Nginx Proxy Inverso maneja certificados SSL (HTTPS Let's Encrypt) para todos los subdominios.

---

## 💰 3. Análisis de Costos Linode (Shared CPU - Norteamérica)

| Plan Linode Shared | vCPU | RAM | SSD | Transferencia | Costo Mensual | Costo por Hora | Estado |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Shared 8GB | 4 vCPU | 8 GB | 160 GB | 5 TB | $48.00 USD | $0.0720/hr | Insuficiente en picos |
| **Shared 16GB** | **6 vCPU** | **16 GB** | **320 GB** | **8 TB** | **$96.00 USD** | **$0.1440/hr** | 🟢 **RECOMENDADO** |
| Shared 32GB | 8 vCPU | 32 GB | 640 GB | 10–16 TB | $192.00 USD | $0.2880/hr | Sobredimensionado |
| Shared 64GB | 16 vCPU | 64 GB | 1280 GB | 20 TB | $384.00 USD | $0.5760/hr | Excesivo |

---

## 📊 4. Matriz de Consumo de Memoria RAM

| Componente | Reposo | Carga Media | Picos Máximos (Builds/Jobs) |
| :--- | :--- | :--- | :--- |
| **MGH Frontend (Next.js)** | ~150 MB | ~300 MB | ~800 MB |
| **MGH Backend (NestJS)** | ~150 MB | ~350 MB | ~600 MB |
| **Plane Web UI (Next.js)** | ~180 MB | ~300 MB | ~600 MB |
| **Plane API Core (Django)** | ~250 MB | ~500 MB | ~900 MB |
| **Plane Celery Workers** | ~200 MB | ~400 MB | ~800 MB |
| **PostgreSQL DB** | ~250 MB | ~600 MB | ~1.5 GB |
| **Redis / Valkey** | ~80 MB | ~200 MB | ~500 MB |
| **MinIO Storage** | ~150 MB | ~300 MB | ~600 MB |
| **Nginx & OS Kernel** | ~200 MB | ~400 MB | ~600 MB |
| **TOTAL COMBINADO** | **~1.6 GB** | **~3.35 GB** | **~6.95 GB** |

### Justificación de Elección (Shared 16GB - $96/mes):
- **Por qué NO 8GB ($48/mes)**: En picos de compilación (`npm run build`) o procesamiento intensivo en Celery, la RAM consumida alcanza los **~6.95 GB**. En un VPS de 8GB, el Kernel de Linux activará el *OOM Killer (Out Of Memory)* y detendrá PostgreSQL o NestJS.
- **Por qué SÍ 16GB ($96/mes)**: Ofrece más de 8 GB de RAM libres como margen de seguridad para garantizar estabilidad total sin caídas.

---

## 🌐 5. Esquema de Enrutamiento y Dominios (Nginx Reverse Proxy)

```
mgh.midominio.com     ──> Nginx Proxy (443 SSL) ──> MGH Next.js (Port 3000)
api-mgh.midominio.com ──> Nginx Proxy (443 SSL) ──> MGH NestJS (Port 4000)
plane.midominio.com   ──> Nginx Proxy (443 SSL) ──> Plane Web UI (Port 8000)
api-plane.midominio.com ─> Nginx Proxy (443 SSL) ──> Plane API Core (Port 8000)
```

**Conclusión Infraestructura**: Aprobar la contratación del servidor **Linode Shared 16GB ($96.00 USD/mes)** en la región Norteamérica. Métodos de pago aceptados: Tarjeta de Crédito / PayPal.

---

## 🤖 6. Estudio y Evaluación de Planes de IA para Programación (Code Assistants)

### A. Herramientas Evaluadas

1. **Google Antigravity (AGY) & Gemini Coding Assistant**:
   - **Descripción**: Entorno agéntico autónomo desarrollado por Google DeepMind. Ejecuta agentes paralelos, terminal, herramientas MCP y contexto masivo (1M–2M tokens).
   - **Fortalezas**: Pair-programming autónomo, refactorización multimodular y ejecuciones sin costo por puesto fijo mediante CLI/SDK y API de Gemini.
   - **Costo**: Incluido vía Antigravity / API Tokens Gemini 1.5 & 2.0 / Google One AI Premium ($19.99/mes).

2. **Claude (Anthropic - Claude Pro / Claude Team)**:
   - **Descripción**: Modelo líder en razonamiento lógico, refactorización de código y precisión (Claude 3.5 Sonnet / 3.7 Sonnet).
   - **Fortalezas**: Máxima calidad en TypeScript (NestJS/Next.js) y Python (Django). Baja tasa de alucinaciones.
   - **Precios**:
     - *Claude Pro*: $20.00 USD / usuario / mes.
     - *Claude Team*: $25.00 – $30.00 USD / usuario / mes (mínimo 5 usuarios).

3. **Cursor IDE (AI-First Code Editor)**:
   - **Descripción**: Editor basado en VS Code con indexado local completo del repositorio (*Codebase Indexing*).
   - **Fortalezas**: Permite alternar entre Claude 3.5 Sonnet, GPT-4o y Gemini 1.5 Pro en el mismo editor.
   - **Precios**:
     - *Cursor Pro*: $20.00 USD / usuario / mes.
     - *Cursor Business*: $40.00 USD / usuario / mes.

4. **GitHub Copilot (Microsoft / OpenAI)**:
   - **Descripción**: Asistente integrado en el ecosistema GitHub / VS Code.
   - **Precios**:
     - *Copilot Individual*: $10.00 USD / usuario / mes.
     - *Copilot Business*: $19.00 USD / usuario / mes.

---

### B. Recomendación Estratégica de IA

1. **Opción Principal (Máxima Productividad)**:
   - Combinar **Google Antigravity** (para tareas agénticas autónomas, refactorizaciones complejas e integración MCP) con **Cursor Pro ($20.00 USD/mes)** o **Claude Pro ($20.00 USD/mes)** por desarrollador.
2. **Opción Económica / Equipo**:
   - Adquirir licencias de **GitHub Copilot Business ($19.00 USD/mes)** para autocompletado continuo en VS Code y apoyar desarrollos complejos en **Google Antigravity**.
