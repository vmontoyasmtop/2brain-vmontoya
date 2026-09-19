---
title: "Guía Operativa: Prueba Piloto del Agente Empresarial (MasterGroup Enterprise)"
type: "guide"
area: "trabajo"
project: "2brain-product"
created: 2026-09-18
updated: 2026-09-18
author: "ALFRED (Mayordomo & Copiloto Ejecutivo)"
tags:
  - prueba-piloto
  - agente-empresarial
  - mastergroup
  - setup-empresa
---

# 🚀 Guía de Activación: Prueba Piloto del Agente Empresarial

*Paso a paso para configurar y probar el **Agente Empresarial** usando la plantilla sanitizada `2brain-template` y la cuenta corporativa de MasterGroup.*

---

## 🎯 1. Preparación del Entorno

1. **Ubicación Base**: La plantilla lista se encuentra en `C:\Users\vmontoyaMG\Desktop\2brain-template`.
2. **Directorio de Prueba**: Podemos crear una copia limpia en `C:\Users\vmontoyaMG\Desktop\2brain-mastergroup-empresa` o ejecutar el setup directamente.

---

## 🚀 2. Pasos de Activación (Solo 3 Minutos)

### Paso 1: Ejecutar el Setup Interactivo
Abrir PowerShell y ejecutar:
```powershell
cd C:\Users\vmontoyaMG\Desktop\2brain-template
.\setup.ps1
```

**Ingresar los datos empresariales**:
- **Nombre del Usuario**: `Víctor Montoya / Dirección Ejecutiva`
- **Nombre del Agente**: `ALFRED Business` (o `MasterAI`)
- **Empresa / Organización**: `MasterGroup VE`

### Paso 2: Autenticación con la Cuenta Corporativa
En la misma terminal, ejecutar:
```bash
agy auth login
```
Seleccionar *"Iniciar sesión con Google"* e ingresar las credenciales de la cuenta corporativa (`soporte@mastergroupve.com` / cuenta de empresa).

---

## 🤖 3. Armar los Subagentes Empresariales Específicos (`agents/`)

Dentro de la carpeta `agents/` del proyecto empresarial, agregamos o adaptamos los subagentes especializados para la empresa:

1. **`operations_expert.md` (Experto en Operaciones IT & Sucursales)**:
   - Encargado de redactar informes de soporte, supervisión de Xetux, Helpdesk e inventario.
2. **`sales_proposal_expert.md` (Experto en Cotizaciones & Propuestas Comercial)**:
   - Encargado de formular cotizaciones, propuestas comerciales en PDF/Docs y presupuestos.
3. **`finance_analyst.md` (Analista de Finanzas & Cuentas por Pagar/Cobrar)**:
   - Encargado de procesar hojas de cálculo de CxP, CxC y balances mensuales.
4. **`software_architect.md` (Copiloto de Código MasterHub & Proyectos)**:
   - Encargado de supervisar los microservicios de MasterHub, Brotapp y Meniox.

---

## 🧪 4. Pruebas de Funcionamiento

Una vez autenticado:
1. Probar la consulta a las 6 áreas del Agente Empresarial.
2. Generar un documento corporativo de prueba usando el subagente `docs_expert.md`.
3. Validar el tiempo de respuesta y la precisión agéntica.
