---
title: "Solución: Error TypeError en NestJS Swagger con tsx y esbuild (ParameterMetadataAccessor)"
type: "concept"
area: "programacion"
created: 2026-10-24
updated: 2026-10-24
tags:
  - nestjs
  - swagger
  - openapi
  - tsx
  - esbuild
  - typescript
  - troubleshooting
  - zetsu-docs
  - kakuzu-backend
---

# 🛠️ Solución Técnica: `TypeError: Cannot read properties of undefined (reading '0')` en NestJS Swagger

**Cronista & Documentación**: 🌿 Zetsu (🌑 Zetsu Negro) con la supervisión de 🤵 ALFRED  
**Área**: 💻 `programacion` (Backend, NestJS, TypeScript, Tooling)  
**Proyecto de Referencia**: `EL CUADRE POS` (`C:\Users\vmont\OneDrive\Desktop\el-cuadre-pos\backend`)  

---

## 💥 Síntoma & Trace del Error

Al arrancar un servidor **NestJS** utilizando `tsx` (`tsx watch src/main.ts`):

```text
[Nest] 10976  - 24/10/2026, 10:49:59 p. m.     LOG [NestFactory] Starting Nest application...
[Nest] 10976  - 24/10/2026, 10:49:59 p. m.     LOG [InstanceLoader] AppModule dependencies initialized +15ms
...
C:\Users\...\node_modules\@nestjs\swagger\dist\services\parameter-metadata-accessor.js:14
            type: types[param.index],
                       ^

TypeError: Cannot read properties of undefined (reading '0')
    at .../@nestjs/swagger/dist/services/parameter-metadata-accessor.js:14:24
    at .../node_modules/lodash/lodash.js:13469:38
    at .../node_modules/lodash/lodash.js:4967:15
    at baseForOwn (.../node_modules/lodash/lodash.js:3032:24)
    at mapValues (.../node_modules/lodash/lodash.js:13468:7)
    at ParameterMetadataAccessor.explore (.../@nestjs/swagger/dist/services/parameter-metadata-accessor.js:13:59)
    at exploreApiParametersMetadata (.../@nestjs/swagger/dist/explorers/api-parameters.explorer.js:20:58)
    at .../@nestjs/swagger/dist/swagger-explorer.js:73:45
```

El servidor colapsa inmediatamente durante el ciclo de exploración de rutas de `@nestjs/swagger` sin llegar a escuchar peticiones HTTP.

---

## 🔬 Análisis de Causa Raíz (Zetsu Negro)

1. **Dependencia de `@nestjs/swagger` en `Reflect.getMetadata`**:
   Para generar la documentación OpenAPI automáticamente sin exigir `@ApiProperty` en cada argumento de función, Swagger inspecciona los tipos mediante la API de reflexión de TypeScript:
   ```typescript
   const types = Reflect.getMetadata('design:paramtypes', target, key);
   ```

2. **La limitación arquitectónica de `tsx` / `esbuild`**:
   - `tsx` utiliza internamente **`esbuild`** para transpolar TypeScript a JavaScript en memoria a velocidad ultra-rápida.
   - `esbuild` **NO implementa la emisión de metadatos de decoradores heredados de TypeScript** (`emitDecoratorMetadata: true`), ya que requiere análisis semántico de tipos que `esbuild` intencionalmente omite para mantener su velocidad en C++/Go.
   - En consecuencia, en tiempo de ejecución, `Reflect.getMetadata('design:paramtypes', ...)` devuelve **`undefined`**.

3. **El Punto de Ruptura en `@nestjs/swagger`**:
   En `parameter-metadata-accessor.js`, el código asume que `types` es un arreglo:
   ```javascript
   // types es undefined -> undefined[0] lanza TypeError!
   type: types[param.index]
   ```

---

## 🛡️ Solución Definitiva (El Estándar Akatsuki)

Para resolver este fallo en proyectos NestJS sin renunciar a la recarga en vivo (*hot-reload*), se debe prescindir de `tsx` en el backend y utilizar la tubería oficial de compilación de NestJS:

### Paso 1: Instalar `@nestjs/cli` en dependencias de desarrollo
```bash
npm install --save-dev @nestjs/cli
```

### Paso 2: Configurar `nest-cli.json` con el Plugin Oficial de Swagger
Crear o editar `nest-cli.json` en la raíz del proyecto backend:

```json
{
  "$schema": "https://json.schemastore.org/nest-cli",
  "collection": "@nestjs/schematics",
  "sourceRoot": "src",
  "compilerOptions": {
    "deleteOutDir": true,
    "plugins": ["@nestjs/swagger"]
  }
}
```

> [!TIP]
> El plugin `"@nestjs/swagger"` en `nest-cli.json` intercepta el AST de TypeScript durante la compilación, extrayendo los tipos e inyectando metadatos OpenAPI de forma nativa sin pérdida de rendimiento.

### Paso 3: Asegurar la configuración en `tsconfig.json`
Verificar que `tsconfig.json` incluya los flags requeridos por NestJS:

```json
{
  "compilerOptions": {
    "module": "commonjs",
    "target": "ES2021",
    "emitDecoratorMetadata": true,
    "experimentalDecorators": true,
    "sourceMap": true,
    "outDir": "./dist"
  }
}
```

### Paso 4: Actualizar los Scripts en `package.json`
Sustituir `tsx` por los binarios oficiales de Nest CLI:

```json
{
  "scripts": {
    "build": "nest build",
    "start": "node dist/main.js",
    "start:dev": "nest start --watch",
    "start:debug": "nest start --debug --watch",
    "start:prod": "node dist/main.js"
  }
}
```

---

## ✅ Verificación del Resultado

Al ejecutar:
```bash
npm run start:dev
```

La consola de Nest CLI compila con soporte de decoradores íntegro:
```text
[10:52:43 p. m.] Found 0 errors. Watching for file changes.
[Nest] LOG [NestFactory] Starting Nest application...
[Nest] LOG [RouterExplorer] Mapped {/api/auth/login, POST} route
[Nest] LOG [RouterExplorer] Mapped {/api/products, GET} route
[Nest] LOG [Kakuzu-Backend] ⚡ EL CUADRE POS - Backend NestJS iniciado exitosamente
[Nest] LOG [Kakuzu-Backend] 🌐 Servidor escuchando en: http://localhost:3001
[Nest] LOG [Kakuzu-Backend] 📑 Swagger UI montado en: http://localhost:3001/api/docs
```

La petición HTTP a `http://localhost:3001/api/docs` responde con **`HTTP 200 OK`**.

---

## 🔗 Referencias Relacionadas en 2brain
- [[el-cuadre-pos-arquitectura-tecnica]]: Arquitectura técnica de EL CUADRE POS.
- [[el-cuadre-pos-guia-testing-swagger]]: Guía de pruebas interactivas con Swagger UI.
- [[pilar-programacion]]: Índice maestro de conceptos y runbooks de desarrollo.
