---
title: "Regla Estándar de Diseño y Tokens UI/UX Frontend (MasterHub)"
type: "guide"
area: "programacion"
created: 2026-09-25
updated: 2026-09-25
sources: []
tags:
  - ui
  - ux
  - frontend
  - nextjs
  - tailwind
  - masterhub
  - design-system
---

# 🎨 Regla Estándar de Diseño y Tokens UI/UX Frontend (MasterHub)

Documento normativo oficial redactado por **ALFRED** / **Legolas Hojaverde** para regir el desarrollo y la estandarización de interfaces en `apps/frontend-ui-dashboard` dentro del ecosistema **MasterHub**.

---

## 📌 1. Principio Fundamental: Patrón Híbrido Institucional

El diseño de MasterHub (como se observa en **Tickets/Helpdesk**, **Resumen RRHH** y **Equipos/Inventario**) implementa un **patrón híbrido de alto impacto**:

1. **Bloques de Mando y Control Oscuros (`Master Black`)**:
   - Tarjetas KPI, Bloques de Búsqueda/Filtros, Botones de Enlace Superior y Ventanas Modales utilizan el fondo institucional `bg-[var(--master-black)]` con bordes finos `border-white/10`, textos en blanco (`text-white`, `text-white/60`, `text-white/40`), sombras profundas (`shadow-xl`, `shadow-2xl`) y acentos dorados/marca (`brand-gradient-text`, `bg-accent/20 text-accent`).
2. **Tablas de Datos Claras / Semánticas**:
   - Para garantizar la máxima legibilidad y auditoría de datos densos (montos, facturas, fechas, estados), las tablas principales utilizan contenedores de fondo claro `bg-white border border-border shadow-sm`, con cabeceras `bg-bg-subtle text-muted`, filas interactivas `hover:bg-surface-hover`, textos principales en `text-foreground` y badges semánticos (`Badge`).

> [!IMPORTANT]
> **REGLA DE CONTEXTO VISUAL**:
> - En bloques oscuros (`bg-[var(--master-black)]`, modales oscuros): usar `text-white`, `text-white/70`, `text-white/40`, inputs `bg-white/5 border-white/10 text-white` y selects `bg-neutral-900 border-white/10 text-white [color-scheme:dark]`.
> - En tablas de datos claras (`bg-white`): usar `text-foreground`, `text-muted` y badges con variantes semánticas.

---

## 🏛️ 2. Especificación de Componentes

### 2.1. Tarjetas KPI de Dashboard (Master Black)
Deben seguir el componente de métricas oscuras idéntico a Tickets y Equipos:
```tsx
<FadeIn delay={0.05} className="rounded-xl border border-white/10 bg-[var(--master-black)] p-4 shadow-xl">
  <div className="flex items-center gap-3">
    <div className="inline-flex h-10 w-10 items-center justify-center rounded-xl bg-accent/20 text-accent">
      <MaterialSymbolIcon name="receipt_long" className="brand-icon text-[20px]" color="current" />
    </div>
    <div className="min-w-0">
      <p className="text-xs uppercase tracking-[0.16em] text-white/60">Facturas Registradas</p>
      <p className="brand-gradient-text mt-1 text-2xl font-semibold">{count}</p>
    </div>
  </div>
  {helper && <p className="mt-2 text-xs text-white/40">{helper}</p>}
</FadeIn>
```

### 2.2. Bloque de Filtros y Búsqueda (Master Black)
Contenedor oscuro con elevación:
```tsx
<FadeIn className="rounded-xl border border-white/10 bg-[var(--master-black)] shadow-2xl p-4">
  <div className="grid grid-cols-1 gap-3 md:grid-cols-12">
    {/* Input de Búsqueda */}
    <div className="relative md:col-span-6">
      <span className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3 text-white/40">
        <MaterialSymbolIcon name="search" className="text-lg" />
      </span>
      <input
        type="text"
        placeholder="Buscar..."
        className="w-full rounded-xl border border-white/10 bg-white/5 py-2 pl-9 pr-3 text-xs text-white placeholder:text-white/40 outline-none ring-accent focus:ring-1 focus:border-accent"
      />
    </div>
    {/* Selectores */}
    <div className="md:col-span-3">
      <select
        className="w-full rounded-xl border border-white/10 bg-neutral-900 px-3 py-2 text-xs text-white outline-none ring-accent focus:ring-1 focus:border-accent [&>option]:bg-neutral-900 [&>option]:text-white [color-scheme:dark]"
      >
        <option value="ALL">Todos los Estados</option>
      </select>
    </div>
  </div>
</FadeIn>
```

### 2.3. Botones de Enlace Superior
```tsx
<Link
  href="/dashboard/finance/cxp/approval"
  className="rounded-xl border border-white/10 bg-[var(--master-black)] px-3 py-2 text-xs font-medium text-white/80 hover:bg-white/10 hover:text-white transition inline-flex items-center gap-2 shadow-md"
>
  <MaterialSymbolIcon name="fact_check" className="text-base text-warning" />
  Bandeja de Aprobación
</Link>
```

### 2.4. Modales (`FormModal`) Oscuros
Todas las ventanas modales de edición, creación, detalle y liquidación deben utilizar `theme="dark"`:
```tsx
<FormModal
  isOpen={isOpen}
  onClose={onClose}
  title="Título del Formulario"
  description="Descripción institucional."
  size="xl"
  theme="dark"
>
  {/* Etiquetas */}
  <label className="mb-1 block text-xs font-medium text-white/70">Nombre del Campo</label>
  
  {/* Inputs oscuros */}
  <input
    type="text"
    className="w-full rounded-xl border border-white/10 bg-white/5 px-3 py-2 text-sm text-white placeholder:text-white/40 outline-none ring-accent focus:ring-1 focus:border-accent"
  />

  {/* Selects oscuros */}
  <select
    className="w-full rounded-xl border border-white/10 bg-neutral-900 px-3 py-2 text-sm text-white outline-none ring-accent focus:ring-1 focus:border-accent [&>option]:bg-neutral-900 [&>option]:text-white [color-scheme:dark]"
  >
    <option value="...">Opción</option>
  </select>

  {/* Botones de Pie de Modal */}
  <div className="flex justify-end gap-2.5 pt-3 border-t border-white/10">
    <button
      type="button"
      className="rounded-xl border border-white/10 bg-white/5 px-4 py-2 text-xs font-medium text-white/80 hover:bg-white/10 hover:text-white transition"
    >
      Cancelar
    </button>
    <button
      type="submit"
      className="brand-button inline-flex items-center gap-1.5 rounded-lg px-4 py-2 text-sm font-semibold transition shadow-md"
    >
      Guardar
    </button>
  </div>
</FormModal>
```

### 2.5. Tablas de Datos Institucionales (Claras / Semánticas)
```tsx
<FadeIn delay={0.1} className="relative overflow-x-auto rounded-xl border border-border bg-white shadow-sm">
  <table className="min-w-full divide-y divide-border text-sm">
    <thead className="bg-bg-subtle">
      <tr className="text-left text-muted">
        <th className="px-4 py-3 font-semibold text-foreground">Documento</th>
        <th className="px-4 py-3 font-semibold text-foreground">Proveedor</th>
        <th className="px-4 py-3 text-right font-semibold text-foreground">Monto Total</th>
        <th className="px-4 py-3 text-center font-semibold text-foreground">Estado</th>
        <th className="px-4 py-3 text-center font-semibold text-foreground">Acciones</th>
      </tr>
    </thead>
    <tbody className="divide-y divide-border">
      <tr className="hover:bg-surface-hover transition-colors">
        <td className="px-4 py-3 font-mono font-semibold text-foreground">#FAC-001</td>
        <td className="px-4 py-3 text-foreground">Inversiones MG</td>
        <td className="px-4 py-3 text-right font-mono font-bold text-foreground">$1,200.00</td>
        <td className="px-4 py-3 text-center">
          <Badge variant="brand" size="sm" dot>En Proceso</Badge>
        </td>
        <td className="px-4 py-3 text-center">...</td>
      </tr>
    </tbody>
  </table>
</FadeIn>
```

---

## 🛡️ 3. Módulos de Referencia en el Código
Para verificar este patrón en producción, consultar:
1. **Tickets**: `apps/frontend-ui-dashboard/src/components/dashboard/helpdesk/helpdesk-tickets-client.tsx`
2. **Finanzas (CxP)**: `apps/frontend-ui-dashboard/src/components/dashboard/finance/cxp-dashboard-client.tsx`
3. **Resumen RRHH**: `apps/frontend-ui-dashboard/src/components/dashboard/hr/hr-summary.tsx`
4. **Equipos**: `apps/frontend-ui-dashboard/src/components/dashboard/products/`
