# A30 獨立事實查核紀錄

日期：2026-10-20（Asia/Taipei）。Reviewer：`/root/facts_b10_a30`。

本輪實際以 curl 經繼承的 HTTPS 代理讀取 8 個列入來源，保持 TLS 驗證，User-Agent 為專案 editorial 值。以下均為本輪讀到的內容，不沿用舊 review 的 sources_opened 或 PASS。原始頁面暫存於 repo 外 `/tmp/brand-facts-b10-a30`；本文件只留必要核對摘要。

## 來源讀取結果

| 索引（JSON零起算） | 來源 | HTTP | HTML字元數 |
| --- | --- | --- | --- |
| 0 | [IKEA](https://www.ikea.com/us/en/this-is-ikea/about-us/from-humble-origins-to-global-brand-a-brief-history-of-ikea-pubad29a981/) | 200 | 904859 |
| 1 | [IKEA Museum](https://ikeamuseum.com/en/explore/product-stories/lovet-coffee-table-1956/) | 200 | 99350 |
| 2 | [IKEA Museum](https://ikeamuseum.com/en/explore/the-story-of-ikea/flatpacks/) | 200 | 90691 |
| 3 | [IKEA Museum](https://ikeamuseum.com/en/explore/designer-portraits/gillis-lundgren/) | 200 | 122313 |
| 4 | [IKEA Museum](https://ikeamuseum.com/en/explore/the-story-of-ikea/the-first-ikea-store/) | 200 | 115537 |
| 5 | [Wikipedia](https://en.wikipedia.org/wiki/IKEA) | 200 | 1477982 |
| 6 | [Wikipedia](https://en.wikipedia.org/wiki/Ready-to-assemble_furniture) | 200 | 103318 |
| 7 | [The Conversation（Cathrine Jansson-Boyd，Anglia Ruskin University，2018年）](https://theconversation.com/the-ikea-effect-how-ingvar-kamprads-company-changed-the-way-we-shop-90896) | 200 | 177530 |

## must_verify 逐項判定

| 零起算主張索引 | 實際核對與必要邊界 |
| --- | --- |
| 0 | IKEA官方簡史明載1953採平整包裝，郵購家具運輸成本與損壞率高，並說平整包裝原已存在。 |
| 1 | 博物館LÖVET及Flatpacks頁皆支持1953型錄三桌、1956型錄LÖVET不是第一款；Flatpacks頁寫Ovendals展示新五金桌。 |
| 2 | Flatpacks頁明確表示IKEA不是發明者，最早例子據說Thonet椅，瑞典Triva為1944且不成功；維基百科另一頁另記Triva1943，稿內只歸屬博物館，不把兩種年份合併成無歸屬定論。 |
| 3 | Ready-to-assemble furniture維基百科載Lundgren鋸桌腳以放進車內及1956開始販售的報導版本。列入的博物館四頁本輪均未見此故事，但無法推及官方全部網站，故僅作有歸屬版本，不當1953起源。 |
| 4 | IKEA官方簡史支持1943／17歲創立、筆皮夾、1948家具與名稱字首。 |
| 5 | 第一家店博物館頁寫1958/10/28及some furniture可當日帶回；原稿泛稱家具已修為部分平整包裝家具。維基百科亦有開店日期。 |
| 6 | Lundgren博物館頁載over 400、2012 Tenzing及物流效率促成平整包裝大規模推行；不把評審片段摘要說成完整評語。 |
| 7 | Flatpacks頁支持家中自組降低零售價、密平包裝提升運載儲存量、1960/70年代缺螺絲及難懂說明造成不良口碑。 |
| 8 | Wikipedia IKEA頁有one-way與讓人看完整間店的說明；The Conversation原文支持圓形單向、怕錯過與捷徑很少走的心理分析。稿末原把公司動機寫成定論，已改明確歸屬該學者，不保證人人多買。 |

## 本輪更正與限制

- 本輪實際重讀全部8個列入來源，更新checked日期。
- 將1958年第一家店可當日帶回範圍限為部分平整包裝家具，貼合博物館some furniture原文。
- 修正now段與takeaway，把賣場心理解讀明確歸屬The Conversation學者，刪去把兩件事都描述成公司精算動機的過度結論。
- 保留拆桌腳故事的維基百科轉述歸屬與四個博物館頁面的範圍限制。

- 沒有查詢正式站的既有集數，不能據此宣稱題目未製作；本收據核准企劃事實，不核准未來逐字稿、旁白、圖片或成片。
- 所有列入來源都讀得到HTML。無需新增 reviewer_only。A30的Wikipedia IKEA全文超過40,000字，但日期與one-way位於worker前40,000字內；B10維基百科worker文字31,403字，相關主張未超過上限。

最終企劃故事雜湊：`4a492455abd4df6db063951a56a0d12b8e7e46363e3b57c613c7db765d458c8c`。以 `STORY_KEYS` 投影後執行 `storyProblems`、`reviewProblems`，均無問題。
