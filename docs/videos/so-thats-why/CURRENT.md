# 原來如此事務所：目前採用規格

2026-11-01，依站主「用奇聞檔案局的新規則來優化、整理並剔除不好的題目、補更好的題目，可參考十萬個為什麼」。

**新選題從 [本次整理與首批順序](refresh-20261101/README.md) 開始，完整規格在 [新版製作規格](refresh-20261101/SPEC.md)。**
三季原始題庫、查核包、五語文案、排程與既有影片是歷史來源；新版以逐題處置決定是否仍適合開新長片，不刪原稿、不沿用舊核准。

這次完成的是編輯規格、題庫取捨與本機查詢入口。共用主機工人的提示詞、後台題庫與已上架影片不會因這份文件自動改變；正式同步見新版交接。

```powershell
node tools/video/so-thats-why/cli.mjs check
node tools/video/so-thats-why/cli.mjs list
node tools/video/so-thats-why/cli.mjs brief S42
```

`brief` 是撰稿起點，會帶出原來源限制、新標題與最新規格；它不是可直接匯入的已審劇本，也不呼叫付費服務。退下長片清單的題目拒絕輸出 brief，須用 `show <id>` 查取捨理由。
