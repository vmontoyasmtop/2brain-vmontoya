---
title: "Concepto: Story Points (SP) y Estimación de Esfuerzo en Scrum"
type: "concept"
area: "programacion"
created: 2026-09-14
updated: 2026-09-14
sources:
  - "wiki/proyectos/propuesta-scrum-modulo-finanzas.md"
tags:
  - scrum
  - story-points
  - estimacion
  - agile
  - pm
---

# 💡 Concepto: Story Points (SP) y Estimación Ágil

Los **Story Points (SP)** o *Puntos de Historia* son la unidad de medida estándar en la metodología **Scrum** para estimar el **esfuerzo, la complejidad técnica y el riesgo relativo** que requiere completar una Historia de Usuario (User Story) o tarea de software.

---

## 📊 Escala de Fibonacci e Interpretación de Complejidad

En estimación Scrum se utiliza tradicionalmente la secuencia modificada de Fibonacci:

| Puntos (SP) | Nivel de Complejidad | Ejemplo Típico de Desarrollo |
| :--- | :--- | :--- |
| **1 SP** | Mínima / Trivial | Cambio de etiqueta UI, ajuste de constante o linter. |
| **2 – 3 SP** | Baja | Modelado de esquema Prisma/PostgreSQL, CRUD básico. |
| **5 SP** | Media | Lógica de negocio (ej. Motor de Retenciones SENIAT, cálculo de IVA, consumos API). |
| **8 SP** | Alta | Módulos complejos con múltiples integraciones (ej. Conciliación masiva CSV). |
| **13+ SP** | Muy Alta / Épica | Debe subdividirse en Historias de Usuario más pequeñas. |

---

## 🎯 ¿Por qué usar Story Points junto al Presupuesto de Horas?

1. **Desacoplar Complejidad de Tiempo**: Las horas miden duración, pero los Story Points miden **dificultad**. Una tarea de 5 SP puede tomar 6 horas a un senior pero 12h a un junior.
2. **Justificación Comercial**: Permite explicar al cliente la densidad y el peso técnico de cada entregable en la propuesta comercial.
3. **Velocidad del Sprint**: Permite medir la cantidad de SP que el desarrollador/equipo puede entregar de forma constante en cada Sprint (ejemplo: 21 SP en 30 horas).

---

## 🔗 Referencias Cruzadas
- [[Propuesta Metodológica Scrum: Módulo de Finanzas (finance-ms)|proyectos/propuesta-scrum-modulo-finanzas.md]]
- [[Desglose Presupuestario y Cotización: Módulo de Finanzas|proyectos/desglose-presupuesto-cotizacion-finance-ms.md]]
