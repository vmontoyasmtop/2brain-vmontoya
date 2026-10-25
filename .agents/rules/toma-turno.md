# Protocolo TOMA_TURNO (Inicio de Jornada)
Ejecuta de inmediato y sin pedir confirmación:
1. **Sincronización Git**: git pull origin master
2. **Lectura de Memoria**: Leer entradas recientes de wiki/log.md y wiki/life-dashboard.md.
3. **Inicio de Servicios**: Verificar e iniciar en segundo plano python scripts/telegram_bot.py si existe.
4. **Consulta Multicuenta de Nube**: Consultar Google Calendar (personal y trabajo), Gmail y ClickUp.
5. **Informe de Bienvenida Ejecutiva**: Presentar al Señor el resumen del último turno, agenda del día, alertas y primer bloque de enfoque.
