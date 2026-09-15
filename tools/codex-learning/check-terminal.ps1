$ErrorActionPreference = 'Stop'
$repoRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '../..')).Path
$evidenceRoot = Join-Path $repoRoot 'docs/codex-learning/evidence'
$labRoot = Join-Path $evidenceRoot ('terminal-lab-' + [guid]::NewGuid().ToString('N'))
$childPath = Join-Path $labRoot 'lesson one'
New-Item -ItemType Directory -Path $childPath | Out-Null
'Terminal practice: this is lesson one.' | Set-Content -LiteralPath (Join-Path $childPath 'note.txt') -Encoding utf8
$results = [System.Collections.Generic.List[string]]::new()
Push-Location -LiteralPath $labRoot
try {
    if ((Get-ChildItem -Name) -notcontains 'lesson one') { throw 'Fixture not found' }
    Set-Location -LiteralPath '.\lesson one'
    $actual = Get-Content -LiteralPath '.\note.txt'
    if ($actual -ne 'Terminal practice: this is lesson one.') { throw 'Readback mismatch' }
    $results.Add('Quoted path containing spaces reads the exact UTF-8 sample')
    Set-Location -LiteralPath '..'
    if ((Get-Location).Path -ne $labRoot) { throw 'Parent navigation mismatch' }
    $results.Add('Parent navigation returns to the practice root without moving files')
    $missingFailed = $false
    try { Set-Location -LiteralPath '.\missing-folder' } catch { $missingFailed = $true }
    if (-not $missingFailed -or (Get-Location).Path -ne $labRoot) { throw 'Failure changed location' }
    $results.Add('Missing destination fails and preserves the working location')
    if (Test-Path -LiteralPath '.\missing-folder') { throw 'Unexpected folder creation' }
    if ((Get-Content -LiteralPath '.\lesson one\note.txt') -ne $actual) { throw 'Unexpected file modification' }
    $results.Add('All navigation operations preserve the original file and do not create the missing folder')
} finally {
    Pop-Location
}
@{ checkedAt = [DateTime]::UtcNow.ToString('o'); environment = "Windows / PowerShell $($PSVersionTable.PSVersion)"; checks = $results; limitations = @('Shell exercise only; no Codex model task or macOS/Linux runtime was tested') } |
    ConvertTo-Json -Depth 4 | Set-Content -LiteralPath (Join-Path $evidenceRoot 'terminal-basics.json') -Encoding utf8
Write-Output "$($results.Count) terminal exercise checks passed; sample retained in the evidence folder"
