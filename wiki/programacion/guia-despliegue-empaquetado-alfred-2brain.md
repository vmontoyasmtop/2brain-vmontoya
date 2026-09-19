---
title: "Guía de Empaquetado y Despliegue Rápido de ALFRED & 2brain en Cualquier PC"
type: "guide"
area: "programacion"
created: 2026-09-14
updated: 2026-09-18
tags:
  - 
---

# 📦 Guía de Empaquetado y Despliegue Rápido y Seguro: ALFRED & 2brain

Guía para empaquetar y clonar el asistente **ALFRED** junto a todo el conocimiento de **2brain** en cualquier computadora de forma **100% segura**, **sin exponer claves ni tokens privados en Git**.

---

## 🔒 Arquitectura de Seguridad (Cero Fugas de Claves)

* `.gitignore` ignora automáticamente todos los archivos `.env`, `.env.local`, `credentials.json` y `token.json`.
* El script [`scripts/setup-alfred-2brain.ps1`](file:///C:/Users/vmontoyaMG/Desktop/2brain/scripts/setup-alfred-2brain.ps1) **no contiene ninguna clave quemada o hardcodeada**.
* Las claves se leen de forma aislada desde `scripts/.env.local` (el cual creas en la máquina destino copiando `scripts/.env.template`) o se solicitan interactivamente la primera vez.

---

## ⚡ Procedimiento de Despliegue en 3 Pasos

### Paso 1: Clonar el Repositorio `2brain`
En la nueva PC (en la carpeta Escritorio):
```powershell
cd C:\Users\<Su_Usuario>\Desktop
git clone https://github.com/tu-usuario/2brain.git
cd 2brain
```

### Paso 2: Crear el archivo de credenciales local (No rastreado por Git)
Copia la plantilla `.env.template` como `.env.local`:
```powershell
Copy-Item .\scripts\.env.template .\scripts\.env.local
```
Edita `scripts/.env.local` y pega tus tokens de ClickUp (`CLICKUP_PERSONAL_TOKEN` y `CLICKUP_TRABAJO_TOKEN`).

### Paso 3: Ejecutar el Script de Auto-Configuración
Ejecuta el script PowerShell de auto-instalación:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\setup-alfred-2brain.ps1
```

---

## 🛠️ Los 6 Servidores MCP Configurados Automáticamente

| Servidor MCP | Función | Cuenta Vinculada | Tipo de Credencial |
| :--- | :--- | :--- | :--- |
| **`clickup-personal`** | Gestión de tareas y proyectos personales | `SmartOpsVE` | Personal API Token |
| **`clickup-trabajo`** | Gestión de tareas y sprints corporativos | `Mastergroupve` | Personal API Token |
| **`google-calendar-trabajo`** | Agenda laboral y time-blocking IT | `soporte@mastergroupve.com` | OAuth 2.0 |
| **`google-calendar-personal`** | Agenda personal y ministerial | `vmontoya.smartopsve@gmail.com` | OAuth 2.0 |
| **`gmail-trabajo`** | Correos corporativos y reportes sucursales | `soporte@mastergroupve.com` | OAuth 2.0 |
| **`gmail-personal`** | Correos personales y notificaciones | `vmontoya.smartopsve@gmail.com` | OAuth 2.0 |

---

## 🔗 Referencias Cruzadas
- [[guia-configuracion-mcp-google-calendar-gmail|Guía de Instalación y Configuración de Servidores MCP (Google Calendar & Gmail Multicuenta)]]
- [[llm-wiki-pattern|LLM Wiki Pattern]]: Modelo de wiki persistente.
- [[life-dashboard|Dashboard de Vida & Centro de Control]]
