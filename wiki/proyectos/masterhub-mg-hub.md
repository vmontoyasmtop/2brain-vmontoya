---
title: "Proyecto: MasterHub (MG-HUB)"
type: "concept"
area: "proyectos"
created: 2026-09-12
updated: 2026-09-12
tags:
  - proyectos
  - microservicios
  - nestjs
  - nextjs
  - docker
  - nx
---

# 💼 Proyecto: MasterHub (MG-HUB)

**MasterHub** es una plataforma de software empresarial basada en una arquitectura distribuida de **Microservicios NestJS** unificada con un frontend Next.js mediante **npm workspaces** y **Nx Monorepo**.

**Área**: [[Área Proyectos - Software Independiente|pilar-proyectos.md]]  
**Subagentes Evaluadores**: [[Subagente Backend JS Expert|../../agents/backend_js_expert.md]] & [[Subagente Frontend UI Expert|../../agents/frontend_ui_expert.md]]

---

## 🛠️ Microservicios & Estructura

- **`api-gateway`**: Gateway centralizador de peticiones HTTP/RPC.
- **`auth-ms`**: Servicio de autenticación, JWT e identidades.
- **`hr-ms`**: Servicio de gestión de Recursos Humanos (Human Resources).
- **`finance-ms`**: Servicio de gestión de Cuentas por Pagar (CxP), Egresos, Fiscal SENIAT, CxC y Caja Chica. Ver [[Módulo de Finanzas: Especificación Técnica (finance-ms)|masterhub-modulo-finanzas.md]].
- **`helpdesk-sm`**: Servicio de mesas de ayuda y soporte. Ver [[Guía de Operación y API Helpdesk|masterhub-helpdesk-api.md]].
- **`inventory-sm`**: Servicio de inventario y stock.
- **`wiki-sm`**: Servicio de base de conocimiento interna.
- **`frontend-ui-dashboard`**: Dashboard administrativo principal en Next.js.

---

## 📖 Documentación Interna Relacionada
- [[Módulo de Finanzas: Especificación Técnica (finance-ms)|masterhub-modulo-finanzas.md]]
- [[MasterHub Helpdesk - Guía de Operación y API|masterhub-helpdesk-api.md]]


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
- [[Área Programación - Conocimiento Técnico|../programacion/pilar-programacion.md]]
