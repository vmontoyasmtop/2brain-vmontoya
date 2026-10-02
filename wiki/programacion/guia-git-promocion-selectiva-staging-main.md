# Guía Git: Promoción Selectiva de Cambios (Staging / Dev a Main) sin Merge Masivo

- **Área**: 💻 `programacion` & 🚀 `proyectos`
- **Proyecto**: MasterHub Monorepo (`MG-HUB`)
- **Autor / Asistente**: 🤵 **ALFRED Pennyworth**
- **Fecha de Registro**: 2026-10-01
- **Estado**: Activo / Documentado

---

## 1. Contexto y Problemática

En el flujo de integración continua de MasterHub existen ramas intermedias (`dev` y `staging`) donde convergen desarrollos paralelos (por ejemplo, múltiples iteraciones de finanzas, retenciones SENIAT, facturas, etc.).

Cuando se concluye una funcionalidad prioritaria o un hotfix (por ejemplo: **Reubicación de Administración a Sistema y Módulo de Permisos Granulares SÍ/NO**), surge la necesidad de **promover única y exclusivamente esa funcionalidad a `main`** para su despliegue en producción, **sin realizar un `git merge staging` o `git merge dev` completo** que arrastraría código incompleto o no auditado.

---

## 2. Estrategias Técnicas

### Estrategia A: `git cherry-pick` mediante Rama de Release / PR (Recomendada)
Esta es la vía estándar empresarial para pasar por code-review y auditoría de GitHub Actions sin contaminar `main`:

```bash
# 1. Asegurar tener main actualizado
git checkout main
git pull team main

# 2. Crear una rama de release aislada desde main
git checkout -b release/sistema-rbac-granular main

# 3. Aplicar exclusivamente el commit deseado (ejemplo: commit 1636422)
git cherry-pick 1636422

# 4. Subir la rama al repositorio remoto
git push team release/sistema-rbac-granular

# 5. Crear el Pull Request en GitHub:
# Base: main <- Compare: release/sistema-rbac-granular
```

> [!TIP]
> Si son múltiples commits consecutivos, se puede especificar un rango:
> `git cherry-pick hashPrimerCommit^..hashUltimoCommit`

---

### Estrategia B: Extracción Selectiva por Archivos o Carpetas (`git checkout / restore`)
Útil cuando el código deseado no está aislado en un solo commit, sino disperso en varios commits de `staging`:

```bash
# 1. Posicionarse en una rama basada en main
git checkout -b release/parche-selectivo main

# 2. Traer selectivamente solo los archivos o directorios desde staging
git checkout staging -- apps/frontend-ui-dashboard/src/app/dashboard/users/
git checkout staging -- apps/frontend-ui-dashboard/src/lib/rbac.ts
git checkout staging -- apps/auth-ms/src/auth/

# 3. Revisar estado y confirmar
git status
git commit -m "feat(system): portar módulo rbac y usuarios selectivamente desde staging"
git push team release/parche-selectivo
```

---

### Estrategia C: `git cherry-pick` Directo a `main` (Fast-track)
Si el usuario cuenta con permisos de push directo a `main` y desea aplicar el parche de inmediato:

```bash
git checkout main
git pull team main
git cherry-pick 1636422
git push team main
```

---

## 3. Registro de Caso Práctico (Turno 2026-10-01)

- **Commit en Dev**: `1636422`
  - *Mensaje*: `feat(system): reubicar administracion a sistema, modulo rbac con permisos granulares si/no y filtros por sede`
  - *Alcance*:
    1. Reubicación semántica de enlaces de navegación (Usuarios, Personal, Auditoría, Respaldos) bajo «Sistema».
    2. Modal interactivo 3-en-1: Roles departamentales, Permisos Granulares SÍ/NO (con interruptores independientes por acción) y Perfil.
    3. Corrección de filtros de visibilidad de sedes para Gerentes en Tickets y Vacantes.
    4. Corrección de columna `Department.sedeCount` en base de datos.
- **Acción Programada para 2026-10-02**:
  - Aplicar Estrategia A para generar el PR limpio a `main` usando el commit `1636422`.
  - Tarea programada en Google Tasks: `UERUNTM2eDF1MVhxU2pvRA`.
