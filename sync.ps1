# Script de Sincronización Automática 2brain Multiequipo

Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "   ALFRED 2brain - Sincronización Automática Git" -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host ""

$fecha = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$branch = (git branch --show-current).Trim()
if (-not $branch) { $branch = "master" }

# 1. Pull de cambios remotos
Write-Host "[1/3] Descargando últimos cambios remotos (git pull origin $branch)..." -ForegroundColor Yellow
git pull origin $branch --quiet

# 2. Agregar cambios locales
Write-Host "[2/3] Guardando cambios locales en el historial..." -ForegroundColor Yellow
git add .
$changes = git status --porcelain
if ($changes) {
    git commit -m "auto(2brain): sincronización de contenido [$fecha]" --quiet
    Write-Host "  Cambios locales registrados con exito." -ForegroundColor Green
} else {
    Write-Host "  No se detectaron cambios locales nuevos." -ForegroundColor Gray
}

# 3. Push a la nube
Write-Host "[3/3] Subiendo cambios respaldados a la nube (git push origin $branch)..." -ForegroundColor Yellow
git push origin $branch --quiet

Write-Host ""
Write-Host "Sincronizacion completada exitosamente!" -ForegroundColor Green
