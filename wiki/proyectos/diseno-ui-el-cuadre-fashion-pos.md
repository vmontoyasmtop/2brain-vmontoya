---
title: "Especificación UI/UX: El Cuadre POS (Fashion & Footwear Edition - Google Stitch)"
type: "concept"
area: "proyectos"
status: "completed"
created: 2026-10-29
updated: 2026-10-29
tags:
  - konan-uiux
  - sai-designer
  - stitch
  - el-cuadre-pos
  - fashion-retail
  - footwear
  - design-tokens
  - tailwind
---

# 🦋 Especificación UI/UX: EL CUADRE POS — Fashion & Footwear Edition

**Diseñadora UI/UX Líder**: 🦋 Konan (El Ángel de Papel — Akatsuki Design Labs)  
**Dirección de Arte & Brand Book**: 🎨 Sai (Técnica Chōjū Giga)  
**Herramienta Oficial**: **Google Stitch Cloud** ([`https://stitch.withgoogle.com/`](https://stitch.withgoogle.com/))  
**Proyecto Google Stitch**: `projects/15301442243370859300` ("El Cuadre POS - Caja, Viveres y Abasto Criollo")  
**Design System Oficial Stitch**: `El Cuadre POS - Fashion & Footwear` (`assets/3d9ff97b56004f41806d87b7f61059dc`)  
**Rubro**: Tiendas de Ropa, Calzado, Boutiques, Sneaker Stores & Accesorios  
**Entorno de Mostrador**: Terminal táctil panorámico (Widescreen Touch Terminal 1080p/4K)  
**Prototipo Interactivo Standalone**: [`stitch_el_cuadre_fashion_pos.html`](prototipos/stitch_el_cuadre_fashion_pos.html)  
**Showcase de Marca & Logos**: [`brand-assets-el-cuadre-fashion.html`](brand-assets-el-cuadre-fashion.html)  

---

## 🎨 Suite Oficial de las 5 Pantallas en Google Stitch

| N° | Vista / Pantalla | Screen ID en Google Stitch | Archivos Oficiales Exportados |
| :---: | :--- | :---: | :--- |
| **01** | **Caja Táctica POS (Widescreen Terminal 1080p)** | [`e5f837028e3b4bc4942576a3136dd23f`](https://stitch.withgoogle.com/projects/15301442243370859300) | 🖼️ [`stitch_el_cuadre_fashion_pos.png`](assets/stitch_el_cuadre_fashion_pos.png) (1.04 MB)<br>💻 [`stitch_el_cuadre_fashion_pos_official.html`](prototipos/stitch_el_cuadre_fashion_pos_official.html) |
| **02** | **Módulo de Canje & Cambio de Tallas (Exchange Flow)** | [`ad386d682d5b4c95b9fd14bba7c10566`](https://stitch.withgoogle.com/projects/15301442243370859300) | 🖼️ [`stitch_el_cuadre_fashion_canje.png`](assets/stitch_el_cuadre_fashion_canje.png) (1.04 MB)<br>💻 [`stitch_el_cuadre_fashion_canje.html`](prototipos/stitch_el_cuadre_fashion_canje.html) |
| **03** | **Generador de Etiquetas Térmicas 50x30mm con Barcode** | [`3dfefb3b003d4dcaa264d5604b77abd2`](https://stitch.withgoogle.com/projects/15301442243370859300) | 🖼️ [`stitch_el_cuadre_fashion_etiquetas.png`](assets/stitch_el_cuadre_fashion_etiquetas.png) (503 KB)<br>💻 [`stitch_el_cuadre_fashion_etiquetas.html`](prototipos/stitch_el_cuadre_fashion_etiquetas.html) |
| **04** | **Pasarela de Cobranza Bimoneda & Pagos Mixtos Retail** | [`a6eb8e0e5aef47598c7ea646c6568cd8`](https://stitch.withgoogle.com/projects/15301442243370859300) | 🖼️ [`stitch_el_cuadre_fashion_cobro.png`](assets/stitch_el_cuadre_fashion_cobro.png) (1.15 MB)<br>💻 [`stitch_el_cuadre_fashion_cobro.html`](prototipos/stitch_el_cuadre_fashion_cobro.html) |
| **05** | **Inventario Matriz de Tallas & Colores con Alerta Stock** | [`0cb8ae1d03a8447b8b75bd606fa4cb63`](https://stitch.withgoogle.com/projects/15301442243370859300) | 🖼️ [`stitch_el_cuadre_fashion_inventario.png`](assets/stitch_el_cuadre_fashion_inventario.png) (684 KB)<br>💻 [`stitch_el_cuadre_fashion_inventario.html`](prototipos/stitch_el_cuadre_fashion_inventario.html) |

---

## 1. Arquitectura de Experiencia Táctil (Countertop UX)

A diferencia de un kiosco de alimentos donde prima el pesaje decimal de balanza, en el retail de moda y calzado los cuellos de botella del cajero son:
1. **La búsqueda y validación de tallas disponibles sin tener que ir físicamente al almacén**.
2. **La discriminación visual de combinaciones de color/swatch**.
3. **El canje inmediato de prendas devueltas por ajuste de talla sin descuadrar la caja ni el kardex**.
4. **La impresión rápida de etiquetas térmicas adhesivas (50x30mm) con código de barras Code-128 para cajas o etiquetas colgantes (hangtags)**.

### Disposición Split-Screen Táctica (68% Catálogo / 32% Ticket & Cobro)
- **Header Superior**:
  - Logotipo oficial *Atelier* con isotipo C + Check textil en oro champán y cobalto.
  - Switcher dinámico de rubro (*Ropa & Calzado* ↔ *Víveres & Minimarkets*).
  - Ticker de tasa BCV en vivo editable con semáforo de sincronización.
  - Accesos directos a **Canje / Devolución**, **Generador de Etiquetas Térmicas 50x30mm** y **Bloqueo PIN**.
- **Barra de Departamentos**:
  - Pills táctiles horizontales: *Todos los Artículos, Calzado Caballero, Calzado Dama, Calzado Niños, Camisas & Franelas, Pantalones & Jeans, Vestidos & Faldas, Accesorios & Gorras*.
- **Buscador & Pistola Láser**:
  - Input auto-enfocado para lectores de códigos de barra USB/Bluetooth con simulación de escaneo rápido de SKU.
- **Grid de Productos**:
  - Tarjetas de alta densidad táctil con fotografía de producto, badge de colección, precio dual ($ USD y Bs.) y contador de tallas en stock.
- **Modal de Variantes (Tallas & Colores)**:
  - Botones táctiles grandes para calzados (36-44) y prendas (XS-XXL) con **semáforo de stock**: Verde (disponible con conteo), Ámbar (última unidad), Gris tachado (agotado, deshabilitado).
  - Swatches circulares de color con muestra tonal y nombre comercial.
  - Stepper de cantidad táctil (+ / -).
- **Panel de Cobranza (Carrito)**:
  - Desglose con badges explícitos `[TALLA]` y `[COLOR]`.
  - Cobranza multimoneda venezolana: Efectivo $, Pago Móvil (con QR y referencia), Punto de Venta (voucher), Zelle y Biopago.

---

## 2. Design Tokens Oficiales (Sai & Konan)

| Token | Hex / Utility CSS | Flutter (`ThemeData`) | Aplicación |
| :--- | :--- | :--- | :--- |
| **Ónix Boutique** | `#0B0F17` / `bg-[#0B0F17]` | `Color(0xFF0B0F17)` | Lienzo principal del terminal táctil. |
| **Grafito Lujoso** | `#131D2D` / `bg-[#131D2D]` | `Color(0xFF131D2D)` | Superficie de tarjetas y headers. |
| **Panel Elevado** | `#182438` / `bg-[#182438]` | `Color(0xFF182438)` | Contenedor de totales y modales. |
| **Borde Couture** | `#2A3C59` / `border-[#2A3C59]` | `Color(0xFF2A3C59)` | Delimitadores y separadores de cuadrícula. |
| **Cobalto Eléctrico**| `#3B82F6` / `text-[#3B82F6]` | `Color(0xFF3B82F6)` | Acciones primarias y acentos de navegación. |
| **Rose Fashion** | `#F43F5E` / `bg-rose-500` | `Color(0xFFF43F5E)` | Badge de rubro, selección activa y botón CTA. |
| **Oro Champán** | `#F59E0B` / `text-[#F59E0B]` | `Color(0xFFF59E0B)` | Acentos premium, remache textil y ofertas. |
| **Menta BCV** | `#10B981` / `text-emerald-400`| `Color(0xFF10B981)` | Indicador de tasa oficial y totales en Bolívares. |

---

## 3. Especificación Técnica para la Implementación (Itachi & Kisame)

### Directrices para Itachi (Frontend Web Next.js)
1. **Componente `VariantSelectorModal.tsx`**:
   - Abrir como overlay modal accesible con soporte de teclado numérico táctil.
   - Calcular dinámicamente el SKU compuesto: `${product.skuBase}-${size}-${colorCode}`.
2. **Componente `ThermalLabelPreview.tsx`**:
   - Maquetar a tamaño físico exacto 50mm $\times$ 30mm en CSS con `@page { size: 50mm 30mm; margin: 0; }`.
   - Renderizar código de barras Code-128 con `bwip-js` o SVG puro.
3. **Componente `ExchangeModal.tsx`**:
   - Permitir registrar devolución de prenda con ingreso a stock (`status: RETURNED_RESTOCKED`) y entrega de nueva talla en la misma transacción (`diferencia: $0.00`).

### Directrices para Kisame (Mobile Flutter)
1. **Widget `SizeStockGrid`**:
   - `GridView.builder` con ratio 1.2 para pulsación táctil con pulgares o lápiz óptico.
   - Feedback háptico (`HapticFeedback.selectionClick()`) en selección de talla y color.
2. **Soporte Bluetooth ESC/POS / TSPL**:
   - Drivers para etiquetadoras térmicas portátiles (Xprinter / Zebra / Rongta) vía Bluetooth SPP / BLE.
