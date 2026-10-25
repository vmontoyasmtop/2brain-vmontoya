---
title: "Especificación UI/UX: Marchante POS (Stitch Design Tokens & Layout)"
type: "concept"
area: "proyectos"
status: "completed"
created: 2026-10-24
updated: 2026-10-24
tags:
  - konan-uiux
  - design-tokens
  - stitch
  - marchante-pos
  - tailwind
  - pos
---

# 🦋 Especificación de Diseño UI/UX: Marchante POS
**Diseñadora Líder**: 🦋 Konan (El Ángel de Dios — UI/UX Designer Akatsuki)  
**Herramienta Oficial**: **Google Stitch API** (`https://stitch.googleapis.com/mcp`)  
**Proyecto Google Stitch**: `projects/11957781762907952110`  
**Pantalla Generada**: `projects/11957781762907952110/screens/70e2a48709dd4ed3a1c3ecc3a18a3283`  
**Design System Oficial Stitch**: `Mercado Slate` (`assets/33347c813f37499abe0ff6b8ae2a56e6`)  
**Resolución de Salida**: 2560 × 2048 (4K POS Terminal)  
**Archivos Generados por Stitch**:
- 🖼️ Screenshot HD: [`wiki/proyectos/assets/stitch_marchante_pos.png`](file:///c:/Users/vmont/OneDrive/Desktop/2brain-vmontoya/wiki/proyectos/assets/stitch_marchante_pos.png)
- 💻 Código HTML/Tailwind Oficial: [`wiki/proyectos/prototipos/stitch_marchante_pos.html`](file:///c:/Users/vmont/OneDrive/Desktop/2brain-vmontoya/wiki/proyectos/prototipos/stitch_marchante_pos.html)
- 📋 Tarea en ClickUp: [🦋 US-01 en ClickUp (86bcqv6b4)](https://app.clickup.com/t/86bcqv6b4)

---

## 1. Concepto Visual & Filosofía Criolla ("El Marchante" en Stitch)

A través de la API oficial de **Google Stitch**, Konan generó el Design System **"Mercado Slate"** diseñado específicamente para terminales POS táctiles de mercados populares y fruterías:
- **Ergonomía Táctil Resistiva y Capacitiva**: Botones y componentes interactivos con áreas mínimas de `48px × 48px` y teclado numérico de `64px × 64px`, evitando toques accidentales con manos húmedas o con guantes.
- **Bi-Monetary Legibility (Legibilidad Bimonetaria)**: Visualización simultánea del total en **Dólares ($ USD)** en tipografía display `Space Grotesk` (`#4edea3` / `#10b981`) y el equivalente en **Bolívares (Bs.)** en `headline-lg` (`#ffb95f` / `#f59e0b`).
- **Control de Pesaje Integrado (Kg vs Unid)**: Badges distintivos en `JetBrains Mono` para productos por peso (`KG` en cian `#38bdf8`) vs productos empacados (`UNID` en `#94a3b8`).

---

## 2. Design Tokens Semánticos (Tailwind & Flutter)

| Token | Propósito | Tailwind CSS | Flutter (`Color` / `TextStyle`) |
| :--- | :--- | :--- | :--- |
| **Primary Brand** | Botones de acción, checkout y acentos activos | `bg-emerald-500 hover:bg-emerald-400 text-slate-950` | `Color(0xFF10B981)` |
| **Accent Bimonetario** | Precios y subtotales en Bolívares (Bs.) | `text-amber-400 font-mono` | `Color(0xFFFBBF24)` |
| **Surface Dark** | Fondo principal de la aplicación | `bg-slate-950` | `Color(0xFF020617)` |
| **Card Surface** | Tarjetas de productos y paneles | `bg-slate-900/60 border-slate-800` | `Color(0xFF0F172A)` |
| **Text Primary** | Títulos y precios destacados | `text-white font-bold` | `Colors.white` |
| **Text Muted** | Stocks disponibles, categorías y fechas | `text-slate-400 text-xs` | `Color(0xFF94A3B8)` |
| **Danger / Merma** | Bajas por descomposición y mermas | `bg-rose-500/20 text-rose-300 border-rose-500/30` | `Color(0xFFF43F5E)` |

---

## 3. Disposición de Pantalla (Master Layout de 2 Columnas)

```
+-----------------------------------------------------------------------------------+
|  🛒 MARCHANTE POS  |  Tasa BCV: Bs. 45.00  |  [🥀 Merma]  |  [🔒 Arqueo]  | Caja 01 |
+-------------------------------------------------+---------------------------------+
|  [ 🔍 Buscar producto / Escanear código (F2) ]  |  🧾 Ticket #ORD-1042  [🗑️ Vaciar]|
|  [🧺 Todos] [🥑 Frutas/Verduras] [📦 Víveres]   |---------------------------------|
|-------------------------------------------------|  🍅 Tomate Perita  0.750 Kg     |
|  [🍅 Tomate]    [🥔 Papa]      [🧅 Cebolla]     |     0.750 Kg × $1.80  $1.35     |
|  $1.80 / Kg     $1.20 / Kg     $1.50 / Kg       |  🌽 Harina P.A.N.  2 und        |
|                                                 |     2 und × $1.40     $2.80     |
|  [🍌 Plátano]   [🥑 Aguacate]  [🥕 Zanahoria]   |                                 |
|  $0.90 / Kg     $2.20 / Kg     $1.10 / Kg       |---------------------------------|
|                                                 |  Subtotal:            $4.15     |
|  [🌽 Harina P]  [🍚 Arroz M]   [🍾 Aceite]      |  Total Bs:       Bs. 186.75     |
|  $1.40 und      $1.25 und      $3.20 und        |  TOTAL USD:           $4.15     |
|                                                 |  [ 💳 COBRAR VENTA (F12) ]      |
+-------------------------------------------------+---------------------------------+
```

---

## 4. Instrucciones para el Clan de Desarrollo

- 👁️ **Para Itachi (Next.js)**:
  - Implementar la vista del POS dividida en `flex flex-col md:flex-row h-screen`.
  - Usar Zustand o React Context para la gestión reactiva del `cart` y `currentRate`.
  - Atajos de teclado: `F2` para enfocar buscador, `F12` o `Espacio` para abrir modal de cobro.
- 🖤 **Para Kakuzu (Backend & DB)**:
  - La Server Action `createSale` debe recibir el array de ítems y descontar el stock en SQLite con transacción atómica `prisma.$transaction`.
- 🦈 **Para Kisame (Flutter)**:
  - Replicar el layout usando `Row` con `Expanded(flex: 6)` para el grid y `Expanded(flex: 4)` para el ticket, utilizando `GridView.builder` con `SliverGridDelegateWithFixedCrossAxisCount`.
