# A01 第 12 輪候選全文獨立預審

日期：2026-10-17。範圍是正式機唯讀 `snapshot-104` 的六章工人實稿；第 12 輪只**假設**移除 `turn-08`／`6i8x` 並退休當前主張 `t19`。這不是已寫入的稿、工人敘事 PASS、正式 `script-review.json`，也不是聲畫或成片驗收。我沒有修改正式機或共用檔案。

## 鎖定的證據

| 檔案 | SHA-256 |
| --- | --- |
| `snapshot-104/docs/videos/story-rolling-suitcase-v2/script.md` | `65e7fbe9fa980b4687c835a4a117bb2ce2f36be8009ce85139ee00e4fb42b3c4` |
| `snapshot-104/docs/videos/story-rolling-suitcase-v2/video.json` | `66fa192bc314a787a0ab66ec2a93976b4110138f4184747de7d3bfda2c5a6812` |
| `snapshot-104/docs/videos/story-rolling-suitcase-v2/verify-1.md` | `cad5e5d5bca357b4a427306edc092973809418804f9fcb75c98cc7691fa24314` |
| `snapshot-104/story-rolling-suitcase-v2/review/narrative.json` | `b75694ec2987d21423dff727c509a1a2ff893e7ac25b574d058051e292fd13b9` |
| 凍結編輯參考稿 `scripts/A01.md` | `f91816021ebea28e1957199a5c73ccc588748e988730efc92e0486d09d5215c6` |

上述各值由本機對檔重算，非單靠前次報告。`auto.json` 仍是 `blocked`、`prompt_fixes:narrative`，第 11 輪 `one_line` 與 `no_recap` 為 false，均指向 `6i8x`。候選剪掉該句後，必須以新正式稿雜湊重新查核、聽眾審稿與敘事盲評，不得沿用第 11 輪判語。

## 六章獨立閱讀

| 章 | 讀稿結論 |
| --- | --- |
| 開場 | 從 Sadow 提兩只重箱、工人推著輪板的具體時刻開始。1928 家庭、1970 百貨、1987 車庫按年代順序各留未揭結果；問題與後文回收對得上。225 個漢字／數字，按 250–300 字／分鐘只是約 45–54 秒的稿面估算。 |
| 起源 | 先回 1928 年 Anita 一家的輪子箱，再到 1943／1946 專利，最後回到機場輪板引出的 Sadow 樣品與 1970 年申請。館藏只稱 Anita 的「一只」，沒有把 1928 年當製作年或說 Sadow 是首創。進百貨的問題引到下一章。 |
| 百貨 | 先拒賣，副總裁親試、叫回買手，1970 年 10 月貨架出現，最後才說 Sadow 對顧客反應的回憶。銷售觀察有歸屬，沒有補造數字。章末專利中「那段路」引到航站。 |
| 航站 | 先回答長路，再從普通外形、兩半輪組、可拆拖帶與提把走向橫拖的使用界線；十個場景約 272 漢字，機械細節密集但每場增加新結構，沒有直接把專利當銷量原因。需用實際插畫與旁白確認聽眾能一遍聽懂。 |
| 機師 | Travelpro 對翻倒及腳踝的說法有口頭歸屬；安檢拆裝→車庫鎖車與箱→原型不能拆→日常箱形問題→1987 直立箱，動作連續。刪 `turn-08` 後，`turn-07b` 可直通 `turn-08b`，不遺失必需的行動或伏筆。1989 專利的凹輪／支腳／拉桿明確稱為較晚專利設計，沒有倒推成 1987 原型。 |
| 現在與片尾 | 1997 平衡四輪直立箱、2000 多方向萬向輪接住上一章四輪疑問；樓梯前不能靠輪子減掉重量，保留新界線。片尾回答「買得到、帶得順手」、提一個與個人使用相關的留言題並邀請訂閱，沒有口播下一集。 |

故事主線是「輪子已有，哪些使用與通路障礙還沒解」：1928 自製品→Sadow 原型／零售→航站使用→Plath 直立拉桿→四輪轉向。人與品牌會換，問題未換；文中沒有主張發明者互相師承。就**候選文字**而言，未發現除 `6i8x` 外另一個確定要擋住剪句的敘事重複；機師章專利機構段落仍是聽覺與畫面風險，應在真聲音／插畫小樣檢查。

## 來源核對與界線

- [ABC 對 Sadow 的原始訪問](https://abcnews.com/Travel/suitcase-wheels-turns-40-radical-idea-now-travel/story?id=11779469)支持波多黎各輪板、四個金屬腳輪與繩子、百貨拒賣、Macy's 副總裁試走與 1970 年 10 月展示；「顧客很快接受」僅是 Sadow 回憶，現稿已有歸屬。媒體頁未給銷量，稿也沒有編數字。
- [Winnetka Historical Society 原文](https://www.winnetkahistory.org/gazette/before-her-time-anita-willets-burnhams-rolling-suitcase/)支持 1928 旅前發問、兒子以嬰兒車輪與伸縮木把手製箱、丈夫反應、旅後演講仍帶輪子箱與館藏。頁面館藏圖說標 1927，不能據此斷言製作年；現稿守住這條界線。
- [Sadow 專利 US3653474A](https://patents.google.com/patent/US3653474A/en)支持 1970-02-16 申請、1972-04-04 核准、先前 Kelly 專利引用、航站自行搬運、普通箱形、箱蓋與箱身分裝輪組、可拆拖帶與原提把。現稿稱這些為申請書／專利設計，未當成商品銷售調查。
- [USA TODAY／ABC 對 Plath 的報導](https://abcnews.com/Travel/rollaboard-luggage-celebrates-wheelie-big-birthday/story?id=17024603)支持安檢彈力繩拆裝、車庫把推車鎖在硬殼箱上及安檢員要求拆箱；現稿把具爭議的靈感軼事歸屬給報導／Plath。[Travelpro 沿革](https://travelpro.com/blogs/the-travelpro-blog/the-history-of-rolling-luggage)支持 1987、兩輪直立拉桿、1989 搬倉庫、1991 全職，翻倒／撞腳踝是競爭者描述，不能當普遍實測。
- [Plath 專利 US4995487A](https://patents.google.com/patent/US4995487A/en)支持 1989-08-08 申請、1991-02-26 核准、凹入式兩輪、支腳、傾斜後輪子承重、摩擦固定拉桿；專利出於 1989，不證明 1987 原型已有每項細節。
- [Samsonite 2011 招股書](https://corporate.samsonite.com/on/demandware.static/-/Sites-InvestorRelations-Library/default/dwa68533ea/PDF/announcements/2011/20110602100852_Samsonite_Final_Prospectus_en.pdf)的年表與術語表支持 1997 可推可拉的平衡四輪直立箱、2000 四輪多方向 Spinners。稿不說世界首創或跟 Plath 直接承襲。

這是抽核主要事實與全文每章的歸屬，不取代目前章檔與合併稿的新一輪正式查核。`claims.md` 若因剪句仍保留 active `t19`，即使口播已刪也要按受審交易退休它，讓場景、主張與合併稿一致；舊稽核紀錄保留。

## 片長、配音與奇聞規格

- 現存實稿為 **79 景、108 句、2,255 個漢字與數字、2,735 個可見字元**（只計 `旁白：` 後的文字；英文字母另計可見字元）。刪 `6i8x` 後約 **78 景、107 句、2,226 個漢字與數字**。以每分鐘 250／300 字兩種純文字假設推算，候選正文約 **8:54／7:25**；加既定 5 秒片頭與 21 秒片尾，粗估約 **9:20／7:51**。這個區間橫跨「正文至少 8 分鐘」門檻，**不能判定實際時長達標**。開場粗估 45–54 秒也不是 TTS 證據。凍結參考稿 2,712 字的 9:02 粗估不可套用到較短的工人稿。須量正式台灣口音 `timeline.json`、語音長度及最後 `ffprobe`；不足時只按來源補新事件／解釋並重新審，不能用停頓、重播或片頭片尾湊。
- `series.json` 鎖定 `image_model: image-01`、`look: {"preset":"cute-mystery"}`、`visual_tier: stills`、10 分鐘；`video.json` 78 個 `shot` 加 1 個 `outro`，插畫占正文遠高於 70%，沒有卡片串接與生成 clip 路線；`subtitles.burn_in=false`。這符合品牌故事借用奇聞檔案局的**規格與說故事結構**，但並無實際 MiniMax 插畫可驗畫風。專利零件特寫與安檢場景必須在畫面審核時確認可愛卡通、可讀且不把示意圖冒充歷史證物。
- `video.json` 的單人聲音是 Gemini `Sulafat` 台灣華語中快語速。共用詞典對 `Sadow`、`Macy's`、`Samsonite` 有讀法，`Anita`、`Plath`、`Rollaboard`、`Travelpro` 等為空值；實際發音與頓點尚未試聽，不能宣稱可用。`The Luggage That Glides`、`747` 與兩件專利的年代也需聽 TTS 並核對可關閉繁中 CC 對時。英／日／韓配音不因這份文字預審啟動。
- 現稿沒有可點片尾連結的驗證。5 秒片頭需在濃縮開場後、21 秒片尾需在三句收尾後；要在成片及私密播放器實測，不能從稿面推出已完成。

## 當前阻擋與預審結論

1. 第 11 輪真實敘事結果仍 FAIL；`turn-08`／`6i8x` 與 active `t19` 尚未在正式來源中受控移除、重併及取得新輪次查核、聽眾與敘事結果。
2. 這份全文預審對候選剪法沒有新增確定的史實或敘事阻擋；但**不是正式逐字稿 PASS**。必須拿實際新稿的雜湊再做獨立審稿，才能簽正式收據。
3. 正文是否達 8 分鐘、台灣華語人名讀法、插畫畫風、CC 與片頭片尾連結都缺媒體實測；其中時長有明顯低於下限的可能，需在付費圖像批量前用真實 TTS 定案。

預審判定：**候選剪句方向可繼續；A01 尚未可宣稱審稿完成或開始批量成片。**
