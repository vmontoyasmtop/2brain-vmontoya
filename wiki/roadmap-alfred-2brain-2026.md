---
title: "Roadmap de Evolución: ALFRED & Sistema 2brain 2026"
type: "guide"
area: "general"
created: 2026-09-13
updated: 2026-09-18
sources: []
tags:
  - 
---

# 🗺️ Roadmap de Evolución: ALFRED & Sistema 2brain 2026

Plan de trabajo estratégico para convertir a **ALFRED** en un mayordomo ejecutivo hiper-autónomo y transformar a **2brain** en un **Sistema Operativo de Vida (Life OS)** sincronizado y automatizado en tiempo real.

---

## 🎯 Objetivo Principal

Integrar las capacidades multiactivas de ALFRED (procesamiento de lenguaje natural, subagentes especializados, herramientas MCP de Google) con una infraestructura de respaldo en la nube y pipelines de automatización continua (*Auto-Ingest*).

---

## 📍 Fase 1: Sincronización Multiequipo & Nube (Semana 1) [COMPLETADA]

- [x] **1.1. Control de Versiones Git**: Repositorio `git` inicializado con el commit base de las 6 áreas.
- [x] **1.2. Script de Auto-Sync**: Creado [[sync.ps1](file:///C:/Users/vmontoyaMG/Desktop/2brain/sync.ps1)] para sincronizar cambios en un solo clic.
- [x] **1.3. Repositorio Remoto GitHub Privado**: Conectado exitosamente con `origin/master` en `vmontoyasmtop/2brain-vmontoya.git`.
- [x] **1.4. Acceso Multidispositivo**: Configurada la sincronización mediante `sync.ps1` para sincronizar cambios de forma transparente.

---

## 📍 Fase 2: Automatización de Ingesta Inteligente (Semana 2)

- [ ] **2.1. Watchdog de Carpeta `raw/`**: Script en Python/Node que vigile `C:\Users\vmontoyaMG\Desktop\2brain\raw\` para disparar al [Subagente Ingestor](./agents/ingestor.md) al detectar nuevos archivos.
- [ ] **2.2. Webhooks de n8n (YouTube & NotebookLM)**: Flujo de n8n para enviar transcripciones y resúmenes directamente a `raw/` desde Telegram o móvil.
- [ ] **2.3. Skill Slash Command `/ingest`**: Comando personalizado en Antigravity para procesar enlaces o documentos con una sola orden.

---

## 📍 Fase 3: Integración Profunda de Canales MCP (Semana 3)

- [ ] **3.1. Gestión Proactiva de Bloques de Tiempo**: ALFRED verificará diariamente la agenda de **Trabajo** y **Personal** para proteger los bloques profundos (08:30-10:30 / 13:30-15:30).
- [ ] **3.2. Briefing Ejecutivo Matutino**: Reporte diario enviado al iniciar la jornada con correos clave de MasterGroup, tareas del [[life-dashboard|Dashboard de Vida & Centro de Control (Life OS)]] y sermones/estudios bíblicos pendientes.
- [ ] **3.3. Creación Directa de Eventos**: Permitir agendar citas en Google Calendar directamente por lenguaje natural usando herramientas MCP.

---

## 📍 Fase 4: Autonomía Contextual & Mantenimiento 2brain (Semana 4)

- [ ] **4.1. Auditoría Semanal con Jardinero**: Ejecutar al [Subagente Jardinero](./agents/gardener.md) para reparar enlaces huérfanos, validar frontmatter y mantener la wiki limpia.
- [ ] **4.2. Dashboard de Vida Dinámico**: Actualización automática de avances semanales por las 6 áreas.

---

## 📍 Fase 5: Infraestructura Cloud 24/7 & RAG Vectorial (Semana 5+)

- [ ] **5.1. Despliegue en Servidor Cloud VPS**: Implementar el stack de Docker Compose documentado en [[arquitectura-alfred-cloud-vps|Arquitectura & Despliegue Cloud VPS: ALFRED 2brain 24/7]].
- [ ] **5.2. Memoria Semántica con Qdrant**: Indexación de todas las notas de la wiki para búsquedas y consultas contextuales RAG en lenguaje natural vía Telegram.
- [ ] **5.3. Bot de Telegram Multimodal Autónomo**: Daemon permanente con transcripción de voz de alta duración y guardado directo en `raw/inbox/`.
- [ ] **5.4. Git Auto-Sync Daemon**: Ciclos automáticos de commit y push hacia el repositorio remoto `vmontoyasmtop/2brain-vmontoya`.

---

## 🔗 Páginas Relacionadas
- [[arquitectura-alfred-cloud-vps|Arquitectura & Despliegue Cloud VPS: ALFRED 2brain 24/7 (Docker Stack & RAG)]]
- [[life-dashboard|Dashboard de Vida & Centro de Control]]
- [[plan-organizacion-priorizacion-it|Plan de Organización y Priorización Laboral para Analista de IT]]
- [[guia-configuracion-mcp-google-calendar-gmail|Guía de Instalación y Configuración de Servidores MCP (Google Calendar & Gmail Multicuenta)]]
