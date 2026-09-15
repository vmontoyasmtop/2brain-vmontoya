---
title: "Desglose Presupuestario y Cotización: Módulo de Finanzas (finance-ms)"
type: "concept"
area: "proyectos"
created: 2026-09-14
updated: 2026-09-14
sources:
  - "raw/finanzas/cotizacion-modulo-finanzas.md"
  - "wiki/proyectos/propuesta-scrum-modulo-finanzas.md"
tags:
  - finanzas
  - cotizacion
  - presupuesto
  - masterhub
  - scrum
  - hitos
---

# 💵 Desglose Presupuestario y Cotización: Módulo de Finanzas (`finance-ms`)

Documento comercial de valoración económica y desglose detallado de tareas por horas para el desarrollo del microservicio de finanzas de MasterHub.

---

## 💵 Términos Comerciales & Estructura de Pagos

* **Tarifa Hora/Desarrollo**: **$5.00 USD / hora**.
* **Presupuesto Total**: **$600.00 USD** (120 Horas Totales).
* **Esquema de Cobro**: Pago por Hitos contra entrega probada de cada Sprint (**4 Cuotas de $150.00 USD**).
* **Timebox por Sprint**: **30 Horas** (2 Semanas).

---

## 📊 Desglose por Sprints y Tareas

### 🔴 SPRINT 1: MVP Cuentas por Pagar (CxP) & Motor Fiscal SENIAT
**Monto Hito 1**: **$150.00 USD** (30 Horas × $5/h) | **21 SP**

| Tarea / User Story | Descripción del Trabajo | Horas | Subtotal ($5/h) | SP |
| :--- | :--- | :---: | :---: | :---: |
| **US 1.1: Modelado Prisma (`finance_db`)** | Tablas `Supplier`, `Invoice`, `DocType` y `InvoiceStatus` en PostgreSQL/Prisma. | 4 h | $20.00 USD | 3 SP |
| **US 1.2: API CxP & Regla Tasa BCV** | Endpoints de carga CxP por BU + Cronjob BCV diario + congelación IVA fecha emisión. | 6 h | $30.00 USD | 5 SP |
| **US 1.3: Motor Retenciones SENIAT** | Lógica impositiva 75%/100% IVA y alícuotas ISLR (2% condominios, 3% fletes, 5% alquileres). | 6 h | $30.00 USD | 5 SP |
| **US 1.4: Correlativos SENIAT & PDF** | Correlativo de 14 dígitos SENIAT + Cronjob Martes 5 PM + reporte PDF consolidado. | 6 h | $30.00 USD | 5 SP |
| **US 1.5: Dashboard UI CxP & Pruebas** | Formulario Next.js para carga CxP y vista de tabla de propuesta semanal. | 8 h | $40.00 USD | 3 SP |
| **SUBTOTAL HITO 1** | **Entrega MVP CxP + Retenciones + PDF** | **30 h** | **$150.00 USD** | **21 SP** |

---

### 🟡 SPRINT 2: Egresos, Enrutamiento Bancario & Archivos TXT
**Monto Hito 2**: **$150.00 USD** (30 Horas × $5/h) | **18 SP**

| Tarea / User Story | Descripción del Trabajo | Horas | Subtotal ($5/h) | SP |
| :--- | :--- | :---: | :---: | :---: |
| **US 2.1: Enrutamiento Bancario** | Reglas de pago: BNC para facturas fiscales y Provincial para notas de entrega. | 10 h | $50.00 USD | 8 SP |
| **US 2.2: Archivos Planos TXT** | Generador de lotes TXT formateados conforme a la banca (BNC / Provincial). | 10 h | $50.00 USD | 5 SP |
| **US 2.3: Soportes MinIO (S3)** | Carga obligatoria de transferencias a MinIO y actualización a estatus `PAID`. | 10 h | $50.00 USD | 5 SP |
| **SUBTOTAL HITO 2** | **Entrega Egresos + TXT Bancarios** | **30 h** | **$150.00 USD** | **18 SP** |

---

### 🔵 SPRINT 3: Cuentas por Cobrar (CxC) & Conciliación Masiva CSV
**Monto Hito 3**: **$150.00 USD** (30 Horas × $5/h) | **15 SP**

| Tarea / User Story | Descripción del Trabajo | Horas | Subtotal ($5/h) | SP |
| :--- | :--- | :---: | :---: | :---: |
| **US 3.1: Conciliación Masiva CSV** | Módulo de cruce automático entre reportes de ventas Xetux y extractos bancarios. | 18 h | $90.00 USD | 8 SP |
| **US 3.2: Comisiones POS e ISLR** | Calculadora de descuento 2% ISLR TC y comisión 0.30% por lote. | 12 h | $60.00 USD | 7 SP |
| **SUBTOTAL HITO 3** | **Entrega Conciliación CSV + POS** | **30 h** | **$150.00 USD** | **15 SP** |

---

### 🟢 SPRINT 4: Caja Chica, Cuota Marketing (4%) & Cierre Gerencial
**Monto Hito 4**: **$150.00 USD** (30 Horas × $5/h) | **13 SP**

| Tarea / User Story | Descripción del Trabajo | Horas | Subtotal ($5/h) | SP |
| :--- | :--- | :---: | :---: | :---: |
| **US 4.1: Arqueo de Caja Chica** | Registro de pagos tienda y cuadre físico de efectivo los Miércoles por sucursal. | 14 h | $70.00 USD | 8 SP |
| **US 4.2: Cuota Marketing & Dashboard** | Cálculo semanal del 4% sobre Venta Neta y Dashboard Gerencial unificado. | 16 h | $80.00 USD | 5 SP |
| **SUBTOTAL HITO 4** | **Entrega Final Módulo Finanzas** | **30 h** | **$150.00 USD** | **13 SP** |

---

## 🔗 Referencias Cruzadas
- [[Propuesta Metodológica Scrum: Módulo de Finanzas (finance-ms)|proyectos/propuesta-scrum-modulo-finanzas.md]]
- [[Módulo de Finanzas: Especificación Técnica (finance-ms)|proyectos/masterhub-modulo-finanzas.md]]
- [[Proyecto: MasterHub (MG-HUB)|proyectos/masterhub-mg-hub.md]]
- [[Concepto: Story Points (SP) y Estimación de Esfuerzo en Scrum|concepts/story-points-y-estimacion-scrum.md]]
