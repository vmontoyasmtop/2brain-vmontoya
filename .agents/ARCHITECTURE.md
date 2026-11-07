# Arquitectura del Sistema de Agentes — 1 Núcleo · 2 Packs de dominio · 1 Pipeline

> Estado: **propuesta de diseño** (2026-11-07). No reemplaza todavía a [`AGENTS.md`](../AGENTS.md); lo complementa.
> Autor: ALFRED. Aprobación pendiente del Señor.

---

## 1. Decisión

Los tres conjuntos de agentes **no compiten**: son tres dominios reales.

| Dominio | Agente / Pack | Alcance |
| :--- | :--- | :--- |
| Vida y conocimiento | **ALFRED** (núcleo) | Agenda, wiki, 6 áreas, orquestación, entrega de turno |
| Proyectos propios y freelance | **Akatsuki** | SmartOps, El Cuadre POS, BrotApp, WebCastro, Meniox… |
| MasterGroup | **La Compañía del Anillo** | MG-HUB, MasterHub, CRM-MG, Plane |

El defecto actual no es tener tres dominios: es haberlos implementado como **tres forks de los mismos archivos**, sin contrato de pack, sin router y sin pipeline común. La corrección es:

> **Un solo runtime y una sola fuente de verdad; un núcleo (ALFRED) y dos packs de dominio; un pipeline de desarrollo compartido.**

### ADR-001 — Un núcleo, tres packs
ALFRED no es un pack: es el runtime, la memoria y el router. Akatsuki y Fellowship son packs que se cargan según el proyecto.

### ADR-002 — `.agents/skills/` es la única fuente
Cada rol vive en `.agents/skills/<slug>/SKILL.md`. `agents/` y `.agents/rules/` pasan a ser **capas generadas** por script (compatibilidad con Antigravity), nunca editadas a mano.

### ADR-003 — Un pipeline, distinto casting
Las 8 etapas del ciclo de desarrollo son idénticas para ambos packs. Lo único que cambia es **qué personaje ocupa cada etapa**.

### ADR-004 — La evidencia vive en la wiki, no en el chat
Cada gate deja un artefacto en `wiki/proyectos/<id>/`. Un gate sin artefacto no está aprobado.

---

## 2. Mapa objetivo

```text
ALFRED (núcleo)
│  identidad · agenda · 6 áreas · router · memoria · entrega de turno
│
├── Especialistas de vida (core)
│   ├── pastoral        (ministerial)
│   ├── finanzas        (finanzas)
│   ├── wellness        (familiar)
│   ├── it-support      (trabajo / Xetux)
│   └── docs-expert     (Google Docs con banner)
│
├── Wiki ops (core)
│   ├── ingest · synthesizer · gardener
│
├── Pack AKATSUKI  →  SmartOps y proyectos propios
│   ├── pain-pm · orochimaru-arch-devops
│   ├── konan-uiux · sai-designer
│   ├── itachi-frontend · kakuzu-backend · kisame-mobile
│   ├── hidan-qa · deidara-pentest · sasori-defense
│   └── zetsu-docs · tobi-marketing
│
└── Pack FELLOWSHIP  →  MasterGroup / MG-HUB
    ├── grandalf (lead) · aragorn (PM)
    ├── legolas (front) · gimli (back) · galadriel (DB)
    ├── frodo (DevOps) · elrond (QA/refactor)
    ├── samwise (IT/ops) · merry (docs) · pippin (redacción)
    ├── boromir (finanzas MG)
    └── prestados: deidara-pentest · sasori-defense · konan-uiux
```

**Regla de pertenencia:** un rol tiene un pack dueño. Si otro pack lo necesita, se declara en `borrowed:` del manifiesto. No se duplica el archivo.

---

## 3. Contrato de pack

Cada pack se declara en `.agents/packs/<id>.yaml`:

```yaml
id: akatsuki
domain: "Proyectos propios y freelance"
owner: "El Señor"
repos:
  root: "${SMARTOPS_PATH}"
tracker:
  system: clickup
roles:
  pm: pain-pm
  architect: orochimaru-arch-devops
  ...
borrowed: []
overrides:
  security: [deidara-pentest, sasori-defense]
```

Campos obligatorios: `id`, `domain`, `roles`, `repos`, `tracker`.
Campos opcionales: `borrowed`, `overrides`, `conventions`.

---

## 4. Enrutamiento (router)

Orden de resolución, de mayor a menor confianza:

1. **Ruta del repositorio** — si el `cwd` o el repo del proyecto cae bajo `MG_HUB_PATH` → `fellowship`; bajo `SMARTOPS_PATH` → `akatsuki`.
2. **Registro de proyecto** — `.agents/projects.yaml` asocia `id` → pack.
3. **Palabras clave** — "Xetux" → `it-support`; "sermón" → `pastoral`; "presupuesto" → `finanzas`.
4. **Pregunta única** — si sigue ambiguo, ALFRED pregunta una sola vez y registra la respuesta.

Si un path configurado no existe, el router **no adivina**: lo reporta y pide la ruta correcta.

---

## 5. Presupuesto de contexto (harness)

| Capa | Cuándo se carga | Límite |
| :--- | :--- | :--- |
| `AGENTS.md` (núcleo) | Siempre | ≤ 6 KB |
| Manifiesto de pack | Al fijar dominio | ≤ 2 KB |
| Skill de rol | Al despachar la etapa | ≤ 6 KB |
| `dev-cycle` (estándar) | En toda tarea de código | ≤ 4 KB |
| Referencias / plantillas | Bajo demanda | — |

Objetivo por tarea: **15–20 KB** de instrucciones, frente a los ~26 KB actuales (AGENTS.md de 21 KB + rol de 5 KB).

Regla: el catálogo de skills solo aporta `name` + `description`; el cuerpo se carga cuando la etapa lo exige.

---

## 6. Contrato de delegación (subagentes)

Toda delegación debe incluir estos siete campos. Sin ellos, el subagente no arranca:

```text
1. OBJETIVO      resultado esperado en una frase
2. CONTEXTO      proyecto, pack, etapa, enlaces a wiki/ADRs
3. INSUMOS       archivos, contratos, credenciales disponibles
4. RESTRICCIONES stack, estilo, seguridad, no tocar X
5. DoD           criterios verificables de terminado
6. SALIDA        formato exacto (archivo, diff, informe)
7. ARCHIVOS      rutas que puede leer/escribir
```

Plantilla en `.agents/templates/handoff.md`.

---

## 7. Herramientas del harness DSH por etapa

| Etapa | Herramienta | Patrón |
| :--- | :--- | :--- |
| Intake | `ask_user_question`, `create_goal` | Clasificar dominio; abrir goal si dura varias sesiones |
| Discovery | `web_search`, `web_fetch`, `subagent` | Investigación aislada; REA si es competencia |
| Plan | skill PM + `scripts/clickup_api.py` | Gherkin, SP, dependencias, riesgos |
| Design | `konan-uiux` + `scripts/stitch_api.py`, `orochimaru` | Prototipo + ADR + OpenAPI + modelo de datos |
| Build | `subagent` / `subagent_fork` | Un subagente por vertical; `workflow` si hay ≥5 archivos |
| Verify | `hidan-qa` / `elrond` + `job_*` | Tests en background; el job no bloquea |
| Security | `deidara-pentest` + `sasori-defense` | Red team y remediación en pasadas separadas |
| Release | `frodo` + `present` | Release notes, rollback, artefacto presentado |
| Operate | `schedule_create`, `gardener` | Ceremonias y auditoría semanal |

**Limitación actual detectada:** este runtime no tiene MCP de Google Calendar, Gmail ni ClickUp conectados. La agenda de ALFRED hoy depende de Antigravity o de scripts locales. Ver §11, Fase 3.

---

## 8. Ciclo de desarrollo unificado — 8 etapas y 8 gates

| # | Etapa | Gate (evidencia obligatoria) | Akatsuki | Fellowship |
| :-: | :--- | :--- | :--- | :--- |
| 0 | **Intake** | Ficha en `projects.yaml` + pack asignado | ALFRED | ALFRED |
| 1 | **Discovery** | `01-discovery.md`: problema, usuarios, alcance, métricas de éxito | Pain | Aragorn |
| 2 | **Plan** | `02-plan.md`: historias Gherkin, SP, dependencias, riesgos, DoR | Pain | Aragorn |
| 3 | **Design** | `03-architecture.md`: ADR + OpenAPI + modelo de datos + prototipo | Orochimaru · Konan · Kakuzu | Grandalf · Legolas · Galadriel |
| 4 | **Build** | PR + CI verde + cobertura ≥ 85 % + lint/type limpios | Itachi · Kakuzu · Kisame | Legolas · Gimli |
| 5 | **Verify** | `05-test-report.md`: AC probados, regresión, UAT | Hidan | Elrond |
| 6 | **Security** | `06-security.md`: SAST/DAST, OWASP, hallazgos y remediación | Deidara + Sasori | *prestados* Deidara + Sasori |
| 7 | **Release** | `07-release.md`: notas, smoke test, rollback probado, docs | Zetsu + Frodo | Frodo + Merry |
| 8 | **Operate** | `08-retro.md` + métricas actualizadas | Pain + Zetsu | Samwise + Merry |

### Definición de Listo (DoR)
- Problema y usuarios claros.
- Criterios de aceptación en Gherkin.
- Contratos UX/API acordados.
- Dependencias y riesgos identificados.
- Estimación y datos de prueba disponibles.
- Clasificación de seguridad (¿toca auth, pagos, datos personales?).

### Definición de Terminado (DoD)
- Código mergeado con revisión.
- Tests unitarios + integración; cobertura ≥ 85 % en lo tocado.
- Lint, tipos y build sin errores.
- Documentación y changelog actualizados.
- Gate de seguridad aprobado (sin críticos/altos abiertos).
- Desplegado en staging y UAT firmado.
- Monitoreo/alertas y rollback definidos.
- Entrada en `wiki/log.md` y página de proyecto actualizada.

### Carriles alternos
- **Fast lane (hotfix):** Intake → Plan-lite → Build → Verify → Release. Seguridad solo si toca auth/datos/pagos.
- **Spike (investigación):** time-box de 1 día; salida = ADR con decisión, no código.

---

## 9. Evidencia y memoria por proyecto

```text
wiki/proyectos/<id>/
├── 00-intake.md
├── 01-discovery.md
├── 02-plan.md
├── 03-architecture.md
├── 05-test-report.md
├── 06-security.md
├── 07-release.md
├── 08-retro.md
└── metrics.md
```

Esto sustituye gradualmente los 146 archivos planos de `wiki/proyectos/` por hubs por proyecto. La migración es incremental: el proyecto que se toque, se ordena.

---

## 10. Métricas y ceremonias

**DORA + calidad:** lead time, cycle time, frecuencia de despliegue, change failure rate, MTTR, cobertura, defectos escapados, % de gates con evidencia.

**Ceremonias** (vía `schedule_create`, solo si el Señor lo pide):
- Standup diario 07:30 (ALFRED).
- Revisión semanal de portafolio (viernes).
- Planning quincenal por pack.
- Retro por release.

---

## 11. Roadmap de implementación

| Fase | Alcance | Esfuerzo | Riesgo |
| :--- | :--- | :--- | :--- |
| **F0 — Reparación** | Codificación UTF-8 (34 archivos), rutas `${MG_HUB_PATH}`, `invoke_subagent` → `subagent`, registrar `gdocs-formatting` | 2 h | Bajo |
| **F1 — Núcleo + packs** | `AGENTS.md` ≤ 150 líneas, manifiestos, router, `projects.yaml`, generador de capas, script de auditoría | 1 día | Medio |
| **F2 — Pipeline** | Skill `dev-cycle`, plantillas de gates, DoR/DoD, PR template, CI | 1–2 días | Medio |
| **F3 — Observabilidad** | Métricas por proyecto, evals de enrutamiento, conectar agenda (MCP o CLI Google), ceremonias | continuo | Bajo |

**Orden recomendado:** F0 → F1 → F2 → F3. No borrar `agents/` hasta que F1 genere y verifique las capas derivadas.

---

## 12. Criterio de éxito

1. Un rol se edita en **un solo archivo**.
2. Cualquier tarea de código se enruta a un pack **sin preguntar**.
3. Todo gate deja evidencia en la wiki.
4. La auditoría corre en CI y falla ante corrupción, duplicado o ruta muerta.
5. ALFRED puede responder "¿en qué va el proyecto X?" leyendo un solo hub.
