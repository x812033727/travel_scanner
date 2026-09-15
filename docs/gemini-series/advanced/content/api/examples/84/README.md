# 84 快取比較

同一份長文件與三個相同問題在cache-lab。CLI的action明確分開API家族：implicit是Interactions，create/query/delete是generateContent。先設定帳號、金鑰與成本上限。

```powershell
.venv/Scripts/python.exe 84/cache-lab/main.py implicit --live --output implicit-observed.json
.venv/Scripts/python.exe 84/cache-lab/main.py create --live --ledger my-cache.json --output cache-created.json
.venv/Scripts/python.exe 84/cache-lab/main.py query --live --ledger my-cache.json --output explicit-1.json
.venv/Scripts/python.exe 84/cache-lab/main.py delete --live --ledger my-cache.json --output cache-deleted.json
```

隱含一次三題，手動query每次一題；手動重跑請換檔名。TTL300秒不是免費時間。到期後查原名稱並保存錯誤；404仍要核對ID與到期時間，其餘錯誤不能稱清理完成。第一輪不保證未命中，usage缺值不補零。usage-log.csv空白not_run，真實用量與保存費/帳單待測。SDK合成4500 cached tokens不能當遠端結果。
