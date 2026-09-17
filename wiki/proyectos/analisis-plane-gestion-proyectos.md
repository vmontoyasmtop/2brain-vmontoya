---
title: "Análisis Técnico y Despliegue de Plane (makeplane/plane)"
type: "concept"
area: "proyectos"
created: 2026-09-17
updated: 2026-09-17
tags:
  - plane
  - jira-alternative
  - self-hosted
  - docker
  - coolify
  - hetzner
---

# 📋 Análisis Técnico y Guía de Despliegue: Plane (`makeplane/plane`)

*Análisis para evaluación de self-hosting de Plane como herramienta de gestión de proyectos (alternativa open-source a Jira/Linear/ClickUp).*

---

## 🔍 1. Resumen Ejecutivo
**Plane** es una plataforma *open-source* de gestión de proyectos diseñada para equipos de ingeniería de software. Ofrece tableros Kanban, listas, seguimiento de Sprints (Cycles), backlog, roadmaps de módulos (Modules) y gestión de incidencias con una interfaz reactiva de alto rendimiento.

---

## 🛠️ 2. Stack Tecnológico & Arquitectura
- **Frontend**: Next.js / React (TypeScript).
- **Backend API**: Python / Django REST Framework.
- **Base de Datos Relacional**: PostgreSQL.
- **Caché y Cola de Trabajos Asíncronos**: Redis.
- **Almacenamiento de Archivos y Soportes**: MinIO (S3 compatible) o Amazon S3.
- **Reverse Proxy**: Nginx / Traefik.

---

## 🖥️ 3. Requisitos de Infraestructura
- **CPU**: Mínimo 2 vCPUs (Recomendado: 4 vCPUs para producción).
- **RAM**: Mínimo 4 GB RAM (Recomendado: 8 GB RAM).
- **Disco**: 20–40 GB SSD.
- **OS**: Ubuntu 22.04 LTS / 24.04 LTS con Docker Engine & Compose.

---

## 🚀 4. Métodos de Despliegue en Nuestro Servidor (Hetzner Cloud)

### Método A: Vía Coolify (PaaS) — Recomendado
1. En el panel de **Coolify**, ir a `New Resource` ➔ `Services`.
2. Seleccionar **Plane** del catálogo oficial.
3. Configurar dominio público (ej. `plane.mastergroupve.com`).
4. Hacer clic en `Deploy` (Coolify gestiona SSL Traefik, PostgreSQL, Redis y MinIO automáticamente).

### Método B: Vía CLI / Docker Compose
1. Conectar por SSH al servidor VPS.
2. Ejecutar script oficial de instalación:
   ```bash
   curl -fsSL https://prime.plane.so/install/ | sh -
   ```
3. Configurar el archivo `plane-app/plane.env` (Dominio, Puertos).
4. Iniciar servicios mediante `./setup.sh` (Opción 2 - Start).

---

*Nota: Guardado para generación posterior de Google Doc corporativo.*
