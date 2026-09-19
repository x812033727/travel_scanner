# 獨立查核：ai-workflow-model-routing-cascade

查核代理：未參與撰稿。查核日 **2026-09-19**（文章的 `checked_on` 是 2026-09-18，
內容包七條 source 與研究紀錄八處一致，七頁今天重抓後內容沒有變動，
依規格**不因重查而改**）。

查核方式：`sources[]` 七條全部以 `curl -sL -A "Mokaair-editorial"` 重抓並讀 body，
逐句把 title、description、正文每一句、summary 五句、callout、表格十六格與 caption、
FAQ 六題、圖解四格與 `hero_label`、兩個 `code` 區塊的每一個識別字對回原文；
研究紀錄原有 22 條 `verbatim_quote` 用程式做**連續字串**比對。
**任何請求的 UA、標頭、查詢字串與表單都沒有放入 email 或任何個人資料**，
也**沒有使用 `sources[]` 以外的網址替文章補任何事實**
（為了反駁而讀的三個頁面見下一節，它們沒有進文章）。

檢查的主張：**131 條**（正文 74 句／子句、summary 5 句、FAQ 6 題答句、callout 1、
表格 16 格、表格與圖解 caption 各 1、圖解 4 組節點、`hero_label`、title、description、
兩個範例共 21 個識別字），外加研究紀錄 22 條引文。
**改了 15 條（20 個編輯點）**，另有 4 件留給站主。

## 重抓結果：七條 sources 今天都讀到正文，不是空殼

| source | HTTP | bytes | body 是正文嗎 |
| --- | --- | --- | --- |
| `openrouter.ai/docs/guides/routing/routers/auto-router` | 200 | 767,890 | **是**。`<title>` 為「Auto Router - Intelligent Model Selection」；Overview／How It Works／Cost Tier／Pricing 各節全文可讀；`Access Denied`／`Just a moment`／`Enable JavaScript` 各 **0** 次 |
| `openrouter.ai/docs/guides/routing/model-fallbacks` | 200 | 602,157 | **是**。`<title>` 為「Model Fallbacks - Automatic Failover Between Models」；How it works／Fallback behavior／Limitations 全文可讀 |
| `docs.litellm.ai/docs/routing` | 200 | 648,230 | **是**。`<title>` 為「Router - Load Balancing \| liteLLM」；Routing Strategies、Cooldowns、Retries 各節全文可讀 |
| `platform.claude.com/docs/en/models/overview` | 200 | 367,902 | **是**。四欄比較表整表可讀（Claude API ID、Pricing、Context window 各列） |
| `platform.claude.com/docs/en/get-started` | 200 | 521,783 | **是**。`pip install anthropic`、`export ANTHROPIC_API_KEY`、快速上手片段都在 |
| `platform.claude.com/docs/en/cli-sdks-libraries/sdks/python` | 200 | 754,022 | **是**。Handling errors／Retries／Timeouts／Long requests 各節全文可讀 |
| `platform.claude.com/docs/en/api/messages/create` | 200 | 1,416,524 | **是**。回應範例含 `content` 區塊與 `usage` 全欄位 |

**為了反駁而讀、但沒有進文章的三個頁面**（協調者點名的）：

- `openrouter.ai/docs/features/model-routing` → **302 導到** `…/routers/auto-router`，
  位元組數與 source 完全相同（767,890）。協調者要對的頁面就是 `sources[0]`。
- `platform.claude.com/docs/en/about-claude/models/overview` → **302 導到**
  `…/docs/en/models/overview`（367,902）。`models-seen.json` 記的是舊網址，
  內容包記的是導向後的網址，兩者同一頁；本代理**沒有改** `models-seen.json` 的既有條目。
- `raw.githubusercontent.com/anthropics/anthropic-sdk-python/main/README.md` → 200，
  但只有 **1,144 bytes**，今天已經是一份存根：它自己寫
  「Full documentation is available at platform.claude.com/docs/en/api/sdks/python」，
  而那個網址又 302 回 `sources[5]`。
  **結論：撐 `max_retries` 與 `with_options(timeout=…)` 的就是 `sources[5]`，不需要換來源**（詳見下面「協調者點名的五項」第 3 點）。

## 改掉的 15 條（20 個編輯點）

### 最重的五處

1. **「最大嘗試次數」的計法跟自己的範例相反。**
   H2-3 第 2 段原寫「整個級聯另外設一個最大嘗試次數，**同一顆重試或換模型升級都算進同一個計數**」，
   `cascade.py` 的註解也寫 `# counts every call: retry, escalate or fallback alike`。
   但那個迴圈**根本不會重打同一階**：`except` 分支一律 `tier_index += 1` 再 `continue`，
   同一顆模型的重試是 SDK 在**一次呼叫內部**做完的（`Certain errors are automatically retried
   2 times by default`），迴圈看不到，也不會被計數。
   已改成「計的是升級與 fallback 的次數，同一顆模型的重試由套件在一次呼叫內部處理、**不算進**這個計數」，
   註解同步改成 `# escalations and fallbacks; SDK retries happen inside one call`。

2. **`cascade.py` 漏接官方錯誤表上的 `APIConnectionError`。**
   正文寫「捕捉到**逾時或錯誤**，就把索引往上移一階」，程式卻只寫
   `except (APITimeoutError, APIStatusError)`。SDK 文件的錯誤表把
   `APIConnectionError` 單獨列成一列（status code 欄是 `N/A`），官方範例也是
   `except anthropic.APIConnectionError as e:` 排在最前面——
   自動重試用完之後的連線錯誤會**直接穿出整個級聯**，級聯就白寫了。
   已把 import 與 `except` 都補上 `APIConnectionError`（行數不變，仍是 42 行）。
   本代理在暫存目錄用假的 `anthropic` 模組重跑，連線錯誤現在會正確 fallback 到下一階。

3. **`cost_tier` 掉了文件上最要緊的那個限定，表格又漏掉同一頁的 `provider.max_price`。**
   原文是「`A tier is a band, not a ceiling, so models cheaper than the band are excluded
   as well as models above it.`」——**比該帶便宜的模型也會被排除**，草稿只寫「選便宜到最強的價格帶」。
   同一頁的 Pricing 節還寫著「`To cap what a request may cost, provider.max_price still
   applies: it filters the endpoints of whichever models the router resolves.`」，
   而表格「成本控制」那一格只寫「`cost_tier` 只選價格帶，不是每請求的金額上限」，
   讀起來像是 OpenRouter 沒有辦法限制單次花費。
   正文已補上五個值（`low`、`medium`、`high`、`xhigh`、`max`）與「是一條帶不是上限」，
   表格那一格已補上 `provider.max_price`。

4. **LiteLLM 的策略被寫成中文描述，不是 `routing_strategy` 真正吃的值。**
   草稿寫「官方文件列出的策略包含 simple-shuffle（預設）、**依剩餘配額挑節點、依延遲挑節點與依價格挑節點**」——
   句子前面才剛說「在 Router 類別上設 `routing_strategy` 這個參數」，讀者會以為那幾句中文就是值。
   文件範例實際寫的是 `routing_strategy="simple-shuffle"`、`"usage-based-routing"`、
   `"latency-based-routing"`、`"cost-based-routing"`（四個字串都逐字查到）。
   正文與表格都已改成這四個值，並補上文件自己的建議
   「`We recommend using simple-shuffle (default) for best performance in production.`」。
   同時補上研究紀錄查到卻沒用上的那一句：
   「`num_retries is not the same knob as max_retries.`」——本文自己的範例正好用了 `max_retries`，
   不講清楚兩者不是同一個設定，讀者很容易把兩篇的參數混在一起。

5. **FAQ 第 5 題把 LiteLLM 說成「跑在自己使用者流量上」。**
   原答句是「它們是平台或套件已經寫好、**跑在自己使用者流量上**的路由邏輯」。
   這句對 OpenRouter 成立（`It is powered by the market: the aggregate spend of millions of
   people using OpenRouter`），對 LiteLLM **不成立**：LiteLLM 的 Router 是
   「`Load-balance across multiple deployments`」，跑的是**你自己設定的節點**，
   跟 LiteLLM 的使用者流量無關。已分開寫成兩句。

### 其餘十處

6. **`>=500` 被寫成中文數字。** 原文 `408 Request Timeout, 409 Conflict, 429 Rate Limit,
   and >=500 Internal errors are all retried by default`，草稿寫「五百以上的伺服器錯誤」
   → 改「**500 以上的伺服器內部錯誤**」（數字照原文，`Internal` 補回）。
7. **逾時與重試的關係漏了一句。** 草稿寫「超過重試仍然逾時會丟出 APITimeoutError」，
   文件是兩句：`On timeout, the SDK throws an APITimeoutError.` 加
   `Note that requests that time out are retried twice by default.`
   已改成「**逾時的請求同樣預設重試兩次**，逾時時套件丟出的是 APITimeoutError」。
8. **「三階的輸入輸出價格差好幾倍」沒有歸屬也不精確。**
   已改成「**依 Anthropic 的模型頁**，由輕到重的輸入與輸出單價**各差到五倍**」——
   今天逐格讀到 `$1 / input MTok`／`$5 / output MTok`（Haiku 4.5）與
   `$5 / input MTok`／`$25 / output MTok`（Opus 5），兩個方向都正好五倍。
9. **`route_and_call.py` 的價格註解掛錯來源。** 原註解
   `# USD per MTok, from the official pricing page (see sources)`，
   但 `sources[]` 裡沒有 Pricing 頁，六個單價全部讀自 Models overview
   → 改成 `read on the official models overview page (see sources)`。
10. **範例的「語言」規則其實只是數中文字數。** H2-1 把語言規則講成「中英夾雜或含大量專有名詞」，
    程式裡是 `cjk_count = sum("一" <= ch <= "鿿" …)` 加一個 200 字門檻。
    已在第一段程式的解說補一句：「範例把『語言』這條規則簡化成數中文字數，要分辨中英夾雜得另外寫。」
11. **表格 OpenRouter「逾時與重試」那格的否定句已限縮到查法。**
    原句「這篇讀到的頁面沒有列出獨立的逾時或重試參數」
    → 「這篇讀到的 **Auto Router 與 Model Fallbacks 兩頁**沒有列出……」。
    （查核結果見下一節，結論成立。）
12. **表格 LiteLLM「成本控制」那格界定過寬。** 原句「可依 rpm、tpm 限流，同樣不是每請求的金額上限」
    → 「rpm、tpm 是各節點每分鐘的用量上限，用來挑節點或濾掉超限的節點，不是每次請求的金額上限」。
    Router 頁講 rpm／tpm 的地方是
    「`Picks a deployment based on the provided Requests per minute (rpm) or Tokens per minute (tpm)`」，
    是**挑節點**，不是替請求設金額上限；LiteLLM 的 Budget Routing 是**另一個沒讀的文件頁**
    （只在這一頁的左側導覽出現名字），所以這一格不做全稱否定。
13. **description 與導言說「只放進對照表」，但 H2-5 有一整段散文。**
    改成「只做對照」與「只用一段和一張對照表列出」。
14. **「這兩個平台」。** LiteLLM 是套件與自架 Proxy，不是平台（本系列第 4 篇就是這樣寫的）
    → 改「這兩個工具」。
15. **H2-1 的規則門檻沒有實測聲明。** 那一段把「短句用輕量、長文換中階」講成經驗規則，
    本站沒有量過 → 段末補「規則怎麼切、門檻放在哪裡要看自己的流量調整，**本站沒有實測**」。

## 程式範例重驗

兩塊都抽到 `SCRATCH/agents/workflow/fc-ai-workflow-model-routing-cascade/` 重跑
`python3 -m py_compile`，**都通過**；改完之後再跑一次，仍然通過，
行數也沒變（檢查器算法 `code.count("\n") + 1`，39 與 42，與研究紀錄 `code_samples` 一致）。

| 區塊 | 語言 | 行數 | 編譯 | 比對過的識別字 | 文件 |
| --- | --- | --- | --- | --- | --- |
| `route_and_call.py` | python | 39 | ok | `claude-haiku-4-5-20251001`／`claude-sonnet-5`／`claude-opus-5` 三個 id 與六個單價、`client.with_options(timeout=…)`、`messages.create(model, max_tokens, messages)`、`message.content` 區塊的 `type`／`text`、`message.usage.input_tokens`／`output_tokens` | models/overview、cli-sdks-libraries/sdks/python、api/messages/create |
| `cascade.py` | python | 42 | ok | `from anthropic import Anthropic`、`api_key=os.environ[…]`、`max_retries`（預設 2）、`APITimeoutError`、`APIConnectionError`、`APIStatusError` | get-started、cli-sdks-libraries/sdks/python |

**離線行為重跑**（不打任何 API，用暫存目錄裡一個假的 `anthropic` 模組，
`sources[]` 之外沒有安裝或呼叫任何東西）：七種情境加一次成本上限觸發，
行為與正文描述一致——信心夠就停在第一階；信心不夠連升兩階；三階都不夠就回目前最好的答案；
逾時、連線錯誤、狀態錯誤都 fallback 到下一階（連線錯誤是**這次修好的**）；
長輸入或含任務關鍵字直接從中階起跑；累積花費超過 `COST_CAP_USD` 時，
**下一次呼叫前**就停止並回傳目前最好的答案。

金鑰檢查：兩塊都只從 `os.environ` 讀，沒有字面金鑰、沒有 `<YOUR_KEY>`、
沒有 `eval`、沒有刪檔命令，網路呼叫帶 `timeout`，輸出那一行寫著「示意」。

## 查過而且正確的部分（沒有動）

- **三個模型 id 今天仍列在 Claude 模型頁的 `Claude API ID` 欄**：
  `claude-haiku-4-5-20251001`、`claude-sonnet-5`、`claude-opus-5`。
  六個單價逐格對上：`$1 / input MTok`、`$5 / output MTok`（Haiku 4.5）；
  `$2 / input MTok`、`$10 / output MTok`（Sonnet 5）；
  `$5 / input MTok`、`$25 / output MTok`（Opus 5）。
  三個 id 本來就在 `models-seen.json`，**沒有新增任何條目**。
- **OpenRouter 逾時／重試的否定結論成立。** 兩頁的渲染後正文以詞界比對
  `timeout`／`timeouts`／`retry`／`retries` 皆 **0** 次；原始 HTML 的 4 次 `Timeout`
  全部是 JS 的 `setTimeout`，1 次 `retries` 出現在站台導覽帶進來的**別頁**中繼資料
  （Render Workflows 的 `og:description`）。與正文無關，否定句成立。
- **Auto Router 四句逐字對上**：`Set your model to openrouter/auto`、
  `A fast, lightweight classifier assigns each prompt one of ~30 fine-grained task types`、
  `over a trailing 7-day window`／`Share of Spend`、
  `If classification or rankings are ever unavailable, the router degrades gracefully to a
  default model set`。`models` 陣列依序 fallback 那一格也對上 Model Fallbacks 頁的
  `Provide an array of model IDs in priority order.`
- **LiteLLM 的 `allowed_fails`／`cooldown_time` 描述成立**：
  `cooldown model if it fails > 1 call in a minute`、
  `During cooldown, the specific deployment is temporarily removed from the available pool`；
  `num_retries` 與 `retry_after` 兩個參數名與用途也對上。
- **Anthropic SDK 的三個選項全部在 `sources[5]` 上**：預設逾時 10 分鐘、
  `timeout` 接受 float 或 `httpx2.Timeout`、`client.with_options(timeout=5.0).messages.create(`、
  `max_retries=0,  # default is 2`（所以 `max_retries` 確實是**用戶端建構子**的選項、預設 2），
  兩者可以並用（文件就是一個設在用戶端、一個用 `with_options` 覆寫單次呼叫）。
- **回應欄位對得上**：`content` 區塊有 `"type": "text"` 與 `"text"`，
  `usage` 有 `"input_tokens": 2095` 與 `"output_tokens": 503`。
- **自評信心全篇都寫成「這篇的做法」**（H2-2「這篇用最簡單的做法」、callout、FAQ 第 2 題），
  沒有任何一句把它寫成供應商建議；官方文件也沒有這種建議，研究紀錄已記。
- **研究紀錄 22 條 `verbatim_quote` 全部通過連續字串比對**，每條的 `url` 都在 `sources[]` 內，
  `code_samples` 的 `label` 與 `lines` 與內容包相符。
  （第 12 條 `num_retries is not the same knob as max_retries.` 一度比對失敗，
  是本代理抽字程式把 `<code>` 標籤換成空白造成的假陰性；直接比對原始 HTML 後成立。）
- **界線檢查全部通過**：只有**一個** `warning` callout、**沒有**免責段落；
  沒有購買、訂閱或投資建議；沒有推薦式比價；沒有「台灣可用」；
  廠商宣稱都帶歸屬（「OpenRouter 的文件寫」「Anthropic 官方的 Python 套件文件寫」）；
  沒有把預覽或 beta 功能寫成已推出（引到的四個功能在文件上都沒有 beta／preview 標記）；
  正文中間沒有 `link` 區塊；FAQ 答案沒有網址；沒有簡體字、沒有 Markdown 或 HTML 語法。
- **與必連文章的分工成立**：`ai-model-tiers-explained` 的 zh-TW title
  「同一家為什麼有好幾個模型：旗艦、中階、輕量怎麼選」與正文引述**逐字相同**，
  只用一句帶過分層；第 3 篇 `ai-workflow-cost-quality-latency`（標題
  「成本、品質、延遲：多模型流程怎麼取捨」，與第二個結尾連結的 text 逐字相同）
  的估算表沒有被重講——本篇只寫「有上限、怎麼算累計」，沒有任何單價出現在正文，
  單價只在程式的 `TIERS` 裡；第 4 篇 `ai-workflow-unified-api-layer`（標題
  「統一 API 層：OpenRouter 與 LiteLLM 換模型不改程式」）的 `base_url`、
  OpenAI 相容端點、託管閘道 vs 自架 Proxy，本篇一個字都沒碰。
  第 3 篇反過來也寫著「實際要升級多少比例，是《模型路由與級聯：便宜先試、貴的兜底》的主題」，
  兩篇互相指認，Opus 5 的 `$5`／`$25` 兩邊一致。
- **第一個結尾連結的 text 與系列目錄標題逐字相同**，第二個依指派保留工作標題
  （今天第 3 篇的內容包已經存在，標題正好相同，所以自檢不再有 FAIL）。
- **`checked_on` 2026-09-18** 在內容包七條 source 與研究紀錄一致，未更動。

## 協調者點名的五項：查證結果

1. **H2-5 第三段逐句核對**：`Auto Router`／`openrouter/auto`／`~30 fine-grained task types`／
   7 天花費占比／退回預設模型集**全部成立**；`cost_tier` 少了「是帶不是上限」與五個值，已補。
   LiteLLM 這半段問題較多：策略值不是文件的字串（已改成四個值）、
   漏掉文件自己對正式環境的建議（已補）、漏掉 `num_retries` 與 `max_retries` 不是同一個設定（已補）。
   `allowed_fails`、`cooldown_time`、`num_retries`、`retry_after` 四個參數名與行為描述**本來就正確**。
2. **OpenRouter 那條消極陳述**：兩頁**確實沒有** timeout／retry 字樣（見上一節的詞界比對），
   範圍句保留，只把「這篇讀到的頁面」寫明是哪兩頁。
3. **`Anthropic(max_retries=2)` 與 `client.with_options(timeout=…)` 可以並用**：
   `sources[]` 沒有列 GitHub repo，而今天那份 raw README 只剩 1,144 bytes 的存根，
   自己把讀者指回 `platform.claude.com`（該網址 302 回 `sources[5]`）。
   撐這兩個參數的就是 `sources[5]`，而且它同時給了兩種寫法
   （`client = Anthropic(max_retries=0, # default is 2)` 與
   `client.with_options(timeout=5.0).messages.create(`），並用沒有問題，**來源不必換**。
   `max_retries=2` 寫的是文件標明的預設值，屬於「把旋鈕寫出來」，不是改行為。
   「五百以上的伺服器錯誤」對 `>=500 Internal errors` 已照原文改成「500 以上的伺服器內部錯誤」。
4. **三個模型 id 今天都還在頁上**（見上一節）；「自評信心」全篇都是本文的做法，
   沒有一句寫成供應商建議，**不用改**。
5. **成本上限那一段沒有任何單價數字**，只講「有上限、怎麼算累計」，與第 3 篇分工正確。
   程式 `TIERS` 裡的六個單價每一個都在 `sources[3]` 的模型頁上讀到；
   H2-4 新加的「各差到五倍」也是由這六個數字直接得出，並已標明出處。

## 留給站主的事

1. **`MAX_ATTEMPTS = 4` 在目前的三階級聯裡永遠碰不到。** 迴圈每次失敗或升級都往上一階，
   從最底層起算最多只跑三次。本輪只改掉會誤導的註解與正文（不再宣稱它會計同一顆的重試），
   **沒有動迴圈**。要讓這個上限真的有作用，得讓同一階可以重打（那是另一種設計），
   或把它當成日後階數變多時的保險；兩種都要改到骨幹，交給站主決定。
2. **`run_cascade` 回傳的 `attempts` 會比實際呼叫次數多一。** 碰到成本上限那一圈
   （`if spent >= COST_CAP_USD: break`）沒有真的呼叫，但迴圈計數已經前進。
   正文沒有描述這個欄位的語意，所以本輪沒有動；要精確就得多一行計數器，
   會動到 `code_samples` 的 `lines`。
3. **前提段寫「需要 Python 3.11 以上」，Anthropic 的 SDK 文件今天寫的最低版本是 Python 3.10。**
   3.11 是本系列技術篇的統一環境要求、不是套件需求，範例也沒有用到 3.11 才有的語法。
   要一致可以改寫成「本系列統一用 3.11 以上」，但那會動到其他篇，留給站主。
4. **`models-seen.json` 的 Anthropic 條目記的是 `…/docs/en/about-claude/models/overview`，
   內容包記的是導向後的 `…/docs/en/models/overview`。** 兩者今天是同一頁（302），
   依規格本代理**不改別人的條目**；站主若要統一，請整份一起換，不要單改一條。

## 自檢

```
WARN - lint raw_internal_url: 2 article link(s) as raw URLs; run `pack_cli relink` so they become article inlines that follow the target's publication
OK ai-workflow-model-routing-cascade paragraphs 2764 code_blocks 2 sources 7
```

**沒有 FAIL**（指派預期的那條 FAIL 已經消失：第 3 篇 `ai-workflow-cost-quality-latency`
的內容包今天已經存在，標題與第二個結尾連結的 text 逐字相同）。
只剩 `pack_cli relink` 的 WARN，那是協調者的事。
段落字數 **2,764**（1,800–3,000，改前 2,519），title 17 units，description 192 units。

## 結論

`needs_second_round`。改了 15 條、20 個編輯點，超過規格的十處門檻，
其中兩處是**程式與正文互相矛盾**（最大嘗試次數的計法、漏接 `APIConnectionError`）。
**沒有換掉任何一個程式範例，也沒有動骨幹論述**——級聯的四個步驟、
三階的模型與價格、信心門檻的設計都原樣保留。

第二輪只需要回來源逐句查**本輪新寫進去的每一句**：
H2-1 段末、H2-3 第 2 段（三處改寫）、H2-4 第 1 段的「各差到五倍」、
第一段程式後的「語言規則」那一句、H2-5 第 2 段與第 3 段（LiteLLM 半段整段重寫）、
表格四格（LiteLLM 路由依據、OpenRouter 逾時與重試、兩邊的成本控制）、FAQ 第 5 題、
以及 `cascade.py` 的 import／`except`／`MAX_ATTEMPTS` 註解三行。
不需要重做全篇。

## 第二輪

查核代理：未參與撰稿，也未參與第一輪。查核日 **2026-09-19**。
範圍是第一輪改動過的每一段與新寫進去的每一句，不是整篇重做。
文章的 `checked_on` 仍是 **2026-09-18**：七頁今天重抓後內容沒有變動，
也沒有依今天的頁面改任何數字，依 FACTCHECK 規則**不因重查而改**。

查核方式：`sources[]` 七條全部以 `curl -sL -A "Mokaair-editorial"` 再抓一次並讀 body；
研究紀錄的 `verbatim_quote` 用程式做**連續字串**比對；兩個範例重新 `python3 -m py_compile`，
並在暫存目錄用假的 `anthropic` 模組（第一輪的做法，不打任何 API）跑九種情境。
**任何請求的 UA、標頭、查詢字串與表單都沒有放入 email 或任何個人資料**，
也**沒有使用 `sources[]` 以外的網址替文章補任何事實**。

覆核的主張：**68 條**（第一輪改過的 20 個編輯點逐句回原文，加上受它們牽動的
H2-3 第 2 段全段、H2-5 第 3 段全段、表格四格、FAQ 第 5／6 題、圖解與 summary 的數字、
兩個範例的識別字與行為），外加研究紀錄 43 條引文的連續字串比對。
**改了 7 處**（其中 2 處是第一輪留給站主的程式問題）。

### 七條 sources 今天仍是正文，不是空殼

| source | HTTP | bytes | body 是正文嗎 |
| --- | --- | --- | --- |
| `openrouter.ai/…/routers/auto-router` | 200 | 767,890 | **是**。`<title>` 為「Auto Router - Intelligent Model Selection」；Overview／How It Works／Cost Tier／Pricing 全文可讀 |
| `openrouter.ai/…/model-fallbacks` | 200 | 602,157 | **是**。`<title>` 為「Model Fallbacks - Automatic Failover Between Models」 |
| `docs.litellm.ai/docs/routing` | 200 | 648,230 | **是**。`<title>` 為「Router - Load Balancing \| liteLLM」；Routing Strategies、Cooldowns、Retries、Session Affinity 全文可讀 |
| `platform.claude.com/docs/en/models/overview` | 200 | 367,902 | **是**。四欄比較表整表可讀 |
| `platform.claude.com/docs/en/get-started` | 200 | **521,993** | **是**。第一輪是 521,783，差 210 bytes 是頁面版本字串，`pip install anthropic`、`export ANTHROPIC_API_KEY` 與引到的兩句原文都沒有變 |
| `platform.claude.com/docs/en/cli-sdks-libraries/sdks/python` | 200 | 754,022 | **是**。Handling errors／錯誤表／Retries／Timeouts 全文可讀 |
| `platform.claude.com/docs/en/api/messages/create` | 200 | 1,416,524 | **是**。回應範例含 `content` 與 `usage` 全欄位 |

三頁 `Access Denied`／`Just a moment`／`Enable JavaScript` 皆 **0** 次（七頁都是）。

### 研究紀錄的引文

第一輪留下的 **43 條** `verbatim_quote` 全部以連續字串比對**通過**，
每條的 `url` 都在 `sources[]` 內，沒有一條需要換片段或刪事實。
本輪新增 **3 條**（見下面第 4 處），一樣通過比對，合計 **46 條**。

### 改掉的 7 處

**1. `MAX_ATTEMPTS = 4` 在三階級聯裡永遠碰不到**（第一輪留給站主的第 1 件）。
迴圈每次失敗或升級都 `tier_index += 1`，從最底層起算最多只跑三次，
所以 `4` 這個上限是死的。改成與階數一致的寫法：

```
- MAX_ATTEMPTS = 4          # escalations and fallbacks; SDK retries happen inside one call
+ MAX_ATTEMPTS = len(TIERS)  # one call per tier; SDK retries happen inside one call
```

`len(TIERS)` 讓上限正好等於可達的呼叫次數，日後加一階也自動跟著走。
模擬跑出來 `MAX_ATTEMPTS = 3`，與可達上限相同。

**2. `run_cascade` 回傳的 `attempts` 比實際呼叫多一**（第一輪留給站主的第 2 件）。
碰到 `if spent >= COST_CAP_USD: break` 那一圈沒有真的呼叫，迴圈變數卻已經前進。
改成在呼叫前遞增的獨立計數器：

```
-   for attempt in range(1, MAX_ATTEMPTS + 1):
+   calls = 0
+   for _ in range(MAX_ATTEMPTS):
      if spent >= COST_CAP_USD:
-       break
+       break  # checked before the call, so this round never spends anything
      tier = TIERS[tier_index]
+     calls += 1
-   best["attempts"] = attempt
+   best["attempts"] = calls  # calls really made, not loop rounds
```

修正前後的差別在模擬的第 9 種情境上看得到：成本上限那一圈，
改前 `attempts=2`（只打了 1 次），改後 `attempts=1`。
順帶修掉一個潛在的 `NameError`：`MAX_ATTEMPTS` 若被讀者改成 0，
原本的 `attempt` 不會被繫結。**行數 42 → 44**，研究紀錄 `code_samples` 已同步。

**3. H2-3 第 2 段的「最大嘗試次數」跟著程式改。**
原文「計的是升級與 fallback 的次數」
→ 「計的是**實際打出去的呼叫次數**，升級與 fallback 各算一次」，
並補上一句把程式行為講明白：
「範例直接把這個上限設成階數：迴圈每失敗或升級一次就往上一階，
每一階最多只打一次，所以**在這個範例裡**寫成比階數大的數字永遠不會生效。」
（否定句限縮在「這個範例」，不是對級聯設計的全稱判斷。）

**4. 第一輪換上去的 LiteLLM 策略清單自己漏掉一個值。**
第一輪把中文描述改成文件真正吃的字串是對的，但它寫
「官方文件的範例用到的值有 simple-shuffle、usage-based-routing、latency-based-routing 與 cost-based-routing」——
**同一頁還有 `least-busy`**：策略清單的標題就寫
`Routing Strategies - Weighted Pick, Rate Limit Aware, Least Busy, Latency Based, Cost Based`，
頁上也有 `router = Router(model_list=model_list, routing_strategy="least-busy")` 的完整範例。
四個值讀起來像是完整清單，實際不是。
改用**文件自己的列舉**（Session Affinity 那節的原文，一句就涵蓋五個值）：
`so it works with every strategy on this page (simple-shuffle, least-busy, usage-based-routing-v2, latency-based-routing, cost-based-routing)`
→ 正文與表格都改成「文件把這一頁上的策略列成 simple-shuffle、least-busy、
usage-based-routing-v2、latency-based-routing 與 cost-based-routing 五個值」。
（句子限定在「這一頁」，因為 `usage-based-routing` 不帶 `-v2` 的寫法在同一頁另一個範例也還在，
不做「參數只吃這五個」的全稱宣稱。五個值沒有一個帶 beta／preview／deprecated 標記；
頁上唯一標 deprecated 的 Semantic Auto Router 本篇沒有引。）
研究紀錄新增三條引文：上面那句列舉、`Load-balance across multiple deployments (e.g. Azure/OpenAI)`、
`router = Router(model_list=model_list, routing_strategy="least-busy")`。

**5. FAQ 第 5 題新寫的那句在正文裡沒有對應。**
第一輪把 FAQ5 拆成兩句是對的，但新句子「LiteLLM 的 Router 則是跑在自己程式裡的套件，
**在自己設定的多個節點之間分流**」在正文找不到落點——H2-5 第 3 段直接從
`routing_strategy` 講起，從沒說 Router 是做什麼的。
已在正文補上（依 Router 頁自己的第一句 `Load-balance across multiple deployments (e.g. Azure/OpenAI)`）：
「LiteLLM 的 Router 則是**在自己設定的多個節點之間分流**，挑節點的方式在 Router 類別上用
routing_strategy 這個參數指定……」，FAQ 答案這才 ⊆ 正文。

**6. 表格「路由依據／LiteLLM」那一格同步**：補上「在自己設定的多個節點之間分流」與同一份五個值。

**7. FAQ 第 6 題把「最大嘗試次數」列進「示意數字」，改完程式後不再成立。**
原文「這篇範例裡的門檻、逾時秒數、**最大嘗試次數**與成本上限都只是示意……不是建議值」
→ 「這篇範例裡的信心門檻、逾時秒數與成本上限都只是示意……不是建議值；
**最大嘗試次數則是直接設成階數，不是另外挑的數字**」。
（不是為了字數刪限定詞：那一項改由正文新句子承接，仍在 FAQ 裡交代。）

### 程式範例重驗

兩塊都從內容包重新抽出到 `SCRATCH/agents/workflow/fc2-ai-workflow-model-routing-cascade/run/`，
`python3 -m py_compile` **都通過**（改前改後各跑一次）。

| 區塊 | 語言 | 行數 | 編譯 | 本輪比對的重點 | 文件 |
| --- | --- | --- | --- | --- | --- |
| `route_and_call.py` | python | 39（未動） | ok | 三個模型 id 與六個單價逐格重對；`with_options(timeout=…)`、`messages.create(model, max_tokens, messages)`、`content` 區塊的 `type`／`text`、`usage.input_tokens`／`output_tokens` | models/overview、sdks/python、api/messages/create |
| `cascade.py` | python | **42 → 44** | ok | `APITimeoutError`／`APIConnectionError`／`APIStatusError` 三個類別對錯誤表（`APIConnectionError` 的 status code 欄是 `N/A`，單列一列）；`max_retries` 預設 2；`MAX_ATTEMPTS` 與 `attempts` 兩處修正 | get-started、sdks/python |

**離線行為模擬**（假的 `anthropic` 模組，九種情境，完全不連外）：

| 情境 | 實際呼叫 | `attempts` | 結果 |
| --- | --- | --- | --- |
| 信心夠，停在第一階 | 1（haiku） | 1 | PASS |
| 信心不夠連升兩階 | 3（haiku→sonnet→opus） | 3 | PASS |
| 三階都不夠 | 3 | 3 | PASS，回傳目前最好的答案（sonnet，0.5） |
| **逾時** → 升級 | 2 | 2 | PASS |
| **連線錯誤** → 升級 | 2 | 2 | PASS（第一輪補的 `APIConnectionError` 確實生效） |
| **狀態錯誤** → 升級 | 2 | 2 | PASS |
| 三階全部失敗 | 3 | 3 | PASS，沒有答案可回 |
| 長輸入／任務關鍵字 | 1（直接 sonnet） | 1 | PASS |
| **成本上限觸發** | 1 | **1**（改前是 2） | PASS |

每次呼叫送進去的 `timeout` 都是 `PER_CALL_TIMEOUT`（20.0），
`Anthropic()` 收到的 `api_key` 來自環境變數、`max_retries=2`。
金鑰檢查：兩塊都只從 `os.environ` 讀，沒有字面金鑰、沒有 `<YOUR_KEY>`、
沒有 `eval`、沒有刪檔命令，輸出那一行寫著「示意」。

### 覆核過而且正確、沒有動的部分

- **H2-4「依 Anthropic 的模型頁，由輕到重的輸入與輸出單價各差到五倍」成立。**
  今天把四欄比較表的欄位對齊後逐格讀：Haiku 4.5 `$1 / input MTok`、`$5 / output MTok`；
  Sonnet 5 `$2`／`$10`；Opus 5 `$5`／`$25`。輸入 1→5、輸出 5→25，兩個方向都正好五倍。
  同一頁還有更貴的 Claude Fable 5.1（`$10`／`$50`），但句子限定在本篇的三階，沒有過度宣稱。
- **OpenRouter 的否定句仍然成立。** Auto Router 與 Model Fallbacks 兩頁的渲染正文以詞界比對
  `timeout`／`timeouts`／`retry`／`retries` 皆 **0** 次（`max_price` 在 Auto Router 頁 1 次）。
  表格那一格已經寫明是「這篇讀到的 Auto Router 與 Model Fallbacks 兩頁」，範圍正確。
- **`cost_tier` 那一串全對**：五個值、`A tier is a band, not a ceiling…`、`provider.max_price`、
  `openrouter/auto`、`~30 fine-grained task types`、7 天 `Share of Spend`、退回預設模型集。
  本篇用的是 `openrouter/auto` 而不是頁上的 `openrouter/auto-beta`，
  也沒有用頁上標 `Deprecated` 的 `cost_quality_tradeoff`。
- **Anthropic Python SDK 的每一個旋鈕今天都還在頁上**：預設逾時 10 分鐘、
  `timeout` 接受 float 或 `httpx2.Timeout`、`client.with_options(timeout=5.0).messages.create(`、
  `max_retries=0,  # default is 2`、`Certain errors are automatically retried 2 times by default`
  加 `>=500 Internal errors`、`On timeout, the SDK throws an APITimeoutError.`、
  `Note that requests that time out are retried twice by default.`
- **Python 版本不改。** SDK 文件今天寫 `Python 3.10 or later is required.`，
  本篇兩處（導言第 2 段、H2-4 第 1 段）都寫「Python 3.11 以上」，
  但**都沒有把 3.11 說成 SDK 的要求**——那是 BRIEF 規定的系列統一環境要求，
  依指派維持 3.11+。
- **三個模型 id 仍列在模型頁 `Claude API ID` 欄，也都已在 `models-seen.json` 內；
  本輪沒有新增任何條目。**
- **第一輪為了字數刪掉但書、限定詞或歸因？沒有。** 第一輪把段落字數從 2,519 推到 2,764，
  全部是補限定詞（「本站沒有實測」「一條帶不是上限」「這篇讀到的兩頁」「依 Anthropic 的模型頁」）
  或把中文描述換成文件原字串，沒有一處是刪東西湊字數。本輪再補 112 字，**2,876**（1,800–3,000）。
- **界線**：整篇**一個** `warning` callout、**沒有**免責段落；沒有購買、訂閱或投資建議；
  沒有推薦式比價；沒有「台灣可用」；沒有驚嘆號、簡體字、Markdown 或 HTML 語法；
  廠商宣稱都帶歸屬（「OpenRouter 的文件寫」「文件註明」「Anthropic 官方的 Python 套件文件寫」
  「依 Anthropic 的模型頁」「文件並註明」）；本篇引到的功能沒有一個帶 beta／preview／deprecated 標記；
  正文中間沒有 `link` 區塊；FAQ 答案沒有網址。
- **與兄弟篇的分工與標題**（協調者點名的四篇今天逐字核對過內容包）：
  本篇正文只點名三篇，且與今天的 zh-TW title 逐字相同——
  `ai-model-tiers-explained`「同一家為什麼有好幾個模型：旗艦、中階、輕量怎麼選」、
  `ai-workflow-cost-quality-latency`「成本、品質、延遲：多模型流程怎麼取捨」、
  `ai-workflow-unified-api-layer`「統一 API 層：OpenRouter 與 LiteLLM 換模型不改程式」。
  `ai-workflow-cross-review-judge`「多模型互審：LLM 當評審、投票與集成怎麼做」、
  `ai-workflow-failures-and-guardrails`「失敗案例與防護：迴圈、費用爆炸與代理間注入」、
  `ai-workflow-structured-handoff`「模型之間交接資料：JSON Schema 與結構化輸出」
  本篇**一個字都沒有點名**，所以沒有標題要對；內容上也沒有碰互審、防護與結構化輸出，
  不矛盾也不重講。與第 3 篇的分工仍然成立（本篇正文沒有任何單價，單價只在 `TIERS` 裡）；
  與第 4 篇的 `base_url`／OpenAI 相容端點也完全沒有交集。
- **結尾兩個 link**：第一個 text 逐字是「多模型 AI 工作流教學：從拆任務到串接不同模型」；
  第二個指向 `ai-workflow-cost-quality-latency`，text 逐字等於它今天的 zh-TW title
  「成本、品質、延遲：多模型流程怎麼取捨」（自檢也會擋，今天通過）。
- **summary 五句、圖解四格、表格十六格都沒有正文以外的數字**；
  表格用到的「七天」「三十種」在正文都有。

### 留給站主的事

1. **`models-seen.json` 的 Anthropic 條目記的是 `…/docs/en/about-claude/models/overview`，
   內容包記的是導向後的 `…/docs/en/models/overview`。** 與第一輪同一件事，
   兩者是同一頁（302）；依規格本代理不改別人的條目，要統一請整份一起換。
2. **`provider.max_price` 與 `rpm`／`tpm` 只出現在表格，正文沒有展開。**
   這是研究紀錄 `unverified_or_excluded` 記下的刻意分工（展開會變成 Provider Selection
   與 Budget Routing 的教學），規格也只要求 summary 與圖解的數字進正文。
   站主若希望表格完全被正文覆蓋，才需要動。
3. `pack_cli relink` 的 WARN 仍在，那是協調者的事。

### 自檢

```
WARN - lint raw_internal_url: 2 article link(s) as raw URLs; run `pack_cli relink` so they become article inlines that follow the target's publication
OK ai-workflow-model-routing-cascade paragraphs 2876 code_blocks 2 sources 7
```

**沒有 FAIL。** 段落字數 **2,876**（第一輪後 2,764），code 區塊 39 與 44 行。

### 結論

`ok`。改了 7 處，其中 2 處是第一輪留給站主的程式問題（現在程式與正文一致，
模擬九種情境全數符合正文描述），1 處是第一輪自己新寫的清單漏了 `least-busy`，
1 處是第一輪新寫的 FAQ 句子在正文沒有落點。
**沒有換掉任何程式範例，也沒有動骨幹論述**——級聯的四個步驟、三階的模型與價格、
信心門檻的設計、規則路由的三條規則都原樣保留。
第一輪的 15 條改動，覆核後**沒有一條需要退回**。
