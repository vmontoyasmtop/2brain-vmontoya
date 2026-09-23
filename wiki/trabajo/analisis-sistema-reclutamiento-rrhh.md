---
title: "Análisis Técnico: Documento Maestro de Reclutamiento y Selección RRHH"
type: "concept"
area: "trabajo"
created: 2026-09-22
updated: 2026-09-22
sources:
  - "raw/trabajo/Control_de_Reclutamiento.xlsx"
  - "raw/trabajo/reclutamiento_rrhh_mastergroup.csv"
tags:
  - rrhh
  - reclutamiento
  - data-mapping
  - masterhub
  - hr-ms
  - google-sheets
---

# 📊 Análisis Técnico: Documento Maestro de Reclutamiento y Selección RRHH

**Documento Fuente**: `Control de Reclutamiento` (Google Spreadsheet)  
**ID Hoja**: `1v6ev0D-3x3HTtSXWlmHDPyiG1-zB9DOTOaDd-XsJFwc`  
**Propietaria**: Franmarys González (`fgonzalez@mastergroupve.com`)  
**Compartido por**: Eva Colmenares (`ecolmenares@mastergroupve.com`)  
**Ubicación Local Raw**: [`raw/trabajo/Control_de_Reclutamiento.xlsx`](file:///C:/Users/vmontoyaMG/Desktop/2brain/raw/trabajo/Control_de_Reclutamiento.xlsx)  
**Carpeta de Extracción CSV**: [`raw/trabajo/recruitment_parsed/`](file:///C:/Users/vmontoyaMG/Desktop/2brain/raw/trabajo/recruitment_parsed)

---

## 🏛️ 1. Estructura General del Libro (5 Pestañas Clave)

El documento representa el histórico operacional completo de Reclutamiento y Selección de **Master Group**, compuesto por 5 libros de trabajo especializados:

| Pestaña | Filas con Datos | Propósito Operacional | Estado en MasterHub |
| :--- | :---: | :--- | :--- |
| **`Entrevistas`** | **1.996** | Base histórica masiva de postulantes para cargos operativos de tiendas y restaurantes. | Compatible con `Candidate` & `Interview` |
| **`Vacantes`** | **117** | Control correlativo (`VAC-001`) de vacantes abiertas, cubiertas y fuentes. | Compatible con `JobVacancy` (Task 2.1) |
| **`Llamados no asistieron`** | **33** | Registro de inasistencias a citaciones de entrevistas. | Estado `NO_SHOW` en `Interview` |
| **`Head Count`** | **28** | Matriz de dotación autorizada vs real por Sede (A / I / N). | Compatible con métricas de plantilla |
| **`Entrevistas Area Administrativa`** | **10** | Expedientes cualitativos de candidatos a Finanzas y Administración. | Compatible con `Candidate` + Notas de evaluación |

---

## 🔍 2. Desglose Detallado por Pestaña

### 2.1 Pestaña `Entrevistas` (1.996 Postulantes Operativos)
Es el núcleo del reclutamiento en sedes/tiendas.
* **Campos Registrados**:
  1. `#`: Correlativo numérico.
  2. `Nombre`: Nombre y apellido del postulante.
  3. `Cargo Postulado`: Ej: *Empaquetador, Cocinero / Sushero, Cajera, Ayudante Integral, Mesonero, Bartender*.
  4. `Domicilio`: Sector o zona de residencia.
  5. `CV (link)`: Nombre de archivo de CV (ej: `Curriculum Diana 2025.pdf`, `Dargelis Ramirez Cajera.png`).
  6. `Medio de Postulación`: Canal de captación (Instagram, Computrabajo, Bumeran, Referido).
  7. `Fecha de Entrevista`: Fecha serial Excel.
  8. `Entrevistado`: Reclutador asignado (ej: *Mesa, R*, *Villarroel, A*, *Sala, D*).
  9. `Devengado actual`: Salario en empleo previo.
  10. `Expectativa Salarial`: Rango aspirado.
  11. `Canditado`: Estado del postulante (*Elegible*, *Descartado*, *En Proceso*).
  12. `Sede`: Código de Unidad de Negocio (ej: `BU1BLT`, `BU2BLB`, `BU3BLN`, `BU4BAV`, `BU5BSB`, `BU6BSLC`, `BU13LG`, `BU17ANNER`).
  13. `Asistió`: Booleano (*Si* / *No*).
  14. `Feedback`: Observaciones técnicas del entrevistador.
  15. `Comentarios Adicionales`: Motivos de descarte o confirmaciones de ingreso.

---

### 2.2 Pestaña `Vacantes` (117 Requerimientos)
Permite auditar el cumplimiento de solicitudes de tienda.
* **Campos**: `ID Vacante` (`VAC-001`), `Cargo`, `Unidad de Negocio`, `Fecha Apertura`, `Mes`, `Año`, `Fecha Ingreso`, `Estatus` (*Cubierta*, *En Proceso*), `Fuente de Reclutamiento`.
* **Hallazgo Clave**: Los códigos de Sede (`BU1BLT` - Boleíta, `BU2BLB` - Baruta, `BU3BLN` - Los Naranjos, `BU4BAV` - Altamira Village, `BU5BSB` - San Bernardino, etc.) corresponden 1:1 con la tabla `sites` de MasterHub.

---

### 2.3 Pestaña `Head Count` (Matriz de Plantilla 2026)
Establece las reglas de negocio para determinar si una tienda puede o no abrir una vacante:
* **Métricas**:
  * **A (Aprobado)**: Plazas presupuestadas y autorizadas por la Dirección General.
  * **I (Instalado)**: Colaboradores actualmente activos y trabajando en la tienda.
  * **N (Necesidad)**: Brecha o déficit (`N = A - I`). Si `N > 0`, se justifica la vacante.
* **Cargos Monitoreados**: Gerente, Supervisor, Jefe de Cocina, Cocinero, Sushero, Ayudante de Cocina, Mantenimiento, Bartender, Anfitriona, Cajeras (Salón, Feria, Delivery), Empaquetador, Mesonero, Motorizado.

---

### 2.4 Pestaña `Entrevistas Area Administrativa` (Evaluaciones Cualitativas)
Contiene las entrevistas en profundidad para posiciones corporativas (Finanzas, CxP, CxC, Contabilidad):
* Contiene perfiles con transcripción detallada de trayectoria laboral previa (Banco de Venezuela, Profit Plus, Richi Tortas, condominios).
* Detalle de aspiraciones salariales en divisas ($300 a $600 USD) y expectativas de beneficios.
* Evaluación de competencias contables (conciliaciones bancarias, declaraciones SENIAT, parafiscales).

---

## 🗺️ 3. Matriz de Mapeo hacia MasterHub (`hr-ms` / `hr_db`)

| Campo Google Sheet | Modelo Prisma | Campo Prisma `hr_db` | Tipo / Regla |
| :--- | :--- | :--- | :--- |
| `Nombre` | `Candidate` | `firstName` / `lastName` | Split de la cadena de texto |
| `Cargo Postulado` | `Candidate` | `positionApplied` | String o FK a `JobPosition` |
| `Domicilio` | `Candidate` | `address` / `city` | Dirección de habitación |
| `CV (link)` | `Candidate` | `cvUrl` / `cvKey` | Nombre del PDF / carga a MinIO S3 |
| `Medio de Postulación` | `Candidate` | `source` | `WEB`, `PHONE`, `REFERRAL`, `WALK_IN` |
| `Canditado` (Estatus) | `Candidate` | `status` | `Elegible` ➔ `ELEGIBLE`, Descarte ➔ `DESCARTADO` |
| `Sede` (`BU1BLT`, etc.) | `Candidate` | `siteId` / `siteName` | Slug normalizado a la sede MasterHub |
| `Entrevistado` (Reclutador) | `Interview` | `interviewerName` | Nombre del reclutador responsable |
| `Fecha de Entrevista` | `Interview` | `scheduledAt` | Conversión de número serial Excel a ISO 8601 |
| `Asistió` | `Interview` | `status` | Si es 'No' ➔ `NO_SHOW`, Si es 'Si' ➔ `COMPLETED` |
| `Feedback` / `Comentarios` | `Interview` | `notes` / `feedback` | Observaciones técnicas registradas |
| `Expectativa Salarial` | `Candidate` | `salaryExpectation` | Monto o rango en USD |

---

## 🚀 4. Recomendaciones de Implementación para el Módulo RRHH

1. **Script de Ingesta Masiva / Seed Histórico**:
   - Crear un comando CLI en `apps/hr-ms/prisma/seed-candidates.ts` que lea `Entrevistas.csv` e inserte los 1.996 candidatos con sus respectivas entrevistas sin duplicar registros.
2. **Normalizador de Fechas Excel**:
   - Convertir los timestamps seriales de Excel (ej: `45994.0` ➔ `2025-12-03`) de manera automática durante la ingesta.
3. **Módulo de Head Count en Frontend**:
   - Incorporar en el Dashboard de RRHH la tabla interactiva de `Head Count` (A / I / N) para que los gerentes solo puedan solicitar vacantes cuando la sede tenga plazas vacantes (`N > 0`).
4. **Cierre de Tarea ClickUp**:
   - La tarea [TASK: Analizar documento / CSV de reclutamiento actual](https://app.clickup.com/t/86bc5jbfa) cuenta ahora con la auditoría y análisis completados.
