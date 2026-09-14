---
title: "Concepto: LLM Wiki Pattern"
type: concept
created: 2026-09-11
updated: 2026-09-11
sources:
  - "raw/karpathy-llm-wiki-gist.md"
tags:
  - concept
  - llm-wiki
  - knowledge-management
---

# 🧠 LLM Wiki Pattern

El **LLM Wiki Pattern** es un paradigma de gestión del conocimiento personal ideado por [[Andrej Karpathy]]. Propone la creación de un **Segundo Cerebro compilado de forma incremental por un LLM**.

## 🔄 RAG vs LLM Wiki

| Característica | RAG Tradicional | LLM Wiki Pattern |
| :--- | :--- | :--- |
| **Procesamiento** | Efímero (se busca en cada query) | Compuesto (se actualiza persistentemente) |
| **Artefacto** | Ninguno (solo respuestas en chat) | Wiki persistente en Markdown (`wiki/`) |
| **Relaciones** | Búsqueda por fragmentos vectoriales | Enlaces explícitos (`[[Wikilinks]]`) |
| **Mantenimiento** | Cero estructura mantenida | El LLM mantiene referencias y elimina redundancias |

## 🏗 Componentes de la Arquitectura

- **Fuentes Crudas (`raw/`)**: Documentos inmutables de entrada.
- **La Wiki (`wiki/`)**: Artefacto persistente estructurado en:
  - `summaries/`: Resúmenes de fuentes.
  - `entities/`: Páginas sobre personas, proyectos o herramientas.
  - `concepts/`: Páginas sobre ideas y síntesis.
- **Esquema (`AGENTS.md`)**: Reglas y contratos que guían la disciplina del agente.
- **Índice (`index.md`) & Log (`log.md`)**: Registro estructurado y cronológico.

## 🛠️ Herramientas de Apoyo

- [[Obsidian]]: Visualizador e IDE para explorar enlaces y grafos.
- **Dataview / Marp**: Plugins para generar tablas dinámicas y diapositivas.
