---
name: gdocs-formatting
description: Reglas y estándar de maquetación nativa de Google Docs mediante Google Docs/Drive API. Prohíbe volcar texto en formato Markdown plano y exige aplicar estilos nativos (HEADING_1, HEADING_2, TITLE, SUBTITLE, insertTable, createParagraphBullets, fondo sombreado para bloques de código).
---

# 📄 Skill de Maquetación Nativa en Google Docs

## 🚫 Regla de Oro: Prohibido Volcar Markdown Plano
NUNCA verter texto que contenga sintaxis Markdown cruda (`#`, `##`, `**texto**`, `| tabla |`, ```código```) dentro del cuerpo de un documento de Google Docs.

## 🎨 Estándar Obligatorio de Estilos Nativos
Cada vez que se cree o actualice un Google Doc (usando `documentation-agent` o la API de Google Docs):

1. **Plantilla Maestra y Banner:**
   - Mantener el Header / Banner corporativo oficial clonado desde `15K2DXsBD7_HYI4jBJEHNV1lq9B6lRcHf66GUIzOwZxc`.
2. **Jerarquía Novedosa de Párrafos (`updateParagraphStyle`):**
   - Título principal: `TITLE` (Centrado, negrita, 22pt, `#0F172A`).
   - Subtítulo: `SUBTITLE` (Centrado, cursiva, 13pt, `#2563EB`).
   - Secciones Principales: `HEADING_1` (Negrita, 16pt, `#0F172A`, espacio superior 14pt, inferior 6pt).
   - Subsecciones: `HEADING_2` (Negrita, 13pt, `#2563EB`, espacio superior 10pt, inferior 4pt).
   - Sub-subsecciones: `HEADING_3` (Negrita, 11pt, `#334155`).
3. **Índice Interactivo de Contenidos:**
   - Todo documento técnico debe contar con un bloque de **Índice de Contenidos** estructurado al inicio.
4. **Viñetas Nativas (`createParagraphBullets`):**
   - Aplicar viñetas nativas de Google Docs (`BULLET_DISC_CIRCLE_SQUARE`) en listas de elementos.
5. **Bloques de Código & Mapeo de APIs (`updateTextStyle`):**
   - Para fragmentos de código, llamados a APIs o comandos de terminal, formatear el texto con tipografía monoespaciada (`Consolas` / `Courier New`), tamaño 9.5pt y fondo sombreado suave (`backgroundColor: #F8FAFC`).
