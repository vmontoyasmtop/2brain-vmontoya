# 🏪 MasterHub HR — Portal Exclusivo de Reclutamiento para Gerente de Tienda

## 📌 Resumen de Gestión (Aragorn PM & Alfred)
* **Proyecto**: MasterHub (`b60ea600-1f86-4177-87df-6b6ed0063874`)
* **Módulo**: `HR-MS` (`0d84505e-5a91-452d-be32-50072240e888`)
* **Gestor Oficial**: [Plane — projects.mastergroupve.com](https://projects.mastergroupve.com/it---mg/projects/b60ea600-1f86-4177-87df-6b6ed0063874)
* **Fecha Objetivo de Ejecución**: **Lunes, 05 de Octubre de 2026**
* **Responsable Técnico**: Ing. Víctor Montoya
* **Inspiración y Requerimientos**:
  * Pizarra Operativa (`raw/proyectos/hr-ms/reclu.jpeg`)
  * Flujo Oficial RYS (`raw/proyectos/hr-ms/Proceso RYS.pptx (2) (1).pdf`)

---

## 🎯 Decisión Arquitectónica: Página Dedicada vs. Vista Compartida

En lugar de sobrecargar la vista global de analistas de RRHH con condicionales de renderizado, se establece una **página dedicada e independiente**:
* **Ruta**: `/dashboard/store-recruitment` (o `/dashboard/tienda/reclutamiento`).
* **Audiencia Exclusiva**: Roles `STORE_MANAGER`, `ADMIN`, `SUPER_ADMIN`.
* **Ventajas**:
  1. **Aislamiento Total**: El Gerente de Tienda no tiene acceso ni distracción con nóminas, contratos generales, tabuladores o expedientes de otras sucursales.
  2. **Experiencia UI Fiel a la Pizarra**: Interfaz dividida en 2 paneles (Master-Detail) con botones rápidos binarios.
  3. **Seguridad y Rendimiento**: Consultas acotadas por defecto a la sucursal del gerente (`siteId` / `buId`).

---

## 📋 Estructura de Tareas en Plane (`project.masterhubve.com`)

### 🏆 Tarea Contenedora Principal
* **ID**: [`MASTERHUB-131`](https://projects.mastergroupve.com/it---mg/projects/b60ea600-1f86-4177-87df-6b6ed0063874/issues/acde77c6-dede-4d01-a291-bfeff7580bba)
* **Título**: `[HR-MS] Vista Dedicada para Gerente de Tienda: Selección y Control de Vacantes (Store Portal)`
* **Prioridad**: Urgente (`urgent`) | **Fecha**: `2026-10-05`
* **Etiquetas**: `rrhh`, `frontend`, `backend`
* **Módulo**: `HR-MS`

---

### 🔹 Subtarea 1: Enrutamiento y Guard RBAC
* **ID**: [`MASTERHUB-132`](https://projects.mastergroupve.com/it---mg/projects/b60ea600-1f86-4177-87df-6b6ed0063874/issues/2a8bd766-eaa4-447e-bbdb-fd4587850eb8)
* **Título**: `[HR-MS / Subtarea 1] Enrutamiento y Control de Acceso RBAC para Gerente de Tienda`
* **Objetivo**: Crear la ruta física `/dashboard/store-recruitment` protegida por `useAuth` y `hasRole(['STORE_MANAGER', 'ADMIN', 'SUPER_ADMIN'])`.
* **Criterios de Aceptación (Gherkin)**:
  * **Dado** un usuario con rol `STORE_MANAGER`,
  * **Cuando** accede a `/dashboard/store-recruitment`,
  * **Entonces** visualiza únicamente la consola de su sucursal, bloqueando cualquier intento de visualización de candidatos de otras tiendas.
  * **Dado** un usuario con rol no autorizado (ej. `USER`, `FINANCE_ASSISTANT`),
  * **Cuando** intenta acceder a la ruta,
  * **Entonces** es redirigido al dashboard principal o pantalla de error 403.

---

### 🔹 Subtarea 2: Interfaz Master-Detail (Vacantes vs Candidatos)
* **ID**: [`MASTERHUB-133`](https://projects.mastergroupve.com/it---mg/projects/b60ea600-1f86-4177-87df-6b6ed0063874/issues/bdfa2a23-27ed-49f5-bf84-a4305b3b94d1)
* **Título**: `[HR-MS / Subtarea 2] Interfaz Master-Detail: Vacantes de Sede vs Candidatos Asignados`
* **Objetivo**: Construir el layout de 2 columnas según la pizarra (`reclu.jpeg`).
* **Componentes**:
  * **Columna Izquierda (Vacantes)**: Requisiciones de la tienda (`JobRequisition` / `VacancyRequest`).
    * Botón `+ Solicitar Vacante` (Modal rápido `REEMPLAZO` / `CRECIMIENTO` con cargos oficiales).
    * Badge de cantidad de candidatos en espera de prueba.
  * **Columna Derecha (Candidatos RRHH)**: Lista de postulantes preseleccionados para la vacante activa.
    * Nombre, Cédula, Teléfono y enlace al CV en PDF.
* **Criterios de Aceptación (Gherkin)**:
  * **Dado** que el gerente selecciona una vacante en la columna izquierda,
  * **Cuando** hace clic sobre ella,
  * **Entonces** la columna derecha carga reactivamente solo los candidatos vinculados por RRHH a esa requisición.

---

### 🔹 Subtarea 3: Acciones Rápidas (Asistencia & Decisión de Selección)
* **ID**: [`MASTERHUB-134`](https://projects.mastergroupve.com/it---mg/projects/b60ea600-1f86-4177-87df-6b6ed0063874/issues/d95eb45d-8bc4-4042-889a-850f5f0cb4a6)
* **Título**: `[HR-MS / Subtarea 3] Botonera de Acción Rápida: Control de Asistencia y Decisión (Día de Prueba)`
* **Objetivo**: Proveer la botonera operativa de dos pasos:
  1. **Control de Asistencia**: `[✓ Asistió]` / `[✗ No Asistió]`.
  2. **Decisión**: `[✓ Contratar]` / `[✗ Descartar]`.
* **Criterios de Aceptación (Gherkin)**:
  * **Dado** un candidato asignado al día de prueba,
  * **Cuando** el gerente marca `[✗ No Asistió]`,
  * **Entonces** se actualiza el registro en `hr_db` y RRHH recibe notificación para reprogramar o archivar.
  * **Cuando** el gerente marca `[✓ Contratar]`,
  * **Entonces** el estado avanza a `ELEGIBLE_CONTRATACION` y se habilita la sección inferior de recaudos.
  * **Cuando** marca `[✗ Descartar]`, se abre un modal de 1 campo para registrar el motivo (ej. falta de destreza técnica, actitud) enviando feedback directo a RRHH.

---

### 🔹 Subtarea 4: Carga Digital de Recaudos (Carga DOC ➔ Drive Sync)
* **ID**: [`MASTERHUB-135`](https://projects.mastergroupve.com/it---mg/projects/b60ea600-1f86-4177-87df-6b6ed0063874/issues/f4e26e4f-c81c-44d0-8362-140e78a2149e)
* **Título**: `[HR-MS / Subtarea 4] Carga Digital de Recaudos (Carga DOC) y Sincronización de Expediente`
* **Objetivo**: Integrar la zona de carga de recaudos (Cédula, RIF, Cuenta Bancaria, CV) que sube los archivos a Google Drive / B2K+ Storage y vincula las URLs al expediente del empleado.
* **Criterios de Aceptación (Gherkin)**:
  * **Dado** un candidato en estado de contratación,
  * **Cuando** el gerente o RRHH suben los soportes digitales desde la consola,
  * **Entonces** los archivos se organizan automáticamente en la carpeta de Drive de la tienda (`/RRHH/Expedientes/{CI}_{Nombre}`) y quedan disponibles para la firma de formatos (Rutograma, Confidencialidad) y alta en nómina.

---

## 🗺️ Diagrama del Flujo en la Nueva Página

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  /dashboard/store-recruitment  [🏪 Sucursal: B2K+ / Operaciones]             │
├──────────────────────────┬───────────────────────────────────────────────────┤
│ 📋 VACANTES DE LA SEDE   │ 👤 CANDIDATOS ASIGNADOS POR RRHH                  │
│                          │                                                   │
│ • Cajera (1 pendiente)  │ Postulante: María Delgado  [📄 Ver CV]            │
│   [Activa - 2 cand.]     │ ────────────────────────────────────────────────  │
│                          │ 1. Asistencia a Día de Prueba:                    │
│ • Pasillero (2 vacantes) │    [ ✓ Asistió ]         [ ✗ No Asistió ]         │
│   [Sin candidatos aún]   │                                                   │
│                          │ 2. Decisión del Gerente:                          │
│ ──────────────────────── │    [ ✓ CONTRATAR ]       [ ✗ DESCARTAR ]          │
│ [+ Solicitar Vacante]    ├───────────────────────────────────────────────────┤
│                          │ 📂 CARGA DOC (Recaudos Digitales ➔ Google Drive)  │
│                          │ [ Cédula ] [ RIF ] [ Cuenta Bancaria ] [ Examen ] │
└──────────────────────────┴───────────────────────────────────────────────────┘
```

---

## 🚀 Tareas Complementarias de Fase 2 (Derivadas del Análisis PDF RYS vs. MGH)

Para completar al 100% el circuito operacional entre Reclutamiento, Tienda e Ingreso formal, se han generado en Plane las siguientes tareas hijas de la Épica [`MASTERHUB-22`](https://projects.mastergroupve.com/it---mg/projects/b60ea600-1f86-4177-87df-6b6ed0063874/issues/82071e7f-3ed4-471d-8b36-d8254677df62):

1. **[`MASTERHUB-136`](https://projects.mastergroupve.com/it---mg/projects/b60ea600-1f86-4177-87df-6b6ed0063874/issues/617cadb8-97dc-4cda-a0ba-fd97ab5c762d)**: Generador Automático de Formatos de Ingreso en PDF
   * **Objetivo**: Emisión automatizada en PDF de los 4 formatos obligatorios: Compromiso de Confidencialidad, Manejo de Efectivo (Cajeras), Rutograma de Trayecto y Notificación de Riesgo Laboral (LOPCYMAT).
2. **[`MASTERHUB-137`](https://projects.mastergroupve.com/it---mg/projects/b60ea600-1f86-4177-87df-6b6ed0063874/issues/20eae1a0-1f2f-48b1-9fbb-ba8f2a5772fb)**: Gestión y Tracking de Exámenes Médicos Pre-Empleo & Checklist de Aptitud
   * **Objetivo**: Digitalizar el agendamiento y carga de resultados (Apto / No Apto), sincronizándolo con la Ficha Médica de `Employee` en Fase 1.
3. **[`MASTERHUB-138`](https://projects.mastergroupve.com/it---mg/projects/b60ea600-1f86-4177-87df-6b6ed0063874/issues/26f6855a-56cf-4781-84f8-0f45d078978c)**: Bandeja Central de RRHH: Asignación y Notificación de Candidatos a Vacantes de Tienda
   * **Objetivo**: Proveer al equipo de RRHH la acción de asignar candidatos preseleccionados a la vacante de una tienda para que aparezcan de inmediato en la consola del Gerente de Tienda con alerta por correo/sistema.
4. **[`MASTERHUB-139`](https://projects.mastergroupve.com/it---mg/projects/b60ea600-1f86-4177-87df-6b6ed0063874/issues/d0145fee-4e1c-4328-b3ee-6ec18823378e)**: Control de Plantilla Orgánica y Cupos de Vacantes por Sede (Headcount Budget)
   * **Objetivo**: Validar requisiciones contra el presupuesto de puestos autorizado por tienda para evitar sobrecontrataciones no aprobadas.
5. **[`MASTERHUB-140`](https://projects.mastergroupve.com/it---mg/projects/b60ea600-1f86-4177-87df-6b6ed0063874/issues/a983817b-6479-45a8-8999-fca65a2000c2)**: Módulo de Jornadas de Reclutamiento y Entrevistas Masivas (Jornadas RRHH)
   * **Objetivo**: Permitir al equipo de RRHH convocar, registrar en modo Fast-Track in situ y calificar masivamente a los postulantes durante las jornadas presenciales de reclutamiento, alimentando el banco de elegibles para las tiendas.

