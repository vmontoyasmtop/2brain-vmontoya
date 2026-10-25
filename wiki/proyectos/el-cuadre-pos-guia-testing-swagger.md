---
title: "Guía Interactiva de Testing con Swagger UI: EL CUADRE POS"
type: "concept"
area: "proyectos"
status: "active"
created: 2026-10-24
updated: 2026-10-24
tags:
  - kakuzu-backend
  - swagger
  - openapi
  - testing
  - el-cuadre-pos
  - nestjs
---

# 🧪 Guía de Testing Interactivo con Swagger UI — EL CUADRE POS
**Arquitecto Backend**: 🖤 Kakuzu (Akatsuki Backend & DB)  
**URL Oficial de Swagger UI**: [http://localhost:3001/api/docs](http://localhost:3001/api/docs)  
**URL Especificación OpenAPI JSON**: [http://localhost:3001/api/docs-json](http://localhost:3001/api/docs-json)  
**Ubicación Local**: `C:\Users\vmont\OneDrive\Desktop\el-cuadre-pos\docs\GUIA_TESTING_SWAGGER.md`  

---

## 🚀 Cómo Iniciar el Backend para Pruebas

Haga doble clic en el archivo:
`C:\Users\vmont\OneDrive\Desktop\el-cuadre-pos\iniciar-backend.bat`

O por terminal:
```bash
cd C:\Users\vmont\OneDrive\Desktop\el-cuadre-pos\backend
npm run start:dev
```

---

## 📋 Módulos y Flujo de Pruebas en Swagger

| Módulo | Endpoint Clave | Acción de Prueba |
| :--- | :--- | :--- |
| 🔐 **Autenticación** | `POST /api/auth/login` | Iniciar sesión con `admin`/`admin123` o `cajero`/`cajero123`. |
| 💵 **Caja y Turnos** | `GET /api/cash-sessions/current` | Verificar sesión activa con base de $50 USD. |
| 💸 **Gastos Menores** | `POST /api/cash-sessions/expense` | Registrar salida de dinero para bolsas/hielo. |
| ⚖️ **Productos** | `GET /api/products` | Explorar 15 productos por unidad y por Kg ($ y Bs). |
| 🧾 **Ventas y Vueltos** | `POST /api/sales` | Simular compra de tomates (Kg) y harina con cálculo de vuelto. |
| 📒 **Libro de Fiados** | `GET /api/customers` | Consultar deudas de Doña Carmen y Roberto Gómez. |
| 💳 **Abonos a Cuenta** | `POST /api/customers/{id}/payments` | Registrar abono de $10 y ver reducción de deuda. |
| 🥬 **Control de Mermas** | `POST /api/losses` | Dar de baja frutas dañadas con justificación técnica. |
| 🔒 **Arqueo Ciego** | `POST /api/cash-sessions/close` | Conteo físico a ciegas y dictamen de cuadre. |
