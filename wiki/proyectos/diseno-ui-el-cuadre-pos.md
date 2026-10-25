---
title: "Especificación UI/UX: El Cuadre POS (Google Stitch - Suite Completa de 6 Vistas)"
type: "concept"
area: "proyectos"
status: "completed"
created: 2026-10-24
updated: 2026-10-24
tags:
  - konan-uiux
  - stitch
  - el-cuadre-pos
  - design-tokens
  - tailwind
  - pos
  - meniox-market
---

# 🦋 Suite Completa de Diseño UI/UX en Google Stitch: EL CUADRE POS
**Diseñadora Líder**: 🦋 Konan (El Ángel de Dios — UI/UX Designer Akatsuki)  
**Herramienta Oficial**: **Google Stitch API** (`https://stitch.googleapis.com/mcp`)  
**Proyecto Google Stitch**: `projects/15301442243370859300` ("El Cuadre POS - Widescreen Touch Terminal")  
**Design System Oficial Stitch**: `El Cuadre POS` (`assets/51495007ab54497bac424dfa184a26ff`)  
**Lista en ClickUp**: [📊 EL CUADRE POS en ClickUp](https://app.clickup.com/90141555783/v/li/901422611886)  

---

## 🎨 Las 6 Vistas Oficiales Generadas en Google Stitch

Cada pantalla responde directamente al desglose de Historias de Usuario (US) gestionadas por **Pain** en ClickUp:

| Vista | Nombre en Google Stitch | Screen ID en Stitch | US en ClickUp | Archivos Locales Descargados |
| :---: | :--- | :--- | :---: | :--- |
| **01** | **Caja Táctica POS (Widescreen Terminal)** | `a40df8b2126b402ca037e3a082d12d6e` | US-04 | 🖼️ [`stitch_el_cuadre_pos.png`](file:///c:/Users/vmont/OneDrive/Desktop/2brain-vmontoya/wiki/proyectos/assets/stitch_el_cuadre_pos.png)<br>💻 [`stitch_el_cuadre_pos.html`](file:///c:/Users/vmont/OneDrive/Desktop/2brain-vmontoya/wiki/proyectos/prototipos/stitch_el_cuadre_pos.html) |
| **02** | **Balanza de Pesaje (Produce Scale Modal)** | `4b659cc336f24f669be18b7414a436ed` | US-01 / US-04 | 🖼️ [`stitch_el_cuadre_pesaje.png`](file:///c:/Users/vmont/OneDrive/Desktop/2brain-vmontoya/wiki/proyectos/assets/stitch_el_cuadre_pesaje.png)<br>💻 [`stitch_el_cuadre_pesaje.html`](file:///c:/Users/vmont/OneDrive/Desktop/2brain-vmontoya/wiki/proyectos/prototipos/stitch_el_cuadre_pesaje.html) |
| **03** | **Pasarela de Cobro Bimoneda (Checkout Modal)** | `bdfab85bfedd4b2eab4849ccfeafff23` | US-05 | 🖼️ [`stitch_el_cuadre_cobro.png`](file:///c:/Users/vmont/OneDrive/Desktop/2brain-vmontoya/wiki/proyectos/assets/stitch_el_cuadre_cobro.png)<br>💻 [`stitch_el_cuadre_cobro.html`](file:///c:/Users/vmont/OneDrive/Desktop/2brain-vmontoya/wiki/proyectos/prototipos/stitch_el_cuadre_cobro.html) |
| **04** | **Cierre de Turno & Arqueo Diario (El Cuadre)** | `b0aadeab9ad34d258ddd181bfc2b7ca8` | US-03 / US-07 | 🖼️ [`stitch_el_cuadre_arqueo.png`](file:///c:/Users/vmont/OneDrive/Desktop/2brain-vmontoya/wiki/proyectos/assets/stitch_el_cuadre_arqueo.png)<br>💻 [`stitch_el_cuadre_arqueo.html`](file:///c:/Users/vmont/OneDrive/Desktop/2brain-vmontoya/wiki/proyectos/prototipos/stitch_el_cuadre_arqueo.html) |
| **05** | **Libro de Fiados Digital (Cuentas por Cobrar)** | `40e273f7f19d48c89d42ae51ca18c92d` | US-10 | 🖼️ [`stitch_el_cuadre_fiados.png`](file:///c:/Users/vmont/OneDrive/Desktop/2brain-vmontoya/wiki/proyectos/assets/stitch_el_cuadre_fiados.png)<br>💻 [`stitch_el_cuadre_fiados.html`](file:///c:/Users/vmont/OneDrive/Desktop/2brain-vmontoya/wiki/proyectos/prototipos/stitch_el_cuadre_fiados.html) |
| **06** | **Inventario Híbrido & Control de Mermas** | `3ecddedc4a0148c397cd3b62d7f3011d` | US-06 | 🖼️ [`stitch_el_cuadre_inventario.png`](file:///c:/Users/vmont/OneDrive/Desktop/2brain-vmontoya/wiki/proyectos/assets/stitch_el_cuadre_inventario.png)<br>💻 [`stitch_el_cuadre_inventario.html`](file:///c:/Users/vmont/OneDrive/Desktop/2brain-vmontoya/wiki/proyectos/prototipos/stitch_el_cuadre_inventario.html) |

---

## 🏛️ Desglose Visual & Funcional de Cada Vista

### 1. Vista Principal: Caja Táctica POS
- **Propósito**: Pantalla dividida táctil (60% catálogo / 40% ticket activo).
- **Características**: Buscador predictivo con escáner de código de barras, filtros por categoría (`Frutas & Verduras por Kg`, `Víveres Empacados`, `Charcutería`, `Bebidas`), badges de doble precio ($ y Bs.) y botón gigante de cobro.

### 2. Modal de Pesaje & Balanza Digital
- **Propósito**: Manejo de productos a granel sin calculadora manual.
- **Características**: LCD digital en vivo (`1.450 Kg`), botones de peso rápido criollos (`1/4 Kg`, `1/2 Kg`, `1 Kg`, `2 Kg`), teclado numérico para gramos exactos, botón de tara y visor de subtotal reactivo.

### 3. Pasarela de Cobro Bimonetario & Vueltos
- **Propósito**: Agilizar la cola y eliminar errores de vuelto en efectivo y digital.
- **Características**: Pestañas de método de pago (Efectivo $, Efectivo Bs, Pago Móvil dinámico con código QR + RIF/Teléfono + referencia, Punto Bancario con voucher y Fiado). Calculador automático de vuelto en verde fosforescente.

### 4. Cierre de Turno & Arqueo Diario (El Cuadre)
- **Propósito**: Cuadre ciego del turno en 2 minutos.
- **Características**: Comparativa de Lote del Punto vs Sistema, total en banco de Pago Móvil vs Sistema, conteo físico de gaveta ($ y Bs.) con detección de sobrantes/faltantes, registro de gastos menores (hielo, bolsas) y botón de reporte a WhatsApp.

### 5. Libro de Fiados Digital (Cuentas por Cobrar)
- **Propósito**: Erradicar el cuaderno de papel y lápiz en las cuentas corrientes de vecinos.
- **Características**: Tarjetas de clientes con saldo adeudado, límite de crédito, historial de compras, botón de "Registrar Abono ($ o Pago Móvil)" y botón directo para enviar recordatorio de saldo por WhatsApp.

### 6. Inventario Híbrido & Control de Mermas
- **Propósito**: Mantener el inventario cuadrado entre productos secos y perecederos.
- **Características**: Tabla de stock dual (decimales para Kg vs enteros para unidades), alertas de stock mínimo crítico, y modal de **Baja por Merma / Pudrición** (motivo: pudrición, maduración excesiva o golpe) para ajustar stock real sin registrar ventas falsas.
