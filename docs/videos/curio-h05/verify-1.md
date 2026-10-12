# H05｜第一輪獨立事實查核

- 查核日期：2026-10-12；reviewer：h03_research，未撰寫本集完整稿。
- **結果：PASS_WITH_NOTES，0 未解事實，0 NOT FOUND；可通過文字事實關卡。** 不是音訊、圖片、成片或播放器核准。
- 正式 `video.json` SHA：`007bd144583905a61774bf0c7e92ac389431018bc955c2a0335cea759f984768`。
- 正式 `claims.md` SHA：`4c1ab06a23eb749d757d56a214f2e2ac02597c84df0bab44cf1c96e900acce76`；核准 A brief SHA：`b384685061f457187f4ba3c189ebc7c99dfa275607853f397c2e8ec5f5df2803`，未改 brief。
- 研究歷史稿現行 SHA：`41d8cfce8bb8f65b8b6023ff61ca72d3895178e979c316c7a3efa65487c5d646`；科學稿 SHA：`c05eb74fb39cbab90b67086b81f8e51ef6afba6e832f37d2b4eda5108953fd6e`。
- 初稿 110 景／134 句已全讀；修正後105景／129句、31個非 shot 場景的全部 data、標題、說明、tags、縮圖及來源欄位已覆核。24項主張全部映射，未知claim、漏列scene、過期scene anchor均為0。

## 實際讀取、HTTP與證據範圍

本輪依 verifier-video prompt 建立逐景、逐句、所有 data 及 metadata 清單後核對。初稿清單保存在外部 `_audit/fact-review-candidate-inventory.json`；初版canonical清單在 `fact-review-initial-canonical-inventory.json`；最終清單在 `fact-review-final-inventory.json`，SHA `3cfe44158f8e7330954a504dbe94283eecf938148aa32ee2d5f72a077e706b21`。清單記載完整文字與每個場景的主張，並非只靠writer的claims表。

- F1案件、F2機票、F3聲明、F4／F5存檔：當日以web工具重開正文，實讀本集所引全部相關段落及圖說。本機editorial User-Agent直連五頁均回403，原始錯誤保留在 `_audit/verify1-sources/access.json`；**沒有把403改填200**。web讀取沒有顯示數字HTTP狀態，故表中照實標記。
- P1論文：web遭cookie轉址；InvokeWebRequest的HTTP200實為Client Challenge，未拿它作證。改用標準curl與指定editorial User-Agent取得HTTP200真正全文，已獨立讀摘要、導言、Methods、Results、Discussion、Conclusions、權利段。原文 `_audit/verify1-sources/nature-curl.html` SHA `4a20f5348076c20070eab179fdcab00c76c601d966b5c807a60b74ae80edf34f`，去HTML註解及script後文字另存 `nature-curl.txt`；沒有重做實驗或重讀其引用的三份河川研究。
- F6 FAA年表：當日web開啟官方PDF，實讀index161的1971-11-24條，確認727及機尾階梯；沒有把讀一條記成整本逐頁審閱。HTTP數字未顯示。
- 讀取區別與當日時間記於 `_audit/verify1-sources/readback.json`；本事實輪0次web search、0 provider calls。FBI各頁同屬一機關；P1是作者研究，不是獨立FBI鑑定。

## 完整主張表

位置列出該主張實際使用的所有場景、line ID；非shot附data，對應清單保留每個欄位的精確文字。一般提問、場景氣氛與修辭不被假記成可實證的新歷史事實。

| # | 已核對的主張／範圍 | 全部使用位置 | URL | HTTP／實讀狀態 | Verdict | Before → after |
|---|---|---|---|---|---|---|
| c01 | 贖金為 20 萬美元，要求四具降落傘；贖金採 20 美元面額。四具是要求／交付數量，未聲稱全帶在身上；未判定面額由誰指定。 | `hook-recovered-money`（`x8wvho`；`data`）<br>`airport-window-day`（`kap3mn`）<br>`demand-question`（`mnfj8v`）<br>`seattle-ground`（`t1tdc6`）<br>`ransom-demand`（`n2fxc1`、`1f482p`；`data`）<br>`sealed-ransom-bag`（`4q0gpx`）<br>`packed-parachute`（`beuc28`） | [F1](https://www.fbi.gov/history/cases-and-criminals/db-cooper-hijacking)、[F5](https://archives.fbi.gov/archives/news/stories/2009/march/in-search-of-d.b.-cooper)、[F6](https://www.faa.gov/sites/faa.gov/files/about/history/chronolog_history/b-chron.pdf) | FBI：直連403；web正文可讀<br>F6：web PDF 可讀，HTTP未顯示 | CONFIRMED | 不變；依正文確認，未擴大原資料的證明範圍。 |
| c02 | 1971-11-24，自稱 Dan Cooper 的男子在波特蘭以現金買西北東方航空 305 班單程票，前往西雅圖。 | `hook-counter-question`（`3yy2me`）<br>`boarding-date`（`9gys05`、`bs4cu1`；`data`）<br>`portland-counter`（`2tsxj3`）<br>`ticket-original`（`3vkmvf`；`data`）<br>`one-way-ticket-envelope`（`ieh79o`）<br>`boarding-aisle`（`qjz1qd`） | [F2](https://www.fbi.gov/history/artifacts/d-b-cooper-plane-ticket)、[F1](https://www.fbi.gov/history/cases-and-criminals/db-cooper-hijacking) | FBI：直連403；web正文可讀 | CONFIRMED | 不變；依正文確認，未擴大原資料的證明範圍。 |
| c03 | 票面用名是 Dan Cooper，D.B. 是後來媒體傳播的稱呼；購票用名不能證明真名，也未指定唯一誤傳者。 | `hook-ticket-wallet`（`dnd961`）<br>`ticket-original`（`3vkmvf`；`data`）<br>`two-names`（`448nhm`、`2lcdgm`；`data`）<br>`name-empty-seat`（`yzbgw1`）<br>`boarding-aisle`（`qjz1qd`）<br>`objects-not-ending`（`7ua38j`）<br>`three-known-facts`（`wuhlhs`、`huejad`、`i9fjlf`；`data`） | [F2](https://www.fbi.gov/history/artifacts/d-b-cooper-plane-ticket)、[F1](https://www.fbi.gov/history/cases-and-criminals/db-cooper-hijacking)、[F5](https://archives.fbi.gov/archives/news/stories/2009/march/in-search-of-d.b.-cooper) | FBI：直連403；web正文可讀 | CONFIRMED | 不變；依正文確認，未擴大原資料的證明範圍。 |
| c04 | 男子用紙條威脅空服員，聲稱公事包內有炸彈。敘事限於威脅與見聞；未確認裝置效力，不描畫內部結構。 | `folded-note`（`6d62mo`）<br>`briefcase-closed`（`85mz96`）<br>`threat-record`（`ba5hy4`；`data`）<br>`briefcase-latches`（`a5w65d`）<br>`cabin-back`（`nqggtb`） | [F2](https://www.fbi.gov/history/artifacts/d-b-cooper-plane-ticket)、[F1](https://www.fbi.gov/history/cases-and-criminals/db-cooper-hijacking) | FBI：直連403；web正文可讀 | CONFIRMED | 不變；依正文確認，未擴大原資料的證明範圍。 |
| c05 | 在西雅圖交付錢與降落傘，36 名乘客獲釋，幾名機組員留下。36 不含機組。 | `cabin-back`（`nqggtb`）<br>`airport-window-day`（`kap3mn`）<br>`demand-question`（`mnfj8v`）<br>`seattle-ground`（`t1tdc6`）<br>`delivery-table`（`iqeru1`）<br>`passenger-count`（`kafx85`；`data`）<br>`vacant-cabin`（`n83otb`）<br>`cabin-front-curtain`（`yagvt5`）<br>`people-and-object`（`uqvxcx`、`owlxfm`；`data`）<br>`flight-sequence`（`8k8waq`、`8rmuh5`、`d8na5v`；`data`） | [F1](https://www.fbi.gov/history/cases-and-criminals/db-cooper-hijacking)、[F2](https://www.fbi.gov/history/artifacts/d-b-cooper-plane-ticket) | FBI：直連403；web正文可讀 | CONFIRMED | 不變；依正文確認，未擴大原資料的證明範圍。 |
| c06 | 飛機再從西雅圖起飛，機組後來安全降落；乘客離機與機組續飛是兩個階段。 | `vacant-cabin`（`n83otb`）<br>`cabin-front-curtain`（`yagvt5`）<br>`people-and-object`（`uqvxcx`、`owlxfm`；`data`）<br>`second-flight-night`（`vtsfnl`）<br>`flight-sequence`（`8k8waq`、`8rmuh5`、`d8na5v`；`data`）<br>`arrival-cabin`（`g2w7ud`） | [F1](https://www.fbi.gov/history/cases-and-criminals/db-cooper-hijacking)、[F2](https://www.fbi.gov/history/artifacts/d-b-cooper-plane-ticket)、[F6](https://www.faa.gov/sites/faa.gov/files/about/history/chronolog_history/b-chron.pdf) | FBI：直連403；web正文可讀<br>F6：web PDF 可讀，HTTP未顯示 | CONFIRMED | 不變；依正文確認，未擴大原資料的證明範圍。 |
| c07 | 晚上八點多，劫機者帶著贖金從飛機離開；FAA 記機尾階梯。往雷諾途中是航程位置，未報精確分鐘或落地點；出口只在地面空機示意。 | `flight-sequence`（`8k8waq`、`8rmuh5`、`d8na5v`；`data`）<br>`tail-stairs-ground`（`l3e2nh`）<br>`night-clouds`（`j01856`）<br>`forest-unknown`（`l0lcr3`） | [F1](https://www.fbi.gov/history/cases-and-criminals/db-cooper-hijacking)、[F2](https://www.fbi.gov/history/artifacts/d-b-cooper-plane-ticket)、[F6](https://www.faa.gov/sites/faa.gov/files/about/history/chronolog_history/b-chron.pdf) | FBI：直連403；web正文可讀<br>F6：web PDF 可讀，HTTP未顯示 | CONFIRMED | 不變；依正文確認，未擴大原資料的證明範圍。 |
| c08 | 領帶留在機上並保存；FBI 說於 2001 年從領帶取得 DNA 樣本。字幕說基因樣本，字卡保留 DNA。 | `arrival-cabin`（`g2w7ud`）<br>`objects-question`（`w6lulu`）<br>`tie-original`（`63ovsa`；`data`）<br>`tie-storage-box`（`hfg20z`）<br>`sample-room`（`yr2w73`）<br>`sample-and-identity`（`2dv25w`、`9cuyiu`；`data`） | [F4](https://archives.fbi.gov/archives/news/stories/2007/december/dbcooper_123107)、[F1](https://www.fbi.gov/history/cases-and-criminals/db-cooper-hijacking) | FBI：直連403；web正文可讀 | CONFIRMED | 不變；依正文確認，未擴大原資料的證明範圍。 |
| c09 | 領帶與案件的關係，不自動證明每個樣本來自劫機者；指認仍須把樣本來源接到特定的人。屬依原資料界定的證據限制，沒有添加混合人數。 | `sample-and-identity`（`2dv25w`、`9cuyiu`；`data`）<br>`comparison-desk`（`q8jffy`）<br>`objects-not-ending`（`7ua38j`） | [F4](https://archives.fbi.gov/archives/news/stories/2007/december/dbcooper_123107)、[F3](https://www.fbi.gov/contact-us/field-offices/seattle/news/press-releases/update-on-investigation-of-1971-hijacking-by-d.b.-cooper) | FBI：直連403；web正文可讀 | CONFIRMED（含推論界線） | 不變；依正文確認，未擴大原資料的證明範圍。 |
| c10 | 到劫機案發五週年時，曾考慮 800 多名人選，大多被排除；不是進入第五年，也不是整段調查的人選總數，未列任何嫌疑人。確定身分仍未公布。 | `empty-name-file`（`kb8zmc`）<br>`portrait-limit`（`5g1qdi`）<br>`investigation-candidates`（`ekhbdm`；`data`）<br>`archive-many-folders`（`a6tel6`）<br>`comparison-desk`（`q8jffy`）<br>`fate-remains-open`（`fn1ooq`） | [F1](https://www.fbi.gov/history/cases-and-criminals/db-cooper-hijacking)、[F3](https://www.fbi.gov/contact-us/field-offices/seattle/news/press-releases/update-on-investigation-of-1971-hijacking-by-d.b.-cooper) | FBI：直連403；web正文可讀 | CHANGED → CONFIRMED | 進入第五年 → 到案發五週年；字卡、`ekhbdm`、c10與研究紀錄已同步。 |
| c11 | 探員 Larry Carr 回顧兩名空服員分別受訪、外貌描述相近；旁白標明卡爾的回顧，不把描述當身分證明。 | `witness-interview-room`（`gh7d6e`）<br>`two-empty-chairs`（`acbm6o`）<br>`interview-notebook`（`pk4lzt`）<br>`portrait-limit`（`5g1qdi`） | [F4](https://archives.fbi.gov/archives/news/stories/2007/december/dbcooper_123107) | FBI：直連403；web正文可讀 | CONFIRMED | 不變；依正文確認，未擴大原資料的證明範圍。 |
| c12 | 1980-02-10，八歲 Brian Ingram 在 Tena Bar 哥倫比亞河岸發現部分贖金；FBI 金額為 5,800 美元，序號與贖金相符。距案發八年多；論文約 6,000 是約數。 | `hook-recovered-money`（`x8wvho`；`data`）<br>`hook-empty-bank`（`hy0n0i`）<br>`hook-money-and-person`（`xcyiet`、`0lw4i4`；`data`）<br>`sealed-ransom-bag`（`4q0gpx`）<br>`river-chapter-bridge`（`wkdz9n`）<br>`discovery-question`（`ni8bje`）<br>`discovery-date`（`1w4j52`、`jkxh5w`；`data`）<br>`boy-bank`（`oz4hby`）<br>`sand-find`（`xaybl7`）<br>`money-serial-match`（`0fqgbq`；`data`）<br>`recovered-amount`（`vw3ni8`；`data`）<br>`three-known-facts`（`wuhlhs`、`huejad`、`i9fjlf`；`data`）<br>`money-known-origin`（`nk8rvm`） | [F5](https://archives.fbi.gov/archives/news/stories/2009/march/in-search-of-d.b.-cooper)、[F1](https://www.fbi.gov/history/cases-and-criminals/db-cooper-hijacking)、[P1](https://www.nature.com/articles/s41598-020-70015-z) | FBI：直連403；web正文可讀<br>P1：curl 200 正文 | CONFIRMED | 不變；依正文確認，未擴大原資料的證明範圍。 |
| c13 | 探員卡爾認為生還可能性低，這是具名判斷，不是已證明的生死結局；真實身分與最終下落未確認。 | `search-empty-land`（`gb1urz`）<br>`survival-question`（`vhxmuj`）<br>`carr-view`（`2znsmj`；`data`）<br>`opinion-evidence-gap`（`xj1qom`）<br>`fate-remains-open`（`fn1ooq`）<br>`escape-story-limit`（`tnppth`）<br>`objects-not-ending`（`7ua38j`）<br>`two-kinds-of-inference`（`xdrjf4`、`ne1s5l`；`data`） | [F4](https://archives.fbi.gov/archives/news/stories/2007/december/dbcooper_123107)、[F5](https://archives.fbi.gov/archives/news/stories/2009/march/in-search-of-d.b.-cooper)、[F1](https://www.fbi.gov/history/cases-and-criminals/db-cooper-hijacking) | FBI：直連403；web正文可讀 | CONFIRMED | 不變；依正文確認，未擴大原資料的證明範圍。 |
| c14 | 發現錢的位置未證明完整搬運路線、其他錢的位置或人的下落。論文記出土地距報稱 Ariel 跳傘區約 30 公里；不是已知落點或漂流長度。 | `hook-empty-bank`（`hy0n0i`）<br>`hook-money-and-person`（`xcyiet`、`0lw4i4`；`data`）<br>`night-clouds`（`j01856`）<br>`forest-unknown`（`l0lcr3`）<br>`discovery-question`（`ni8bje`）<br>`small-return`（`hq1p3t`）<br>`other-money-unknown`（`7bvfhj`）<br>`place-not-route`（`wqfnmw`）<br>`zone-and-bank`（`tgq3r4`、`pi6auh`；`data`）<br>`distance-not-drift`（`2lt8vw`）<br>`route-still-missing`（`jaj1pu`）<br>`route-not-complete`（`q79cb3`） | [F5](https://archives.fbi.gov/archives/news/stories/2009/march/in-search-of-d.b.-cooper)、[P1](https://www.nature.com/articles/s41598-020-70015-z) | FBI：直連403；web正文可讀<br>P1：curl 200 正文 | CONFIRMED（含推論界線） | 不變；依正文確認，未擴大原資料的證明範圍。 |
| c15 | 5,800 ÷ 200,000 × 100 = 2.9%，小於 3%。分子為本次尋回金額，分母為原交付贖金；未按通膨換算。 | `fraction-question`（`i180w7`）<br>`ransom-proportion`（`56rgvu`、`2j1ugk`、`ugards`；`data`）<br>`small-return`（`hq1p3t`）<br>`outro`（`gv8ke2`、`7zoolz`、`dgufsb`；`data`） | [F1](https://www.fbi.gov/history/cases-and-criminals/db-cooper-hijacking)、[F5](https://archives.fbi.gov/archives/news/stories/2009/march/in-search-of-d.b.-cooper) | FBI：直連403；web正文可讀 | CONFIRMED（含推論界線） | 不變；依正文確認，未擴大原資料的證明範圍。 |
| c16 | Kaye、Meltzer 2020 年研究只分析一張原始贖鈔；同張的數個切片不等於多張原鈔，不擴大到全部尋回或全部贖金。 | `hook-microscope`（`3cecc9`）<br>`transport-question`（`h6syro`）<br>`study-year`（`g2gwqe`）<br>`single-bill-sample`（`rhj7vo`）<br>`study-sample-scale`（`ys3em9`、`yal4ge`；`data`） | [P1](https://www.nature.com/articles/s41598-020-70015-z) | P1：curl 200 正文 | CONFIRMED | 不變；依正文確認，未擴大原資料的證明範圍。 |
| c17 | 研究以顯微鏡分析原鈔上的矽藻，與十一月、三月取得河水的現代鈔票比較；不是案發當晚水樣。圖像只作通用實驗室情境，不冒充論文圖或重做實驗。 | `diatom-observation`（`z0pidb`）<br>`diatom-explained`（`na689w`）<br>`seasonal-comparison`（`n8dzt2`）<br>`modern-controls`（`j9782f`） | [P1](https://www.nature.com/articles/s41598-020-70015-z) | P1：curl 200 正文 | CONFIRMED | 不變；依正文確認，未擴大原資料的證明範圍。 |
| c18 | 作者據矽藻類型、季節資料等，推測浸水較符合五月至六月而非十一月。沒有確定年份，也沒有定出抵岸或埋藏日期；不把季節推論說成定論。 | `hook-microscope`（`3cecc9`）<br>`transport-question`（`h6syro`）<br>`seasonal-comparison`（`n8dzt2`）<br>`bloom-season`（`q0zto0`）<br>`season-inference`（`77qz33`、`nbdnk8`；`data`）<br>`season-not-arrival`（`howr48`）<br>`simple-story-changed`（`fmp55y`）<br>`two-kinds-of-inference`（`xdrjf4`、`ne1s5l`；`data`） | [P1](https://www.nature.com/articles/s41598-020-70015-z) | P1：curl 200 正文 | CONFIRMED（含推論界線） | 不變；依正文確認，未擴大原資料的證明範圍。 |
| c19 | 原鈔內側有較大矽藻；作者另以鈔票、沙及富矽藻水觀察滲入，支持先浸水再被沙覆蓋的解釋。這是研究推論，不證明全部實際搬運情境。 | `season-not-arrival`（`howr48`）<br>`layers-sample`（`qmjt32`）<br>`burial-experiment`（`lx8dlw`）<br>`immersion-before-burial`（`n3u83z`；`data`） | [P1](https://www.nature.com/articles/s41598-020-70015-z) | P1：curl 200 正文 | CONFIRMED（含推論界線） | 不變；依正文確認，未擴大原資料的證明範圍。 |
| c20 | 方法仍待後續驗證；微小元素訊號接近 EDS 能力極限，僅作定性輔助。研究質疑當晚直接浸水的簡單版本，沒有解釋錢如何、為何到河岸，也沒確認人。 | `element-analysis-limit`（`pk9syd`、`r53u5v`；`data`）<br>`prototype-method`（`oz8f3n`）<br>`simple-story-changed`（`fmp55y`）<br>`route-still-missing`（`jaj1pu`）<br>`science-chapter-question`（`wdpqbw`）<br>`study-contribution`（`3gdgej`） | [P1](https://www.nature.com/articles/s41598-020-70015-z) | P1：curl 200 正文 | CONFIRMED（含推論界線） | 不變；依正文確認，未擴大原資料的證明範圍。 |
| c21 | FBI 於 2016-07-08 轉移調查資源，07-12 公布不再主動調查；資源轉向其他優先事項。案發至調整約 44 年 7 個月，旁白用將近 45 年。 | `science-chapter-question`（`wdpqbw`）<br>`case-answer-threshold`（`u3c7mf`）<br>`resources-date`（`qu5nef`、`jhjba4`；`data`）<br>`active-investigation`（`1jbwgh`；`data`）<br>`other-priorities`（`dxn6za`）<br>`status-and-answer`（`pmvj5a`、`vz8s8t`；`data`）<br>`research-after-statement`（`6ocrfg`、`0gpub5`；`data`） | [F3](https://www.fbi.gov/contact-us/field-offices/seattle/news/press-releases/update-on-investigation-of-1971-hijacking-by-d.b.-cooper) | FBI：直連403；web正文可讀 | CONFIRMED | 不變；依正文確認，未擴大原資料的證明範圍。 |
| c22 | 2016 聲明仍保留相關證物並接受特定降落傘／贖金實物訊息；資源安排不等於身分或最終下落已確認，也不是全部資訊永久拒收。 | `status-and-answer`（`pmvj5a`、`vz8s8t`；`data`）<br>`retained-evidence`（`xujqrr`）<br>`physical-leads`（`8t7icg`、`docw8e`；`data`）<br>`evidence-reopening-limit`（`02zl9d`）<br>`three-known-facts`（`wuhlhs`、`huejad`、`i9fjlf`；`data`） | [F3](https://www.fbi.gov/contact-us/field-offices/seattle/news/press-releases/update-on-investigation-of-1971-hijacking-by-d.b.-cooper)、[F1](https://www.fbi.gov/history/cases-and-criminals/db-cooper-hijacking) | FBI：直連403；web正文可讀 | CONFIRMED | 不變；依正文確認，未擴大原資料的證明範圍。 |
| c23 | 探員的生還看法、研究者的浸水推論及機關的資源決策，是不同問題；2020 論文發表本身不能證明正式重啟調查。此為證據範圍的整理，不宣稱此後機關完全沒有動作。 | `two-kinds-of-inference`（`xdrjf4`、`ne1s5l`；`data`）<br>`do-not-join-the-gaps`（`ditcoc`）<br>`research-after-statement`（`6ocrfg`、`0gpub5`；`data`） | [F3](https://www.fbi.gov/contact-us/field-offices/seattle/news/press-releases/update-on-investigation-of-1971-hijacking-by-d.b.-cooper)、[F4](https://archives.fbi.gov/archives/news/stories/2007/december/dbcooper_123107)、[P1](https://www.nature.com/articles/s41598-020-70015-z) | FBI：直連403；web正文可讀<br>P1：curl 200 正文 | CONFIRMED（含推論界線） | 不變；依正文確認，未擴大原資料的證明範圍。 |
| c24 | 收束：票據留下購票用名，部分贖金序號相符，但身分、最終下落與完整路線仍缺足夠證據；2.9% 只回答尋回比例。 | `return-question`（`b2xl3y`）<br>`money-known-origin`（`nk8rvm`）<br>`route-not-complete`（`q79cb3`）<br>`study-contribution`（`3gdgej`）<br>`outro`（`gv8ke2`、`7zoolz`、`dgufsb`；`data`） | [F1](https://www.fbi.gov/history/cases-and-criminals/db-cooper-hijacking)、[F2](https://www.fbi.gov/history/artifacts/d-b-cooper-plane-ticket)、[F3](https://www.fbi.gov/contact-us/field-offices/seattle/news/press-releases/update-on-investigation-of-1971-hijacking-by-d.b.-cooper)、[P1](https://www.nature.com/articles/s41598-020-70015-z) | FBI：直連403；web正文可讀<br>P1：curl 200 正文 | CONFIRMED（含推論界線） | 不變；依正文確認，未擴大原資料的證明範圍。 |

## 其他可見文字與非旁白欄位

| 欄位 | 核對結果與範圍 |
|---|---|
| youtube.title／thumbnail.data | 問句未宣稱已破案；縮圖5,800美元與c12一致，標題沒有承諾唯一搬運路線。此標題沿核准brief；文字事實可用，實際縮圖可讀性未測。 |
| youtube.description | 20萬、5,800、八年多、2.9%、2020、單張、五月至六月與未知年份、2016資源轉移逐項一致。情境插圖與原件有區分；繁中CC為製作規格，沒有當作已交付媒體。 |
| youtube.tags／sources | 僅案件／主題名稱，沒有新增嫌疑人或指控；七個source URL與2026-10-12讀取日期一致。P1標題為簡稱，作者與年份正確。 |
| photo.data／assets | 四個photo場景使用三張既有原件，贖金重用一次。1980是尋回事實，不冒稱照片拍攝日或挖掘現場；領帶、票名圖說與FBI正文一致。授權與像素實看沿research-assets的獨立紀錄，本輪未將讀報告冒稱自己看過三張圖片。 |
| 全部74個shot prompts | 已讀英文物件與構圖；屬情境圖，不加入特定嫌疑人、埋錢者、確定落點、危險操作或精確研究裝置。機尾階梯與研究托盤的改動見下；尚未生成，不能判像素正確。 |
| 2.9%實算 | 已回讀 `_audit/recovered-ransom-calculation.json`，5,800÷200,000=0.029；乘100為2.9%，確實小於3%。只比較同幣值原額，沒有通膨換算或外推其他贖金下落。 |

## 本輪修正與範圍

1. **F01／唯一歷史數值時點修正：c10。** 原「進入第五年」會比五週年早一年；FBI F1寫by the five-year anniversary。現字卡 `investigation-candidates.data.title`、`ekhbdm`與c10改成到案發五週年，research-history第11項也已同步。800多人不是被起訴人數，亦非45年調查的總人數。
2. **圖像／機制表述限縮。** `immersion-before-burial`由同時存在的水沙托盤，改原生steps「先浸水／後被沙覆蓋」，source明寫作者推論；`n3u83z`揭露兩步，與P1討論相符，沒有新定量或事故定論。
3. **情境照明與結構。** `arrival-cabin`改艙內燈光、窗外暗，不再以「天亮後」暗示另一天；`tail-stairs-ground`明確三引擎／高尾翼／後腹部階梯位置，是停機空景，不重建開傘或落點。正式像素仍待後續觀看。
4. **口語／reveal，不增事實。** `2lcdgm`直接唸「迪比庫柏」；`season-inference`第一句先對十一月、第二句對作者推測五月至六月及未知年份，沒有把作者推論升格。贖金序號段改既有原件照片，數字與旁白不變。
5. **刪重複，不刪必要限制。** 移除sample-cap、sealed-evidence-envelope、study-boundary、mystery-remains-specific、closing-archive及各自一句；樣本來源未確定、研究不等於身分或完整路線、相關物證保存等仍有明確保留。五個刪除ID未留在claims anchors。

以歷史主張計為1組FACT change；即使把兩組圖像語意限縮也保守計入，仍不超過3組。**不觸發必須第二輪事實查核的門檻**。本輪reviewer沒有改video、claims、brief或任何媒體；修正由作者／主代理執行後回讀。

## 沒有改動的疑點與結論界線

- 1971-11-24至1980-02-10是八年多；P1「九年、約6,000」是概述，稿採精確日期與FBI5,800，不搬入不合日曆的整九年。
- Dan是購票用名；不證明真名，亦不逕自證明是假名。D.B.媒體稱呼有FBI原文支持；沒有編造首位誤傳記者。
- 20美元只說交付面額，不決定誰指定；36只指乘客，4具只指要求數量。未使用票價、飲料、精確飛行速度或尾梯操作。
- 領帶DNA只確認2001年取樣，不確認每個樣本屬誰；Carr低生還判斷有具名來源，不是死亡證明。未引入在世嫌疑人。
- P1單張原鈔、同張切片、現代對照、作者季節推論、夾層矽藻與定性元素能力限制均已核正文。未推成所有錢的年份、到岸／掩埋日期、確定搬運者、身分或生死；未報方法段互相不一致的現代對照鈔票總數。
- 2016是7月8日資源調整、12日公告；仍接受特定傘／贖金實物，沒有寫正式結案、已破解或2024重啟。此為2026-10-12所讀官方頁狀態；沒有宣稱窮盡全部卷宗或機關此後毫無工作。

## 聽眾與機械檢查

- 129句全文覆核：長於40字符0、口說拉丁詞0、旁白括號／URL0、查核過程旁白0、say覆寫0；不需假填say_for。
- 改後季節兩格按句揭露；浸水／覆沙一整句同時揭露兩步，沒有先秀尚未介紹的另一種季節結論。其他29個原生／photo場景的事實文字已逐項比對，實際reveal節奏與像素仍需render驗證。
- 本輪實跑原生純函式 `lintVideo`，0 errors；3 warnings為daylight 46/74、empty 38/74、window 33/74構圖重複，屬視覺多樣性，不是事實未解。依主代理分工未呼叫CLI stage；主代理另已實跑原生lint0 errors。
- 原生估算129句／2403口說單位、約11.516分鐘；是估算，沒有用來證明配音正文或成片長度。音訊、全片聆聽、生成像素、render、播放器CC均非本報告PASS範圍。
- 站主立場2／3／4／6／9與A角度一致；未發現把推論當事實或未做實驗說成親測的意見衝突。

總計24組主張，23組CONFIRMED、1組CHANGED後CONFIRMED；0 unresolved／NOT FOUND。完整129句、31個非shot data及metadata已覆核；最終結論只綁開頭列出的SHA。正式站大綱自動核准沒有代替本次查核。

## 增量回讀：研究字卡揭露順序（2026-10-12）

- 當前 source SHA：`4bc69184d825ff650e40366d03d90f59516ee3da2839576da21a28921129a96f`；claims 仍為 `4c1ab06a23eb749d757d56a214f2e2ac02597c84df0bab44cf1c96e900acce76`。
- 獨立比較完整 before／after JSON：唯一差異是 `research-after-statement.data.left` 與 `data.right` 交換。2020 年研究先隨 `6ocrfg` 出現，2016 年調查資源安排第二格隨 `0gpub5` 比較；所有 line 欄位、ID、文字、reveal、claims 與其他資料完全相同。
- c21／c23 的年份、機關決策與研究者推論界線未變；沒有新增歷史主張，也不暗示 2020 年正式重啟調查。**增量事實回讀 PASS，0 新增必修**；原24項查核仍適用。此處驗證來源資料與語句對拍，不另宣稱新 render 像素或播放器已審。
- 逐值證據：外部 `_audit/research-card-reveal-fix/factual-readback.json`；原檔保留於同目錄 `video-before.json`。字幕預提案 `7ef045ae…` 的129句與11處純換行建議仍相符；正式字幕及時間尚待完成後另核。
