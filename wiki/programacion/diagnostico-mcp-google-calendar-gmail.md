---
title: "Diagnóstico y Solución de Servidores MCP (Google Calendar & Gmail)"
type: "guide"
area: "programacion"
created: 2026-09-12
updated: 2026-09-18
sources: []
tags:
  - 
---

# 🛠️ Diagnóstico y Solución de Servidores MCP (Google Calendar & Gmail)

Documentación técnica generada por **ALFRED** para resolver el error de inicialización de los servidores MCP de Google en **Antigravity**.

---

## ✅ Estado de los Servidores MCP (100% OPERATIVOS)

Todos los 4 servidores MCP configurados en `C:\Users\vmontoyaMG\.gemini\config\mcp_config.json` han sido autenticados, probados y verificados exitosamente:

1. **`gmail-trabajo` & `gmail-personal` (`mcp-server-gmail`)**:
   - **Estado**: ✅ COMPLETADO
   - **Fichas**: `C:\Users\vmontoyaMG\.gmail-mcp\credentials.json` y `token.json`.

2. **`google-calendar-trabajo` (`mcp-server-google-calendar`)**:
   - **Estado**: ✅ COMPLETADO
   - **Fichas**: `C:\Users\vmontoyaMG\.gcal-trabajo-mcp\credentials.json` y `token.json` (Puerto 3000).

3. **`google-calendar-personal` (`mcp-server-google-calendar`)**:
   - **Estado**: ✅ COMPLETADO
   - **Fichas**: `C:\Users\vmontoyaMG\.gcal-personal-mcp\credentials.json` y `token.json` (Puerto 3001).

---

## 🛠️ Correcciones Técnicas Aplicadas por ALFRED

- **Parche de Decodificación node-fetch / Node 24**: Se configuró `NODE_TLS_REJECT_UNAUTHORIZED=1` y se ajustó la cabecera `Accept-Encoding: identity` en `node-fetch` para evitar errores `ERR_STREAM_PREMATURE_CLOSE` durante la recepción de tokens OAuth.
- **Aislamiento Multicuenta**: Se crearon directorios de credenciales y tokens independientes (`.gcal-trabajo-mcp` y `.gcal-personal-mcp`) para permitir el funcionamiento paralelo sin colisión de sesiones.
- **Client ID Verificado**: Se configuró el Client ID principal sin restricciones de usuarios de prueba para garantizar acceso transparente a ambas cuentas.
