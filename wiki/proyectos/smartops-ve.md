---
title: "Proyecto: SmartOps VE"
type: "project"
area: "proyectos"
created: 2026-09-12
updated: 2026-09-18
tags:
  - 
---

# ⚡ Proyecto: SmartOps VE

**SmartOps VE** es un portal web corporativo y plataforma de servicios técnicos desplegada sobre Google Cloud Run y respaldada por Firebase Cloud Functions.

**Área**: [[pilar-proyectos|Área Proyectos - Software Independiente]]  
**Subagentes Evaluadores**: [Subagente Frontend UI Expert](../../agents/frontend_ui_expert.md) & [Subagente Backend JS Expert](../../agents/backend_js_expert.md)

---

## 🛠️ Stack Tecnológico

- **Frontend Framework**: Next.js `15.5` + React `18.3`
- **UI Components & Estilos**: Material UI (`@mui/material` `7`), Tailwind CSS `3.4`, Radix UI, Framer Motion.
- **Backend / Cloud Serverless**: Firebase Admin SDK `14` + Firebase Functions `6`
- **Linter & Formatter**: Biome JS `1.9`
- **Despliegue & DevOps**: Docker (Multi-stage build) + Google Cloud Run (`gcloud run deploy`)

---

## ⚡ Comandos de Despliegue y Desarrollo

- `npm run dev`: Servidor de desarrollo en puerto 3000.
- `npm run docker:dev`: Compilar e iniciar contenedor Docker local.
- `npm run deploy:cloud-run`: Desplegar imagen de producción en Google Cloud Run.
- `npm run lint`: Ejecutar Biome Linter & TypeScript check.

---

## 🔗 Relación en 2brain
- [[pilar-programacion|Área Programación - Conocimiento Técnico]]
