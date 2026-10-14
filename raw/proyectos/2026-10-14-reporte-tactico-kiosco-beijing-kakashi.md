# 🥷 Reporte Táctico: Certificación y Plan de Pruebas Kiosco Beijing Restaurant

- **Fecha**: 2026-10-14
- **Agente Responsable**: 🥷 **Kakashi Sensei** (Mobile UI/UX Ninja) & 🧙‍♂️ **Grandalf** (Tech Lead)
- **Ubicación del Código**: `C:\Users\vmontoyaMG\Desktop\beijing_menu`
- **Hardware Objetivo**: Pantalla Táctil Vertical **APOLOSIGN SW3299T** (32" 4K UHD, Android 16, Rockchip RK3576).

---

## 1. Certificación de Calidad

- **Análisis Estático (`flutter analyze`)**: 100% limpio (`No issues found!`, 0 errores, 0 lints rotos).
- **Pruebas Unitarias (`flutter test`)**: 6 de 6 aprobadas (`CartViewModel` validando subtotal, IVA 16% SENIAT, total general, variantes por porción, operaciones matemáticas y generación de código de orden).
- **Stack**: Flutter 3.47.6 / Dart 3.13.5 en canal stable.

---

## 2. Diagnóstico de Dispositivos y ADB

- **Ruta ADB**: `C:\Users\vmontoyaMG\AppData\Local\Android\sdk\platform-tools\adb.exe`.
- **Dispositivos Locales Detectados**: Windows Desktop, Chrome y Edge.
- **Terminales Android Conectados**: Ninguno en este instante. La pantalla Apolosign se puede enlazar por cable USB-C o por Wi-Fi ADB (`adb connect <IP>:5555`).

---

## 3. Comandos de Compilación del APK

- **APK Universal Release**:
  ```powershell
  flutter build apk --release
  ```
- **APK Optimizado ARM64 (SoC RK3576)**:
  ```powershell
  flutter build apk --release --split-per-abi
  ```

---

## 4. Opciones de Prueba Inmediata para Hoy

1. **Prueba Inmediata en Navegador Web (Chrome)**:
   ```powershell
   cd C:\Users\vmontoyaMG\Desktop\beijing_menu
   flutter run -d chrome
   ```
   *Nota*: Abrir DevTools (F12) y fijar tamaño vertical `1080 x 1920`.

2. **Prueba en Dispositivo Físico (Apolosign SW3299T o Tablet)**:
   - Activar depuración USB en Ajustes de Desarrollador.
   - Instalar vía ADB:
     ```powershell
     & "C:\Users\vmontoyaMG\AppData\Local\Android\sdk\platform-tools\adb.exe" install -r build\app\outputs\flutter-apk\app-release.apk
     ```
   - O copiar el APK generado a un pendrive USB para instalación manual.
