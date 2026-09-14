---
title: "Guía de Instalación y Configuración de Servidores MCP (Google Calendar & Gmail Multicuenta)"
type: "concept"
area: "programacion"
created: 2026-09-13
updated: 2026-09-13
sources: []
tags:
  - mcp
  - google-calendar
  - gmail
  - antigravity
  - configuracion
  - guia
  - oauth
---

# 📖 Guía Completa: Configuración de Servidores MCP para Google Calendar y Gmail (Multicuenta)

Guía técnica creada por **ALFRED** para instalar, configurar y autenticar los servidores MCP (Model Context Protocol) de Google Calendar y Gmail en **Antigravity** o cualquier cliente MCP en equipos nuevos.

---

## 📌 1. Requisitos Previos

- **Node.js** (v18 o superior) y **npm / npx** instalados en el sistema.
- Acceso a un **Client ID** y **Client Secret** de OAuth 2.0 en Google Cloud Console (con las APIs de **Gmail API** y **Google Calendar API** habilitadas).

---

## 📂 2. Estructura de Directorios Independientes (Multicuenta)

Para evitar que las cuentas Laboral y Personal sobreescriban sus fichas de acceso (`token.json`), cree las siguientes carpetas en el directorio raíz del usuario (`%USERPROFILE%` / `~`):

```text
C:\Users\<usuario>\
├── .gmail-mcp\               # Credenciales y Token para Gmail
├── .gcal-trabajo-mcp\        # Credenciales y Token para Calendar Trabajo (Puerto 3000)
└── .gcal-personal-mcp\       # Credenciales y Token para Calendar Personal (Puerto 3001)
```

---

## 🔑 3. Formato del Archivo `credentials.json`

En cada una de las carpetas anteriores, cree un archivo `credentials.json`. 

> [!IMPORTANT]
> Es fundamental utilizar la clave `"web"` (en lugar de `"installed"`) para garantizar que la librería de autenticación `@google-cloud/local-auth` abra un puerto HTTP fijo (`3000` o `3001`) en lugar de un puerto dinámico aleatorio.

### Ejemplo para Trabajo (`C:\Users\<usuario>\.gcal-trabajo-mcp\credentials.json`):
```json
{
  "web": {
    "client_id": "<TU_CLIENT_ID>.apps.googleusercontent.com",
    "client_secret": "<TU_CLIENT_SECRET>",
    "redirect_uris": [
      "http://localhost:3000/oauth2callback"
    ]
  }
}
```

### Ejemplo para Personal (`C:\Users\<usuario>\.gcal-personal-mcp\credentials.json`):
```json
{
  "web": {
    "client_id": "<TU_CLIENT_ID>.apps.googleusercontent.com",
    "client_secret": "<TU_CLIENT_SECRET>",
    "redirect_uris": [
      "http://localhost:3001/oauth2callback"
    ]
  }
}
```

---

## ⚙️ 4. Configuración Global en Antigravity (`mcp_config.json`)

Edite o cree el archivo de configuración global de MCP en Antigravity (`C:\Users\<usuario>\.gemini\config\mcp_config.json`):

```json
{
  "mcpServers": {
    "google-calendar-trabajo": {
      "command": "npx.cmd",
      "args": [
        "-y",
        "mcp-server-google-calendar",
        "run"
      ],
      "env": {
        "NODE_TLS_REJECT_UNAUTHORIZED": "1",
        "GOOGLE_CLIENT_ID": "<CLIENT_ID_TRABAJO>",
        "GOOGLE_CLIENT_SECRET": "<CLIENT_SECRET_TRABAJO>",
        "GOOGLE_REDIRECT_URI": "http://localhost:3000/oauth2callback",
        "GOOGLE_CREDENTIALS_PATH": "C:\\Users\\<usuario>\\.gcal-trabajo-mcp\\credentials.json",
        "GOOGLE_TOKEN_PATH": "C:\\Users\\<usuario>\\.gcal-trabajo-mcp\\token.json"
      }
    },
    "google-calendar-personal": {
      "command": "npx.cmd",
      "args": [
        "-y",
        "mcp-server-google-calendar",
        "run"
      ],
      "env": {
        "NODE_TLS_REJECT_UNAUTHORIZED": "1",
        "GOOGLE_CLIENT_ID": "<CLIENT_ID_PERSONAL_O_VERIFICADO>",
        "GOOGLE_CLIENT_SECRET": "<CLIENT_SECRET>",
        "GOOGLE_REDIRECT_URI": "http://localhost:3001/oauth2callback",
        "GOOGLE_CREDENTIALS_PATH": "C:\\Users\\<usuario>\\.gcal-personal-mcp\\credentials.json",
        "GOOGLE_TOKEN_PATH": "C:\\Users\\<usuario>\\.gcal-personal-mcp\\token.json"
      }
    },
    "gmail-trabajo": {
      "command": "npx.cmd",
      "args": [
        "-y",
        "mcp-server-gmail"
      ],
      "env": {
        "NODE_TLS_REJECT_UNAUTHORIZED": "1",
        "GOOGLE_CLIENT_ID": "<CLIENT_ID_TRABAJO>",
        "GOOGLE_CLIENT_SECRET": "<CLIENT_SECRET_TRABAJO>"
      }
    },
    "gmail-personal": {
      "command": "npx.cmd",
      "args": [
        "-y",
        "mcp-server-gmail"
      ],
      "env": {
        "NODE_TLS_REJECT_UNAUTHORIZED": "1",
        "GOOGLE_CLIENT_ID": "<CLIENT_ID_PERSONAL>",
        "GOOGLE_CLIENT_SECRET": "<CLIENT_SECRET_PERSONAL>"
      }
    }
  }
}
```

---

## 🚀 5. Flujo de Primera Autenticación Interactivas

Para generar los archivos de fichas de sesión (`token.json`) por primera vez en un equipo nuevo:

1. **Autenticar Gmail**:
   Ejecute en la terminal interactiva:
   ```powershell
   npx -y mcp-server-gmail
   ```
   *Se abrirá el navegador para seleccionar la cuenta y aprobar permisos.*

2. **Autenticar Google Calendar (Trabajo)**:
   ```powershell
   cmd /c "set NODE_TLS_REJECT_UNAUTHORIZED=1&& set GOOGLE_CLIENT_ID=<CLIENT_ID>&& set GOOGLE_CLIENT_SECRET=<SECRET>&& set GOOGLE_REDIRECT_URI=http://localhost:3000/oauth2callback&& set GOOGLE_CREDENTIALS_PATH=C:\Users\<usuario>\.gcal-trabajo-mcp\credentials.json&& set GOOGLE_TOKEN_PATH=C:\Users\<usuario>\.gcal-trabajo-mcp\token.json&& npx -y mcp-server-google-calendar run"
   ```

3. **Autenticar Google Calendar (Personal)**:
   ```powershell
   cmd /c "set NODE_TLS_REJECT_UNAUTHORIZED=1&& set GOOGLE_CLIENT_ID=<CLIENT_ID>&& set GOOGLE_CLIENT_SECRET=<SECRET>&& set GOOGLE_REDIRECT_URI=http://localhost:3001/oauth2callback&& set GOOGLE_CREDENTIALS_PATH=C:\Users\<usuario>\.gcal-personal-mcp\credentials.json&& set GOOGLE_TOKEN_PATH=C:\Users\<usuario>\.gcal-personal-mcp\token.json&& npx -y mcp-server-google-calendar run"
   ```

---

## 🛠️ 6. Solución de Problemas Frecuentes (Troubleshooting)

| Error Observado | Causa | Solución |
| :--- | :--- | :--- |
| `ERR_CONNECTION_REFUSED` | La credencial usaba `"installed"` en lugar de `"web"`, lo que provocaba apertura de puertos aleatorios dinámicos. | Cambiar la raíz del JSON de credenciales a `"web"` para forzar el uso del puerto definido en `redirect_uris`. |
| `ERR_STREAM_PREMATURE_CLOSE` | Incompatibilidad del descompresor `gzip`/`zlib` en Node.js 24 al recibir la respuesta de token. | Definir la variable de entorno `"NODE_TLS_REJECT_UNAUTHORIZED": "1"` en la llamada o parchear `node-fetch` a `Accept-Encoding: identity`. |
| `Error 403: access_denied` | La app de Google Cloud está en modo *"Testing"* y la cuenta no está registrada en *Test Users*. | Utilizar un Client ID de un proyecto verificado/en producción o agregar el email bajo la pestaña *Test Users* en GCP Console. |
