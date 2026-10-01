---
title: "Estándar de Arquitectura Prisma v7 en Monorepos Dockerizados (MasterHub)"
type: "guide"
area: "programacion"
created: 2026-09-30
updated: 2026-09-30
tags:
  - prisma
  - postgresql
  - docker
  - masterhub
  - nestjs
---

# 🛠️ Estándar de Arquitectura Prisma v7 en Monorepos Dockerizados (MasterHub)

*Guía definitiva de resolución al conflicto de versiones Prisma (v5 vs v7), eliminación del error pendular de datasource `url`, y estándar para todos los microservicios en MasterHub.*

---

## 🚨 1. El Problema: "El Conflicto Pendular de Versiones"

En proyectos monorepo con Node.js y Docker (como `MG-HUB`), es común que el entorno local y el contenedor Docker terminen en versiones dispares de Prisma si no se fija una versión raíz estricta:

| Entorno | Versión Prisma | Comportamiento con `url` en `schema.prisma` |
|---|---|---|
| **Host Local (Windows)** | Prisma `5.22.0` (instalado en root o global) | **Exige** `url = env(...)` dentro de `datasource db`. Si no existe, arroja: `Error code: P1012: Argument "url" is missing in data source block "db"`. |
| **Docker / CI (Linux Alpine)** | Prisma `7.10.0` (instalado por `package.json` del microservicio) | **Prohíbe** `url` dentro de `datasource db`. Si existe, arroja: `Error code: P1012: The datasource property url is no longer supported in schema files. Move connection URLs for Migrate to prisma.config.ts`. |

### El Síntoma del "Péndulo":
1. Al probar en local con Prisma 5, el comando falla diciendo que falta `url`. El desarrollador añade `url = env("DATABASE_URL")` a `schema.prisma`.
2. Al compilar en Docker (`RUN npm run prisma:generate`), Prisma 7 en el contenedor rompe el build con error P1012.
3. Se remueve la línea para que Docker pase, pero entonces las migraciones locales fallan nuevamente.

---

## 💡 2. La Solución Arquitectónica: Estandarización a Prisma 7

A partir de Prisma v7, la configuración de conexión a la base de datos se desacopla del esquema declarativo (`schema.prisma`) y se traslada a un archivo TypeScript de configuración oficial (`prisma.config.ts`).

### A. Estructura Requerida por Microservicio
```text
apps/<microservicio>/
├── prisma/
│   ├── schema.prisma          <-- SOLO define provider. NUNCA url.
│   └── migrations/            <-- Historial de migraciones SQL
├── prisma.config.ts           <-- NUEVO: Fuente de verdad de conexión para Prisma 7 CLI
├── package.json               <-- Dependencias fijadas a ^7.8.0+
└── src/
    └── prisma/
        └── prisma.service.ts  <-- Instanciación de runtime (NestJS)
```

### B. `schema.prisma` (Sin `url`)
```prisma
generator client {
  provider = "prisma-client-js"
  output   = "../generated/prisma"
}

datasource db {
  provider = "postgresql"
  // ¡PROHIBIDO url = env("DATABASE_URL") en Prisma 7!
}

// Modelos y Enums...
```

### C. `prisma.config.ts` (Archivo Oficial Prisma 7)
Debe crearse en la raíz del microservicio:
```typescript
import 'dotenv/config';
import { defineConfig } from 'prisma/config';

export default defineConfig({
  schema: 'prisma/schema.prisma',
  migrations: {
    path: 'prisma/migrations',
  },
  datasource: {
    url: process.env.DATABASE_URL || 'postgresql://dummy:dummy@localhost:5432/dummy',
  },
});
```

---

## 🚀 3. Sincronización del Entorno Local

Para que la máquina del desarrollador no continúe usando la versión antigua de Prisma 5:

1. **Actualizar Prisma en la raíz del repositorio**:
   ```bash
   npm install -D prisma@^7.8.0 @prisma/client@^7.8.0
   ```
2. **Comprobar la versión activa**:
   ```bash
   npx prisma -v
   # Debe retornar: Prisma CLI Version : 7.x.x
   ```
3. **Generar y Migrar con scripts de workspace**:
   ```bash
   # Dentro de apps/<microservicio>:
   npm run prisma:generate
   npx prisma migrate dev --name <nombre_migracion>
   ```

---

## 📋 4. Checklist para Nuevos Microservicios en MasterHub

- [ ] `prisma/schema.prisma` solo contiene `provider = "postgresql"`.
- [ ] `prisma.config.ts` existe y define `datasource.url`.
- [ ] `package.json` incluye `"prisma": "^7.8.0"` y `"@prisma/client": "^7.8.0"`.
- [ ] Dockerfile ejecuta `RUN npm run prisma:generate` tras copiar los archivos.
- [ ] Dockerfile ejecuta `CMD ["sh", "-c", "npx prisma migrate deploy && npm run start:prod"]`.
