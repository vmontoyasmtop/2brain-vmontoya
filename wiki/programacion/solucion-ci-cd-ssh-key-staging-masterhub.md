# Diagnóstico y Solución: Error de Conexión SSH en Despliegue de Staging (GitHub Actions)

- **Área**: 💻 `programacion` & 🚀 `proyectos`
- **Proyecto**: MasterHub Monorepo (`MG-HUB`)
- **Workflow**: `.github/workflows/deploy-staging.yml`
- **Servidor Objetivo**: `172.238.221.116` (Usuario: `root`, Puerto: `22`, Dominio: `staging.mastergroupve.com`)
- **Fecha**: 2026-10-01 (Para atención prioritaria a primera hora: 2026-10-02)
- **Estado**: ⚠️ Diagnosticado & Solución Lista para Ejecutar

---

## 1. Síntoma y Registro de Error

Al realizar el merge de `dev` a `staging`, GitHub Actions dispara el workflow `Deploy to Staging Server` (`deploy-staging.yml`), el cual falla inmediatamente (0s) en el paso `Deploy via SSH to Staging`:

```log
Run appleboy/ssh-action@v1.0.3
  with:
    host: 172.238.221.116
    username: root
    port: 22
...
2026/10/02 03:13:52 Error: can't connect without a private SSH key or password
```

---

## 2. Análisis de Causa Raíz (RCA)

1. En el workflow `.github/workflows/deploy-staging.yml`, la acción `appleboy/ssh-action@v1.0.3` requiere obligatoriamente una clave privada SSH (`key`) o una contraseña (`password`):
   ```yaml
   key: ${{ secrets.STAGING_SSH_KEY || secrets.SSH_KEY || secrets.ssh_key || ... }}
   password: ${{ secrets.STAGING_SSH_PASSWORD || secrets.SSH_PASSWORD || ... }}
   ```
2. En la configuración del repositorio remoto GitHub (`vmontoyamg-png/MG-HUB` en `Settings -> Secrets and variables -> Actions`), **no existe** ningún Secret configurado con el nombre `SSH_KEY` o `STAGING_SSH_KEY`, o su valor está vacío.
3. Al no existir el secret, el runner de GitHub Actions inyecta una cadena vacía `""`, provocando que la librería SSH de Go aborte con:
   `Error: can't connect without a private SSH key or password`.

---

## 3. Verificación de Conectividad (Validada por ALFRED)

ALFRED realizó una prueba de conexión SSH directa desde la máquina local hacia el servidor VPS usando la clave ed25519 local:
```bash
ssh -o BatchMode=yes -o ConnectTimeout=5 -i C:\Users\vmontoyaMG\.ssh\id_ed25519 root@172.238.221.116 echo "connected"
# Resultado: "connected" (Conexión exitosa al 100%)
```
* **Conclusión**: El servidor `172.238.221.116` tiene autorizada la clave pública de `C:\Users\vmontoyaMG\.ssh\id_ed25519.pub`. Solo hace falta inyectar la clave privada `C:\Users\vmontoyaMG\.ssh\id_ed25519` en los Secrets de GitHub Actions.

---

## 4. Procedimiento de Solución Inmediata (Primera Hora)

1. **Obtener el contenido de la clave privada**:
   Abrir o copiar el archivo local:
   `C:\Users\vmontoyaMG\.ssh\id_ed25519`
   *(Incluyendo los encabezados `-----BEGIN OPENSSH PRIVATE KEY-----` y `-----END OPENSSH PRIVATE KEY-----`)*.

2. **Cargar el Secret en GitHub**:
   - Navegar a: `https://github.com/vmontoyamg-png/MG-HUB/settings/secrets/actions`
   - Clic en **New repository secret**.
   - **Name**: `SSH_KEY` (o `STAGING_SSH_KEY`)
   - **Secret**: Pegar el contenido íntegro de `id_ed25519`.
   - Clic en **Add secret**.

3. **Re-lanzar el Despliegue**:
   - Ir a la pestaña **Actions** en GitHub: `https://github.com/vmontoyamg-png/MG-HUB/actions`
   - Seleccionar la corrida fallida de `Deploy to Staging` y pulsar **Re-run jobs** (o hacer push/merge a `staging`).
   - El despliegue clonará/actualizará `/var/www/mgh/staging` y levantará los contenedores con `docker compose -f docker-compose.staging.yml up -d --build`.
