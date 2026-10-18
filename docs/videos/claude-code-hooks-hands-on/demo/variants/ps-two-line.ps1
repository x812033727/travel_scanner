# Model-free: the PowerShell pipe test written on two lines (a line may end on the pipe).
# Usage, from the project folder:  powershell -NoProfile -File <this file>
Get-Content -Raw fixtures/stop.json |
  node .claude/hooks/gate.mjs 2>$null; $LASTEXITCODE
Get-Content -Raw fixtures/stop-again.json |
  node .claude/hooks/gate.mjs; $LASTEXITCODE
