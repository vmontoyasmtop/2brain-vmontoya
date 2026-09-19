---
title: "Propuesta Metodológica Scrum: Módulo de Finanzas (finance-ms)"
type: "project"
area: "proyectos"
created: 2026-09-14
updated: 2026-09-18
tags:
  - 
---

# 🚀 Propuesta Metodológica Scrum — Módulo de Finanzas (`finance-ms`)

Propuesta de desarrollo ágil basada en la metodología **Scrum**, con sprints iterativos e incrementales de **2 Semanas** (presupuesto timeboxed de **30 horas por Sprint**).

---

## 📐 Marco Metodológico y Capacidad de Desarrollo

* **Metodología**: Scrum (Desarrollo incremental por Sprints con entregables funcionales en cada hito).
* **Timeframe Relativo**: Sprints de **2 Semanas** contadas a partir de la aprobación oficial ($T_0$).
* **Capacidad Estimada por Sprint**: **30 Horas Efectivas de Desarrollo** (10h en semanas laborales: 2h/día Lun-Vie + 5h fin de weekend).
* **Valoración Económica**: **$20.00 USD / hora** | **$600.00 USD / Sprint** (Total Proyecto 120h: **$2,400.00 USD**).
* **Referencia de Mercado (Anclaje)**: Valoración Agencia $5,400 USD (Ahorro del +55% sin licencias recurrentes).

---

## 🏃 Roadmap de Sprints & Entregables por Hitos

```
+-------------------------------------------------------------------------------------------------+
|                         ROADMAP SCRUM POR SPRINT Y HORAS TIMEBOXED                              |
+-------------------------------------------------------------------------------------------------+
| SPRINT 1 (T0 a T0+14d) : MVP CxP & Motor Fiscal SENIAT                  [30h | 21 SP]           |
| SPRINT 2 (T0+14d a T0+28d) : Egresos, Enrutamiento BNC/Provincial & TXT [30h | 18 SP]           |
| SPRINT 3 (T0+28d a T0+42d) : CxC & Conciliación Masiva CSV              [30h | 15 SP]           |
| SPRINT 4 (T0+42d a T0+56d) : Caja Chica, Cuota Marketing (4%) & Cierre  [30h | 13 SP]           |
+-------------------------------------------------------------------------------------------------+
```

---

## 🏆 SPRINT 1: MVP Cuentas por Pagar (CxP) & Motor Fiscal SENIAT
* **Duración**: **2 Semanas** ($T_0$ ➔ $T_0 + 14$ días)
* **Presupuesto Timebox**: **30 Horas** | **Story Points**: 21 SP
* **Sprint Goal**: Entregar un sistema funcional para registrar facturas/valijas de sucursales, congelar IVA a fecha de emisión, calcular retenciones SENIAT (75%/100% IVA e ISLR) y generar la **Propuesta Semanal de Pago** en PDF.

### User Stories & Tareas del Sprint 1:

1. **US 1.1: Modelado de Datos y Estructura Core** (4h | 3 SP)  
   *Modelos `Supplier`, `Invoice`, `DocType` y `InvoiceStatus` en PostgreSQL / Prisma ORM.*
2. **US 1.2: API de Carga CxP & Cronjob Tasa BCV** (6h | 5 SP)  
   *Verificación mandatoria con Xetux por BU + Cronjob de consumo de tasa BCV diaria y congelación de IVA (Art. 16 Ley IVA).*
3. **US 1.3: Motor de Retenciones Fiscales SENIAT** (6h | 5 SP)  
   *Cálculo automático de 75%/100% IVA, alícuotas ISLR (2% condominios, 3% fletes, 5% alquileres) y correlativo de 14 dígitos.*
4. **US 1.4: Propuesta Semanal de Pago & PDF** (6h | 5 SP)  
   *Cronjob de recopilación automática los Martes a las 5:00 PM, ciclo de aprobación y reporte PDF consolidado.*
5. **US 1.5: Dashboard UI Básico & Pruebas** (8h | 3 SP)  
   *Formulario interactivo en Next.js para carga CxP y vista de tabla de propuesta semanal.*

---

## 📦 SPRINT 2: Egresos, Enrutamiento Bancario & Archivos TXT
* **Duración**: **2 Semanas** ($T_0 + 14$d ➔ $T_0 + 28$d)
* **Presupuesto Timebox**: **30 Horas** | **Story Points**: 18 SP
* **Sprint Goal**: Automatizar la emisión de pagos mediante enrutamiento inteligente de cuentas y lotes de archivos planos TXT.

---

## 📊 SPRINT 3: Cuentas por Cobrar (CxC) & Conciliación Bancaria
* **Duración**: **2 Semanas** ($T_0 + 28$d ➔ $T_0 + 42$d)
* **Presupuesto Timebox**: **30 Horas** | **Story Points**: 15 SP
* **Sprint Goal**: Eliminar discrepancias de ventas cruzando extractos bancarios CSV con reportes de Xetux y calculando comisiones POS.

---

## 💼 SPRINT 4: Caja Chica, Cuota de Marketing (4%) & Cierre
* **Duración**: **2 Semanas** ($T_0 + 42$d ➔ $T_0 + 56$d)
* **Presupuesto Timebox**: **30 Horas** | **Story Points**: 13 SP
* **Sprint Goal**: Finalizar el control de efectivo por sucursal, automatizar la retención de marketing del 4% y entregar el Dashboard Gerencial.

---

## 🔗 Referencias Cruzadas
- [[masterhub-modulo-finanzas|Módulo de Finanzas: Especificación Técnica (finance-ms)]]
- [[masterhub-mg-hub|Proyecto: MasterHub (MG-HUB)]]
- [[life-dashboard|Dashboard de Vida & Centro de Control]]
