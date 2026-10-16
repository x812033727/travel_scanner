# A01 round12 來源綁定敘事候選 — HOLD／未審查

這是由 [round11 隔離候選](../A01-round11-candidate/README.md)衍生的本機版本，並依兩輪獨立審查的 P1／P2 意見收斂；第二輪仍判 **HOLD**。`build.mjs` 逐檔驗證 round11 章節雜湊後，加入 **16 個一鏡一句**的旁白與可愛插畫提示詞、改寫 6 句既有旁白、調整 origin 前八鏡順序。候選層已修正 Anita 造箱圖、Sadow 專利示例措辭、Plath 拉桿摩擦導件圖與 1991 年轉職圖；`r12t01` 明列兩份來源。五筆繼承的 `NOT FOUND` 來源缺席理由另有[逐項稽核](../A01-round12-source-integrity-followup-20261016.md)，其中 `n14` 原來指向仍在稿中的 `now-06/tszs`，本候選把這句重新綁為 `PENDING`。歷史 round11 裁決檔不改，`engine-13/w9bj` 仍是 round11 原句。新句與改句均有逐句來源 map。本候選未替換主機 A01、未呼叫模型或媒體供應商，也不是新的審稿收據。第九輪正式整片敘事 panel 的 `chapters_link`、`payoffs`、`one_thread` FAIL 仍在；此輪 **沒有真實 verifier、listener、敘事 panel、TTS、MiniMax 圖像或成片驗收**。

## 六章的故事接力

| 章 | 敘事任務與章尾交接 | 第 12 輪新增的可核實材料 | 300 CPM 靜態估時 |
| --- | --- | --- | ---: |
| hook | Sadow 看到輪板，先問為何箱子仍靠人提；並預告更早家庭自製品、百貨阻力和 1987 車庫。下一章回到最早那只箱子。 | 沿用 round11 | 51.4 秒 |
| origin | 依館方記述順排 Anita 1928 旅前發問→兒子造箱→一家六口出發→丈夫仍提重箱→旅後帶箱講座→館藏，再接更晚專利與 Sadow 樣品；以赴紐約推銷交給下一章。 | 3 新鏡、5 句既有館方旁白改為明示歸屬；出發鏡改為六名匿名家人。 | 122.3 秒 |
| idea | Macy's 起初不買、有人願試、終於上架；銷售與專利時間分清。章尾問旅客要自己走的長路在哪。 | 沿用 round11 | 105.7 秒 |
| engine | 回答旅客在大型航站自搬長路的困難；申請書的普通箱形、兩半箱底的輪組、平地拖帶和台階手提接回使用情境。章尾仍問機組員為何要換拉法。 | Sadow 原始專利 6 新鏡；鉚釘細節與 1974 Samsonite 資料只留研究筆記，不進口播。 | 70.7 秒 |
| turn | 1987 車庫原型→同在 1989 年搬倉庫／申請較晚專利（不指定先後）→精選凹輪、支腳、拉桿機制→1991 年專利核准／離職（不指定先後）；章尾問直立箱能否四輪轉向。 | 刪除重複的安檢、落地卸裝敘述；較晚專利 7 新鏡，原型／專利界線只說一次。 | 157.5 秒 |
| now | 接上 Samsonite 1997／2000 四輪設計，回應開場「能滾還缺什麼」，再以觀眾自己的使用經驗結束。 | 沿用 round11 | 45.7 秒 |

章時間取自 `validation.json` 的同一個 `estimateTimeline(..., 300)`，是帶預設句間停頓的**合成前文字推估**，上表四捨五入。章節銜接是作者設計，尚未由獨立聽眾或真 panel 判定連貫。

## 來源與年代邊界

- [Sadow US3653474A 原始專利](https://patents.google.com/patent/US3653474A/en)：1970 申請、1972 核准。BACKGROUND、SUMMARY、SPECIFIC EXAMPLE 與 claim 1 支持航站自搬、普通箱形、分在蓋與身的輪組、可拆拖帶及原提把。`r12e04` 現在明說是專利示例，不把紙面結構說成已核實的上市實物；鉚釘／內襯細節仍留在來源筆記，這版不講。專利的構造不能推定每只上市箱的實物細節或市場成因；「台階」只是使用情境示意。
- [Winnetka Historical Society 館藏敘述](https://www.winnetkahistory.org/gazette/before-her-time-anita-willets-burnhams-rolling-suitcase/)：館方引 Anita 遊記支持旅前發問、兒子造箱；丈夫反應與旅後隨箱巡講是**館方轉述**，不是已逐頁核對的 1933 原書文字。作者的網頁 `open` 逾時、官方搜尋索引可讀全文；另一名獨立審查者於 2026-10-16 05:23:44–48 UTC 直接取得官方頁 HTTP 200、raw body 123873 bytes、SHA-256 `0219df34bcd52f93ff9346883ad865af9e9a0c65e2efba87079d62dcaefb1fb4`。這是來源可讀證據，**不是對本次改稿的第二輪逐句 PASS**。插畫用匿名家庭示意，不重建真人肖像。
- [Samsonite 2011 官方招股書](https://corporate.samsonite.com/on/demandware.static/-/Sites-InvestorRelations-Library/default/dwa68533ea/PDF/announcements/2011/20110602100852_Samsonite_Final_Prospectus_en.pdf) 印刷頁 72 年表記 1974 Silhouette 系列有該品牌第一款帶輪箱。獨立審查認為原單句破壞故事線，因此這版**不播**，只保留來源筆記，也不推定它與 Sadow 產品的因果。
- [Plath US4995487A 原始專利](https://patents.google.com/patent/US4995487A/en) 資料欄記 1989-08-08 申請、1991-02-26 核准；SUMMARY、DETAILED DESCRIPTION 支持凹輪、支腳與拉桿摩擦固定，其中 FIG. 4 與說明書是偏心導件在套筒上端以摩擦卡住拉桿的依據。[ABC／USA TODAY 2012 報導](https://abcnews.com/Travel/rollaboard-luggage-celebrates-wheelie-big-birthday/story?id=17024603) 以報導日往前 25 年指向 **1987** 年車庫 Rollaboard；`r12t01` 的 [source map](source-map.json) 同時列原始專利與這份報導。[Travelpro 自家年表](https://travelpro.com/blogs/the-travelpro-blog/the-history-of-rolling-luggage) 記 1989 年搬倉庫、1991 年離職。沒有資料可證明同一年的兩件事誰先誰後；後來專利也不能當作 1987 原型的拆解紀錄。
- 逐句 `source_url`、精確段落／圖／權利要求及 `support_type` 在 [source-map.json](source-map.json)。16 句新旁白與 6 句改寫旁白都標 `PENDING_INDEPENDENT_REVIEW`，原舊句與改句也逐一列出。另有五筆 `inherited_claim_reconciliation`，保留舊裁決與註記；四個退休場景仍是歷史 `NOT FOUND`，活著的 `now-06/tszs` 改成 `PENDING`。`source-delta.json` 只擴充候選 source pack 與待核事實，沒有改 round11 歷史檔；所有候選主張還須獨立重新裁決。

## 片長與畫面風險

`validation.json` 記錄 79 scenes／108 lines，其中 78 張是 `cute-mystery` 插畫鏡頭的**文字提示詞**，最後一張為 outro 卡。沒有任何生成圖片、畫素檢查、配音或成片。

| 靜態速率 | 帶工具預設停頓的六章估時 | 對 540–660 秒正文帶的意義 |
| --- | ---: | --- |
| 250 units／分鐘（工具預設） | 647.6 秒，10:47.6 | 在帶內，但接近上限 |
| 300 units／分鐘 | 553.3 秒，9:13.3 | 暫在帶內 |
| 320 units／分鐘 | 525.8 秒，8:45.8 | 低於 540 秒下限 |
| 340 units／分鐘（快語速壓力測試） | 500.3 秒，8:20.3 | 低於下限 |

這些數字**不能證明 540 秒最低線已達成**：320 CPM 的估算已低於下限，實際 TTS 的字速、停頓、剪接及片頭片尾還須另外量測。不能用空白、拉長靜圖或變速去湊片長；若實測低於 540 秒，須由獨立編輯找出仍有來源、觀眾想知道且不重複的新敘事材料，否則維持 HOLD。原規格的 5 秒片頭和 21 秒片尾仍須在實際合成時另核。

離線 `lintVideo` 為 0 error／38 warnings，`cuteStoryVisualProblems` 為 0 error。警告含 14 個逾 10 秒靜圖鏡頭、跨章重複年份與許多面向角色漫劇而非旁白插畫的 craft 提醒。這些警告不能被 0 error 抹掉；新插畫也必須看真圖是否對物件、年代、手部機械關係和轉場。實際敘事聲畫審查仍未做。

第二輪盲評特別要查 `engine` 的 6 鏡機制是否真的都服務「長路如何少提箱」主線；`turn` 的 7 鏡是否把 1989／1991 專利誤當 1987 實物，或因安檢情節已有 `turn-05`～`turn-08` 而仍顯重複；`origin` 重排後是否能自然地從家庭故事走到商店阻力。若聽感顯得拖沓，不能只憑總秒數保留鏡頭。

## 可重建範圍與下一關

在儲存庫根目錄執行：

```powershell
& 'C:\Users\x8120\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe' 'docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/A01-round12-candidate/build.mjs' --check
```

`--check` 只讀所有 round11 base、`additions.mjs` 與 `source-delta.json`，確認新候選的六章、series、逐句來源、估時與 manifest 都可位元組重現；`--write` 只會改本資料夾。`manifest.json` 對六章、source map、validation 作 SHA-256 綁定。

交給未參與寫稿者逐句核來源、六章連續聽感和聲畫關係，對相同 bytes 跑新一輪事實、listener、整片 narrative panel；若任何項失敗即修稿並另版覆審。真實 TTS 長度與首批真圖驗收再決定是否能進入 A01 既有有限額的製作流程。這份候選自身**不授權主機安裝、付費媒體、B18、後五支或 YouTube 上傳**。
