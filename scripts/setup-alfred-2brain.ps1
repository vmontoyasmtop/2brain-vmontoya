<#
.SYNOPSIS
    Script de Despliegue e Instalación Automatizada de ALFRED & 2brain SYSTEM (COMPLETO & SEGURO)
.DESCRIPTION
    Configura de forma automatizada y segura todos los servidores MCP:
    - ClickUp Personal & Trabajo (Tokens de API)
    - Google Calendar Personal & Trabajo (OAuth credentials + mcp_config)
    - Gmail Personal & Trabajo (OAuth credentials + mcp_config)
    - Regla global de ALFRED
#>

Param(
    [string]$ClickUpPersonalToken,
    [string]$ClickUpTrabajoToken,
    [string]$GoogleClientId,
    [string]$GoogleClientSecret
)

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " 🎩 DESPLIEGUE Y CONFIGURACIÓN INTEGRAL DE ALFRED & 2BRAIN" -ForegroundColor Yellow
Write-Host "==========================================================" -ForegroundColor Cyan

# Cargar variables desde .env.local o .env si existe en scripts/
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$envLocalPath = Join-Path $scriptDir ".env.local"
if (-not (Test-Path $envLocalPath)) {
    $envLocalPath = Join-Path $scriptDir ".env"
}

if (Test-Path $envLocalPath) {
    Write-Host " -> Leyendo archivo de credenciales locales: $envLocalPath" -ForegroundColor Gray
    Get-Content $envLocalPath | ForEach-Object {
        if ($_ -match '^\s*([^#=]+)\s*=\s*(.*)\s*$') {
            $name = $matches[1].Trim()
            $val = $matches[2].Trim()
            if (-not [string]::IsNullOrEmpty($val) -and -not $val.StartsWith("pk_...")) {
                Set-Variable -Name $name -Value $val -Scope Script
            }
        }
    }
}

# Asignar variables de parámetro o cargadas desde .env.local
if ([string]::IsNullOrEmpty($ClickUpPersonalToken) -and $script:CLICKUP_PERSONAL_TOKEN) {
    $ClickUpPersonalToken = $script:CLICKUP_PERSONAL_TOKEN
}
if ([string]::IsNullOrEmpty($ClickUpTrabajoToken) -and $script:CLICKUP_TRABAJO_TOKEN) {
    $ClickUpTrabajoToken = $script:CLICKUP_TRABAJO_TOKEN
}
if ([string]::IsNullOrEmpty($GoogleClientId) -and $script:GOOGLE_CLIENT_ID) {
    $GoogleClientId = $script:GOOGLE_CLIENT_ID
}
if ([string]::IsNullOrEmpty($GoogleClientSecret) -and $script:GOOGLE_CLIENT_SECRET) {
    $GoogleClientSecret = $script:GOOGLE_CLIENT_SECRET
}

# Solicitud interactiva si falta algún token o credencial
if ([string]::IsNullOrEmpty($ClickUpPersonalToken)) {
    $ClickUpPersonalToken = Read-Host "Ingrese su ClickUp Personal Token (pk_...)"
}
if ([string]::IsNullOrEmpty($ClickUpTrabajoToken)) {
    $ClickUpTrabajoToken = Read-Host "Ingrese su ClickUp Trabajo Token (pk_...)"
}
if ([string]::IsNullOrEmpty($GoogleClientId)) {
    $GoogleClientId = Read-Host "Ingrese su Google Client ID"
}
if ([string]::IsNullOrEmpty($GoogleClientSecret)) {
    $GoogleClientSecret = Read-Host "Ingrese su Google Client Secret"
}

# 1. Comprobar Node.js y Git
Write-Host "`n[1/5] Verificando requisitos del sistema..." -ForegroundColor Green

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Error "Git no está instalado. Por favor instala Git antes de continuar."
    exit 1
}
Write-Host " -> Git: OK" -ForegroundColor Gray

if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Error "Node.js no está instalado. Por favor instala Node.js (v18+) antes de continuar."
    exit 1
}
Write-Host " -> Node.js: OK" -ForegroundColor Gray

# 2. Verificar Antigravity CLI
if (-not (Get-Command agy -ErrorAction SilentlyContinue)) {
    Write-Host " -> Instalando Google Antigravity CLI (@google/antigravity)..." -ForegroundColor Yellow
    npm install -g @google/antigravity
} else {
    Write-Host " -> Antigravity CLI (agy): OK" -ForegroundColor Gray
}

# 3. Configurar Perfil y Regla Global de ALFRED
Write-Host "`n[2/5] Configurando perfil y regla global de ALFRED..." -ForegroundColor Green

$userHome = [System.Environment]::GetFolderPath('UserProfile')
$geminiDir = Join-Path $userHome ".gemini"
$configDir = Join-Path $geminiDir "config"
$rulesDir = Join-Path (Join-Path $geminiDir "antigravity-cli") "rules"

New-Item -ItemType Directory -Force -Path $configDir | Out-Null
New-Item -ItemType Directory -Force -Path $rulesDir | Out-Null

$ruleContent = @"
# Rol del Agente: ALFRED — Mayordomo & Asistente Ejecutivo 2brain

Tu nombre es **ALFRED**. Eres el Mayordomo de Vida y Asistente Ejecutivo Personal del usuario en su sistema **2brain**. Tu fuente de conocimiento principal es el repositorio ubicado en:
`$userHome\Desktop\2brain`

## Estructura de Conocimiento de 2brain (6 Áreas):
1. 🏢 **trabajo**: Analista IT & Soporte en Xetux (`raw/trabajo/`, `wiki/trabajo/`).
2. 💻 **programacion**: Conocimiento Técnico & Lenguajes (`raw/programacion/`, `wiki/programacion/`).
3. 🚀 **proyectos**: Software Independiente & Apps (`raw/proyectos/`, `wiki/proyectos/`).
4. ⛪ **ministerial**: Pastorado, Teología & sermones (`raw/ministerial/`, `wiki/ministerial/`).
5. 🏡 **familiar**: Vida Personal & Bienestar (`raw/familiar/`, `wiki/familiar/`).
6. 💰 **finanzas**: Gestión Económica & Presupuesto (`raw/finanzas/`, `wiki/finanzas/`).

## Principios de Actuación:
- **Gestión Multicuenta**: Distingue entre la cuenta Laboral (Xetux/MasterGroup) y la Personal/Ministerial.
- **Time-blocking**: Respeta y gestiona los bloques de trabajo IT, estudio y tiempo personal.
- **Tono**: Atento, impecable, eficiente, proactivo y siempre listo a la orden, como ALFRED.
"@

Set-Content -Path (Join-Path $rulesDir "user_global.md") -Value $ruleContent -Encoding UTF8
Write-Host " -> Regla global de ALFRED creada." -ForegroundColor Gray

# 4. Crear Carpetas Locales de MCPs y Credenciales OAuth de Google
Write-Host "`n[3/5] Creando carpetas MCP y configurando OAuth de Google..." -ForegroundColor Green

$mcpDirs = @{
    "clickup-personal" = Join-Path $userHome ".clickup-personal-mcp"
    "clickup-trabajo"  = Join-Path $userHome ".clickup-trabajo-mcp"
    "gcal-trabajo"     = Join-Path $userHome ".gcal-trabajo-mcp"
    "gcal-personal"    = Join-Path $userHome ".gcal-personal-mcp"
    "gmail-trabajo"    = Join-Path $userHome ".gmail-trabajo-mcp"
    "gmail-personal"   = Join-Path $userHome ".gmail-personal-mcp"
}

foreach ($key in $mcpDirs.Keys) {
    New-Item -ItemType Directory -Force -Path $mcpDirs[$key] | Out-Null
}

# Guardar tokens de ClickUp
Set-Content -Path (Join-Path $mcpDirs["clickup-personal"] ".env") -Value "CLICKUP_API_TOKEN=$ClickUpPersonalToken" -Encoding UTF8
Set-Content -Path (Join-Path $mcpDirs["clickup-trabajo"] ".env") -Value "CLICKUP_API_TOKEN=$ClickUpTrabajoToken" -Encoding UTF8

# Crear credentials.json para Google Calendar & Gmail (Trabajo y Personal)
$googleCredsTrabajo = @"
{
  "web": {
    "client_id": "$GoogleClientId",
    "client_secret": "$GoogleClientSecret",
    "redirect_uris": [
      "http://localhost:3000/oauth2callback"
    ]
  }
}
"@

$googleCredsPersonal = @"
{
  "web": {
    "client_id": "$GoogleClientId",
    "client_secret": "$GoogleClientSecret",
    "redirect_uris": [
      "http://localhost:3001/oauth2callback"
    ]
  }
}
"@

# Escribir credentials.json en cada directorio de Google si no existe
Set-Content -Path (Join-Path $mcpDirs["gcal-trabajo"] "credentials.json") -Value $googleCredsTrabajo -Encoding UTF8
Set-Content -Path (Join-Path $mcpDirs["gmail-trabajo"] "credentials.json") -Value $googleCredsTrabajo -Encoding UTF8
Set-Content -Path (Join-Path $mcpDirs["gcal-personal"] "credentials.json") -Value $googleCredsPersonal -Encoding UTF8
Set-Content -Path (Join-Path $mcpDirs["gmail-personal"] "credentials.json") -Value $googleCredsPersonal -Encoding UTF8

Write-Host " -> Carpetas y credenciales OAuth de Google & ClickUp listas." -ForegroundColor Gray

# 5. Generar mcp_config.json unificado (6 Servidores MCP)
Write-Host "`n[4/5] Generando mcp_config.json unificado (6 Servidores MCP)..." -ForegroundColor Green

$mcpConfigPath = Join-Path $configDir "mcp_config.json"
$homeEscaped = $userHome.Replace('\','\\')

$mcpJson = @"
{
  "mcpServers": {
    "google-calendar-trabajo": {
      "command": "npx.cmd",
      "args": [
        "-y",
        "mcp-server-google-calendar",
        "run"
      ],
      "env": {
        "NODE_TLS_REJECT_UNAUTHORIZED": "1",
        "GOOGLE_CLIENT_ID": "$GoogleClientId",
        "GOOGLE_CLIENT_SECRET": "$GoogleClientSecret",
        "GOOGLE_REDIRECT_URI": "http://localhost:3000/oauth2callback",
        "GOOGLE_CREDENTIALS_PATH": "$homeEscaped\\.gcal-trabajo-mcp\\credentials.json",
        "GOOGLE_TOKEN_PATH": "$homeEscaped\\.gcal-trabajo-mcp\\token.json"
      }
    },
    "google-calendar-personal": {
      "command": "npx.cmd",
      "args": [
        "-y",
        "mcp-server-google-calendar",
        "run"
      ],
      "env": {
        "NODE_TLS_REJECT_UNAUTHORIZED": "1",
        "GOOGLE_CLIENT_ID": "$GoogleClientId",
        "GOOGLE_CLIENT_SECRET": "$GoogleClientSecret",
        "GOOGLE_REDIRECT_URI": "http://localhost:3001/oauth2callback",
        "GOOGLE_CREDENTIALS_PATH": "$homeEscaped\\.gcal-personal-mcp\\credentials.json",
        "GOOGLE_TOKEN_PATH": "$homeEscaped\\.gcal-personal-mcp\\token.json"
      }
    },
    "gmail-trabajo": {
      "command": "npx.cmd",
      "args": [
        "-y",
        "mcp-server-gmail",
        "--creds-file-path",
        "$homeEscaped\\.gmail-trabajo-mcp\\credentials.json",
        "--token-path",
        "$homeEscaped\\.gmail-trabajo-mcp\\token.json"
      ],
      "env": {
        "NODE_TLS_REJECT_UNAUTHORIZED": "1",
        "GOOGLE_CLIENT_ID": "$GoogleClientId",
        "GOOGLE_CLIENT_SECRET": "$GoogleClientSecret"
      }
    },
    "gmail-personal": {
      "command": "npx.cmd",
      "args": [
        "-y",
        "mcp-server-gmail",
        "--creds-file-path",
        "$homeEscaped\\.gmail-personal-mcp\\credentials.json",
        "--token-path",
        "$homeEscaped\\.gmail-personal-mcp\\token.json"
      ],
      "env": {
        "NODE_TLS_REJECT_UNAUTHORIZED": "1",
        "GOOGLE_CLIENT_ID": "$GoogleClientId",
        "GOOGLE_CLIENT_SECRET": "$GoogleClientSecret"
      }
    },
    "clickup-personal": {
      "command": "npx.cmd",
      "args": [
        "-y",
        "@cavort-it-systems/clickup-mcp"
      ],
      "env": {
        "CLICKUP_API_TOKEN": "$ClickUpPersonalToken"
      }
    },
    "clickup-trabajo": {
      "command": "npx.cmd",
      "args": [
        "-y",
        "@cavort-it-systems/clickup-mcp"
      ],
      "env": {
        "CLICKUP_API_TOKEN": "$ClickUpTrabajoToken"
      }
    }
  }
}
"@

Set-Content -Path $mcpConfigPath -Value $mcpJson -Encoding UTF8
Write-Host " -> mcp_config.json generado exitosamente con 6 MCPs." -ForegroundColor Gray

Write-Host "`n[5/5] Estado de Verificación de Sesiones Google" -ForegroundColor Green
$gcalTrabajoToken = Join-Path $mcpDirs["gcal-trabajo"] "token.json"
$gcalPersonalToken = Join-Path $mcpDirs["gcal-personal"] "token.json"

if (Test-Path $gcalTrabajoToken) {
    Write-Host " -> Google Calendar Trabajo: Sesión Activa" -ForegroundColor Gray
} else {
    Write-Host " -> Google Calendar Trabajo: Requiere autorización OAuth inicial al primer uso." -ForegroundColor Yellow
}

if (Test-Path $gcalPersonalToken) {
    Write-Host " -> Google Calendar Personal: Sesión Activa" -ForegroundColor Gray
} else {
    Write-Host " -> Google Calendar Personal: Requiere autorización OAuth inicial al primer uso." -ForegroundColor Yellow
}

Write-Host "`n==========================================================" -ForegroundColor Cyan
Write-Host " 🎉 ¡ALFRED Y SUS 6 SERVIDORES MCP ESTÁN INTEGRALMENTE CONFIGURADOS!" -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "Para iniciar ALFRED en su terminal o IDE:" -ForegroundColor Yellow
Write-Host "  agy" -ForegroundColor White
Write-Host ""
