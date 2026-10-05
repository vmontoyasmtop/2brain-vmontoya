# 👥 MasterHub — Microservicio de Recursos Humanos (`MS-HR`)

## 📌 Resumen del Proyecto
* **Proyecto**: Suite MasterHub - Módulo de RRHH
* **Liderazgo Técnico**: Ing. Víctor Montoya
* **Gestor de Tareas**: [Plane (projects.mastergroupve.com)](https://projects.mastergroupve.com/it---mg/projects/b60ea600-1f86-4177-87df-6b6ed0063874/modules/0d84505e-5a91-452d-be32-50072240e888)
* **Sprint Activo / Tarea Inmediata**: [`MASTERHUB-131`](https://projects.mastergroupve.com/it---mg/projects/b60ea600-1f86-4177-87df-6b6ed0063874/issues/acde77c6-dede-4d01-a291-bfeff7580bba) — Portal de Selección & Vacantes para Gerente de Tienda
* **Tags**: `rrhh`, `frontend`, `backend`

---

## 🗺️ Roadmap de Desarrollo (Plan de Fases)

### 🔹 Fase 1: Core del Expediente & Ficha Integral
* Ficha Médica de colaboradores
* Registro de Tallas y Uniformes
* Datos Vehiculares y Logísticos
* Expediente único de colaborador

### 🔹 Fase 2: Reclutamiento, Selección & Onboarding
* Gestión de vacantes abiertas
* Banco de CVs y postulantes
* Pruebas de selección
* Flujo de onboarding digital

### 🔹 Fase 3: Nómina, Tabulador Salarial & Variaciones
* Tabulador salarial por cargos
* Gestión de variaciones (días redoblados, incidencias, deducciones)
* Cálculo y validación de nómina

### 🔹 Fase 4: Desincorporaciones (Offboarding) & KPIs
* Flujo de offboarding y liquidación
* Indicadores clave de rotación de personal (KPIs)

---

## 🏗️ Arquitectura Técnica
- **Base de Datos**: `hr_db` en PostgreSQL.
- **Esquema de Datos**: Prisma ORM.
- **Endpoints REST**: Exposición a través de API Gateway.
- **Frontend UI**: Dashboard UI integrado en MasterHub.
