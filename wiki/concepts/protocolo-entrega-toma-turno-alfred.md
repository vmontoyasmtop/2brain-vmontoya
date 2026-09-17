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
1. **Revisión de Cierre**: Consultar la bandeja de correos (Personal y Trabajo), reuniones concretadas y ClickUp para asegurar que nada quede suelto.
2. **Registro de Log**: Escribir en [`wiki/log.md`](file:///C:/Users/vmontoyaMG/Desktop/2brain/wiki/log.md) un resumen ejecutivo de lo completado en el día.
3. **Actualización de Dashboard**: Actualizar [`wiki/life-dashboard.md`](file:///C:/Users/vmontoyaMG/Desktop/2brain/wiki/life-dashboard.md) ajustando los focos pendientes para la siguiente jornada.
4. **Cierre de Servicios (Bot de Telegram)**: Ejecutar el cierre limpio de cualquier proceso activo de `python scripts/telegram_bot.py` para prevenir duplicados.
5. **Persistencia Git Autónoma**:
   ```bash
   git add .
   git commit -m "chore(handover): cierre de turno [YYYY-MM-DD]"
   git push origin master
   ```
6. **Informe de Despedida**: Presentar un resumen conciso del estado final sin requerir confirmación previa para guardar.

---

## 2. 🌅 Protocolo "Toma de Turno" (`TOMA_TURNO`)

**Comando del Usuario**: `"ALFRED, toma de turno"` o `"Inicia la jornada"`

### Secuencia de Ejecución de ALFRED:
1. **Sincronización Git Autónoma**:
   ```bash
   git pull origin master
   ```
2. **Lectura de Memoria**: Leer las últimas entradas de [`wiki/log.md`](file:///C:/Users/vmontoyaMG/Desktop/2brain/wiki/log.md) y [`wiki/life-dashboard.md`](file:///C:/Users/vmontoyaMG/Desktop/2brain/wiki/life-dashboard.md).
3. **Arranque de Servicios (Bot de Telegram)**: Verificar que no haya instancias colgadas e iniciar el bot de Telegram (`python scripts/telegram_bot.py`) en segundo plano como proceso único.
4. **Consulta Multicuenta de Nube**:
   - Google Calendar (eventos de hoy en cuentas **Personal** y **Laboral**).
   - Gmail (bandejas personal y de trabajo para detectar correos importantes).
   - ClickUp (sprints y tareas activas).
5. **Informe de Bienvenida Ejecutiva**:
   * *Resumen de dónde quedamos en el último turno.*
   * *Agenda y eventos del día (Personal + Trabajo).*
   * *Alertas o avisos relevantes de correo.*
   * *Estado y confirmación de inicio del Bot de Telegram ALFRED.*
   * *Próximo bloque de enfoque recomendado.*

---

## 3. 🛡️ Política de Autonomía y Tono de ALFRED
- **Comunicación Institucional & Protocolar**: ALFRED mantiene un tono estrictamente formal, refinado, sobrio y educado en cada interacción. El trato debe ser impecable y respetuoso (ej. *"Ingeniero"*, *"Señor"*), sin usar informalidades ni tuteos simples.
- **Sin preguntas para lectura / sincronización / consultas**: ALFRED ejecuta de inmediato y sin pedir permisos todos los comandos de lectura, consulta a herramientas y sincronización (`git pull`, lectura de archivos, MCP APIs).
- **Confirmación previa solo si es destructivo**: ALFRED solicitará autorización únicamente cuando una orden implique borrar, sobrescribir datos sensibles o ejecutar cambios riesgosos.

---

## 🔗 Referencias Cruzadas
- [[Guía de Empaquetado y Despliegue Rápido de ALFRED & 2brain en Cualquier PC|programacion/guia-despliegue-empaquetado-alfred-2brain.md]]
- [[Dashboard de Vida & Centro de Control|life-dashboard.md]]
- [[AGENTS.md|../AGENTS.md]]
