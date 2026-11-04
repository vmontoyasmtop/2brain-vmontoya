---
title: "Blueprint Técnico Sprint 1: Monorepo, Dockerización y Núcleo de Datos (SmartOps Quant Engine)"
type: "architecture"
area: "proyectos"
created: 2026-11-02
updated: 2026-11-02
tags:
  - orochimaru
  - kakuzu
  - akatsuki
  - arquitectura
  - docker
  - redis
  - prisma
  - monorepo
  - telegram
---

# 🐍🖤 Blueprint Técnico Sprint 1: SmartOps Quant Engine 2.0

**Arquitectos Responsables**: 🐍 **Orochimaru** (Chief Architect & DevOps) & 🖤 **Kakuzu** (Backend & DB Architect)  
**Sprint**: 🏃 Sprint 1 (15 SP) — Fundación & Unificación Arquitectónica  
**Supervisión**: ☁️ **Pain (Tendō)** & 👑 **El Señor**

---

## 🏛️ 1. Topología del Monorepo (`smartops-quant-engine`)

```text
smartops-quant-engine/
├── .github/workflows/          # CI/CD: Lint, Typecheck, Test coverage >85% (Hidan)
├── docker/
│   ├── Dockerfile.engine       # Runtime híbrido (Node 20 + Python 3.12)
│   └── redis/redis.conf        # Configuración Redis L2 RAM Cache (Appendonly: yes)
├── packages/
│   ├── shared-core/            # TypeScript / Python: Tipos, Logger Winston, Telemetría Telegram
│   │   ├── prisma/             # Schema Prisma unificado (PostgreSQL / SQLite)
│   │   ├── src/telegram/       # Bot de control remoto interactivo (/status, /pnl, /pause)
│   │   └── src/risk/           # Guardián de riesgo institucional (Drawdown 5%, Hard Stops)
│   ├── defi-arbitrage/         # Módulo ArbiON DeFi (Hardhat, Solidity, Uniswap v3 Flash Swaps)
│   ├── cex-streaming/          # Módulo ArbiON CEX (WebSockets Binance L2, Zero-Fee Maker)
│   └── mt5-quant/              # Módulo QuantON & ToVE (US100, Gold, BTC MT5 connector & LEAN)
├── docker-compose.yml          # Orquestación de infraestructura local y VPS
├── .env.example                # Variables de entorno tipadas
└── package.json                # Workspace unificado
```

---

## 🐳 2. Infraestructura Docker Compose Multi-Contenedor (Orochimaru)

```yaml
version: '3.8'

services:
  # ⚡ Redis para Libros de Órdenes L2 y Caché en Memoria (< 1ms)
  quant-redis:
    image: redis:7-alpine
    container_name: smartops-quant-redis
    restart: unless-stopped
    command: redis-server --appendonly yes --requirepass ${REDIS_PASSWORD:-smartops_secret}
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    networks:
      - quant-network

  # 🐘 Base de Datos Relacional para Historial de Trades & Métricas
  quant-postgres:
    image: postgres:16-alpine
    container_name: smartops-quant-postgres
    restart: unless-stopped
    environment:
      POSTGRES_DB: smartops_quant
      POSTGRES_USER: ${POSTGRES_USER:-smartops}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-smartops_secure_pass}
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - quant-network

  # 🚀 Motor de Telemetría & Orquestador Central
  quant-orchestrator:
    build:
      context: .
      dockerfile: docker/Dockerfile.engine
    container_name: smartops-quant-orchestrator
    restart: unless-stopped
    environment:
      NODE_ENV: production
      DATABASE_URL: "postgresql://${POSTGRES_USER:-smartops}:${POSTGRES_PASSWORD:-smartops_secure_pass}@quant-postgres:5432/smartops_quant?schema=public"
      REDIS_URL: "redis://:${REDIS_PASSWORD:-smartops_secret}@quant-redis:6379"
      TELEGRAM_BOT_TOKEN: ${TELEGRAM_BOT_TOKEN}
      TELEGRAM_CHAT_ID: ${TELEGRAM_CHAT_ID}
    depends_on:
      - quant-redis
      - quant-postgres
    networks:
      - quant-network

networks:
  quant-network:
    driver: bridge

volumes:
  redis_data:
  postgres_data:
```

---

## 💎 3. Esquema Prisma de Persistencia Blindada (Kakuzu)

```prisma
// packages/shared-core/prisma/schema.prisma

generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

enum EngineType {
  DEFI_ARBITRAGE
  CEX_TRIANGULAR
  MT5_QUANT
}

enum TradeDirection {
  BUY
  SELL
  TRIANGULAR_CYCLE
}

enum TradeStatus {
  DETECTED
  EXECUTING
  COMPLETED
  REVERTED
  FAILED
}

// Registro auditado de cada oportunidad de arbitraje detectada
model ArbitrageOpportunity {
  id              String      @id @default(uuid())
  engine          EngineType
  pairRoute       String      // Ej: "USDT->BTC->FDUSD->USDT" o "WETH->USDC->DAI->WETH"
  grossSpreadPct  Decimal     @db.Decimal(10, 4)
  netProfitEst    Decimal     @db.Decimal(18, 8)
  gasCostEst      Decimal?    @db.Decimal(18, 8)
  executed        Boolean     @default(false)
  createdAt       DateTime    @default(now())

  trades          ExecutionTrade[]

  @@index([engine, createdAt])
}

// Historial inmutable de operaciones ejecutadas
model ExecutionTrade {
  id              String                @id @default(uuid())
  opportunityId   String?
  opportunity     ArbitrageOpportunity? @relation(fields: [opportunityId], references: [id], onDelete: SetNull)
  engine          EngineType
  symbol          String                // Ej: "US100", "XAUUSD", "BTCUSDT"
  direction       TradeDirection
  entryPrice      Decimal               @db.Decimal(18, 8)
  exitPrice       Decimal?              @db.Decimal(18, 8)
  lotSize         Decimal               @db.Decimal(10, 4)
  pnlRealized     Decimal?              @db.Decimal(18, 8)
  pnlPct          Decimal?              @db.Decimal(10, 4)
  feeTotal        Decimal               @default(0) @db.Decimal(18, 8)
  status          TradeStatus           @default(EXECUTING)
  txHashOrTicket  String?               // Hash EVM o Ticket MT5
  startedAt       DateTime              @default(now())
  closedAt        DateTime?

  @@index([engine, status, startedAt])
}

// Snapshots de rendimiento para telemetría SaaS e inversores
model DailyPerformanceSnapshot {
  id              String      @id @default(uuid())
  engine          EngineType
  date            DateTime    @db.Date
  startingBalance Decimal     @db.Decimal(18, 4)
  closingBalance  Decimal     @db.Decimal(18, 4)
  dailyPnl        Decimal     @db.Decimal(18, 4)
  dailyPnlPct     Decimal     @db.Decimal(10, 4)
  maxDrawdownPct  Decimal     @db.Decimal(10, 4)
  winRate         Decimal     @db.Decimal(5, 2)
  totalTrades     Int
  createdAt       DateTime    @default(now())

  @@unique([engine, date])
}
```

---

## 📱 4. Hub de Telemetría y Control Remoto Telegram (Kakuzu & Orochimaru)

El bot unificado de Telegram escucha eventos del motor y permite gobernar las operaciones:

| Comando | Acción del Motor | Respuesta al Señor |
| :--- | :--- | :--- |
| `/status` | Sondea la salud de los 3 motores (DeFi, CEX, MT5) y latencia Redis. | Estado en vivo: Activo/Pausado, Uptime y memoria. |
| `/pnl` | Consulta los balances y PnL acumulado de la jornada. | Balance actual, ganancias realizadas en $ y % del capital. |
| `/pause` | Activa el interruptor de parada de emergencia (*Circuit Breaker*). | Cancela órdenes pendientes y detiene nuevas entradas. |
| `/resume` | Reactiva el ciclo de escaneo y trading normal. | Reinicia subscripciones WebSockets y escaneo. |
| `/risk` | Consulta el estado del guardián de Drawdown de Axi Select / Prop Firm. | Drawdown actual vs. límite 5% permitido. |

---

## 🔗 Relación en 2brain
- [[ecosistema-trading-smartops|Ecosistema SmartOps Quant]]
- [[rea-smartops-trading-arbitrage-benchmarks|Informe REA Benchmarking Akatsuki]]
- [[pilar-proyectos|Área Proyectos]]
