# 從新開 PowerShell 的 73 資料夾逐行執行；同名目錄已存在時先停下核對。
New-Item -ItemType Directory -Path './isolated-user' -ErrorAction Stop
$env:GEMINI_CLI_HOME = (Resolve-Path -LiteralPath './isolated-user').Path
Write-Output $env:GEMINI_CLI_HOME
# 完成教學後關閉這個視窗，不將測試位置設成永久環境變數。
