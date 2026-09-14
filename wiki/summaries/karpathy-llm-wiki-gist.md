---
title: "Resumen: LLM Wiki Pattern por Andrej Karpathy"
type: summary
created: 2026-09-11
updated: 2026-09-11
sources:
  - "raw/karpathy-llm-wiki-gist.md"
tags:
  - llm
  - second-brain
  - architecture
  - karpathy
---

# 📄 Resumen: LLM Wiki Pattern por Andrej Karpathy

- **Fuente**: `raw/karpathy-llm-wiki-gist.md`
- **Autor original**: [[Andrej Karpathy]]
- **Concepto clave**: [[LLM Wiki Pattern]]

## 💡 Puntos Clave

1. **Diferencia con RAG**: En RAG tradicional, el modelo busca fragmentos y redescubre el conocimiento desde cero en cada pregunta. En **LLM Wiki**, el modelo compila e incrementa un artefacto persistente (la wiki).
2. **Artefacto Compuesto**: La wiki es un conjunto de archivos Markdown interconectados donde las referencias cruzadas, síntesis y contradicciones ya han sido procesadas.
3. **Roles**:
   - **Humano**: Curaduría de fuentes en `raw/`, dirección de investigación y formulación de preguntas.
   - **LLM**: Mantenimiento, resúmenes, referencias cruzadas, linting y actualización de páginas.
   - **[[Obsidian]]**: Interfaz IDE para visualizar la wiki y la vista de grafo.
4. **3 Capas de Arquitectura**:
   - `raw/` (Fuentes inmutables).
   - `wiki/` (Páginas de entidades, conceptos, resúmenes e índices mantenidas por el LLM).
   - `AGENTS.md` (Esquema y protocolo para disciplinar al agente).
5. **3 Operaciones Principales**: `INGEST`, `QUERY`, `LINT`.
