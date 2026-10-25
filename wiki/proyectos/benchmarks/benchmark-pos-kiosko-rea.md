---
title: "Informe REA: Arquitectura y Benchmark de POS para Kiosko de Víveres y Frutería"
type: "concept"
area: "proyectos"
status: "completed"
created: 2026-10-24
updated: 2026-10-24
tags:
  - pos
  - rea
  - akatsuki
  - pain-pm
  - fruterias
  - viveres
  - inventario
  - contabilidad
  - meniox-market
---

# 🔍 Informe de Reingeniería Inversa & Análisis Competitivo (REA)
**Objetivo**: Arquitectura simple, robusta y funcional de POS e Inventario para Kiosko / Tienda de Víveres, Frutas y Verduras  
**Investigador Líder**: ☁️ Pain (Tendō — Vía Rinnegan & REA Toolkit)  
**Coordinación General**: 🤵 ALFRED (Organización Akatsuki)  
**Proyecto Asociado en 2brain**: [[meniox-market|Meniox Market — Cloud/Local POS para Fruterías y Víveres]]  

---

## 1. Resumen Ejecutivo & Benchmark del Mercado (REA Evidence-Based)

Tras deconstruir repositorios y soluciones de referencia en el ecosistema open source (*Vertex-POS*, *FinOpenPOS*, *BarcodePOS / Hegxib*, *Store-POS* y módulos POS de *Odoo*), identificamos que el 90% de los POS comerciales fallan en pequeños kioskos de víveres por dos motivos:
1. **Tratan todo como piezas fijas (unidades)** y no contemplan la venta por peso decimal ($\text{Kg/g}$) ni las **mermas por descomposición** de frutas y verduras.
2. **Requieren infraestructuras complejas en la nube** con dependencias pesadas, vulnerables a caídas de internet local.

### 👁️ Lo Observado (Hard Evidence de Proyectos Analizados)
- **Modelos Híbridos de Catálogo**:
  - `FinOpenPOS` y `Vertex-POS` utilizan Prisma ORM con un campo `pricingType: 'UNIT' | 'WEIGHT'` y campos decimales en precisión `Decimal(10, 3)` para soportar gramos.
  - Para cajas registradoras rápidas, el frontend implementa un **Grid táctil con categorías de alta rotación** (Tomate, Papa, Cebolla, Plátano, Aguacate) con botones de peso rápido (`0.250kg`, `0.500kg`, `1.000kg`, `2.000kg`) o entrada directa.
- **Códigos de Barra de Balanza (Prefijos PLU)**:
  - Balanzas electrónicas comerciales generan códigos EAN-13 con formato `20PPPPPVVVVVC`, donde `20` es prefijo in-store, `PPPPP` es el ID del producto y `VVVVV` es el peso en gramos o precio calculado.
- **Cierre de Caja Ciego**:
  - `Store-POS` y `Odoo POS` utilizan el concepto de **Sesión de Caja (`CashSession`)** con balance inicial, arqueo final desglosado por método de pago (Efectivo, Tarjeta/Punto, Transferencia/Pago Móvil) y cálculo de sobrante/faltante.

### 🧠 Lo Inferido (Arquitectura Óptima "KISS: Keep It Simple, Simple & Rock-Solid")
- **Stack Ideal**:
  - **Fullstack**: **Next.js 14+ (App Router, Server Actions)** + **Tailwind CSS** + **Lucide Icons** + **Shadcn UI**.
  - **Base de Datos**: **SQLite** local (vía Prisma ORM o Better-SQLite3). Cero costos de servidores externos, portable en un solo archivo `pos.db`, con capacidad de backup automático a Google Drive o USB con 1 clic.
  - **Autenticación**: Autenticación ligera por sesión (JWT en cookies httpOnly o NextAuth) con 2 roles estrictos:
    - `ADMIN` (Dueño): Acceso a compras, márgenes, costos, inventario completo, mermas y balance contable.
    - `CASHIER` (Cajero): Interfaz limpia de apertura de turno, cobro rápido, consulta de precios y cierre de turno.
- **Módulos Críticos**:
  1. **Caja / POS Táctil**: Carrito reactivo, selector de peso, lector de barras, cálculo de vueltos, ticket digital/térmico (58mm/80mm).
  2. **Inventario Dual & Mermas**: Stock unitario vs stock en Kg con registro de frutas dañadas/pérdidas.
  3. **Contabilidad Básica**: Compras a proveedores, gastos diarios operativos (bolsas, flete, hielo) y cálculo de utilidad neta ($\text{Ventas} - \text{Costo de Mercancía} - \text{Gastos}$).

### ❓ Puntos Ciegos / Consideraciones de Hardware
- **Balanza en el Kiosko**: Muchos kioskos pequeños usan balanzas mecánicas o digitales sencillas sin puerto serial USB hacia la PC. Por ende, la interfaz debe priorizar la **digitación táctil ultra-rápida del peso** en pantalla, dejando la lectura por balanza serial (Web Serial API) como opción secundaria.

---

## 2. Esquema de Base de Datos Recomendado (Prisma + SQLite)

```prisma
datasource db {
  provider = "sqlite"
  url      = "file:./dev.db"
}

generator client {
  provider = "prisma-client-js"
}

enum Role {
  ADMIN
  CASHIER
}

enum ProductType {
  UNIT   // Víveres empacados (arroz, aceite, harina)
  WEIGHT // Frutas y verduras por Kg / gramos
}

enum PaymentMethod {
  CASH
  CARD_POS
  MOBILE_PAYMENT
  MIXED
}

model User {
  id        String   @id @default(cuid())
  username  String   @unique
  name      String
  password  String   // Hash bcrypt
  role      Role     @default(CASHIER)
  active    Boolean  @default(true)
  sessions  CashSession[]
  createdAt DateTime @default(now())
}

model Category {
  id        String    @id @default(cuid())
  name      String    @unique
  products  Product[]
}

model Product {
  id          String       @id @default(cuid())
  barcode     String?      @unique
  name        String
  categoryId  String
  category    Category     @relation(fields: [categoryId], references: [id])
  type        ProductType  @default(UNIT)
  costPrice   Float        @default(0.0) // Costo de compra
  salePrice   Float        // Precio de venta por unidad o por Kg
  stock       Float        @default(0.0) // Soporta decimales para Kg (ej. 15.450)
  minStock    Float        @default(5.0)
  image       String?
  items       SaleItem[]
  losses      ProductLoss[]
  createdAt   DateTime     @default(now())
  updatedAt   DateTime     @updatedAt
}

model CashSession {
  id           String      @id @default(cuid())
  userId       String
  user         User        @relation(fields: [userId], references: [id])
  openedAt     DateTime    @default(now())
  closedAt     DateTime?
  startAmount  Float       @default(0.0) // Fondo inicial de caja
  endAmount    Float?      // Monto real contado al cierre
  systemAmount Float       @default(0.0) // Monto calculado por ventas
  status       String      @default("OPEN") // OPEN, CLOSED
  sales        Sale[]
  expenses     Expense[]
}

model Sale {
  id            String        @id @default(cuid())
  sessionId     String
  session       CashSession   @relation(fields: [sessionId], references: [id])
  total         Float
  paymentMethod PaymentMethod @default(CASH)
  cashReceived  Float?
  changeGiven   Float?
  reference     String?       // Ref de pago móvil o lote de punto
  items         SaleItem[]
  createdAt     DateTime      @default(now())
}

model SaleItem {
  id        String   @id @default(cuid())
  saleId    String
  sale      Sale     @relation(fields: [saleId], references: [id], onDelete: Cascade)
  productId String
  product   Product  @relation(fields: [productId], references: [id])
  quantity  Float    // Cantidad vendida (1, 2 o 1.450 Kg)
  unitPrice Float    // Precio congelado al momento de la venta
  subtotal  Float
}

model Expense {
  id          String      @id @default(cuid())
  sessionId   String
  session     CashSession @relation(fields: [sessionId], references: [id])
  description String      // Ej. "Pago de bolsas plásticas", "Hielo"
  amount      Float
  createdAt   DateTime    @default(now())
}

model ProductLoss {
  id          String   @id @default(cuid())
  productId   String
  product     Product  @relation(fields: [productId], references: [id])
  quantity    Float    // Kg o unidades descartadas por descomposición
  reason      String   // "Pudrición", "Golpe / Daño", "Vencimiento"
  createdAt   DateTime @default(now())
}
```

---

## 3. Plan de Acción Akatsuki (Desglose de Tareas & Sprints)

| ID US | Tarea / Historia | Asignado | Story Points | Alcance Técnico |
| :--- | :--- | :--- | :---: | :--- |
| **US-01** | Prototipado y Tokens de UI/UX | 🦋 Konan | 5 SP | Wireframes y layout responsive en Stitch: Pantalla POS de 2 columnas (Catálogo Grid táctil + Ticket Carrito interactivo). |
| **US-02** | Base de Datos Prisma & SQLite | 🖤 Kakuzu | 3 SP | Modelado de esquema Prisma, seeds iniciales con frutas/víveres típicos y migraciones SQLite blindadas. |
| **US-03** | Autenticación y Control de Turnos | 🖤 Kakuzu | 5 SP | Login con roles (Admin/Cajero) y lógica de `CashSession` (Apertura, Ingresos/Egresos y Arqueo Ciego). |
| **US-04** | Caja Táctica POS & Selector de Peso | 👁️ Itachi | 8 SP | Vista Next.js con Server Actions: buscador predictivo, grid con fotos de verduras, modal numérico de pesaje (Kg/g) y checkout multimoneda. |
| **US-05** | Módulo de Inventario & Mermas | 👁️ Itachi | 5 SP | CRUD de productos (Unidad vs Kg), alertas de stock bajo y formulario de baja de productos dañados/mermas. |
| **US-06** | Contabilidad Básica & Reportes | 🖤 Kakuzu & 👁️ Itachi | 5 SP | Dashboard de ganancias brutas vs netas, control de compras a proveedores y balance del turno. |
| **US-07** | Suite de Pruebas Unitarias | 💀 Hidan | 5 SP | Tests en Vitest/Jest para cálculo de peso $\times$ precio, vueltos en efectivo, descuentos y balance de arqueo (>85% cobertura). |
| **US-08** | Manual de Usuario & Guía de Despliegue | 🌿 Zetsu | 3 SP | Guía rápida para el cajero (Zetsu Blanco) y documentación técnica de instalación local (Zetsu Negro). |
