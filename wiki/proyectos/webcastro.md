---
title: "Proyecto: WebCastro"
type: "concept"
area: "proyectos"
created: 2026-09-12
updated: 2026-09-15
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

## 🚀 Estado del Proyecto (Septiembre 2026)

- [x] **Botón de WhatsApp en Header**: Actualizado a verde `#25D366` con texto *"Escríbenos"* y enlace directo a chat en [CastroHeader.tsx](file:///C:/Users/vmontoyaMG/Desktop/WebCastro/src/Header/CastroHeader.tsx).
- [x] **Botón Flotante de WhatsApp**: Componente [WhatsAppFloatingButton.tsx](file:///C:/Users/vmontoyaMG/Desktop/WebCastro/src/components/landing/WhatsAppFloatingButton.tsx) integrado en el layout principal con menú desplegable para seleccionar números de atención (`+58 412 964-3616` y `+58 414 390-4751`).
- [x] **Plantilla de Correo HTML con Respuesta WhatsApp**: Controlador REST en [route.ts](file:///C:/Users/vmontoyaMG/Desktop/WebCastro/src/app/api/contact/route.ts) con plantilla HTML de alta conversión y botón directo para responder por WhatsApp al cliente.
- [x] **Optimización SEO, Metadatos & Sitemap**: Metadatos globales, OpenGraph, Twitter Cards, `robots.txt` y `sitemap.xml` dinámico configurados e integrados.
- [x] **Corrección de Build en Vercel (Migraciones Dev batch = -1)**: Creado script autoejecutable `scripts/clean-dev-migrations.mjs` en hook `prebuild` de `package.json` y `push: false` en `payload.config.ts` para eliminar automáticamente registros de desarrollo en PostgreSQL antes de la compilación en Vercel.
- [ ] **Pendiente (Configuración de Gmail SMTP)**: Colocar las credenciales reales en `.env` cuando el cliente o usuario disponga de la Contraseña de Aplicación de 16 caracteres (`SMTP_USER`, `SMTP_PASS`, `CONTACT_EMAIL_RECEIVER`).

---

## 🔗 Relación en 2brain
- [[Área Programación - Conocimiento Técnico|../programacion/pilar-programacion.md]]
