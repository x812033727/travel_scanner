$ErrorActionPreference = 'Stop'
$repoRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '../..')).Path
$evidenceRoot = Join-Path $repoRoot 'docs/codex-learning/evidence'
$labRoot = Join-Path $evidenceRoot ('cli-lab-' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $labRoot | Out-Null
$checks = [System.Collections.Generic.List[string]]::new()
$module = Get-Content -Raw -LiteralPath (Join-Path $repoRoot 'docs/codex-learning/deep/modules/35.json') | ConvertFrom-Json
$setup = ($module.blocks | Where-Object { $_.type -eq 'code' -and $_.code.StartsWith('$cliLab =') }).code
if (-not $setup) { throw 'Missing published exercise commands' }
$script = [scriptblock]::Create($setup)
Push-Location -LiteralPath $labRoot
try {
    # Execute the authored PowerShell sample unchanged, not a duplicate test version.
    & $script | Out-Null
    $windowsLab = Join-Path $labRoot 'codex windows lab'
    Set-Location -LiteralPath $windowsLab
    $before = (Get-FileHash -LiteralPath 'note.txt' -Algorithm SHA256).Hash
    if ((Get-Content -LiteralPath 'note.txt') -ne 'WINDOWS-CLI-01') { throw 'Marker mismatch' }
    if ((Get-ChildItem -File).Count -ne 1) { throw 'Unexpected initial files' }
    $checks.Add('Exact authored PowerShell sample creates the expected marker in a path containing spaces')
    $null = Get-Content -LiteralPath 'note.txt'
    if ((Get-FileHash -LiteralPath 'note.txt' -Algorithm SHA256).Hash -ne $before) { throw 'Read changed file' }
    $checks.Add('Independent readback preserves SHA-256 and file count')
    $failed = $false
    try { $null = Get-Content -LiteralPath 'missing-note.txt' } catch { $failed = $true }
    if (-not $failed -or (Test-Path -LiteralPath 'missing-note.txt')) { throw 'Missing-file test failed' }
    $checks.Add('Missing-file read fails without creating a file')
    Set-Location -LiteralPath $labRoot
    $refused = $false
    try { & $script | Out-Null } catch { $refused = $_.Exception.Message -match 'Choose a new practice folder name' }
    if (-not $refused -or (Get-FileHash -LiteralPath (Join-Path $windowsLab 'note.txt')).Hash -ne $before) { throw 'Existing practice data was not preserved' }
    $checks.Add('Rerunning the authored setup refuses an existing folder and preserves prior bytes')

    $greetingLab = Join-Path $labRoot 'codex-cli-lab'
    New-Item -ItemType Directory -Path $greetingLab | Out-Null
    $greetingModule = Get-Content -Raw -LiteralPath (Join-Path $repoRoot 'docs/codex-learning/deep/modules/05.json') | ConvertFrom-Json
    $original = ($greetingModule.blocks | Where-Object { $_.type -eq 'code' -and $_.code.StartsWith('Hello, traveler.') }).code
    $originalPath = Join-Path $greetingLab 'greeting.original.txt'
    $editedPath = Join-Path $greetingLab 'greeting.txt'
    [IO.File]::WriteAllText($originalPath, $original)
    [IO.File]::WriteAllText($editedPath, $original.Replace('Hello, traveler.', 'Hello, Codex learner.'))
    $lines = Get-Content -LiteralPath $editedPath
    if ($lines.Count -ne 2 -or $lines[0] -ne 'Hello, Codex learner.' -or $lines[1] -ne 'Lesson marker: CLI-START-01') { throw 'Reference edit mismatch' }
    if ([IO.File]::ReadAllText($originalPath) -cne $original) { throw 'Backup changed' }
    $checks.Add('Deterministic one-line reference edit preserves marker and independent original')
    [IO.File]::WriteAllText($editedPath, [IO.File]::ReadAllText($originalPath))
    if ((Get-FileHash -LiteralPath $editedPath).Hash -ne (Get-FileHash -LiteralPath $originalPath).Hash) { throw 'Restoration mismatch' }
    $checks.Add('Restoration returns exact original bytes')
} finally {
    Pop-Location
}
$version = (& codex --version | Out-String).Trim()
if ($LASTEXITCODE -ne 0) { throw 'Version lookup failed' }
foreach ($subcommand in @('login', 'resume')) {
    $help = & codex $subcommand --help | Out-String
    if ($LASTEXITCODE -ne 0 -or $help -notmatch "Usage: codex $subcommand") { throw "Help lookup failed: $subcommand" }
}
$checks.Add('Installed Windows CLI version and login/resume help are readable without a model task')
@{
    checkedAt = [DateTime]::UtcNow.ToString('o')
    environment = "Windows / PowerShell $($PSVersionTable.PSVersion) / $version"
    checks = $checks
    limitations = @('No installer, login, model request, sandbox setup, macOS or Linux/WSL runtime was executed', 'The edit is a deterministic reference transformation, not a Codex-generated result')
} | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath (Join-Path $evidenceRoot 'cli-basics.json') -Encoding utf8
Write-Output "$($checks.Count) CLI exercise checks passed; fixtures retained in evidence"
