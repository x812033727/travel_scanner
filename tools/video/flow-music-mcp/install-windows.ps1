<#
.SYNOPSIS
  One-shot Windows setup helper for Mokaair Google Flow Music MCP (`mokaair-flow-music`).

.DESCRIPTION
  Checks Node.js >= 22, Chrome, and FFmpeg on Windows, warns if the checkout
  sits inside OneDrive, optionally writes MCP client configs (`Antigravity`,
  `Claude Desktop`, `Codex`), and runs `npm run flow-music -- doctor`.

.EXAMPLE
  powershell -ExecutionPolicy Bypass -File tools\video\flow-music-mcp\install-windows.ps1 -WriteSetup
#>

param(
  [switch]$WriteSetup
)

$ErrorActionPreference = "Stop"

$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..\..")).Path
Write-Host "[mokaair-flow-music] Repo root: $RepoRoot" -ForegroundColor Cyan

if ($RepoRoot -match "OneDrive") {
  Write-Warning "This checkout is inside OneDrive ($RepoRoot). Move it to a non-synced folder before running Chrome automation."
}

$nodeCmd = Get-Command node -ErrorAction SilentlyContinue
if (-not $nodeCmd) {
  throw "Node.js >= 22 is required. Install from https://nodejs.org/ or run: winget install OpenJS.NodeJS.LTS"
}
$nodeVer = (& node -v).Trim()
$nodeMajor = [int]($nodeVer.TrimStart("v").Split(".")[0])
if ($nodeMajor -lt 22) {
  throw "Node.js $nodeVer detected, but >= 22 is required."
}
Write-Host "[mokaair-flow-music] Node.js $nodeVer OK" -ForegroundColor Green

if (-not (Get-Command ffmpeg -ErrorAction SilentlyContinue)) {
  Write-Warning "ffmpeg not found on PATH. Install with: winget install Gyan.FFmpeg"
} else {
  Write-Host "[mokaair-flow-music] ffmpeg OK" -ForegroundColor Green
}

Push-Location $RepoRoot
try {
  Write-Host "[mokaair-flow-music] Running flow-music doctor..." -ForegroundColor Cyan
  & npm run flow-music -- doctor

  if ($WriteSetup) {
    Write-Host "[mokaair-flow-music] Writing MCP client configs (with .bak backups)..." -ForegroundColor Cyan
    & npm run flow-music -- setup --write
  } else {
    Write-Host "[mokaair-flow-music] Previewing MCP client configs (re-run with -WriteSetup to write automatically)..." -ForegroundColor Cyan
    & npm run flow-music -- setup
  }

  Write-Host ""
  Write-Host "[mokaair-flow-music] Next step — sign into www.flowmusic.app manually in isolated Chrome (0 passwords touched):" -ForegroundColor Green
  Write-Host "  npm run flow-music -- login" -ForegroundColor White
  Write-Host "  npm run flow-music -- status" -ForegroundColor White
} finally {
  Pop-Location
}
