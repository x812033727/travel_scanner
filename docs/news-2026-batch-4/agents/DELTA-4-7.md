# 批次 4.7（2026-09-20 起的新聞，只做 zh-TW）：對既有規格的差異

批次 4.7 沿用 4.1～4.3 的代理規格（`agents/`＝幣圈、`agents/tech/`＝科技、`agents/ai/`＝AI）與
[`DELTA-4-5.md`](DELTA-4-5.md)、[`DELTA-4-6.md`](DELTA-4-6.md) 的全部規則；只有下面幾件事不同或要再說一次。
**這份文件的規則優先於各垂直規格、DELTA-4-5 與 DELTA-4-6 裡與它衝突的句子。**

1. **窗口是 2026-09-20 00:00 台北（2026-09-19T16:00Z）起的新聞，另加三則站主點名的補寫件。**
   三位探索代理掃到 2026-09-22T15:33–15:44Z（台北 9/22 23:33–23:44），候選清單在
   [`../candidates-since-0920-ai.md`](../candidates-since-0920-ai.md)、
   [`../candidates-since-0920-tech.md`](../candidates-since-0920-tech.md)、
   [`../candidates-since-0920-crypto.md`](../candidates-since-0920-crypto.md)（原樣搬進 repo，未改字）。
   站主圈選 15 篇，其中**三則的事件日在窗口外**，是前幾輪列過卻一直沒寫的補寫件，不是本輪的新消息：
   Anthropic 生命科學驗證方案（09-17）、Meta One（09-15）、財政部台財稅字第 11504611390 號令（09-03）。
   這三則的正文不可寫成「最近」「本週」，要照事件日寫，並交代為什麼現在才整理（來源當時讀不到／上一輪額度已滿，擇其一，依研究紀錄）。

2. **只做 zh-TW。** 站主 2026-09-20 決定。內容包 `locales` 只有 `zh-TW`；研究紀錄**沒有** `translations` 欄位；
   沒有翻譯、沒有逐語審稿階段。規格裡凡是「翻譯代理」「逐語審稿」「hero_label 的五語」「圖檔五語」的段落一律跳過；
   圖檔只出 zh-TW 一份。**自檢一律不帶 `--full`**：`check_article.py <slug>`（出圖後 `check_article.py <slug> --assets`）。
   `--full` 只多加四個翻譯的檢查（腳本文件字串第 3–4 行），對 zh-TW-only 文章必然 FAIL，且不帶它不會漏掉任何 zh-TW 原文與研究紀錄的檢查。

3. **研究紀錄由專責的研究代理寫，不是探索代理。** 探索代理只交候選清單（站主圈選用）；圈選後每個 slug 一位 opus 研究代理，
   照 4.5 的 schema（範例 `docs/ai-news-2026-09-late/research/ai-news-anthropic-pace-metrics-20260917.json`）寫成 JSON。
   最終版放在各垂直工作區（同 DELTA-4-5 第 7 條）：AI `docs/ai-news-2026-09-late/research/`、
   科技 `docs/tech-news-2026/research/`、幣圈 `docs/crypto-news-2026/research/`。那一份對撰稿與查核**都有拘束力**：
   `must_not_write`、`not_said`、`unverified_or_excluded`、`live_data_warnings`、`sources[]` 照 4.3／4.5 的規則處理。
   本批有一份**前期研究紀錄可以起手**：`docs/news-2026-batch-4/research/tech-news-moda-mydata-student-loan-20260917.json`
   （`sourcing_verdict: partial`，只有 moda 新聞稿與 MyData 首頁兩條）；研究代理要把它當草稿讀，不是當定稿抄。

4. **沒有前期修正清單**（同 4.5 第 1 條、4.6 第 3 條）：`corrections_applied` 寫 `[]`。

5. **`display_order` 照下表**，由 `check_article.py` 的 `RELATED` 順序決定（已經寫進去了，不要再動順序）：
   AI 接 **171** 起、科技接 **321** 起、幣圈接 **217** 起。
   **這張表的順序是站主圈選的順序，不是候選清單自己提的號碼**——科技的 Petal 與 ENISA 因此與
   `candidates-since-0920-tech.md` 寫的 325／324 對調。slug 沿用候選清單提的那一個；候選清單沒提的（三則補寫件）在這裡定。

   | 垂直 | slug | display_order | 事件日（台北） |
   | --- | --- | --- | --- |
   | AI | `ai-news-openai-math-advisory-20260921` | 171 | 2026-09-21 |
   | AI | `ai-news-openai-frontier-standards-20260921` | 172 | 2026-09-21 |
   | AI | `ai-news-anthropic-life-sciences-verification-20260917` | 173 | 2026-09-17 |
   | AI | `ai-news-meta-one-subscription-20260915` | 174 | 2026-09-15 |
   | AI | `ai-news-openai-academy-paths-20260921` | 175 | 2026-09-21 |
   | AI | `ai-news-nvidia-physical-ai-safety-20260921` | 176 | 2026-09-21 |
   | 科技 | `tech-news-googlebook-launch-20260921` | 321 | 2026-09-21 |
   | 科技 | `tech-news-eu-data-centre-rating-20260921` | 322 | 2026-09-21 |
   | 科技 | `tech-news-cisa-kev-zyxel-gs1900-20260921` | 323 | 2026-09-21 |
   | 科技 | `tech-news-meta-petal-subsea-cable-20260921` | 324 | 2026-09-21 |
   | 科技 | `tech-news-enisa-threat-landscape-20260922` | 325 | 2026-09-22 |
   | 科技 | `tech-news-moda-mydata-student-loan-20260917` | 326 | 2026-09-17 |
   | 幣圈 | `crypto-news-taiwan-deposit-token-pilot-20260922` | 217 | 2026-09-22 |
   | 幣圈 | `crypto-news-sec-innovation-exemption-20260917` | 218 | 2026-09-17 |
   | 幣圈 | `crypto-news-taiwan-vasp-tax-ruling-20260903` | 219 | 2026-09-03 |

   **Googlebook 只寫一篇，寫在科技垂直**（`tech-news-googlebook-launch-20260921`）。候選清單把它同時列進 AI 與科技並請協調者裁定；
   站主已裁定：**AI 垂直不寫 Googlebook**。同日三篇官方文（預購、內建智慧、外觀設計）與 5 月的發表文都進同一篇的 `sources[]`，
   Magic Pointer／Rambler 這些 Gemini 功能由科技這一篇一起交代，不另開 AI 篇。

6. **第一個結尾連結**：索引標題**不改**，逐字照抄（同 DELTA-4-5 第 3 條、DELTA-4-6 第 5 條）：
   - AI：`2026 年 AI 新聞總整理：1 月至 9 月的重點與生活應用` → `https://mokaair.com/zh-TW/life/ai-news-2026-january-september-index`
   - 科技：`2026 年科技新聞總整理：硬體、平台、電信與法規的重點` → `https://mokaair.com/zh-TW/life/tech-news-2026-index`
   - 幣圈：`2026 年加密貨幣新聞總整理：法規、技術與產業的重點` → `https://mokaair.com/zh-TW/life/crypto-news-2026-index`

7. **第二個結尾連結**指向下表那篇**既有已發布**文章（**不是同批在寫的文章**）。
   text 逐字照抄下表的標題——那是該內容包現行的 zh-TW `title`，一個字都不要改寫、不要補前後綴；
   網址是 `https://mokaair.com/zh-TW/life/<目標 slug>`。`check_article.py` 對它不應有 FAIL。

   | 本批 slug | 第二個連結的目標 | text（逐字） |
   | --- | --- | --- |
   | `ai-news-openai-math-advisory-20260921` | `ai-news-pace-the-frontier-20260912` | Amodei 呼籲放慢前沿 AI：〈We Must Pace the Frontier〉的主張與界線 |
   | `ai-news-openai-frontier-standards-20260921` | `ai-news-openai-misalignment-reports-20260917` | OpenAI 公布失準通報框架：6 份報告都出自訓練階段 |
   | `ai-news-anthropic-life-sciences-verification-20260917` | `ai-news-anthropic-threat-report-20260910` | Anthropic 九月威脅情報報告：七類 AI 濫用與被盯上的 API 金鑰 |
   | `ai-news-meta-one-subscription-20260915` | `ai-news-meta-muse-spark-20260408` | Meta Muse Spark 登場：社群裡的 AI 助手如何改變搜尋與提問？ |
   | `ai-news-openai-academy-paths-20260921` | `ai-news-chatgpt-work-20260709` | ChatGPT Work 正式亮相：如何把跨檔案工作交代清楚？ |
   | `ai-news-nvidia-physical-ai-safety-20260921` | `ai-news-frontier-governance-20260528` | OpenAI 前沿治理框架公開：50 人、10 億美元門檻怎麼來、誰追得到 |
   | `tech-news-googlebook-launch-20260921` | `tech-news-windows-project-zenith-20260904` | 微軟發布 Project Zenith：Windows 開發機的統一記憶體與頻寬門檻 |
   | `tech-news-eu-data-centre-rating-20260921` | `tech-news-eu-cra-reporting-20260911` | 歐盟《網路韌性法》通報義務上路：9 月 11 日起，誰要多快通報 |
   | `tech-news-cisa-kev-zyxel-gs1900-20260921` | `tech-news-cisa-kev-linux-kernel-20260918` | CISA 同一天兩則公告：三個 Linux 核心漏洞列入「已遭利用」清單 |
   | `tech-news-meta-petal-subsea-cable-20260921` | `tech-news-taiwan-matsu-cable-tm4-20260918` | 中華電信宣布臺馬第四海纜完工：近 14 億元、三路由備援與 1.9 Tbps |
   | `tech-news-enisa-threat-landscape-20260922` | `tech-news-cisa-kev-linux-kernel-20260918` | CISA 同一天兩則公告：三個 Linux 核心漏洞列入「已遭利用」清單 |
   | `tech-news-moda-mydata-student-loan-20260917` | `tech-news-taiwan-sovereign-ai-corpus-20260915` | 臺灣主權 AI 訓練語料庫啟動民間語料徵集：授權條款與客語語料現況 |
   | `crypto-news-taiwan-deposit-token-pilot-20260922` | `crypto-news-genius-act-occ-20260302` | 美國 OCC 穩定幣發行規則草案：一比一準備金、兩個營業日贖回與定期申報 |
   | `crypto-news-sec-innovation-exemption-20260917` | `crypto-news-sec-regulation-crypto-assets-20260821` | SEC 提出 Regulation Crypto Assets 草案：兩項募集豁免與一個安全港，尚未定案 |
   | `crypto-news-taiwan-vasp-tax-ruling-20260903` | `crypto-news-taiwan-vasp-act-20260630` | 虛擬資產服務法三讀通過：七種服務商、穩定幣許可與仍未定的施行日 |

   兩篇科技文指向同一個目標（Zyxel 與 ENISA 都連 CISA 那篇）是刻意的：一篇談同一個機制的下一個案例，
   一篇談「為什麼漏洞修補的優先序比買設備重要」，兩邊都會用到它。`RELATED` 允許多對一。
   目標裡有兩篇是 4.6 的 zh-TW-only 文章（`tech-news-cisa-kev-linux-kernel-20260918`），這在本批沒有問題——
   本批不跑 `--full`，不會去比對四個譯文的標題。

8. **索引由協調者在同一個 PR 補，撰稿代理不要碰索引。**
   三個索引文章（`ai-news-2026-january-september-index`、`tech-news-2026-index`、`crypto-news-2026-index`）
   的標題**不改**；15 個連結由協調者跑
   `python update_index.py ai tech crypto --locale=zh-TW`（先 `--dry-run` 看 diff）加進去，
   **只動 zh-TW 文件，en／ja／ko／zh-CN 一個位元組都不動**。`CITED` 對本批維持全空
   （AI 索引已引 19／20 條、科技 17 條，而且單邊加來源會讓五語文件的來源清單不一致）。
   4.6 是把索引拆成另一張票才補的；本批**不拆**，索引與 15 篇同一個 PR。

9. **本批沒有「更新既有五語文章」。** 候選清單列了三則「改維護票」的項目
   （Mac mini／Mac Studio 上市日 → `tech-news-apple-m6-m5-ultra-20260825`、NVIDIA DSX Ready → `tech-news-nvidia-vera-rubin-20260915`、
   主權 AI 語料庫 22 億 Tokens → `tech-news-taiwan-sovereign-ai-corpus-20260915`），以及 FDIC 併購草案 Question 60
   → `crypto-news-fdic-genius-act-20260410`。**這四則本批一律不做**：4.6 已經證明五語系、zh-TW 已頂 3,000 字、
   `sources` 已四條的文章加一節會與 checker 互斥（見 4.6 票的 Notes）。要做就另開票，不要塞進本批的 PR。

10. **事件日與查核日**同 DELTA-4-5 第 5、6 條（台北時間；slug 後綴、`news_date`、正文第一段三者一致），
    `checked_on` 寫你**實際重抓來源那一天**。已裁決的四件事照抄、不要重新推導：

    - **佔位時刻不換算**（沿用 OpenAI `00:00` 與 4.6 第 7 條 Accenture `16:00` 的判例）：
      `ai-news-nvidia-physical-ai-safety-20260921` 的頁面時刻 `16:00`（台北 9/22 00:00）是整點排程佔位，
      **事件日維持 2026-09-21**，不可換算成 9/22。
    - **`ai-news-meta-one-subscription-20260915`**：JSON-LD `datePublished` 2026-09-15T15:00:59Z（台北 9/15 23:00）是事件日；
      `dateModified` 2026-09-16T20:22:09Z **不是**事件日。若正文用到 9/16 更新後才有的內容，要在正文寫明「9 月 16 日更新」並歸因，
      但 slug 與 `news_date` 一律 **2026-09-15**。
    - **`crypto-news-sec-innovation-exemption-20260917`**：命令的署期與豁免效期起算日都是 **2026-09-17**，那是事件日；
      **9/22 刊登聯邦公報（91 FR 60168–60184）是「現在可以寫了」的觸發，不是事件**。第一段照事件日寫 9/17，
      並在同段或第二段交代「9 月 22 日刊登聯邦公報後全文才讀得到」。
    - **`crypto-news-taiwan-vasp-tax-ruling-20260903`** 的事件日是行政院公報刊登日 **2026-09-03**（032 卷 164 期）。
      台灣主管機關頁面印的日期本來就是台北時間，不換算。

11. **網路請求**同 DELTA-4-5 第 9 條、DELTA-4-6 第 9 條，再加本輪探索踩到的幾條：

    - UA 一律 `curl -sSL -A 'Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)'`，同一主機間隔 ≥1 秒。
      **任何請求的 UA、標頭、查詢字串、表單、筆記都不得帶入任何人的姓名、email 或個人資料。**
    - **不要猜網址或 API 路徑。**「回 200、bytes 很大」不等於讀到了：軟性 404、維護頁、SPA 殼都會這樣。
      判準是**項目數與最新一筆的日期**，不是狀態碼。
    - `openai.com/index/*` 的 403 是**間歇性**的（本輪五篇一次全過）。被擋要現場重測，不要沿用舊紀錄，不要用 Wayback；
      讀不到就換 `cdn.openai.com`／`developers.openai.com`／對方公司的稿。
    - `sec.gov` 的 HTML **可能** 403（上一輪四種組合全擋、本輪一次就過）。擋住時走
      新聞稿／聲明／演講 RSS、聯邦公報全文 `federalregister.gov/documents/full_text/text/<YYYY>/<MM>/<DD>/<doc>.txt`、或 govinfo 的 PDF。
    - **NCC 官網是 Angular SPA**，舊 `news.aspx` 失效、API 的 folder id 在 bundle 裡找不到。改走行政院公報
      `gazette.nat.gov.tw`，而且**要帶 cookie jar**（先打首頁 `-c`，之後 `-b`）——不帶的話每個日期都回最新一期；
      進階查詢要重複三組 `keywords`／`fields`／`logics`，否則回 500。本輪逐筆看過 09-21、09-22 兩期共 48 筆，沒有 NCC 項目，
      寫法一律是「**NCC 新聞稿未查到**」，不是「NCC 沒有發布」。
    - **歐盟 press corner 的網頁會轉址到外殼**（本輪 22,157 bytes 的導覽殼），全文要用**列印 PDF 端點**取得。
    - **`blog.google` 的文章帶一塊「Read AI-generated summary」**，一律跳過：Googlebook 那篇的摘要寫
      「shipping to select countries beginning October 4」，正文寫的是 10/4 美國、10/5 加拿大／英國／愛爾蘭／法國／德國／澳洲——
      **抄摘要會漏掉「台灣不在名單上」這個對讀者最重要的事實。**
      另外 `blog.google/android/rss/`、`/chrome/rss/`、`/pixel/rss/` 三個子站 feed 現在都是軟性 404，改用 `/rss/` 與 `/products-and-platforms/rss/`。
    - **Apple 的頁面帶 NBSP 與 U+2011（不斷行連字號）**，逐字引用前要正規化，不要把 U+2011 原樣搬進內容包。
    - **兩個「會騙人的零」**（本輪幣圈探索的發現，兩個都會安靜地把整條線索掃成空白）：
      1. **金管會 `news_list.jsp` 的關鍵字查詢會回 0 筆**——虛擬資產／穩定幣／虛擬通貨／加密資產四個詞全部 0 筆、
         回 200、bytes 幾乎相同、沒有錯誤訊息，上一輪同一管道「虛擬資產」還有 30 筆。
         **改用不帶關鍵字的列表（`pagesize=60`）按日期逐日核對**；本輪的存款代幣試辦只有這條路徑找得到。
      2. **聯邦公報 API 的 SEC 機關代號必須是 `securities-and-exchange-commission`**；
         `securities-exchange-commission` 回 400 `{"errors":{"agencies":"invalid value"}}`，**會把 SEC 整個機關掃成空白**。
    - **MAS（`/news` 整份是維護頁）、SFC（軟性 404）、Qwen（純 SPA 殼，可取文字 4 字元）、DeepSeek（軟性 404 回文件頁）
      一律寫「讀不到」**，不可寫成「沒有發布」，也不可當成否定句的依據。

12. **查核報告要進 repo**（恢復 4.1–4.5 的做法；4.6 沒做）：每一篇的查核報告寫成
    `docs/news-2026-batch-4/factcheck-draft/<slug>.md`，兩輪各一節（第二輪那節標題寫「第二輪」），
    與內容包同一個 PR 提交。第二輪照 `agents/SECOND-ROUND.md`（AI 用 `agents/ai/SECOND-ROUND.md`、科技用 `agents/tech/SECOND-ROUND.md`）：
    **逐句回一手來源**，特別是第一輪自己新寫進去、沒有人查過的句子。4.6 十一篇兩輪合計改了 327 處，第二輪不能省。

13. **工具與環境（4.6 的教訓，照做就好）**：

    - `cmd | tail` 會把 lint／checker 的失敗吃掉。**每個檢查都導到 log 檔並印出 exit code**，不要用管線接 `&&`。
    - FAIL 訊息含中文，Windows 上要 `PYTHONIOENCODING=utf-8`，否則 `UnicodeEncodeError` 會蓋掉真正的錯誤。
    - **表格 `caption` ≤ 200 字、`description` 120–200 字**（`apply_corrections.py` 超過欄位上限時會整筆 `SKIPPED`，要看那一行）。
    - **改內容包用文字插入，不要 `json.dump`**——`json.dump` 會把表格陣列展開成多行，整份 diff 沒法看。
    - Python 用 `apps/api/.venv/Scripts/python.exe`；多個代理同時跑**不要用 `uv run`**（搶鎖）。`pypdf` 在系統 `python`，不在 venv。
    - 重跑 `build_assets.py` 不會動到沒改字的 JPG；`git status` 裡一整排 SVG「修改」只是工作樹的 CRLF，`git add` 後就消失。

14. **讀者優先的新聞寫法**（站主 2026-09-21 對美食特輯的退稿意見，同樣適用新聞）：

    - **正文不要出現「本文」。** 規格裡「本文於 2026 年 M 月 D 日查核」那句改寫成
      「這一篇的資料在 2026 年 M 月 D 日查核」這類直接說話的句子（日期照你自己的 `checked_on`）；callout 同理。
      指涉自己用「這一篇」，不用「本文」。
    - **查證紀律不要寫進正文。** 讀者要知道的是「這件事是什麼、現在什麼狀態、管到誰、跟我有什麼關係、怎麼自己去官方頁查」；
      「我們讀了官方頁」「官方表示」不是內容。歸因該做，但不要每一句都掛一次「官方」——
      22 篇韓國美食特輯出現了 989 次「官方」就是這樣被退的。
    - **`description` 不寫查證流水帳**，最多在句尾帶一個「（2026 年 9 月查證）」，不要寫成「本文於……查核，讀了……」。
    - 第一段就要讓讀者知道跟自己有沒有關係（台灣在不在名單上、什麼時候輪到台灣、現在能不能用）。

15. **每一篇都要有一張圖。** `build_assets.py` 的 `_DRAWINGS` 現在**沒有**本批任何一個 slug——
    本次規劃刻意不加，因為構圖要照文章最後定稿的數字畫。撰稿定稿後由撰稿代理或協調者替每個 slug 加一個繪圖函式並登記進 `_DRAWINGS`，
    然後才跑 `check_article.py <slug> --assets`。沒加就會直接 `SystemExit: no drawing for <slug>; add one to _DRAWINGS in build_assets.py`。
    圖上的數字不可以比正文強，也不可以出現來源沒印的清點數字（同 HANDOVER 第 3 節）。

16. **幣圈固定免責 callout 逐字照 `crypto.md` 樣板，含「本文」二字**（協調者 2026-09-23 裁決）。第 14 條的「不寫本文」不及於這個 callout：它與已發布的幣圈文章逐字相同、只換查核日，撰稿與查核都不得改寫。正文其餘任何地方仍不得出現「本文」。
