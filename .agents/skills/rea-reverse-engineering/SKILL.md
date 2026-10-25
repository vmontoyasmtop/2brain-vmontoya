---
name: rea-reverse-engineering
description: >-
  Skill de Reingeniería Inversa (basada en morluto/rea): inspecciona y deconstruye aplicaciones web, móviles, binarios y competencia de mercado mediante análisis basado en evidencias para transformar hallazgos en requerimientos y tareas en ClickUp.
---

# 👁️‍🗨️ Skill: REA — Reverse Engineer Anything (morluto/rea)

> *"Con la visión omnisciente del Rinnegan y el protocolo REA, ninguna arquitectura competidora permanece oculta. Deconstruimos el software rival para superarlo."*

Esta skill integra la metodología y herramientas del repositorio **`morluto/rea`** (**Reverse Engineer Anything**) para que **Pain (Tendō)** y la Organización Akatsuki investiguen proyectos de software existentes, realicen benchmarking competitivo y efectúen reingeniería inversa de aplicaciones para crear implementaciones limpias (*Clean-Room Implementation*) superiores.

---

## 🔬 Capacidades del Protocolo REA

### 1. Ecosistemas & Objetivos de Análisis
- **Aplicaciones Web & SPA**:
  - Análisis de bundles minificados de JavaScript/TypeScript (Webpack, Vite, Turbopack).
  - Mapeo de rutas, llamadas a APIs REST/GraphQL, cabeceras de autenticación y estructuras de estado.
  - Extracción de esquemas de datos implícitos a partir de formularios y respuestas JSON.
- **Aplicaciones de Escritorio (Electron / Tauri / .NET)**:
  - Extracción e inspección de archivos `.asar` de Electron.
  - Desensamblado e inspección de binarios y dependencias.
- **Aplicaciones Móviles (Android APK / iOS IPA)**:
  - Decompilación de código APK (JADX) y análisis de manifests, permisos y componentes.
  - Inspección de bases de datos locales SQLite embebidas y consumo de APIs remotas.

### 2. Marco de Análisis Basado en Evidencias (Evidence-Based Architecture)
Para evitar alucinaciones, todo informe de reingeniería inversa debe clasificar los hallazgos en 3 niveles estrictos:
1. **👁️ Lo Observado (Hard Evidence)**:
   - Rutas de red exactas (`POST /api/v2/checkout`), cabeceras HTTP, payloads JSON comprobados, dependencias de `package.json`.
2. **🧠 Lo Inferido (Architectural Deductions)**:
   - Flujos de negocio asumidos, máquinas de estado, patrones de diseño (CQRS, Event-Driven, MVC).
3. **❓ Lo Desconocido (Unknowns / Limitations)**:
   - Lógica de servidor opaca no expuesta en cliente, endpoints con cifrado propietario o código ofuscado.

---

## 🛠️ Modos de Ejecución Técnica

### A. Ejecución vía CLI / NPM Runner
Para inicializar o vincular REA a los entornos de trabajo:
```bash
npx rea-agents@latest setup
```
- Registra el servidor MCP de REA para agentes compatibles.
- Configura las rutas hacia herramientas de inspección locales (decompiladores, parsers).

### B. Flujo de Trabajo para Pain (Investigación Competitiva ➡️ ClickUp)
1. **Fase de Extracción**: Pain o el agente investigador inspecciona la URL, APK o repositorio del proyecto competidor.
2. **Fase de Informe REA**: Se genera el documento de síntesis en `wiki/proyectos/benchmarks/[nombre-competidor].md`.
3. **Fase de Conversión en ClickUp**: Pain traduce las fortalezas y debilidades del competidor en:
   - **Épica de Producto**: Superar la funcionalidad analizada eliminando cuellos de botella.
   - **Historias de Usuario (Gherkin)**: Redactadas con base en las evidencias extraídas.
   - **Despacho Akatsuki**:
     - 🦋 **Konan**: Diseña en Stitch una UX superior resolviendo los puntos de dolor detectados.
     - 🖤 **Kakuzu**: Diseña un esquema de base de datos más eficiente y seguro.
     - 👁️ **Itachi** & 🦈 **Kisame**: Construyen clientes web/móvil más ligeros y rápidos.

---

## 📋 Plantilla Estándar de Informe REA

```markdown
# 🔍 Informe de Reingeniería Inversa & Análisis Competitivo (REA)
**Objetivo / Competidor**: [Nombre del Software o URL]  
**Investigador Líder**: ☁️ Pain (Vía Rinnegan & REA Toolkit)  
**Fecha**: YYYY-MM-DD  

## 1. Resumen Ejecutivo & Stack Tecnológico Identificado
- **Frontend**: [React / Next.js / Vue / Flutter / etc.]
- **Backend / APIs**: [REST / GraphQL / WebSockets]
- **Persistencia Detectada**: [PostgreSQL / SQLite / Firebase]
- **Diferenciador Clave**: [Propuesta de valor del competidor]

## 2. Hallazgos Basados en Evidencia
### 👁️ Evidencia Observada (Datos Reales)
- **Endpoints Clave**:
  - `GET /api/v1/items`: Devuelve array con paginación basada en cursor.
  - `POST /api/v1/auth/refresh`: Manejo de refresh token por cookies HttpOnly.
- **Modelos de Datos Extraídos**:
  ```typescript
  interface CompetitorEntity {
    id: string;
    status: string;
    metadata: Record<string, unknown>;
  }
  ```

### 🧠 Deducciones e Inferencias de Arquitectura
- El competidor utiliza un patrón de optimistic UI para la creación de tareas.
- Presenta latencias altas en reportes por falta de indexación en fechas.

### ❓ Puntos Ciegos / Limitaciones
- Algoritmo interno de scoring procesado en backend privado.

## 3. Plan de Acción Akatsuki (Conversión a ClickUp)
| ID US | Tarea / Historia | Ninja Asignado | Ventaja Competitiva a Implementar |
| :--- | :--- | :--- | :--- |
| US-01 | Rediseño de interfaz en Stitch | 🦋 Konan | Flujo de checkout en 2 pasos (vs 5 del rival) |
| US-02 | Optimización de endpoints en NestJS | 🖤 Kakuzu | Caching con Redis y transacciones atómicas |
| US-03 | Modo offline en Flutter | 🦈 Kisame | Persistencia SQLite local inexistente en el rival |
```
