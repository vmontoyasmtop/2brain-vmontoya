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
- **Estado actual**: 🟢 **PROYECTO ACTIVO (En Fase de Despliegue y Pruebas)**.
- **Caso de uso**: Control de proyectos de desarrollo de software (Brotapp, MasterHub, CRM-MG, Meniox) y flujo de tareas del equipo IT.

---

## 🛠️ 2. Stack Tecnológico & Arquitectura

| Componente | Tecnología |
| :--- | :--- |
| **Frontend UI** | Next.js 14 / React (TypeScript) |
| **Backend API** | Python / Django REST Framework |
| **Base de Datos** | PostgreSQL 15+ |
| **Caché / Queues** | Redis (Valkey) |
| **Object Storage** | MinIO (S3 Compatible) o AWS S3 |
| **Proxy / SSL** | Traefik / Nginx |

---

## 🚀 3. Guía Paso a Paso para Activar el Proyecto

### Opción A: Activación Rápida Local (Entorno de Pruebas en PC)
Para probar Plane localmente en Windows/Linux usando Docker Desktop o Docker Engine:

1. **Clonar repositorio / Crear directorio de trabajo**:
   ```bash
   mkdir -p ~/projects/plane-local && cd ~/projects/plane-local
   ```
2. **Descargar e iniciar con el script oficial de Plane**:
   ```bash
   curl -fsSL https://prime.plane.so/install/ | sh -
   ```
3. **Seleccionar opción 1 (Setup)**, configurar puertos (ej. `8080`) y presionar opción **2 (Start)**.
4. **Acceder en el navegador**: `http://localhost:8080` (Crear cuenta de Administrador Inicial).

---

### Opción B: Activación en Servidor Producción (VPS / Cloud)

#### Vía Coolify (PaaS Automático - Recomendado):
1. Abrir panel de **Coolify** ➔ `New Resource` ➔ `Services`.
2. Buscar **Plane** en el catálogo de servicios.
3. Asignar dominio (ej. `plane.mastergroupve.com`).
4. Presionar `Deploy`. Coolify aprovisiona SSL de Let's Encrypt, PostgreSQL, MinIO y Redis automáticamente.

#### Vía Docker Compose manual en VPS:
```bash
# 1. Descargar script de despliegue autónomo
curl -fsSL https://prime.plane.so/install/ | sh -

# 2. Editar plane.env con el dominio público y secreto JWT
nano plane-app/plane.env

# 3. Iniciar servicios en segundo plano
./setup.sh
```

---

## 📌 4. Hoja de Ruta (Roadmap de Activación)

- [x] **Fase 1**: Análisis técnico de requisitos y arquitectura base.
- [ ] **Fase 2**: Despliegue de instancia de prueba (Local / VPS).
- [ ] **Fase 3**: Configuración de primer espacio de trabajo (Workspace), Proyectos y Roles de usuario.
- [ ] **Fase 4**: Integración con Webhooks (Notificaciones en Telegram/Discord/Slack).
- [ ] **Fase 5**: Migración de tareas activas de proyectos 2brain a Plane.

---

## 🔗 Enlaces Relacionados
- [[pilar-proyectos|Pilar Proyectos]]
- [[masterhub-mg-hub|Proyecto: MasterHub (MG-HUB)]]
