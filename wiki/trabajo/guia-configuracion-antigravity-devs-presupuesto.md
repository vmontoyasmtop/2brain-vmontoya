---
title: "Manual Operativo: Configuración de Antigravity para Equipos con Límite de Presupuesto ($4.99 USD/dev)"
type: "guide"
area: "trabajo"
project: "MasterGroup"
created: 2026-09-18
updated: 2026-09-18
tags:
  - antigravity
  - gemini-api
  - ai-studio
  - presupuesto
  - control-costos
  - onboarding-devs
---

# 📋 Manual Operativo: Configuración de Antigravity para Equipos ($4.99 USD/dev)

*Guía paso a paso para dar de alta desarrolladores en Google AI Studio / Google Cloud con límite de cobro estricto ($4.99/mes), uso paralelo de Antigravity CLI + IDE y monitoreo centralizado.*

---

## 🎯 1. Estructura del Modelo

- **Límite Financiero Máximo**: $4.99 USD por desarrollador al mes (Corte automático, sin cobros adicionales).
- **Herramientas Habilitadas Simultáneamente**: Antigravity CLI (`agy`) + Antigravity Extension / IDE.
- **Control & Auditoría**: Panel unificado de facturación para el Administrador (**Señor Montoya**).

---

## 🚀 PASO 1: Configurar la Cuenta Administradora Matriz & Facturación

1. Acceder a **[Google Cloud Console Billing](https://console.cloud.google.com/billing)** o **[Google AI Studio](https://aistudio.google.com/)** con la cuenta corporativa principal (`soporte@mastergroupve.com`).
2. Vincular la tarjeta corporativa de MasterGroup en el perfil de facturación.
3. Crear un proyecto matriz de desarrollo denominado: **`MasterGroup-Antigravity-AI`**.

---

## 🛡️ PASO 2: Configurar el Límite Estricto de Presupuesto ($4.99 USD/dev)

1. En la consola de Google Cloud, ir al menú desplegable ➔ **Facturación (Billing)** ➔ **Presupuestos y alertas (Budgets & alerts)**.
2. Hacer clic en **`Crear Presupuesto` (Create Budget)**.
3. **Nombre del Presupuesto**: `Presupuesto Dev - [Nombre del Desarrollador]`.
4. **Importe**: Seleccionar *Importe especificado* e ingresar **`4.99`** (USD).
5. **Alertas de Presupuesto**:
   - 50% ($2.50 USD) ➔ Notificación por correo al Administrador.
   - 80% ($4.00 USD) ➔ Notificación por correo al Administrador.
   - 100% ($4.99 USD) ➔ Notificación crítica por correo + Desactivación automática de cobros adicionales.

---

## 🔑 PASO 3: Generar y Asignar API Key para el Desarrollador

1. Ingresar a **[Google AI Studio - API Keys](https://aistudio.google.com/app/apikey)**.
2. Hacer clic en **`Create API key`**.
3. Seleccionar el proyecto corporativo `MasterGroup-Antigravity-AI`.
4. Asignar un alias identificador (ej. `API_KEY_DEV_PEDRO`).
5. Copiar la clave generada (`AIzaSy...`).

---

## 💻 PASO 4: Configuración en la Computadora del Desarrollador (CLI + IDE)

En la estación de trabajo del desarrollador, ejecutar los siguientes comandos para configurar el consumo de **Antigravity CLI** e **IDE** al mismo tiempo:

### A. En Windows (PowerShell):
```powershell
# 1. Configurar la clave de API como variable de entorno permanente
[System.Environment]::SetEnvironmentVariable('GEMINI_API_KEY', 'CLAVE_API_DEL_DEV_AQUI', 'User')

# 2. Verificar que la clave esté activa
$env:GEMINI_API_KEY
```

### B. En Linux / macOS (Terminal):
```bash
# 1. Guardar la variable en el perfil del usuario
echo 'export GEMINI_API_KEY="CLAVE_API_DEL_DEV_AQUI"' >> ~/.bashrc
source ~/.bashrc
```

### C. Uso Simultáneo (CLI + IDE):
- **Antigravity CLI**: Abrir la consola y ejecutar `agy` o los comandos agénticos. La CLI detectará automáticamente `GEMINI_API_KEY`.
- **Antigravity IDE / VS Code**: Instalar la extensión de Antigravity o usar el chat del IDE; consumirá la misma API Key compartida en segundo plano sin entrar en conflicto.

---

## 📊 PASO 5: Monitoreo Centralizado de Consumos (Para Señor Montoya)

Para revisar el gasto y volumen de uso de todos los miembros del equipo:

1. **Dashboard de Gastos ($)**:
   - Ir a [Google Cloud Billing Overview](https://console.cloud.google.com/billing).
   - Filtrar por desarrollador/proyecto para ver la gráfica de consumo diario en USD.
2. **Dashboard de Tokens & Métricas**:
   - Ir a [Google AI Studio Plan & Quotas](https://aistudio.google.com/app/plan_information).
   - Visualizar llamadas por minuto (RPM), solicitudes diarias (RPD) y consumo acumulado por clave de API.
