# 📄 PROPUESTA COMERCIAL Y TÉCNICA
## Desarrollo del Módulo de Finanzas, Facturación & Conciliación (`Finance MS`)

**Proyecto**: MasterHub (Plataforma Administrativa & Operativa)  
**Destinatario**: Dirección General & Jefatura de Finanzas  
**Presentado por**: Ing. Victor Montoya — Líder de Arquitectura de Software  
**Fecha**: 14 de Septiembre, 2026  

---

## 🎯 1. Resumen Ejecutivo & Objetivo

La presente propuesta tiene como objetivo el diseño, desarrollo e implementación a medida del microservicio **`Finance MS`**, un módulo financiero nativo para **MasterHub** concebido para automatizar la gestión contable, facturación, retenciones fiscales SENIAT, cuentas por cobrar/pagar y conciliación bancaria.

El proyecto se iniciará con una **fase de levantamiento y estudio operativo de las hojas de cálculo (Google Sheets/Excel) actuales**, permitiendo auditar la dinámica operativa real, identificar qué fórmulas y flujos deben migrarse y cuáles optimizarse. Con ello, MasterHub eliminará procesos manuales dispersos, automatizará la emisión de comprobantes fiscales y centralizará la información financiera en tiempo real.

---

## 📊 2. Análisis de Mercado & Retorno de Inversión (ROI)

Frente a soluciones comerciales estándar como **Profit Plus** u **Odoo Enterprise**, la implementación a medida para MasterHub representa una ventaja económica y tecnológica abrumadora:

| Criterio | Profit Plus Corporativo | Odoo Enterprise | 🎯 **MasterHub a Medida** |
| :--- | :--- | :--- | :--- |
| **Inversión Licencias Año 1** | $3,500 – $5,750 USD | $87 – $142 USD / usuario / año | **$0 USD (Código Propio)** |
| **Costo Implementación** | $1,500 – $4,000 USD | $5,000 – $15,000 USD | **Incluido en la Propuesta** |
| **Mantenimiento Anual** | $500 – $1,200 USD (SMA) | Recurrente de por vida | **$0 USD (Mantenimiento interno)** |
| **Integración con MasterHub** | Rígida / Compleja | Vía API externa (Lenta) | **100% Nativa (TypeScript / Prisma)** |
| **Costo Total Año 1** | **$5,000 – $10,000+ USD** | **$6,000 – $20,000+ USD** | **$2,400 USD – $6,000 USD** |

---

## 💡 3. Opciones de Ejecución y Presupuesto

Ofrecemos dos modalidades de ejecución estructuradas bajo metodología **Scrum**:

```
+---------------------------------------------------------------------------------------------------------+
|                                    TABLA COMPARATIVA DE OPCIONES                                       |
+---------------------------------------------------------------------------------------------------------+
| CARACTERÍSTICA                      | OPCIÓN A: DESARROLLO ESTÁNDAR    | OPCIÓN B: EXPRÉS POR PREMURA  |
+-------------------------------------+----------------------------------+--------------------------------+
| Modalidad de Ejecución              | Ritmo Estándar (1 Dev)           | Equipo Dual / Entrega Exprés   |
| Duración por Sprint                 | Sprints de 3 Semanas             | Sprints Acelerados (1.5 Sem.)  |
| Tiempo Total de Entrega             | 12 Semanas (3 Meses)             | 6 Semanas (1.5 Meses)          |
| Inversión Total del Proyecto        | $2,400.00 USD                    | $6,000.00 USD (Pago por Premura)|
| Forma de Pago (4 Hitos / Sprints)   | 4 cuotas de $600.00 USD          | 4 cuotas de $1,500.00 USD      |
| Tipo de Servicio                    | Desarrollo Programado            | Prioridad Absoluta & Fast-Track|
| Control de Calidad                  | Pruebas funcionales estándar     | Code Review + E2E + IA Matching|
+---------------------------------------------------------------------------------------------------------+
```

### 🔹 Opción A: Desarrollo Estándar (**$2,400.00 USD**)
Modalidad estándar para la implementación del módulo con un ritmo de desarrollo sostenido.
* **Tiempo Total**: **12 Semanas** (3 Meses).
* **Esquema de Cobro**: 4 Hitos funcionales de **$600.00 USD** cancelados al finalizar cada Sprint de 3 semanas.
* **Duración por Sprint**: 3 semanas por hito.

### 🚀 Opción B: Entrega Exprés por Premura (**$6,000.00 USD**)
Modalidad de **alta prioridad y entrega acelerada en la mitad del tiempo** asignando un equipo dual dedicado para cumplir requerimientos urgentes de negocio.
* **Tiempo Total**: **6 Semanas** (1.5 Meses).
* **Esquema de Cobro**: 4 Hitos de **$1,500.00 USD** cancelados al finalizar cada Sprint acelerado de 1.5 semanas.
* **Incluye adicionalmente**: Asignación dual prioritaria, Fast-Track delivery en la mitad del tiempo, engine de conciliación bancaria masiva con IA y suite de pruebas automatizadas (E2E).

---

## 🏃 4. Roadmap Metodológico por Sprint

El proyecto se ejecutará en 4 Hitos funcionales:

* **Sprint 1: Levantamiento Operativo (Sheets), Base de Datos & Motor Fiscal SENIAT**
  * **Estudio Operativo de Hojas de Cálculo (Sheets/Excel)**: Análisis detallado de las plantillas operativas actuales para mapear flujos de trabajo, reglas de negocio y seleccionar qué datos tomar y cuáles descartar.
  * Modelado de datos en PostgreSQL / Prisma ORM alineado a la operativa analizada.
  * Captura de CxP y congelación de IVA (Art. 16 Ley IVA).
  * Retenciones automáticas SENIAT (75%/100% IVA e ISLR).
* **Sprint 2: Motor de Facturación & Egresos**
  * Generación de Facturas, Cotizaciones y Notas de Crédito (PDF).
  * Enrutamiento de pagos bancarios y exportación de archivos planos TXT (BNC/Provincial).
* **Sprint 3: Cuentas por Cobrar (CxC) & Conciliación Bancaria**
  * Módulo de Cuentas por Cobrar (CxC) y control de cobros.
  * Conciliación automática masiva de estados de cuenta bancarios (CSV / TXT).
* **Sprint 4: Analytics, Caja Chica & Despliegue en Producción**
  * Control de efectivo por sucursal y cuota de marketing (4%).
  * Dashboard Financiero Gerencial y Audit Logs fiscal.
  * Despliegue en entorno de Producción y handover.

> ⏱ **Duración según opción elegida**:
> * **Opción A**: 3 semanas por Sprint (Semanas 1-3, 4-6, 7-9, 10-12). Total: 12 semanas.
> * **Opción B**: 1.5 semanas por Sprint (Semanas 1-1.5, 1.5-3, 3-4.5, 4.5-6). Total: 6 semanas.

---

## 🔒 5. Términos Comerciales & Control de Alcance

1. **Gestión de Requerimientos Extra y Control de Alcance**:  
   Una vez aprobados los entregables del Sprint e iniciado el desarrollo, **cualquier requerimiento adicional fuera de la operativa definida en el levantamiento inicial será planificado en un Sprint Extra**, lo cual ajustará el costo total del proyecto según su complejidad.
2. **Modalidad de Pago por Hito Entregado**: Los pagos se realizarán de forma fraccionada al finalizar cada Sprint, previa validación y aprobación por parte de la Jefatura de Finanzas en el ambiente de Staging.
3. **Modalidad Opción B (Premura y Prioridad)**: El valor de $6,000.00 USD de la Opción B corresponde a una tarifa fija por servicio de premura, prioridad de asignación y dedicación dual para acelerar la entrega a **6 semanas**.
4. **Propiedad Intelectual**: El 100% del código fuente, modelos de base de datos y documentación serán propiedad exclusiva de la empresa tras la liquidación final.
5. **Garantía Post-Lanzamiento**: Se otorgan **30 días de garantía sin costo** en Opción A (**60 días en Opción B**).
6. **Cero Costos Recurrentes**: No existen licencias por usuario ni mantenimientos obligatorios.

---

### 📝 Aprobación de la Propuesta

Aceptado por la Gerencia: ___________________________  
Fecha: ____ / ____ / 2026  
Opción Seleccionada: [  ] Opción A ($2,400 USD - 12 Semanas)   |   [  ] Opción B ($6,000 USD Exprés - 6 Semanas)
