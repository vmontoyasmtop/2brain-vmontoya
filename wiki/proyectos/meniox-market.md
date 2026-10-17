---
title: "Proyecto: Meniox Market — Cloud POS & Gestión para Fruterías, Minimarkets y Víveres"
type: "project"
area: "proyectos"
status: "planning"
created: 2026-10-16
updated: 2026-10-16
tags:
  - meniox
  - meniox-market
  - pos
  - retail
  - fruteria
  - viveres
  - bimonetario
  - pagos-mixtos
---

# 🛒 Proyecto: Meniox Market — Cloud POS para Fruterías, Minimarkets y Víveres

**Meniox Market** es una extensión del ecosistema **Meniox**, adaptada como un sistema de punto de venta (POS) y gestión operativa ágil para pequeños y medianos comercios de alimentos (fruterías, verdulerías, bodegones y abastos de víveres).

Su misión fundamental es **sustituir el cuaderno manual de papel y lápiz** por una plataforma digital ultrarrápida, moderna e intuitiva, que opera sobre internet cotidiano y resuelve los cuellos de botella reales de estos comercios: **pesaje a granel, pagos en punto de débito y pago móvil, cuentas por cobrar (fiados) y arqueo de caja sin discrepancias**.

---

## 🎯 1. Perfil del Negocio y Diagnóstico Operativo

| Dimensión | Realidad Operativa Actual | Solución con Meniox Market |
| :--- | :--- | :--- |
| **Registro de Ventas** | Cuaderno de hojas y papel; notas sueltas propensas a extravío y borrones. | **Caja Web Táctil / Numérica**: Registro de venta en 3 clics, con o sin mouse. |
| **Frutas y Verduras** | Pesaje manual en balanza; cálculo mental o calculadora para saber el monto. | **Malla Táctil con Selector de Peso**: Ingreso de Kilos/Gramos y cálculo automático. |
| **Cobro en Bs.** | Punto de venta bancario y Pago Móvil con verificación en celular. | **Módulo Bimonetario Integrado**: Registro de referencia de voucher y de Pago Móvil. |
| **Cierre de Jornada** | Conteo manual que toma 1 hora; descuadres entre efectivo y banco. | **Arqueo Ciego en 1 Clic**: Cuadre automático de Punto, Pago Móvil y Gaveta. |
| **Fiados / Clientes** | Anotados en páginas de libreta; olvidos de cobro y pérdidas de capital. | **Módulo de Crédito / Cuentas por Cobrar**: Saldo pendiente y abonos por cliente. |

---

## 🏗️ 2. Arquitectura de Producto (Local-First On-Premise & LAN)

Apalancándose en los componentes ya probados de **Meniox** (core transaccional), **Xetux** (lógica de caja bimonetaria) y **MasterHub** (diseño UI limpio y reactivo), el sistema opera con arquitectura **Local-First On-Premise**:

```mermaid
flowchart TD
    subgraph TIENDA["🏪 Red Local de la Tienda (LAN / Wi-Fi)"]
        HOST["🖥️ Servidor Local / PC Caja Principal\n• Core Standalone Meniox Market\n• Base de Datos Local Embebida\n• Operación 100% Offline (Zero Downtime)"]
        
        TERM2["📱 Terminal 2 / Tablet Pesaje"]
        BAL["⚖️ Balanza Mostrador"]
        PRN["🖨️ Impresora Térmica 58/80mm (ESC/POS)"]
        BANC["💳 Punto de Débito (Voucher)"]
        PM["📱 Pago Móvil (QR / Ref)"]

        HOST --- BAL
        HOST --- PRN
        TERM2 -.->|Wi-Fi Local (192.168.x.x)| HOST
    end

    subgraph CLOUD["☁️ Nube Opcional"]
        CLOUD_BACKUP["🔄 Backup Automático & Sync Tasa BCV"]
    end

    HOST -.->|Cuando hay Conexión| CLOUD_BACKUP
```

---

## 🌟 3. Flujo Operativo Paso a Paso (La Experiencia del Cajero)

### Paso 1: Ingreso de Ítems al Ticket
* **Frutas y Verduras (A Granel / Peso)**:
  - Malla visual con fotos grandes de productos comunes (Tomate, Cebolla, Papa, Plátano, Aguacate, Cambur, Zanahoria).
  - Al pulsar el botón, se abre un teclado numérico táctil donde se digita el peso en la balanza (ej. `1.250` Kg o botones de `1/2 Kg`, `1 Kg`, `2 Kg`). El sistema multiplica precio $\times$ peso automáticamente.
* **Víveres Empacados (Por Unidad)**:
  - Búsqueda por nombre predictivo o escaneo de código de barras tradicional (Harina, Arroz, Aceite, Enlatados, Bebidas).

### Paso 2: Cobro Multimoneda & Pagos Mixtos
La pantalla muestra el total exacto en **Dólares ($)** y en **Bolívares (Bs.)** según la tasa del día.
El cajero selecciona cómo paga el cliente:
* `[ 💳 Punto de Venta ]`: Registra el monto cobrado en el terminal bancario y opcionalmente los últimos 4 dígitos del voucher.
* `[ 📱 Pago Móvil ]`: Muestra en pantalla el QR con los datos del comercio (Teléfono, Cédula/RIF, Banco) y campo para los 4 dígitos de la referencia.
* `[ 💵 Efectivo $ / Bs. ]`: Calculador de cambio/vuelto exacto en la moneda que se entregue.
* `[ 🤝 Cuenta Pendiente / Fiado ]`: Si el cliente es habitual y completa el pago luego, se asigna a su cuenta personal con límite de crédito.

### Paso 3: Cierre de Caja & Arqueo Diario
Al finalizar la jornada laboral:
1. El cajero o dueño presiona **"Cerrar Turno / Arqueo"**.
2. El sistema genera un consolidado automático:
   - **Total Punto de Débito**: Debe coincidir exactamente con el reporte "Lote / Cierre" del POS bancario.
   - **Total Pago Móvil**: Monto exacto recibido en la cuenta bancaria.
   - **Total Efectivo $ y Bs.**: Monto exacto que debe haber en la gaveta física.
3. Permite imprimir el resumen en ticket o **enviarlo por WhatsApp al dueño** con un solo toque.

---

## 🗺️ 4. Hoja de Ruta de Implementación

### 🔹 Fase 1: Core del POS & Catálogo Bimonetario (MVP)
- [ ] Configuración del proyecto web (PWA ligera responsive para PC/Laptop o Tablet).
- [ ] Catálogo de productos: soporte dual para ítems pesables (Kg) e ítems por unidad.
- [ ] Tasa de cambio editable con actualización a tasa oficial o manual.
- [ ] Carrito de compras con cálculo automático de peso $\times$ precio.

### 🔹 Fase 2: Pasarela de Cobro y Cierre de Caja
- [ ] Registro de pagos mixtos (Punto de Venta + Pago Móvil + Efectivo).
- [ ] Control de apertura y cierre de caja con arqueo por método de pago.
- [ ] Registro rápido de gastos operativos diarios (ej. *"Pago transporte"*, *"Compra hielo/bolsas"*).

### 🔹 Fase 3: Gestión de Mermas & Cuentas por Cobrar (Fiados)
- [ ] Registro de mermas y frutas dañadas para ajuste de inventario real.
- [ ] Directorio de clientes habituales y control de saldo pendiente (libro de fiados digital).
- [ ] Dashboard móvil para el dueño con ventas del día y ganancias estimadas.

---
*Documento registrado en 2brain — Proyectos Personales de Víctor Montoya.*
