# H05 v2｜獨立事實覆核（第 1 輪）

日期：2026-10-14。原覆核者沒有撰寫 H05 v2 的旁白；對 `bcd345c709606643` 稿先完成 11 題盲式敘事評讀，再閱讀本稿與來源。寫手隨後修正兩處 11 月對照措辭，並依敘事評語窄修乘客、傘與距離句；`3be74c4b985cd1a7` 曾由另一獨立盲評以 11/11 題通過。其後的片尾縮短、刪景、河岸回呼、去重及圖文對位修訂由改句者作增量來源自查；最新敘事版 **`299218902636bb97` 已獲新的獨立 11/11 盲評**，並抽查 FBI 案件史與 Kaye–Meltzer 論文。原 35 組逐項表是第一輪獨立查核，後續抽查不冒稱現行稿的全量逐欄重審。本文件不代替音訊聽審、站主審閱或成片 QA。

## 範圍、版本及來源

- 本次讀回的 `video.json` SHA-256：`d281c7ec9654255a2cd1e8f0d2afe735b0344fad521ecaa2d5bd296dc1037a4f`；`script.md`：`d9a452eb6233248c694330d3431e73152a52b2d34480b2e2882609bf599c1031`；`claims.md`：`f28b073e1836e0d62a455b0ffa92fdfd5c81225b208895db7f4294b91f1a061b`；`brief.md`：`4d83268083771b7ad744e4130c31bb9587f0e2bc5c7a3337adbec91675fbdda7`。目前敘事 hash `299218902636bb97`，93 景、108 句、六章；舊版內容清單與舊 SHA 僅供歷史追溯。
- 原覆核從 96 景抽出 111 句旁白及場景 `data`、縮圖、YouTube 標題／說明／標籤，共 468 個原始字串欄位；逐項清單在外部工作目錄 `_tools/claim-inventory.json`。現行已再刪景與改示意卡，不能把舊清單誤稱為現行逐欄重抽。下表把同一事實在多張卡片／旁白中的重現合併為可追溯主張組，並另列未納入寫手 `c01–c30` 的序號清單主張、發行文案和三張原件照。畫面中的虛構桌面、光線、鏡頭運動只作情境插圖，列為 `OUT OF SCOPE`；不應呈現為原始現場紀錄。
- 2026-10-14 以編輯用 User-Agent 重新取得 FBI 案件史、機票、2007 回顧、2009 回顧、2016 聲明、FBI Vault 序號資料及 Nature 2020 論文，HTTP 皆 200；Nature 站跳轉 `?error=cookies_not_supported`，但完整論文正文可讀。FAA 年表 PDF 在 curl 為 403，但官方 PDF 可由網頁工具直接讀取第 161 頁 1971-11-24 條；其機尾階梯與四具傘說法亦與 FBI 官方頁相合。Commons 兩張原件頁、FBI 案件頁、DOJ 權利政策重新開啟皆 200。

來源代號（下表 URL 欄均為可點擊原網址）：[F1 FBI 案件史](https://www.fbi.gov/history/cases-and-criminals/db-cooper-hijacking)、[F2 FBI 機票](https://www.fbi.gov/history/artifacts/d-b-cooper-plane-ticket)、[F3 FBI 2007](https://archives.fbi.gov/archives/news/stories/2007/december/dbcooper_123107)、[F4 FBI 2009](https://archives.fbi.gov/archives/news/stories/2009/march/in-search-of-d.b.-cooper)、[F5 FBI 2016](https://www.fbi.gov/contact-us/field-offices/seattle/news/press-releases/update-on-investigation-of-1971-hijacking-by-d.b.-cooper)、[F6 FBI Vault 序號](https://vault.fbi.gov/D-B-Cooper%20/D.B.%20Cooper%20Part%2006)、[P1 Kaye–Meltzer 2020](https://www.nature.com/articles/s41598-020-70015-z)、[A1 FAA 年表](https://www.faa.gov/sites/faa.gov/files/about/history/chronolog_history/b-chron.pdf)、[W1 機票原件](https://commons.wikimedia.org/wiki/File:July_2016_D.B._Cooper_Plane_Ticket_(28379315406).jpg)、[W2 贖金原件](https://commons.wikimedia.org/wiki/File:Money_stolen_by_D._B._Cooper.jpg)、[L1 FBI 公有領域標記](https://commons.wikimedia.org/wiki/Template:PD-USGov-FBI)、[L2 DOJ 政策](https://www.justice.gov/legalpolicies)。

補充本輪來源：[F7 FBI Scientists Hunt for D.B. Cooper 影片逐字稿](https://www.fbi.gov/video-repository/newss-scientists-hunt-for-d.b.-cooper/view)，由 Brian Ingram 與 Tom Kaye 直接說明沙地的三捆 20 美元鈔票；2026-10-14 網頁可讀。

## 逐項主張

下表 `where` 中的 `cNN` 是 `video.json` 各景的 `claims[]` 鍵，已同時檢查該組所有 `lines[].text`／`say` 及 `data`。資料欄另標出帶數值或引文的卡片。`—` 表示文稿原樣保留；兩處 `CHANGED` 是寫手接獲本輪回報後所做的唯一事實措辭修正。

| # | 主張 | where（句 ID／scene.data） | URL | HTTP | 判定 | 修改前 → 修改後 |
| --- | --- | --- | --- | --- | --- | --- |
| 01 / c01 | 要求並獲交 20 萬美元、20 美元面額及四具傘；並未稱四具全帶走。 | h5v017–h5v019、h5v023；`ransom-demand.data.stats` | [F1](https://www.fbi.gov/history/cases-and-criminals/db-cooper-hijacking)、[F2](https://www.fbi.gov/history/artifacts/d-b-cooper-plane-ticket)、[A1](https://www.faa.gov/sites/faa.gov/files/about/history/chronolog_history/b-chron.pdf) | 200／200／網頁可讀 | CONFIRMED | — |
| 02 / c02 | 1971-11-24 在波特蘭現金買赴西雅圖單程票，乘 305 班機。 | h5v001–h5v003、h5v038；`ticket-original.data.caption` | [F1](https://www.fbi.gov/history/cases-and-criminals/db-cooper-hijacking)、[F2](https://www.fbi.gov/history/artifacts/d-b-cooper-plane-ticket) | 200 | CONFIRMED | — |
| 03 / c03 | 購票用名 Dan Cooper；D.B. 是其後媒體稱呼，不等於已證實真名。 | h5v003、h5v038–h5v040；`two-names.data` | [F1](https://www.fbi.gov/history/cases-and-criminals/db-cooper-hijacking)、[F2](https://www.fbi.gov/history/artifacts/d-b-cooper-plane-ticket)、[F4](https://archives.fbi.gov/archives/news/stories/2009/march/in-search-of-d.b.-cooper) | 200 | CONFIRMED | — |
| 04 / c04 | 紙條威脅及公事包裡所見電線、紅色物件；未確認炸彈效力。 | h5v005–h5v006、h5v012–h5v013；`threat-record.data.quote` | [F1](https://www.fbi.gov/history/cases-and-criminals/db-cooper-hijacking)、[F2](https://www.fbi.gov/history/artifacts/d-b-cooper-plane-ticket) | 200 | CONFIRMED | — |
| 05 / c05 | 西雅圖交錢與傘後釋放 36 名乘客，幾名機組留機。 | h5v015、h5v022–h5v027；`passenger-count.data.stats`、`people-and-object.data` | [F1](https://www.fbi.gov/history/cases-and-criminals/db-cooper-hijacking)、[F2](https://www.fbi.gov/history/artifacts/d-b-cooper-plane-ticket) | 200 | CONFIRMED | — |
| 06 / c06 | 乘客離機後飛機續航，機組後來安全降落。 | h5v026–h5v030、h5v033；`people-and-object.data` | [F1](https://www.fbi.gov/history/cases-and-criminals/db-cooper-hijacking)、[F2](https://www.fbi.gov/history/artifacts/d-b-cooper-plane-ticket) | 200 | CONFIRMED | — |
| 07 / c07 | 晚上八點多從飛機後方跳離；機尾階梯此前放下，確切落點未確認。 | h5v007、h5v031–h5v033；`open-tail.data.prompt`、`tail-stairs-ground.data.steps` | [F1](https://www.fbi.gov/history/cases-and-criminals/db-cooper-hijacking)、[F2](https://www.fbi.gov/history/artifacts/d-b-cooper-plane-ticket)、[A1](https://www.faa.gov/sites/faa.gov/files/about/history/chronolog_history/b-chron.pdf) | 200／200／網頁可讀 | 編稿增量相符；待獨立重綁 | h5v031 的「從那裡」收窄為 FBI 直接說的「從飛機後方」。 |
| 08 / c08 | 領帶留機；2001 年由領帶取得 DNA 樣本。 | h5v009、h5v067、h5v069；`tie-original.data.caption`、`sample-and-identity.data.left` | [F1](https://www.fbi.gov/history/cases-and-criminals/db-cooper-hijacking)、[F3](https://archives.fbi.gov/archives/news/stories/2007/december/dbcooper_123107) | 200 | CONFIRMED | — |
| 09 / c09 | 領帶及樣本不能單獨證明人的身分，須有可靠對象比對。 | h5v048、h5v066、h5v070–h5v072；`sample-and-identity.data.right` | [F3](https://archives.fbi.gov/archives/news/stories/2007/december/dbcooper_123107)、[F5](https://www.fbi.gov/contact-us/field-offices/seattle/news/press-releases/update-on-investigation-of-1971-hijacking-by-d.b.-cooper) | 200 | CONFIRMED（證據限制） | — |
| 10 / c10 | 案發五週年時已考慮逾 800 人，除約兩打外均排除；無確定指認。 | h5v043、h5v046–h5v048；`investigation-candidates.data.stats` | [F1](https://www.fbi.gov/history/cases-and-criminals/db-cooper-hijacking)、[F5](https://www.fbi.gov/contact-us/field-offices/seattle/news/press-releases/update-on-investigation-of-1971-hijacking-by-d.b.-cooper) | 200 | CONFIRMED | — |
| 11 / c11 | Carr 回顧兩名空服員分開受訪，描述幾乎相同；不當身分證明。 | h5v041–h5v044 | [F3](https://archives.fbi.gov/archives/news/stories/2007/december/dbcooper_123107) | 200 | CONFIRMED | — |
| 12 / c12 | 1980-02-10 八歲 Brian Ingram 在 Tena Bar 發現三捆腐朽的 20 美元鈔票；FBI 精確金額 5,800 美元，序號相符。 | h5v008、h5v052–h5v057；`discovery-date.data.stats`、`recovered-amount.data.stats` | [F1](https://www.fbi.gov/history/cases-and-criminals/db-cooper-hijacking)、[F4](https://archives.fbi.gov/archives/news/stories/2009/march/in-search-of-d.b.-cooper)、[F7](https://www.fbi.gov/video-repository/newss-scientists-hunt-for-d.b.-cooper/view)、[P1](https://www.nature.com/articles/s41598-020-70015-z) | 200／200／200／先前可讀 | 編稿增量相符；待獨立重綁 | h5v052 首句即點名開場男孩並給日期，h5v053 才揭三捆；FBI 影片逐字稿由 Brian 本人及 Kaye 說明三捆。 |
| 13 / c13 | Carr 認為生還可能性很低，屬具名意見；沒有遺體結論。 | h5v049–h5v050、h5v073–h5v074；`carr-view.data.quote` | [F3](https://archives.fbi.gov/archives/news/stories/2007/december/dbcooper_123107)、[F1](https://www.fbi.gov/history/cases-and-criminals/db-cooper-hijacking) | 200 | CONFIRMED（明示意見） | — |
| 14 / c14 | 研究論文記沙洲離「報稱」Ariel 跳傘區約 30 公里；非落地點、漂流距離或完整搬運路線。 | h5v032、h5v061–h5v065；`zone-and-bank.data` | [P1](https://www.nature.com/articles/s41598-020-70015-z)、[F1](https://www.fbi.gov/history/cases-and-criminals/db-cooper-hijacking) | 200 | CONFIRMED | 刪除 h5v108，不影響此數值界線。 |
| 15 / c15 | 5,800／200,000＝2.9%，只算已尋回比例。 | h5v058–h5v060；`ransom-proportion.data.steps` | [F1](https://www.fbi.gov/history/cases-and-criminals/db-cooper-hijacking)、[F4](https://archives.fbi.gov/archives/news/stories/2009/march/in-search-of-d.b.-cooper) | 200 | CONFIRMED（算式複核） | — |
| 16 / c16 | 2020 年論文只分析 Brian Ingram 持有的一張原始贖鈔，同張多切片不等於多鈔。 | h5v084–h5v087；`study-sample-scale.data` | [P1](https://www.nature.com/articles/s41598-020-70015-z) | 200 | CONFIRMED | — |
| 17 / c17 | 原鈔矽藻與 11 月 13 日直接入哥倫比亞河的現代鈔票、3 月 1 日 Tena Bar 河水對照；不是 1971 年水樣。 | h5v010、h5v088–h5v094；`modern-controls.data`、`control-limit.data.prompt` | [P1](https://www.nature.com/articles/s41598-020-70015-z) | 200 | CHANGED | h5v090「冬天的對照鈔票」→「十一月的對照鈔票」；明列實驗月份。 |
| 18 / c18 | 矽藻組合與文獻盛期支持作者的五月至六月浸水推論；不定年份、到岸日。 | h5v093–h5v098、h5v107；`season-inference.data` | [P1](https://www.nature.com/articles/s41598-020-70015-z) | 200 | CHANGED | h5v093「和冬季對照不一樣」→「和那張對照鈔票不一樣」；不把 11 月概稱冬季。 |
| 19 / c19 | 較大矽藻進入紙鈔夾層；乾鈔先埋沙再灌水的對照只在紙邊滲入小藻／碎片，支持先浸水後覆沙的推論。 | h5v098–h5v103；`burial-edge.data.prompt`、`immersion-before-burial.data.steps` | [P1](https://www.nature.com/articles/s41598-020-70015-z) | 200 | CONFIRMED（研究推論） | — |
| 20 / c20 | EDS 微小元素訊號近偵測極限，僅定性；季節推定法仍待驗證，也不定到岸日期。 | h5v104–h5v107、h5v109；`element-analysis-limit.data`、`outro.data` | [P1](https://www.nature.com/articles/s41598-020-70015-z) | 200 | CONFIRMED（限制有保留） | 原 h5v108 的概括收束刪除，片尾首次直接回答日期問題。 |
| 21 / c21 | FBI 於 2016-07-08 轉移資源、07-12 公布；未宣布破案。 | h5v075–h5v077；`resources-date.data.stats`、`status-and-answer.data` | [F5](https://www.fbi.gov/contact-us/field-offices/seattle/news/press-releases/update-on-investigation-of-1971-hijacking-by-d.b.-cooper) | 200 | CONFIRMED | — |
| 22 / c22 | 保存證物；仍接受與贖金或降落傘相關的特定新物證。 | h5v077、h5v080–h5v082；`physical-leads.data.steps` | [F5](https://www.fbi.gov/contact-us/field-offices/seattle/news/press-releases/update-on-investigation-of-1971-hijacking-by-d.b.-cooper) | 200 | CONFIRMED | — |
| 23 / c23 | 2020 私人研究是新問題，不等於 FBI 2016 資源決定被撤回。 | h5v073–h5v074、h5v075–h5v077、h5v084；`carr-view.data`、`resources-date.data`、`study-year.data` | [F5](https://www.fbi.gov/contact-us/field-offices/seattle/news/press-releases/update-on-investigation-of-1971-hijacking-by-d.b.-cooper)、[P1](https://www.nature.com/articles/s41598-020-70015-z) | 200 | CONFIRMED（證據範圍） | — |
| 24 / c24 | 物證可確認部分鈔票序號，卻不足以確定人的去處、搬運者、完整路線或抵岸日；片尾提問及訂閱句無獨立事實。 | h5v107、h5v109–h5v111；`outro.data` | [F1](https://www.fbi.gov/history/cases-and-criminals/db-cooper-hijacking)、[P1](https://www.nature.com/articles/s41598-020-70015-z) | 200／先前可讀 | 編稿增量相符；待獨立重綁 | h5v107 先界定到岸日未知，h5v109「證明贖金，不證明人」回答標題；「證明贖金」專指序號相符，不是金額本身能鑑定鈔票。 |
| 25 / c25 | 空服員另寫紙條給機長；續航命令指向墨西哥城。 | h5v016、h5v029 | [F1](https://www.fbi.gov/history/cases-and-criminals/db-cooper-hijacking) | 200 | CONFIRMED | — |
| 26 / c26 | FBI 飛行中得知消息，代號 NORJAK，訪談數百人、搜機身與各地線索。 | h5v021、h5v034–h5v035、h5v045 | [F1](https://www.fbi.gov/history/cases-and-criminals/db-cooper-hijacking) | 200 | CONFIRMED | — |
| 27 / c27 | 黑領帶屬案中物件，跳機前摘下；畫面未用品牌推身分。 | h5v014、h5v068；`tie-original.data.caption` | [F1](https://www.fbi.gov/history/cases-and-criminals/db-cooper-hijacking) | 200 | CONFIRMED | — |
| 28 / c28 | 起飛前點波本加蘇打。 | h5v004 | [F1](https://www.fbi.gov/history/cases-and-criminals/db-cooper-hijacking) | 200 | CONFIRMED | — |
| 29 / c29 | 四具傘中帶走兩具；餘傘之一的繩用於綁贖金袋。 | h5v036–h5v037；`chutes-carried.data.stats`、`chute-cord.data.prompt` | [F1](https://www.fbi.gov/history/cases-and-criminals/db-cooper-hijacking)、[F3](https://archives.fbi.gov/archives/news/stories/2007/december/dbcooper_123107) | 200 | CONFIRMED | — |
| 30 / c30 | 2016 聲明提到「突然有錢」類逸聞，未達確認身分所需證明。 | h5v078–h5v079 | [F5](https://www.fbi.gov/contact-us/field-offices/seattle/news/press-releases/update-on-investigation-of-1971-hijacking-by-d.b.-cooper) | 200 | CONFIRMED | — |
| 31 | 交付的 10,000 張 20 美元鈔票有完整 FBI 序號清單。 | h5v020（c01/c12）；`money-serial-match.data.caption` | [F6](https://vault.fbi.gov/D-B-Cooper%20/D.B.%20Cooper%20Part%2006)、[F1](https://www.fbi.gov/history/cases-and-criminals/db-cooper-hijacking) | 200 | CONFIRMED | — |
| 32 | 標題、說明、標籤及縮圖僅承諾 5,800 美元可證明的事；說明明列 2.9%、2020 單鈔推論、2016 決定與三原件照，沒有承諾找出帶錢者。 | `youtube.title`／`description`／`tags[]`；`thumbnail.data` | [F1](https://www.fbi.gov/history/cases-and-criminals/db-cooper-hijacking)、[F5](https://www.fbi.gov/contact-us/field-offices/seattle/news/press-releases/update-on-investigation-of-1971-hijacking-by-d.b.-cooper)、[P1](https://www.nature.com/articles/s41598-020-70015-z) | 200 | CONFIRMED（文案符合內文） | 原「誰帶走了它／指向誰」已由寫手在本輪前改成「證明了什麼／證明什麼」。 |
| 33 | 機票原件身分、FBI 署名及公有領域標記；檔案像素與登記 SHA 相符。 | `assets[0]`、`ticket-original.data.image` | [W1](https://commons.wikimedia.org/wiki/File:July_2016_D.B._Cooper_Plane_Ticket_(28379315406).jpg)、[F2](https://www.fbi.gov/history/artifacts/d-b-cooper-plane-ticket)、[L1](https://commons.wikimedia.org/wiki/Template:PD-USGov-FBI) | 200 | CONFIRMED | — |
| 34 | 損毀鈔票原件身分、FBI 署名及公有領域標記；非發現現場照。 | `assets[1]`、`money-serial-match.data.image` | [W2](https://commons.wikimedia.org/wiki/File:Money_stolen_by_D._B._Cooper.jpg)、[F1](https://www.fbi.gov/history/cases-and-criminals/db-cooper-hijacking)、[L1](https://commons.wikimedia.org/wiki/Template:PD-USGov-FBI) | 200 | CONFIRMED | — |
| 35 | 領帶照出自 FBI 案件頁；FBI／DOJ 內容無第三方權利標示，依政策為公有領域；檔案 SHA 相符。 | `assets[2]`、`tie-original.data.image` | [F1](https://www.fbi.gov/history/cases-and-criminals/db-cooper-hijacking)、[L2](https://www.justice.gov/legalpolicies) | 200 | CONFIRMED（個別攝影者未標） | — |
| 36 | 情境插圖的視角、光線、普通桌面、匿名人物與無字道具不主張現場原貌；不可讓觀眾誤認為檔案照。 | 所有 `scenes[].data.prompt`／`camera`／`visual`，含 `open-boy` 的陰天光線與研究場景的概念示意 | 本稿 `youtube.description` 及 [asset-register.md](asset-register.md) 的區分 | 本地文件 | OUT OF SCOPE（視覺製作） | — |

## 最終盲評後的增量覆核

下表只檢查 `f7d68dd1667c6f25` 之後的改動：先有數句旁白與比較卡窄修，後有兩張圖文對位插圖修正；最後的插圖修正沒有再改旁白。FBI 案件史在本輪直接讀到「36 名乘客換取錢及傘、留下幾位機組再起飛」及「四具傘帶走兩具」；Kaye–Meltzer 論文直接記沙洲距**報稱**跳傘區約 30 公里。

| # | 最終主張／位置 | URL | HTTP | 判定 | 增量結論 |
| --- | --- | --- | --- | --- | --- |
| Δ1 | h5v024–h5v028；`delivery-table.data.prompt`、`passenger-count.data.stats`、`people-and-object.data`、`vacant-cabin.data.prompt` | [F1](https://www.fbi.gov/history/cases-and-criminals/db-cooper-hijacking)、[F2](https://www.fbi.gov/history/artifacts/d-b-cooper-plane-ticket) | 200 | CONFIRMED | 錢與傘上機後 36 名乘客獲准下機，劫機者與幾位機組員留下，班機再起飛；概念圖現畫機艙內錢袋與敞開的乘客艙門，與「從這扇門」相接。並未宣稱實際袋子在機艙的精確座位。 |
| Δ2 | h5v036；`chutes-carried.data.stats` | [F1](https://www.fbi.gov/history/cases-and-criminals/db-cooper-hijacking)、[F3](https://archives.fbi.gov/archives/news/stories/2007/december/dbcooper_123107) | 200 | CONFIRMED | 「只帶走其中兩具」符合官方圖說；現行改用 4／2 原生數字卡，無虛構傘包外形或位置。 |
| Δ3 | h5v063–h5v064；`zone-and-bank.data`、c14 | [P1](https://www.nature.com/articles/s41598-020-70015-z) | 200 | CONFIRMED | 「兩地相隔約三十公里」由前句「報稱跳傘區」與字卡兩地標籤界定；不是實際落地點或漂流里程。 |
| Δ4 | `youtube.title`／`description`／`tags[]`、`thumbnail.data`、c05／c06／c14／c29 | [F1](https://www.fbi.gov/history/cases-and-criminals/db-cooper-hijacking)、[F5](https://www.fbi.gov/contact-us/field-offices/seattle/news/press-releases/update-on-investigation-of-1971-hijacking-by-d.b.-cooper)、[P1](https://www.nature.com/articles/s41598-020-70015-z) | 200 | CONFIRMED | 標題、說明、縮圖仍問 5,800 美元「證明了什麼」，未承諾辨認帶錢者；c05／c06／c14／c29 的來源與新句相符。 |

## 結論與交接

- **事實主張組：35**；原獨立覆核為 33 `CONFIRMED`、2 `CHANGED`、0 `NOT FOUND`。兩處事實修改只把 11 月對照樣本說準，沒有改數值、人物或因果結論；前次增量四組均 `CONFIRMED`。`3be74c4b985cd1a7` 曾獨立通過 11/11，`4b50c92d23951614` 為 10/11；目前 `299218902636bb97` 的外部 `review/narrative.json` 已記錄新的獨立 **11/11 PASS**。FBI 案件史及 Kaye–Meltzer 原論文作了增量來源抽查，畫面成圖後仍須檢查是否忠於來源。
- **會隨時間變動的說法：** FBI 2016 聲明的資源安排與物證提交邀請，本文均明說是該聲明的內容；FBI 現行案件史與機票頁在 2026-10-14 可讀，仍未指認身分。2020 論文發表後是否有其他研究，不是本稿主張。`video.json.sources[].checked_on` 保留寫手原 2026-10-12 檢查日，本輪讀回日期見本報；FAA PDF 的 curl 403 不冒充 HTTP 200。
- **觀點：** Carr 的生還判斷與 Kaye–Meltzer 的浸水順序／季節推論均具名且有保留；與 `brief.md` 的站主觀點沒有矛盾。旁白沒有把猜測或 2016 資源決定寫成破案。
- **聽稿：** 現行 108 句中無超過 40 字、Latin 字母、括號、URL 或「經查證／本影片」式查核語句；無 `say` 覆寫。已檢查 reveal 在相應字卡句出現時才開，不提前揭曉研究結論。三句片尾共用一張卡，靜態估 7.5 秒；仍需在實際聲音時間軸與成片播放檢查。
- **機械檢查：** `node tools/video/cli.mjs lint --slug curio-h05-v2 --json`：0 errors、0 warnings；現稿靜態估 8.681 分，實際 TTS 時長見文末最新狀態。`renderProblems(video.json, root, {workdir})` 和 `cadenceProblems` 為 `[]`；最長畫面 7.5 秒、65 張插圖覆蓋約 62.9%。三張工作目錄 JPEG 與 `assets[]` 及 `asset-register.md` 的原覆核一致；原件照片卡的全圖、裁切與 credit 仍待正式預覽／成片抽格。
- **曾懷疑而未改：** 論文摘要把尋回金額寫約 6,000 美元，本片用 FBI 的精確 5,800；論文的約 30 公里指沙洲到**報稱**跳傘區，沒有被寫成漂流距離；FAA 官方 PDF 的直接 curl 遭 403，但可直接讀官方頁面內容。場景插圖的天氣／實驗桌外觀沒有現場影像證據，因此只能維持清楚的示意標示。

## 上一輪三句片尾縮短的增量核對（2026-10-14，歷史紀錄）

原 `h5v109`–`h5v111` 依序縮為「鈔票對上，去處未知。」「哪件物證最意外？」「訂閱，繼續查證。」；line ID、場景、字卡、`claims[]` 和三句預設停頓均未變。第一句前半只指已尋回鈔票的序號對上贖金，[FBI 案件史](https://www.fbi.gov/history/cases-and-criminals/db-cooper-hijacking)直接支持；後半承接前句未定到岸日與搬運者，並保留 FBI 所述劫機者最後去向未知，不把單鈔研究擴張成人的身分或完整路線結論。後兩句為觀眾提問及訂閱邀請，不新增史實。

該輪 `narrative --slug curio-h05-v2` 讀到舊雜湊 `a0ba45ab2d064527`。改句者使用原始旁白做 11 題**非盲增量自檢**，11 題均答是，答案在外部 `review/narrative-outro-selfcheck.json`，verdict 在外部 `_tools/outro-selfcheck/curio-h05-v2/review/narrative.json`；這些不覆蓋舊版獨立盲評檔，也不算現行稿的獨立敘事核准。

## 六章收束修稿的增量核對（2026-10-14，歷史稿）

刪去 `route-still-missing` 唯一一句 `[h5v108]` 後，`[h5v107]`「有了季節和先後，能把到岸日定到某一天嗎？」直接接片尾 `[h5v109]`「到岸日，仍是空白。」`video.json.loops` 的 payoff 因而從已刪 `[h5v108]` 轉到 `[h5v109]`；企劃收為六章。新片尾首次直接回答確切抵岸日不可從單鈔研究算出，符合 [Kaye–Meltzer 原論文](https://www.nature.com/articles/s41598-020-70015-z)只推論浸水季節及先後次序的界線；未新增年份、搬運者或落點結論。`outro.claims[]` 改為 `c20/c24`，`c15` 仍留在百分比場景。

`script --slug curio-h05-v2` 在該輪重生為 95 景、110 句、六章、敘事 hash `4b50c92d23951614`。當輪靜態估時 **528.600 秒**，片尾 **7.267 秒**；`lint` 0/0、`cadenceProblems=[]`、`renderProblems=[]`，插圖占比 **68.0%**。後來獨立盲評對此 hash 為 10/11，指出開場河岸男孩在 `[h5v052]` 未點名重述；本節數值不是現行稿的關卡結論。

## 河岸回呼、領帶橋接與片尾答案的增量核對（2026-10-14，歷史稿）

改稿者重讀 [FBI 案件史](https://www.fbi.gov/history/cases-and-criminals/db-cooper-hijacking)及[FBI 對 Ingram、Kaye 的影片逐字稿](https://www.fbi.gov/video-repository/newss-scientists-hunt-for-d.b.-cooper/view)。前者只直接說從飛機後方跳出，故 `[h5v031]` 不再把跳離位置說死在階梯上；後者由發現者及研究者描述沙地上的三捆 20 美元鈔票。`[h5v052]` 直接回呼開場男孩，給 1980-02-10；`[h5v053]` 才新增三捆和面額，`[h5v054]` 只補姓名與八歲，避免連續兩次回呼。`[h5v066]` 從河岸物證轉去機上領帶，隔約 85 秒後 `[h5v083]` 才點名河岸鈔票，帶出不同的研究問題。

`[h5v107]` 先以單鈔研究不能定抵岸日為界，轉問片名的 5,800 美元；`[h5v109]` 首次直答「證明贖金，不證明人」。這是序號對上部分贖金與仍無法指認劫機者的合併判斷，不指金額本身有鑑定力，也未稱研究已找出搬運路線。`open-aisle` 現呈匿名持票入座者，`open-tie` 呈領帶旁的示意取樣場景；均無可讀假票據或宣稱精確採樣手法。三捆新字卡只在 `[h5v053]` 對應的發現景出現。

當輪旁白 hash `29e5faca8dd64a64`，靜態估 **531.267 秒**，95 景、110 句、六章；片尾 **7.5 秒**、最長畫面 **7.5 秒**、插圖占比約 **67.7%**。`lint` 0 errors／0 warnings、`cadenceProblems=[]`、`renderProblems=[]`。本節只是該輪修稿者的來源增量自查，**不是現行稿的獨立事實簽核或敘事盲評**。

## 第三輪盲評後去重與畫面對位（2026-10-14，歷史稿）

第三輪獨立盲評對舊 `29e5faca8dd64a64` 為 8/11；本段只記改稿者的來源增量判斷。依 [FBI 案件史](https://www.fbi.gov/history/cases-and-criminals/db-cooper-hijacking)、[FBI 2007 回顧](https://archives.fbi.gov/archives/news/stories/2007/december/dbcooper_123107)和 [Kaye、Meltzer（2020）](https://www.nature.com/articles/s41598-020-70015-z)既有讀回，逐項確認：

| 位置 | 現行改動 | 來源界線 |
| --- | --- | --- |
| `[h5v051]`、`[h5v083]` | 刪去兩句只報過場的景，前句直接切到男孩發現／2020 年研究。 | 日期、三捆鈔票、FBI 2016 決定及 2020 年研究本身仍由原句承載；沒有把研究寫成 FBI 重新開案。 |
| `[h5v072]`、`loops[]` | 領帶問句明確落在「樣本仍沒在公開檔案裡帶出真名」；兩條領帶 loop 改綁此句。 | FBI 記有樣本，但公開資料沒有據此識別劫機者；不指樣本必屬他，也不斷言日後不可能識別。 |
| `[h5v038]`、`[h5v058]`、`[h5v085]` | 去掉短距離或多餘「還記得」，保留購票用名、金額算式與原鈔持有人。 | 史實和算式未改；全片保留五次遠距離點名回呼。 |
| `open-question`、`transport-question`、`tie-storage-box`、`single-bill-sample`、`diatom-observation` | 紙條與領帶用概念插圖；原鈔只畫空白磨損邊緣；顯微觀察改為來源標示的原生文字卡。 | 不生成紙條原文、真實序號、偽造顯微照或個人身分。 |
| `tail-stairs-ground`、`modern-controls`、`burial-experiment` | 改為原生步驟／文字卡，分別標示機尾跳離且落點未知、現代對照非原鈔、埋沙灌水為對照實驗。 | FBI 只直接記從飛機後方跳出；Kaye、Meltzer 原研究僅支持其對照條件與推論，不是歷史現場影像。 |

該輪敘事 hash **`67f7da561ba1deaa`**，**93 景、108 句、六章**；靜態 **516.3 秒（8.605 分）**，片尾 **7.5 秒**、最長畫面 **7.5 秒**、插圖占比 **65.0%**。`lint` **0 errors／0 warnings**；`cadenceProblems=[]`、`renderProblems=[]`。這是歷史修稿的增量來源核對，**不是**後續敘事 hash 的獨立盲評或原覆核者重簽。

## 河岸與原鈔章的接續修訂（2026-10-14，現行編稿增量）

前一輪 `67f7da561ba1deaa` 的獨立盲評指出 `[h5v052]` 和 `[h5v084]` 仍像突然換章。這次把 `[h5v050]` 留成「那筆贖金呢」的問題，[`h5v052`] 才讓開場男孩在 1980-02-10 挖到破鈔；把 `[h5v082]` 留成已找回原鈔還能說什麼的問題，[`h5v084]` 才報 2020 年 Kaye、Meltzer 一張原鈔研究，`loops[]` 新綁 `[h5v082]` 到 `[h5v097]` 的浸水季節推論。金額、序號和研究結論未改。事件日期見 [FBI 案件史](https://www.fbi.gov/history/cases-and-criminals/db-cooper-hijacking)；研究的單鈔與發表年份見 [Kaye、Meltzer 原文](https://www.nature.com/articles/s41598-020-70015-z)。

`[h5v020]` 現說地面「準備交付」的鈔票已記序號，讓字卡及口播發生在西雅圖實際交付 `[h5v023]` 之前，不把先後倒置；FBI 的序號對照與贖金金額主張維持不變。`[h5v010]` 只預告原鈔切片的顯微分析，沒有把實際取樣日期說成論文的 2020 發表日期。`tail-stairs-ground` 卡只問落點，下一景才說地面沒人能指出位置；開場 `open-tail` 保留飛機遠景，不畫無來源的空中展開階梯、人物或落點。這些是敘事及示意界線調整，不新增嫌疑人、漂流路線或生死結論。

此輪旁白版的敘事 hash **`3f5a31da88e7f485`**，**93 景、108 句、六章**；靜態 **520.867 秒（8.681 分）**，片尾 **7.5 秒**、最長畫面 **7.5 秒**。後續兩張畫面改原生卡，插圖占比降至 **62.9%**。`lint` **0 errors／0 warnings**，`cadenceProblems=[]`、`renderProblems=[]`。本段是修稿者的增量核對；正式合成後必須確認正文至少 8:00。

## 圖像生成前的畫面修訂（2026-10-14，歷史稿）

本輪只改 `look`、畫面 prompt、兩張場景的版型和原生卡文字；旁白、章序、場景 ID 與語音 hash `f50a446cd77d3d5a` 不變。因 `narrativeHash` 會納入場景版型，敘事 hash 改為 `8d6630c419867e31`，原 11 題盲評須依新 hash 重做。`look` 保留已選定的 `cute-mystery` C3 具名預設及原始風格文字，末尾加上條件句：只有明列人物才畫 chibi；空景和物件景維持無生命、無五官的形體，避免憑空加人。`open-counter` → `open-ticket` → `open-aisle` 用同一種深色商務外套與成年匿名人物串起現金購票和機艙入座；機票的印字面朝向畫面外，卡通圖不冒充 FBI 原件。`open-tail` 只留遠距飛機與雲層，空中機尾階梯細節仍由文字卡承載。

五組重複構圖已拆開：`open-note` 畫客艙傳紙條、`captain-note` 畫送到駕駛艙；`agency-alert` 畫概念性接訊辦公室、`interview-notebook` 畫訪談筆記；`aircraft-search` 畫機艙搜索、`comparison-desk` 畫兩份見證紀錄與證物待比對；`nationwide-leads` 畫未標點的美國地圖、`archive-many-folders` 畫候選檔案；`sample-room` 畫領帶旁的樣本容器、`modern-control-context` 畫河水對照採集。它們都不聲稱還原特定現場文書或採樣動作。

`discovery-date` 標「插畫重建」，接續的 `boy-bank` 只畫匿名男孩和印刷面背離鏡頭的三捆紙鈔；`single-bill-sample` 只畫一張原鈔的空白破損邊緣。`chutes-carried` 改成 FBI 來源的 4／2 數字卡，`diatom-observation` 改成署名研究的文字卡，不生成想像中的傘包配置或偽顯微影像。這些是畫面風險收窄，原來的事實主張未增加。

畫面修訂後 `lint` **0 errors／0 warnings**；估算 `cadenceProblems=[]`、`renderProblems=[]`，106 個畫面狀態平均 **4.9 秒**、最長 **7.5 秒**，65 張插圖占正文估時 **62.9%**；65 個 shot prompt 均不重複。`keyframes --dry-run` 確認 MiniMax `image-01`、1K、65 張，單次預估約 **US$0.88**；這不是實際生成或圖像驗收。

## 最新敘事與音訊狀態（2026-10-14）

視覺修訂後的敘事 hash **`299218902636bb97`**，由另一名只讀旁白的盲評者答完 11 題，外部 `review/narrative.json` 記錄 **11/11 PASS**；FBI 案件史與 Kaye–Meltzer 2020 論文另做來源抽查，未擴大為每一個新畫面欄位的獨立重審。現行 `lint` 仍為 0 errors／0 warnings、93 景、108 句。後續若變動旁白或版型，需檢查關卡雜湊是否失效。

本版 `tts` 時間軸為 **535.533 秒（8:55.5）**，其中兩句重錄、100 句沿用 v2 既有音檔；外部 `timeline.json` 的語音 hash 為 `9264cb545d070dd8`。`check-audio` 停在 speech/transcribe POST 結果不明的持有狀態（請求 SHA-256 前綴 `903424`），尚無音訊核准。未確認該次請求結果前，不清除持有狀態或重送；音訊聽審、圖片逐張審查、成片播放與站主驗收各自仍待完成。
