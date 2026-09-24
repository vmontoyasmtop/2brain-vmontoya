---
title: "Proyecto: WebCastro"
type: "project"
area: "proyectos"
created: 2026-09-12
updated: 2026-09-18
tags:
  - 
---

# 🌐 Proyecto: WebCastro

**WebCastro** es un sitio web corporativo de alto rendimiento construido con **Payload CMS 3.88**, **Next.js 16**, **React 19** y almacenamiento en la nube.

**Área**: [[pilar-proyectos|Área Proyectos - Software Independiente]]  
**Subagentes Asignados**: [Subagente Frontend UI Expert](../../agents/frontend_ui_expert.md) & [Subagente Backend JS Expert](../../agents/backend_js_expert.md)

---

## 👥 Matriz de Delegación a Subagentes

Para garantizar la mantenibilidad y evolución sin fricciones de **WebCastro**, las responsabilidades quedan delegadas formalmente de la siguiente manera:

| Dominio / Componente | Subagente Responsable | Tareas Delegadas |
| :--- | :--- | :--- |
| **Frontend, UI & UX** | 🎨 [Subagente Frontend UI Expert](../../agents/frontend_ui_expert.md) | - Mantenimiento y estilizado en Tailwind CSS `4.1` & Radix UI primitives.<br>- Botón flotante y de header para WhatsApp ([CastroHeader.tsx](file:///C:/Users/vmontoyaMG/Desktop/WebCastro/src/Header/CastroHeader.tsx), [WhatsAppFloatingButton.tsx](file:///C:/Users/vmontoyaMG/Desktop/WebCastro/src/components/landing/WhatsAppFloatingButton.tsx)).<br>- Optimización SEO dinámico, OpenGraph, `robots.txt` y rendición visual en React 19.<br>- Formulario de contacto interactivo en cliente. |
| **Backend, CMS & Infra** | ⚙️ [Subagente Backend JS Expert](../../agents/backend_js_expert.md) | - Configuración Payload CMS `3.88` y esquemas de Lexical Rich Text.<br>- Base de Datos PostgreSQL, soporte `@payloadcms/db-postgres` y migraciones DB.<br>- Almacenamiento Vercel Blob (`@payloadcms/storage-vercel-blob`).<br>- Script de prebuild/limpieza de migraciones dev (`scripts/clean-dev-migrations.mjs`).<br>- Configuración de proveedor SMTP de Gmail (`CONTACT_EMAIL_RECEIVER`, `SMTP_USER`, `SMTP_PASS`) en el controlador [route.ts](file:///C:/Users/vmontoyaMG/Desktop/WebCastro/src/app/api/contact/route.ts). |

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

- [x] **Auditoría Frontend Completa (Subagente Frontend UI Expert)**: Verificados [CastroHeader.tsx](file:///C:/Users/vmontoyaMG/Desktop/WebCastro/src/Header/CastroHeader.tsx), [WhatsAppFloatingButton.tsx](file:///C:/Users/vmontoyaMG/Desktop/WebCastro/src/components/landing/WhatsAppFloatingButton.tsx), `layout.tsx` y SEO metadatos. TypeScript Check 0 errores.
- [x] **Auditoría Backend & CMS Completa (Subagente Backend JS Expert)**: Payload 3.88 en orden con Neon Postgres, Vercel Blob Storage activo y script `npm run prebuild` verificado contra DB.
- [x] **Botón de WhatsApp en Header**: Actualizado a verde `#25D366` con texto *"Escríbenos"* y enlace directo a chat.
- [x] **Botón Flotante de WhatsApp**: Componente integrado en layout principal con desplegable multi-número (`+58 422 038-7323` y `+58 412 964-3616`).
- [x] **Plantilla de Correo HTML con Respuesta WhatsApp**: Controlador REST en [route.ts](file:///C:/Users/vmontoyaMG/Desktop/WebCastro/src/app/api/contact/route.ts) con plantilla HTML de alta conversión.
- [x] **Optimización SEO, Metadatos & Sitemap**: Metadatos globales, OpenGraph, Twitter Cards, `robots.txt` y `sitemap.xml` dinámico.
- [x] **Solución a Fallo Vercel Build (`enum_pages_blocks_cta_button_action already exists`)**: Convertidas las declaraciones de tipos ENUM, tablas, claves foráneas e índices en la migración [20260912_022810.ts](file:///C:/Users/vmontoyaMG/Desktop/WebCastro/src/migrations/20260912_022810.ts) a bloques PL/pgSQL totalmente **idempotentes** con `DO $$ BEGIN ... EXCEPTION WHEN duplicate_object THEN null; END $$;` e `IF NOT EXISTS`. Subido a `origin/main` para desbloquear la compilación automática en Vercel.
- [x] **Manual Tecnológico de Gestión de Contenido (Payload CMS)**: Documentación integral de arquitectura informativa, catálogo de 19 bloques modulares, gestión de colecciones/globales, live preview y revalidación ISR en [MANUAL_TECNICO_GESTION_CONTENIDO_PAYLOAD.md](file:///C:/Users/vmontoyaMG/Desktop/WebCastro/docs/MANUAL_TECNICO_GESTION_CONTENIDO_PAYLOAD.md).
- [x] **Persistencia de Consultas en BD & Panel Payload**: Creada la colección `Consultas` ([Consultas/index.ts](file:///C:/Users/vmontoyaMG/Desktop/WebCastro/src/collections/Consultas/index.ts)), migración idempotente [20260919_032259_add_consultas.ts](file:///C:/Users/vmontoyaMG/Desktop/WebCastro/src/migrations/20260919_032259_add_consultas.ts) y persistencia activa en el controlador [route.ts](file:///C:/Users/vmontoyaMG/Desktop/WebCastro/src/app/api/contact/route.ts).
- [x] **Ajustes de UI/UX en Sobre Nosotros**: Reubicación inferior del badge flotante *"100% Calidad Garantizada"* (`-bottom-14 sm:-bottom-16`) para liberar la foto y justificación elegante de párrafos con `hyphens-auto`.
- [x] **Corrección de Toast en QuoteModal (`c9ab13e`)**: Resuelto error en [QuoteModal.tsx](file:///C:/Users/vmontoyaMG/Desktop/WebCastro/src/components/landing/QuoteModal.tsx) donde `e.currentTarget` se perdía tras la llamada asíncrona a la API, disparando erróneamente un mensaje de fallo de red en lugar del toast de confirmación verde *"¡Solicitud Enviada!"*.
- [x] **Checklist y Justificación en Hero (`906ec9f`)**: Añadido parseo inteligente en [Hero/Component.tsx](file:///C:/Users/vmontoyaMG/Desktop/WebCastro/src/collections/Pages/blocks/Hero/Component.tsx) para transformar automáticamente listas y objetivos con viñetas en un checklist con tarjetas translúcidas e iconos dorados de verificación (`fa-circle-check`), además de justificar los párrafos descriptivos con `hyphens-auto`.
- [x] **Despliegue a Producción Vercel (`906ec9f`)**: Subido a `origin/main` con soporte completo de Webpack en build y renderizado dinámico de objetivos.
- [ ] **Pendiente (Configuración de Gmail SMTP)**: Colocar las credenciales reales en `.env` cuando se disponga de la Contraseña de Aplicación de 16 caracteres (`SMTP_USER`, `SMTP_PASS`, `CONTACT_EMAIL_RECEIVER`).

---

## 🔗 Relación en 2brain
- [[pilar-programacion|Área Programación - Conocimiento Técnico]]
