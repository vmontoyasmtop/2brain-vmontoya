---
title: "Manual Técnico & Guía Maestra Operativa: SmartOps Quant Engine 2.0 (ArbiON & QuantON)"
type: "guide"
area: "proyectos"
created: 2026-11-02
updated: 2026-11-02
tags:
  - smartops
  - manual-tecnico
  - trading-algoritmico
  - arbitraje-triangular
  - flash-loans
  - binance-streaming
  - mt5
  - axi-select
  - akatsuki
---

# 📘 Manual Técnico & Guía Maestra: SmartOps Quant Engine 2.0

> **Elaborado por la Organización Akatsuki para El Señor Víctor Montoya**  
> **Arquitectura & DevOps**: 🐍 Orochimaru | **Backend & Smart Contracts**: 🖤 Kakuzu | **Seguridad**: 💣 Deidara & 🦂 Sasori  
> **QA & Pruebas**: 💀 Hidan | **Documentación**: 🌿 Zetsu (Negro & Blanco) | **Frontend & UI**: 👁️ Itachi & 🦋 Konan  
> **Ubicación del Código**: `raw/proyectos/repos/smartops-quant-engine/`

---

## 🎯 1. Resumen Ejecutivo (Para Entenderlo Sin Complicaciones)

### ¿Qué es SmartOps Quant Engine 2.0?
Es un **sistema autónomo de finanzas cuantitativas y arbitraje triangular** diseñado para extraer ganancias de ineficiencias de precios en los mercados financieros, bajo una regla inviolable: **cero riesgo de liquidación del capital propio**.

### La Analogía de las Tres Turbinas y el Guardián de la Bóveda
Para visualizar cómo opera el sistema, imagínelo como una planta financiera de tres turbinas independientes custodiadas por un centinela:

```mermaid
graph TD
    subgraph CENTRAL["🛡️ GUARDIÁN CENTRAL DE CAPITAL & COMANDO"]
        G["Guardián de Riesgo (RiskGuardian / 5% DD)"]
        T["Centro de Mando Telegram (/status, /pause, /pnl)"]
        D[("Base de Datos PostgreSQL 16 + Redis L2")]
    end

    subgraph T1["⚡ TURBINA 1: ARBITRAJE DEFI (ON-CHAIN)"]
        M1["Préstamo Flash Loan Balancer (0% fee)"] --> S1["3 Swaps en Uniswap v3"]
        S1 --> R1{"¿Hay Ganancia Neta?"}
        R1 -->|SÍ| W1["Paga Préstamo y Guarda Ganancia"]
        R1 -->|NO| F1["Revert Atómico (Cero Pérdida)"]
    end

    subgraph T2["🏢 TURBINA 2: ARBITRAJE CEX (BINANCE)"]
        M2["WebSockets L2 en Vivo (< 10ms)"] --> S2["Cálculo Triangular RAM"]
        S2 --> R2{"¿Spread Neto >= 0.04%?"}
        R2 -->|SÍ (Maker 0% Fee)| W2["Órdenes Pasivas Post-Only"]
        R2 -->|NO| F2["Mercado Eficiente (No Opera)"]
    end

    subgraph T3["📊 TURBINA 3: TRADING CUANTITATIVO MT5"]
        M3["Nasdaq 100, Oro & Bitcoin"] --> S3["Filtro de Sesión NY (09:30-16:00 EST)"]
        S3 --> R3["Cálculo Dinámico de Lotaje (Riesgo 2%)"]
        R3 --> W3["Ejecución con SL/TP Obligatorio"]
    end

    CENTRAL --> T1
    CENTRAL --> T2
    CENTRAL --> T3
    T3 -.->|Webhook Telemetría| SAAS["🌐 Invst-smartops-front (Dashboard Inversores)"]
```

1. **Turbina 1 (DeFi On-Chain / Web3)**: Pide millones prestados por fracciones de segundo en la blockchain (Flash Loan con 0% de interés), compra barato en un exchange descentralizado, vende caro en otro, devuelve el préstamo y se queda la diferencia. **Si el precio se mueve en contra, la transacción se cancela automáticamente como si nunca hubiera existido.**
2. **Turbina 2 (CEX Streaming / Binance)**: Escucha las cotizaciones de Binance mil veces por segundo por WebSockets. Busca desajustes entre 3 monedas (ej. `USDT -> BTC -> FDUSD -> USDT`) y solo opera si las comisiones de la plataforma son **0.00% (Maker Zero-Fee)**.
3. **Turbina 3 (MT5 Quant / Cuentas de Fondeo)**: Opera Nasdaq, Oro y Bitcoin en MetaTrader 5 respetando a rajatabla las reglas institucionales de **Axi Select / FTMO** (máximo 2% de riesgo por trade, paro absoluto si se pierde 5%).
4. **El Guardián y el Panel**: Un centinela digital que apaga los bots si el mercado se vuelve loco (*Circuit Breaker*), mientras le informa a usted en tiempo real al teléfono móvil por Telegram y alimenta el dashboard web para sus clientes e inversores.

---

## 🏛️ 2. Arquitectura Global del Monorepo

El código está estructurado como un **Monorepo modular** de grado empresarial:

```text
smartops-quant-engine/
├── docker-compose.yml              # Infraestructura reproducible (Redis 7 + PostgreSQL 16)
├── .env.example                    # Plantilla de secretos y llaves de acceso
├── package.json                    # Workspace unificado
├── test_all_modules.py             # Verificador maestro de pruebas automáticas
├── test_live_binance.py            # Consultor en vivo de cotizaciones reales de Binance
├── docker/
│   ├── Dockerfile.engine           # Contenedor híbrido Node.js 20 + Python 3.12
│   └── redis/redis.conf            # Configuración de memoria RAM L2 ultra-rápida
└── packages/
    ├── shared-core/                # Núcleo común: Prisma ORM, Logger, Guardián de Riesgo y Telegram
    ├── defi-arbitrage/             # Smart Contracts Solidity, Tick Math y enrutador anti-MEV
    ├── cex-streaming/              # Conectores WebSockets AsyncIO, libros L2 y Circuit Breakers
    └── mt5-quant/                  # Estrategias YAML, gestión Axi Select y widget Next.js
```

---

## ⚡ 3. Turbina 1: Arbitraje DeFi Atómico (`defi-arbitrage`)

### ¿Por qué fallaba la versión vieja (`ArbiON_v1.0`)?
La versión anterior solo observaba el mercado, calculaba precios consultando a un contrato de la blockchain por internet (tardaba 2 segundos) y si enviaba una transacción, los "bots sándwich" de la mempool pública se adelantaban y le robaban la ganancia (*Frontrunning*).

### La Solución Implementada en la Versión 2.0:
1. **Contrato Inteligente `FlashTriangularArbitrage.sol` (Solidity 0.8.24)**:
   - Utiliza **Balancer Vault** (`0xBA12222222228d8Ba445958a75a0704d566BF2C8`) para obtener **Flash Loans con 0% de comisión**.
   - Ejecuta los 3 intercambios consecutivos dentro del mismo bloque de transacciones:
     - Salto 1: `Token A ➔ Token B` (Uniswap v3).
     - Salto 2: `Token B ➔ Token C` (Uniswap v3).
     - Salto 3: `Token C ➔ Token A` (Uniswap v3).
2. **Reversión de Seguridad Infranqueable**:
   ```solidity
   if (finalAmountA < borrowedAmount + params.minNetProfit) {
       revert ArbitrageNotProfitable(finalAmountA, totalTarget);
   }
   ```
   Si el dinero obtenido al final es menor que el préstamo más la ganancia mínima exigida, la red Ethereum/Polygon **deshace la operación por completo**. No se pierde ni un centavo del capital del fondo.
3. **Cálculo de Precios en Memoria RAM (`UniswapV3TickMath`)**:
   - Convierte el valor matemático `sqrtPriceX96` a precio real en **0.0001 segundos** dentro de la memoria del servidor, sin hacer llamadas de red externas.
4. **Enrutamiento Privado Anti-MEV (`MevProtectedRouter`)**:
   - Envía las órdenes directamente a los validadores de la red usando **Flashbots Protect** o **FastLane**, haciendo que la transacción sea 100% invisible para los bots piratas de la mempool.

---

## 🏢 4. Turbina 2: Arbitraje CEX en Binance (`cex-streaming`)

### ¿Por qué fallaba la versión vieja (`ArbiON_BV1.0`)?
Operaba con peticiones HTTP lentas (REST) y lanzaba órdenes a mercado (*Taker*). Cada orden a mercado paga 0.10% de comisión en Binance. En 3 operaciones seguidas, el bot pagaba **0.30% en comisiones**, devorando cualquier ganancia que normalmente suele ser del 0.05%.

### La Solución Implementada en la Versión 2.0:
1. **Streaming por WebSockets (`BinanceStreamConnector`)**:
   - Conexión continua a los canales `@bookTicker` de Binance Spot. Los precios entran a la memoria del bot en menos de **10 milisegundos**.
2. **Estrategia Maker Zero-Fee**:
   - El sistema opera únicamente cuando la ruta incluye pares promocionales de Binance con **0.00% de comisión Maker** (como los pares basados en **FDUSD** y stablecoins).
3. **Fórmula Matemática Estricta**:
   $$\text{Spread Neto} = \left[ \left( \frac{1}{\text{Ask}_{AB}} \right) \cdot \text{Bid}_{BC} \cdot \text{Bid}_{CA} \cdot (1 - f_{AB}) \cdot (1 - 0.00) \cdot (1 - 0.00) - 1 \right] \times 100$$
   Si el retorno neto no supera **+0.04% libre de comisiones**, el bot no dispara ninguna orden.
4. **Centinela Anti-Pánico (`CexCircuitBreaker`)**:
   - Si el diferencial entre compra y venta supera el **1.50%** (síntoma de desplome de mercado o desvinculación de una stablecoin), el bot se apaga solo y entra en modo de alerta.

---

## 📊 5. Turbina 3: Trading Cuantitativo MT5 & Reglas de Fondeo (`mt5-quant`)

### Estandarización Institucional (Axi Select / Prop Firms)
Diseñado para gestionar cuentas de fondeo profesionales sin violar jamás los términos del broker:

1. **Riesgo Fijo del 2% por Trade**:
   - El bot nunca adivina el tamaño de la posición. Calcula la cantidad exacta de lotes con la fórmula:
     $$\text{Lotaje} = \frac{\text{Balance} \times 0.02}{\text{Stop Loss en Puntos} \times \text{Valor del Punto}}$$
     *Ejemplo comprobado*: En una cuenta de \$10,000 USD, con un Stop Loss de 40 puntos en el Nasdaq, el bot compra exactamente **5.00 lotes** (arriesgando exactamente \$200 USD).
2. **Hard Stop en Drawdown del 5.00%**:
   - Si una racha de pérdidas alcanza el 5% de caída desde el balance más alto registrado, el sistema bloquea inmediatamente la cuenta para evitar su descalificación.
3. **Filtro de Liquidez de Nueva York**:
   - Solo abre posiciones de **09:30 AM a 04:00 PM hora de Nueva York**, cuando los grandes bancos y fondos institucionales están operando y los spreads son mínimos.
4. **Configuración Multi-Activo por YAML**:
   - `config/us100.yaml`: Nasdaq 100 (Estrategia NY Breakout).
   - `config/gold.yaml`: Oro XAUUSD (Estrategia Scalper M5 con volatilidad ATR).
   - `config/btc.yaml`: Bitcoin (Estrategia Volatility Breakout 24/7).

---

## 🌐 6. Telemetría SaaS y Widget para Inversores

Para que su plataforma de inversiones (`Invst-smartops-api` e `Invst-smartops-front`) muestre el rendimiento en vivo:

1. **Webhook de Emisión (`TelemetryClient`)**:
   - Envía automáticamente al backend el estado del fondo cada minuto:
     `{ poolId, balance, equity, dailyPnl, maxDrawdownPct, winRate, totalTrades }`.
2. **Widget en Next.js (`PoolTelemetryWidget`)**:
   - Componente React/Tailwind listo para incrustar en el panel de clientes con:
     - Tarjetas de balance y equity flotante.
     - Ganancia diaria en dólares y porcentaje.
     - **Medidor de Drawdown** con semáforo de riesgo (Verde / Ámbar / Rojo).
     - Estado de salud del bot (`ONLINE` / `CIRCUIT_BREAKER`).

---

## 📱 7. Centro de Comando Remoto en Telegram

El Señor puede supervisar y gobernar toda la maquinaria desde su teléfono móvil a través del bot interactivo (`shared-core/src/telegram/bot.ts`):

| Comando | Acción del Motor | Utilidad Práctica |
| :--- | :--- | :--- |
| **`/status`** | Audita la salud de las 3 turbinas, memoria y latencia. | Saber si todo está en línea en 1 segundo. |
| **`/pnl`** | Consulta el balance, ganancias acumuladas y retorno %. | Ver cuánto dinero ha generado el sistema hoy. |
| **`/pause`** | **Freno de emergencia de un toque**. | Cancela órdenes pendientes y detiene nuevas entradas ante noticias extremas. |
| **`/resume`** | Quita el freno de emergencia. | Vuelve a autorizar el trading normal. |
| **`/risk`** | Informa el drawdown actual vs. el límite del 5%. | Verificar qué tan lejos está la cuenta del límite de Axi Select. |

---

## 🛠️ 8. Guía Práctica de Verificación y Puesta en Marcha

### Paso 1: Ejecutar la Batería Completa de Pruebas Automáticas
Desde la raíz del proyecto, ejecute en PowerShell:
```powershell
python raw\proyectos\repos\smartops-quant-engine\test_all_modules.py
```
* **Qué valida**: Ejecuta 12 pruebas unitarias (6 de CEX y 6 de MT5) y realiza una simulación completa de trading institucional en 2 segundos.

### Paso 2: Probar el Mercado Real de Binance en Vivo
```powershell
python raw\proyectos\repos\smartops-quant-engine\test_live_binance.py
```
* **Qué valida**: Se conecta a los servidores en tiempo real de Binance, consulta los precios actuales de BTC, FDUSD y USDT, y evalúa matemáticamente si existe una ineficiencia aprovechable en ese preciso instante.

### Paso 3: Configurar las Claves Reales en `.env`
Edite el archivo `.env` en `raw/proyectos/repos/smartops-quant-engine/`:
```env
TELEGRAM_BOT_TOKEN="Su_Token_de_Telegram"
TELEGRAM_CHAT_ID="Su_Chat_ID_de_Telegram"
BINANCE_API_KEY="Su_API_Key_de_Binance"
BINANCE_SECRET_KEY="Su_Secret_de_Binance"
EVM_PRIVATE_KEY="Su_Llave_Privada_para_Polygon_o_Base"
```

### Paso 4: Levantar los Servicios en Segundo Plano (Docker)
```powershell
cd raw\proyectos\repos\smartops-quant-engine
docker compose up -d
```
* **Servicios que inician automáticamente**:
  - `quant-redis` (puerto `6379`): Memoria RAM para cotizaciones ultra-rápidas.
  - `quant-postgres` (puerto `5432`): Base de datos relacional para registro de operaciones.
  - `quant-orchestrator`: Motor central con bot interactivo de Telegram.

---

## 🔗 Páginas y Fichas Relacionadas en 2brain
- [[ecosistema-trading-smartops|Diagnóstico General del Ecosistema SmartOps Quant]]
- [[rea-smartops-trading-arbitrage-benchmarks|Informe REA: Benchmarking y Desconstrucción Competitiva]]
- [[smartops-quant-engine-blueprint-sprint1|Sprint 1: Monorepo y Dockerización]]
- [[smartops-defi-arbitrage-atomic-flash-loans|Sprint 2: DeFi Atómico con Flash Loans]]
- [[smartops-cex-streaming-zero-fee-engine|Sprint 3: CEX Streaming & Zero-Fee]]
- [[smartops-mt5-quant-telemetry-saas|Sprint 4: MT5 Quant & Telemetría SaaS]]
- [[pilar-proyectos|Área Proyectos]]
- [[pilar-programacion|Área Programación]]
