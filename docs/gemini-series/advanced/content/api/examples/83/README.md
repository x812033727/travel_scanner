# 83 File Search

原創十份v1文件在 specifications，更新版在 revisions。documents.json是本機全文對照，template ledger沒有真實資源。從 examples 根目錄操作，所有--live須有金鑰與費用上限。

```powershell
.venv/Scripts/python.exe 83/file-search-demo/main.py create --live --ledger my-index.json
.venv/Scripts/python.exe 83/file-search-demo/main.py import --live --ledger my-index.json --file 83/specifications/S001-v1.txt --id S001 --version v1
.venv/Scripts/python.exe 83/file-search-demo/main.py poll --live --ledger my-index.json --id S001 --version v1
```

依序替換S002至S010。pending時查原Operation，不重傳；uncertain先核對唯一display_name、Files與store文件。沒有明確ID就停止，不能自行填成功。

```powershell
.venv/Scripts/python.exe 83/file-search-demo/main.py query --live --ledger my-index.json --question 'S003 的容量是多少？請附來源' --output s003-v1.json
.venv/Scripts/python.exe 83/file-search-demo/main.py import --live --ledger my-index.json --file 83/revisions/S003-v2.txt --id S003 --version v2
.venv/Scripts/python.exe 83/file-search-demo/main.py poll --live --ledger my-index.json --id S003 --version v2
.venv/Scripts/python.exe 83/file-search-demo/main.py delete-document --live --ledger my-index.json --id S003 --version v1
.venv/Scripts/python.exe 83/file-search-demo/main.py query --live --ledger my-index.json --question 'S003 的容量是多少？請附來源' --output s003-v2.json
.venv/Scripts/python.exe 83/file-search-demo/main.py cleanup --live --ledger my-index.json
```

v1容量260、v2容量280；新版完成且刪舊版後才能查。真實引文、更新後答案與刪除後查無各自核對。86若沿用此索引，須同步本機documents及golden題庫到相同版本，或另建獨立v1教學索引。cleanup只清本帳本資源。
