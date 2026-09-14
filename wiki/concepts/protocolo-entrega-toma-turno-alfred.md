---
title: "Protocolo de Entrega y Toma de Turno de ALFRED (Sincronización Multi-PC)"
type: "concept"
area: "programacion"
created: 2026-09-14
updated: 2026-09-14
sources:
  - "AGENTS.md"
tags:
  - alfred
  - 2brain
  - handover
  - git
  - sync
  - multi-pc
---

# 🔄 Protocolo de Entrega y Toma de Turno (Multi-PC Context Sync)

Mecanismo oficial de **ALFRED** para mantener continuidad absoluta de contexto, tareas y decisiones entre la **PC de Trabajo** y la **PC de Casa**.

---

## 1. 🌆 Protocolo "Entrega de Turno" (`ENTREGA_TURNO`)

**Comando del Usuario**: `"ALFRED, entrega de turno"` o `"Cierra la jornada"`

### Secuencia de Ejecución de ALFRED:
1. **Registro de Log**: Escribir en [`wiki/log.md`](file:///C:/Users/vmontoyaMG/Desktop/2brain/wiki/log.md) un resumen ejecutivo de lo completado en el día (tareas de ClickUp cerradas, eventos atendidos, código desarrollado o sermones avanzados).
2. **Actualización de Dashboard**: Actualizar [`wiki/life-dashboard.md`](file:///C:/Users/vmontoyaMG/Desktop/2brain/wiki/life-dashboard.md) moviendo tareas activas y fijando los focos pendientes para la siguiente jornada.
3. **Persistencia Git**:
   ```bash
   git add .
   git commit -m "chore(handover): cierre de turno [YYYY-MM-DD]"
   git push origin master
   ```
4. **Despedida**: Presentar un resumen conciso de 3 puntos del estado final.

---

## 2. 🌅 Protocolo "Toma de Turno" (`TOMA_TURNO`)

**Comando del Usuario**: `"ALFRED, toma de turno"` o `"Inicia la jornada"`

### Secuencia de Ejecución de ALFRED:
1. **Sincronización Git**:
   ```bash
   git pull origin master
   ```
2. **Lectura de Memoria**: Leer las últimas entradas de [`wiki/log.md`](file:///C:/Users/vmontoyaMG/Desktop/2brain/wiki/log.md) y [`wiki/life-dashboard.md`](file:///C:/Users/vmontoyaMG/Desktop/2brain/wiki/life-dashboard.md).
3. **Consulta de Nube**: Consultar Google Calendar (eventos de hoy) y ClickUp (sprints activos).
4. **Informe de Bienvenida**:
   * *Resumen de dónde quedamos en el último turno.*
   * *Agenda del día actual.*
   * *Próximo bloque de enfoque recomendado.*

---

## 🔗 Referencias Cruzadas
- [[Guía de Empaquetado y Despliegue Rápido de ALFRED & 2brain en Cualquier PC|programacion/guia-despliegue-empaquetado-alfred-2brain.md]]
- [[Dashboard de Vida & Centro de Control|life-dashboard.md]]
- [[AGENTS.md|../AGENTS.md]]
