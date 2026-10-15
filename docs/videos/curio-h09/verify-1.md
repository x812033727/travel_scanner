# H09 獨立逐句史料查核與正式劇本回讀

- 查核日期：2026-10-15（台灣時間）；查核者與 F03／Z01、B06 改稿者分開。
- **有效稿件**：正式旁白 docs/videos/curio-h09/script.md SHA-256 E9404ADD9954E66AA6C26FC3725D7C0ABD09D91B9E571ED2631C152E4579633C；編輯底稿 script-draft.md SHA-256 011C1AC587BF2C2801F82DA224994F4A790FE248A3F7CF4386FF1E5D27264314；主張表 claims.md SHA-256 AED33CE89AA8598E3577664750FB8DE128581E06A1C87C6413C39CA850CC6C48。
- **結果：史料與主張界線 PASS，僅限上述文字及查得的 2026-10-14 官方考察進度。** 新版 B06 的「戰艦 Colorado」有美國海軍原始機構資料支持；其餘 99 段正式旁白相對於前次 D63D46A3… 查核稿未改字。此收據不證明新旁白音訊、插畫、成片、後台核准或上架狀態；考察仍在進行，錄音與發布前須再查新公告。
- 方法：逐句回讀 95 行編輯底稿、100 段正式旁白與 H09-C01–C17。前輪已核對 F03、Z01 相對更早底稿的改字；本輪把現稿與已查核的 D63D46A3… 正式稿逐句比對，只有第 26 段／底稿 B06 的「巡洋艦」改為「戰艦」，其餘 99 段正式旁白文字相同。現稿 95 行去掉編輯標記後依序連接，與 video.json 的 100 段台詞及正式 script.md 的 100 段旁白依序連接，文字完全相同。段落切分本身不增加事實主張。

## 前次送審後正式稿雜湊回綁

送審前本收據記錄的正式稿 SHA-256 是 F2890AA3BE81026F846B9F76F9BA59A1C8B69FEBF7D3D7A7BFB8C0EF6DECC0A1；送審指令重產 `script.md` 後，當時實際送審檔案的 SHA-256 為 D63D46A3E93F7469B9A610CDBD83FB599A1A313D9AAA0A0233EF02C1951C9F82。舊 F2890… 檔案未保存成可比對的快照，因此無法把位元組差異精確歸因；不能僅因兩份雜湊不同，就推稱旁白文字有改動。

本次重新抽取現行正式稿的 100 句旁白，與現行 `video.json` 的 100 句 `text` 逐句相等（0 處差異）；把底稿 95 行移除 ID 和來源標記後依序連接，與正式稿的旁白正文也相等。現行 `script.md` 位元組與 `tools/video/core/screenplay.mjs` 對現行 `video.json` 的確定性輸出相等，尾碼為 `narrative e35c29ff860aad3d`、`speech 10622d25bb00eca4`；底稿 B06 與主張表 C07 已更正，因此兩份檔案的雜湊也如檔頭更新。本輪再查普渡大學公告，至 2026-10-15 查得最新仍為 10 月 14 日水下調查開始、資料待分析，無 Taraia 物件鑑定結果。本次 PASS 僅回綁上述正式稿的史料文字，不替代新音訊及後續考察的重查。

## B06 更正：Colorado 是戰艦

| 行 ID／正式句 ID | 獨立判斷 | 證據與界線 |
| --- | --- | --- |
| B06／colorado-seaplane | PASS | 現稿「戰艦 Colorado 派水上飛機往東南的島群尋找。」與[美國海軍歷史與遺產司令部的航空搜索史](https://www.history.navy.mil/content/history/museums/nnam/education/articles/from-the-cockpit--stories-of-naval-aviation/naval-aviation-and-the-search-for-amelia-earhart.html)一致：Colorado 為 battleship BB-45，搭載三架 O3U Corsair 觀測水上飛機，7 月 7 日開始空中搜索。美國海軍[艦史](https://www.history.navy.mil/research/histories/ship-histories/danfs/c/colorado-iii.html)也將其列為 BB-45，記載該艦及艦載航空隊參與未成功的尋人行動；[美國海軍照片說明](https://www.history.navy.mil/our-collections/photography/us-navy-ships/battleships/colorado-bb-45/NH-55275.html)辨認艦上飛機為 O3U-3 Corsair。原稿的「巡洋艦」不符艦種，已在 B06、正式稿及 H09-C07 更正。這些來源支持艦種、機型與搜索行動，沒有證明飛機在哪裡失事。 |

## 本版兩句新文字

| 行 ID／正式句 ID | 獨立判斷 | 證據與界線 |
| --- | --- | --- |
| F03／h0op7m6k | PASS | 「潟湖那處異常裡，有沒有能辨認為艾爾哈特那架 Electra 的部件？」明確是要由現場回答的問題，沒有暗示已有部件。H09-C14、C16 與 [ALI 的 Taraia 研究及作業計畫](https://www.archaeologychannel.org/taraia/) 都把影像列為尚待直接辨認的物件；[普渡 10 月 14 日公告](https://www.purdue.edu/newsroom/2026/Q4/earhart-expedition-update-underwater-survey-of-taraia-object-begins/)只證明調查開始、資料待分析。 |
| Z01／h0ctdw9q | PASS，依日期限定 | 「截至十月十四日，仍沒有能確認屬於那架 Electra 的殘骸。艾爾哈特最後飛向哪裡，仍無法定案。」H09-C05 為前句最直接的主張界線；H09-C04、C06 支持無法定案的兩種位置推論，H09-C16 與普渡 10 月 14 日公告支持最新目標尚未鑑定。這是截至當日已查來源的結論，不能讀成日後也不會找到。底稿 Z01 行內來源標籤目前列 C04、C06、C16，少列最直接的 C05；查核已核對 C05，建議下次修訂編輯標記時補上並重綁稿件雜湊。 |

## 沿用正文的逐段事實界線

| 範圍 | 本次回讀 |
| --- | --- |
| O01–A11 | [NARA 最後通訊紀錄](https://www.archives.gov/college-park/highlights/earhart-log)支持約 8:43 的 157／337 訊息；7:42 的燃油訊息另在前。稿中沒有把位置線當成確定座標或已證實航跡。「未建立完整雙向通聯」沒有抹掉她曾聲稱聽到船方訊號的細節。 |
| B01–B18 | 搜救約 16 天、超過 25 萬平方英里；Colorado 是 BB-45 戰艦，其三架 O3U Corsair 觀測水上飛機參與搜索；海軍近豪蘭落水是當時的推斷，不是找到飛機的結果。加德納島正式報告與 TIGHAR 抄錄的飛行員信分開；事後訊號始終稱「疑似」。[1937 年搜索報告原件](https://www.archives.gov/files3/research/ameliaearhart/releases/2025/1217/080_PC31-22_146_08_Report_of_Earhart_Search_by_U.S._Navy_and_U.S._Coast_Guard_July_2_18_1937.pdf)的逐頁覆核沿用前輪獨立查核紀錄，本輪沒有重新下載整份 PDF。 |
| C01–D13 | 1940 年骨頭及物件據 TIGHAR 公布的殖民地文件，沒有把骨頭誤寫成文件。Hoodless 的報告是 1941-04-04，判男性、約 45–55 歲，身高估約 5 呎 5 吋半。[Hoodless 文件](https://tighar.org/Projects/Earhart/Archives/Documents/Bones_Chronology5.html)與 [Jantz 2018 論文摘要](https://journals.upress.ufl.edu/fa/article/view/525)分別支持當時判定和後來的量測再分析；2015 年 Cross／Wright 意見僅依後者摘要轉述。99% 是與參考樣本的相似度排序，不是身分概率；現無骨頭可直接驗 DNA。 |
| E01–E13 | ALI 把 Taraia 當待驗假說，[TIGHAR 2021 判讀](https://tighar.org/Publications/TTracks/2021Vol_37/TIGHARTracks37_02_June_2021.pdf)提出木頭或漂木的異議。2024 年豪蘭附近深海影像落空與 2026 年尼庫馬羅羅潟湖目標是兩處不同物件；稿中未移植岩石結論，也沒把影像輪廓當作殘骸鑑定。 |
| F01–F15 | [普渡 10 月 12 日抵達公告](https://www.purdue.edu/newsroom/2026/Q4/earhart-expedition-update-crew-arrives-at-nikumaroro-launches-critical-phase-of-amelia-earhart-plane-search/)與 [10 月 13 日上岸公告](https://www.purdue.edu/newsroom/2026/Q4/earhart-expedition-update-crew-arrives-onshore-sets-up-operations-on-nikumaroro/)支持抵達、上岸、沙洲踏查及地表物件搜尋；[10 月 14 日公告](https://www.purdue.edu/newsroom/2026/Q4/earhart-expedition-update-underwater-survey-of-taraia-object-begins/)與照片說明支持 F06–F07：無人機已查看目標，磁力儀及側掃聲納已開始調查，資料仍待分析。F08–F10 把水力探針與清淤留在後續；F09 是依 ALI 作業順序的連接推論，並非已量得的結果。F11–F14 保留金屬、形狀、鉚釘及木頭的鑑別條件；稿中沒有聲稱已挖出、驗明或運回 Electra。 |
| Z01–Z03 | Z01 以目前未找到可確認機身及去向未定收束；Z02–Z03 只是留言與訂閱邀請，不另加史實。 |

## 查核範圍與下一關

前輪重新開啟 NARA 通訊頁、Jantz 摘要、ALI 作業計畫、普渡 10 月 12–14 日公告，並對照原有 TIGHAR、NARA 搜索報告查核紀錄。本輪新增核對美國海軍歷史與遺產司令部的航空搜索史、BB-45 艦史及 O3U-3 照片說明；官方頁面擷取曾回傳 502，文字由該機構頁面的搜尋索引取得，故以多個同機構來源互證。普渡 10 月 14 日公告明說目前太早下結論；[普渡研究基金會考察公告列表](https://amelia.prf.org/)本輪查得最新仍為 10 月 14 日。這只能界定本次文字查核的資料時點，不能替後來的現場結果背書。

此 PASS 只處理可核對的旁白事實。本輪 B06 由「巡洋艦」改成「戰艦」，前一版音訊及音訊 QA 不能證明新朗讀；須依新稿重錄並核音訊、時長及同步。後台劇本核准綁雜湊，前次 D63D46A3… 的核准不涵蓋 E9404ADD…；正式成片與上架前另須重查 Purdue／ALI 的最新公告，若有新發現，須改稿、重新查核並重新送審。
