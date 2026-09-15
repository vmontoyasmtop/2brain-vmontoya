# Documento Comercial de Cotización y Desglose de Tareas
## Módulo de Finanzas (`finance-ms`) — MasterHub

---

### 💵 Tarifa de Desarrollo y Términos Comerciales
* **Tarifa Hora/Desarrollo**: **$10.00 USD / hora**.
* **Esquema de Pago**: Pago por Hitos / Sprints entregados (4 Entregas de $300 USD c/u).
* **Capacidad por Sprint**: 30 Horas Timeboxed (2 Semanas).
* **Costo Total del Proyecto**: **$1,200.00 USD** (120 Horas Totales).

---

### 📊 Desglose Detallado por Sprints, Tareas y Costo

```
+---------------------------------------------------------------------------------------------------+
|                         DESGLOSE PRESUPUESTARIO (TARIFA $10/HORA)                                 |
+---------------------------------------------------------------------------------------------------+
| SPRINT 1 : MVP Cuentas por Pagar (CxP) & Motor Fiscal SENIAT       [30h | $300 USD]               |
| SPRINT 2 : Egresos, Enrutamiento BNC/Provincial & Archivos TXT    [30h | $300 USD]               |
| SPRINT 3 : Cuentas por Cobrar (CxC) & Conciliación Masiva CSV     [30h | $300 USD]               |
| SPRINT 4 : Caja Chica, Cuota Marketing (4%) & Cierre Gerencial    [30h | $300 USD]               |
+---------------------------------------------------------------------------------------------------+
| TOTAL GENERAL (120 HORAS TOTALES)                                      | $1,200.00 USD            |
+---------------------------------------------------------------------------------------------------+
```

---

### 🔴 SPRINT 1: MVP Cuentas por Pagar (CxP) & Motor Fiscal SENIAT
**Entregable Hito 1**: Sistema funcional de carga CxP, motor de retenciones del SENIAT (75%/100% IVA e ISLR), tasa BCV automática y reporte PDF de Propuesta de Pago.  
**Inversión Sprint 1**: **30 Horas × $10/h = $300.00 USD** | **21 SP**

| Tarea / User Story | Descripción del Trabajo Técnico | Horas | Costo ($10/h) | SP |
| :--- | :--- | :---: | :---: | :---: |
| **US 1.1: Modelado de Datos Prisma (`finance_db`)** | Creación de esquemas en PostgreSQL/Prisma para las tablas `Supplier`, `Invoice`, `DocType` y `InvoiceStatus`. Migraciones iniciales y relaciones de base de datos. | 4 h | $40.00 USD | 3 SP |
| **US 1.2: API CxP & Regla Tasa BCV (Art. 16 IVA)** | Endpoints REST/TCP para registro de facturas por BU. Validación mandatoria con Xetux. Cronjob de consumo diario de la tasa BCV y congelación de IVA a fecha de emisión. | 6 h | $60.00 USD | 5 SP |
| **US 1.3: Motor de Retenciones Fiscales SENIAT** | Lógica impositiva de retención de IVA (75% u 100% según contribuyente especial) y alícuotas de ISLR (Condominios 2%, Alquileres 5%, Fletes 3%). | 6 h | $60.00 USD | 5 SP |
| **US 1.4: Correlativos SENIAT & Propuesta PDF** | Generación de correlativos estándar SENIAT (14 dígitos IVA e ISLR). Cronjob de recopilación los Martes 5 PM y generación de PDF consolidado descargable. | 6 h | $60.00 USD | 5 SP |
| **US 1.5: Dashboard UI Básico & Pruebas** | Formulario en Next.js para carga de CxP por BU, vista de tabla de comprobantes fiscalizados y módulo de propuesta semanal de pago. | 8 h | $80.00 USD | 3 SP |
| **SUBTOTAL SPRINT 1** | **Entrega de Hito 1 (MVP CxP + SENIAT + PDF)** | **30 h** | **$300.00 USD** | **21 SP** |

---

### 🟡 SPRINT 2: Egresos, Enrutamiento Bancario & Archivos TXT
**Entregable Hito 2**: Módulo de emisión de egresos, enrutamiento por tipo de documento y exportación de TXT bancarios para lotes BNC y Provincial.  
**Inversión Sprint 2**: **30 Horas × $10/h = $300.00 USD** | **18 SP**

| Tarea / User Story | Descripción del Trabajo Técnico | Horas | Costo ($10/h) | SP |
| :--- | :--- | :---: | :---: | :---: |
| **US 2.1: Enrutamiento Bancario Inteligente** | Regla de cuentas de origen: Facturas Fiscales procesadas desde BNC; Notas de Entrega procesadas desde Banco Provincial. | 10 h | $100.00 USD | 8 SP |
| **US 2.2: Generación de Archivos Planos TXT** | Motor de exportación masiva en formato `.TXT` compatible con la plataforma del BNC y Banco Provincial para pagos por lote. | 10 h | $100.00 USD | 5 SP |
| **US 2.3: Soportes Digitales en MinIO (S3)** | Carga obligatoria de comprobantes de transferencia (PDF/JPG) almacenados en MinIO S3 y actualización de estatus a `PAID`. | 10 h | $100.00 USD | 5 SP |
| **SUBTOTAL SPRINT 2** | **Entrega de Hito 2 (Egresos + TXT Bancarios)** | **30 h** | **$300.00 USD** | **18 SP** |

---

### 🔵 SPRINT 3: Cuentas por Cobrar (CxC) & Conciliación Bancaria CSV
**Entregable Hito 3**: Módulo de conciliación masiva CSV de ventas Xetux vs. extracto bancario y calculadora de comisiones POS.  
**Inversión Sprint 3**: **30 Horas × $10/h = $300.00 USD** | **15 SP**

| Tarea / User Story | Descripción del Trabajo Técnico | Horas | Costo ($10/h) | SP |
| :--- | :--- | :---: | :---: | :---: |
| **US 3.1: Conciliación Masiva CSV** | Módulo de importación de reportes CSV de ventas Xetux y extractos bancarios. Algoritmo de cruce automático por día, sede y método de pago. | 18 h | $180.00 USD | 8 SP |
| **US 3.2: Calculadora Comisiones POS e ISLR** | Deducción automática del 2% ISLR en ventas con tarjeta de crédito y comisiones bancarias por lote (0.30%). | 12 h | $120.00 USD | 7 SP |
| **SUBTOTAL SPRINT 3** | **Entrega de Hito 3 (Conciliación CSV + POS)** | **30 h** | **$300.00 USD** | **15 SP** |

---

### 🟢 SPRINT 4: Caja Chica, Cuota Marketing (4%) & Cierre Gerencial
**Entregable Hito 4**: Módulo de arqueos de caja chica por tienda, deducción del 4% de marketing y Dashboard Gerencial unificado.  
**Inversión Sprint 4**: **30 Horas × $10/h = $300.00 USD** | **13 SP**

| Tarea / User Story | Descripción del Trabajo Técnico | Horas | Costo ($10/h) | SP |
| :--- | :--- | :---: | :---: | :---: |
| **US 4.1: Control y Arqueo de Caja Chica** | Registro de compras con tarjeta débito tienda vía valijas y módulo de cuadre físico de efectivo los Miércoles por sucursal. | 14 h | $140.00 USD | 8 SP |
| **US 4.2: Cuota de Marketing (4%) & Dashboard** | Cálculo semanal del 4% sobre Venta Neta sin IVA (descontando delivery/propinas) y cuadro de mando gerencial final. | 16 h | $160.00 USD | 5 SP |
| **SUBTOTAL SPRINT 4** | **Entrega de Hito 4 (Caja Chica + Marketing + Cierre)** | **30 h** | **$300.00 USD** | **13 SP** |

---

### 💰 Resumen Financiero Consolidado

* **Costo Total del Proyecto**: **$1,200.00 USD**
* **Horas Totales Estimadas**: **120 Horas**
* **Esquema de Pago**: 4 Hitos de **$300.00 USD** contra entrega y demostración de cada Sprint.
