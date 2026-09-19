---
title: "Proyecto: Meniox"
type: "project"
area: "proyectos"
created: 2026-09-12
updated: 2026-09-18
tags:
  - 
---

# 🛒 Proyecto: Meniox

**Meniox** es un sistema integral de **Point of Sale (POS)** y **Administración de Franquicias**, diseñado con microservicios escalables, cola de mensajes Asíncrona (RabbitMQ) y apps cliente (Next.js + App Móvil POS).

**Área**: [[pilar-proyectos|Área Proyectos - Software Independiente]]  
**Subagentes Evaluadores**: [Subagente Backend JS Expert](../../agents/backend_js_expert.md) & [Subagente Frontend UI Expert](../../agents/frontend_ui_expert.md)

---

## 🛠️ Arquitectura de Microservicios (`apps/`)

- **`gateway`**: API Gateway principal.
- **`auth-service`**: Autenticación y control de acceso.
- **`org-service`**: Gestión de organizaciones y sucursales.
- **`catalog-service`**: Catálogo de productos, categorías y precios.
- **`inventory-service`**: Control de existencias, almacenes y stock.
- **`sales-service`**: Procesamiento de ventas y facturación.
- **`franchise-admin`**: Portal de administración de franquicias en Next.js 15 + Tailwind CSS 4 + Framer Motion.
- **`pos-mobile`**: App móvil de punto de venta rápida para terminales de caja.

---

## ⚙️ Stack Tecnológico

- **Backend**: NestJS `11` + TypeScript `5.9`
- **Mensajería / Broker**: RabbitMQ (`amqplib` `0.10`)
- **Base de Datos**: PostgreSQL (`pg` `8.16`)
- **Frontend Admin**: Next.js `15`, React `19`, Tailwind CSS `4`, Lucide React, SweetAlert2.

---

## ⚡ Comandos de Ejecución

- `npm run start:gateway`: Iniciar Gateway API.
- `npm run start:auth`, `start:catalog`, `start:inventory`, `start:sales`: Iniciar microservicios individuales.
- `npm run start:franchise-admin`: Iniciar panel de franquicias en puerto 3010.
- `npm run start:pos-mobile`: Iniciar aplicación móvil POS.

---

## 🔗 Relación en 2brain
- [[pilar-programacion|Área Programación - Conocimiento Técnico]]
- [[pilar-finanzas-personales|Área Finanzas - Gestión Económica]]
