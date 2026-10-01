---
title: "Propuesta de Integración: Google Workspace APIs en MasterHub Helpdesk"
type: "proposal"
area: "trabajo"
created: 2026-09-29
updated: 2026-09-29
tags:
  - trabajo
  - masterhub
  - helpdesk
  - google-workspace
  - gmail-api
  - calendar-api
  - tasks-api
  - drive-api
---

# 🚀 Propuesta de Arquitectura: Integración Google Workspace en Helpdesk MasterHub

## 📌 1. Resumen Ejecutivo
El presente documento describe el diseño técnico, la arquitectura de autenticación y los casos de uso para conectar **MasterHub Helpdesk** (`apps/helpdesk-sm`) con las APIs de **Google Workspace** (**Gmail**, **Google Calendar**, **Google Tasks** y **Google Drive**), automatizando los flujos de soporte técnico entre la jefatura de IT (Ing. Víctor Montoya), el técnico de soporte (Romny Simoza) y los usuarios de Master Group.

---

## 🎯 2. Objetivos y Casos de Uso por API

```mermaid
flowchart LR
    subgraph MH["🎫 MasterHub Helpdesk"]
        T["Ticket Creado / Asignado"]
        ATT["Adjuntos (Fotos, PDFs, Logs)"]
        VIS["Visita Técnica Programada"]
        NOT["Notificación / Respuesta"]
    end

    subgraph GOOGLE["☁️ Google Workspace APIs"]
        GM["📧 Gmail API\n(soporte@mastergroupve.com)"]
        GC["📅 Google Calendar API\n(Agendas Técnicas)"]
        GT["☑️ Google Tasks API\n(Lista de Romny / Técnico)"]
        GD["📁 Google Drive API\n(Almacenamiento Corporativo)"]
    end

    NOT <-->|Lectura y Envío de Hilos (ThreadID)| GM
    T -->|Crea Tarea Automática| GT
    VIS -->|Crea Evento con Notificación| GC
    ATT -->|Almacena en Carpeta del Ticket| GD
```

### 1. 📧 Gmail API (`soporte@mastergroupve.com`)
* **Inbound (Email to Ticket):** Ingesta automática de correos entrantes dirigidos a `soporte@mastergroupve.com`. El sistema extrae asunto, cuerpo y adjuntos para generar el ticket sin intervención manual.
* **Outbound & Threading:** Las respuestas emitidas desde la plataforma MasterHub se envían a través de la cuenta oficial de Gmail manteniendo el `threadId`, garantizando que el usuario final visualice un único hilo ordenado y evitando filtros de spam corporativo.

### 2. ☑️ Google Tasks API (Asignación Automática a Técnicos)
* **Asignación sin Fricción:** Al asignar o delegar un ticket a Romny Simoza (u otro técnico), el backend crea automáticamente una tarea en su lista de **Google Tasks** vinculada a su cuenta de Google Workspace (`soporte@mastergroupve.com` o correo asignado).
* **Campos Sincronizados:** Título del ticket, fecha límite (`dueDate`), prioridad y enlace directo a la vista de resolución en MasterHub.
* **Cierre Bidireccional:** Al tachar la tarea en la app móvil o panel lateral de Google Tasks, MasterHub detecta la actualización y transiciona el ticket a estado `RESOLVED` o `IN_PROGRESS`.

### 3. 📅 Google Calendar API (Agendamiento de Visitas Técnicas)
* **Time-Blocking Operativo:** Cuando un ticket requiere una intervención en sitio o visita a sucursal Xetux con fecha programada (`scheduledDate`), se crea automáticamente un evento en el calendario de Romny y de la sucursal/solicitante.
* **Prevención de Conflictos:** Bloquea la agenda técnica para evitar solapamientos durante las jornadas de inventario o soporte de cajas.

### 4. 📁 Google Drive API (Almacenamiento Descentralizado de Adjuntos)
* **Protección del Almacenamiento VPS:** Sustituye el almacenamiento de archivos pesados en el disco del servidor por una estructura organizada en Google Drive Corporativo:
  `MasterHub / Helpdesk / 2026 / Ticket-{id}/`
* **Acceso y Permisos:** Genera enlaces seguros de visualización previa (`webViewLink`) y descarga para usuarios autenticados.

---

## 🏛️ 3. Estrategia de Autenticación: Service Account con Delegación de Dominio

Para evitar que los analistas deban realizar inicios de sesión continuos con ventanas emergentes de OAuth2, se implementará una **Cuenta de Servicio (Google Cloud Service Account) con Domain-Wide Delegation**:

```text
[Backend: helpdesk-sm] 
      │
      ├── (JWT Bearer con Service Account Key JSON)
      ▼
[Google OAuth Token Endpoint]
      │ (Impersonación de soporte@mastergroupve.com o técnico)
      ▼
[Google Workspace APIs: Gmail / Calendar / Tasks / Drive]
```

### Requisitos de Configuración en Google Cloud:
1. Proyecto en **Google Cloud Console** (ej. `masterhub-workspace-integration`).
2. Activación de APIs:
   - `Gmail API`
   - `Google Calendar API`
   - `Tasks API`
   - `Google Drive API`
3. Creación de Service Account con descarga de clave `service-account.json`.
4. Autorización en **Google Workspace Admin** (`admin.google.com`) -> *Seguridad* -> *Control de Acceso y Datos* -> *Delegación de todo el dominio*:
   - Scopes autorizados:
     - `https://www.googleapis.com/auth/gmail.modify`
     - `https://www.googleapis.com/auth/calendar`
     - `https://www.googleapis.com/auth/tasks`
     - `https://www.googleapis.com/auth/drive.file`

---

## 💻 4. Plan de Implementación en Código (`apps/helpdesk-sm`)

### A. Dependencias
```bash
npm install googleapis
```

### B. Estructura Modular de Archivos
```text
apps/helpdesk-sm/src/google/
├── google.module.ts
├── google-auth.service.ts
└── services/
    ├── google-gmail.service.ts
    ├── google-calendar.service.ts
    ├── google-tasks.service.ts
    └── google-drive.service.ts
```

### C. Ajuste en Esquema de Base de Datos (`prisma/schema.prisma`)
```prisma
model Ticket {
  // ... campos existentes
  googleThreadId        String?
  googleCalendarEventId String?
  googleTaskId          String?
  googleDriveFolderId   String?
}

model TicketAttachment {
  // ... campos existentes
  googleDriveFileId     String?
  googleDriveWebViewUrl String?
}
```

---

## 📋 5. Próximos Pasos para Mañana en la Mañana
1. [ ] **Revisión de Accesos:** Validar acceso de Don Víctor a Google Cloud Console y consola de Google Workspace Admin de Master Group.
2. [ ] **Creación de Service Account:** Generar credenciales JSON para el entorno Staging / Local.
3. [ ] **Scaffold del Módulo Google:** Implementar el módulo `google/` y services en `helpdesk-sm`.
4. [ ] **Sincronización de Tasks:** Probar el endpoint de asignación automática de tareas hacia Romny.
