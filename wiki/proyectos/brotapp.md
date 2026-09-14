---
title: "Proyecto: Brotapp"
type: "concept"
area: "proyectos"
created: 2026-09-12
updated: 2026-09-12
tags:
  - proyectos
  - mobile
  - react-native
  - expo
  - typescript
---

# 📱 Proyecto: Brotapp

**Brotapp** es una aplicación móvil multiplataforma (Android, iOS y Web) construida con tecnologías modernas de desarrollo híbrido.

**Área**: [[Área Proyectos - Software Independiente|pilar-proyectos.md]]  
**Subagente Evaluador**: [[Subagente Frontend UI Expert|../../agents/frontend_ui_expert.md]]

---

## 🛠️ Arquitectura & Stack Tecnológico

- **Framework Móvil**: React Native `0.86.2` + Expo SDK `57`
- **Lenguaje**: TypeScript `6.0`
- **Librería UI**: React `19.2`
- **Almacenamiento Local**: `@react-native-async-storage/async-storage`
- **Componentes Gráficos**: `react-native-svg` & `@expo/vector-icons`
- **Build System**: Expo CLI & Gradle para APKs locales Android (`gradlew.bat assembleRelease`)

---

## ⚡ Scripts Principales

- `npm run start`: Iniciar servidor de desarrollo de Expo.
- `npm run android`: Ejecutar en emulador/dispositivo Android.
- `npm run ios`: Ejecutar en simulador iOS.
- `npm run web`: Ejecutar versión web en navegador.
- `npm run build:apk-local`: Compilar APK de producción local para Android.

---

## 🔗 Relación en 2brain
- [[Área Programación - Conocimiento Técnico|../programacion/pilar-programacion.md]]
