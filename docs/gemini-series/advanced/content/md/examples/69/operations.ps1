# 在解壓後的 69 資料夾，開新的 PowerShell 視窗執行。
$env:GEMINI_CLI_HOME = (Resolve-Path -LiteralPath 'memory-lab/isolated-user').Path
Set-Location -LiteralPath 'memory-lab/project'
git init
gemini --version
gemini
# CLI 內依序輸入 /memory list 與 /memory show；完成後 /quit，關閉此視窗。
