---
title: "SOP: Acceso a pgAdmin en Producción y Purga Quirúrgica de Facturas y Retenciones (MasterHub)"
type: "sop"
area: "trabajo"
created: 2026-10-07
updated: 2026-10-07
tags:
  - database
  - postgresql
  - masterhub
  - pgadmin
  - finance_db
  - cxp
  - seniat
  - mastergroup
---

# 🛡️ SOP: Acceso a pgAdmin en Producción y Purga Quirúrgica de Facturas y Retenciones (MasterHub)

*Protocolo operativo estándar para acceder a pgAdmin en el servidor Linode de producción y ejecutar la limpieza/reinicio controlado de facturas CxP y comprobantes de retención SENIAT sin comprometer catálogos maestros.*

---

## 🔍 1. Información General del Servidor y pgAdmin

- **Servidor VPS Linode**: `172.238.221.116`
- **Dominio de MasterHub**: `https://masterhub.mastergroupve.com`
- **Contenedor pgAdmin**: `masterhub-pgadmin-1` (Puerto `5050`)
- **Contenedor PostgreSQL**: `masterhub-postgres-local-1` (Puerto `5433` expuesto en host, `5432` en red Docker `mghub-network`)

---

## 🌐 2. Acceso y Credenciales a pgAdmin Producción

### A. URLs de Acceso:
1. **Acceso Web Directo**: [http://172.238.221.116:5050](http://172.238.221.116:5050)
2. **Acceso Seguro vía Túnel SSH (Recomendado)**:
   ```powershell
   ssh -L 5050:localhost:5050 root@172.238.221.116
   ```
   *Luego abrir en el navegador local: [http://localhost:5050](http://localhost:5050).*

### B. Credenciales de Inicio de Sesión:
* **Email / Username**: `admin@admin.com`
* **Password**: `admin`

---

## 🐘 3. Registro de la Conexión PostgreSQL en pgAdmin

Si al ingresar no aparece ningún servidor registrado en el panel izquierdo:

1. Clic en **Add New Server** (o Clic derecho en **Servers** ➔ **Register** ➔ **Server...**).
2. **Pestaña General**:
   * **Name**: `MasterHub Producción`
3. **Pestaña Connection**:
   * **Host name/address**: `postgres-local`
   * **Port**: `5432`
   * **Maintenance database**: `postgres` (o `finance_db`)
   * **Username**: `masterhub`
   * **Password**: `masterhub-local`
   * **Save password?**: ✅ Marcado
4. Clic en **Save**.

---

## 🗄️ 4. Protocolo de Purga Quirúrgica en `finance_db`

Para vaciar exclusivamente los registros transaccionales de facturas y comprobantes generados sin alterar los catálogos maestros ni la parametrización:

### A. Matriz de Impacto en Tablas:

| Tabla Física | Acción | Impacto / Datos Eliminados |
| :--- | :--- | :--- |
| **`"TaxRetention"`** | `TRUNCATE` | Todos los comprobantes de retención generados (IVA 75%/100% e ISLR). |
| **`"AccountPayable"`** | `TRUNCATE` | Facturas, notas de entrega, cuentas por pagar cargadas manuales o sincronizadas de Xetux. |
| **`"SeniatVoucherCounter"`** | `TRUNCATE` | Reinicia los correlativos de comprobantes SENIAT para que comiencen desde `00000001` en el nuevo ciclo. |

### B. Tablas Preservadas Intactas (Catálogos Maestros):
* ✅ **`"Supplier"`**: Todos los proveedores registrados con su RIF, categoría y porcentaje de retención.
* ✅ **`"BusinessUnit"`**: Sedes y Unidades de Negocio.
* ✅ **`"xetux_payment_methods"`**: Catálogo de los 33 métodos de pago oficiales.
* ✅ **`"bcv_exchange_rates"`**: Histórico oficial de tasas del Banco Central de Venezuela.
* ✅ **`"IslrRetentionRule"` / `"IslrConcept"`**: Tabulador y reglas de retención ISLR (Decreto 1808).

---

## 💻 5. Script SQL de Ejecución

Dentro de pgAdmin, expandir **`MasterHub Producción`** ➔ **`Databases`** ➔ seleccionar **`finance_db`** ➔ abrir **Query Tool** y ejecutar:

```sql
-- ==============================================================================
-- PURGA CONTROLADA DE FACTURAS CXP Y RETENCIONES SENIAT (finance_db)
-- ==============================================================================

-- 1. Vaciar comprobantes de retención y facturas CxP (en cascada)
TRUNCATE TABLE "TaxRetention", "AccountPayable" CASCADE;

-- 2. Reiniciar los correlativos mensuales de comprobantes SENIAT
TRUNCATE TABLE "SeniatVoucherCounter" CASCADE;
```

### Ejecución alternativa directa vía SSH (CLI):
```bash
ssh root@172.238.221.116 "docker exec -i masterhub-postgres-local-1 psql -U masterhub -d finance_db -c 'TRUNCATE TABLE \"TaxRetention\", \"AccountPayable\", \"SeniatVoucherCounter\" CASCADE;'"
```
