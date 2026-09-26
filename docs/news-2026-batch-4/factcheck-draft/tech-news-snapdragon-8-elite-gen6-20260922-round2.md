# tech-news-snapdragon-8-elite-gen6-20260922 查核報告（第二輪）

- 查核者：獨立查核代理（第二輪），沒有參與撰稿，也沒有參與第一輪
- 查核日：2026-09-26（台北），重抓時間 14:51Z（台北 22:51）
- 內容包：`apps/api/app/guides/content/tech-news-snapdragon-8-elite-gen6-20260922.json`
- 研究紀錄：`docs/tech-news-2026/research/tech-news-snapdragon-8-elite-gen6-20260922.json`（已在 `factcheck` 底下加 `second_round`）
- 規格：`FACTCHECK-48.md`、`agents/tech/SECOND-ROUND.md`（第一輪規格 `agents/tech/FACTCHECK.md` 全部適用）、DELTA-4-8（全）、DELTA-4-7 第 3、4、10、11、14、16 條
- 第一輪報告：`factcheck/tech-news-snapdragon-8-elite-gen6-20260922-round1.md`

## 摘要

- 查了 87 條：CONFIRMED 75、CHANGED 11、NOT FOUND 0、OUT OF SCOPE 1（FAQ 第 2 題問句，依裁定保留）。
- 範圍：第一輪改過或新寫的每一句（26 條，含研究紀錄的修改）；協調者四條裁定（9 條）；但書與否定句回掃（20 條）；以固定種子 20260926 從第一輪 94 條 CONFIRMED 抽出的 32 條。
- 修改：內容包 7 處文字、研究紀錄 9 處文字。第一輪自己的 16 處內容包修改全部站得住，只有 Xiaomi 那一處（兩個位置）還掉了 across。
- 四條裁定：（1）五家夥伴的歸因保留，五個職稱逐一對過 PDF；（2）FAQ 第 2 題問句保留「台積電」，答句刪掉 2 奈米那一句，只說兩份文件都沒有代工廠；（3）callout 第一句主詞已改；（4）新聞稿逐行列數字，兩款平台唯一的規格數字就是 `2nm`（1 次），內容包沒有混進別的數字。
- 最重的三處：Xiaomi 的 across（正文與 FAQ 第 4 題）；第一段與 FAQ 第 1 題的台灣否定句收窄到兩份文件；第四節小標與圖解第四格的「沒寫規格」收窄成「詳細規格」（新聞稿其實寫了 2 奈米與 CPU／GPU／NPU）。
- 研究紀錄：第一輪改了內容包，但紀錄裡還留著「目的是」「是為了」「同時採用」與四處「沒有任何規格數字」。這些已照來源改掉，免得翻譯或審稿時照紀錄改回去。
- 段落字數 2,415 → 2,438（≤3,000）。自檢：`check_article.py` → `OK … zh-TW paragraphs 2438`（exit 0）；`pack_cli lint` 只有 `image_missing` ×2 與 `raw_internal_url`（預期中，exit 1）。
- 結論：`ok`。

## 1. 來源重抓

指令：`curl -sSL --max-time 30 -A 'Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)'`，同一主機間隔 2 秒；UA、標頭、查詢字串都沒有任何人的姓名或 email。落地檔在 `_raw/tech-news-snapdragon-8-elite-gen6-20260922/round2/`（`fetch-log.tsv` 記每一筆）。

| # | 來源 | HTTP | 落地 bytes | 型別 | 正文 | 與第一輪 `round1/` |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 新聞稿 `.md` | 200 | 8,917 | text/markdown | 是（front matter、Highlights、兩節正文、品牌名單、夥伴 PDF 連結） | 逐位元組相同 |
| 2 | Partner Quote Sheet PDF | 200 | 86,268 | application/pdf | 是（2 頁，系統 python 的 pypdf 抽文字，八段引言） | 逐位元組相同 |
| — | 新聞稿 HTML（不在 sources，只驗外殼） | 200 | 13,616 | text/html | 否（React 外殼）；檔案與第一輪只差第 327 行一處（頁面內嵌值），大小相同 | — |

- **verbatim_quote**：研究紀錄 2 條 sources 與 25 條 verified_facts，用程式做連續字串比對，**27/27 命中**。.md 是精確子字串；PDF 是空白正規化並還原 pypdf 拆開的 “T echnologies”／“T echnology”／“T ogether” 後的子字串。唯一含 `|` 的引文是 `Press Note | Sep 22, 2026 | MAUI`，就是新聞稿頁首原樣的一行，不是把不同段落拼在一起。沒有含 `...`／`…` 的引文。
- **詞界比對**（兩份來源；PDF 另在刪掉所有空白後再比一次）：TSMC、Taiwan Semiconductor、foundry、foundries、Samsung、Taiwan、Hawaii、HST、PDT、a.m.、p.m.、GHz、MHz、percent、manufactur、fab、fabricat、built by、produced、Gen 5、previous、cores、cache、LPDDR、UFS、Gbps、price、China 全部 0 次。PST 在 PDF 去空白後的字串裡有 1 次子字串，是跨字拼出來的，詞界比對是 0。PDF 裡的 memory 1 次是 Doubao 引言的 on-device memory，不是規格。

## 2. 改掉的地方（before → after，來源）

來源簡寫：MD＝`https://www.qualcomm.com/news/releases/2026/09/snapdragon-leads-the-agentic-ai-age-with-two-of-the-world-s-fast.md`；PDF＝`https://www.qualcomm.com/content/dam/qcomm-martech/dm-assets/images/company/news-media/media-center/press-kits/snapdragon-summit-2026-press-kit/day-1/documents/PartnerQuoteSheet.pdf`。

### 內容包（7 處）

1. **第三節夥伴段，Xiaomi（但書掉了：across）**
   - before：「說會在即將推出的高階裝置上採用這兩款平台。」
   - after：「說會把這兩款平台用在即將推出的多款高階裝置上，沒有說哪一支用哪一款。」
   - 原文（PDF）：`By leveraging both Snapdragon 8 Elite Extreme Gen 6 and Snapdragon 8 Elite Gen 6 across our upcoming premium devices`。
   - 理由：第一輪拿掉了「同時採用」，但「在……裝置上採用這兩款平台」仍會被譯成 “use both platforms in its upcoming devices”，across 的意思（分布在整條產品線、沒有對應到機型）又不見了。後半句是研究紀錄 verified_facts 本來就寫的「沒有說哪一支用哪一款」，引言裡也確實沒有任何機型名。
2. **FAQ 第 4 題**：同第 1 處。「Xiaomi 說會在即將推出的高階裝置上採用這兩款平台，」→「Xiaomi 說會把這兩款平台用在即將推出的多款高階裝置上、沒有說哪一支用哪一款，」（PDF）。
3. **第一段（否定句沒有指向來源）**
   - before：「查核到 2026 年 9 月 26 日為止，還沒有看到這兩款平台在台灣上市的消息。」
   - after：「查核到 2026 年 9 月 26 日為止，新聞稿與夥伴引言文件都沒有提到這兩款平台在台灣上市的消息。」
   - 依據：MD 與 PDF 的 Taiwan 都是 0 次。
   - 理由：研究代理和兩輪查核都只讀了這兩份文件，沒有查過各品牌的台灣頁面。「還沒有看到……消息」讀起來像已經普查過；SECOND-ROUND 第 4 點要求把範圍不明的否定句收窄到引用的頁面與查核日。
4. **FAQ 第 1 題**：理由同第 3 處。
   - before：「高通新聞稿與 Snapdragon Summit 夥伴引言文件都沒有提到台灣，也沒有給出任何上市日或售價；查核到 2026 年 9 月 26 日為止，還沒有查到台灣上市的官方資訊。」
   - after：「查核到 2026 年 9 月 26 日為止，高通新聞稿與 Snapdragon Summit 夥伴引言文件都沒有提到台灣，也沒有給出任何上市日或售價。」
   - 查核日的限定還在，只是移到有範圍的那一句；刪掉的是超出兩份文件的「官方資訊」。
5. **第四節小標（第一輪第 4 點的連帶）**
   - before：「新聞稿沒寫的事：代工廠、規格、上市日、台灣」
   - after：「新聞稿沒寫的事：代工廠、詳細規格、上市日、台灣」
   - 理由：新聞稿寫了 2 奈米製程節點，以及 Oryon CPU、Adreno GPU、Hexagon NPU，同一篇的表格「製程與架構」列也照登了。說新聞稿「沒寫規格」和表格互相矛盾。它沒寫的是時脈、核心數、快取、記憶體這類詳細規格（MD）。
   - 研究紀錄 `diagram.nodes` 第四格同步修改，見下一小節第 1 處。
6. **FAQ 第 2 題答句（裁定 2）**
   - before：「新聞稿與夥伴引言文件都沒有提到任何晶圓代工廠的名字；新聞稿只寫 8 Elite Gen 6 建構在與 Extreme 版「同樣的」2 奈米製程節點上，沒有說明由誰製造。」
   - after：「新聞稿與夥伴引言文件都沒有提到任何晶圓代工廠的名字，也沒有說明由誰製造。」
   - 理由：問句是「是台積電做的嗎」，接著就答「2 奈米」，台灣讀者會把這當成暗示。依裁定，答句只說兩份文件都沒有代工廠。
   - 2 奈米仍在正文、表格與 FAQ 第 3 題。兩份文件的 foundry、TSMC、Samsung、manufactur、fab、built by 皆 0 次。
7. **callout 第一句（裁定 3，純文字）**
   - before：「這兩款平台是高通 2026 年 9 月 22 日發布的新聞稿，」
   - after：「這兩款平台是高通在 2026 年 9 月 22 日的新聞稿裡發表的，」
   - 沒有新增事實。

### 研究紀錄（9 處文字，另加 `factcheck.second_round`）

1. `diagram.nodes` 第四格：「代工廠、規格、上市日、台灣」→「代工廠、詳細規格、上市日、台灣」（跟著第四節小標改；15 個 CJK 單位，剛好在 checker 的上限內）。
2. verified_facts「為什麼同一代分兩款」：「目的是把最新 AI 功能帶到更廣的高階裝置。」→「這個策略讓高通能在推進行動裝置可能性的同時，把最新 AI 功能帶到更廣的高階裝置（原文 allows us to … while bringing，不寫成「目的是」）。」（MD）。第一輪只改了內容包，紀錄還是「目的是」。
3. verified_facts「同一段引言的下一句」：「設計兩款平台是為了給手機廠（OEM）更多選擇。」→「藉由設計兩款平台，高通讓手機廠（OEM）有更多選擇（原文 By designing two innovative platforms, we're giving OEMs greater choice，不寫成「是為了」）。」（MD）
4. verified_facts Xiaomi：「即將推出的高階裝置會同時採用 …」→「會把 … 用在即將推出的多款高階裝置上（原文 across our upcoming premium devices，不寫成「同時採用」）」，並註明「唯一」只在夥伴文件這個範圍內成立，文章不寫（PDF）。
5. not_said 第 2 條：「沒有規格數字。新聞稿 .md 裡 GHz、%、percent 皆 0 次」→「除了 2nm process node（8 Elite Gen 6 那段，1 次），沒有規格數字。新聞稿 .md 裡 GHz、percent 皆 0 次，9 個 % 都是網址裡的 %20」（MD；原句的「% 0 次」字面上也不對）。
6. editorial_brief：「8 Elite Gen 6 採用「同樣的」2 奈米節點與 Oryon CPU……。沒有任何規格數字、代工廠……」→「……2 奈米節點，並採用 Oryon CPU、Adreno GPU、Hexagon NPU（「同樣的」只修飾 2 奈米節點）……除了 2 奈米製程節點，沒有任何規格數字，也沒有代工廠……」（MD）。
7. editorial_brief 第四節建議：「代工廠、規格數字、……」→「代工廠、2 奈米製程節點以外的規格數字、……」
8. editorial_brief「刻意不寫」：「任何規格數字」→「2 奈米製程節點以外的任何規格數字」。
9. sourcing_notes：「規格數字、代工廠、上市日、售價、台灣資訊不在任何一條來源裡」→「2nm process node 以外的規格數字、……」。

## 3. 協調者裁定

| 裁定 | 做法 | 查核 |
| --- | --- | --- |
| 1. 第三節五家夥伴的歸因保留 | 未改 | PDF 逐一對過：HONOR `President of Products at HONOR`＝產品總裁；Motorola `Executive Director and Head of Global Product Marketing for Motorola Mobility`＝全球產品行銷主管；vivo `Senior Vice President & CTO at vivo`＝資深副總裁暨技術長；Xiaomi `Partner and President of Xiaomi Corporation`＝合夥人暨總裁；RedMagic 用條目名稱，沒寫 ZTE／Nubia 職稱，符合紀錄「不寫品牌從屬」。 |
| 2. FAQ 第 2 題問句保留「台積電」，答句只說兩份文件都沒有代工廠 | 答句刪掉 2 奈米那一句（第 2 節第 6 處） | 答句現在只剩「新聞稿沒有寫」「兩份文件都沒有代工廠名字、沒有說明由誰製造」；全文「台積電」只在這個問句出現 1 次。 |
| 3. callout 第一句主詞 | 改成「這兩款平台是高通在……新聞稿裡發表的」 | 沒有新增事實；後面的電頭、時刻時區、查核日都沒動。 |
| 4. 「2 奈米製程節點以外」四句 | 確認，未改 | 見下。 |

**裁定 4 的依據。** 我把新聞稿 `.md` 每一行的數字都列出來（`_tools/…/round2/scan-before.out` 第 3 節）：

- 日期：`Sep 22, 2026`。
- 產品名裡的 8 與 6，例如 `Snapdragon 8 Elite Gen 6`。
- 圖片網址參數，例如 `wid=814`。
- `%20`。
- 「Contact Information」的兩支電話。
- 「Related Press Releases」裡別的新聞稿，例如 `Dragonwing Q-2390`、`LEAP 2026`、`Sep 21, 2026`。
- 兩款平台自己的規格數字只有第 40 行的 `2nm`（1 次）。

「About Qualcomm」的 four decades 是公司簡介。PDF 裡的數字只有產品名裡的 8／6，以及 `iQOO 16`、`RedMagic 12Pro+`。

內容包 zh-TW 全文的數字：

- 日期：2026、9、22、26。
- 產品名：8、6。
- 奈米：2（9 次，全部是 2 奈米製程節點）。
- 機型名：16（iQOO 16）、12（RedMagic 12Pro+）。
- 第二個結尾連結標題裡的 35（照目標文章 zh-TW 標題逐字）。

沒有任何規格數字混進來。另外用中文數詞寫的地方：

- 「兩款」：原文 `not one, but two`。
- 「三項新功能」「這三點」：原文 `New features:` 下正好三點。
- 「四方面」：原文逐一列出 AI, gaming, camera, and connectivity，不是 including。
- 「之二」：原文 `Two of the`。

這些都是同一句裡就列出項目的計數，不是清點出來的選題數字。

## 4. 回掃但書與範圍

| 但書／限定 | 位置 | 結果 |
| --- | --- | --- |
| including（名單不是全名單） | summary 第 3 條、第三節第一段、FAQ 第 4 題、callout | 四處都在（「以「包括」起頭」「這不是完整名單」） |
| many of the same | summary 第 2 條、第二節第二段、表格兩格、第四節第二段、FAQ 第 3 題、圖解第二格 | 都在（「許多相同的」）；第二節的「——不是全部」見待決第 2 條 |
| allows | 第一節第二段 | 在（「讓高通能」）；研究紀錄同步改掉「目的是」 |
| across devices | Xiaomi：第三節、FAQ 第 4 題 | **已補**（第 2 節第 1、2 處） |
| upcoming | vivo（iQOO 16、iQOO Pad Ultra）、Xiaomi、RedMagic 12Pro+、第三節末段、第五節、callout | 都在（「即將推出」） |
| will debut | 第三節第一段 | 在（「將」「將首度登場」） |
| among the first | 第三節 vivo | 在（「首批之一」），沒有寫成首款 |
| for the first time | 第三節 Motorola | 在，照原句、沒延伸 |
| 否定句的範圍 | 第一段、FAQ 第 1 題 | **已收窄**到兩份文件（第 2 節第 3、4 處）；其餘否定句（summary 第 4 條、第二節、第四節、第三節末段、callout、description、FAQ 第 2、3 題）都以「新聞稿」「夥伴引言文件」或「兩份來源」為主詞，並帶查核日 |
| 「沒寫規格」的寬度 | 第四節小標、圖解第四格、研究紀錄四處 | **已收窄**（第 2 節第 5 處、紀錄第 1、5–9 處）；description 的「時脈等規格數字」本來就限定在時脈這一類，未改 |

**界線**

- `topics` 是 tech、tech-news，沒有 finance；沒有免責 callout，只有一個一般 callout。
- 沒有購買、升級或等待建議：第五節是標明「編輯設計的例子」的讀規格表方法。
- 沒有推定台灣可用，台灣相關的句子都寫「沒有提到」並帶查核日。
- 廠商宣稱都有歸因：最強大、最快之二、三項新功能、多旗艦策略、五家夥伴說法。
- 沒有聯發科、比較或代工廠。

**summary ⊆ 正文，FAQ ⊆ 正文**

- summary 四條都在正文；summary 裡的數字 2026、9、22、2、8、6 都在正文。
- FAQ 答句的事實都在正文。FAQ 第 2 題的「夥伴文件也沒有代工廠」，正文沒有逐字說到，但 PDF 詞界比對 0 次、有來源撐。
- 圖解四格裡的數字只有 8 與 6（產品名），都在正文。

## 5. 逐條主張表

判定：C＝CONFIRMED、CH＝CHANGED、NF＝NOT FOUND、OS＝OUT OF SCOPE。「R1#」是第一輪報告的主張編號。

### A. 第一輪改過或新寫的句子（26 條）

| # | R1# | 位置 | 主張（現行文字） | 判定 | 依據 |
| --- | --- | --- | --- | --- | --- |
| 1 | 6 | description | 「新聞稿沒有寫的代工廠、時脈等規格數字、上市日與台灣資訊」 | C | MD：GHz、Taiwan、foundry 0；「時脈等」限定在時脈這一類，不含製程節點 |
| 2 | 11 | 第一段 | 「在 Snapdragon Summit 期間發布」已刪 | C | 全文「期間」0 次；MD 只有 Summit 標籤與夥伴文件連結 |
| 3 | 21 | summary 2 | 「自研的 Oryon CPU，以及 Adreno GPU 與 Hexagon NPU」 | C | MD `custom-built Qualcomm Oryon™ CPU, rearchitected … Adreno™ GPU, and the advanced … Hexagon™ NPU` |
| 4 | 26 | summary 4 | 「2 奈米製程節點以外的規格數字」 | C | MD 唯一規格數字 `2nm`（第 3 節） |
| 5 | 34 | 第一節第二段 | 「讓高通能把最新 AI 功能帶到更廣的高階裝置」 | C | MD `allows us to … while bringing our latest AI innovations to a broader range of premium devices` |
| 6 | 35 | 第一節第二段 | 「而設計兩款平台讓手機廠（OEM）有更多選擇」 | C | MD `By designing two innovative platforms, we're giving OEMs greater choice` |
| 7 | — | 第一節第二段 | 「新聞稿也說，兩款平台都結合效能與裝置端智慧……四方面有所進步」（歸因精簡後） | C | MD Highlights 第 2 點；該段歸因語 2 個 |
| 8 | — | 第二節第一段 | 「高通稱……並列出三項新功能」（歸因精簡後） | C | MD `New features:` 三點；段尾「這三點都是高通的說法」仍在 |
| 9 | 42 | 第二節第一段 | Adreno Neural Fusion「用 AI 提供智慧化的遊戲圖形（intelligent graphics），帶來更沉浸的遊戲、更豐富的畫面與更長的遊戲時間」 | C | MD `using AI to deliver intelligent graphics for more immersive gameplay, richer visuals, and longer playtime` |
| 10 | — | 第二節第二段 | 刪去重複的「原文是「許多相同的」」後，「許多相同的」（many of the same）仍在 | C | MD |
| 11 | 55 | 表格 | Extreme「製程與架構」：「新聞稿未列（8 Elite Gen 6 那段寫的是「同樣的」2 奈米製程節點）」 | C | MD 的 Extreme 一節沒有製程、Oryon、Hexagon |
| 12 | 70 | 第三節 | Xiaomi「則點名兩款都會用」（刪「唯一」） | C | PDF `By leveraging both …` |
| 13 | 71 | 第三節 | Xiaomi「會在即將推出的高階裝置上採用這兩款平台」 | **CH** | across 掉了；第 2 節第 1 處 |
| 14 | 74 | 第三節末段 | 「能確認的品牌與機型名稱僅止於這一篇列出的部分」 | C | 九個品牌（MD）與三個機型（PDF）都在本篇；12Pro+ 在第五節 |
| 15 | 79 | 第四節第一段 | 「時脈、核心數、快取、記憶體或 2 奈米製程節點以外的其他規格數字」 | C | MD |
| 16 | 88 | 第五節 | 「夥伴引言裡「即將推出」的機型」 | C | 機型名只在 PDF |
| 17 | 94 | FAQ 2 | 「新聞稿只寫 8 Elite Gen 6 建構在與 Extreme 版「同樣的」2 奈米製程節點上」 | **CH** | 事實本身正確，但放在「是台積電做的嗎」的答句裡會形成暗示；依裁定 2 刪除（第 2 節第 6 處） |
| 18 | 96 | FAQ 3 | 「「同樣的」2 奈米製程節點上，採用 Oryon CPU、Adreno GPU 與 Hexagon NPU」 | C | MD：same 只修飾 2nm |
| 19 | 97 | FAQ 3 | 「除了 2 奈米製程節點，新聞稿沒有給出任何規格數字」 | C | MD |
| 20 | 101 | FAQ 4 | Xiaomi「會在即將推出的高階裝置上採用這兩款平台」 | **CH** | 同 #13 |
| 21 | 106 | callout | 「新聞稿除了 2 奈米製程節點，只有定性說法，沒有其他規格數字」 | C | MD |
| 22 | 120 | 紀錄 | event_date_basis：照印的「9 月 22 日」、電頭茂宜島、不寫時區 | C | MD `Press Note \| Sep 22, 2026 \| MAUI`；DELTA-4-8 第 4 條 |
| 23 | 120 | 紀錄 | editorial_brief 第一節建議「不寫時區」 | C | 同上 |
| 24 | 120 | 紀錄 | must_not_write 日期那條 | C | 同上 |
| 25 | — | 紀錄 | must_not_write 新增：Oryon／Adreno／Hexagon／2 奈米不寫成 Extreme 另列的規格 | C | MD |
| 26 | 121 | 紀錄 | verified_facts Adreno Neural Fusion「用 AI 提供智慧化的遊戲圖形」 | C | MD |

### B. 協調者裁定（9 條）

| # | 主張 | 判定 | 依據 |
| --- | --- | --- | --- |
| 27 | HONOR 的產品總裁點名 Extreme | C | PDF |
| 28 | RedMagic 點名 Extreme | C | PDF |
| 29 | vivo 資深副總裁暨技術長：iQOO 16、iQOO Pad Ultra「首批之一」 | C | PDF `among the first devices` |
| 30 | Xiaomi 合夥人暨總裁 | C | PDF |
| 31 | OPPO 的引言沒有點名任一款 | C | PDF（OPPO 段只有 `latest milestone`、agentic AI） |
| 32 | FAQ 2 問句「是台積電做的嗎？」 | OS | 裁定 2 保留 |
| 33 | callout 第一句主詞 | **CH** | 裁定 3（第 2 節第 7 處） |
| 34 | 新聞稿兩款平台唯一的規格數字是 2nm | C | 第 3 節逐行數字表 |
| 35 | 內容包沒有 2 奈米以外的規格數字 | C | 第 3 節 |

### C. 回掃（20 條）

| # | 主張 | 判定 | 依據 |
| --- | --- | --- | --- |
| 36 | 第一段「還沒有看到這兩款平台在台灣上市的消息」 | **CH** | 第 2 節第 3 處 |
| 37 | FAQ 1「還沒有查到台灣上市的官方資訊」 | **CH** | 第 2 節第 4 處 |
| 38 | 第四節小標「新聞稿沒寫的事：代工廠、規格……」 | **CH** | 第 2 節第 5 處 |
| 39 | 研究紀錄圖解第四格「代工廠、規格……」 | **CH** | 同上 |
| 40 | 研究紀錄 verified_facts「目的是」「是為了」 | **CH** | 紀錄第 2、3 處 |
| 41 | 研究紀錄 verified_facts Xiaomi「同時採用」 | **CH** | 紀錄第 4 處 |
| 42 | 研究紀錄 not_said、editorial_brief、sourcing_notes「沒有任何規格數字」 | **CH** | 紀錄第 5–9 處 |
| 43 | including 四處 | C | MD Highlights 第 3 點 |
| 44 | many of the same 七處 | C | MD |
| 45 | upcoming（vivo、Xiaomi、RedMagic） | C | PDF 3 次 |
| 46 | will debut「將首度登場」 | C | MD |
| 47 | 第四節第二段「這兩款平台的來源都沒有提到台灣上市」 | C | 範圍是兩份來源並帶查核日 |
| 48 | 第二節「——不是全部」 | C | 研究紀錄 verified_facts 的讀法；待決第 2 條 |
| 49 | 27 條 verbatim_quote 連續字串 | C | 第 1 節 |
| 50 | 兩個結尾連結 text＝目標 zh-TW title 逐字；目標都有五語 | C | `tech-news-2026-index`、`tech-news-nvidia-mediatek-20260831` 皆 en／ja／ko／zh-CN／zh-TW |
| 51 | 界線：無 finance、只有一個 callout、無購買建議、無台灣推定 | C | 第 4 節 |
| 52 | 「本文」0 次；description 句尾只有「（2026 年 9 月查證）」；title／description／summary 無選題計數 | C | 掃描 |
| 53 | 開頭段歸因語 | C | 見第 6 節與待決第 1 條 |
| 54 | 正文段落歸因語 ≤2（第三節夥伴段依裁定 1 例外） | C | 逐段數過 |
| 55 | 日期：slug 尾碼＝news_date＝第一段 2026-09-22；查核日四處一致 | C | 內容包兩條 source、紀錄、第二段、表格 caption、圖解 caption 都是 2026-09-26 |

### D. 從第一輪 CONFIRMED 隨機抽查（32 條，種子 20260926，`_tools/…/round2/sample_r2.py`）

| # | R1# | 位置 | 主張 | 判定 | 依據 |
| --- | --- | --- | --- | --- | --- |
| 56 | 3 | description | 9/22 同時發表兩款 | C | MD `Sep 22, 2026`、`not one, but two` |
| 57 | 4 | description | 電頭茂宜島 | C | MD `location: "MAUI"` |
| 58 | 7 | description | 句尾「（2026 年 9 月查證）」、無選題計數 | C | 內容包 |
| 59 | 8 | meta | slug＝news_date＝第一段；order 339；topics | C | DELTA-4-8 第 4 條 |
| 60 | 9 | 第一段 | 高通（Qualcomm Technologies）發布新聞稿 | C | MD `Qualcomm Technologies, Inc. unveiled today` |
| 61 | 13 | 第一段 | 沒有印出時刻或時區 | C | 時刻／時區詞 0；沒有 `\d:\d\d` |
| 62 | 19 | summary 2 | 高通稱「多旗艦策略」 | C | MD |
| 63 | 20 | summary 2 | 與 Extreme 版同樣的 2 奈米節點 | C | MD `the same advanced 2nm process node`；上下文唯一的另一款是 Extreme |
| 64 | 22 | summary 2 | 許多相同的功能帶到更多頂級手機 | C | MD |
| 65 | 27 | summary 4 | 沒有上市日、售價、台灣 | C | MD、PDF |
| 66 | 30 | 第一節 | 標題稱「全球最快的行動 SoC 之二」＋英文原文 | C | MD title／H1 |
| 67 | 31 | 第一節 | 正文沒有測試條件或比較對象 | C | fastest 只在標題 2 次 |
| 68 | 32 | 第一節 | 行動手機事業資深副總裁暨總經理 | C | MD |
| 69 | 36 | 第一節 | 效能＋裝置端智慧、四方面進步 | C | MD |
| 70 | 37 | 第二節 | 小標 | C | — |
| 71 | 38 | 第二節 | 「最強大的行動平台」 | C | MD `most powerful mobile platform` |
| 72 | 39 | 第二節 | 用於最先進的 Android 手機 | C | MD |
| 73 | 40 | 第二節 | 列出三項新功能 | C | MD |
| 74 | 41 | 第二節 | AI 代理：更快、更個人化、更可靠、隨一天作息調整 | C | MD |
| 75 | 49 | 第二節 | 沒寫哪一家晶圓廠 | C | 詞界 0 |
| 76 | 51 | 第二節 | 沒列少了哪些功能 | C | MD |
| 77 | 53 | 表格 | 定位／Extreme | C | MD |
| 78 | 54 | 表格 | 定位／Gen 6 | C | MD |
| 79 | 58 | 表格 | 新功能／Gen 6：未逐項列出 | C | MD |
| 80 | 63 | 第三節 | including 名單與原文順序 | C | MD `HONOR, iQOO, Motorola, OnePlus, OPPO, REDMI, RedMagic, vivo, and Xiaomi` |
| 81 | 68 | 第三節 | Motorola 全球產品行銷主管、for the first time | C | PDF |
| 82 | 78 | 第四節 | 沒有任何晶圓代工廠名字 | C | 詞界 0 |
| 83 | 80 | 第四節 | 除標題外沒有跑分或比較對象 | C | MD |
| 84 | 83 | 第四節 | 少了哪些功能沒寫 | C | MD |
| 85 | 85 | 第五節 | 兩款名稱只差「Extreme」 | C | MD |
| 86 | 95 | FAQ 3 | 最強大的行動平台＋三項新功能 | C | MD |
| 87 | 103 | FAQ 5 | 標題說法、正文無測試或比較 | C | MD |

計數：C 75、CH 11、NF 0、OS 1，共 87。

## 6. 讀者優先

- 「本文」0 次；指涉自己用「這篇文章」「這一篇」。
- description 句尾只有「（2026 年 9 月查證）」。
- 開頭段原本只有 1 個歸因語（「新聞稿電頭寫的地點是」）。台灣那句收窄後，多了「新聞稿與夥伴引言文件都沒有提到」：這是否定句必須指向 sources[] 的要求（FACTCHECK-48），事實優先，列為待決第 1 條。
- 其他正文段落的歸因語都 ≤2。第三節夥伴段有五個，依裁定 1 保留。
- 沒有購買建議；「建議」只出現在第二段的「不提供購買建議」，以及 callout 的「以品牌自己公布的資料為準」。

## 7. 留給協調者

1. 第一段現在有兩個指向來源的片語：「新聞稿電頭寫的地點是」與「新聞稿與夥伴引言文件都沒有提到」。後者是讓否定句有範圍，不能拿掉。若嫌多，可以把後者縮成「兩份文件都沒有提到」，但要保留範圍。
2. 第二節 8 Elite Gen 6 那段的「——不是全部」是研究紀錄對 many of the same 的語用讀法，字面上沒有這三個字。我保留它，因為紀錄有拘束力，而且「許多」本來就不等於全部。翻譯請照 many of the same 譯，不要加強成「少了某些功能」。
3. 研究紀錄 verified_facts 裡 Xiaomi 那條仍寫「夥伴文件裡唯一點名兩款都會用的」。在 PDF 的範圍內這句是對的，所以保留，並加註「文章不寫『唯一』」。
4. 圖解第四格改成「代工廠、詳細規格、上市日、台灣」，剛好 15 個 CJK 單位（checker 上限）。四語翻譯的 `translations.diagram` 要照這一版譯。

## 8. 自檢輸出（原樣）

```
OK tech-news-snapdragon-8-elite-gen6-20260922 zh-TW paragraphs 2438
exit=0
```

```
tech-news-snapdragon-8-elite-gen6-20260922
  warning: raw_internal_url: zh-TW: 2 article link(s) as raw URLs; run `pack_cli relink` so they become article inlines that follow the target's publication
  error: image_missing: zh-TW: /guides/tech-news-snapdragon-8-elite-gen6-20260922/hero.jpg
  error: image_missing: zh-TW: /guides/tech-news-snapdragon-8-elite-gen6-20260922/diagram-1.svg
1 entries checked
exit=1
```

輔助檔在 `_tools/tech-news-snapdragon-8-elite-gen6-20260922/round2/`：

- 腳本：`fetch_r2.sh`、`pdftext_r2.py`、`scan_r2.py`、`sample_r2.py`、`edit_r2.py`。
- 修改前的檔案：`backup/`。
- 差異：`pack.diff`、`record.diff`。
- 各次輸出：`scan-before.out`、`scan-after.out`、`sample.out`、`edit.out`、`check.out`、`lint.out`。
