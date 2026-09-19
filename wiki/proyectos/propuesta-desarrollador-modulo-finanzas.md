---
title: "🤝 Propuesta de Colaboración Técnica: Módulo de Finanzas (`Finance MS`) — MasterHub"
type: "project"
area: "proyectos"
created: 2026-09-11
updated: 2026-09-18
tags:
  - 
---

# 🤝 Propuesta de Colaboración Técnica: Módulo de Finanzas (`Finance MS`) — MasterHub

**Proyecto**: MasterHub — Módulo de Finanzas, Facturación & Conciliación  
**Rol Solicitado**: Desarrollador Co-Piloto / Frontend UI & API Integration (Next.js / React / Tailwind)  
**Líder Técnico**: Ing. Víctor Montoya  
**Fecha**: Septiembre 2026  

---

## 📌 1. Visión General del Proyecto

Buscamos integrar a un **Desarrollador Co-Piloto** para la maquetación UI/UX, construcción de componentes interactivos y consumo de APIs REST en el nuevo microservicio **`Finance MS`** de la plataforma empresarial **MasterHub**.

El proyecto comprende la digitalización de Cuentas por Pagar (CxP), Cuentas por Cobrar (CxC), automatización de retenciones fiscales (SENIAT) y conciliación bancaria.

---

## 🛠️ 2. Stack Tecnológico & Responsabilidades

### Stack Principal:
* **Frontend**: Next.js 16 (React 19, Tailwind CSS, Lucide React).
* **Backend API**: Endpoints REST expuestos por API Gateway en NestJS + Prisma ORM.
* **Almacenamiento**: MinIO (S3) para soportes digitales.

### Responsabilidades del Dev Colaborador:
1. Construcción y maquetación de vistas UI/UX responsivas basadas en el diseño acordado.
2. Integración de formularios para captura de facturas, notas de entrega y comprobantes.
3. Consumo de endpoints REST (CxP, CxC, retenciones, reportes).
4. Pruebas de integración UI con el Backend en ambiente de Staging.

---

## 💰 3. Esquema Financiero y Modalidades de Pago

El proyecto se estructura bajo metodología **Scrum en 4 Sprints (4 Hitos)**. Los pagos se realizarán **contra entregable validado** al finalizar cada Sprint.

Ofrecemos dos modalidades según la opción comercial aprobada por la empresa:

```
+---------------------------------------------------------------------------------------------------------+
|                                  TABLA DE COMPENSACIÓN POR MODALIDAD                                    |
+---------------------------------------------------------------------------------------------------------+
| CONCEPTO                            | MODALIDAD A: ESTÁNDAR            | MODALIDAD B: EXPRÉS POR PREMURA|
+-------------------------------------+----------------------------------+--------------------------------+
| Duración Total del Proyecto         | 12 Semanas (3 Meses)             | 6 Semanas (1.5 Meses)          |
| Ritmo de Sprint                     | 3 semanas por Sprint             | 1.5 semanas por Sprint         |
| Pago por Sprint / Hito (4 cuotas)   | $180.00 USD / Sprint             | $450.00 USD / Sprint           |
| Pago Total del Proyecto             | $720.00 USD                      | $1,800.00 USD                  |
| Nivel de Dedicación                 | Ritmo estándar parcial           | Prioridad e intensidad exprés  |
+---------------------------------------------------------------------------------------------------------+
```

---

## 🏃 4. Alcance Entregable por Sprint

| Sprint / Hito | Alcance UI & Integración del Dev | Entregable Clave |
| :--- | :--- | :--- |
| **Sprint 1: Cuentas por Pagar (CxP)** | Vistas de captura de facturas, selección de proveedores, cálculo visual de IVA/retenciones y tabla CxP. | Módulo CxP operativo en Staging. |
| **Sprint 2: Facturación & Egresos** | Vistas de emisión de facturas/cotizaciones, visualizador de PDF y exportación de archivos planos TXT. | Módulo de Facturación & Egresos. |
| **Sprint 3: CxC & Conciliación** | Vistas de Cuentas por Cobrar, interfaz de carga de estados de cuenta CSV y módulo de conciliación. | Módulo CxC & Conciliación. |
| **Sprint 4: Analytics & Handover** | Dashboard de gráficos financieros, exportación de reportes Excel/PDF y pulido final de UX. | Entrega final a Producción. |

---

## 📋 5. Términos y Condiciones de Colaboración

1. **Esquema de Cobro por Hito**: El pago de cada Sprint (**$180.00 USD** en Modalidad A o **$450.00 USD** en Modalidad B) se liquida de forma inmediata una vez demostrado y validado el hito funcional en el entorno de Staging.
2. **Control de Versiones**: Todo el código desarrollado se entregará mediante commits ordenados en el repositorio Git del proyecto.
3. **Soporte Post-Lanzamiento**: Garantía de 30 días para corrección de bugs menores en las interfaces desarrolladas.

---

### 📝 Confirmación de Aceptación

**Aceptado por el Desarrollador**: ___________________________  
**Fecha**: ____ / ____ / 2026  
**Modalidad**: [  ] Modalidad A ($720 USD)   |   [  ] Modalidad B ($1,800 USD Exprés)
