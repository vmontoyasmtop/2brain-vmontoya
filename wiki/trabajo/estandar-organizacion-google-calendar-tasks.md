---
title: "Estándar de Organización de Calendario Laboral (Focus Time & Google Tasks)"
type: "concept"
area: "trabajo"
created: 2026-09-15
updated: 2026-09-15
sources: []
tags:
  - calendar
  - google-tasks
  - focus-time
  - productividad
  - xetux
  - mastergroup
---

# 📅 Estándar Operativo: Organización de Calendario Laboral IT (Xetux / MasterGroup)

Modelo de administración del tiempo para equilibrar el rol de **Analista / Soporte IT** (reactivo) y **Desarrollador de Software / MasterHub** (proactivo/Deep Work) mediante las funciones avanzadas de Google Workspace.

---

## 🎯 1. Tipos de Bloques en el Calendario de Trabajo (`soporte@mastergroupve.com`)

| Tipo en Calendar | Nombre / Formato | Propósito Operativo | Comportamiento en Google Workspace |
| :--- | :--- | :--- | :--- |
| 🛡️ **Focus Time** | `🛡️ [Focus Time] Dev MasterHub` | Desarrollo de software ininterrumpido (Madrugada / Mañana / Tarde). | Auto-rechaza invitaciones a reuniones no programadas. Muestra estado de concentración en Chat/Meet. |
| 🤝 **Evento Standard** | `MKT / Ventas / RRHH Updates` | Reuniones de sincronización presenciales o por Google Meet. | Permite adjuntos de Drive, enlace de Meet y lista de asistentes con RSVP. |
| ⚡ **Bloque Reactivo** | `⚡ [Bloque Reactivo] Soporte Xetux` | Ventana de ráfaga para atender llamadas, tickets de Helpdesk y sucursales. | Permite interrupciones y soporte técnico a usuarios. |
| ☑️ **Google Task** | `Actualizar tasa BCV` / `Ticket #104` | Micro-acciones puntuales con hora exacta o fecha límite. | Aparecen en el panel lateral de Gmail/Calendar. Al completarse se tachan; si se vencen, se trasladan solas. |
| 📍 **Working Location**| `Oficina (Caracas Campus)` | Informar la presencia física (Oficina vs Remoto). | Visible en el perfil de Workspace para coordinar visitas presenciales. |

---

## 🔄 2. Flujo de Trabajo Diario con ALFRED

```mermaid
flowchart TD
    A["🌅 TOMA DE TURNO"] --> B["1. ALFRED lee Google Calendar + Tasks + ClickUp"]
    B --> C["2. Presenta Informe Ejecutado por Categoría: Reuniones | Focus Time | Tasks"]
    C --> D["💻 DURANTE LA JORNADA"]
    D --> E["3. Ajustes al vuelo vía ALFRED ('Mueve el Focus Time a las 14:00', 'Agrega esta Task a las 11:00')"]
    E --> F["🌆 ENTREGA DE TURNO"]
    F --> G["4. Verificación de Tasks completadas + Registro en log.md + Sync Git"]
```

---

## 🛠️ 3. Reglas Operativas de Convivencia

1. **Cortafuegos de Focus Time**: Los bloques de Focus Time son sagrados. ALFRED no agendará compromisos de menor prioridad dentro de un bloque de Focus Time a menos que haya una urgencia crítica de producción (Caja / Sistema caído).
2. **Regla de Micro-tareas (<15 min)**: Cualquier pendiente que tome menos de 15 minutos se registra como **Google Task**, no como un evento de calendario.
3. **Notificaciones y Recordatorios**:
   - Eventos de reunión: Alerta a los 10 minutos prevíos.
   - Tasks: Notificación emergente a la hora fijada.
