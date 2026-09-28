---
title: "SOP: Sincronización y Backup de Base de Datos de Producción a PostgreSQL Local (MasterHub)"
type: "sop"
area: "trabajo"
created: 2026-09-24
updated: 2026-09-24
tags:
  - database
  - postgresql
  - masterhub
  - backup
  - galadriel
  - samwise
---

# 🛡️ SOP: Protocolo Oficial de Respaldo y Sincronización de Base de Datos (Producción ➔ Local)

*Guía estándar y procedimiento automatizado para extraer un volcado atómico de las bases de datos de producción en el servidor Linode y restaurarlas en el PostgreSQL local de desarrollo en Docker.*

---

## 🔍 1. Información General y Alcance

- **Propósito**: Permitir que el equipo y los desarrolladores trabajen localmente con un espejo 100% idéntico y actualizado de la producción real de MasterHub, sin latencia, sin costos de nube y sin riesgo de alterar datos productivos.
- **Servidor Origen**: Servidor Linode VPS `172.238.221.116` (Contenedor `masterhub-postgres-local-1`).
- **Destino Local**: Contenedor Docker `masterhub-postgres-local-1` (Puerto 5433 en host Windows, 5432 en red interna Docker).
- **Subagentes Responsables**:
  - 🔮 **Galadriel de Lorien**: Custodia de integridad de datos, esquemas relacionales y cumplimiento DLP.
  - 🛡️ **Samwise Gamyi**: Operaciones de extracción `pg_dump`, verificación y restauración.

---

## 🗄️ 2. Bases de Datos Sincronizadas

| Base de Datos | Microservicio Asociado | Contenido Clave |
| :--- | :--- | :--- |
| **`auth_db`** | `auth-ms` (3004) | Usuarios, credenciales hash, roles y permisos de acceso. |
| **`hr_db`** | `hr-ms` (3007) | 1,320+ Empleados, 5,500+ registros históricos, 255 HeadCount, Vacantes. |
| **`helpdesk_db`** | `helpdesk-sm` (3005) | 260+ Tickets de soporte, 100+ comentarios, adjuntos y estados. |
| **`inventory_db`** | `inventory-sm` (3002) | Catálogo de activos/productos, asignaciones y logs de auditoría. |
| **`wiki_db`** | `wiki-sm` (3006) | Artículos corporativos, documentación interna y archivos adjuntos. |

---

## ⚡ 3. Ejecución Automatizada

### Opción A. Con una sola instrucción al Agente (Grandalf / ALFRED):
El desarrollador solo necesita indicar en lenguaje natural:
> *"ALFRED / Grandalf, haz backup de producción de la db"*  
> *"Sincroniza la base de datos de producción a local"*

El agente ejecutará de inmediato el script oficial sin fricción ni preguntas intermedias.

### Opción B. Desde Terminal en el repositorio `MG-HUB`:
```powershell
cd C:\Users\vmontoyaMG\Desktop\MG-HUB
npm run db:sync-prod
```

### Opción C. Desde Terminal en `2brain-MG`:
```powershell
powershell -ExecutionPolicy Bypass -File C:\Users\vmontoyaMG\Desktop\2brain-MG\scripts\sync_mgh_prod_db.ps1
```

---

## 📂 4. Almacenamiento de Resguardos SQL

Cada ejecución genera automáticamente volcados SQL con marca temporal en:
`C:\Users\vmontoyaMG\Desktop\MG-HUB\backups\production_server\`

Estructura de archivos:
- `<database>_prod_YYYY-MM-DDTHH-mm-ss.sql`

---

## 🔌 5. Conexión de Microservicios en `.env`

Para que los microservicios locales se comuniquen con este PostgreSQL local, el archivo `.env` en `MG-HUB` debe contener:

```dotenv
DATABASE_URL_AUTH=postgresql://masterhub:masterhub-local@postgres-local:5432/auth_db
DATABASE_URL_HELPDESK=postgresql://masterhub:masterhub-local@postgres-local:5432/helpdesk_db
DATABASE_URL_HR=postgresql://masterhub:masterhub-local@postgres-local:5432/hr_db
DATABASE_URL_INVENTORY=postgresql://masterhub:masterhub-local@postgres-local:5432/inventory_db
DATABASE_URL_WIKI=postgresql://masterhub:masterhub-local@postgres-local:5432/wiki_db
```

*(En caso de requerir volver a la nube Aiven, restaurar las variables guardadas en `.env.aiven`).*
