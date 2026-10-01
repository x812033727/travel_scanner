# 查核報告（第二輪）：ai-news-claude-sonnet-55-20260928

## 第二輪

- 查核者：獨立查核代理（第二輪，opus），2026-09-30（台北）；沒有參與研究、撰稿與第一輪。
- 規格：`agents/ai/SECOND-ROUND.md`、`agents/ai/FACTCHECK.md`（Windows 路徑不適用）、`DELTA-4-10.md`、`DELTA-4-9.md`、`DELTA-4-7.md` 第 11–14 條、`BRIEF.md` 最後一節、`ai.md`，以及協調者指派訊息點名的疑點。
- 改動的檔案：內容包 `apps/api/app/guides/content/ai-news-claude-sonnet-55-20260928.json`（11 處）、研究紀錄 `docs/ai-news-2026-09-late/research/ai-news-claude-sonnet-55-20260928.json`（5 處，另加 `factcheck.second_round`）。round1 報告沒有動。
- 暫存：`/root/news49/s55/agents/fc2/`（`s1.bin`–`s4.bin` 原始回應、`norm.py` 正規化、`s3.txt`／`s3.W.txt` PDF 抽字、`vq.py` 引文比對、`edit_pack.py`／`edit_research.py`／`add_sr.py` 改稿腳本、`check0.log`（改前）／`check.log`（改後））。

### 重抓結果（2026-09-30 UTC 11:52）

UA `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`，`curl -sSL --compressed`，同一主機間隔 1.2 秒；請求沒有任何人的姓名、email 或個資。

| 網址 | HTTP | 落地 bytes | 正文？ |
| --- | --- | --- | --- |
| https://www.anthropic.com/claude-sonnet-5-5 | 200，0 次轉址 | 430,222 | 是（導言、評測表與四個註腳、價格表、Safety、Getting started） |
| https://platform.claude.com/docs/en/models/sonnet-5-5/overview | 200，0 | 429,120 | 是（規格卡、五項破壞性變更、Model IDs、Pricing、Availability） |
| https://www.anthropic.com/claude-sonnet-5-5-system-card | 200，2 次轉址到 `www-cdn.anthropic.com/870c8f52…/Claude%20Sonnet%205.5%20System%20Card.pdf` | 13,101,289 | 是（148 頁，pdfenv 的 pypdf 抽字） |
| https://www.anthropic.com/claude/sonnet | 200，0 | 405,412 | 是（Announcements、Availability and pricing） |

### `verbatim_quote` 比對

HTML 刪註解與 script／style／noscript／svg／template 後做三種正規化（行內標籤→無、所有標籤→空格、所有標籤→無）加 RAW，全部 `html.unescape`、收斂空白、NBSP 與 U+2011 正規化；PDF 用空白收斂版與 ﬁ／ﬂ 連字還原版。**45/45 連續字串通過**：原本 44 條，加上第二輪新增 1 條（System Card §3.3）。沒有含 `...`、`…` 或 `|` 的引文；所有 `url` 都在 `sources[]`。

引文雖然都對得上，但有三條的 `fact` 文字比引文強，已改（見下方研究紀錄改動）。

### 查過的主張（約 62 條）

範圍是第一輪改過的段落、第一輪新寫的句子、summary、FAQ、表格與 caption、圖解 caption、nodes、hero_label、title、description，以及所有 30%、否定句、歸因句。來源代號：A＝公告、M＝模型頁、S＝System Card、P＝產品頁。

第一輪點名的新句子：

| 位置 | 主張 | 判定 | 原文 |
| --- | --- | --- | --- |
| 第 1 段 | 每任務成本比前一代「最多少 30%」，Anthropic 測試量到的，不是牌價調降 | CONFIRMED | A `In our testing, it costs up to 30% less per task than its predecessor.` |
| 第 1 段 | 同家族還有 Opus 5.5 | CONFIRMED | A `the second model in the Claude 5.5 family`、`complement to Claude Opus 5.5` |
| 第 1 節第 2 段 | 公告另寫，較高風險的資安任務會退回 Sonnet 5 | CONFIRMED | A `higher-risk cybersecurity tasks will visibly fall back to Sonnet 5` |
| 第 1 節第 2 段 | 退役日「不早於 2027 年 9 月 28 日」是承諾 | CONFIRMED | M `Retirement Not sooner than September 28, 2027`；M 連結說明 `retirement commitments` |
| 第 2 節第 1 段 | 公告明寫相同的是輸入、輸出、快取讀取三項 | CONFIRMED | A `priced the same as Sonnet 5 at $2 … $10 … and $0.20 per million tokens for cache reads` |
| 第 2 節第 2 段 | 產品頁：對以 token 計費的一般工作負載，估計最多少 30% | CONFIRMED | P `up to an estimated 30% less to run than Sonnet 5 for typical workloads billed by token` |
| 第 2 節第 3 段 | 提示快取最多省 90%、批次省 50%；美國境內工作負載 US-only 1.1 倍 | CONFIRMED | P |
| 表格 | $2／$10／$0.20（A、M）；5 分鐘快取寫入 $2.50（M；A 寫 `Cache writes $2.50`）；1 小時 $4（M）；Batch 輸入與輸出五折（M `50% discount on input and output`） | CONFIRMED（逐格） | A 價格表、M Pricing |
| 表格 caption | 依公告價格表與模型頁、查核日、相同的三項 | CONFIRMED | A、M |
| 第 4 節 FrontierCode 註腳 | Max 較常跑程式審查技能，在 Cognition 檢視的兩個案例裡導致逾時或改到範圍外 | CONFIRMED | A 註 2 `in two cases Cognition examined, this led to a timeout or to extra edits beyond the task's scope` |
| 第 4 節 GDPval 註腳 | 上市前部署有可能影響結構化輸出的 bug，現已修正 | **CHANGED**（補「Anthropic 發現」，「影響」→「讓…回應變差」） | A 註 3 `which we found to have a bug that could degrade responses to requests that use structured outputs … That bug has since been fixed.` |
| 第 5 節第 3 段 | 退回適用自家產品與 API 選擇啟用的開發者；其他平台與供應商可能不同 | CONFIRMED | S §1.5 |

其他逐句回來源後 CONFIRMED 的：title、description、summary 1／3／4／5、第 2 段、第 1 節第 1、3 段、第 3 節三段（產品頁 Anyone can chat、公告 all platforms including AWS／Google Cloud／Microsoft Azure、模型頁五平台與 Model IDs、1M／128K／Jun 2026、effort 預設 Medium／High）、第 4 節第 1 段各分數與註 1、第 5 節第 1、2 段（RSP、CB-1／Autonomy-1、CB-2／Autonomy-2、失準風險低、提示注入 `particularly in coding environments and browser use`、電腦操作拒絕率）、FAQ 1／3／5／6、callout、圖解 caption、四格 nodes、hero_label。詞界計數：`Taiwan` 四頁 0 次；`retire` 只在 M（2 次，Sonnet 5.5 自己的 Retirement 與導覽）；`deprecat` M 2 次（導覽）、S 3 次（模型福祉章節）；`Haiku 5.5` 只在 A 1 次。

### 改掉的地方

內容包 11 處：

1. **第 5 節第 3 段**：刪「所以比照 Opus 5.5 部署類似的防護」。四處寫法不一致：A `safeguards similar to those on Opus 5.5`；S 摘要 `three-stage cyber safeguards are applied to Sonnet 5.5, as they are to Opus 5.5`；S §1.5 `similar blocking classifiers to those on Opus 5`；S §3.3 `cyber safeguards that enforce the same policy as on Claude Opus 5 and Claude Opus 5.5`。照協調者裁定，正文不挑一個當事實，所以不寫比照哪一代。
2. **同段**：補 S §3.3 `users should expect increased refusals with Sonnet 5.5, even on benign cybersecurity-related tasks` →「System Card 提醒，使用者應預期拒絕會變多，即使是無害的資安相關任務也一樣」。原段只有公告的「一般找 bug、修 bug 不受影響」，讀者會以為資安相關的一般請求都不受影響。研究紀錄新增一條 verified_fact 撐這句。
3. **FAQ 4**：「比照 Opus 5.5 部署類似的資安防護」→「是第一個帶資安防護與備援上線的 Sonnet 模型」（A `the first Sonnet model to launch with cyber safeguards and fallbacks`），理由同第 1 處。
4. **第 3 節第 1 段**：「這些官方未說明」→「這幾頁在查核日都沒有說明」（否定句限縮）。
5. **FAQ 2**：同上。
6. **第 1 節第 2 段**：「公告、模型頁與產品頁都沒有寫 Sonnet 5 何時停用」前加「截至查核日」。
7. **summary 1**：「這幾頁沒有寫 Sonnet 5 何時停用」前加「截至查核日」。
8. **summary 2**：「那是 Anthropic 自己測試的說法」→「這是 Anthropic 的說法」。A 的 `typically needs far fewer tokens to do the same work` 沒有說是測試結果。
9. **第 2 節第 1 段**：補「並表示它做同樣的工作通常需要少得多的 tokens」。summary 2 的這句原本不在正文（summary ⊆ 正文）。
10. **第 4 節第 3 段**：「在 Anthropic 與外部測試者的使用中」→「在 Anthropic 自己與外部測試者的測試中」（A `in our own testing, and in that of external testers`）。
11. **第 4 節第 2 段 GDPval 註腳**：見上表；**第 2 節小標**「牌價沒變，變的是每個任務的用量」→「牌價沒變，Anthropic 說變的是每個任務的用量」（「用量變少」是 Anthropic 的宣稱，小標原本沒有歸因）。第 11 處算兩個位置、同一種修正。

研究紀錄 5 處：

- `verified_facts[1]`：刪掉 fact 文字裡沒有來源的「第一個是 9 月 22 日的 Opus 5.5」（第一輪只改了正文）。
- `verified_facts[11]`：「使用中」→「測試中」。
- `verified_facts[18]`：刪「所以比照 Opus 5.5 部署類似的防護」當事實的寫法，改成記下四處不一致。
- `must_not_write`：原本「資安防護照公告寫『比照 Opus 5.5 的類似防護』」與協調者裁定衝突，改成「不寫比照哪一代；要寫就四處並列並寫出處」。
- `verified_facts` 新增第 45 條（S §3.3 拒絕變多）。另加 `factcheck.second_round`。

title、image caption 都沒改，所以 `title`、`diagram.caption` 不必同步。

### 刪但書回掃

逐一比對第一輪與研究紀錄的限定詞：`up to`（四處 30% 都是「最多」、90% 是「最多可省」）、`estimated … for typical workloads billed by token`、`30%+`（「30% 以上」）、`in two cases Cognition examined`、`could`、`particularly in coding environments and browser use`、`may experience different behavior`、`in the coming weeks`、`Not sooner than`，都還在。沒有發現為了字數刪掉的但書或歸因。這一輪加了字，段落從 2,857 變成 2,925（上限 3,000）。

### ⊆ 檢查

- summary 五點：數字（2、10、0.20、70.6%、10.3%）與敘述都在正文；第 2 點的 tokens 那句原本不在正文，已補（第 9 處）。
- FAQ 六題：答案都在正文。FAQ 4 改寫後的句子在第 5 節第 3 段。
- 圖解：nodes 沒有數字；hero_label「同價新一版 Sonnet」、圖解 caption 都在正文撐得住。title 與 description 的數字（2、10）在正文。

### 界線

- 購買建議、「該不該換」：沒有。第 2 段與 callout 都寫「不提供／不是換模型或訂閱的建議」。
- 台灣：沒有推定可用，也沒有推定不可用（「這幾頁沒有提到台灣，也沒有列出開放或限制的地區」）。
- OpenAI／GPT：內容包 0 次。評測只列 Sonnet 5.5／Sonnet 5／Opus 5.5 三欄，公告表的 GPT-6 Sol 欄與成本圖的 GPT 比較都沒有搬進來。
- 攻擊細節：沒有。
- 清點數字：title、summary、圖都沒有來源沒印的清點（「三家」第一輪已刪）。
- callout：只有一個 info callout；topics 沒有 finance；「本文」0 次；ASL 0 次。
- Azure／Foundry：第 3 節第 2 段公告寫 Microsoft Azure、模型頁寫 Microsoft Foundry，各自掛各自的來源；summary 3 只用模型頁的清單。
- 安全分級：照 S 原文（沒有跨過新的 RSP 門檻；Opus 5.5 未跨 CB-2／Autonomy-2 的判定同樣適用；當作已達 CB-1／Autonomy-1 並套用對應緩解），沒有 ASL。

### 留給站主的事

1. 資安防護比照哪一代，四處說法不一致（A、S 摘要寫 Opus 5.5；S §1.5 寫 Opus 5；S §3.3 寫 Opus 5 與 Opus 5.5 同一套政策）。文章現在不寫。若 Anthropic 修訂 System Card，可以再決定要不要寫。生物防護同樣不一致（A 寫同 Sonnet 5，S 寫同 Opus 5），文章也不提。
2. 延續第一輪：產品頁頁首與 FAQ 落後（活頁面）；Sonnet 5 的退役承諾與快取寫入、Batch 是否同價不在 `sources[]`；模型頁 Platforms 的 Amazon Bedrock 要在發布當天重讀。
3. 圖解 SVG 仍待協調者跑 `--assets`；nodes 這一輪沒有改。

### 自檢

```
exit 0
OK ai-news-claude-sonnet-55-20260928 zh-TW paragraphs 2925
```

### 結論

`ok`：這一輪改了 11 處。沒有改到骨幹論述，只在 System Card 前後不一致的地方拿掉一個挑邊的說法、補回一句但書。
