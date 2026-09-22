---
title: "Proyecto: MasterHub (MG-HUB)"
type: "project"
area: "proyectos"
created: 2026-09-12
updated: 2026-09-18
tags:
  - 
---

# 💼 Proyecto: MasterHub (MG-HUB)

**MasterHub** es una plataforma de software empresarial basada en una arquitectura distribuida de **Microservicios NestJS** unificada con un frontend Next.js mediante **npm workspaces** y **Nx Monorepo**.

**Ubicación Local en Escritorio**: `C:\Users\vmontoyaMG\Desktop\MG-HUB`  
**Área**: [[pilar-proyectos|Área Proyectos - Software Independiente]]  
**Repositorio Git (`team`)**: `git@github.com:vmontoyamg-png/MG-HUB.git`  
**Agente Líder Orquestador**: 🧙‍♂️ **Grandalf** (`C:\Users\vmontoyaMG\Desktop\2brain-MG\agents\grandalf.md`)  
**Equipo de Subagentes Especializados**:
- ⚔️ **Aragorn** (`aragorn_pm.md`): PM & Scrum Master
- ⛏️ **Gimli** (`gimli_backend.md`): Backend NestJS & APIs
- 🏹 **Legolas** (`legolas_ui.md`): Frontend Next.js & UI/UX
- 🔮 **Galadriel** (`galadriel_db.md`): PostgreSQL & Prisma ORM
- 💍 **Frodo** (`frodo_devops.md`): Docker Compose & Nx Monorepo
- 👑 **Elrond** (`elrond_code.md`): Arquitectura Fullstack
- 🏛️ **Boromir** (`boromir_finance.md`): Módulo `finance-ms`
- 🛡️ **Samwise** (`samwise_it.md`): Operaciones IT & Helpdesk
- 📜 **Merry** (`merry_docs.md`): Documentación Técnica
- 🖋️ **Pippin** (`pippin_writer.md`): Contenido Ejecutivo

---

## 🛠️ Microservicios & Estructura

- **`api-gateway`**: Gateway centralizador de peticiones HTTP/RPC.
- **`auth-ms`**: Servicio de autenticación, JWT e identidades.
- **`hr-ms`**: Servicio de gestión de Recursos Humanos (Human Resources).
- **`finance-ms`**: Servicio de gestión de Cuentas por Pagar (CxP), Egresos, Fiscal SENIAT, CxC y Caja Chica. Ver [[masterhub-modulo-finanzas|Módulo de Finanzas: Especificación Técnica (finance-ms)]].
- **`helpdesk-sm`**: Servicio de mesas de ayuda y soporte. Ver [[masterhub-helpdesk-api|Guía de Operación y API Helpdesk]].
- **`inventory-sm`**: Servicio de inventario y stock.
- **`wiki-sm`**: Servicio de base de conocimiento interna.
- **`frontend-ui-dashboard`**: Dashboard administrativo principal en Next.js.

---

## 📖 Documentación Interna Relacionada
- [[masterhub-modulo-finanzas|Módulo de Finanzas: Especificación Técnica (finance-ms)]]
- [[masterhub-helpdesk-api|MasterHub Helpdesk - Guía de Operación y API]]


---

## ⚙️ Stack & Infraestructura

- **Compilación**: SWC Compiler (`@swc/core`, `@swc-node/register`) para builds ultra-rápidos.
- **Contenedores**: Docker Compose para orquestación de servicios e infraestructura (`docker-compose.yml`).
- **Monorepo Engine**: Nx `23` + Cross-env.

---

## ⚡ Comandos Principales

- `npm run start:all`: Iniciar todos los microservicios y el dashboard simultáneamente.
- `npm run docker:up`: Levantar todos los servicios en contenedores Docker.
- `npm run docker:down`: Detener infraestructura Docker.

---

## 🔗 Relación en 2brain
- [[pilar-programacion|Área Programación - Conocimiento Técnico]]
