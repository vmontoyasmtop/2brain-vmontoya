---
title: "🛠️ MasterHub Helpdesk — Guía de Operación y API (Gestión de Tickets)"
type: "project"
area: "proyectos"
created: 2026-09-11
updated: 2026-09-18
tags:
  - 
---

# 🛠️ MasterHub Helpdesk — Guía de Operación y API (Gestión de Tickets)

**Proyecto**: [masterhub-mg-hub.md](file:///C:/Users/vmontoyaMG/Desktop/2brain/wiki/proyectos/masterhub-mg-hub.md)  
**Ubicación en Sistema**: `C:\Users\vmontoyaMG\Desktop\MasterHub`  
**Servicio Backend**: `helpdesk-sm` (NestJS Microservice + Prisma ORM + PostgreSQL)  
**API Gateway**: `api-gateway` (NestJS REST Gateway)  

---

## 📌 Visión General de la Módula Helpdesk

El módulo de **Helpdesk** de MasterHub administra solicitudes e incidencias técnicas y operativas con soporte nativo para la **Matriz de Eisenhower** (`urgency` e `importance`).

```mermaid
flowchart LR
    A["Frontend UI Dashboard (Next.js)"] -->|HTTP REST| B["API Gateway (NestJS :3000)"]
    B -->|Microservice Message Pattern| C["helpdesk-sm (NestJS MS)"]
    C -->|Prisma ORM| D["PostgreSQL DB"]
```

---

## 📊 Modelo de Datos del Ticket (`Prisma Schema`)

| Campo | Tipo | Valores / Descripción |
| :--- | :--- | :--- |
| `id` | `String` (cuid) | Identificador único del ticket |
| `title` | `String` | Título principal de la incidencia o requerimiento |
| `description` | `String` | Descripción detallada |
| `type` | `Enum` | `INCIDENT` \| `REQUEST` |
| `source` | `Enum` | `WEB` \| `EMAIL` \| `PHONE` \| `WALK_IN` |
| `status` | `Enum` | `OPEN` \| `IN_PROGRESS` \| `ON_HOLD` \| `RESOLVED` \| `CLOSED` \| `CANCELLED` |
| `priority` | `Enum` | `LOW` \| `MEDIUM` \| `HIGH` \| `CRITICAL` |
| `urgency` | `Enum` | `HIGH` \| `LOW` (Para Matriz de Eisenhower) |
| `importance` | `Enum` | `HIGH` \| `LOW` (Para Matriz de Eisenhower) |
| `siteId` / `siteName` | `String` | Sede u organización |
| `areaId` / `areaName` | `String` | Área o departamento |
| `requesterUserId` / `Name` | `String` | Usuario solicitante |
| `assigneeUserId` / `Name` | `String` | Técnico o analista asignado |
| `resolutionNotes` | `String` | Detalles y diagnóstico de la solución |

---

## 🌐 Endpoints HTTP REST (Vía `api-gateway`)

Todos los endpoints están prefijados con `/helpdesk/` y requieren autenticación `JwtAuthGuard`.

### 1. ➕ Crear Ticket (`POST /helpdesk/tickets`)
**Payload de Ejemplo**:
```json
{
  "title": "Fallo de Impresora en Oficina Central",
  "description": "La impresora HP LaserJet no responde a las peticiones de red.",
  "type": "INCIDENT",
  "source": "WEB",
  "priority": "HIGH",
  "urgency": "HIGH",
  "importance": "HIGH",
  "siteId": "site_01",
  "siteName": "Sede Principal",
  "requesterUserId": "user_123",
  "requesterName": "Juan Pérez"
}
```

---

### 2. 📋 Leer / Listar Tickets (`GET /helpdesk/tickets`)
**Parámetros Query**:
- `page`: Número de página (default: 1)
- `limit`: Cantidad por página (default: 10)
- `status`: Estado específico (`OPEN`, `IN_PROGRESS`, `RESOLVED`, etc.)
- `priority`: Prioridad (`LOW`, `MEDIUM`, `HIGH`, `CRITICAL`)
- `assigneeUserId`: Filtrar por técnico asignado
- `q`: Búsqueda textual por título o descripción

**Ejemplo de Consulta**:
`GET /helpdesk/tickets?status=OPEN&priority=HIGH&page=1&limit=20`

---

### 3. 🔍 Leer un Ticket Específico (`GET /helpdesk/tickets/:id`)
Devuelve la información completa del ticket junto con sus comentarios y archivos adjuntos.

---

### 4. ✏️ Actualizar Ticket (`PATCH /helpdesk/tickets/:id`)
**Payload de Ejemplo (Asignar Técnico y Cambiar Estado a En Proceso)**:
```json
{
  "status": "IN_PROGRESS",
  "assigneeUserId": "tech_456",
  "assigneeName": "Víctor Montoya",
  "assigneeEmail": "soporte@mastergroupve.com"
}
```

**Payload de Ejemplo (Resolver Ticket)**:
```json
{
  "status": "RESOLVED",
  "resolutionNotes": "Se reinició el spooler de impresión y se reconfiguró la IP estática."
}
```

---

### 5. 💬 Agregar Comentario (`POST /helpdesk/tickets/:id/comments`)
**Payload**:
```json
{
  "body": "Se ha solicitado repuesto de cable de red.",
  "authorName": "Víctor Montoya"
}
```

---

### 6. 📊 Matriz de Eisenhower de Tickets (`GET /helpdesk/tickets/eisenhower`)
Agrupa los tickets activos en los 4 cuadrantes según `urgency` e `importance`:
- **C1 (Urgente & Importante)**: `urgency: HIGH`, `importance: HIGH` (Hacer Inmediatamente)
- **C2 (No Urgente & Importante)**: `urgency: LOW`, `importance: HIGH` (Programar)
- **C3 (Urgente & No Importante)**: `urgency: HIGH`, `importance: LOW` (Delegar/Automatizar)
- **C4 (No Urgente & No Importante)**: `urgency: LOW`, `importance: LOW` (Eliminar)

---

## 🛠️ Cómo Probar la API de Helpdesk Localmente

1. **Iniciar Infraestructura**:
   ```bash
   cd C:\Users\vmontoyaMG\Desktop\MasterHub
   docker-compose up -d
   ```
2. **Iniciar Servicios de Desarrollo**:
   ```bash
   npm run start:all
   ```
3. **API Gateway URL**: `http://localhost:3000/helpdesk`

---

## ⚡ Inserción Directa en DB Aiven Cloud via Script Python

Para registrar tickets de soporte al vuelo desde cualquier equipo sin necesidad de levantar Docker o el frontend local:

### 1. Requisito en la PC:
```bash
pip install psycopg2-binary
```

### 2. Script Reutilizable en `2brain`:
El script está alojado en [`scripts/create-masterhub-tickets.py`](file:///C:/Users/vmontoyaMG/Desktop/2brain/scripts/create-masterhub-tickets.py).

### 3. Comando de Ejecución (PowerShell):
```powershell
cd C:\Users\vmontoyaMG\Desktop\2brain
$env:DATABASE_URL="postgres://avnadmin:...@pg-masterhub-masterhub.j.aivencloud.com:28688/helpdesk_db?sslmode=require"
python scripts/create-masterhub-tickets.py
```

**Beneficio**: El script se conecta directamente a la base de datos de producción/nube `helpdesk_db` en **Aiven Cloud**, calcula automáticamente el cuadrante de la **Matriz de Eisenhower** (`urgency`/`importance`), genera IDs únicos tipo CUID y confirma el resultado en la consola.
