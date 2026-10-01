# Estándar Corporativo de Filtros UI y Tablas — MasterHub

**Documento Normativo Institucional — Compañía 2brain-MG**  
**Autor:** Compañía de Desarrollo (Grandalf el Blanco, Legolas Hojaverde, Frodo Bolsón)  
**Destinatarios:** Equipo de Ingeniería Frontend, Finanzas, Producto & DevOps  
**Versión:** 2.0.0  
**Fecha:** Septiembre 2026  

---

## 1. Declaración y Filosofía del Estándar

En todas las aplicaciones y módulos de **MasterHub** (especialmente en el ecosistema de Finanzas, Cuentas por Pagar, Cuentas por Cobrar, Tesorería y Auditoría Fiscal), la interfaz de usuario se rige bajo la regla oficial de la Compañía dictaminada por Víctor Montoya:

> **"Filtros en Master Black institucional, Tablas de datos en Blanco de alto contraste (High-Contrast White Table)."**

Esta directriz combina:
1. **Bloque de Filtros en Master Black:** Elegancia, foco visual y sobriedad ejecutiva oscura (`bg-[var(--master-black)] border-white/10 shadow-2xl`).
2. **Tablas de Datos en Blanco Institucional:** Máxima legibilidad, contraste y rapidez visual en el análisis de cifras y tablas densas de datos (`bg-white border-border shadow-sm`).

Queda formalmente prohibida la discrepancia visual entre módulos. Todas las vistas operativas deben compartir de manera estricta esta arquitectura visual, estados y componentes.

---

## 2. Regla de Oro 1: Contenedor y Encabezado de Filtros (Master Black)

Todo bloque de filtros avanzados debe implementarse dentro de un contenedor `<FadeIn>` oscuro institucional con encabezado oficial y botón de limpieza reactivo:

```tsx
<FadeIn className="rounded-xl border border-white/10 bg-[var(--master-black)] shadow-2xl p-4">
  <div className="flex items-center justify-between pb-3 mb-3 border-b border-white/10">
    <div className="flex items-center gap-2">
      <MaterialSymbolIcon name="filter_list" className="text-base text-accent" />
      <h3 className="text-xs font-semibold uppercase tracking-wider text-white">
        Filtros Avanzados de [Nombre del Módulo]
      </h3>
    </div>
    {hasActiveFilters && (
      <button
        onClick={clearFilters}
        className="text-xs text-accent hover:underline inline-flex items-center gap-1"
      >
        <MaterialSymbolIcon name="close" className="text-sm" />
        Limpiar filtros
      </button>
    )}
  </div>

  <div className="grid grid-cols-1 gap-3 md:grid-cols-12">
    {/* Controles de filtro */}
  </div>
</FadeIn>
```

### Especificaciones Mandatorias de Filtros:
1. **Contenedor:** Fondo `bg-[var(--master-black)]`, borde `border border-white/10`, bordes redondeados `rounded-xl`, sombra `shadow-2xl` y padding `p-4`.
2. **Encabezado:** Separador inferior `border-b border-white/10`, padding inferior `pb-3 mb-3`.
3. **Icono del encabezado:** `filter_list` con color `text-accent`.
4. **Tipografía:** Texto blanco en mayúsculas `uppercase tracking-wider text-xs font-semibold text-white`.
5. **Botón Limpiar:** Se renderiza únicamente si `hasActiveFilters` es verdadero, con icono `close` y estilo `text-xs text-accent hover:underline`.

---

## 3. Regla de Oro 2: Input de Búsqueda con Limpieza Integrada

Todo campo de búsqueda general en filtros debe:
- Disponer de un icono de lupa a la izquierda (`search`).
- Incluir un botón de borrado inmediato con la 'X' (`close`) anclado a la derecha, visible sólo cuando el input contenga texto.

```tsx
<div className="relative md:col-span-4">
  <span className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3 text-white/40">
    <MaterialSymbolIcon name="search" className="text-lg" />
  </span>
  <input
    type="text"
    placeholder="Buscar por N° factura, control, proveedor, RIF..."
    value={searchTerm}
    onChange={(e) => setSearchTerm(e.target.value)}
    className="w-full rounded-xl border border-white/10 bg-white/5 py-2 pl-9 pr-9 text-xs text-white placeholder:text-white/40 outline-none ring-accent focus:ring-1 focus:border-accent"
  />
  {searchTerm.length > 0 && (
    <button
      type="button"
      onClick={() => setSearchTerm('')}
      aria-label="Limpiar búsqueda"
      className="absolute inset-y-0 right-0 flex items-center pr-3 text-white/40 transition hover:text-white"
    >
      <MaterialSymbolIcon name="close" className="text-lg" />
    </button>
  )}
</div>
```

---

## 4. Regla de Oro 3: Selectores `FilterSelect` / `CustomSelect` con Sedes Reales

1. **PROHIBIDO:** Usar `<select>` nativos del navegador con fondos claros o desalineados.
2. **PROHIBIDO:** Usar arrays hardcodeados de sedes (`['CCS', 'VAL', 'MAR', 'MG']`).
3. **OBLIGATORIO:** Las sedes deben consultarse en tiempo de ejecución desde la API oficial de inventario:
   ```ts
   import { listSites, SiteItem } from '@/lib/inventory-api';

   useEffect(() => {
     listSites({ limit: 100 })
       .then((res) => {
         if (res.data?.data) {
           setSites(res.data.data);
         }
       })
       .catch(() => {});
   }, []);
   ```
4. **Matching Flexible:** En el filtrado de comprobantes o registros por sede, el algoritmo debe coincidir por `id`, por `code` o por nombre parcial:
   ```ts
   if (buFilter !== 'ALL') {
     const selectedSite = sites.find((s) => s.id === buFilter);
     const match =
       item.bu?.id === buFilter ||
       item.bu?.code === buFilter ||
       (selectedSite && (item.bu?.code === selectedSite.code || item.bu?.name?.toLowerCase() === selectedSite.name.toLowerCase())) ||
       (item.bu?.name && selectedSite && item.bu.name.toLowerCase().includes(selectedSite.name.toLowerCase())) ||
       item.bu?.name?.toLowerCase().includes(buFilter.toLowerCase());
     if (!match) return false;
   }
   ```
5. **Modales de Creación / Edición:** Reemplazar cualquier selector de sede nativo por `CustomSelect` con buscador integrado (`searchable={true}`).

---

## 5. Regla de Oro 4: Tablas de Datos en Blanco Institucional de Alto Contraste (High-Contrast White Table)

Las tablas principales de datos deben implementar rigurosamente el estándar institucional blanco de alto contraste (`bg-white`, `border-border`, `shadow-sm`, cabeceras `thead bg-bg-subtle text-muted text-foreground`, filas `tbody divide-border divide-y`, textos `text-foreground` y `text-muted`, `hover:bg-bg-subtle/50 transition-colors`):

```tsx
{/* Main Table (High-contrast Institutional White Table) */}
<FadeIn delay={0.1} className="relative overflow-x-auto rounded-xl border border-border bg-white shadow-sm">
  <table className="min-w-full divide-y divide-border text-sm">
    <thead className="bg-bg-subtle">
      <tr className="text-left text-muted">
        <th className="px-4 py-3 font-semibold text-foreground">Documento</th>
        <th className="px-4 py-3 font-semibold text-foreground">Proveedor</th>
        <th className="px-4 py-3 font-semibold text-foreground">Categoría & Detalle</th>
        <th className="px-4 py-3 font-semibold text-foreground">Fechas</th>
        <th className="px-4 py-3 text-right font-semibold text-foreground">Monto Total</th>
        <th className="px-4 py-3 text-center font-semibold text-foreground">Estado</th>
        <th className="px-4 py-3 text-center font-semibold text-foreground">Acciones</th>
      </tr>
    </thead>
    <tbody className="divide-y divide-border">
      {loading ? (
        <tr>
          <td colSpan={7} className="px-4 py-12 text-center text-muted">
            <div className="flex flex-col items-center gap-2">
              <MaterialSymbolIcon name="progress_activity" className="animate-spin text-2xl text-accent" />
              <span>Cargando datos...</span>
            </div>
          </td>
        </tr>
      ) : filteredData.length === 0 ? (
        <tr>
          <td colSpan={7} className="px-4 py-12 text-center text-muted">
            <div className="flex flex-col items-center gap-2">
              <MaterialSymbolIcon name="folder_off" className="text-3xl text-muted" />
              <span className="text-sm font-medium text-foreground">No se encontraron registros</span>
              <span className="text-xs text-muted">Ajusta los filtros avanzados o prueba otra búsqueda.</span>
            </div>
          </td>
        </tr>
      ) : (
        filteredData.map((row) => (
          <tr key={row.id} className="hover:bg-bg-subtle/50 transition-colors">
            {/* Celdas con alto contraste */}
            <td className="px-4 py-3 font-medium text-foreground">{row.name}</td>
            <td className="px-4 py-3 text-right font-mono font-semibold text-foreground">${row.total}</td>
            <td className="px-4 py-3 text-center">
              <Badge variant="brand" size="sm" dot>{row.status}</Badge>
            </td>
          </tr>
        ))
      )}
    </tbody>
  </table>
</FadeIn>
```

### Especificaciones Mandatorias de la Tabla Blanca:
1. **Contenedor:** Fondo `bg-white`, borde `border border-border`, esquinas redondeadas `rounded-xl`, sombra sutil `shadow-sm`.
2. **Encabezado (`thead`):** Fondo `bg-bg-subtle`, textos en `text-foreground font-semibold`, etiquetas accesorias en `text-muted`.
3. **Filas (`tbody`):** Divisores `divide-y divide-border`, efecto hover `hover:bg-bg-subtle/50 transition-colors`.
4. **Contraste de Textos:**
   - Textos principales (nombres, títulos, proveedores, N° documentos): `text-foreground`.
   - Metadatos secundarios (RIF, controles, fechas accesorias): `text-muted`.
   - Cifras y montos monetarios: `font-mono text-foreground font-semibold`.
   - Badges y estados: variantes institucionales (`<Badge variant="brand">`, `<Badge variant="success">`, `<Badge variant="warning">`).
5. **Botones de Acción en Fila:** `text-muted hover:text-foreground hover:bg-surface-hover transition`.

---

## 6. Checklist de Validación para Nuevas Vistas

Antes de solicitar Pull Request o desplegar a `team dev`:
- [ ] Bloque de filtros avanzado en contenedor `<FadeIn>` Master Black (`bg-[var(--master-black)] border-white/10 shadow-2xl`).
- [ ] Título formal del módulo con icono `filter_list` text-accent.
- [ ] Botón de limpieza rápida de filtros funcional.
- [ ] Búsqueda reactiva con icono de lupa a la izquierda y 'X' a la derecha.
- [ ] Sedes cargadas dinámicamente vía `listSites({ limit: 100 })`.
- [ ] Selects implementados exclusivamente con `FilterSelect` o `CustomSelect`.
- [ ] Tablas principales de datos en **Blanco Institucional de Alto Contraste** (`bg-white border-border shadow-sm thead bg-bg-subtle`).
- [ ] Verificación de TypeScript sin errores (`npx tsc --noEmit`).
