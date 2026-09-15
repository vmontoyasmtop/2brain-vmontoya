---
title: "Resumen: Módulo de Finanzas (finance-ms) - MasterHub"
type: "summary"
area: "finanzas"
created: 2026-09-14
updated: 2026-09-14
sources:
  - "raw/finanzas/requerimiento-modulo-finanzas.md"
tags:
  - finanzas
  - masterhub
  - prd
  - seniat
  - cxp
  - cxc
---

# 📄 Resumen: Módulo de Finanzas (`finance-ms`) — MasterHub

Resumen ejecutivo del documento de requerimientos (PRD) levantado para el microservicio de finanzas de Master Group.

---

## 🎯 Puntos Clave del Alcance

1. **Digitalización & SENIAT**: Sustitución del modelo basado en hojas de cálculo y Profit por un microservicio relacional aislado (`finance_db` en PostgreSQL/Prisma) adaptado al marco fiscal venezolano.
2. **4 Fases del Roadmap**:
   - **Fase 1**: Cuentas por Pagar (CxP), Motor de Retenciones SENIAT (75%/100% IVA, ISLR) y Propuesta Semanal de Pago (Martes 5:00 PM).
   - **Fase 2**: Egresos, Enrutamiento Bancario Inteligente (BNC vs. Provincial) y Archivos Planos `.TXT`.
   - **Fase 3**: Cuentas por Cobrar (CxC), Conciliación Masiva CSV (Xetux vs. Banco) y Comisiones POS.
   - **Fase 4**: Arqueo Semanal de Caja Chica, Cuota de Marketing (4%) y Dashboard Gerencial.

---

## 🔗 Referencias Cruzadas
- [[Proyecto: MasterHub (MG-HUB)|proyectos/masterhub-mg-hub.md]]
- [[Módulo de Finanzas: Especificación Técnica (finance-ms)|proyectos/masterhub-modulo-finanzas.md]]
- [[Área Finanzas - Gestión Económica|finanzas/pilar-finanzas-personales.md]]
