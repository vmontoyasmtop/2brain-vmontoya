---
title: "Guía de Instalación y Configuración del Servidor MCP para GitHub"
type: "guide"
area: "programacion"
created: 2026-09-19
updated: 2026-09-19
sources: []
tags:
  - mcp
  - github
  - antigravity
  - devops
  - tools
---

# 📖 Guía de Configuración del Servidor MCP para GitHub (`github-personal`)

Guía técnica elaborada por **ALFRED** para registrar y habilitar el servidor MCP (Model Context Protocol) oficial de **GitHub** (`@modelcontextprotocol/server-github`) en la cuenta personal del usuario (`vmontoya.smartopsve@gmail.com` / `vmontoyasmtop`).

---

## 📌 1. Descripción & Propósito

El servidor MCP `@modelcontextprotocol/server-github` conecta los agentes de IA (como ALFRED / Antigravity) directamente con la API de GitHub, permitiendo:

- **Inspección de Repositorios**: Búsqueda y lectura de código fuente, estructuras de carpetas, ramas y commits en tiempo real.
- **Edición Remota Autónomas**: Creación y modificación de archivos sin requerir clonación local previa.
- **Gestión de PRs e Issues**: Lectura, creación y actualización de Pull Requests, Issues y proyectos de GitHub.
- **Integración con Subagentes**: Permite a los subagentes desarrolladores (Backend, Frontend) inspeccionar repositorios remotos autónomamente.

---

## 🔑 2. Requisitos & Autenticación (Personal Access Token)

La autenticación utiliza un **Personal Access Token (PAT Classic)** generado en GitHub:

1. **Ubicación en GitHub**: `https://github.com/settings/tokens`
2. **Permisos del Token**:
   - `repo` (Acceso completo a repositorios públicos y privados)
   - `workflow` (Ver y desencadenar flujos de trabajo)
   - `read:org` / `user` (Lectura de organización y perfil)
   - `project` (Gestión de tableros de proyectos)
3. **Variable de Entorno**: `GITHUB_PERSONAL_ACCESS_TOKEN` / `GITHUB_TOKEN`.

---

## ⚙️ 3. Configuración en Antigravity (`mcp_config.json`)

El servidor se encuentra registrado en el archivo de configuración global de MCP (`C:\Users\vmontoyaMG\.gemini\config\mcp_config.json`):

```json
{
  "mcpServers": {
    "github-personal": {
      "command": "npx.cmd",
      "args": [
        "-y",
        "@modelcontextprotocol/server-github"
      ],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_************************************",
        "GITHUB_TOKEN": "ghp_************************************"
      }
    }
  }
}
```

---

## 🛠️ 4. Herramientas MCP Expuestas

| Herramienta MCP | Descripción |
| :--- | :--- |
| `github_search_repositories` | Buscar repositorios por nombre, lenguaje o temas. |
| `github_get_file_contents` | Obtener el contenido exacto de un archivo remoto en una rama. |
| `github_create_or_update_file` | Crear o modificar un archivo remoto y hacer commit directo. |
| `github_list_issues` | Listar y filtrar incidencias activas en repositorios. |
| `github_create_issue` | Reportar o crear un nuevo Issue. |
| `github_list_pull_requests` | Consultar Pull Requests y revisiones de código. |
| `github_create_pull_request` | Crear una nueva solicitud de extracción (PR). |

---

## 🔗 Notas Relacionadas
- [[pilar-programacion|Pilar del Área de Programación]]
- [[guia-configuracion-mcp-google-docs|Guía Servidor MCP Google Docs]]
- [[guia-configuracion-mcp-google-calendar-gmail|Guía Servidor MCP Google Calendar & Gmail]]
