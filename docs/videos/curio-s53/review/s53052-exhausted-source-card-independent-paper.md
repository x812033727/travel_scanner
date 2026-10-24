# curio-s53 s53052 耗盡後來源卡：獨立紙審

2026-10-22 UTC；不同作者 reviewer policy_duration_incremental_review。**PASS 書面來源卡**。3 actual已耗盡、0 remaining；不清除先前三張原圖FAIL、不允許第四張。未付費、未動media／manifest。

## 來源判斷

重開固定 `/tmp/s53-sf-relief/56217-0.txt` L4968–4984，原文在證明已買／租舊金山市縣另一地塊後寫 `he was permitted at his own expense to move his house.` 卡引 `at his own expense` 逐字相符；副文「獲准『自費』搬屋」保留permitted語意，不把它說成每戶已完成或一律現付。來源名稱明示San Francisco Relief Survey；這是1913報告的制度記述，不假稱1906現場文件。

原旁白「取得所有權後，也要自費在期限前搬離營地。」屬制度安排。另重開L5010–5025慈善機構搬修寡婦／失能工作者家庭的段落：此卡不得解讀為所有實際費用均由住戶本人支付。後續親友、房東墊付及慈善協助口播原樣保留；卡片沒有推翻那些例外。

124 scenes：109 shot、7 big、7 stats、1 outro；排除outro的正文插圖109/123=88.62%，高於70%。最長連續非shot2，未超3。獨立lint為0 errors／3詞頻warnings。

## 精確未變與綁定

- 將當前唯一卡的template/data逆套作者old，完整video SHA回到先前獨立審核的`327f813308dbad48d43be62faa27826358a0d0d7b93f86b082ebaffd359ec975`。因此只有此卡template/data改變：全部126 spoken及其他scene、既有KEEP、look等完全不變。
- 正式script與claims均包含當前全部126句逐字文字；script重產不代表改口播。
- 本次原文檔SHA重新驗算，來源版本與研究固定值一致。

- `video.json` SHA-256：`7385bb7cf84a293ee55fe671709525ee4f478decfd81d6df24f049e8f644ddee`
- `script.md` SHA-256：`eade31ec115c8df6d56d22c48bba628e37ce62b0437a01e4e0fc4dc909e69568`
- `claims.md` SHA-256：`d1b9c9c0c106bbe7588bb7a5c0250d5e010e9fea6b8bc2d0404409dc859cd893`
- `research.md` SHA-256：`2e61530c650852281402476041175154ee69c414daf7431d6aa0db352e7c3d22`
- `review/s53052-exhausted-source-card-author.json` SHA-256：`c305d945bd383af062fc519cf554587c1053518ef3ca63eb1bc8775d462181ca`
- `/tmp/s53-sf-relief/56217-0.txt` SHA-256：`d627ed287d8a93b9c00225ea47dbdc4f97c36089a890192a602b993c3c185b72`
