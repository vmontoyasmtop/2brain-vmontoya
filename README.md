# 🧠 2brain — LLM-Powered Second Brain (VS Code + Foam)

**2brain** es un sistema de gestión del conocimiento (Segundo Cerebro) basado en la arquitectura **LLM Wiki** formulada por **Andrej Karpathy** ([Gist de referencia](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)), estructurado por **Carpetas de Área** e integrado en **Visual Studio Code** con la extensión **Foam**.

Está organizado físicamente en **6 Áreas Principales**:
1. 🏢 **`trabajo`**: Analista IT & Soporte Técnico en **Xetux**.
2. 💻 **`programacion`**: Conocimiento técnico, lenguajes, frameworks y arquitectura.
3. 🚀 **`proyectos`**: Proyectos de programación independientes y especificaciones de software.
4. ⛪ **`ministerial`**: Predicaciones, sermones, exégesis bíblica, estudios y liderazgo pastoral.
5. 🏡 **`familiar`**: Metas familiares, eventos del hogar, bienestar personal y salud.
6. 💰 **`finanzas`**: Presupuesto personal/familiar, ingresos, diezmos/ofrendas y ahorro.

---

## 📁 Estructura por Áreas

```text
2brain/
├── raw/                      # Fuentes crudas inmutables por área
│   ├── trabajo/
│   ├── programacion/
│   ├── proyectos/
│   ├── ministerial/
│   ├── familiar/
│   ├── finanzas/
│   └── assets/
├── wiki/                     # Conocimiento procesado por los Agentes por área
│   ├── trabajo/              # Notas de soporte IT y Xetux
│   ├── programacion/         # Notas técnicas y guías de código
│   ├── proyectos/            # Notas de apps y proyectos propios
│   ├── ministerial/          # Predicaciones, sermones y estudios bíblicos
│   ├── familiar/             # Notas familiares y personales
│   ├── finanzas/             # Notas de presupuesto y contabilidad
│   ├── concepts/             # Conceptos transversales
│   ├── entities/             # Entidades (personas, software, empresas)
│   ├── summaries/            # Resúmenes de fuentes crudas
│   ├── index.md              # Catálogo maestro indexado por áreas
│   └── log.md                # Log de operaciones
├── agents/                   # Subagentes especializados (8 subagentes)
├── scripts/
│   └── wiki_helper.py        # Herramienta CLI para buscar, auditar por áreas y ver estado
├── AGENTS.md                 # Manual operativo maestro por áreas
└── README.md                 # Este archivo
```

---

## 🤖 Subagentes Especializados Disponibles

| Subagente | Archivo | Área Principal |
| :--- | :--- | :--- |
| 📥 **Ingestor** | [`agents/ingestor.md`](agents/ingestor.md) | Ingerir fuentes crudas de `raw/` a su carpeta en `wiki/`. |
| 🔍 **Synthesizer** | [`agents/synthesizer.md`](agents/synthesizer.md) | Cruzar notas entre áreas y responder dudas profundas. |
| 🧹 **Gardener** | [`agents/gardener.md`](agents/gardener.md) | Auditar enlaces rotos, notas huérfanas y orden de carpetas. |
| 🎨 **Frontend UI Expert** | [`agents/frontend_ui_expert.md`](agents/frontend_ui_expert.md) | Áreas `programacion` y `proyectos` (React, Tailwind, CSS). |
| ⚙️ **Backend JS Expert** | [`agents/backend_js_expert.md`](agents/backend_js_expert.md) | Áreas `programacion` y `proyectos` (Node.js, TS, DBs). |
| ⛪ **Pastoral Assistant** | [`agents/pastoral_assistant.md`](agents/pastoral_assistant.md) | Área `ministerial` (sermones, bosquejos, teología). |
| 🛠️ **IT Support Expert** | [`agents/it_support_expert.md`](agents/it_support_expert.md) | Área `trabajo` (soporte Xetux, manuales, SOPs). |
| 💰 **Finance Manager** | [`agents/finance_manager.md`](agents/finance_manager.md) | Área `finanzas` (presupuestos, cotizaciones, contabilidad). |

---

## 🛠️ Herramientas CLI (`scripts/wiki_helper.py`)

```bash
# Ver estado general con desglose por las 6 áreas
python scripts/wiki_helper.py status

# Buscar términos en toda la wiki
python scripts/wiki_helper.py search "Xetux"

# Ver fuentes pendientes en raw/
python scripts/wiki_helper.py pending
```
