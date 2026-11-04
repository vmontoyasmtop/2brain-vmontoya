---
title: "Especificación UI/UX: El Cuadre Marchador Mobile (US-19 — Suite Completa de 8 Vistas: POS Móvil & Operaciones en Google Stitch)"
type: "concept"
area: "proyectos"
status: "completed"
created: 2026-11-03
updated: 2026-11-03
tags:
  - konan-uiux
  - kisame-mobile
  - kakuzu-backend
  - stitch
  - el-cuadre-pos
  - el-cuadre-marchador
  - mobile-pos
  - flutter
  - us-19
---

# 🦋 Especificación UI/UX: EL CUADRE MARCHADOR MOBILE (POS de Bolsillo & Operaciones de Pasillo)

**Diseñadora UI/UX Líder**: 🦋 Konan (El Ángel de Papel — Akatsuki Design Labs)  
**Ingeniero Mobile Asignado**: 🦈 Kisame Hoshigaki (Flutter & Dart — BLoC / Offline-First)  
**Arquitecto Backend Sync**: 🖤 Kakuzu (NestJS Local LAN API & SQLite WAL)  
**Herramienta Oficial**: **Google Stitch Cloud** ([`https://stitch.withgoogle.com/projects/15301442243370859300`](https://stitch.withgoogle.com/projects/15301442243370859300))  
**Proyecto Google Stitch**: `projects/15301442243370859300` (*El Cuadre POS - Caja, Víveres y Abasto Criollo*)  
**User Story en ClickUp**: [📱 US-19: App Móvil "El Cuadre Marchador" (`86bcxum9q`)](https://app.clickup.com/t/86bcxum9q)  
**Scripts de Despliegue**:
- [`scripts/deploy_marchador_pos_mobile_stitch.py`](../../scripts/deploy_marchador_pos_mobile_stitch.py) *(Módulo POS Móvil: Marchar & Vender)*
- [`scripts/deploy_marchador_mobile_stitch.py`](../../scripts/deploy_marchador_mobile_stitch.py) *(Módulo Operaciones: Escáner, Marcado, Conteo y Etiquetas)*

---

## 🛒 Módulo A: Las 4 Pantallas de POS Móvil ("Cómo se Marcha y Vende en Pasillo")

Diseñadas para que el vendedor/marchador atienda al cliente caminando por el abasto, charcutería, frutería o tienda, armando el pedido en segundos y eligiendo entre **Marchar el pedido a la Caja Principal (Cola Cero)** o **Cobrar directamente en el teléfono**:

| N° | Vista POS Móvil | Screen ID en Google Stitch | Flujo de Venta / Despacho | Archivos Oficiales Exportados (`.png` & `.html`) |
| :---: | :--- | :---: | :--- | :--- |
| **01** | **POS Móvil — Venta en Pasillo & Catálogo Táctil** | [`2e54bb5383834a9a9d72b249f21476bf`](https://stitch.withgoogle.com/projects/15301442243370859300) | Catálogo 2 columnas + Cámara + Sticky Cart Bar (`Marchar a Caja` / `Cobrar Aquí`) | 🖼️ [`stitch_el_cuadre_marchador_pos_catalogo.png`](assets/stitch_el_cuadre_marchador_pos_catalogo.png) (399 KB)<br>💻 [`stitch_el_cuadre_marchador_pos_catalogo.html`](prototipos/stitch_el_cuadre_marchador_pos_catalogo.html) |
| **02** | **POS Móvil — Pesaje en Pasillo & Charcutería (Bottom-Sheet)** | [`1e35c6410cf14aa3b52fa7b1e661f951`](https://stitch.withgoogle.com/projects/15301442243370859300) | Balanza Wi-Fi + Botones `1/4`, `1/2`, `1 Kg` + **Modo Criollo *"Dame X Bs/$"*** | 🖼️ [`stitch_el_cuadre_marchador_pos_pesaje.png`](assets/stitch_el_cuadre_marchador_pos_pesaje.png) (653 KB)<br>💻 [`stitch_el_cuadre_marchador_pos_pesaje.html`](prototipos/stitch_el_cuadre_marchador_pos_pesaje.html) |
| **03** | **POS Móvil — Ticket Activo & "Marchar a Caja" (Cola Cero)** | [`37e5706cc856401b861de6454a245605`](https://stitch.withgoogle.com/projects/15301442243370859300) | Revisión de `#ORD-204`, identificación de cliente/cesta, QR Pre-Ticket y envío LAN | 🖼️ [`stitch_el_cuadre_marchador_pos_ticket.png`](assets/stitch_el_cuadre_marchador_pos_ticket.png) (325 KB)<br>💻 [`stitch_el_cuadre_marchador_pos_ticket.html`](prototipos/stitch_el_cuadre_marchador_pos_ticket.html) |
| **04** | **POS Móvil — Cobro Móvil Bimoneda en Sitio** | [`a1989a16f8494e88a61efdddcdcfd364`](https://stitch.withgoogle.com/projects/15301442243370859300) | Pago Móvil QR en pantalla, Efectivo Mixto `$/Bs`, Vuelto, Fiado y Ticket Bluetooth 58mm | 🖼️ [`stitch_el_cuadre_marchador_pos_cobro.png`](assets/stitch_el_cuadre_marchador_pos_cobro.png) (357 KB)<br>💻 [`stitch_el_cuadre_marchador_pos_cobro.html`](prototipos/stitch_el_cuadre_marchador_pos_cobro.html) |

---

## 🏷️ Módulo B: Las 4 Pantallas de Operaciones en Pasillo (Escáner, Marcado, Conteo y Etiquetas)

Diseñadas para la gestión de inventario en vivo, actualización de precios bimonetarios, recepción de camiones en depósito sin Wi-Fi e impresión portátil de habladores:

| N° | Vista Operativa Móvil | Screen ID en Google Stitch | Escenario Gherkin (US-19) | Archivos Oficiales Exportados (`.png` & `.html`) |
| :---: | :--- | :---: | :---: | :--- |
| **05** | **Escáner por Cámara & Buscador de Pasillo** | [`56370eaa8ec241a580731bf85ca5178c`](https://stitch.withgoogle.com/projects/15301442243370859300) | Escenario 1 (Consulta `<100ms`) | 🖼️ [`stitch_el_cuadre_marchador_escaner.png`](assets/stitch_el_cuadre_marchador_escaner.png) (600 KB)<br>💻 [`stitch_el_cuadre_marchador_escaner.html`](prototipos/stitch_el_cuadre_marchador_escaner.html) |
| **06** | **Ficha de Marcado Bimoneda (`$/Bs`) & Margen** | [`e29e95156ea348bfa6047aae92d5e4ca`](https://stitch.withgoogle.com/projects/15301442243370859300) | Escenario 1 (Edición Precio & Sync) | 🖼️ [`stitch_el_cuadre_marchador_marcado.png`](assets/stitch_el_cuadre_marchador_marcado.png) (210 KB)<br>💻 [`stitch_el_cuadre_marchador_marcado.html`](prototipos/stitch_el_cuadre_marchador_marcado.html) |
| **07** | **Recepción en Depósito & Conteo Offline-First** | [`774321dd5c084074b482e287eca88c06`](https://stitch.withgoogle.com/projects/15301442243370859300) | Escenarios 2 y 4 (Alta & SQLite Batch) | 🖼️ [`stitch_el_cuadre_marchador_conteo.png`](assets/stitch_el_cuadre_marchador_conteo.png) (326 KB)<br>💻 [`stitch_el_cuadre_marchador_conteo.html`](prototipos/stitch_el_cuadre_marchador_conteo.html) |
| **08** | **Cola de Habladores & Impresión Bluetooth 50x30mm** | [`5c47cdeb43d244fc859da0a4ba9fe7e9`](https://stitch.withgoogle.com/projects/15301442243370859300) | Escenario 3 (Etiquetas Code-128 / TSPL) | 🖼️ [`stitch_el_cuadre_marchador_etiquetas.png`](assets/stitch_el_cuadre_marchador_etiquetas.png) (351 KB)<br>💻 [`stitch_el_cuadre_marchador_etiquetas.html`](prototipos/stitch_el_cuadre_marchador_etiquetas.html) |

---

## 🏛️ 1. Anatomía del Flujo "¿Cómo se Marcha y Vende en Mobile?"

En el comercio venezolano de alto tráfico (fruterías, charcuterías, ferreterías y bodegones), el cuello de botella ocurre en la taquilla de cobro. **El Cuadre Marchador POS** resuelve esto con **dos modalidades de despacho desde la palma de la mano**:

1. **Armado Ultrarrápido en Pasillo (`2e54bb5383834a9a9d72b249f21476bf`)**:
   - El marchador acompaña al cliente; escanea productos empaquetados con la cámara o pulsa sobre la cuadrícula táctil de 2 columnas (*Harina P.A.N., Aceite Mazeite, Queso Blanco, Tomate Perita*).
   - Una **Barra Flotante de Pedido Activo (`Sticky Cart Bar`)** permanece fija en la zona inferior del pulgar mostrando `🧾 Pedido #ORD-204 • 5 Artículos • $12.40 USD | Bs. 558.00` con doble disparo: **`🚀 Marchar a Caja`** o **`💳 Cobrar Aquí`**.
2. **Pesaje Inteligente y Modo Criollo *"Dame X Bolívares / Dólares"* (`1e35c6410cf14aa3b52fa7b1e661f951`)**:
   - Al tocar un producto de charcutería o frutería por peso, se despliega un Bottom Sheet conectado por Wi-Fi a la balanza de pasillo (o entrada manual).
   - Incluye atajos criollos (`1/4 Kg`, `1/2 Kg`, `3/4 Kg`, `1 Kg`) y la calculadora inversa **"Dame por Monto"**: si el cliente dice *"Dame Bs. 150 de queso blanco"*, la app divide automáticamente entre el precio en Bs/Kg y le indica al charcutero: **`Cortar exactamente: 0.575 Kg`**.
3. **Despacho "Marchar a Caja Principal — Cola Cero" (`37e5706cc856401b861de6454a245605`)**:
   - El marchador etiqueta el pedido con una referencia visual rápida (*"👤 Cliente: Doña Carmen — Cesta Roja #04"*) y presiona **`🚀 MARCHAR PEDIDO A CAJA PRINCIPAL`**.
   - El pedido entra instantáneamente (`POST /api/orders/marchador-dispatch`) en la pantalla de la Caja Principal del mostrador y genera un **QR de Pre-Ticket** (en pantalla o impreso en ticketera Bluetooth de cintura) para que el cliente solo pague y retire.
4. **Cobro Autónomo en Sitio (`a1989a16f8494e88a61efdddcdcfd364`)**:
   - Si el cliente paga con **Pago Móvil** o **Efectivo exacto**, el mismo marchador le muestra en pantalla el **Código QR Dinámico de Pago Móvil** con el monto exacto en Bolívares (`Bs. 333.00`), valida los últimos 4 dígitos de la referencia (`8492`), combina efectivo `$` + `Bs.`, o lo registra en el **Libro de Fiados**, emitiendo el recibo en su impresora térmica Bluetooth portátil (`58mm`).

---

## 🎨 2. Design Tokens Oficiales para Flutter (`ThemeData`)

| Token Semántico | Hex | Flutter `Color` | Tipografía & Uso en `el-cuadre-mobile` |
| :--- | :---: | :---: | :--- |
| **Background Deep Slate** | `#020617` | `Color(0xFF020617)` | `Scaffold.backgroundColor` — ahorro de batería OLED en pasillo. |
| **Card Surface** | `#0F172A` | `Color(0xFF0F172A)` | Tarjetas de producto, bottom sheets y paneles de conteo. |
| **Elevated Container** | `#1E293B` | `Color(0xFF1E293B)` | Inputs numéricos, píldoras de margen y bordes táctiles. |
| **Primary Emerald (USD)** | `#10B981` | `Color(0xFF10B981)` | `Space Grotesk Bold` — Precios en $, botón *Cobrar Aquí* y CTAs primarios. |
| **Accent Amber (BCV Bs)** | `#F59E0B` | `Color(0xFFF59E0B)` | `JetBrains Mono Bold` — Precios en Bs. BCV, botón *Marchar a Caja* y alertas Offline. |
| **Scale Cyan (Weight Kg)** | `#38BDF8` | `Color(0xFF38BDF8)` | `JetBrains Mono` — Indicadores de balanza (`0.650 Kg`) y conversión inversa de gramos. |
| **Text Primary** | `#F8FAFC` | `Color(0xFFF8FAFC)` | `Inter SemiBold` — Nombres de productos y encabezados. |

---

## 🛠️ 3. Directrices de Implementación para el Clan Akatsuki

### 🦈 Para Kisame (`kisame-mobile` — Flutter & Dart)
1. **Arquitectura BLoC**:
   - `MobilePosCartBloc`: Gestión reactiva del carrito en pasillo, cálculo bimonetario en tiempo real y calculadora inversa `targetAmountBs / (priceUsd * bcvRate) = exactWeightKg`.
   - `OrderDispatchBloc`: Despacho LAN `POST /api/orders/parked` (Pre-venta / Marchar a Caja) y generación de código QR `ELCUADRE://ORD-204`.
   - `ScannerLookupBloc`, `PriceTaggingBloc`, `OfflineSyncBloc` y `ThermalPrintBloc` (soportando recibos de `58mm` ESC/POS y etiquetas adhesivas de `50x30mm` TSPL).

### 🖤 Para Kakuzu (`kakuzu-backend` — NestJS & SQLite WAL)
1. **Endpoints de Venta & Sincronización LAN**:
   - `POST /api/orders/marchador`: Recibe la comanda armada por el marchador (`status: MARCHADO_EN_PASILLO`) y emite un evento WebSocket/SSE a la Caja Principal para que aparezca de inmediato en la bandeja de **"Pedidos Marchados por Cobrar"**.
   - `POST /api/sales/mobile-checkout`: Procesa el cobro completo desde el celular, descuenta el stock en SQLite (`prisma.$transaction`) y registra los pagos mixtos (`USD_CASH`, `BS_PAGO_MOVIL`, `FIADO`).
   - `GET /api/products/barcode/:code`, `PATCH /api/products/:id` y `POST /api/products/batch-sync`.
