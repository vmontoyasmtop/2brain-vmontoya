---
title: "Planificación de Sprints & Backlog Scrum: Módulo de Finanzas (finance-ms)"
type: "concept"
area: "proyectos"
created: 2026-09-16
updated: 2026-09-16
sources:
  - "wiki/proyectos/masterhub-modulo-finanzas.md"
  - "wiki/proyectos/propuesta-scrum-modulo-finanzas.md"
tags:
  - scrum
  - finanzas
  - masterhub
  - clickup
  - sprints
  - gherkin
---

# 📋 Planificación de Sprints & Backlog Scrum: Módulo de Finanzas (`finance-ms`) [Plan B Exprés]

*Plan de trabajo ágil acelerado (Plan B Exprés por Premura) estructurado en 4 Sprints Timeboxed para 1 único desarrollador (Ing. Víctor Montoya).*

---

## 📌 1. Resumen Ejecutivo & Cronograma de Desarrollo

* **Desarrollador Único**: Ing. Víctor Montoya (Dedicación Prioritaria Fast-Track)
* **Modalidad**: Plan B Exprés por Premura ($6,000.00 USD)
* **Duración por Sprint**: 1.5 Semanas (Fast-Track)
* **Total Proyecto**: 4 Sprints | 6 Semanas | 67 Story Points | $6,000.00 USD ($1,500.00 USD / Sprint)

| Sprint | Fechas de Ejecución | Duración | Story Points | Entregable Clave | Hito Financiero |
| :--- | :---: | :---: | :---: | :--- | :---: |
| **Sprint 1** | 21/09/2026 – 01/10/2026 | 1.5 sem | 21 SP | MVP CxP, Motor Fiscal SENIAT, Tasa BCV & Propuesta de Pago PDF | $1,500.00 USD |
| **Sprint 2** | 02/10/2026 – 12/10/2026 | 1.5 sem | 18 SP | Egresos, Enrutamiento Bancario (BNC/Provincial), TXT & MinIO S3 | $1,500.00 USD |
| **Sprint 3** | 13/10/2026 – 23/10/2026 | 1.5 sem | 15 SP | CxC, Conciliación Masiva CSV & Calculadora Comisiones POS | $1,500.00 USD |
| **Sprint 4** | 24/10/2026 – 02/11/2026 | 1.5 sem | 13 SP | Caja Chica, Cuota Marketing 4%, Audit Logs SENIAT & Release Staging/Prod | $1,500.00 USD |

---

## 🔗 2. Tarjetas Creadas en ClickUp (`clickup-trabajo`)

Se han creado e integrado las subtareas hijas bajo la tarea principal **`MS-FINANZAS`** (ID: `86bb7qxde`) en el espacio **MasterHub** / lista **1er Fase**:

1. **Sprint 1: MVP CxP & Motor Fiscal SENIAT** (ID ClickUp: `86bc224z8`)
2. **Sprint 2: Egresos, Enrutamiento BNC/Provincial & TXT** (ID ClickUp: `86bc2251g`)
3. **Sprint 3: CxC & Conciliación Masiva CSV** (ID ClickUp: `86bc22532`)
4. **Sprint 4: Caja Chica, Cuota Marketing (4%) & Release** (ID ClickUp: `86bc225cr`)

---

## 🏃 3. Desglose Detallado por Sprints & Historias de Usuario

### 🏆 SPRINT 1: MVP Cuentas por Pagar (CxP) & Motor Fiscal SENIAT
- **Duración**: 21/09/2026 – 01/10/2026 (1.5 Semanas | 21 SP | Hito: $1,500.00 USD)
- **Goal**: Automatizar la recepción de facturas, cálculo fiscal SENIAT y generación del PDF de propuesta de pago los martes a las 5:00 PM.

#### Historias de Usuario:
1. **US 1.1: Modelado Prisma ORM & Base DB** (4h | 3 SP)
   - *Como* desarrollador, *quiero* crear el esquema Prisma para `Supplier`, `AccountPayable`, `TaxRetention` y `PaymentProposal`, *para* persistir los registros financieros con integridad referencial.
2. **US 1.2: API CxP & Sincronización Tasa BCV** (6h | 5 SP)
   - *Como* analista IT, *quiero* registrar facturas en USD/Bs y consultar la tasa oficial BCV automáticamente, *para* congelar el monto en bolívares a la fecha de emisión.
3. **US 1.3: Motor Fiscal SENIAT (IVA e ISLR)** (6h | 5 SP)
   - *Como* contador, *quiero* que el sistema calcule retenciones del 75%/100% de IVA y porcentajes de ISLR según la categoría del proveedor, *para* emitir el comprobante oficial de 14 dígitos.
   - *Gherkin*:
     - **Dado** que se registra una factura con IVA del 16% de un Proveedor de Retención 75%,
     - **Cuando** se procesa la retención,
     - **Entonces** el sistema calcula exactamente el 75% del IVA facturado y genera el número de comprobante `YYYYMMXXXXXXXX`.
4. **US 1.4: Cronjob de Propuesta Semanal de Pago (PDF)** (6h | 5 SP)
   - *Como* Director (Sr. Emiliano), *quiero* recibir todos los martes a las 5:00 PM una propuesta consolidada en PDF de facturas a pagar, *para* aprobar los egresos de la semana.
5. **US 1.5: UI React / Next.js para Carga y Aprobación** (8h | 3 SP)
   - *Como* usuario de MasterHub, *quiero* una interfaz intuitiva con formularios y tablas interactivas, *para* revisar y aprobar facturas pendientes.

---

### 📦 SPRINT 2: Egresos, Enrutamiento Bancario & Archivos TXT
- **Duración**: 02/10/2026 – 12/10/2026 (1.5 Semanas | 18 SP | Hito: $1,500.00 USD)
- **Goal**: Automatizar la emisión de pagos masivos mediante enrutamiento inteligente de cuentas (BNC / Provincial) y generación de lotes TXT.

#### Historias de Usuario:
1. **US 2.1: Enrutamiento Inteligente de Cuentas Bancarias** (8h | 5 SP)
   - *Como* tesorero, *quiero* asociar cuentas de origen y destino por sucursal/banco, *para* enviar la orden de pago al banco correspondiente.
2. **US 2.2: Generador de Lotes TXT Bancarios (BNC / Provincial)** (8h | 5 SP)
   - *Como* pagador, *quiero* exportar lotes de pago en formato TXT estructurado según las especificaciones de BNC y Banco Provincial, *para* cargarlos directamente en la banca en línea.
3. **US 2.3: Gestión de Soportes Digitales en MinIO (S3)** (8h | 5 SP)
   - *Como* auditor, *quiero* adjuntar comprobantes de transferencia y facturas en formato PDF/imagen a MinIO S3, *para* mantener la valija digital vinculada a cada egreso.
4. **US 2.4: Módulo de Conciliación Manual de Egresos** (6h | 3 SP)
   - *Como* contador, *quiero* marcar pagos como liquidados e ingresar el número de referencia bancaria, *para* cerrar el ciclo de egresos.

---

### 📊 SPRINT 3: Cuentas por Cobrar (CxC) & Conciliación Masiva CSV
- **Duración**: 13/10/2026 – 23/10/2026 (1.5 Semanas | 15 SP | Hito: $1,500.00 USD)
- **Goal**: Cruzar automáticamente los extractos bancarios CSV con las ventas registradas en Xetux y calcular comisiones POS e ISLR TC.

#### Historias de Usuario:
1. **US 3.1: Parser de Extractos Bancarios CSV & Conciliación Masiva** (10h | 5 SP)
   - *Como* analista financiero, *quiero* subir el archivo CSV del banco, *para* que el sistema busque y concilie automáticamente las ventas diarias por fecha y monto.
2. **US 3.2: Calculadora de Comisiones POS (0.30%) y Retención ISLR TC (2%)** (10h | 5 SP)
   - *Como* contador, *quiero* aplicar el cálculo de deducción bancaria del 0.30% y la retención del 2% sobre puntos de venta, *para* registrar el ingreso neto real en caja.
3. **US 3.3: Estado de Cuenta de Clientes & Reclamaciones CxC** (10h | 5 SP)
   - *Como* administrador, *quiero* visualizar saldos pendientes y notas de crédito de clientes corporativos, *para* gestionar la cobranza.

---

### 💼 SPRINT 4: Caja Chica, Cuota Marketing (4%), Audit Logs & Release
- **Duración**: 24/10/2026 – 02/11/2026 (1.5 Semanas | 13 SP | Hito: $1,500.00 USD)
- **Goal**: Arqueo de caja chica por sucursal, automatización de cuota de marketing (4%), trazabilidad SENIAT y despliegue final.

#### Historias de Usuario:
1. **US 4.1: Arqueo e Inspección de Caja Chica Semanal** (8h | 3 SP)
   - *Como* gerente de sucursal, *quiero* registrar gastos menores y vales de caja chica, *para* solicitar la reposición de fondo semanal.
2. **US 4.2: Deducción Automática de Cuota de Marketing (4%)** (6h | 3 SP)
   - *Como* dirección general, *quiero* calcular automáticamente el 4% sobre las ventas brutas de cada sede, *para* destinar el fondo a las campañas publicitarias.
3. **US 4.3: Audit Logs & Trazabilidad SENIAT** (10h | 5 SP)
   - *Como* auditor fiscal, *quiero* un registro inalterable de cada modificación, usuario e IP en comprobantes de retención, *para* garantizar cumplimiento normativo ante el SENIAT.
4. **US 4.4: Despliegue en Staging / Producción & Cierre** (6h | 2 SP)
   - *Como* líder técnico, *quiero* ejecutar las migraciones finales de base de datos y despliegue en Hetzner Cloud con Coolify, *para* poner el módulo 100% en producción.

---

## 🔗 Enlaces Relacionados (Wikilinks)
- [[Módulo de Finanzas: Especificación Técnica (finance-ms)|masterhub-modulo-finanzas.md]]
- [[Propuesta Metodológica Scrum: Módulo de Finanzas (finance-ms)|propuesta-scrum-modulo-finanzas.md]]
- [[Proyecto: MasterHub (MG-HUB)|masterhub-mg-hub.md]]
- [[Dashboard de Vida & Centro de Control|../life-dashboard.md]]
