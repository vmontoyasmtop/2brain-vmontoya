---
title: "Concepto: Guía Completa de Comandos y Atajos de Antigravity CLI"
type: "concept"
area: "programacion"
created: 2026-09-11
updated: 2026-09-18
tags:
  - 
---

# ⚡ Guía Completa de Comandos y Atajos de [[antigravity-cli|Antigravity CLI]]

Esta guía reúne las características avanzadas, comandos slash y mejores prácticas para maximizar el uso de **Antigravity CLI** (`agi`).

---

## 🛠️ Comandos de Inicio y Configuración

- `agi`: Iniciar sesión interactiva en la terminal.
- `agi -c`: Reanudar la última sesión de trabajo guardada.
- `/config`: Cambiar permisos de herramientas (ej. activar *Always proceed* / Modo Yolo) y notificaciones de sonido.

---

## 📋 Comandos Slash Principales

| Comando | Descripción / Uso |
| :--- | :--- |
| `/planning` | Activa el **Modo Planificación**. La IA genera un documento de arquitectura antes de tocar código. |
| `/artifact` | Abre el visualizador interactivo de planes y modificaciones de código. Permite añadir comentarios y correcciones inline. |
| `/btw [pregunta]` | **By The Way**: Hace una pregunta secundaria a la IA mientras esta sigue trabajando en la tarea principal en segundo plano. |
| `/goal [objetivo]` | **Modo Meta**: Lanza un bucle de iteración autónoma continua donde la IA compila, prueba y corrige hasta alcanzar la meta. |
| `/tasks` | Muestra los procesos en ejecución. Presiona `K` para cancelar un proceso o `X` para limpiarlo de la lista. |
| `/skills` | Administra e instala habilidades avanzadas (ej. `frontend-design` de Anthropic). |
| `/agents` | Crea y gestiona subagentes especializados (`research`, `tester`) dentro de la misma sesión. |
| `/model` | Cambia el modelo activo (Gemini 3.5 Flash, Gemini Pro, Claude, GPT open source). |
| `/context` | Muestra el uso visual del búfer de contexto disponible (hasta ~1M tokens). |
| `/usage` | Revisa el consumo de cuota y límites en el plan gratuito/de pago. |
| `/rewind` | Retrocede la sesión de chat y el estado del código a un paso anterior. |
| `/clear` | Limpia el historial de chat para liberar memoria y ahorrar tokens. |

---

## ⌨️ Atajos de Teclado y Modos Rápidos

- `# [comando]` -> **Modo Bash**: Ejecuta comandos de terminal directos sin salir de la sesión (`# git status`, `# dir`).
- `Ctrl + Enter` -> Inserta un **salto de línea** para escribir prompts estructurados multilínea antes de enviar.
- `Flechas Arriba / Abajo` -> Navega por el historial de prompts introducidos anteriormente.
