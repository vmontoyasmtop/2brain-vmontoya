---
title: "Proyecto: Plane - Plataforma de Gestión de Proyectos"
type: "project"
area: "proyectos"
created: 2026-09-17
updated: 2026-09-18
tags:
  - 
---

# 📋 Proyecto: Plane — Plataforma de Gestión de Proyectos (`makeplane/plane`)

*Estrategia, arquitectura y guía de activación para implementar **Plane** como la plataforma central de gestión de proyectos, sprints, backlog e incidencias en MasterGroup.*

---

## 🔍 1. Visión & Objetivos del Proyecto

- **Objetivo**: Desplegar y operacionalizar **Plane** (alternativa *open-source* moderna a Jira/Linear/ClickUp) para centralizar la gestión de tareas, hojas de ruta (Roadmaps), módulos y ciclos de desarrollo (Sprints).
- **Estado actual**: 🟢 **EN PRODUCCIÓN OPERATIVA (`projects.mastergroupve.com`)**.
- **Instancia**: Workspace `it---mg` (ID: `388c5fcf-86fd-4d07-8656-22c23413fe10`).
- **Caso de uso**: Control centralizado de tareas, sprints y módulos de desarrollo de software (MasterHub / MG-HUB, WebCastro, SmartOps VE, Brotapp, CRM-MG).

---

## 🛠️ 2. Stack Tecnológico & Arquitectura

| Componente | Tecnología |
| :--- | :--- |
| **Frontend UI** | Next.js 14 / React (TypeScript) |
| **Backend API** | Python / Django REST Framework |
| **Base de Datos** | PostgreSQL 15+ |
| **Caché / Queues** | Redis (Valkey) |
| **Object Storage** | MinIO (S3 Compatible) o AWS S3 |
| **Proxy / SSL** | Traefik / Nginx (Let's Encrypt SSL) |

---

## 📦 3. Proyecto Activo: MasterHub (`MG-HUB`) en Plane

- **URL del Proyecto**: `https://projects.mastergroupve.com/it---mg/projects/b60ea600-1f86-4177-87df-6b6ed0063874/issues/`
- **ID de Proyecto**: `b60ea600-1f86-4177-87df-6b6ed0063874`
- **Módulos configurados y vinculados**:
  - 🏛️ `Finanzas-MS` (58 tareas / épicas / historias)
  - 👥 `HR-MS` (20 tareas)
  - 🎫 `Helpdesk-MS` (11 tareas)
  - 📦 `Inventario-MS` (4 tareas)
  - 🔐 `Auth-MS` (2 tareas)
  - 📢 `MKT-MS` (1 tarea)
- **Historial de Migración**:
  - Migradas **97 tareas y sub-épicas** desde la lista *1er Fase* de ClickUp (`https://app.clickup.com/90141246758/v/l/li/901418749229`).
  - Script automatizado con manejo de rate-limiting (429 exponential backoff) y asignación automática de estados (Backlog, Todo, In Progress, Done) y prioridades.

---

## 📌 4. Hoja de Ruta (Roadmap de Activación)

- [x] **Fase 1**: Análisis técnico de requisitos y arquitectura base.
- [x] **Fase 2**: Despliegue de instancia en producción (`projects.mastergroupve.com`).
- [x] **Fase 3**: Configuración de Workspace (`it---mg`), Proyecto (`MasterHub`), Módulos y Roles.
- [x] **Fase 4**: Migración masiva de tareas activas desde ClickUp (97/97 tareas de la 1ra Fase importadas exitosamente con API REST).
- [ ] **Fase 5**: Configuración de Webhooks y sincronizaciones automáticas (Telegram / Discord / GitHub CI).

---

## 🔗 Enlaces Relacionados
- [[pilar-proyectos|Pilar Proyectos]]
- [[masterhub-mg-hub|Proyecto: MasterHub (MG-HUB)]]
- [[webcastro|Proyecto: WebCastro (Desarrollo & Tareas)]]
