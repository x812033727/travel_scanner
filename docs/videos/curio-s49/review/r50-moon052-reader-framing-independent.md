# S49 R50 moon052 讀者框架獨立適用性覆核

**KEEP／PASS：僅因電燈拒收此景過度嚴格。** 審閱者 `/root/s38_pf021_last_paper`，先讀現稿、claims來源與圖，再作判斷，不沿用root先前拒因。

## 這一景的時間與敘事層次

凍結prompt是無指定年代的 `adult reader` 在reading desk研究報紙內望遠鏡示意；claims同列明記「虛構報導的想像畫面，非真實月面或器材」。口播是「報導說，這架巨鏡到十二月下旬才裝好，在一月第一週開始運作」，是轉述虛構文章，並沒有把桌邊讀者置於1835年，或聲稱畫面就是巨鏡裝配現場。

固定1859重印L625–634（直接L630–633）確有latter part of December／first week of ensuing month and year。R15 source paper明確區分1859重印與1902後出評論，並接受讀者看草圖而非真觀測器材的框架；本集混有明訂1830年代虛構場景及無年代讀者、檔案查閱者。鄰景moon051指定imagined1830s並不自動把下一景的明確reading desk限制在同年。企劃開場有1835紐約讀者，也不能據此把全片所有讀者一概定年。

## 原生圖

已完整檢視 `moon052-1.jpg` 與selected `moon052-1-trim.jpg`。圖為平面可愛卡通讀者拿報紙、旁有桌燈；電燈確實明確，但可作後來讀者查閱舊報導的普通照明，與此景框架沒有時代矛盾。不可把這個結論套用到明確指定1830s現場或1840s工廠的其他景。紙前望遠鏡有示意圖／小模型的視覺歧義，Jev指出未完全平面印在報紙，但此物不是聲稱真有巨鏡的證物，也沒有展示虛構巨鏡正在運作，屬不改史實敘事的小道具安排。Jev9.29PASS，無照片、3D、油畫或可見黑邊漂移。依curio內容相關插畫標準，本景KEEP，不需額外付費重畫或強行補1835年代。

- `moon052-1.jpg` SHA-256：`7836bc6ea588db838b983f7eaa1198983efcd0b24fc3ff8cc278b7cdc107b13a`
- `moon052-1-trim.jpg` SHA-256：`cf10f65b12f17b78f018b96c54498e98a82358465bd51b95baf3650c0b6cb6ee`

## moon053／054 付費與cached盤點

直接逐筆核media/ledger.json，不只看manifest takes：

- moon053：1次upstream failed、cost $0，沒有產生原生檔；另2次ready image，各$0.0035，實際付費原生2張。seed2 JevFAIL，seed3 JevPASS（selected trim），judge共2次。原生可用額度不能說0；尚最多1張實際原生，亦不可把seed3當已畫3張。
- moon054：2次ready image，各$0.0035。seed1已judge FAIL，seed2ready尚未judge，沒有selected PASS；先利用cached第二圖，已用2actual，僅餘1張，不能重新給3次。

- `moon053-2.jpg` SHA-256：`0c6572ad23d650c3ceb4b5b16c932ce15b971cfb2bd1502c3dd819ef9f59e191`
- `moon053-3.jpg` SHA-256：`fbffd749917268d378c5486f70c635a53df1251167bcc03b04ff4e4fc4e7b599`
- `moon053-3-trim.jpg` SHA-256：`3d2d4c32456ddb34ae13a6409fb9e83dbede8b5472079739fd3c6f5fe380a6bb`
- `moon054-1.jpg` SHA-256：`648de1e5b36a5899263db086626214cc7e4ea18dcb1dc760b386d9b39f5a7241`
- `moon054-2.jpg` SHA-256：`9c1fa7645aa57240e6dc9cc54a6b9b67431768ec32c56723bc94f66e24264ff1`

## 凍結創作檔

- `video.json` SHA-256：`454ea00f42ca79ba6a4c9a356c6fef736c361d04cf269371653225075b9d2955`
- `script.md` SHA-256：`82369f762cc64f70e300e2104a16af3b8e99f1e3296dd81a34152e967f0ecb0a`
- `claims.md` SHA-256：`6ddb3b559418fd7538892b7decbdc8c11d231f3c6927da861625f6dc7cbef7fa`

本票只作52圖的框架適用性與53/54帳本盤點，不代替53/54原圖接受驗收。沒有改prompt、media、manifest、ledger、STOP或git，沒有付費。
