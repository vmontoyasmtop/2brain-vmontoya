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
| **O5** | Cockpit Analítico Xetux en Vivo | 🚀 [[mg-sales-analytics|MG-SALES-ANALYTICS]] | Búsqueda multicriterio en 14 sedes y KPIs en vivo | 🟢 Activo (v1.0) |
| **O6** | MVP EL CUADRE POS (Kiosko & Balanza Criolla) | 🚀 [[el-cuadre-pos-brand-brief-ejecutivo|EL CUADRE POS]] | Terminal Táctil, Balanza Criolla y Arqueo Ciego | 🟢 En Testing (6 US) |

---

## ⚡ Estado de Proyectos y Enfoque Activo (Semana 19/10 – 25/10/2026)

1. ⚖️ **[[el-cuadre-pos-brand-brief-ejecutivo|EL CUADRE POS — Kiosko, Frutería & Abasto Criollo]]**:
   - **Backend**: NestJS + SQLite WAL Mode con Prisma ORM (`elcuadre.db`), seeding con 15 productos criollos reales de mostrador. Swagger UI activo en `http://localhost:3001/api/docs`.
   - **Identidad de Marca**: Brand Book oficial de Sai (`cuadre.noche`, `cuadre.mint`, `cuadre.oro`), logotipo SVG y pack de 10 iconos criollos (`icon-tomate.svg`, etc.) empaquetados en `CriolloIcons.tsx`.
   - **Frontend**: Pantalla táctil widescreen `/pos` con grid de catálogo (filtros y buscador F3), modal de pesaje decimal para balanza con presets y función Tarar, carrito reactivo bimoneda ($/Bs a tasa BCV) y checkout rápido (F12).
   - **ClickUp**: 6 User Stories en columna `TESTING` (`US-01`, `US-02`, `US-03`, `US-11`, `US-12`, `US-04`). Próximas: `US-05` (Cobro Multimoneda) y `US-08` (Tests Vitest con Hidan).

2. 📊 **[[mg-sales-analytics|MG-SALES-ANALYTICS]] (Lanzamiento v1.0)**:
   - Dashboard analítico desacoplado en Next.js 15 + Tailwind CSS v4 con diseño idéntico a MGH.
   - Extracción en vivo de las 14 sedes de Xetux ERP (`ExtractionData/SalesFull`), búsqueda por producto/sede/fechas, KPIs automáticos y exportación CSV.
   - Activo en puerto local `http://localhost:3050`.

3. 🥢 **[[beijing_kiosk|Beijing Restaurant Menú Kiosco (Flutter)]]**:
   - Inspeccionado y certificado por Kakashi Sensei (100% limpio en `flutter analyze`, 6/6 tests aprobados).
   - `DesignCanvas` calibrado para pantalla 4K vertical Apolosign SW3299T (32").
   - Estado: En reposo a la espera del nuevo mockup visual para refinar componentes de interfaz.

4. 🛒 **[[meniox|Proyecto: Meniox (POS & Franquicias)]] & [[meniox-market-plan|Meniox Market]]**:
   - **Meniox Core**: Memoria forense y esquemas Aiven rescatados (14 sedes, 2,126 materias primas). Deuda pendiente en fixtures `inventory.integration.spec.ts`.
   - **Meniox Market (Fruterías & Víveres)**: Diseñada arquitectura Local-First unificada (Next.js + SQLite WAL mode en LAN) para equipos modestos y tolerancia 100% offline. Marco fiscal adaptado post-derogación Providencia SENIAT 0121.
   - **Propuesta Comercial SmartOps VE**: Validados costos a $8/h ($600 USD desarrollo total) + equipamiento en Venezuela + modelo recurrente SaaS ($15-$20/mes). Documento activo en [Google Docs Personal](https://docs.google.com/document/d/1Ev4Y-EbqS_7MhepIWTDQjYOHhPUUyU021Z9tHeMJzx8/edit).
   - **Foco Siguiente Jornada**: Sesión de refinamiento y pulido de la propuesta comercial final para presentación.

5. 💼 **[[masterhub-mg-hub|MasterHub (MG-HUB)]]**:
   - Corregido flujo de facturas CxP: importación de facturas de proveedores por defecto en USD ($).
   - Cambios commiteados y pusheados a la rama `dev` (`1ded2be` y `fbe0a8b`).

---

## 📌 Enlaces Útiles
- 🗺️ [[pilar-proyectos|Ecosistema de Proyectos MasterHub]]
- ⚖️ [[el-cuadre-pos-brand-brief-ejecutivo|EL CUADRE POS — Brand Brief]]
- 📊 [[mg-sales-analytics|Proyecto: MG-SALES-ANALYTICS]]
- 🥢 [[beijing_kiosk|Proyecto: Beijing Kiosk]]
- 🛒 [[meniox|Proyecto: Meniox]]
- 💼 [[masterhub-modulo-finanzas|Plan Fast-Track MS-FINANZAS]]
- 📝 [[log|Log de Bitácora Operativa]]
