---
title: "Bot de Telegram: ALFRED VM (@AlfredVM_bot)"
type: "concept"
area: "programacion"
created: 2026-09-16
updated: 2026-09-16
tags:
  - alfred
  - telegram
  - bot
  - gemini-api
  - 2brain
  - automatizacion
---

# 🤖 Bot de Telegram: ALFRED VM (@AlfredVM_bot)

*Interfaz de chat en vivo e ingesta de datos a 2brain desde Telegram, impulsada por Gemini 3.6 Flash.*

---

## 🎯 Descripción General

El **Bot de Telegram ALFRED VM** ([@AlfredVM_bot](https://t.me/AlfredVM_bot)) permite al usuario interactuar de forma inmediata con ALFRED desde su teléfono móvil o cliente de escritorio de Telegram a costo **$0 USD**.

### Características Principales:
1. **💬 Conversación en Vivo 24/7**: Respuestas ejecutivas con la personalidad de ALFRED, alimentadas por la API de `gemini-3.6-flash` y el contexto actualizado del `life-dashboard.md`.
2. **🎙️ Procesamiento Nativo de Notas de Voz & Audio Multimodal**: ALFRED escucha directamente notas de voz enviadas por Telegram (`voice`/`audio`), guarda un respaldo en `raw/inbox/voice_YYYYMMDD_HHMMSS.ogg` y responde procesando el audio en tiempo real con Gemini 3.6 Flash.
3. **📥 Ingesta Directa a 2brain**: Guardado automático de enlaces (YouTube, NotebookLM, artículos) y archivos adjuntos (PDFs, notas de voz, imágenes) en `raw/inbox/`.
4. **🛠️ Gestión de Helpdesk**: Consulta y creación de tickets de soporte técnico en **MasterHub** mediante comandos reducidos.

---

## ⚙️ Arquitectura & Configuración

El script principal se encuentra ubicado en `scripts/telegram_bot.py`.

### 🔑 Credenciales (`scripts/.env`)
```env
TELEGRAM_BOT_TOKEN=8475383662:AAEAWeXq5jqT1noKU7k85AnIBjVcWzxG7JI
GEMINI_API_KEY=TU_GEMINI_KEY_AQUI
```

### 🧠 Modelo y Motor IA
- **Modelo LLM**: `gemini-3.6-flash` (`v1beta/models/gemini-3.6-flash:generateContent`).
- **Contexto**: Inyecta dinámicamente los primeros 2,000 caracteres de `wiki/life-dashboard.md` en cada interacción para mantener alineación proactiva.

---

## 📱 Comandos y Uso

| Comando | Descripción | Ejemplo de Uso |
| :--- | :--- | :--- |
| `/start` o `/help` | Muestra el menú de bienvenida y guía de comandos. | `/start` |
| `/ticket` | Consulta los últimos 5 tickets registrados en MasterHub Helpdesk. | `/ticket` |
| `/ticket create` | Crea un ticket de Helpdesk con título y descripción. | `/ticket create Falla de Impresora \| Impresora fiscal sin papel` |
| `/ingest <texto/url>` | Fuerza el guardado directo de una nota o enlace en `raw/inbox/`. | `/ingest https://youtube.com/watch?v=123` |
| *(Mensaje Libre)* | Chat abierto con ALFRED usando Gemini 3.6 Flash. | *"¿Cuáles son mis prioridades de hoy?"* |

---

## 🛠️ Ejecución y Servicio en Segundo Plano

Para mantener el bot escuchando activamente en la máquina local o servidor:

```powershell
python scripts/telegram_bot.py
```

---

## 🔗 Enlaces Relacionados
- [[Dashboard de Vida & Centro de Control|../life-dashboard.md]]
- [[Guía de Empaquetado y Despliegue Rápido de ALFRED & 2brain|../programacion/guia-despliegue-empaquetado-alfred-2brain.md]]
- [[MasterHub Helpdesk API & Gestión de Tickets|../proyectos/masterhub-helpdesk-api.md]]
