# 📋 Captura Cruda: Auditoría Forense y Estado Integral del Ecosistema MENIOX

- **Fecha de Auditoría**: 2026-10-14
- **Auditor / Responsable**: 🤵 **ALFRED** (Sistema de Mayordomía & Inteligencia Ejecutiva de Víctor Montoya)
- **Ubicación del Código**: `C:\Users\vmontoyaMG\Desktop\Meniox\meniox`
- **Área 2brain**: 🚀 `proyectos` / [[meniox]]

---

## 1. Resumen Ejecutivo de la Exploración

Meniox es una plataforma integral monorepo (gestor Nx / npm workspaces) para la gestión operativa y financiera de restaurantes y franquicias gastronómicas. Su diseño busca resolver los dolores críticos de sistemas monolíticos tradicionales como **Xetux ERP**: sincronización manual de catálogos y permisos, mermas fantasma por caída de red, falta de trazabilidad en compras e incapacidad de operar en arquitecturas cloud multi-tenant de forma nativa.

---

## 2. Radiografía de la Arquitectura & Servicios

### 2.1 Microservicios Backend (NestJS 11 + TypeScript 5.9)
1. **`apps/gateway`** (Puerto 3000):
   - Proxy reverso y orquestador perimetral HTTP.
   - Valida JWT, extrae claims de tenant (`x-tenant-id`), roles y scopes.
   - Enruta peticiones a los microservicios aguas abajo.
2. **`apps/auth-service`** (Puerto 3001):
   - Emisión y validación de tokens JWT multi-inquilino.
   - Control de acceso basado en roles (RBAC) y scopes de autorización granular.
3. **`apps/org-service`** (Puerto 3002):
   - Gestión de estructura organizacional: Organizaciones (tenants), Marcas, Sucursales (branches) y asignación de bodegas.
4. **`apps/catalog-service`** (Puerto 3003):
   - Catálogo maestro de productos para la venta, categorías, modificadores, combos y listas de precios diferenciadas por sucursal.
5. **`apps/inventory-service`** (Puerto 3004):
   - Corazón operativo de inventarios: control de materias primas/insumos, recetas y subrecetas multinivel.
   - Deducción atómica por venta al consumir eventos de RabbitMQ.
   - Módulo de compras: Órdenes de Compra (OC), Recepciones de Almacén y Facturación de Compras con validación estricta de tolerancias de costo y cantidad.
   - Mermas, transferencias inter-sucursales, gastos operativos y cierres mensuales de inventario.
6. **`apps/sales-service`** (Puerto 3005):
   - Comandas y órdenes POS, cálculo de impuestos, retenciones tipo SENIAT, propinas y pagos divididos (split payments).
   - Implementa **Outbox Pattern** para garantizar la consistencia eventual: persiste el evento `sales.order.paid` / `order.completed` en la base de datos antes de publicarlo en RabbitMQ.
   - Servicio de reconciliación periódica (`SalesReconciliationService`) para detectar órdenes huérfanas o no descontadas.

### 2.2 Aplicaciones Frontend & Móviles
1. **`apps/franchise-admin`** (Puerto 3010):
   - Portal web administrativo construido sobre Next.js 15 (App Router), React 19, Tailwind CSS 4, Framer Motion, TanStack Query y Lucide React.
2. **`apps/pos-mobile`**:
   - Aplicación móvil de punto de venta desarrollada con **React Native & Expo SDK 56**, orientada a tablets y terminales táctiles de caja.
3. **`apps/pos-gustoflow`**:
   - Prototipo experimental de interfaz táctil drill-down con interacción visual dinámica de adición de productos y opciones.

---

## 3. Estado de la Base de Datos & Datos Reales en Cloud

- **Proveedor Cloud**: Aiven PostgreSQL 16
- **Host**: `pg-meniox-masterhub.f.aivencloud.com:28688/defaultdb`
- **Esquemas Aislados por Dominio**:
  - `org.*`: Organizaciones, marcas, sucursales.
  - `catalog.*`: Categorías, productos, combos.
  - `inventory.*`: Materiales, recetas, subrecetas, compras, movimientos, lotes.
  - `sales.*`: Órdenes de venta, líneas de venta, outbox events, pagos.
  - `public.*`: Tablas base de soporte.
- **Volumetría Verificada en Base de Datos Real**:
  - **Tenants**: 2 (`beijing-sushi` y tenant demo/testing).
  - **Sucursales Activas**: 14 sedes pertenecientes a Beijing Sushi.
  - **Catálogo de Venta**: 80 productos activos configurados.
  - **Materias Primas / Insumos**: 2,126 materiales registrados.
  - **Órdenes de Venta**: 12 órdenes procesadas de prueba/flujo inicial.

---

## 4. Hallazgos Técnicos & Tareas Ejecutadas

### 4.1 Corrección de Tipado en `SalesReconciliationService`
- **Problema Detectado**: En `apps/sales-service/src/sales-reconciliation.service.ts`, la propiedad `timer` estaba tipada como `NodeJS.Timeout | null`. Al compilar en entornos con `dom` lib, TypeScript generaba conflicto de tipos (`Type 'Timeout' is not assignable to type 'number'`).
- **Solución Aplicada**:
  - Se ajustó el tipado a `ReturnType<typeof setInterval> | null`.
  - Se aseguró la invocación de `clearInterval(this.timer)` en el ciclo de desmontaje `onModuleDestroy`.
  - Resultado: Suite `tests/sales-reconciliation.service.spec.ts` ejecutada con éxito total: **4 de 4 pruebas unitarias pasadas**.

### 4.2 Deuda Técnica: Suite de Pruebas de Inventario
- **Archivo**: `tests/inventory.integration.spec.ts`
- **Estado**: 28 pruebas fallidas debido a obsolescencia de los mocks y fixtures de prueba frente a las nuevas reglas de negocio de subrecetas, tolerancias de compras y validaciones de stock introducidas en las últimas iteraciones de `inventory-service`. Requiere una sesión de refactorización de tests por parte de Elrond (QA).

### 4.3 Cuello de Botella: Conexiones en `.env` (`POSTGRES_POOL_SIZE`)
- En el archivo `.env`, la variable `POSTGRES_POOL_SIZE` está configurada en `2`. Para una base de datos remota con latencia WAN (Aiven Cloud), este valor satura las conexiones simultáneas durante los tests o al arrancar múltiples microservicios concurrentes.
- **Recomendación**: Incrementar a `POSTGRES_POOL_SIZE=8` o `10`, con un `POSTGRES_IDLE_TIMEOUT=15000`.

### 4.4 Duplicidad de Clientes Móviles
- Coexisten `apps/pos-mobile` y `apps/pos-gustoflow`. La recomendación arquitectónica es tomar la arquitectura de consumo de APIs y endpoints de `pos-mobile` y fusionarla con los componentes visuales táctiles y el drill-down rápido de `pos-gustoflow` para consolidar una única aplicación de producción.

### 4.5 Documento de Rediseño: Módulo de Compras UX
- Localizado en `docs/rediseno-ux-compras.md`. Propone reemplazar las pantallas dispersas de facturas/compras por un **Drawer Centralizado de Orden de Compra (OC)** con ciclo de estados:
  `Borrador ➔ Aprobada ➔ Recibida en Almacén (Recepción Parcial/Total) ➔ Facturada (con verificación de tolerancia de precios)`.

---

## 5. Próximos Pasos Recomendados para Meniox

1. **Alinear la suite de tests de inventario**: Actualizar fixtures en `tests/inventory.integration.spec.ts`.
2. **Consolidar el frontend móvil**: Unificar `pos-gustoflow` dentro de `pos-mobile` bajo Expo SDK.
3. **Implementar el Drawer de Compras UX**: Trasladar el diseño de `docs/rediseno-ux-compras.md` a componentes React en `franchise-admin`.
4. **Optimizar variables de entorno**: Ajustar pool de conexiones y timeouts para Aiven PostgreSQL.
