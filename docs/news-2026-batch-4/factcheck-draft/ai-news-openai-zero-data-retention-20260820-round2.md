# 查核報告（第二輪）：`ai-news-openai-zero-data-retention-20260820`

- 垂直：AI（批次 4.4）、`display_order` 181、`news_date` 2026-08-20、只做 zh-TW
- 第二輪查核者：另一位獨立代理（沒有撰稿、沒有參與第一輪），查核日 **2026-09-23**
- 內容包：`apps/api/app/guides/content/ai-news-openai-zero-data-retention-20260820.json`
- 研究紀錄：`docs/ai-news-2026-09-late/research/ai-news-openai-zero-data-retention-20260820.json`
- 第一輪報告：`C:\Users\x8120\mokaair-work\news44\factcheck\ai-news-openai-zero-data-retention-20260820-round1.md`
- 結論：**複核 51 條主張＋49 條 `verbatim_quote` 連續字串比對；再改 6 處（含 3 處協調者裁定、3 處第二輪自己抓到的事實問題）。verdict `ok`。**

## 1. 今天自己重抓的來源

全部用 `curl -sSL -A 'Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)'`，同主機間隔 2 秒。
請求的 UA、標頭、查詢字串裡沒有任何人的姓名、email 或個人資料。抓取時間 2026-09-23 09:35–09:36（台北）。

| # | 來源 | 狀態 | bytes | 讀到正文？ |
| --- | --- | --- | --- | --- |
| 1 | `https://openai.com/index/offering-zero-data-retention-for-frontier-models/` | 200 | 423,823 | 是。抽出 **8,344 字元**正文，與第一輪抽出的字數相同；含 `OpenAI August 19, 2026`、`Company Safety`、副標、三小節、09-22 更新區塊、四家客戶、CSAM 註腳、Glean 推薦語。 |
| 2 | `https://developers.openai.com/api/docs/guides/your-data` | 200 | 615,506 | 是。另抓 `.md` 版 **79,683 bytes**（與第一輪、研究紀錄完全相同），含 **27 列**端點資格表、資料落地表、CSAM、兩個收回條款。 |
| 3 | `https://developers.openai.com/api/docs/guides/private-safety-processing` | 200 | 460,634 | 是。`.md` 版 **24,849 bytes**（同上），含三項原則、雙層加密、設定與五條客戶責任。 |
| 4 | `https://openai.com/news/rss.xml` | 200 | 744,049 | 是。1,219 個 item；本篇逐字 `<pubDate>Wed, 19 Aug 2026 19:00:00 GMT</pubDate>`。 |

四條 `checked_on` 都是 2026-09-23，與研究紀錄、第二段、表格 caption、圖說一致，**沒有因為我今天重查而改動**。

## 2. 引文比對（規格第 2 條）

研究紀錄 49 條 `verified_facts` 的 `verbatim_quote` 全部用程式對今天抓到的正文做**連續字串**比對
（NFKC 正規化、彎引號與破折號統一、空白壓縮；含 `...`／`…`／`|` 的引文逐片段另外比對）：
**49 條全部命中，0 條拼接、0 條查無。** 命中來源分佈與研究紀錄標的 `url` 一致（公告頁 18 條、RSS 2 條、
資料控制文件 12 條、PSP 指南 17 條；開發者文件的引文絕大多數在 `.md` 與 HTML 抽文兩邊都命中）。

正文裡剩下的一段行內英文引文（PSP 設計目的）今天仍是公告頁上的連續字串。第一輪確認過的 ZDR 定義句
依協調者裁定 1 已從正文移除（見下方 R1），所以正文現在只剩一段英文引文。

## 3. 這一輪改掉的 6 處（before → after）

### 依協調者裁定

**R1（裁定 1）ZDR 定義與濫用監控 30 天背景壓成一句，帶既有的 `article` inline**

- before：第二節第一段整段是 ZDR 定義的英文逐字引文＋中譯（231 字）；第三段句尾「文件也寫明，除非法律要求或為保護服務與第三方而有必要，濫用監控紀錄預設最多保存 30 天——跟後面 PSP 的 30 天保留期是兩回事。」；第四節後面另有一段獨立的 `/v1/agents` `rich_paragraph`。
- after：第二節第一段改成一句 `rich_paragraph`——
  「零資料保留是 API 客戶層級的控制：OpenAI 承諾請求處理完不留提示與回覆，客戶內容也排除在預設最多留 30 天的濫用監控紀錄外；加上查核到 2026 年 9 月 23 日、資料控制表上 /v1/agents 仍不符資格（私密安全處理沒有改變這一格），這幾件事本站在〔OpenAI Agents API 公開 beta：委託 AI 自動化前，先看懂計費與資料位置〕都寫過了。」
  既有的 `article` inline 原封不動搬進這一句；第四節那段獨立段落刪除；第三段句尾的 30 天背景刪除。
- 做法說明：「預設」「最多」兩個限定詞留著（規格第 3 條：但書不可為字數而刪）。`must_not_write` 第 14 條仍成立——Agents API 全篇只被提到這一次並連過去。段數：第二節仍 3 段，第四節 4 段 → 3 段，兩者都在 2–4 內。
- 來源：<https://developers.openai.com/api/docs/guides/your-data>（`By default, abuse monitoring logs … retained for up to 30 days`、`/v1/agents  No  30 days  Until deleted  No  No`）

**R2（裁定 4）不符 ZDR 資格的端點清單補上 `/v1/videos`**

- before：`對話、討論串、向量庫、檔案與批次等端點列為不符合。`
- after：`對話、討論串、向量庫、檔案、批次與影片等端點列為不符合。`
- 今天的表上 `/v1/videos` 的「Zero Data Retention eligible」是 `No`（文件另寫 `v1/videos is currently blocked for MAM or ZDR requests`，正文沒有寫進去）。用的是裁定 1 空出來的字數。
- 來源：同上。

**R3（裁定 3）「美國時間」三處全部改掉**

- before：描述與 summary 第一條`（台北時間；OpenAI 頁面印的是美國時間 8 月 19 日）`；第一段`這一頁印的發布日期是美國時間 2026 年 8 月 19 日`。
- after：`（台北時間；OpenAI 頁面印的日期是 8 月 19 日）`；`這一頁印的發布日期是 2026 年 8 月 19 日`。
- 頁面逐字只印 `OpenAI August 19, 2026`，沒有任何時區字樣；時刻來自 RSS 的 `19:00:00 GMT`。改完之後全篇 grep「美國時間」為 **0 筆**，而 `must_not_write` 第 2 條仍成立：兩個日期都在（頁面印的 8 月 19 日、台北的 8 月 20 日凌晨 3 點），也說明了是時區差。描述長度 193 → **191**（120–200 內）。
- 來源：<https://openai.com/index/offering-zero-data-retention-for-frontier-models/>

### 第二輪自己抓到的

**R4（重）第一輪新寫進去的那一句把兩個收回條款混成一條，並刪掉一個關鍵但書**

- before：`…會事先書面通知；真的走到那一步，內容會改留在 OpenAI 的加密紀錄裡，後者還可能對疑似違規的內容做人工審閱。`
- after：`…會事先書面通知；走到這一步，前者是內容改留在 OpenAI 的加密濫用監控紀錄裡、但除非法律要求否則排除人工審閱，後者是在調查或預防重大風險有合理必要時，可能對分類器判定疑似違規的內容做人工審閱。`
- 文件是**兩條不同的條款、兩種不同的後果**：
  - `Private Retention with Private Safety Processing (fka Eyes Off)`：`customer content will be retained in encrypted abuse monitoring logs in OpenAI-managed infrastructure, **but such content will be excluded from human review unless required by applicable law**.`
  - `Safety Retention`：`… **if reasonably necessary to investigate or prevent severe risk activity**, as notified in advance … In this instance, we **may** retain and human review customer content when using these models that our classifiers detect as potentially violating our Usage Policies or your agreement.`
  第一輪的句子（a）整句刪掉了「除非法律要求否則**排除**人工審閱」這個但書，（b）用「後者」把人工審閱掛到「加密紀錄」上，讀起來變成私密保留那一條也會被人看，（c）漏掉安全性保留的觸發條件「調查或預防重大風險有合理必要時」。這是全篇「人員拿不到內容」在官方文件上唯一寫明的例外，寫反了代價很高。
- 來源：<https://developers.openai.com/api/docs/guides/your-data>

**R5 第五節第一段的否定句沒有跟著第一輪 C4／C5 一起限縮到「內文」**

- before：`公告與兩份開發者文件從頭到尾只談 API 客戶，沒有出現任何 ChatGPT 方案，也沒有出現台灣。`
- after：`公告與兩份開發者文件的內文從頭到尾只談 API 客戶，沒有出現任何 ChatGPT 方案，也沒有出現台灣。`
- 第一輪已經因為公告頁**頁尾導覽**逐字有 `ChatGPT Business`／`ChatGPT Enterprise`／`ChatGPT for Education`，把 summary、第二節與 FAQ1 三處限縮到「公告內文」，卻漏了這一處，而且這一處還多寫了「從頭到尾」。另外兩份開發者頁面的**左側導覽**各有 6 筆 `ChatGPT Work`（`.md` 版正文則是 0 筆），所以「兩份開發者文件」那一半也要一起限縮。
  附帶複核：FAQ1 的清單（Plus／Business／Enterprise／Edu）在兩份開發者頁面連導覽都是 0 筆，第一輪的 C5 寫法**正確，不需要再動**。
- 來源：<https://developers.openai.com/api/docs/guides/your-data>、<https://openai.com/index/offering-zero-data-retention-for-frontier-models/>

**R6 「四份來源都沒有價格」與來源相反（第一輪第 83 條判為確認）**

- before：`官方沒有寫 PSP 或 ZDR 是否收費、儲存空間成本由誰負擔，四份來源都沒有價格；`
- after：`官方沒有寫 PSP 或 ZDR 是否收費、儲存空間成本由誰負擔，四份來源都沒有為這兩項標價；`
- 資料控制文件的 `Data residency controls` 一節逐字印著 `Data residency endpoints are charged a **10% uplift** … for models released on or after March 5, 2026`，並連到官方 pricing 頁。那是資料落地的價格、不是 PSP／ZDR 的價格，但「四份來源都沒有價格」這種無範圍的否定句已經被來源推翻。窄化後的說法（這兩項沒標價）今天在四份來源裡都成立。
- 來源：<https://developers.openai.com/api/docs/guides/your-data>

## 4. 複核第一輪 14 處改動的結果

| 第一輪 | 判定 | 今天的依據 |
| --- | --- | --- |
| C1 標題 | **維持** | 頁面標題逐字 `Offering Zero Data Retention for frontier models`；內文 `Private Safety Processing is designed so we can continue to offer ZDR`、09-22 更新 `enables us to continue offering ZDR as frontier models become more capable`。四份來源沒有任何按模型列的 ZDR 資格表。「為前沿模型提供」對，「延伸到前沿模型」錯。 |
| C2 `may`（兩處） | **維持** | `some serious risks **may** only become visible across multiple interactions`（1 筆）。 |
| C3 `start` | **維持** | `We plan to **start** rolling out Private Safety Processing, and share a technical white paper, in September.`（1 筆）。 |
| C4「公告內文」（兩處） | **維持** | 頁尾導覽逐字有 `ChatGPT Business`／`ChatGPT Enterprise`／`ChatGPT for Education` 各 1 筆。（同一病灶第三處由 R5 補修。） |
| C5 FAQ1 | **維持，不再動** | 兩份開發者頁面（含導覽）`ChatGPT Plus`／`ChatGPT Business`／`ChatGPT Enterprise`／`ChatGPT for Education`／`ChatGPT Edu` 全部 0 筆。 |
| C6 地區（兩處） | **維持** | 資料落地表逐列有 `Japan`／`Singapore`／`South Korea` 等；`Taiwan` 在三份文件各 0 筆（只在 RSS 的別篇出現 1 次）。第一輪把「亞洲或任何特定地區」改成只講台灣是對的。 |
| C7 端點但書 | **維持** | `/v1/chat/completions`、`/v1/responses`、`/v1/images/generations`、`/v1/images/edits` 四格是 `Yes, see below for limitations`，只有 `/v1/embeddings` 是單獨的 `Yes`——「多數還註明另有限制」精確。 |
| C8 刪掉「只」 | **維持** | 原句 `Encrypted customer content is decrypted in an approved, hardware-attested safety runtime that disables human access.` 沒有 only；唯一性寫在 `is designed to be the only workload that can decrypt`（設計目標）。 |
| C9「加密分兩層」（兩處） | **維持** | `Each stored record is **doubly encrypted** when it is retained in customer storage`。 |
| C10「不論哪一種設定」 | **維持** | `even if Zero Data Retention, Modified Abuse Monitoring, or Private Retention with PSP is enabled`（文件）＋`even in Zero Data Retention deployments`（公告註腳）。 |
| C11 圖說「要另外開啟 EKM」 | **維持（裁定 5）** | `We recommend enabling EKM for this additional control.`；研究紀錄 `diagram.caption` 與第四格 `["客戶掌握金鑰", "要另開 EKM，授權可撤銷"]` 今天**沒有動**。 |
| C12 新寫的那一句 | **改（R4）** | 見上。 |
| C13 第一段歸因密度 | **維持** | 改完後開頭段仍只有 1 個歸因語（`OpenAI 表示`）。 |
| C14 第二段 | **維持** | 全篇「本文」「文中」「最近」「本週」「日前」「近日」各 0 筆；補寫理由那一句逐字照 `must_not_write` 第 1 條。 |

## 5. 隨機三分之一的確認條目（抽 33 條，每三條取一條）

抽到第一輪表格的 #2、5、8、11、14、17、21、24、28、31、34、37、41、45、48、51、55、58、61、64、68、72、76、80、84、87、89、92、96、99、102、105、107。
結果：**32 條維持確認，1 條（#45 ZDR 定義句）依裁定 1 從正文移除**；抽中的條目本身沒有一條被推翻。
但複核 #84 時順手讀了同一段的鄰句，才抓到第一輪判為確認的 #83「四份來源都沒有價格」與來源相反（R6）——
抽樣抓不到的錯，是靠把抽中句子的上下文一起讀完抓到的。其中值得記下來的：

- #64「Validated 只代表某次檢查通過、Refresh 不會重跑」：`**Validated** records a successful check, not continuous storage health. **Refresh** doesn't rerun validation.` 逐字成立。
- #80「四份來源沒有第三方稽核」：`audit` 只出現在兩份開發者頁面的導覽（`Compliance API and audit events`），`SOC 2`／`ISO 27001`／`certification`／`certified`／`independent assessor` 全部 0 筆。成立。
- #86「兩份開發者頁面都沒有印最後更新日」：`Last updated`／`Updated on` 今天仍是 0 筆。成立。
- #88 `/v1/agents` 那一列今天仍是 `No | 30 days | Until deleted | No | No`。成立（現在寫在第二節的那一句裡）。
- #89／#100 兩個結尾連結文字：用程式對目標內容包的 `zh-TW` `title` 逐字比對，**兩條都相同**。
- #102–105 四條 `sources[]` 今天全部 200 且讀到正文，`checked_on` 全是 2026-09-23。
- #107 `display_order` 181、`topics` `ai`／`software`／`ai-news`、`kind` `life`：成立。

## 6. 界線與讀者優先（規格第 3–5 條）

- 段落字數 **2,983 → 2,757**（1,800–3,000 內）。裁定 1 空出的 200 多字沒有拿去補寫，**沒有為了字數刪掉任何但書**（`up to`／`may`／`預設`／`最多`／`建議`／「除非法律要求」都在，R4 還補回一個）。
- 歸因密度：開頭段 1 個；正文 17 段裡最多的是 2 個（第一節第一段、第一節第三段、第二節第三段、第三節第一段、第四節第三段），全部在限內。廠商宣稱都有歸因。
- `summary` ⊆ 正文：五條的每個事實都在正文找得到（自檢的「summary 的數字必須出現在正文」也過）。FAQ 五題的答案 ⊆ 正文。圖解四格的數字（30 天）在正文。
- 範圍不明的否定句：改完後全篇的否定句都限縮到「公告內文／兩份開發者文件的內文」「四份來源」「查核到 2026 年 9 月 23 日」。
- 不帶 `finance` 主題、**只有一個 callout**、沒有投資免責段；沒有訂閱／購買／升級／投資建議；沒有推定台灣可用（只寫「沒有出現台灣」）。
- 沒有重寫站上既有的〈OpenAI Agents API 公開 beta〉，也沒有與它矛盾——裁定 1 之後，重疊的兩段背景改成一句指路句。
- 「業界首創」「唯一」「最安全」「從未」0 筆；沒有描述商標圖示或介面截圖；沒有抄任何 ARN、應用程式 ID、bucket 名稱或 curl 指令；沒有引述 Glean 資安長的推薦語。

## 7. 留給協調者的事

1. 第二節現在以一句「本站已經寫過」的指路句開頭（裁定 1 的結果）。那一句自己仍交代了三個事實，不點連結也不會漏掉；但若覺得一節以指路句開頭太像導流，把它移到第二節末尾即可，段數不受影響。
2. 正文只剩 2,757 字，還有 243 字空間沒用。可補而刻意沒補的只有兩樣：濫用監控 30 天的兩個但書（依裁定 1 歸給另一篇），以及 `/v1/videos` 連 ZDR 請求都被擋住的細節（研究紀錄 `verified_facts` 第 32 條）。
3. PSP 技術白皮書依裁定 2 不進 `sources[]`，正文一個字都沒寫。補一個今天發現的事實供日後參考：資料控制文件的 `Private Retention with PSP` 一節現在直接連到白皮書的 **第 35 頁（Appendix A）**，也就是白皮書已經是官方文件鏈的一部分；若日後要寫，仍須照研究紀錄的規定換掉一條 `sources[]`。
4. **圖還沒畫。** 第四格文字依裁定 5 維持「要另開 EKM，授權可撤銷」，圖說維持「（要另外開啟 EKM）」，構圖與 alt 請照這一格，不要畫成「金鑰完全由客戶掌握」。

## 8. 自檢輸出（原樣）

```
OK ai-news-openai-zero-data-retention-20260820 zh-TW paragraphs 2757
check_article exit=0
```

```
ai-news-openai-zero-data-retention-20260820
  error: image_missing: zh-TW: /guides/ai-news-openai-zero-data-retention-20260820/hero.jpg
  error: image_missing: zh-TW: /guides/ai-news-openai-zero-data-retention-20260820/diagram-1.svg
1 entries checked
pack_cli lint exit=1
```

兩條 `image_missing` 是預期內（圖還沒畫）；沒有 `raw_internal_url`。

## 9. 動過的檔案

1. `apps/api/app/guides/content/ai-news-openai-zero-data-retention-20260820.json`（R1–R6）
2. `docs/ai-news-2026-09-late/research/ai-news-openai-zero-data-retention-20260820.json`（只新增 `factcheck.second_round`；`title`、`diagram`、`sources`、`verified_facts` 都沒有動）
3. 本報告

沒有 `git add`／`commit`，repo 裡沒有留下暫存檔（腳本與抓下來的原始檔都在
`C:\Users\x8120\mokaair-work\news44\_tools\ai-news-openai-zero-data-retention-20260820-r2\`）。

## 10. 結論

`ok`。第二輪再改 6 處，其中 R4 是把第一輪新寫的句子改正（漏掉「除非法律要求否則排除人工審閱」這個但書並混用兩個條款），
R5、R6 是把兩條範圍過寬的否定句收回來。標題、`sources[]`、`checked_on`、圖說與圖解節點都沒有再動。
剩下的只有兩張圖要畫。
