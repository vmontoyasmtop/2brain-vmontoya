---
title: "Guía de Instalación y Configuración del Servidor MCP para Google Docs (Trabajo y Personal)"
type: "guide"
area: "programacion"
created: 2026-09-16
updated: 2026-09-18
sources: []
tags:
  - 
---

# 📖 Guía de Configuración del Servidor MCP para Google Docs (Multicuenta)

Guía técnica elaborada por **ALFRED** para registrar y habilitar los servidores MCP (Model Context Protocol) de **Google Docs** para cuentas de **Trabajo** (`soporte@mastergroupve.com`) y **Personal** (`vmontoya.smartopsve@gmail.com`).

---

## 📌 1. Descripción & Propósito

El servidor MCP `@node2flow/google-docs-mcp` conecta los agentes de IA (como ALFRED / Antigravity) directamente con Google Docs en la nube, permitiendo:

- **Creación y Edición Colaborativa**: Creación y modificación de documentos en tiempo real sin requerir edición local de archivos Markdown.
- **Formato Enriquecido**: Generación de documentos ejecutivos con títulos, negritas, listas y tablas.
- **Enlace de Compartición Inmediato**: Generación de enlaces web de Google Drive listos para compartir con directivos.

---

## 📂 2. Estructura de Credenciales Multicuenta

Las credenciales OAuth 2.0 y fichas de token se almacenan en carpetas dedicadas en el perfil de usuario (`%USERPROFILE%`):

```text
C:\Users\Animación MKT\
├── .gdocs-trabajo-mcp\       # Credenciales y Token para Google Docs Trabajo
│   ├── credentials.json
│   └── token.json
└── .gdocs-personal-mcp\      # Credenciales y Token para Google Docs Personal
    ├── credentials.json
    └── token.json
```

---

## 🔑 3. Estructura de `credentials.json`

Cada carpeta contiene el archivo `credentials.json` utilizando la estructura OAuth 2.0 Client ID:

```json
{
  "web": {
    "client_id": "<GOOGLE_CLIENT_ID>",
    "client_secret": "<GOOGLE_CLIENT_SECRET>",
    "redirect_uris": [
      "http://localhost:3000/oauth2callback"
    ]
  }
}
```

---

## ⚙️ 4. Configuración en Antigravity (`mcp_config.json`)

Los servidores están registrados en el archivo de configuración global de MCP (`C:\Users\Animación MKT\.gemini\config\mcp_config.json`):

```json
{
  "mcpServers": {
    "google-docs-trabajo": {
      "command": "npx.cmd",
      "args": [
        "-y",
        "@node2flow/google-docs-mcp"
      ],
      "env": {
        "NODE_TLS_REJECT_UNAUTHORIZED": "1",
        "GOOGLE_CLIENT_ID": "<GOOGLE_CLIENT_ID>",
        "GOOGLE_CLIENT_SECRET": "<GOOGLE_CLIENT_SECRET>",
        "GOOGLE_CREDENTIALS_PATH": "C:\\Users\\Animación MKT\\.gdocs-trabajo-mcp\\credentials.json",
        "GOOGLE_TOKEN_PATH": "C:\\Users\\Animación MKT\\.gdocs-trabajo-mcp\\token.json"
      }
    },
    "google-docs-personal": {
      "command": "npx.cmd",
      "args": [
        "-y",
        "@node2flow/google-docs-mcp"
      ],
      "env": {
        "NODE_TLS_REJECT_UNAUTHORIZED": "1",
        "GOOGLE_CLIENT_ID": "<GOOGLE_CLIENT_ID>",
        "GOOGLE_CLIENT_SECRET": "<GOOGLE_CLIENT_SECRET>",
        "GOOGLE_CREDENTIALS_PATH": "C:\\Users\\Animación MKT\\.gdocs-personal-mcp\\credentials.json",
        "GOOGLE_TOKEN_PATH": "C:\\Users\\Animación MKT\\.gdocs-personal-mcp\\token.json"
      }
    }
  }
}
```
