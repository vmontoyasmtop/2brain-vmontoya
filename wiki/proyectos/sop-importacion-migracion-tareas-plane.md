---
title: "SOP: Protocolo y Script de Importación Masiva de Proyectos y Tareas en Plane"
type: "sop"
area: "proyectos"
created: 2026-09-28
updated: 2026-09-28
tags:
  - plane
  - sop
  - api
  - migracion
  - automatizacion
---

# 📋 SOP: Protocolo y Script de Importación Masiva de Proyectos y Tareas en Plane

*Guía técnica y estándar operativo inalterable para la importación y sincronización masiva de proyectos, épicas, tareas, subtareas y etiquetas hacia la instancia institucional de **Plane** (`https://projects.mastergroupve.com`).*

---

## 🎯 1. Objetivo y Alcance

Estandarizar el procedimiento para migrar e importar lotes de tareas desde fuentes externas (ClickUp, CSVs de exportación, hojas de cálculo o exports de Plane Web) hacia espacios de trabajo en Plane, garantizando:
1. Creación automática de proyectos y validación de nombres según restricciones del motor.
2. Inserción jerárquica (épicas/padres y subtareas vinculadas).
3. Mapeo estricto de estados del flujo de trabajo (`Backlog`, `Todo`, `In Progress`, `Done`, `Cancelled`).
4. Sincronización y alta de etiquetas temáticas y de marcas con paleta de colores.
5. Preservación de enlaces externos (Google Docs, Sheets, enlaces de redes sociales) y fechas límite (`start_date`, `target_date`).
6. Manejo resiliente de cuotas y *rate limiting* de la API de Plane.

---

## 🛠️ 2. Entorno y Especificaciones Técnicas

- **Instancia Central**: `https://projects.mastergroupve.com`
- **Autenticación**: Vía cabecera `x-api-key: plane_api_...`
- **Workspaces Activos**:
  - `it---mg` (ID: `388c5fcf-86fd-4d07-8656-22c23413fe10`): Proyectos IT y MasterHub.
  - `marketing` (ID: `87bc0a43-d43d-47cb-b7ed-20895a642fd7`): Marketing, Eventos, Creadores, Argus, Pantalla Móvil.
- **Script Maestro Oficial**:
  `C:\Users\vmontoyaMG\Desktop\2brain\scripts\import_marketing_to_plane.js`

---

## ⚠️ 3. Reglas Críticas y Particularidades de la API de Plane

Durante el desarrollo e implantación se identificaron las siguientes reglas que **deben respetarse rigurosamente**:

### A. Restricción en Nombres de Proyectos (Caracteres Especiales)
* **Error**: `400 Bad Request` con mensaje `{"non_field_errors": ["Project name cannot contain special characters."]}`.
* **Causa**: Plane no permite paréntesis `()`, corchetes, comas ni símbolos en el nombre del proyecto.
* **Regla**: Sanear siempre los nombres antes del envío (ej: cambiar `Creadores (In House)` a `Creadores In House`).

### B. Manejo de Rate Limiting (Códigos 429 y Error 5900)
* Plane aplica limitación de peticiones por minuto. Retorna dos variantes de bloqueo:
  1. **HTTP 429 Too Many Requests**: Contiene la cabecera `retry-after` en segundos.
  2. **HTTP 200/400 con Payload JSON**: `{"error_code": 5900, "error_message": "RATE_LIMIT_EXCEEDED"}`.
* **Regla**: El script de ingesta implementa reintentos exponenciales con espera dinámica (`waitSec + 1`) y una pausa preventiva de `150ms` entre inserciones de ítems.

### C. Mapeo de Subtareas (Jerarquía de Dos Pasadas)
* Las incidencias hijas requieren el UUID real de la incidencia padre (`parent: <plane_issue_uuid>`).
* **Regla**: El procesador debe dividir las filas en:
  1. **Fase 1 (Principales)**: Tareas sin campo `Parent`. Se insertan y se almacena su correlación en memoria (`csvIdentifier` ➔ `planeId`).
  2. **Fase 2 (Subtareas)**: Tareas con `Parent`. Se resuelven consultando el mapa generado en la Fase 1.

### D. Formato de Contenido Enriquecido
* La API de Plane requiere `description_html`. El texto plano o Markdown debe envolverse en etiquetas `<p>...</p>` y preservar saltos de línea `<br/>` para evitar pérdida de legibilidad.

---

## 🚀 4. Guía de Ejecución del Script Oficial

El script está parametrizado para ejecutarse tanto en modo simulación como en producción real.

### Paso 1: Modo Simulación (Dry-Run Preventivo)
Verifica la lectura del CSV, valida proyectos, mapea estados y muestra qué crearía sin escribir en base de datos:
```powershell
node C:\Users\vmontoyaMG\Desktop\2brain\scripts\import_marketing_to_plane.js --dry-run
```

### Paso 2: Ejecución Real en Producción
Procesa todas las tareas del archivo CSV configurado e inserta en Plane:
```powershell
node C:\Users\vmontoyaMG\Desktop\2brain\scripts\import_marketing_to_plane.js
```

### Paso 3: Especificar un Archivo CSV Distinto
```powershell
node C:\Users\vmontoyaMG\Desktop\2brain\scripts\import_marketing_to_plane.js "C:\ruta\al\archivo.csv"
```

---

## 📊 5. Historial de Migraciones Ejecutadas Exitosamente

| Fecha | Origen / Archivo | Espacio Destino | Tareas | Resultado |
| :--- | :--- | :--- | :---: | :--- |
| **2026-09-23** | ClickUp (Lista 1er Fase MasterHub) | `it---mg` / MasterHub | **97** | 100% migradas por API con módulos (`Finance`, `HR`, `Helpdesk`, etc.). |
| **2026-09-28** | Export Plane Web (`3d0b87dd.csv`) | `marketing` (5 Proyectos) | **70** | 100% migradas en Marketing (57), Eventos (5), ARGUS (4), Creadores (3) y Pantalla Móvil (1). Limpieza de demos completada. |

---

## 🔗 Enlaces Relacionados
- [[plane-gestion-proyectos|Proyecto: Plane - Plataforma de Gestión de Proyectos]]
- [[masterhub-mg-hub|Proyecto: MasterHub (MG-HUB)]]
- [[pilar-proyectos|Pilar Proyectos]]
- [[pilar-trabajo-xetux|Pilar Trabajo]]
