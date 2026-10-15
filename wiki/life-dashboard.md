# 📊 Life & Executive Dashboard — Master Group

Tablero de control ejecutivo para **Victor Montoya** en **Master Group**, concentrando el seguimiento de hitos de desarrollo, Sprints activos y visión estratégica.

---

## 🎯 Objetivos Principales del Trimestre (OKRs Master Group)

| ID | Objetivo Estratégico | Pilar / Proyecto | Métrica / Resultado Clave | Estado |
|----|----------------------|------------------|--------------------------|--------|
| **O1** | Ejecutar Sprint 1 Fast-Track de Finanzas | 🚀 MS-FINANZAS | MVP CxP & Motor Fiscal SENIAT listos (27/09) | 🟡 En progreso |
| **O2** | Desplegar Fase 1 del Expediente de RRHH | 🚀 MS-HR | Ficha Médica, Tallas y Expedientes en producción | 🟡 En progreso |
| **O3** | Mantenimiento y Operación Xetux | 🏢 Trabajo | Actualización diaria de tasa Bs en Xetux | 🟢 Al día |
| **O4** | Consolidar Arquitectura MasterHub | 🚀 Proyectos | API Gateway, PostgreSQL (`finance_db`, `hr_db`) | 🟡 En progreso |
| **O5** | Cockpit Analítico Xetux en Vivo | 🚀 [[mg-sales-analytics\|MG-SALES-ANALYTICS]] | Búsqueda multicriterio en 14 sedes y KPIs en vivo | 🟢 Activo (v1.0) |

---

## ⚡ Estado de Proyectos y Enfoque Activo (Semana 12/10 – 18/10/2026)

1. 📊 **[[mg-sales-analytics|MG-SALES-ANALYTICS]] (Lanzamiento v1.0)**:
   - Dashboard analítico desacoplado en Next.js 15 + Tailwind CSS v4 con diseño idéntico a MGH.
   - Extracción en vivo de las 14 sedes de Xetux ERP (`ExtractionData/SalesFull`), búsqueda por producto/sede/fechas, KPIs automáticos y exportación CSV.
   - Activo en puerto local `http://localhost:3050`.

2. 🥢 **[[beijing_kiosk|Beijing Restaurant Menú Kiosco (Flutter)]]**:
   - Inspeccionado y certificado por Kakashi Sensei (100% limpio en `flutter analyze`, 6/6 tests aprobados).
   - `DesignCanvas` calibrado para pantalla 4K vertical Apolosign SW3299T (32").
   - Estado: En reposo a la espera del nuevo mockup visual para refinar componentes de interfaz.

3. 🛒 **[[meniox|Proyecto: Meniox (POS & Franquicias)]]**:
   - Auditoría forense completa realizada. Rescatada la memoria de los 6 microservicios y base de datos Aiven Cloud (14 sedes Beijing, 2,126 materias primas).
   - Solucionado error TypeScript en `sales-reconciliation.service.ts` (4/4 tests verdes).
   - Deuda pendiente: Alinear fixtures en `inventory.integration.spec.ts`.

4. 💼 **[[masterhub-mg-hub|MasterHub (MG-HUB)]]**:
   - Corregido flujo de facturas CxP: importación de facturas de proveedores por defecto en USD ($).
   - Cambios commiteados y pusheados a la rama `dev` (`1ded2be` y `fbe0a8b`).

---

## 📌 Enlaces Útiles
- 🗺️ [[pilar-proyectos|Ecosistema de Proyectos MasterHub]]
- 📊 [[mg-sales-analytics|Proyecto: MG-SALES-ANALYTICS]]
- 🥢 [[beijing_kiosk|Proyecto: Beijing Kiosk]]
- 🛒 [[meniox|Proyecto: Meniox]]
- 💼 [[masterhub-modulo-finanzas|Plan Fast-Track MS-FINANZAS]]
- 📝 [[log|Log de Bitácora Operativa]]
