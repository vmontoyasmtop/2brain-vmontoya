---
title: "Resumen: Google Lanzó Antigravity CLI y Es Brutal (por Fazt Code)"
type: "summary"
area: "programacion"
created: 2026-09-11
updated: 2026-09-18
tags:
  - 
---

# 📄 Resumen: Google Lanzó Antigravity CLI y Es Brutal

- **Fuente Original**: `raw/Google Lanzó Antigravity CLI y Es Brutal.md`
- **Autor / Creador**: [[fazt-code|Fazt Code]]
- **Herramienta Evaluada**: [[antigravity-cli|Antigravity CLI]]
- **Concepto Relacionado**: [[antigravity-commands-and-shortcuts|Antigravity Commands and Shortcuts]]

---

## 💡 Puntos Clave y Funcionalidades Destacadas

1. **Arquitectura y Rendimiento**:
   - Reescrito desde cero en **Go** (ultrarrápido, rendimiento nativo).
   - Comando ejecutable abreviado: `agi`.
   - Soporta modelos de Google (Gemini 3.5 Flash gratuito, Gemini Pro) y modelos externos/open source.

2. **Comandos Útiles y Gestión de Contexto**:
   - `agi -c`: Reanudar sesiones anteriores de trabajo.
   - `/planning`: Modo de planificación detallada antes de ejecutar cambios grandes.
   - `/artifact`: Historial visual interactivo de planes y modificaciones realizadas.
   - `/btw` (By The Way): Hacer preguntas secundarias a la IA sin interrumpir la tarea que está ejecutando en segundo plano.
   - `#` (Modo Bash): Ejecutar comandos de terminal directos (`# git status`, `# echo`).
   - `Ctrl + Enter`: Escribir prompts multilínea cómodamente.
   - `/rewind`: Retroceder la sesión e historial a un estado anterior.
   - `/tasks`: Ver, gestionar y cancelar procesos en ejecución (`K` para kill, `X` para limpiar).
   - `/context`: Visualización gráfica de tokens y contexto disponible (cerca de 1M tokens).
   - `/goal`: Modo de iteración autónoma continua (la IA prueba y reintenta hasta cumplir el objetivo).
   - `/skills`: Cargar y gestionar habilidades (ej. `frontend-design` de Anthropic).
   - `/agents`: Crear y ejecutar subagentes en paralelo dentro de la misma sesión (`research`, `tester`).
