# Documento de Requerimientos de Producto (PRD)
## Módulo de Finanzas (`finance-ms`) — MasterHub

---

### 1. Resumen Ejecutivo y Alcance General
El módulo de Finanzas de **MasterHub** (`finance-ms`) tiene como objetivo centralizar, automatizar y digitalizar la gestión de Cuentas por Pagar (CxP), Cuentas por Cobrar (CxC), Egresos y Gestión Fiscal de **Master Group**. Actualmente, estos procesos dependen de hojas de cálculo dispersas, cruces manuales y el ERP Profit. La implementación de `finance-ms` eliminará la dependencia de archivos sueltos y garantizará el cumplimiento estricto del marco fiscal venezolano (SENIAT) y las reglas operativas corporativas.

---

### 2. Arquitectura y Stack Tecnológico
* **Microservicio:** `finance-ms` (construido en NestJS sobre transporte TCP).
* **Persistencia:** Base de datos relacional PostgreSQL aislada (`finance_db`) administrada mediante Prisma ORM.
* **API Gateway:** Exposición de endpoints REST autenticados vía JWT.
* **Frontend:** Vistas interactivas en Next.js 16 (React 19, Tailwind CSS, Lucide React, jsPDF).
* **Almacenamiento de Soportes:** Integración con MinIO (almacenamiento S3) para facturas, comprobantes de pago y valijas digitales.
* **Automatización:** NestJS Scheduler (`@nestjs/schedule`) para Cronjobs de tasa BCV y propuesta semanal de pago.

---

### 3. Fases de Desarrollo

```
+-------------------------------------------------------------------------------------------------+
|                                 ROADMAP MÓDULO DE FINANZAS                                      |
+-------------------------------------------------------------------------------------------------+
|  FASE 1: Cuentas por Pagar (CxP) y Propuesta Semanal de Pago                                   |
|  FASE 2: Egresos, Enrutamiento Bancario y Archivos TXT                                          |
|  FASE 3: Cuentas por Cobrar (CxC), Conciliación Xetux vs. Banco y POS                            |
|  FASE 4: Control de Caja Chica, Cuota de Marketing (4%) y Dashboard Gerencial                   |
+-------------------------------------------------------------------------------------------------+
```

---

### 4. Especificación Detallada de Requerimientos

#### 4.1 FASE 1: Cuentas por Pagar (CxP)

##### R1.1 Sincronización Mandatoria con Xetux
* **Regla Crítica de Negocio:** No se permite cargar ninguna factura o documento en CxP sin previa verificación y carga en el sistema de ventas/compras Xetux de la respectiva Unidad de Negocio (BU/Sede).
* **Flujo:** La recepción física de valijas diarias alimenta la verificación en Xetux antes del registro en MasterHub.

##### R1.2 Campos y Clasificación de Documentos
* **Tipos de Documento:** `Factura Fiscal`, `Nota de Entrega`, `Recibo / Email`.
* **Campos Obligatorios de Entrada:**
  * Identificación del Proveedor (RIF, Razon Social).
  * Unidad de Negocio / Sede (BU).
  * Categoría / Concepto (Víveres, Licores, Alquileres, Condominios, Fletes, Servicios Técnicos, Internet).
  * Número de Documento y Número de Control.
  * Base Imponible, Alícuota y Monto de IVA.
  * Fecha de Emisión y Fecha de Recepción (Recepción de Valija).
  * Días de Crédito (Parametrizables: Default 15 días; Pepsicola 7 días; Condominios primeros 5 días del mes).
  * Fecha de Vencimiento (`dueDate = issueDate + creditDays`).

##### R1.3 Tasa de Cambio Oficial (BCV) y Cálculo de IVA (Art. 16 Ley del IVA)
* **Cronjob BCV:** Consumo diario automatizado de la tasa del Banco Central de Venezuela.
* **Regla Impositiva del IVA:** El IVA **siempre** se calcula y bloquea a la tasa de cambio de la **fecha de emisión** de la factura, sin importar si el pago se ejecuta semanas después.

##### R1.4 Motor de Retenciones Fiscales (SENIAT)
* **Notas de Entrega:** Se omite cálculo de IVA y retenciones. Solo procesa la Base Imponible.
* **Retención de IVA:**
  * Validación automática de la categoría de contribuyente en SENIAT (Contribuyente Especial vs. Ordinario).
  * Retención del **75%** o **100%** del IVA según calificación.
  * Soporte para alícuotas del 8% (Salmón), 16% (Víveres/General) y Licores (Art. 18).
* **Retención de ISLR:**
  * Aplicación estricta sobre la Base Imponible según el concepto del servicio:
    * Condominios: **2%**
    * Alquileres: **5%**
    * Fletes: **3%**
    * Servicios Técnicos / Profesionales: Alícuota correspondiente.

##### R1.5 Generación de Correlativos de Comprobantes
* **Estructura Standard SENIAT:** `Año / Mes / Secuencia` (Ejemplo: `202509000000178`).
* **Retenciones de IVA:** Correlativo de 14 dígitos.
* **Retenciones de ISLR:** Secuencia de 2 o 3 dígitos finales.

##### R1.6 Cronjob de Propuesta de Pago Semanal
* **Programación:** Todos los **Martes a las 5:00 PM**.
* **Acción:** Recopila facturas con estatus `Vencido` o próximo a vencer por BU, genera un reporte PDF consolidado y envía un correo a la Dirección (Sr. Emiliano) con el asunto `"Propuesta de Pago MES / DD / AÑO"`.
* **Ciclo de Estados:** `NOT_DUE` (No Vencido), `DUE` (Vencido), `PENDING` (Pendiente), `IN_PROCESS` (En Proceso / Estudio), `APPROVED` (Aprobado), `NOT_APPROVED` (No Aprobado — requiere justificación obligatoria), `PAID` (Pagado).

---

#### 4.2 FASE 2: Egresos y Emisión de Pagos

##### R2.1 Enrutamiento Bancario Inteligente
* **Regla de Cuentas de Origen:**
  * Facturas Fiscales ➔ Procesadas desde la cuenta del **Banco Nacional de Crédito (BNC)**.
  * Notas de Entrega ➔ Procesadas desde la cuenta del **Banco Provincial**.

##### R2.2 Generación de Archivos Planos TXT
* Exportación masiva de archivos `.TXT` formateados conforme a los requerimientos de la banca nacional (BNC y Provincial) para carga directa de lotes de pago.

##### R2.3 Redondeo de Efectivo
* Redondeo automático para pagos en efectivo o divisas físicas: `>= 0.50` redondea al entero superior; `< 0.50` redondea al entero inferior.

##### R2.4 Gestión de Soportes Digitales (MinIO)
* Subida obligatoria de capturas de transferencia/comprobantes (PDF/JPG) asociados al pago, almacenados en MinIO y cambio automático del documento a estatus `PAID`.
* Protocolo de notificación a proveedores vía WhatsApp/Email tras liquidación.

---

#### 4.3 FASE 3: Cuentas por Cobrar (CxC) y Conciliación Bancaria

##### R3.1 Conciliación de Ventas (Xetux vs. Extracto Bancario)
* Módulo de carga masiva de archivos CSV:
  1. Reporte de ventas por método de pago descargado de Xetux (CSV).
  2. Estado de Cuenta Bancario (CSV).
* Cruce automático por día, sede y método de pago, destacando discrepancias en pantalla.

##### R3.2 Calculadora de Comisiones POS e ISLR
* Descuento automático del **2% de ISLR** en ventas procesadas con Tarjeta de Crédito.
* Deducción de comisiones bancarias específicas por banco/lote (0.30% u otros acuerdos contractuales).

---

#### 4.4 FASE 4: Caja Chica, Cuota de Marketing y Reportes

##### R4.1 Arqueo Semanal de Caja Chica
* Registro de facturas pagadas con tarjeta de débito tienda vía valija.
* Cuadre físico de efectivo realizado obligatoriamente los días **Miércoles** por sucursal.

##### R4.2 Cuota de Marketing (4%)
* Cálculo automatizado semanal del **4% sobre la Venta Neta**.
* Deducción previa de montos por concepto de delivery y propinas.
* Generación de reporte de Ventas Netas Sin IVA por sucursal.

---

### 5. Resumen de Modelos de Base de Datos (Prisma Schema Draft)

```prisma
model Supplier {
  id              String    @id @default(uuid())
  rif             String    @unique
  name            String
  isSpecialTax    Boolean   @default(false) // Contribuyente Especial SENIAT
  creditDays      Int       @default(15)
  invoices        Invoice[]
}

model Invoice {
  id              String        @id @default(uuid())
  buId            String
  supplierId      String
  supplier        Supplier      @relation(fields: [supplierId], references: [id])
  docType         DocType       // FISCAL_INVOICE, DELIVERY_NOTE, RECEIPT
  docNumber       String
  controlNumber   String?
  baseAmount      Float
  ivaAmount       Float         @default(0)
  totalAmount     Float
  exchangeRate    Float         // Tasa BCV fecha de emisión
  issueDate       DateTime
  receptionDate   DateTime
  dueDate         DateTime
  status          InvoiceStatus @default(NOT_DUE)
  retentionIva    Float         @default(0)
  retentionIslr   Float         @default(0)
  payments        Payment[]
}

enum DocType {
  FISCAL_INVOICE
  DELIVERY_NOTE
  RECEIPT
}

enum InvoiceStatus {
  NOT_DUE
  DUE
  PENDING
  IN_PROCESS
  APPROVED
  NOT_APPROVED
  PAID
}
```
