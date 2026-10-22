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
| **O6** | MVP EL CUADRE POS (Kiosko & Balanza Criolla) | 🚀 [[el-cuadre-pos-brand-brief-ejecutivo|EL CUADRE POS]] | Terminal Táctil, Balanza, Finanzas y Arqueo Ciego | 🟢 92.8% Completado (13/14 US) |

---

## ⚡ Estado de Proyectos y Enfoque Activo (Noviembre 2026)

### 🔔 Recordatorios y Bloques Agendados (Alertas Push 15 min antes)
- [ ] **04-Nov 08:00 PM** — 🦈 **Sesión Nocturna SmartOps / El Cuadre Marchador Mobile (US-19)** ([Evento en Google Calendar `t50op5t36grfs632jin8o46074`](https://www.google.com/calendar/event?eid=dDUwb3A1dDM2Z3JmczYzMmppbjhvNDYwNzQgdm1vbnRveWEuc21hcnRvcHN2ZUBt) | [Subtarea ClickUp `86bcxuxe1`](https://app.clickup.com/t/86bcxuxe1)): Continuar implementación de las **8 pantallas móviles generadas en Google Stitch** (4 vistas de POS Móvil: Venta en Pasillo, Pesaje Criollo *"Dame X Bs/$"*, Ticket & Marchar a Caja Principal y Cobro Móvil con Pago Móvil QR; + 4 vistas Operativas: Escáner por Cámara, Marcado Bimoneda `$/Bs`, Recepción/Conteo Offline-First SQLite y Cola de Etiquetas Bluetooth `50x30mm`) junto a **Kisame** (Flutter) y **Kakuzu** (NestJS LAN Sync).

1. ⚖️ **[[el-cuadre-pos-brand-brief-ejecutivo|EL CUADRE POS — Kiosko, Frutería, Moda & Abasto Criollo]]**:
   - **📱 App Móvil "El Cuadre Marchador" ([[diseno-ui-el-cuadre-marchador-mobile|US-19 — Suite de 8 Pantallas en Google Stitch]])**:
     - Desplegadas por **🦋 Konan** en Google Stitch (`projects/15301442243370859300`) las **8 pantallas móviles nativas**:
       - **Módulo POS Móvil (4 vistas)**: Venta en Pasillo (`2e54bb5383834a9a9d72b249f21476bf`), Pesaje & Modo Criollo *"Dame X Bs/$"* (`1e35c6410cf14aa3b52fa7b1e661f951`), Ticket & Marchar a Caja Principal (`37e5706cc856401b861de6454a245605`) y Cobro Móvil Bimoneda con QR en Sitio (`a1989a16f8494e88a61efdddcdcfd364`).
       - **Módulo Operaciones de Pasillo (4 vistas)**: Escáner por Cámara `<100ms` (`56370eaa8ec241a580731bf85ca5178c`), Marcado Bimoneda `$/Bs` & Margen (`e29e95156ea348bfa6047aae92d5e4ca`), Recepción & Conteo Offline-First SQLite (`774321dd5c084074b482e287eca88c06`) y Cola de Etiquetas Bluetooth `50x30mm` (`5c47cdeb43d244fc859da0a4ba9fe7e9`).
   - **Backend & Finanzas**: NestJS + SQLite WAL Mode con Prisma ORM (`elcuadre.db`). Endpoint de finanzas, egresos de caja menor y utilidad neta (`US-07`). 26/26 pruebas unitarias aprobadas por Hidan (100%).
   - **Frontend & Arnés de Calidad**: Next.js 14 App Router protegido por el Arnés Akatsuki (`quality-harness.js`) con 0 errores y compilación limpia (8/8 páginas estáticas).
   - **Documentación & Manuales**: Manual del Cajero ilustrado y guías offline incorporadas en `/docs` (`US-09`).
   - **Sprint ClickUp**: **13 de 14 User Stories completadas (92.8%)**. Única pendiente: `US-10` (Libro de Fiados Digital).
   - **💡 Backlog Futuro & Roadmap V2**: Documentado en [[el-cuadre-pos-roadmap-v2-rea|EL CUADRE POS — Roadmap Estratégico V2 & Benchmarking REA]] (Balanzas Seriales en vivo, Impresión ESC/POS directa, Multi-Caja LAN Mesh y App Flutter para el dueño).
   - **Repositorio Oficial**: [GitHub (`vmontoyasmtop/el-cuadre-pos`)](https://github.com/vmontoyasmtop/el-cuadre-pos) sincronizado en `origin/main`.

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

## ⏰ Matriz de Time-Blocking Oficial (Google Calendar: `vmontoya@mastergroupve.com`)

| Día de la Semana | Bloque Matutino (09:00 - 11:30 / 12:30) | Almuerzo | Bloque Vespertino (13:30 - 16:30) |
| :--- | :--- | :---: | :--- |
| **Lunes** | 🧪 **TIME QA & TESTING**: Pruebas funcionales y regresión | 🍽️ 12:30-13:30 | 🧠 **DEEP WORK**: Arquitectura, modelado y diseño |
| **Martes** | 💻 **TIME DEV**: Programación intensiva con subagentes | 🍽️ 12:30-13:30 | 💻 **TIME DEV**: Construcción de features & endpoints |
| **Miércoles** | 🧪 **TIME QA & TESTING**: Auditoría de interfaces y cajas | 🍽️ 12:30-13:30 | 🧠 **DEEP WORK**: Foco cognitivo y PR reviews |
| **Jueves** | 💻 **TIME DEV**: Programación intensiva con subagentes | 🍽️ 12:30-13:30 | 💻 **TIME DEV**: Mobile (Kakashi), APIs y microservicios |
| **Viernes** | 🧪 **TIME QA & TESTING**: Certificación semanal de sprints | 🍽️ 12:30-13:30 | 🧠 **DEEP WORK**: Cierre técnico y consolidación |

*(Nota: De 08:30 a 09:00 de Lunes a Viernes se mantiene la **Daily Meeting IT** con Soporte).*

---

## 📌 Enlaces Útiles
- 🗺️ [[pilar-proyectos|Ecosistema de Proyectos MasterHub]]
- ⚖️ [[el-cuadre-pos-brand-brief-ejecutivo|EL CUADRE POS — Brand Brief]]
- 📊 [[mg-sales-analytics|Proyecto: MG-SALES-ANALYTICS]]
- 🥢 [[beijing_kiosk|Proyecto: Beijing Kiosk]]
- 🛒 [[meniox|Proyecto: Meniox]]
- 💼 [[masterhub-modulo-finanzas|Plan Fast-Track MS-FINANZAS]]
- 📝 [[log|Log de Bitácora Operativa]]
