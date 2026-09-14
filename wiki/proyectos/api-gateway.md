---
title: "Proyecto: API Gateway Core"
type: "concept"
area: "proyectos"
created: 2026-09-12
updated: 2026-09-12
tags:
  - proyectos
  - api-gateway
  - nestjs
  - aws-s3
  - microservicios
---

# 🛠️ Proyecto: API Gateway Core

**API Gateway Core** es un microservicio base e infraestructura de ruteo para proyectos construidos con NestJS y almacenamiento AWS.

**Área**: [[Área Proyectos - Software Independiente|pilar-proyectos.md]]  
**Subagente Evaluador**: [[Subagente Backend JS Expert|../../agents/backend_js_expert.md]]

---

## 🛠️ Stack Tecnológico

- **Framework**: NestJS `11` + Express platform
- **Microservices Package**: `@nestjs/microservices`
- **Almacenamiento Cloud**: AWS SDK v3 para S3 (`@aws-sdk/client-s3`)
- **Validación & Transformación**: `class-validator` & `class-transformer`
- **Testing**: Jest `30` + Supertest `7`

---

## ⚡ Comandos Principales

- `npm run start:dev`: Iniciar servidor de gateway en modo desarrollo.
- `npm run build`: Compilar proyecto NestJS.
- `npm run test`: Ejecutar pruebas unitarias en Jest.

---

## 🔗 Relación en 2brain
- [[Área Programación - Conocimiento Técnico|../programacion/pilar-programacion.md]]
