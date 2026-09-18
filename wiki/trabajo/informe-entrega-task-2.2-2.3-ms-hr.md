---
title: "Informe Técnico: Desarrollo y Entrega de Tasks 2.2 y 2.3 (MS-HR)"
type: "report"
area: "trabajo"
project: "MasterHub"
module: "MS-HR"
created: 2026-09-18
author: "ALFRED (Mayordomo & Copiloto Ejecutivo)"
status: "completed"
tags:
  - ms-hr
  - rrhh
  - masterhub
  - onboarding
  - candidatos
  - empleados
---

# 📋 Informe Técnico: Entrega de Tasks 2.2 y 2.3 (Módulo MS-HR)

**Proyecto**: MasterHub — Microservicio de Recursos Humanos (`hr-ms`)  
**Autor**: ALFRED (Copiloto Ejecutivo) & Subagentes de Desarrollo (Backend & Frontend)  
**Fecha de Entrega**: 18 de Septiembre de 2026  
**Ubicación del Documento**: `wiki/trabajo/informe-entrega-task-2.2-2.3-ms-hr.md`

---

## 🎯 1. Resumen Ejecutivo

El presente informe documenta la culminación y verificación técnica de las tareas **TASK 2.2** y **TASK 2.3** correspondientes a la **Fase 2 (Reclutamiento, Selección y Onboarding)** del Módulo de Recursos Humanos (`MS-HR`) en la plataforma **MasterHub**.

- **TASK 2.2 (Registro de Candidatos, Carga de CVs en MinIO/S3 y Control de Entrevistas)**: Permite la captura de expedientes de postulantes, correlativo automático de carnet (`candidatoNum`), almacenamiento de archivos PDF en MinIO (S3) e historial completo de entrevistas y cambios de estado.
- **TASK 2.3 (Puente de Onboarding: Candidato ➔ Empleado)**: Permite convertir con un solo clic a un candidato elegible en un trabajador activo en la base de datos central de RRHH (`Employee`), clonando sus datos, asignando la Sede/Departamento/Cargo y estableciendo una regla de negocio automática de **30 días en período de prueba**.

---

## 🏗️ 2. Arquitectura Técnica Implementada

### 🛠️ 2.1 Backend (`hr-ms` & `api-gateway`)

#### 1. Esquema Prisma ORM (`prisma/schema.prisma`)
- **Modelo `Candidate`**: Incorpora `candidatoNum` (autoincremental), borrado lógico (`deletedAt`), `status` (`ENTREVISTADO`, `EN_PROCESO`, `PRUEBA_TECNICA`, `ELEGIBLE`, `CONTRATADO`, `DESCARTADO`), `stage` (`CONTACTO_INICIAL`, `ENTREVISTA`, `PRESELECCION`, `OFERTA`, `CONTRATACION`), `cvUrl`, `cvKey`, `hiredAt` y vinculación opcional `employeeId`.
- **Modelo `Interview`**: Soporta agendamiento de citas, entrevistadores, notas de evaluación y estados (`SCHEDULED`, `COMPLETED`, `CANCELLED`, `PASSED`, `FAILED`).
- **Modelo `Employee`**: Recibe la conversión del candidato con estatus `ACTIVE` y metadatos de auditoría de prueba:
  ```json
  {
    "isProbation": true,
    "probationEndDate": "2026-10-18T11:16:00.000Z",
    "hiredFromCandidateId": "candidato-id-cuid"
  }
  ```

#### 2. Servicios & DTOs
- `HireCandidateDto` (`hr-ms/src/candidates/dto/hire-candidate.dto.ts` y `api-gateway/src/hr/dto/hire-candidate.dto.ts`):
  - `siteId?: string`: ID de la Unidad de Negocio / Sede.
  - `departmentId?: string`: ID del Departamento asignado.
  - `jobTitle?: string`: Cargo oficial de contratación.
  - `hireDate?: string`: Fecha efectiva de ingreso.
  - `notes?: string`: Observaciones de la contratación.
  - `performedBy?: string`: Usuario reclutador que ejecuta la acción.

- `CandidatesService.hire(id, dto)` (`hr-ms/src/candidates/candidates.service.ts`):
  1. Busca al candidato por ID o `candidatoNum`.
  2. Verifica si ya posee `employeeId` vinculado (retorna registro existente si aplica).
  3. Comprueba si existe un `Employee` previo por Cédula (`ci`) o Correo (`email`).
  4. Si no existe, crea el registro `Employee` con datos de contacto, cargo y 30 días de prueba en `metadata`.
  5. Actualiza `Candidate` a estatus `CONTRATADO`, etapa `CONTRATACION`, fija `hiredAt = new Date()` y enlaza `candidate.employeeId`.
  6. Registra un evento en `CandidateHistory` con tipo `'HIRED'`.

#### 3. Endpoints REST Expuestos (`api-gateway`)
| Método | Endpoint REST | Patrón de Mensaje TCP | Descripción |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/v1/hr/candidates` | `hr.candidate.list` | Listado de candidatos con filtros multifactor |
| `POST` | `/api/v1/hr/candidates` | `hr.candidate.create` | Alta de nuevo candidato postulado |
| `POST` | `/api/v1/hr/candidates/:id/cv` | `hr.candidate.uploadCv` | Subida de CV en formato PDF a MinIO S3 |
| `POST` | `/api/v1/hr/candidates/:id/hire` | `hr.candidate.hire` | **Contratación directa y generación de Ficha de Empleado** |
| `POST` | `/api/v1/hr/candidates/:id/interviews` | `hr.interview.create` | Agendamiento de entrevistas |

---

### 🎨 2.2 Frontend UI (`frontend-ui-dashboard`)

1. **Cliente API ([`candidates-api.ts`](file:///C:/Users/Animación%20MKT/Desktop/MasterHub/frontend-ui-dashboard/src/lib/candidates-api.ts))**:
   - Expone la función `hireCandidate(id: string, dto?: HireCandidateDto)` conectada al endpoint REST.
2. **Modal de Contratación ([`HireCandidateModal.tsx`](file:///C:/Users/Animación%20MKT/Desktop/MasterHub/frontend-ui-dashboard/src/components/dashboard/hr/candidates/HireCandidateModal.tsx))**:
   - Formulario modal interactivo con selección dinámica de Sede (BU) y Departamento, confirmación de Cargo y Fecha de Ingreso.
   - Manejo de estados de carga (spinner), validaciones y alertas con SweetAlert2.
3. **Integración en Tablas y Vistas ([`candidate-dashboard.tsx`](file:///C:/Users/Animación%20MKT/Desktop/MasterHub/frontend-ui-dashboard/src/components/dashboard/hr/candidates/candidate-dashboard.tsx))**:
   - Botón interactivo **`🟢 Contratar`** en cada fila de postulantes elegibles.
   - Botón **`🟢 Contratar Candidato`** en la cabecera del modal de detalle de candidatos.

---

## 🧪 3. Guía de Pruebas y QA Checklist

Para ejecutar el control de calidad (QA) de las versiones **2.2** y **2.3**, siga estos pasos en la interfaz de MasterHub:

- [ ] **QA 1 (Carga de Candidatos & CVs - Task 2.2)**:
  1. Ingrese al Dashboard de RRHH ➔ Sección **Candidatos & Selección** (`/dashboard/hr/candidates`).
  2. Haga clic en `+ Registrar Candidato` e ingrese datos de prueba (Cédula, Nombres, Cargo, Sede).
  3. Adjunte un archivo PDF de currículum en el Dropzone y confirme la subida a MinIO.
  4. Verifique que se genere el número de candidato correlativo (ej: `CAN-00012`).

- [ ] **QA 2 (Agendamiento de Entrevistas - Task 2.2)**:
  1. Abra el detalle del candidato registrado.
  2. En la pestaña *Entrevistas*, haga clic en `+ Agendar Entrevista`.
  3. Programe la fecha/hora y compruebe que el historial muestre la entrevista en estado `SCHEDULED`.

- [ ] **QA 3 (Conversión Candidato ➔ Empleado - Task 2.3)**:
  1. En la lista de candidatos, ubique un postulante en estado `ELEGIBLE` o `PRUEBA_TECNICA`.
  2. Haga clic en el botón verde **`🟢 Contratar`**.
  3. En el modal `HireCandidateModal`, confirme la Sede, el Departamento, el Cargo y la Fecha de Ingreso.
  4. Presione **"Confirmar Contratación"**.
  5. Verifique la aparición del Toast SweetAlert2 confirmando la creación de la Ficha de Empleado con **30 días en período de prueba**.
  6. Diríjase al módulo de **Directorio de Trabajadores** (`/dashboard/hr/employees`) y compruebe que el nuevo colaborador aparezca registrado en estado **ACTIVO**.

---

## 📂 4. Ubicación de Archivos en el Sistema

- **Documento de Informe**: [`wiki/trabajo/informe-entrega-task-2.2-2.3-ms-hr.md`](file:///C:/Users/Animación%20MKT/Desktop/2brain-vmontoya/wiki/trabajo/informe-entrega-task-2.2-2.3-ms-hr.md)
- **Monorrepositorio MasterHub**: [`C:\Users\Animación MKT\Desktop\MasterHub`](file:///C:/Users/Animación%20MKT/Desktop/MasterHub)
- **Microservicio Backend `hr-ms`**: [`C:\Users\Animación MKT\Desktop\MasterHub\hr-ms`](file:///C:/Users/Animación%20MKT/Desktop/MasterHub/hr-ms)
- **API Gateway**: [`C:\Users\Animación MKT\Desktop\MasterHub\api-gateway`](file:///C:/Users/Animación%20MKT/Desktop/MasterHub/api-gateway)
- **Frontend App Router**: [`C:\Users\Animación MKT\Desktop\MasterHub\frontend-ui-dashboard`](file:///C:/Users/Animación%20MKT/Desktop/MasterHub/frontend-ui-dashboard)

---
*Informe generado automáticamente por ALFRED el 18/09/2026.*
