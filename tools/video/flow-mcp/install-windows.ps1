<#
.SYNOPSIS
  One-shot Windows setup helper for Mokaair Google Flow MCP (Route A).

.DESCRIPTION
  Checks Node.js >= 22, Chrome, FFmpeg, uv, and gflow-cli on Windows, warns if
  the checkout sits inside OneDrive, pulls the latest Google Drive video rules
  (`npm run vdrive -- pull-rules explainer`), optionally writes MCP client
  configs (`Claude Desktop`, `Codex`, `Antigravity`), and runs `flow doctor`.

.EXAMPLE
  powershell -ExecutionPolicy Bypass -File tools\video\flow-mcp\install-windows.ps1 -WriteSetup
#>

param(
  [switch]$SkipInstall,
  [switch]$UpgradeGflow,
  [switch]$WriteSetup,
  [switch]$SkipPullRules
)

$ErrorActionPreference = "Stop"

$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..\..")).Path
Write-Host "[mokaair-flow] Repo root: $RepoRoot" -ForegroundColor Cyan

if ($RepoRoot -match "OneDrive") {
  Write-Warning "This checkout is inside OneDrive ($RepoRoot). Move it to a non-synced folder like C:\dev\travel_scanner before running Chrome automation."
}

# 1. Node.js >= 22
$nodeCmd = Get-Command node -ErrorAction SilentlyContinue
if (-not $nodeCmd) {
  throw "Node.js >= 22 is required. Install from https://nodejs.org/ or run: winget install OpenJS.NodeJS.LTS"
}
$nodeVer = (& node -v).Trim()
$nodeMajor = [int]($nodeVer.TrimStart("v").Split(".")[0])
if ($nodeMajor -lt 22) {
  throw "Node.js $nodeVer detected, but >= 22 is required."
}
Write-Host "[mokaair-flow] Node.js $nodeVer OK" -ForegroundColor Green

# 2. uv
$uvCmd = Get-Command uv -ErrorAction SilentlyContinue
if (-not $uvCmd -and -not $SkipInstall) {
  Write-Host "[mokaair-flow] Installing uv..." -ForegroundColor Yellow
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
  $localBin = Join-Path $env:USERPROFILE ".local\bin"
  if ($env:PATH -notlike "*$localBin*") {
    $env:PATH = "$localBin;$env:PATH"
  }
  $uvCmd = Get-Command uv -ErrorAction SilentlyContinue
}
if (-not $uvCmd) {
  Write-Warning "uv not found on PATH yet. Restart PowerShell after installing uv, then run: uv tool install gflow-cli"
} else {
  Write-Host "[mokaair-flow] uv OK: $(& uv --version)" -ForegroundColor Green
  if (-not $SkipInstall) {
    $gflowExe = Join-Path $env:USERPROFILE ".local\bin\gflow.exe"
    if ($UpgradeGflow -and (Test-Path $gflowExe)) {
      Write-Host "[mokaair-flow] Upgrading gflow-cli..." -ForegroundColor Yellow
      & uv tool upgrade gflow-cli
    } elseif (-not (Get-Command gflow -ErrorAction SilentlyContinue) -and -not (Test-Path $gflowExe)) {
      Write-Host "[mokaair-flow] Installing gflow-cli via uv..." -ForegroundColor Yellow
      & uv tool install gflow-cli
    } else {
      Write-Host "[mokaair-flow] gflow-cli already installed (pass -UpgradeGflow to update)." -ForegroundColor Green
    }
  }
}

# 3. FFmpeg check
if (-not (Get-Command ffmpeg -ErrorAction SilentlyContinue)) {
  Write-Warning "ffmpeg not found on PATH. Install with: winget install Gyan.FFmpeg"
} else {
  Write-Host "[mokaair-flow] ffmpeg OK" -ForegroundColor Green
}

# 4. Pull Drive SSOT rules (canon sheets + FLOW-PRODUCTION-RULES.md)
Push-Location $RepoRoot
try {
  if (-not $SkipPullRules) {
    Write-Host "[mokaair-flow] Pulling Google Drive rules & canon character sheets..." -ForegroundColor Cyan
    & npm run vdrive -- pull-rules explainer
  }

  # 5. Run doctor
  Write-Host "[mokaair-flow] Running flow doctor..." -ForegroundColor Cyan
  & npm run flow -- doctor

  # 6. Preview or write MCP client configs
  if ($WriteSetup) {
    Write-Host "[mokaair-flow] Writing MCP client configs (with .bak backups)..." -ForegroundColor Cyan
    & npm run flow -- setup --write
  } else {
    Write-Host "[mokaair-flow] Previewing MCP client configs (re-run with -WriteSetup to write automatically)..." -ForegroundColor Cyan
    & npm run flow -- setup
  }

  Write-Host ""
  Write-Host "[mokaair-flow] Next step — sign into Google Flow manually in Chrome (0 passwords touched):" -ForegroundColor Green
  Write-Host "  npm run flow -- login" -ForegroundColor White
  Write-Host "  npm run flow -- status" -ForegroundColor White
} finally {
  Pop-Location
}
