---
title: "Proyecto: CRM-MG"
type: "concept"
area: "proyectos"
created: 2026-09-12
updated: 2026-09-12
tags:
  - proyectos
  - crm
  - nestjs
  - prisma
  - openai
  - websockets
  - nx
---

# 🏢 Proyecto: CRM-MG

**CRM-MG** es un sistema monorepo empresarial de Customer Relationship Management (CRM) potenciado con Inteligencia Artificial (OpenAI) y comunicación en tiempo real.

**Área**: [[Área Proyectos - Software Independiente|pilar-proyectos.md]]  
**Subagentes Evaluadores**: [[Subagente Backend JS Expert|../../agents/backend_js_expert.md]] & [[Subagente Frontend UI Expert|../../agents/frontend_ui_expert.md]]

---

## 🛠️ Arquitectura & Stack Tecnológico

### ⚙️ Backend (API en `apps/api`)
- **Framework**: NestJS `11` + Express platform
- **ORM & Base de Datos**: Prisma ORM `6` + PostgreSQL
- **IA & Automatización**: OpenAI Node SDK (`openai`)
- **Tiempo Real**: WebSockets con `@nestjs/websockets` & `socket.io`
- **Autenticación**: Passport JWT (`@nestjs/passport` + `bcrypt`)
- **Documentación API**: Swagger (`@nestjs/swagger`)
- **Validación DTO**: `class-validator` & `class-transformer`

### 🎨 Frontend (Web en `apps/web`)
- **Framework**: Next.js / React
- **Gestión Monorepo**: Nx Workspaces `23`

---

## ⚡ Comandos de Base de Datos y Ejecución

- `npm run db:generate`: Generar cliente de Prisma.
- `npm run db:push`: Aplicar cambios de esquema Prisma a PostgreSQL.
- `npm run start:api:dev`: Iniciar API en modo desarrollo con auto-reload.
- `npm run start:web`: Iniciar frontend web.

---

## 🔗 Relación en 2brain
- [[Área Programación - Conocimiento Técnico|../programacion/pilar-programacion.md]]
- [[Área Finanzas - Gestión Económica|../finanzas/pilar-finanzas-personales.md]]
