# Bitácora de Cierre de Turno y Diagnóstico: Fallo de Login en Staging y Producción (auth-ms)

**Fecha:** 2026-10-02 / 2026-10-03  
**Autor:** ALFRED (Mayordomo & Asistente Ejecutivo 2brain)  
**Para:** Don Víctor Montoya  
**Estado:** Documentado y Listo para Ejecución en Turno Mañana  

---

## 1. Síntoma Reportado
* Al intentar iniciar sesión desde el Frontend (`/login`) tanto en Staging (`staging.mastergroupve.com`) como en Producción (`masterhub.mastergroupve.com`), la autenticación no se completa y arroja error en pantalla.

---

## 2. Diagnóstico Técnico y Causa Raíz

Al inspeccionar los logs en caliente del microservicio `auth-ms` en el VPS (`172.238.221.116`), se detectó la traza exacta del fallo:

```text
[Nest] 1 - 10/03/2026, 3:49:48 AM ERROR [RpcExceptionsHandler] PrismaClientKnownRequestError: 
Invalid `this.prisma.user.findFirst()` invocation in
/app/dist/src/users/users.service.js:110:45

getaddrinfo EAI_AGAIN postgres-local
  code: 'EAI_AGAIN',
  meta: {
    modelName: 'User'
  },
  clientVersion: '7.8.0'
```

### Hallazgos de Red Docker (`docker inspect`):
1. **En Staging (`masterhub-auth-ms-staging`):**
   * El contenedor de staging pertenece a la red: `masterhub-staging_mghub-network-staging`.
   * El contenedor `masterhub-postgres-local-1` pertenece **únicamente** a la red de producción: `masterhub_mghub-network`.
   * **Consecuencia:** Los contenedores de Staging no pueden resolver por DNS ni alcanzar el hostname `postgres-local`, resultando en `EAI_AGAIN` inmediato.
2. **En Producción (`masterhub-auth-ms-1`):**
   * Aunque ambos contenedores están en `masterhub_mghub-network`, el servicio `auth-ms` falló con `EAI_AGAIN` durante la resolución DNS interna de Docker al intentar consultar `postgres-local:5432`, o el contenedor `auth-ms` no refrescó la conexión tras el reinicio de PostgreSQL.

---

## 3. Plan de Acción Inmediato para Mañana

### Paso 1: Conectar `masterhub-postgres-local-1` a la red de Staging (o viceversa)
En el VPS:
```bash
docker network connect masterhub-staging_mghub-network-staging masterhub-postgres-local-1
```
*(O configurar `docker-compose.staging.yml` para usar la red `masterhub_mghub-network` como `external: true`)*.

### Paso 2: Reiniciar `auth-ms` en Producción y Staging con resolución verificada
```bash
docker restart masterhub-auth-ms-1 masterhub-auth-ms-staging
```

### Paso 3: Probar resolución y conectividad desde dentro de los contenedores
```bash
docker exec masterhub-auth-ms-1 ping -c 2 postgres-local
docker exec masterhub-auth-ms-staging ping -c 2 postgres-local
```

### Paso 4: Validar Login End-to-End
* Probar login con credenciales en `https://staging.mastergroupve.com/login`.
* Probar login con credenciales en `https://masterhub.mastergroupve.com/login`.

---

## 4. Estado de los Componentes al Cierre de Turno
* **Freno de Pago (Payment Brake / Xetux)**: 100% implementado, probado con 68 tests unitarios pasando, esquemas Prisma sincronizados en `finance_db` de staging y prod, y documentación SOP generada.
* **Plane**: Tarea **`MASTERHUB-124`** programada para validación funcional del freno de pago.
* **Git Remotes**: `team` y `origin` perfectamente alineados en local, staging y producción apuntando al repo de la organización.
* **Políticas DLP**: Se mantuvo rigurosamente la directriz de **CERO pérdida de datos**, sin usar banderas destructivas.
