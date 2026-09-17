---
title: "Patrón de Migraciones Idempotentes en Payload CMS 3.x con PostgreSQL (Vercel Build Fix)"
type: "concept"
area: "programacion"
created: 2026-09-16
updated: 2026-09-16
sources:
  - "wiki/proyectos/webcastro.md"
tags:
  - postgresql
  - payload-cms
  - vercel
  - migraciones
  - nextjs
  - typescript
---

# 🛠️ Patrón de Migraciones Idempotentes en Payload CMS 3.x con PostgreSQL (Vercel Build Fix)

*Solución técnica y estándar de arquitectura para evitar fallos de duplicidad de tipos ENUM, tablas e índices durante el proceso de build en Vercel con Payload CMS 3.x y Neon PostgreSQL.*

---

## 🚨 El Problema: Error de Build en Vercel (`already exists`)

Durante el despliegue automático en Vercel, el servidor de Next.js ejecuta `payload.init()` durante la compilación de rutas estáticas/SSR. Si la aplicación tiene migraciones registradas en `prodMigrations`, Payload intenta ejecutarlas contra la base de datos de producción (Neon PostgreSQL).

Si los tipos `ENUM`, tablas o restricciones fueron creados previamente (por ejemplo, durante el desarrollo local o sincronizaciones en caliente), PostgreSQL lanza una excepción fatal:

```text
caused by: error: type "enum_pages_blocks_cta_button_action" already exists
query: CREATE TYPE "public"."enum_pages_blocks_cta_button_action" AS ENUM('modal', 'link');
```

Debido a que PostgreSQL no soporta nativamente la sintaxis `CREATE TYPE IF NOT EXISTS`, la transacción de la migración falla y cancela el proceso `next build` en Vercel con código de salida `1`.

---

## 💡 La Solución: Idempotencia con Bloques PL/pgSQL

Para resolver este conflicto sin afectar la integridad del esquema, las sentencias SQL en las migraciones de Payload CMS debe convertirse a un formato **100% Idempotente**.

### 1. Creación Idempotente de Tipos ENUM
Envolver la creación de cada `ENUM` en un bloque `DO $$ BEGIN ... EXCEPTION WHEN duplicate_object THEN null; END $$;`:

```sql
DO $$ BEGIN
  CREATE TYPE "public"."enum_pages_blocks_cta_button_action" AS ENUM('modal', 'link');
EXCEPTION
  WHEN duplicate_object THEN null;
END $$;
```

### 2. Modificación de Valores en ENUMs Existentes
Cuando se agregan nuevos valores a un `ENUM` existente (`ALTER TYPE ... ADD VALUE`), envolver en la misma captura de excepción:

```sql
DO $$ BEGIN
  ALTER TYPE "public"."enum_pages_blocks_column_columns_block_type" ADD VALUE 'proyecto' BEFORE 'hero';
EXCEPTION
  WHEN duplicate_object THEN null;
END $$;
```

### 3. Creación y Eliminación de Tablas e Índices
Utilizar las cláusulas nativas `IF NOT EXISTS` e `IF EXISTS`:

```sql
CREATE TABLE IF NOT EXISTS "proyectos" (
  "id" serial PRIMARY KEY NOT NULL,
  "titulo" varchar NOT NULL
);

CREATE INDEX IF NOT EXISTS "proyectos_created_at_idx" ON "proyectos" USING btree ("created_at");
DROP INDEX IF EXISTS "pages_blocks_testimonials_testimonials_avatar_idx";
```

### 4. Adición de Columnas y Claves Foráneas (Constraints)
Envolver la adición de columnas y restricciones de integridad en bloques de captura de excepción:

```sql
-- Agregar Columna
DO $$ BEGIN
  ALTER TABLE "footer" ADD COLUMN "show_text_brand" boolean DEFAULT true;
EXCEPTION
  WHEN duplicate_column THEN null;
END $$;

-- Agregar Constraint (Foreign Key)
DO $$ BEGIN
  ALTER TABLE "pages_blocks_cta" 
  ADD CONSTRAINT "pages_blocks_cta_parent_id_fk" 
  FOREIGN KEY ("_parent_id") REFERENCES "public"."pages"("id") ON DELETE cascade;
EXCEPTION
  WHEN duplicate_object THEN null;
END $$;
```

---

## ⚙️ Complemento: Limpieza de Migraciones Dev (`clean-dev-migrations.mjs`)

Además de la idempotencia en SQL, es crucial agregar un script de `prebuild` en `package.json` para purgar los registros de desarrollo que tengan `batch = -1` en la tabla `payload_migrations`:

```json
{
  "scripts": {
    "prebuild": "node scripts/clean-dev-migrations.mjs",
    "build": "next build"
  }
}
```

### Script `scripts/clean-dev-migrations.mjs`:
```javascript
import pg from 'pg'

const { Pool } = pg

async function cleanDevMigrations() {
  const connectionString = process.env.DATABASE_URL_UNPOOLED || process.env.DATABASE_URL
  if (!connectionString) {
    console.log('[prebuild] No DB connection string found, skipping.')
    return
  }

  const pool = new Pool({ connectionString })
  try {
    const res = await pool.query('DELETE FROM "payload_migrations" WHERE batch = -1')
    console.log(`[prebuild] Cleaned ${res.rowCount} dev migration entries (batch = -1).`)
  } catch (err) {
    console.warn('[prebuild] Warning cleaning dev migrations:', err.message)
  } finally {
    await pool.end()
  }
}

cleanDevMigrations()
```

---

## 🔗 Enlaces Relacionados
- [[Proyecto: WebCastro|../proyectos/webcastro.md]]
- [[Subagente Backend JS Expert|../../agents/backend_js_expert.md]]
- [[Área Programación - Conocimiento Técnico|pilar-programacion.md]]
