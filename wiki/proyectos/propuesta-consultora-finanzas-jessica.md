---
title: "💼 Propuesta de Colaboración Funcional & QA: Módulo de Finanzas (`Finance MS`) — MasterHub"
type: "project"
area: "proyectos"
created: 2026-09-11
updated: 2026-09-18
tags:
  - proyectos
  - project
  - propuesta_consultora_finanzas_jessica
---

# 💼 Propuesta de Colaboración Funcional & QA: Módulo de Finanzas (`Finance MS`) — MasterHub

**Proyecto**: MasterHub — Módulo de Finanzas, Facturación & Conciliación  
**Rol Asignado**: Consultora Funcional de Finanzas & Especialista QA / UAT  
**Dirigido a**: Lcda. Jessica (Jefatura / Especialista de Finanzas)  
**Presentado por**: Ing. Víctor Montoya — Líder de Arquitectura de Software  
**Fecha**: Septiembre 2026  

---

## 🎯 1. Objetivo del Rol

Garantizar que el desarrollo del nuevo microservicio **`Finance MS`** para **MasterHub** refleje fielmente la operativa contable y fiscal de **Master Group**, eliminando la dependencia de archivos sueltos de Excel y automatizando la auditoría bajo la normativa del SENIAT.

El rol abarca desde el **Levantamiento Operativo Inicial** de las hojas de cálculo actuales hasta la **Validación y Pruebas de Aceptación (QA / UAT)** de cada entregable funcional en ambiente de Staging.

---

## 📋 2. Responsabilidades Clave por Fase del Proyecto

### Phase 1: Levantamiento Operativo de Hojas de Cálculo (Sheets / Excel)
1. **Auditoría de Plantillas Actuales**: Revisión guiada de las hojas de trabajo (Google Sheets / Excel) utilizadas por Finanzas para identificar datos necesarios, fórmulas contables y eliminar redundancias.
2. **Definición de Reglas Fiscales & SENIAT**: Validación de alícuotas de IVA (8%, 16%, Licores), porcentajes de retención de IVA (75% / 100%), retenciones de ISLR por categoría (Condominios 2%, Alquileres 5%, Fletes 3%, Servicios) y congelamiento de IVA a fecha de emisión (Art. 16 Ley IVA).
3. **Mapeo de Estructura Bancaria**: Confirmación de enrutamiento por tipo de documento (BNC para facturas fiscales; Banco Provincial para notas de entrega) y formatos de archivos planos TXT.

### Phase 2: Control de Calidad (QA) & Pruebas UAT por Sprint
1. **Pruebas de Usuario (UAT)**: Realizar pruebas funcionales en el entorno de Staging previo a la liberación de cada Sprint.
2. **Homologación de Cálculos**: Verificar que los montos, comprobantes correlativos y retenciones generados por MasterHub coincidan exactamente con la normativa contable.
3. **Firma de Aprobación de Hito**: Emitir el visto bueno funcional para proceder con la liberación de pagos de cada hito.

---

## 💰 3. Esquema Financiero y Modalidades de Compensación

La compensación económica está directamente vinculada al cumplimiento y aprobación de los **4 Sprints (Hitos)** del proyecto. Los pagos se efectuarán **contra la validación y firma del hito** en Staging.

```
+---------------------------------------------------------------------------------------------------------+
|                                TABLA DE COMPENSACIÓN FUNCIONAL & QA                                    |
+---------------------------------------------------------------------------------------------------------+
| CONCEPTO                            | MODALIDAD A: ESTÁNDAR            | MODALIDAD B: EXPRÉS POR PREMURA|
+-------------------------------------+----------------------------------+--------------------------------+
| Duración Total del Proyecto         | 12 Semanas (3 Meses)             | 6 Semanas (1.5 Meses)          |
| Ritmo de Sprint                     | 3 semanas por Sprint             | 1.5 semanas por Sprint         |
| Pago por Sprint / Hito (4 cuotas)   | $90.00 USD / Sprint              | $225.00 USD / Sprint           |
| Pago Total del Proyecto             | $360.00 USD                      | $900.00 USD                    |
| Intensidad de Revisiones            | Estándar (1 revisión por hito)   | Exprés / Prioridad Alta        |
+---------------------------------------------------------------------------------------------------------+
```

---

## 🏃 4. Entregables y Criterios de Aceptación QA por Sprint

| Sprint / Hito | Alcance de Levantamiento & Pruebas QA de Jessica | Criterio de Aprobación para Pago |
| :--- | :--- | :--- |
| **Sprint 1: Cuentas por Pagar (CxP) & SENIAT** | • Levantamiento de plantillas CxP.<br>• Validación de cálculo de retenciones IVA (75%/100%) e ISLR.<br>• Verificación de correlativos de comprobantes SENIAT. | Aprobación funcional de tabla CxP y comprobantes en Staging. |
| **Sprint 2: Egresos & Enrutamiento Bancario** | • Auditoría de enrutamiento BNC vs. Provincial.<br>• Validación de formato de archivos planos TXT.<br>• Verificación de subida de soportes de pago (MinIO). | Aprobación de generación de TXT bancario y soporte digital. |
| **Sprint 3: CxC & Conciliación Bancaria** | • Mapeo de flujo de Cuentas por Cobrar.<br>• Pruebas de conciliación masiva con estados de cuenta CSV.<br>• Verificación de saldos y abonos. | Aprobación del motor de conciliación y reporte de CxC. |
| **Sprint 4: Caja Chica, Marketing (4%) & Release** | • Definición de reglas de Caja Chica por sucursal.<br>• Validación de cálculo del 4% de cuota de Marketing.<br>• Auditoría final de Dashboard Gerencial. | Firma de Acta de Aceptación Final y Pase a Producción. |

---

## 📑 5. Condición de Cobro

- **Hito Aprobado = Pago Liberado**: El monto correspondiente a cada Sprint (**$90.00 USD** en Modalidad A o **$225.00 USD** en Modalidad B) se liberará una vez que la Lcda. Jessica valide y firme la conformidad del hito en el ambiente de Staging.

---

### 📝 Confirmación y Conformidad

**Lcda. Jessica (Consultora Finanzas & QA)**: ___________________________  
**Ing. Víctor Montoya (Líder Técnico)**: ___________________________  
**Fecha**: ____ / ____ / 2026  
**Modalidad Aceptada**: [  ] Modalidad A ($360 USD)   |   [  ] Modalidad B ($900 USD Exprés)
