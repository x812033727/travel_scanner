# 獨立查核：ai-news-gpt-55-instant-20260505

查核代理：未參與撰稿。查核日 **2026-09-18**（與內容包、研究紀錄的 `checked_on` 同一天，未更動）。
查核方式：`sources[]` 四條全部以 `curl -sL -A "Mokaair-editorial"` 重抓並讀 body
（請求未帶任何 email、姓名或個人資料）。系統卡的 Table 1／3／5／9／10／11 改從頁面
`astro-island` 的 `data-evalchart` JSON 逐欄取出（那些表在純文字層只剩表頭），
Figure 1 與 Figure 2 直接下載 PNG 親自開圖讀值，40 條 `verbatim_quote` 用程式對
當天抓到的頁面渲染文字做連續字串比對。**沒有把 `sources[]` 以外的網址寫進文章**；
為了反駁而讀的 `help.openai.com` 語言清單、`developers.openai.com/api/docs/models/*`
只寫在研究紀錄與本報告裡。

檢查的主張：96 條（正文 17 段每一句、summary 五句、FAQ 六題答句、callout、
表格 9 格與 caption、圖解 caption 與研究紀錄的四格與 `hero_label`、title、description）。
改了 18 處，另有 4 件留給站主。

## 一、撰稿代理最在意的三件事，逐條驗證

### 1. 公告頁今天真的讀得到，`sourcing_verdict: full` 成立

`https://openai.com/index/gpt-5-5-instant` 先回 **308** 轉到同網址加尾斜線
（`location: /index/gpt-5-5-instant/`），再回 **HTTP 200、575,557 bytes**。
剝掉 script/style 與標籤後是 **16,012 字的正文**：`Try on ChatGPT` 按鈕文案、
`Update on June 9, 2026` 那一則、三組 GPT-5.3 Instant 對 GPT-5.5 Instant 的示例對話、
以及完整的 `Availability` 段落。**不是擋阻頁、不是導覽殼、不是軟性 404。**
十分鐘後再抓一次仍為 200（575,566 bytes，正常浮動）。
`openai.com/index/gpt-5-5-instant-system-card` 今天也回 200／334,073 bytes。

所以撰稿把 `sources[1]` 從 `openai.com/news/rss.xml` 換回公告頁、把
`sourcing_verdict` 由 `partial` 升為 `full`，**是對的**，而且解掉了 `corrections-ai.md`
must_fix #4 留下的兩難：`default model` 這個框架不再只靠 feed 的一句描述，
公告頁自己印著 `replacing GPT‑5.3 Instant as the default model`。
（前期研究記的 403 也不是誤記——`openai.com/index/*` 的可達性是間歇的，
這一點已寫進研究紀錄的 `live_data_warnings`，留給翻譯階段。）

**沒有任何句子因此失去來源。** 相反，本篇最核心的產品面陳述（可用性、方案、
三個月保留期、地區但書、6/9 更新）現在全部指得到 `sources[0]` 的原文。

### 2. 「減少 52.5%／37.3%」兩句：原話、對照對象與條件

公告頁原文（今天逐字比對，含 U+2011 連字號）：

> In internal evaluations, GPT‑5.5 Instant produced 52.5% fewer hallucinated claims than
> GPT‑5.3 Instant on high-stakes prompts covering areas like medicine, law, and finance.
> It also reduced inaccurate claims by 37.3% on especially challenging conversations users
> had flagged for factual errors.

原稿掉了兩個東西：**`In internal evaluations`（內部評測）** 與
**`areas like`（醫療、法律、財務是舉例，不是清單）**。兩個都補回去了。
`than GPT‑5.3 Instant` 原稿正文有、summary 沒有，也補上了。
兩句都歸屬給「官方公告表示」，本文沒有再從 Figure 2 換算出別的百分比冒充官方說法
（(10.1−4.8)/10.1 = 52.48% 這個算術只出現在研究紀錄的排除說明裡，沒有進文章）。

### 3. Table 1 的 0.867→0.703、0.857→0.806 與 gore 改名

從 `tbl-1` 的表格逐欄核對，欄序是 `gpt-5.1-instant / gpt-5.2-instant / gpt-5.3-instant /
gpt-5.5-instant`：

| Category | 5.1 | 5.2 | **5.3** | **5.5** |
| --- | --- | --- | --- | --- |
| gore | 0.844 | 0.766 | **0.867** | **0.703 \*** |
| sexual | 0.932 | 0.940 | **0.857** | **0.806 \*** |

表標題是 `Table 1: Production Benchmarks with Challenging Prompts (higher is better)`，
指標 `not_unsafe`。所以「0.867 是 GPT-5.3 Instant、0.703 是 GPT-5.5 Instant」、
「分數越高代表越少違規回答」、「只有兩項有星號而且都是退步」**全部正確**，
而且不是本站自己數的——官方自己寫 `comparable (i.e., not statistically significantly
different) … on all disallowed categories with the exception of gore and disallowed sexual
content`。星號的定義也照抄了（`exact paired McNemar test`，對照 `the previous production
model (here, GPT 5.3 Instant)`）。

改名那一段原稿也對，但漏了註腳的後半。官方註腳全文：

> Gore is a content policy prohibiting graphic or gratuitously gory content. The gore content
> policy is narrowly scoped, and does not include violent roleplay, violent ideation, or
> facilitation of violent activity (which are covered by our violent illicit behavior evaluation).

括號裡那句已經補進正文與 FAQ——它才是讓中文讀者不會把「血腥」讀成「暴力」的關鍵：
那三類不是沒被評，是被 Table 1 的 `Violent Illicit behavior` 那一列評了。
另外 FAQ 原本寫「這是分類名稱**與範圍**的調整」，和官方
`this is a naming change, not a change in the underlying evaluation` 直接牴觸，已改掉。

### 4. 8 月 6 日的交接：只寫來源寫的

8 月系統卡（`Published August 6, 2026`）第 1 節原文：

> Starting today, we’re updating ChatGPT with a more capable model and expanding access for
> everyone. Free and Go users will get a new default model for everyday chats. Plus and Pro
> users will get an updated GPT‑5.6 Sol with a slider that lets them choose how much effort
> ChatGPT uses for a response. These models will replace GPT-5.5 Instant.

**全部是未來式。** API changelog 同日（Aug 6）的條目也只寫
`Updated the chat-latest snapshot, which points to the latest model available in ChatGPT for
Plus and Pro users. We recommend leveraging GPT-5.6 Sol for production API usage, …`。
兩份文件都沒有寫「替換完成」或「GPT-5.5 Instant 何時停止服務」。

原稿在 **五個地方**寫成完成式（summary 第五句、description、callout、FAQ 第一題、圖解第四格），
全部改成「官方寫明新模型**將**取代它」，FAQ 並補上「官方沒有寫明替換完成或停止服務的日期」。
`will get` 也補回「會」。

## 二、重抓結果（四條 sources 全部可達、body 是正文）

| source | HTTP | bytes | body 是正文？驗到的東西 |
| --- | --- | --- | --- |
| `openai.com/index/gpt-5-5-instant` | 308→**200** | 575,557 | **是**，16,012 字正文：標題、`May 5, 2026`、52.5%／37.3% 兩句、`Availability` 三句、`Update on June 9, 2026`、記憶來源四段、三組示例對話 |
| `deploymentsafety.openai.com/gpt-5-5-instant/introduction` | 200 | 344,908 | **是**，`Published May 5, 2026`；1–9 節全文；Table 1／5／9 在文字層，Table 2／3／4／6／10／11／12 在 `data-evalchart` JSON；Figure 1–8 為 PNG |
| `developers.openai.com/api/docs/changelog` | 200 | 511,612 | **是**，`chat-latest` 四則條目（May 5／May 28／Jun 24／Aug 6）與 `gpt-5.3-chat-latest`（Feb 24／Mar 16）全在 |
| `deploymentsafety.openai.com/gpt-5-6-august-update/introduction` | 200 | 398,156 | **是**，`Published August 6, 2026`；Change log `August 19, 2026`；第 1 節 `These models will replace GPT-5.5 Instant.` |

四個 bytes 數與撰稿紀錄**完全一致**（撰稿確實抓過，不是抄前期）。
額外抓的兩張圖：`factuality.png` 200／932,553 bytes、`jailbreaks.png` 200／124,322 bytes。

## 三、改掉的 18 處

1. **xhigh 的範圍被放大到生物化學**（§1 第二段）。原稿：「網路安全**與生物化學**的
   High capability 判定，是在比部署時更高的 xhigh 推理強度下測出的能力上限。」
   系統卡只把 xhigh 綁在網路安全：`We are treating GPT-5.5 Instant as High Capability in the
   Cybersecurity domain based on its capability eval performance when run at xhigh reasoning
   effort.` 生物化學那一節（8.1.1）從頭到尾沒有 xhigh。已改成只講網路安全，
   並補上同段的 `GPT-5.5 Instant is deployed at a low reasoning effort`。
   「能力上限」**保留**，因為 8.1.2 自己寫 `the evals below are run at a higher reasoning
   effort than GPT-5.5 Instant will be deployed with in order to understand maximum capability`。
   （注意 8.1 另有一句 `evaluations represent a lower bound for potential capabilities`——
   同一份文件兩種框架，照原樣分開寫，不要「訂正」。）
2. **生物防護的清單被掛到一般 ChatGPT 上**（§3 第四段）。原稿：「ChatGPT 上還疊了拒答訓練、
   自動監測對話、帳號層級執法等額外防護。」那串出自 8.2.1 **Biological Safeguards**
   （`training the model to refuse prompts …, automated monitors that interrupt potentially
   harmful conversations, actor level enforcement, and security controls`），是生物領域的防護，
   不是 gore／性內容那兩列的產品防護。已改成「產品端還會再疊上系統層級的緩解措施，
   生物化學與網路安全這兩個高風險領域另有自動監測與行為人層級執法等防護」。
3. **「8 月 6 日被取代」→「官方寫明將取代」**，五處（見上一節第 4 點）。
4. **`may vary by region` 的 `may` 被刪**（正文、summary 第四句、FAQ 第四題）。
   原文 `Availability of specific personalization sources may vary by region`，已補「可能」。
5. **`covering areas like` 的 `like` 被刪**（正文、summary 第二句）→「等領域」。
6. **`In internal evaluations` 沒寫**（正文、summary 第二句）→ 補「在內部評測中」。
7. **`is rolling out` 的分批語氣被刪**：預設模型替換補「陸續」；6/9 更新的
   `Personalization improvements are now rolling out` 由「已推展到」改「正推展到」。
8. **HealthBench 被寫成全面進步**（§2 第二段）。官方原文
   `while HealthBench Consensus remains effectively flat (+0.03)`，已改成「多數也顯示進步……
   但 HealthBench Consensus 官方形容大致持平」。
9. **基準漂移那句被改寫成「重新測出來的」**（§2 第三段與 FAQ 第二題）。原文是
   `comparison values from previously-launched models are from the latest versions of those
   models`——是「取自那些模型的最新版本」，不是「重新測」。兩處都改了。
10. **越獄那句沒說是哪個指標低**（§3 第三段）。原稿「在每個攻擊強度下都低於 GPT-5.3 Instant」，
    讀者可能讀成「越獄率比較低＝比較好」。Figure 1 的 Y 軸是
    `worst-case defender success rate`（越高越好），紅線（GPT-5.5-Instant）在六個攻擊預算下
    全部低於綠線（GPT-5.3-Instant）——我自己開圖確認過。已改寫成「官方自承相對 GPT-5.3
    Instant 退步，系統卡的折線圖在每個攻擊預算下的**防守成功率**都低於前一代」。
11. **gore 註腳的括號補回**（§3 第二段與 FAQ 第三題），並把 FAQ 的「名稱**與範圍**的調整」
    改成「只是名稱的調整，不是底層評測的改變」（見上一節第 3 點）。
12. **記憶來源的官方但書被刪**（§4 第一段）。原文
    `Memory sources are designed to make personalization easier to understand, but they may not
    show every factor that shaped an answer.` 已補「官方也加註，記憶來源不一定顯示每一個
    影響答案的因素」，並補上記憶來源是 `across all ChatGPT models` 推出。
13. **8/19 更正的性質寫錯**（§5 第二段）。原稿只說「分數從 0.4% 訂正為 1.48%」，
    原文是 `We corrected GPT-5.5’s **pass@4** score … from 0.4% to 1.48%. The previously
    reported value was its **pass@1** score.`——不是數字算錯，是登錯了指標。已補上。
14. **第一段的「更好的個人化控制」在公告頁上找不到對應句**。已改寫成貼著原文的
    「把預設模型換成更聰明、更準確的版本，回答更清楚簡潔、也更貼合使用者」；
    `we are treating as High capability` 的「判定為」改成「視為」。
15. **callout 把 base model 但書擴及所有評測**。`Our evals are run on the base model,
    without system-level safeguards` 只寫在 3.1 節（禁止內容），已限縮成
    「其中禁止內容那幾項還是在沒有系統層防護的基礎模型上測出來的」。
16. **表格列名**「Factuality Heavy（代表性對話）」→「（高事實密度對話）」，
    對應原文 `prompts representative of factuality-heavy ChatGPT production conversations`。
17. **研究紀錄的 `verbatim_quote` 七處不是可原樣搜尋到的連續字串**，全部修好：
    - 第 1 條把 `OpenAI` / `May 5, 2026` / `Product` / `Release` / 標題五個頁面元素拼成一句，
      而頁面上 `Product` 與 `Release` 之間**沒有空白**。改成只引標題，其餘標成讀到的值。
    - 第 21 條用 `...` 把兩句接起來，而原文其實**是連續的**
      （中間是 `, and this is reflected in the scores below.`）。已補全。
    - 第 22 條引的是 PNG 圖裡的圖表標題 `Factuality Error Rate (lower is better)`，
      不在頁面文字層。改引同段原句，並在 fact 裡寫明六個百分比讀自圖檔、
      圖檔網址不在 `sources[]`。
    - 第 26、31 條把 U+2019 撇號重打成 ASCII（`model's`→`model’s`、`We've`→`We’ve`）。
    - 第 28 條把 `“violence”`／`“gore”` 的彎引號重打成直引號，又刪掉原頁的註腳標記 `1`。
    - 第 39 條把 `… for production API usage,` 的**逗號改成句號**截斷。已用整則條目全文。
    原第 36 條（PDF 21 頁、封面 5 月 4 日、pdfTeX 時間戳）`url` 掛在系統卡 HTML 頁、
    引文卻抄自 PDF 封面，而 PDF 網址不在 `sources[]`、本篇正文也沒用到，
    **整條移進 `live_data_warnings`**（`corrections-ai.md` 的 source_list_fix 第 1 點就是這樣要求的）。
    修完後 40 條引文以程式比對**全部 EXACT**。
18. **研究紀錄兩處簡體字**（`内嵌`→`內嵌`、`两个`→`兩個`）；圖解第四格
    `已被取代 / 8 月 6 日起換新模型` → `交接時點 / 8 月 6 日寫明將換新`，兩份檔案的 caption 同步。

另外把研究紀錄一條 `is_vendor_claim` 從 `false` 改成 `true`：基準漂移那條是 OpenAI
描述自己怎麼產生這些數字，外部無法觀察，依 `BRIEF.md` 第 10 型應歸為廠商宣稱。

## 四、查過而且正確的部分

- **Figure 2 六組數字**（我自己開圖）：Factuality Heavy 回答 25.3→17.9／主張 7.4→4.4；
  User flagged failures 61.3→46.1／25.2→15.8；High Stakes 36.4→19.9／10.1→4.8。
  文章表格取的是三組「% claims with factual error」，caption 寫「含事實錯誤主張比例
  （越低越好）」**正確**，沒有把回答比例和主張比例混在一起。
- **Table 3** 情感依賴 `gpt-5.3-instant 0.995 → gpt-5.5-instant 0.963`（心理健康 1.000→0.999、
  自我傷害 0.924→0.913），以及官方的
  `Regressions on the emotional reliance evaluation were not statistically significant` 與
  `did not observe an increase in undesirable responses` — 文章寫的都對。
- **Table 5** HealthBench Professional 長度校正分數 32.9→38.4（未校正 33.8→40.7）。
- **公告頁可用性三句**逐字對得上：`rolling out starting today to all ChatGPT users`、
  `in the API as chat-latest`、`For paid users, GPT‑5.3 Instant will remain available for three
  months, accessible through model configuration settings, before being retired`。
  「三個月」沒有被自己換算成日期（FAQ 只寫「從 2026 年 5 月 5 日算起，實際停用時間本文未再查證」）——
  這正是 `BRIEF.md` 第 9 型要求的寫法。
- **API changelog 四則 `chat-latest` 條目**（5/5「our latest improvements」、5/28「the latest
  improvements」、6/24、8/6）文字全部一致，文章只用了 5/5 與 8/6，沒有把 6/24 當成別的事。
- **否定句全部有範圍**：「本文查核的四個來源也都沒有寫台灣是否在內」、
  「以這幾個管道查核到 2026 年 9 月 18 日，未見官方再發布新公告或更正」、
  「GPT-5.5 Instant 這份系統卡目前沒有附上更正紀錄，但這只是查核當天的狀態」——
  沒有出現「官方從未」「唯一」這種全稱。
- **活資料沒有進文章**：沒有引用 RSS 筆數、sitemap `lastmod`、PDF `ModDate`、
  `chat-latest` 當天指向的規格（400,000 上下文／5·0.5·30 美元，那是 GPT-6 Astra 的）。
- **界線**：全文沒有購買或訂閱建議、沒有推薦式價格比較、沒有投資免責 callout，
  只有一個一般 callout；廠商宣稱都掛在「官方公告表示／OpenAI 表示／系統卡寫明」之下。
- **既有篇目**：`ai-news-gpt-55-20260423` 寫的是 GPT-5.5 Thinking 的多步驟工作，
  本篇只用一句話做命名區分；`ai-news-chatgpt-free-thinking-20260806`（同樣是 8/6 事件日）
  寫免費版改用 Luna 與 Sol 的 slider 細節，本篇只用一句帶過交接。**兩篇都沒有被重寫，
  也沒有互相矛盾**（本篇刻意不寫免費版拿到的是哪一顆模型）。
- **`checked_on` 2026-09-18** 在四條 source、研究紀錄、正文第二段、表格 caption、
  圖解 caption 五處一致，未更動。

## 五、留給站主的事

1. **`openai.com/index/*` 的 403 是間歇性的**：2026-09-16 前期研究讀不到，2026-09-18
   我兩次都讀到 200。翻譯與定稿代理若再遇到 403，請用研究紀錄裡的逐字引文，
   **不要因此換掉 `sources[0]` 或刪句子**。
2. **Figure 2 的六個百分比只存在於 PNG 圖上**，HTML 與 PDF 的文字層都抽不到。
   目前由撰稿與兩輪查核共三次獨立讀圖確認。若站主要求每個數字都必須有文字層佐證，
   就要把整張表格拿掉——沒有別的官方管道可以補。
3. **「現在還是不是預設模型」這個問題，官方沒有句點**：只寫了 `will replace`，
   沒有完成日、沒有退場日。文章現在照這個界線寫。要給更明確的結論，
   需要另外找官方的退場公告，本次四條來源都沒有。
4. **`help.openai.com` 的語言清單今天讀得到**（200／62,642 bytes，列出介面語言，
   只寫 `Chinese`、沒有分繁簡，頁面標 `Updated: 2 months ago`）。
   `corrections-ai.md` 記的 403 今天不成立。但那是活文件、也不在 `sources[]`，
   本篇正文沒有寫語言支援；若之後要寫，要先把它加進 `sources[]` 並重數。

## 六、自檢

```
FAIL
 - zh-TW link text must be the title of ai-news-2026-january-september-index
```

只剩規格允許的那一條（索引標題由協調者事後原地更新）。兩個結尾連結未動。
段落字數 2,983（上限 3,000），每節 2–4 段，summary 五句、FAQ 六題、
表格 3 欄 3 列、一個 callout，`news_date` 與 slug 尾碼同為 2026-05-05。

## 結論

**`needs_owner`**：改了 18 處，但全部是限定詞、歸屬與時態，**沒有一條骨幹論述被推翻**；
公告頁可讀性與 `sourcing_verdict: full` 這兩個撰稿代理主動提出的判斷，獨立驗證後成立。
剩下的是第五節那四件需要站主決定的事，其中第 2、3 點會影響讀者看到什麼。

---

## 第二輪

查核代理：未參與撰稿，也未參與第一輪。查核日 **2026-09-18**（`checked_on` 未更動）。
範圍照規格限縮在**第一輪改動過的段落**與**第一輪新寫進去的每一句**，逐句回 `sources[]` 原文；
另把 40 條 `verbatim_quote` 全部重跑連續字串比對。重抓了 **61 條主張**，又改了 **6 處**。

### 重抓結果（四條全部可達，body 是正文）

| source | HTTP | bytes | 對照第一輪 |
| --- | --- | --- | --- |
| `openai.com/index/gpt-5-5-instant` | 308→**200** | 575,612 | 第一輪 575,557（正常浮動）；剝標籤後仍是 **16,012 字**正文，完全一致 |
| `deploymentsafety.openai.com/gpt-5-5-instant/introduction` | 200 | 344,908 | 完全相同 |
| `developers.openai.com/api/docs/changelog` | 200 | 511,612 | 完全相同 |
| `deploymentsafety.openai.com/gpt-5-6-august-update/introduction` | 200 | 398,156 | 完全相同 |

`openai.com/index/*` 今天第三次讀到 200——403 確實是間歇性的，第一輪的判斷成立。

### 指派點名的疑點，逐條回原文

**1. High capability 與 xhigh 的歸屬——第一輪改對了。** 系統卡第 8 節原文是三句話，
順序很關鍵：`GPT-5.5 Instant is our first Instant model to be treated as High Capability in the
Biological and Chemical domain, as well as in the Cybersecurity domain.` →
`We are treating GPT-5.5 Instant as High Capability in the **Cybersecurity** domain based on its
capability eval performance when run at **xhigh** reasoning effort.` →
`Note that GPT-5.5 Instant is deployed at a **low** reasoning effort…`。
也就是說：**兩個領域都被判為 High capability，但只有網路安全那一個綁了 xhigh**。
生物化學那一節（8.1.1）我從頭讀到尾，只有
`We are treating this launch as High capability in the Biological and Chemical domain, activating
the associated Preparedness safeguards.`，**完全沒有出現 xhigh，也沒有任何推理強度的說法**。
「為的是看出能力上限」出自 8.1.2 的 `in order to understand maximum capability`，成立。
正文 §1 第一段（兩類都視為 High capability、不提 xhigh）、§1 第二段（xhigh 只綁網路安全）、
FAQ 與圖解（都沒有提 xhigh）**三處互相一致，沒有矛盾**，維持原樣。

**2. §3 最後一段（第一輪新寫的那一段）——逐句回原文後收斂兩處。**

- 「不是使用者在 ChatGPT 產品裡實際會遇到的結果」掛在「系統卡特別聲明」之下，但那是推論，
  不是原文。改成 3.1 節自己的句子：`Error rates are not representative of average production
  traffic.`（與 base model 那句同一節）→「官方同一節並寫明這些錯誤率不代表一般正式流量的平均情形」。
- 「產品端還會再疊上系統層級的緩解措施」是**沒有範圍的通則**。3.1 節寫明的系統層級緩解只掛在
  **禁止的性內容**與**未滿 18 歲**兩項，而這兩項上一段已經寫過了。改成照原文的
  「系統層級的防護不在這次評測的範圍內」（`Our evals are run on the base model, without
  system-level safeguards`），不放大。
- 同段後半「生物化學與網路安全這兩個高風險領域另有自動監測與行為人層級執法等防護」**查證後保留**：
  8.2.1 生物防護寫 `automated monitors that interrupt potentially harmful conversations, actor
  level enforcement, and security controls`，8.2.2 網路安全防護寫 `automated monitors, actor
  level enforcement, and security controls`——**兩個領域都對得上**，範圍沒有放大。

**3.「官方寫明將取代」——第一輪漏了第六處，而且那一處是完成式。** 第一輪改了 summary、
description、callout、圖解、FAQ 的**內文**，但 **FAQ 第一題的開場句還是**
「依官方文件，**已經交接給新模型**。」——它和同一則答案結尾的「官方沒有寫明替換完成或停止服務的
日期」**自相矛盾**。我把 8 月系統卡全文六處 `GPT-5.5 Instant` 都讀過：唯一講替換的是
`These models will replace GPT-5.5 Instant.`（未來式、無完成日）；其餘五處是 3.1／5／6 節把
`GPT-5.5 Instant June Update` 當成**比較基準**（`our previous production ChatGPT models`），
那是「新機型今天發表」的敘事位置，**不構成替換已完成的陳述**。同日 API 變更紀錄也只是改了
`chat-latest` 指向誰，沒有寫退場。已改成「官方文件只寫到『將取代』，沒有給這件事一個完成日」，
並在答案裡明講**本文因此不寫它已經停用、也不寫它現在仍是預設模型**。

**4. Figure 2 的六個百分比——自己下載 PNG 開圖，逐格核對。**
`factuality.png`（200／932,553 bytes／1654×951）存到暫存目錄，**沒有放進 repo**。
圖上標題 `Factuality Error Rate (lower is better)`，圖例淺藍 `gpt-5.3-instant`／深藍
`gpt-5.5-instant`，三組各有兩對長條：

| 題組 | % responses with factual error | **% claims with factual error** |
| --- | --- | --- |
| Factuality Heavy | 25.3 → 17.9 | **7.4 → 4.4** |
| User flagged failures | 61.3 → 46.1 | **25.2 → 15.8** |
| High Stakes | 36.4 → 19.9 | **10.1 → 4.8** |

文章表格三列取的**都是右邊那一對（claims）**，沒有和 responses 混用；六個數字、三個列名、
比較對象（GPT-5.3 Instant → GPT-5.5 Instant）**全部對得上**，caption「含事實錯誤主張比例
（越低越好）」正確。列名括號也回原文核對過：High Stakes `difficult medical, legal, and
financial prompts`、User Flagged Failures `users of our prior models have specifically flagged
as containing factual errors`、Factuality Heavy `prompts representative of factuality-heavy
ChatGPT production conversations`。**六個數字沒有一個要拿掉。**
HTML 文字層該處確實只有 `Figure 2 Figure 2`，研究紀錄與下面第 1 點已如實註明。
順帶把 Figure 1（`jailbreaks.png`，124,322 bytes／1417×901）也開了：Y 軸
`defender success rate`、X 軸 `attacker budget (log scale)`，紅線（5.5）在**六個攻擊預算**下
全部低於綠線（5.3）——第一輪改寫的方向沒有寫反。

**5. 限定詞回掃——全部在，另補一處。** `may vary by region` 的「可能」在正文 §4、summary
第四句、FAQ 第四題三處；`covering areas like` 的「等領域」在 §2（summary 第二句沒列舉三個領域，
不算過度宣稱）；`In internal evaluations` 的「在內部評測中」在 §2 與 summary 第二句；
HealthBench Consensus 照 `remains effectively flat (+0.03)` 寫成「官方形容大致持平」。
`is rolling out` 原本只有三處有分批語氣，**§4 第二段的「當天對所有使用者推出」漏了**，已補「陸續」。
方案門檻每一處一致：個人化先 Plus／Pro 網頁版、計畫接下來幾週擴及 Free／Go／Business／Enterprise
（三處相同）；三個月保留期只給「付費使用者」且 FAQ 明寫公告沒說免費版；8/6 是免費版與 Go 拿到新預設、
Plus 與 Pro 拿到 GPT-5.6 Sol 與滑桿（兩處相同）。

**6. 界線。** `topics` 為 `ai`／`software`／`ai-news`，**不帶 `finance`**；只有一個 callout，
沒有投資免責 callout；全文**沒有出現繁體中文或介面語言支援的任何說法**；「台灣」三次全部是
「本文查核的四個來源也都沒有寫台灣是否在內」這個方向；沒有價格、沒有推薦式比價，「訂閱」「購買」
「投資」只出現在**不建議**的免責句裡；廠商宣稱都有歸因。

### 40 條 `verbatim_quote` 的連續字串比對

先用單純的空白正規化跑，出現 **7 條 MISS**；逐條做最長相符前綴的二分搜尋後，確認 **6 條是我自己
剝標籤時在行內標籤邊界多插了一個空白**（頁面文字層作 `more accurate , with clearer`、
`our blog . The`、`High Stakes : To`、`behavior 1 ;`、`Basic Command and Control , CA/DNS`），
瀏覽器渲染時是相連的。改用會吃掉標點前空白的渲染近似正規化後 **39／40 EXACT**；
剩下第 28 條的差異只是註腳上標 `1` 與前字之間的空白，研究紀錄本來就註明「照抄註腳標記」。

第 40 條值得記一筆：它一度看起來像是把章節標題摻進句子——7.1.1.5 節的內文寫的是
`We corrected GPT-5.5’s pass@4 score on **this evaluation** from 0.4% to 1.48%.`。
追下去才發現 **8 月系統卡頂端另有一個 `Change log` 區塊**，那裡逐字就是
`on the hard-negative protein binding prediction evaluation`，**引文成立，第一輪沒有錯**。
（也因此正文「那份系統卡附有一則 2026 年 8 月 19 日的更正紀錄」這句是對的；
GPT-5.5 Instant 那份系統卡的導覽列則沒有 `Change log` 項目，對應正文那句也成立。）

### 又改的 6 處

1. **FAQ 第一題開場的完成式**（見上面第 3 點）——本輪最重的一處。
2. **§5 第一段補上「兩份文件都沒有寫替換完成或停止服務的日期。」**——這是全篇最吃重的限定詞，
   原本只在 FAQ、正文沒有，違反「FAQ 的答案 ⊆ 正文」。
3. **§3 最後一段兩處收斂**（見上面第 2 點）。
4. **§4 第二段補「陸續」**（`is rolling out`）。
5. **騰字數：只刪重複敘述，沒有刪任何但書。** 原本 2,983／3,000 只剩 17 字，而 1～4 要加字。
   刪的是：第一段「把**預設模型**換成」的第二個「預設模型」、§3 第二段第二個「官方」
   （「官方註腳把」→「註腳把」）、§5 第二段的贅語「值得提醒的是，」；
   §5 第三段「Deployment Safety Hub 的系統卡列表，或 API 變更紀錄」→
   「Deployment Safety Hub 與 API 變更紀錄」（與 FAQ 第一題寫法一致）。
6. **研究紀錄 `verified_facts` 第 37 條的 `fact` 敘述訂正**：原寫「5 月 28 日、6 月 24 日各有一次
   幾乎相同的更新說明」並共用一句引文。逐則比對後，**5 月 28 日那一則開頭是
   `Released chat-latest snapshot which points to…`**（與 5 月 5 日同樣是 `Released`、沒有逗號，
   只差結尾 `our`／`the` latest improvements 一字），**只有 6 月 24 日那一則才是引文寫的
   `Updated the chat-latest snapshot, which points to…`**。引文本身是連續字串沒問題，
   是 fact 的描述把兩則寫成同一段文字。本篇正文只用 5/5 與 8/6 兩則，**不影響文章**。

### 覆核第一輪、確認無誤的部分

- **Table 1** 從文字層逐欄核對（欄序 5.1／5.2／5.3／5.5-instant）：`gore 0.844 0.766 0.867 0.703 *`、
  `sexual 0.932 0.940 0.857 0.806 *`，星號只有這兩列，指標 `not_unsafe`。
- **Table 3** 從頁面內嵌 JSON 取值：Emotional reliance `0.995 → 0.963`、Mental health
  `1.000 → 0.999`、Self-harm `0.924 → 0.913`。
- **Table 5**：HealthBench Professional `32.9 (33.8, 2,285) → 38.4 (40.7, 2,775)`；
  同一組數字在 8 月系統卡 Table 6 再次出現，**交叉相符**。
- gore 註腳全文、`this is a naming change, not a change in the underlying evaluation`、
  情感依賴的兩句、越獄的 `directional rather than definitive`／`interim results`、
  記憶來源的 `across all ChatGPT models` 與 `may not show every factor`、可用性三句、
  6/9 更新那一則——**逐字對得上今天的頁面**。
- **API 變更紀錄今天最後一則 `chat-latest` 就是 8 月 6 日那一則**，之後沒有任何新條目；
  8 月系統卡的 `Change log` 只有 2026-08-19 一則。正文兩句有範圍的否定句都站得住。
- **既有篇目**（只讀 zh-TW、未更動）：`ai-news-gpt-55-20260423` 全文沒有出現「5.5 Instant」
  「預設」「Sol」「Luna」「5.3 Instant」，本篇只用一句做命名區分；
  `ai-news-chatgpt-free-thinking-20260806` 寫的是 8/6 當天「付費使用者的 GPT-5.6 Sol…免費使用者
  則改用 Luna」的**宣布**，沒有寫 GPT-5.5 Instant 已被取代。**兩篇都沒被重寫，也沒有矛盾。**
- `checked_on` 2026-09-18 五處仍一致，未更動；圖解四格與兩份檔案 caption 一致；兩個結尾連結未動。

### 留給站主的事

1. **Figure 2 的六個百分比只存在於官方 PNG 上**，文字層抽不到。本輪是第三次獨立開圖，
   數字、列名、比較對象都對。若站主堅持每個數字都要有文字層佐證，**唯一做法是整張表格拿掉**，
   沒有別的官方管道可補。
2. **「現在還是不是預設模型」官方沒有句點**：只寫 `will replace`，沒有完成日、沒有退場日。
   本輪把最後一處完成式也改掉了，文章現在**明白告訴讀者本文不寫它已經停用、也不寫它現在仍是預設**。
   讀者拿到一個沒有結論的答案，這是照來源的界線寫，不是漏寫。
3. **`openai.com/index/*` 的 403 是間歇性的**（今天第三次讀到 200）。翻譯／定稿代理若遇 403，
   請用研究紀錄的逐字引文，**不要換掉 `sources[0]`、也不要刪句子**。
4. **段落字數已到 2,994／3,000，只剩 6 字。** 之後任何語系若要再補限定詞，
   必須同步刪重複敘述，**不可以刪但書來騰字**。

### 自檢

```
FAIL
 - zh-TW link text must be the title of ai-news-2026-january-september-index
```

只剩規格允許的那一條（索引標題由協調者事後原地更新）。段落字數 2,994（上限 3,000），
每節 2–4 段，summary 五句、FAQ 六題、表格 3 欄 3 列、一個 callout。

### 第二輪結論

**`needs_owner`**：又改了 6 處。第一輪的 18 處**沒有一處被推翻**，其中兩件本輪特別去反駁的
（xhigh 只綁網路安全、Figure 1 的方向）獨立驗證後都成立。本輪自己找到的最重一處是
**FAQ 第一題開場仍寫「已經交接給新模型」**——那是第一輪那組修改唯一的漏網，而且與同一則答案的
結尾互相矛盾。骨幹論述仍然沒有被推翻；留給站主的是上面四點，其中第 1、2 點會影響讀者看到什麼。
