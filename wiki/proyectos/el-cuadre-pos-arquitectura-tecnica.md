---
title: "Arquitectura Técnica & Plan Maestro: EL CUADRE POS"
type: "concept"
area: "proyectos"
status: "active"
created: 2026-10-24
updated: 2026-10-24
tags:
  - pain-pm
  - orochimaru-arch
  - zetsu-docs
  - el-cuadre-pos
  - nestjs
  - sqlite-wal
  - nextjs
  - flutter
  - offline-first
  - meniox-market
---

# 🌿 Blueprint de Arquitectura Técnica & Especificación Funcional: EL CUADRE POS
**Líderes de Proyecto & Arquitectura**: ☁️ Pain (PM & Scrum Master) & 🐍 Orochimaru (Chief Architect & DevOps)  
**Redacción & Estandarización Documental**: 🌿 Zetsu (🌑 Zetsu Negro / ⚪ Zetsu Blanco)  
**Entorno de Ejecución**: `C:\Users\vmont\OneDrive\Desktop\el-cuadre-pos`  
**Lista Oficial en ClickUp**: [📊 EL CUADRE POS (ID: 901422611886)](https://app.clickup.com/90141555783/v/li/901422611886)  

---

## 👥 Equipo de Desarrollo Akatsuki

| Miembro | Rol | Misión en EL CUADRE POS |
| :--- | :--- | :--- |
| ☁️ **Pain** | Project Manager & Scrum Master | Gestión de Épicas, User Stories Gherkin y Sprints en ClickUp. |
| 🐍 **Orochimaru** | Chief Software Architect & DevOps | Diseño de Arquitectura Hexagonal, SQLite WAL y Outbox Pattern. |
| 🦋 **Konan** | UI/UX Designer (Stitch) | Suite de 6 pantallas y Design System en Google Stitch. |
| 🖤 **Kakuzu** | Backend & Database Architect | NestJS, Prisma ORM, transacciones atómicas SQLite y DTOs Swagger. |
| 👁️ **Itachi** | Frontend Web Engineer | Terminal táctil POS en Next.js App Router, Tailwind & Shadcn UI. |
| 🦈 **Kisame** | Mobile Engineer | App móvil en Flutter (BLoC) para pesaje y pedidos por Wi-Fi LAN. |
| 💀 **Hidan** | QA Engineer & Stress Tester | Pruebas unitarias e integración en Vitest/Jest (>85% cobertura). |
| 💣 **Deidara** | Pentesting & Red Team | Hacking ético, auditoría de inyecciones y seguridad local. |
| 🦂 **Sasori** | Ciberseguridad Blue Team | Hardening de base de datos, cifrado bcrypt y validación de DTOs. |
| 🌿 **Zetsu** | Docs Specialist & Chronicler | Especificaciones OpenAPI, diagramas C4 y manuales de cajero. |
| 👑 **El Señor** | Dueño del Producto & Aprobación UAT | Pruebas finales de aceptación en entorno real. |

---

## 🌑 Documentación Técnica (Zetsu Negro & Orochimaru)

### 1. Topología del Sistema: Monolito Hexagonal Local Edge + LAN

EL CUADRE POS está concebido para operar bajo condiciones severas de conectividad (cortes de luz, fallos de internet, inestabilidad de red). Funciona como un **Edge Server Local** en el mostrador:

```mermaid
flowchart TD
    subgraph LAN ["🏢 Red Local del Abasto / Kiosko (100% Offline-First)"]
        subgraph Terminal_Principal ["🖥️ Terminal Principal (PC Mostrador)"]
            UI["💻 Frontend Web POS (Next.js / Itachi)<br/>Puerto 3000"]
            Nest["⚙️ Backend API (NestJS / Kakuzu)<br/>Puerto 3001"]
            DB[("💾 SQLite WAL Engine<br/>elcuadre.db")]
            Perif["🔌 Periféricos Locales<br/>Balanza USB/RS232 + Impresora Térmica + Lector"]
        end

        subgraph Dispositivos_Moviles ["📱 Dispositivos Auxiliares en Tienda"]
            Mob1["📱 Teléfono Dueño (Flutter / Kisame)<br/>Toma de Pedidos en Pasillo"]
            Tab2["📟 Tablet Frutería / Charcutería<br/>Pesaje Remoto en Balanza"]
        end

        UI -->|HTTP / WebSocket| Nest
        Mob1 -->|Wi-Fi LAN / IP 192.168.1.X:3001| Nest
        Tab2 -->|Wi-Fi LAN / IP 192.168.1.X:3001| Nest
        Nest -->|Prisma ORM / Latencia < 2ms| DB
        Nest -->|Driver Serial / ESC-POS| Perif
    end

    subgraph Nube ["☁️ Nube Opcional (Telemetría & Backup)"]
        OutboxWorker["📦 Outbox Sync Worker"]
        CloudDB[("🌐 Cloud Postgres / Coolify")]
    end

    Nest --> OutboxWorker
    OutboxWorker -.->|Sincronización Asíncrona cuando haya Internet| CloudDB
```

---

### 2. Diagrama de Secuencia: Ciclo de Cobro Táctico Multimoneda

```mermaid
sequenceDiagram
    autonumber
    actor C as 🧑‍💼 Cajero
    participant UI as 🖥️ Frontend POS (Itachi)
    participant API as ⚙️ Backend NestJS (Kakuzu)
    participant DB as 💾 SQLite WAL (elcuadre.db)
    participant P as 🖨️ Impresora Térmica

    C->>UI: Escanea código de barras o selecciona Fruta (Kg)
    UI->>UI: Calcula precio en USD y Bs según tasa activa
    C->>UI: Presiona botón gigante "COBRAR TICKET"
    UI->>C: Muestra Modal de Pagos (Efectivo $, Bs, Pago Móvil, Fiado)
    C->>UI: Ingresa monto recibido (Ej: Billete $20 para ticket de $14.50)
    UI->>UI: Calcula vuelto exacto ($5.50 o equivalente en Bs)
    C->>UI: Confirma Transacción
    UI->>API: POST /api/sales (Payload de Venta Atómica)
    activate API
    API->>DB: BEGIN TRANSACTION
    API->>DB: INSERT into Sale & SaleItem
    API->>DB: INSERT into Payment (Desglose de métodos)
    API->>DB: UPDATE Product Stock (Resta Kg o Unidades)
    API->>DB: COMMIT TRANSACTION
    deactivate API
    API-->>UI: 201 Created (Sale ID & Recibo Generado)
    UI->>P: Emisión de Ticket de Vuelto / Comprobante
    UI->>UI: Limpia carrito y abre gaveta de dinero
```

---

### 3. Modelo Entidad-Relación (ERD) en SQLite WAL

```mermaid
erDiagram
    User ||--o{ CashSession : "abre / cierra"
    CashSession ||--o{ Sale : "contiene"
    CashSession ||--o{ Expense : "registra"
    Category ||--o{ Product : "clasifica"
    Product ||--o{ SaleItem : "se vende en"
    Product ||--o{ ProductLoss : "genera mermas"
    Sale ||--o{ SaleItem : "compuesta por"
    Sale ||--o{ Payment : "liquidada con"
    Customer ||--o{ Sale : "compra a crédito"
    Customer ||--o{ CreditPayment : "abona deuda"

    User {
        string id PK
        string username UK
        string name
        string password
        string role "ADMIN | CASHIER"
        boolean active
    }

    Product {
        string id PK
        string barcode UK
        string name
        string type "UNIT | WEIGHT"
        float costPrice
        float salePrice
        float stock "Decimal en Kg o entero"
        float minStock
    }

    CashSession {
        string id PK
        string userId FK
        datetime openedAt
        datetime closedAt
        float startAmount
        float endAmount
        float systemAmount
        string status "OPEN | CLOSED"
    }

    Sale {
        string id PK
        string sessionId FK
        string customerId FK
        float totalUsd
        float totalBs
        float exchangeRate
        string paymentMethod
        string status "COMPLETED | CREDIT | CANCELLED"
    }

    Customer {
        string id PK
        string name
        string phone
        string idNumber
        float creditLimit
        float balance "Saldo Deudor"
    }

    ProductLoss {
        string id PK
        string productId FK
        float quantity "Kg o Unidades"
        string reason "Pudrición | Golpe | Deshidratación"
        datetime createdAt
    }
```

---

## ⚪ Especificación Funcional & Manual del Negocio (Zetsu Blanco & Pain)

### 1. El Manejo de la Balanza y Productos por Peso (Kg / g)
- **Problema en Fruterías**: Los sistemas genéricos fuerzan a escribir unidades enteras. En un abasto criollo, el cliente pide *"medio kilo de tomate y dos plátanos"*.
- **Solución El Cuadre**: 
  - El modal de pesaje ofrece **botones de peso rápido**: `1/4 Kg (250g)`, `1/2 Kg (500g)`, `1 Kg (1000g)`, `2 Kg (2000g)`.
  - Soporte de balanza USB/Serial en tiempo real con botón de **Tara** para descontar el peso de bolsas o bandejas.
  - La cantidad se almacena en formato decimal (`1.450 Kg`), recalculando automáticamente el subtotal: `1.450 Kg * $1.80/Kg = $2.61 USD`.

### 2. El Libro de Fiados Digital (Cuentas por Cobrar)
- **Realidad del Comercio Popular**: Clientes de confianza se llevan víveres anotados en una libreta de papel que se pierde o mancha.
- **Solución El Cuadre**:
  - Cada cliente tiene ficha con Cédula, Teléfono, Límite de Crédito y Saldo Deudor acumulado.
  - Al vender con método `CREDIT`, el ticket pasa a estado `PENDING_CREDIT` y el saldo deudor del cliente aumenta automáticamente.
  - Módulo de **Abonos Parciales**: Doña Carmen puede abonar $10 en efectivo o en Bs al cambio del día, descontándose inmediatamente de su deuda pendiente.

### 3. Cierre de Turno & Arqueo Ciego ("El Cuadre")
- **Control Antifraude**: El cajero **no ve** cuánto dinero dice el sistema que debería haber en caja.
- **Protocolo de Cierre**:
  1. El cajero cuenta físicamente los billetes de USD, billetes de Bs, comprobantes de Punto de Venta y pagos móviles.
  2. Ingresa los montos reales en el modal de arqueo.
  3. El sistema compara contra las ventas registradas y emite el dictamen:
     - 🟢 **CUADRE PERFECTO**: Diferencia $0.00.
     - 🟡 **SOBRANTE**: Dinero extra en gaveta.
     - 🔴 **FALTANTE / DESCUADRE**: Alerta de pérdida para revisión del supervisor.

---

## ☁️ Alineación con Sprints en ClickUp (Pain)

| Subtarea ClickUp | Nombre de la Tarea | Estado Actual | Responsable |
| :---: | :--- | :---: | :---: |
| `86bcqv6b4` | US-01: Prototipado UI/UX en Stitch (6 Vistas) | **TESTING** | 🦋 Konan |
| `86bcqv6dp` | US-02: Base de Datos SQLite, Prisma & Seeds Criollos | **TESTING** | 🖤 Kakuzu |
| `86bcqv6du` | US-03: Login & Turnos de Caja (Apertura/Arqueo Ciego) | **TESTING** | 🖤 Kakuzu / 👁️ Itachi |
| `86bcqw6a6` | US-11: Identidad Visual Oficial, Logotipo SVG & Brand Book | **TO DO** | 🎨 Sai |
| `86bcqw6fd` | US-12: Pack de Iconos Criollos SVG & Assets para Balanza | **TO DO** | 🎨 Sai |
| `86bcqw6vc` | US-13: Mockups Fotorealistas en Mostrador & Banners de Redes | **TO DO** | 🎨 Sai / 🎭 Tobi |
| `86bcqv6e2` | US-04: Caja Táctica POS (Widescreen Terminal) | **TO DO** | 👁️ Itachi |
| `86bcqv6fm` | US-05: Pasarela de Cobro Multimoneda & Vueltos | **TO DO** | 👁️ Itachi / 🖤 Kakuzu |
| `86bcqv6h0` | US-06: Inventario Híbrido & Mermas de Perecederos | **TO DO** | 🖤 Kakuzu / 👁️ Itachi |
| `86bcqv6h8` | US-07: Contabilidad & Gastos de Caja Menor | **TO DO** | 🖤 Kakuzu |
| `86bcqv6he` | US-08: Tests Unitarios Vitest >85% | **TO DO** | 💀 Hidan |
| `86bcqv6hy` | US-09: Manual del Cajero & Guía Offline | **TO DO** | 🌿 Zetsu |
| `86bcqv8c7` | US-10: Libro de Fiados Digital / CxC | **TO DO** | 🖤 Kakuzu / 👁️ Itachi |
