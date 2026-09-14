# Script de Sincronización Automática 2brain Multiequipo

Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "   ALFRED 2brain - Sincronización Automática Git" -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host ""

$fecha = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

# 1. Pull de cambios remotos
Write-Host "[1/3] Descargando últimos cambios remotos (git pull)..." -ForegroundColor Yellow
git pull origin main --quiet

# 2. Agregar cambios locales
Write-Host "[2/3] Guardando cambios locales en el historial..." -ForegroundColor Yellow
git add .
$changes = git status --porcelain
if ($changes) {
    git commit -m "auto(2brain): sincronización de contenido [$fecha]" --quiet
    Write-Host "  ✅ Cambios locales registrados con éxito." -ForegroundColor Green
} else {
    Write-Host "  ℹ️ No se detectaron cambios locales nuevos." -ForegroundColor Gray
}

# 3. Push a la nube
Write-Host "[3/3] Subiendo cambios respaldados a la nube (git push)..." -ForegroundColor Yellow
git push origin main --quiet

Write-Host ""
Write-Host "¡Sincronización completada exitosamente!" -ForegroundColor Green
