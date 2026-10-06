---
title: "🤝 Propuesta de Colaboración Técnica: Módulo de Finanzas (finance-ms) — $500/Sprint"
type: "project"
area: "proyectos"
created: 2026-10-05
updated: 2026-10-05
tags:
  - propuesta
  - desarrollador
  - finanzas
  - masterhub
  - sprints
---

# 🤝 Propuesta de Colaboración Técnica: Módulo de Finanzas (`finance-ms`) — MasterHub

**Proyecto**: MasterHub — Módulo de Finanzas, Facturación, Fiscalidad SENIAT & Conciliación  
**Rol Solicitado**: Desarrollador Co-Piloto / Fullstack UI & API Integration (Next.js / React / TypeScript)  
**Líder Técnico**: Ing. Víctor Montoya  
**Fecha**: Octubre 2026  
**Esquema de Compensación**: **$500.00 USD por Sprint** (Total: **$2,000.00 USD** / 4 Sprints)

---

## 📌 1. Visión General del Proyecto

Buscamos integrar a un **Desarrollador Co-Piloto** para colaborar directamente con el Líder Técnico en la construcción, maquetación UI/UX, desarrollo de componentes interactivos y consumo de APIs en el microservicio **`finance-ms`** de la plataforma empresarial **MasterHub**.

El módulo automatiza:
- Cuentas por Pagar (CxP) y Cuentas por Cobrar (CxC).
- Motor de retenciones fiscales SENIAT (75%/100% IVA e ISLR).
- Generación de archivos planos TXT para pagos bancarios (BNC / Banco Provincial).
- Conciliación masiva de extractos bancarios CSV y control de caja chica.

---

## 🛠️ 2. Stack Tecnológico & Alcance de Responsabilidades

### Stack Principal del Proyecto:
* **Frontend**: Next.js 16 (React 19, Tailwind CSS, Lucide React, Shadcn/UI).
* **Backend API & DB**: NestJS / Express REST APIs + Prisma ORM (PostgreSQL).
* **Almacenamiento**: MinIO (S3 compatible) para soportes y valija digital.
* **Control de Versiones & CI/CD**: Git / GitHub + Hetzner Cloud con Coolify.

### Responsabilidades del Desarrollador:
1. **Maquetación UI/UX**: Construir vistas responsivas, modales y formularios reactivos basados en los requerimientos del módulo.
2. **Consumo e Integración de APIs**: Conectar la interfaz con los endpoints provistos por el Backend (validaciones, estados de carga, manejo de errores).
3. **Manejo de Formularios y Tablas Complejas**: Carga de facturas, tablas paginadas de CxP/CxC, filtros por sucursal y selectores dinámicos de retenciones.
4. **Validación en Staging**: Ejecutar pruebas de integración conjuntas con el Líder Técnico en el entorno de pruebas.

---

## 💰 3. Esquema Financiero & Condiciones de Pago

El desarrollo se gestionará bajo metodología **Scrum en 4 Sprints Timeboxed**. La remuneración se liquidará **contra entrega y validación funcional** de cada hito en el entorno de Staging.

```
+---------------------------------------------------------------------------------------------------------+
|                                    ESQUEMA DE COMPENSACIÓN POR HITO                                      |
+---------------------------------------------------------------------------------------------------------+
| SPRINT / HITO                         | DURACIÓN ESTIMADA    | ENTREGABLE PRINCIPAL     | PAGO POR HITO |
+---------------------------------------+----------------------+--------------------------+---------------+
| Sprint 1: MVP CxP & Motor Fiscal      | 1.5 a 2 Semanas      | Vistas CxP + Retenciones | $500.00 USD   |
| Sprint 2: Egresos & Lotes Bancarios   | 1.5 a 2 Semanas      | Egresos + Generador TXT  | $500.00 USD   |
| Sprint 3: CxC & Conciliación Masiva   | 1.5 a 2 Semanas      | CxC + Parser CSV Bancos  | $500.00 USD   |
| Sprint 4: Caja Chica & Release Final  | 1.5 a 2 Semanas      | Arqueo Caja + Dashboard  | $500.00 USD   |
+---------------------------------------+----------------------+--------------------------+---------------+
| TOTAL PROYECTO                        | 6 a 8 Semanas        | 4 Hitos Completos        | $2,000.00 USD |
+---------------------------------------------------------------------------------------------------------+
```

---

## 🏃 4. Desglose de Entregables por Sprint

### 🏆 SPRINT 1: Cuentas por Pagar (CxP) & Motor Fiscal SENIAT
* **Compensación**: **$500.00 USD**
* **Alcance del Dev**:
  * Formulario reactivo para registro de facturas multimoneda (USD/Bs).
  * Componente visual para cálculo y previsualización de retenciones de IVA (75%/100%) e ISLR.
  * Tabla interactiva de cuentas por pagar con filtros por estado y proveedor.
  * Modal/vista para revisión y aprobación de la propuesta semanal de pago en PDF.

### 📦 SPRINT 2: Egresos, Enrutamiento Bancario & Archivos TXT
* **Compensación**: **$500.00 USD**
* **Alcance del Dev**:
  * Interfaz de selección de cuentas bancarias de origen/destino (BNC y Banco Provincial).
  * Componente para exportar y descargar lotes de pago en formato TXT estructurado.
  * Módulo para adjuntar y visualizar comprobantes de transferencia y soportes en S3 (MinIO).
  * Pantalla de conciliación y liquidación manual de egresos.

### 📊 SPRINT 3: Cuentas por Cobrar (CxC) & Conciliación Masiva CSV
* **Compensación**: **$500.00 USD**
* **Alcance del Dev**:
  * Interfaz Drag & Drop para carga masiva de extractos bancarios en CSV.
  * Tabla comparativa de conciliación (ventas registradas vs. extracto bancario).
  * Vistas de estados de cuenta de clientes corporativos y gestión de saldos pendientes.
  * Componente visual para deducción de comisiones POS (0.30%) y retención ISLR TC (2%).

### 💼 SPRINT 4: Caja Chica, Dashboard Financiero & Cierre
* **Compensación**: **$500.00 USD**
* **Alcance del Dev**:
  * Módulo de registro de vales, gastos menores y arqueo semanal de caja chica por sucursal.
  * Dashboard de métricas financieras (resumen de ingresos, egresos, retenciones del mes).
  * Pulido general de UI/UX, estados de error, responsive design y pruebas finales con QA.
  * Puesta a punto para pase a Producción.

---

## 📋 5. Términos y Metodología de Trabajo

1. **Liquidación Inmediata por Hito**: El monto de **$500.00 USD** correspondiente a cada Sprint se pagará de manera inmediata tras la revisión y aprobación del hito funcional desplegado en Staging.
2. **Acompañamiento Técnico**: El Líder Técnico (Ing. Víctor Montoya) proveerá la arquitectura base, endpoints documentados, esquemas de BD y soporte diario para dudas técnicas.
3. **Flujo de Trabajo Git**: El código se entregará a través de Pull Requests en ramas de feature organizadas y tipadas.
4. **Garantía y Ajustes**: Compromiso de 15 días posteriores a la entrega de cada hito para corrección de bugs o ajustes menores en las interfaces desarrolladas.

---

### 📝 Confirmación de Acuerdo y Aceptación

**Nombre del Desarrollador**: _____________________________________________  
**Documento / ID**: _____________________________________________________  
**Firma**: ___________________________ **Fecha**: _____ / _____ / 2026  
**Líder Técnico (MasterHub)**: Ing. Víctor Montoya  
