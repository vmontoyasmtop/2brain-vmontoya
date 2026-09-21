---
title: "SOP: Protocolo Oficial de Creación de Tickets en MasterHub Helpdesk"
type: "concept"
area: "trabajo"
created: 2026-09-21
updated: 2026-09-21
sources:
  - "raw/trabajo/soporte_helpdesk.md"
tags:
  - sop
  - helpdesk
  - masterhub
  - xetux
  - tickets
---

# 📋 SOP: Protocolo Oficial de Creación de Tickets en MasterHub Helpdesk

Este protocolo establece el procedimiento estándar e inalterable que **ALFRED** y sus subagentes deben ejecutar cuando el usuario (**Señor**) solicite crear, registrar o procesar tickets de soporte técnico para **MasterHub Helpdesk**.

---

## 🏛️ 1. Arquitectura y Entorno de Ejecución

* **Sistema Destino**: **MasterHub Helpdesk** (Microservicio `helpdesk-sm`).
* **Directorio del Proyecto**: `C:\Users\vmontoyaMG\Desktop\MasterHub\helpdesk-sm`
* **Base de Datos Centralizada**: **PostgreSQL en Aiven Cloud** (`helpdesk_db`).
* **Cadena de Conexión**: `postgres://avnadmin:[PASSWORD]@pg-masterhub-masterhub.j.aivencloud.com:28688/helpdesk_db?sslmode=no-verify` (Variable de entorno `DATABASE_URL` en `Desktop/MasterHub/helpdesk-sm/.env`).
* **Mecanismo de Inserción Nativo**: Cliente ORM Prisma (`@prisma/client`) o ejecución via `npx tsx prisma/create-today-tickets.ts`.

> [!IMPORTANT]
> **Regla de Oro**: NUNCA crear los tickets de soporte IT en herramientas externas como ClickUp cuando el usuario solicite tickets de Helpdesk/MasterHub. La fuente de verdad oficial es la base de datos de **MasterHub (`helpdesk_db`) en Aiven Cloud**.

---

## 📐 2. Estándar de Campos del Ticket (`Prisma Schema`)

Al recibir un reporte (audio de Telegram en `raw/inbox/` o texto en el chat), ALFRED mapeará los datos a la estructura oficial del modelo `Ticket`:

| Campo Prisma | Tipo / Enum | Valor / Regla Mapeada |
| :--- | :--- | :--- |
| `title` | `String` | `[Sucursal/Sede] Breve resumen - Nombre del Solicitante` |
| `description` | `String` (Text) | Detalle completo de la falla, comportamiento anómalo y contexto. |
| `type` | `INCIDENT \| REQUEST` | `INCIDENT` para fallas/fallos, `REQUEST` para requerimientos. |
| `source` | `PHONE \| WALK_IN \| EMAIL \| WEB` | `PHONE` (si proviene de audio/llamada) o `WALK_IN` / `WEB`. |
| `status` | `TicketStatus` | `OPEN` (por defecto al crear) o `IN_PROGRESS`. |
| `priority` | `LOW \| MEDIUM \| HIGH \| CRITICAL` | Clasificación técnica de severidad del problema. |
| `urgency` | `LOW \| HIGH` | Nivel Eisenhower de urgencia operacional. |
| `importance` | `LOW \| HIGH` | Nivel Eisenhower de impacto al negocio. |
| `siteId` & `siteName` | `String` | Identificador y nombre de la sucursal (ej: `site_bqto` / `Sucursal Barquisimeto`). |
| `requesterUserId` | `String` | ID slug del usuario (ej: `user_edgar_bqto`). |
| `requesterName` | `String` | Nombre completo y cargo del solicitante. |
| `assigneeName` | `String` | **Víctor Montoya** (por defecto). |
| `assigneeEmail` | `String` | `soporte@mastergroupve.com` (por defecto). |

---

## ⚡ 3. Flujo Paso a Paso de Ejecución para ALFRED

```mermaid
flowchart TD
    A["🎙️ Reporte Recibido (Telegram Inbox / Chat)"] --> B["🔍 Extraer Sucursal, Solicitante y Falla"]
    B --> C["📝 Formatear Campos según Estándar Prisma"]
    C --> D["⚡ Ejecutar Script Nativo TSX en helpdesk-sm"]
    D --> E["☁️ Confirmar Registro en Aiven Cloud helpdesk_db"]
    E --> F["✅ Entregar Confirmación Ejecutiva con ID al Señor"]
```

1. **Captura e Ingesta**:
   - Si proviene de Telegram: Leer el archivo sidecar `.md` generado en `raw/inbox/`.
   - Si proviene de dictado directo: Extraer la sucursal, el usuario afectado y la falla.
2. **Ejecución en MasterHub**:
   - Navegar a `C:\Users\vmontoyaMG\Desktop\MasterHub\helpdesk-sm`.
   - Incorporar o ejecutar la inserción con `npx tsx prisma/create-today-tickets.ts`.
3. **Verificación & Informe**:
   - Confirmar el retorno exitoso de `id`, `status` y `createdAt`.
   - Presentar un informe ejecutivo claro con el ID único asignado.

---

## 🔗 Enlaces Relacionados
* [[pilar-trabajo-xetux|Pilar Trabajo & Soporte IT Xetux]]
* [[index|Índice Maestro de 2brain]]
