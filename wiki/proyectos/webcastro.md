---
title: "Proyecto: WebCastro"
type: "concept"
area: "proyectos"
created: 2026-09-12
updated: 2026-09-12
tags:
  - proyectos
  - payload-cms
  - nextjs
  - postgresql
  - tailwind
---

# 🌐 Proyecto: WebCastro

**WebCastro** es un sitio web corporativo de alto rendimiento construido con **Payload CMS 3.88**, **Next.js 16**, **React 19** y almacenamiento en la nube.

**Área**: [[Área Proyectos - Software Independiente|pilar-proyectos.md]]  
**Subagentes Evaluadores**: [[Subagente Frontend UI Expert|../../agents/frontend_ui_expert.md]] & [[Subagente Backend JS Expert|../../agents/backend_js_expert.md]]

---

## 🛠️ Stack Tecnológico

- **CMS Headless**: Payload CMS `3.88` (con Lexical Rich Text, SEO plugin, Form Builder, Redirects & Search plugins).
- **Framework Web**: Next.js `16.3` + React `19.2`
- **Base de Datos**: PostgreSQL adaptado vía `@payloadcms/db-postgres`
- **Estilos & UI**: Tailwind CSS `4.1`, Radix UI Primitives, Lucide Icons.
- **Almacenamiento de Medios**: Vercel Blob (`@payloadcms/storage-vercel-blob`)
- **Testing & E2E**: Vitest + Playwright (`@playwright/test`)
- **Procesamiento de Imágenes**: Sharp `0.34`

---

## ⚡ Comandos Principales

- `pnpm dev`: Iniciar servidor de desarrollo en Next.js + Payload Admin.
- `pnpm build`: Generar migraciones de Payload y compilar la aplicación.
- `pnpm payload`: Iniciar comandos CLI de Payload CMS.
- `pnpm test`: Ejecutar suites de integración y pruebas E2E.

---

## 🔗 Relación en 2brain
- [[Área Programación - Conocimiento Técnico|../programacion/pilar-programacion.md]]
