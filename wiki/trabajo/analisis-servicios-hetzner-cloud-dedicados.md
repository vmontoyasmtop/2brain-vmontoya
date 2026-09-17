---
title: "Análisis Integral de Servicios de Hetzner Online (Cloud, Dedicados, Storage & Networking)"
type: "concept"
area: "trabajo"
created: 2026-09-17
updated: 2026-09-17
tags:
  - hetzner
  - cloud
  - vps
  - dedicated-servers
  - storage-box
  - coolify
  - infra
---

# 🌐 Análisis Integral de Servicios de Hetzner Online (`hetzner.com`)

*Evaluación ejecutiva y técnica de las líneas de servicio de Hetzner Online para la infraestructura de MasterGroup (MasterHub) y SmartOps VE.*

---

## 📊 1. Resumen Ejecutivo
**Hetzner Online** es uno de los proveedores de infraestructura en la nube y servidores dedicados (*Bare Metal*) más competitivos del mercado global. Destaca por ofrecer la mejor relación **Rendimiento / Precio**, reduciendo costos entre un **60% y 80%** frente a proveedores tradicionales como AWS, Google Cloud o Microsoft Azure.

---

## ☁️ 2. Líneas de Producto Principales

### 1. Hetzner Cloud (Servidores Nube / VPS)
Servidores virtuales con almacenamiento NVMe ultrarrápido, aprovisionamiento en segundos e integración nativa con Docker, Kubernetes, Terraform y **Coolify**.

*   **Línea CAX (ARM64 - Ampere Altra)**:
    *   Arquitectura ARM de alta eficiencia energética y excelente costo/rendimiento. Ideal para microservicios NestJS, containers Docker y aplicaciones web.
*   **Línea CX / CPX (Shared vCPU - AMD EPYC / Intel Xeon)**:
    *   `CX`: Instancias de bajo costo para tareas livianas, entornos staging y bots.
    *   `CPX`: Instancias con mayor capacidad de cómputo y rendimiento de CPU sostenido.
*   **Línea CCX (Dedicated vCPU - AMD EPYC)**:
    *   vCPUs 100% dedicados para bases de datos críticas (PostgreSQL/MySQL), caché intensivo o compilaciones de producción sin vecino ruidoso (*noisy neighbor*).
*   **Servicios Nube Complementarios**:
    *   **Cloud Volumes**: Almacenamiento en bloque SSD/NVMe extensible hasta 10 TB por volumen.
    *   **Load Balancers**: Balanceadores de carga gestionados con terminación SSL/TLS automática.
    *   **Primary / Floating IPs**: Direcciones IPv4/IPv6 asignables dinámicamente.
    *   **Cloud Firewalls**: Cortafuegos de red gratuitos a nivel de infraestructura.

---

### 2. Dedicated Servers (Servidores Bare Metal)
Servidores físicos sin capa de virtualización, ideales para cargas de trabajo extremas, clústeres de bases de datos de alto rendimiento o virtualización propia (Proxmox/ESXi).

*   **AX-Line (AMD Ryzen / AMD EPYC)**: Máximo rendimiento multinúcleo para desarrollo, compilaciones y aplicaciones exigentes.
*   **EX-Line (Intel Core / Intel Xeon)**: Servidores equilibrados orientados a plataformas empresariales.
*   **PX-Line (Enterprise Xeon con Memoria ECC)**: Servidores de grado empresarial con redundancia de hardware y corrección de errores en memoria.
*   **SX-Line (Storage Dedicated)**: Servidores de almacenamiento masivo con capacidades de 100 TB a 500+ TB en discos enterprise.
*   **Server Auction (Börse / Subasta de Servidores)**: Servidores dedicados reacondicionados **sin costo de instalación (No Setup Fee)** a precios altamente descontados.

---

### 3. Storage Box (Almacenamiento de Respaldo / Backups)
Almacenamiento externo masivo de bajo costo diseñado específicamente para copias de seguridad remotas y valijas digitales.

*   **Protocolos Soportados**: SFTP, SCP, FTP/FTPS, Samba/CIFS, WebDAV, `rsync`, `BorgBackup` y `Restic`.
*   **Planes**: Desde 1 TB (`BX11`) hasta 10 TB+ (`BX31`).
*   **Uso en MasterGroup**: Ideal para respaldos automáticos diarios de bases de datos PostgreSQL (via `pg_dump`) y archivos de MinIO S3.

---

### 4. Ubicaciones de Datacenters & Red
- **Europa**: Alemania (Núremberg y Falkenstein) y Finlandia (Helsinki). Datacenters propios con energía 100% verde y cumplimiento estricto GDPR.
- **Norteamérica**: EE. UU. (Ashburn, Virginia y Hillsboro, Oregón) — *ideal para baja latencia con Venezuela/LATAM*.
- **Asia-Pacífico**: Singapur.
- **Tráfico**: 20 TB de transferencia mensual incluida por servidor nube (1 Gbps / 10 Gbps de ancho de banda).

---

## 🎯 3. Estrategia Sugerida para MasterGroup & SmartOps

| Capa de Infraestructura | Servicio Hetzner Recomendado | Caso de Uso |
| :--- | :--- | :--- |
| **PaaS & Microservicios (MasterHub)** | **Hetzner Cloud CPX / CAX + Coolify** | Despliegue de `api-gateway`, `hr-ms`, `finance-ms`, `auth-ms`, `frontend-ui-dashboard`. |
| **Bases de Datos de Producción** | **Hetzner Cloud CCX (Dedicated vCPU)** | PostgreSQL principal con almacenamiento NVMe persistente. |
| **Backups & Valija Digital** | **Hetzner Storage Box (BX11/BX21)** | Copias de seguridad remotas automatizadas en segundo plano. |
| **Bypass SSL & Routing** | **Cloud Load Balancer / Traefik** | Enrutamiento seguro HTTPS y balanceo de carga. |

---

*Documento elaborado para referencia del equipo de arquitectura y subagentes.*
