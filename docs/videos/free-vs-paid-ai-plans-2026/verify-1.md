# 查核報告 第 1 輪（大綱 B 重寫稿）— free-vs-paid-ai-plans-2026

查核日 2026-09-30。查核者不是撰稿者。所有網址用 `Mokaair-editorial/1.0` 標頭以 curl 讀取、跟隨轉址、去掉 HTML 註解後比對。舊的 `verify-1.md`、`verify-p1-20260929*.md` 查的是舊稿，只當背景，沒有當成新稿的證據。抽出的宣稱清單與頁面文字在 `mokaair-work/videos/free-vs-paid-ai-plans-2026/_tools/verify-r1/`。

今天 help.openai.com 回 200 且是真內容（不是擋頁），所以 ChatGPT 的價格與年繳多了一個官方來源。

## 讀過的官方頁

| 代號 | 網址 | HTTP |
| --- | --- | --- |
| CP | https://chatgpt.com/pricing/ | 200 |
| LP | https://learn.chatgpt.com/docs/pricing | 200 |
| HP | https://help.openai.com/en/articles/6950777-what-is-chatgpt-plus | 200 |
| HG | https://help.openai.com/en/articles/11989085-what-is-chatgpt-go | 200 |
| HT | https://help.openai.com/en/articles/9793128-about-chatgpt-pro-tiers | 200 |
| AP | https://claude.com/pricing | 200 |
| AS | https://support.claude.com/en/articles/8325606-what-is-the-pro-plan | 200 |
| GT | https://gemini.google/tw/subscriptions/（轉址加 ?hl=zh-TW） | 200 |
| GU | https://gemini.google/us/subscriptions/（轉址加 ?hl=en） | 200 |
| GL | https://support.google.com/gemini/answer/16275805（含 ?hl=en） | 200 |
| R | apps/api/app/guides/content/ai-free-vs-paid-plans-2026.json（站內） | 本機 |

## 宣稱表

| # | 宣稱 | 位置 | 來源 | HTTP | 判定 | 前 → 後 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | ChatGPT Plus 每月 20 美元 | 2a7g, plans, tw-price, d82r, title | LP「$20 /month」、HP「$20/month (billed monthly)」 | 200 | CONFIRMED | |
| 2 | Claude Pro 月繳 20 美元 | qncs, u75p, plans, tw-price | AP「$20 if billed monthly」 | 200 | CONFIRMED | |
| 3 | Google AI Pro 美國 19.99 美元 | pcxk, plans | GU「$19.99 / month」 | 200 | CONFIRMED | |
| 4 | Google AI Pro 台灣頁 NT$650 | pcxk, 9u7y, plans, tw-price | GT「每月 NT$ 650 元」 | 200 | CONFIRMED | |
| 5 | Plus 列：Sol、Codex、更多訊息和上傳 | plans.rows[0] | CP 模型表、Codex 列、方案卡「Expanded messages and uploads」 | 200 | CONFIRMED | |
| 6 | Claude Pro 列：Opus、Claude Code、更多用量 | plans.rows[1] | AP 模型表與功能表、「More usage」 | 200 | CONFIRMED | |
| 7 | AI Pro 列：4 倍用量、100 萬上下文、5 TB | plans.rows[2], dv2r, recap | GT／GU 方案卡、GL 上下文表 | 200 | CONFIRMED | |
| 8 | Gemini 免費 32k、AI Pro 100 萬，差三十倍以上 | tgz3, hook-turn.sub, pmf3, 9xau, wg56 | GL「32k tokens」「1 million tokens」；1,000,000／32,000＝31.25 | 200 | CONFIRMED | |
| 9 | Sol 從 Plus 開始才有，免費版和 Go 沒有（不寫版本） | aphm, models.items[0], xbdx | CP 模型表：GPT-6.1 Sol、GPT-6 Sol、GPT-5.6 Sol 三列都是 Free No／Go No／Plus Yes；HG「Go does not include GPT-5.6 Sol」 | 200 | CONFIRMED（不寫版本號是安全的：每個 Sol 版本在各方案的有無一致） | |
| 10 | Claude Pro 有 Opus，免費版沒有 | jef9, 3nqx | AP 模型表 Opus：No／Yes | 200 | CONFIRMED | |
| 11 | Fable 在 Pro 要另外買用量點數 | cji8 | AP 表「Usage credits」與說明「Pro users can access Fable via usage credits」 | 200 | CONFIRMED | |
| 12 | Gemini 免費版也摸得到 Pro 模型 | rtkb, models.items[2] | GT「3.1 Pro 的存取權限可能會變動」、GU「Varying access to 3.1 Pro」 | 200 | CONFIRMED | |
| 13 | 引文「3.1 Pro 的存取權限可能會變動」 | gemini-quote.data | GT 免費欄原文 | 200 | CONFIRMED | |
| 14 | AI Pro 那一欄寫「以更高權限使用 Pro 模型」 | i85v | GT／GU：這句在 AI Pro 卡的「Google 搜尋」列（註 4，AI 模式），不是 Gemini 應用程式；Gemini 的說法在常見問題「解鎖更多權限，使用 Google 最強大的 3.1 Pro 模型」 | 200 | CHANGED | 「AI Pro 那一欄寫的，則是以更高權限使用 Pro 模型。」→「AI Pro 的說明則寫，解鎖更多權限，使用最強大的 Pro 模型。」 |
| 15 | Claude Pro 每 5 小時重置，另有每週上限 | qq5y, usage.items[0] | AS「reset every five hours」「weekly usage limit that applies across all models」 | 200 | CONFIRMED | |
| 16 | Gemini AI Pro 免費版 4 倍、每 5 小時重設 | zrce, usage.items[1] | GT 註 2、GL「refreshes every 5 hours until you reach your weekly limit」 | 200 | CONFIRMED | |
| 17 | Plus 聊天官網只寫更多訊息和上傳、沒有數字 | wm8p, usage.items[2] | CP「Expanded messages and uploads」「Limits apply」 | 200 | CONFIRMED（見懷疑 1） | |
| 18 | Plus 的 Codex 用 Sol 每 5 小時約 15–160 則本機訊息 | wkj5, codex-usage | LP FAQ：GPT-6.1 Sol 15-160、GPT-6 Sol 15-150 | 200 | CONFIRMED | |
| 19 | Luna 約 350–3,000 則 | 35vi, codex-usage | LP FAQ：GPT-6 Luna 350-3,000 | 200 | CONFIRMED | |
| 20 | 只是估計、不是固定上限、每週也可能有限額 | zy7w, codex-usage.source | LP「not fixed message limits」「Weekly limits may also apply」 | 200 | CONFIRMED | |
| 21 | Plus 快速模型約 54K | smht, context-table | CP「GPT Instant total context window」Plus 54K | 200 | CONFIRMED | |
| 22 | Plus 推理模型約 256K | smht, context-table | CP「GPT Reasoning total context window」Plus 256K | 200 | CONFIRMED | |
| 23 | Claude 最多 100 萬、看模型 | uxq3, bsqu, context-table, pages-example | AP「Up to 1M varies by model」（Free／Pro／Max 同） | 200 | CONFIRMED | |
| 24 | AI Plus 128k | 59cp, gemini-ladder | GL「128k tokens」 | 200 | CONFIRMED | |
| 25 | 100 萬 token 約 1,500 頁 | rbvq, pages-example.rows[2] | GL「up to 1,500 pages of text」；GT「多達 1,500 頁」 | 200 | CONFIRMED | |
| 26 | 照比例免費版約 48 頁、AI Plus 約 192 頁 | 8bv4, pages-example.rows[0..1] | 1,500×32/1,000＝48；1,500×128/1,000＝192，有「照這個比例」限定 | — | CONFIRMED（算術；見懷疑 3） | |
| 27 | AI Pro 能整份放進兩百頁 | 7xd2 | 1,500 > 200 | 200 | CONFIRMED | |
| 28 | Plus 快速約 40 頁、推理約 320 頁 | kymt, pages-example.rows[3..4] | CP「input maximum」Plus ~40／~320 pages | 200 | CONFIRMED | |
| 29 | Claude 官網沒換成頁數 | bsqu, pages-example.rows[5] | AP 只有「Up to 1M varies by model」 | 200 | CONFIRMED | |
| 30 | 放不進時回答可能漏掉細節 | mzfa | GL「miss connections or details」 | 200 | CONFIRMED | |
| 31 | 說明欄文章有比較表和決策圖 | itwf, cta | R：table 1、image 1（含「決策」） | 本機 | CONFIRMED | |
| 32 | Plus 的 Codex：網頁、命令列、編輯器、iOS | g28b, unique.rows[0] | LP「on the web, in the CLI, in the IDE extension, and on iOS」 | 200 | CONFIRMED | |
| 33 | 免費版是有限的 Codex | unique.rows[0] | CP Codex 列 Free「Limited」 | 200 | CONFIRMED | |
| 34 | Claude Code 免費版沒有 | pr79, aw45, unique.rows[1] | AP 功能表 No／Yes | 200 | CONFIRMED | |
| 35 | AI Pro：影片生成、1,000 點 Flow、5 TB | gt6g, unique.rows[2], who-for | GT／GU AI Pro 卡 | 200 | CONFIRMED | |
| 36 | 免費版沒列影片生成、15 GB | unique.rows[2] | GT／GU 免費卡；另 GL 功能表 Video generation 未訂閱欄是非勾選圖示 | 200 | CONFIRMED（原本是推論，現在有官方表格支持） | |
| 37 | Flow 是 Google 的 AI 創意工作室 | kvju | GU「AI creative studio to create cinematic scenes and stories」 | 200 | CONFIRMED（「做影片場景用的」是口語轉述） | |
| 38 | 深度研究：免費版和 Go 有限制 | suek | CP Deep research Limited／Limited／Yes | 200 | CONFIRMED | |
| 39 | 推理式圖片生成 Plus 起 | figp | CP Image generation with Thinking No／No／Yes | 200 | CONFIRMED | |
| 40 | 互動式表格和圖表 Plus 起 | wx7y | CP No／No／Yes | 200 | CONFIRMED | |
| 41 | 舊版模型 Plus 可選、免費版和 Go 不行 | way4 | CP Legacy models No／No／Yes；HG 同 | 200 | CONFIRMED | |
| 42 | Claude 研究功能免費版沒有 | 53t5 | AP Research No／Yes | 200 | CONFIRMED | |
| 43 | 設計、簡報、文件工具 Pro 才有 | 8pmc | AP Claude Design, Slides, Docs No／Yes | 200 | CONFIRMED | |
| 44 | Microsoft 365 整合 Pro 才有 | e93x | AP Claude for Microsoft 365 No／Yes | 200 | CONFIRMED | |
| 45 | Gemini 從 AI Plus 開始就能生成影片 | x6zs, who-for.right | GU Plus 卡「access to more features like video generation」；GL 功能表 | 200 | CONFIRMED | |
| 46 | Claude 標價不含稅 | u75p, tw-price | AP「Prices shown don't include applicable tax」 | 200 | CONFIRMED | |
| 47 | Claude Pro 年繳一次 200 美元 | 499y, annual, tw-price | AP「$200 billed up front」、Billing cycle「Monthly and annual」 | 200 | CONFIRMED | |
| 48 | 月繳一年 240、省 40、每月約 3.33 | 499y, xr7c, annual | 20×12＝240；240−200＝40；40÷12＝3.33 | — | CONFIRMED | |
| 49 | ChatGPT Plus 官網只寫月繳 | rn7x, tw-price, annual | CP FAQ「monthly plans for Go, Plus and Business」；HG「do not support annual billing … for ChatGPT Go, Plus, or Pro」 | 200 | CONFIRMED（官方其實明說沒有年繳，旁白說法偏保守但正確） | |
| 50 | Gemini 台灣頁只列月費 | rn7x, tw-price, annual | GT 各方案都只有「每月」 | 200 | CONFIRMED | |
| 51 | ChatGPT 台幣看結帳時顯示 | d82r | HG「All purchases are in USD - we offer a local currency billing in a limited set of countries」 | 200 | CONFIRMED | |
| 52 | ChatGPT Go 每月 8 美元 | w7rz, entry | LP「$8 /month」 | 200 | CONFIRMED | |
| 53 | AI Plus 台灣頁每月 NT$165 | jbnx, entry | GT「每月 NT$ 165 元」（GU $4.99） | 200 | CONFIRMED | |
| 54 | ChatGPT Pro 100 美元起、三檔 | sg7x, higher-tier | LP「From $100」「$100, $200, or $500」；CP「Your choice of 3 usage tiers」；HT 三檔、只有月繳 | 200 | CONFIRMED | |
| 55 | Claude Max 100 美元起、Pro 的 5 或 20 倍 | czrs, higher-tier | AP「From $100」「Choose 5x or 20x more usage than Pro」；FAQ 以每 5 小時 session 計 | 200 | CONFIRMED | |
| 56 | AI Ultra 美國 99.99 起、台灣 NT$3,300 起、AI Pro 的 5／20 倍 | 4jev, higher-tier | GU $99.99／$199.99；GT NT$3300（5 倍）／NT$6500（20 倍） | 200 | CONFIRMED | |
| 57 | Claude 設定裡的用量頁寫下次重置時間 | qjrm, usage-check | AS「see your next reset time in Settings > Usage」 | 200 | CONFIRMED | |
| 58 | Gemini 網頁左下角設定裡的用量限制 | 8ns4, usage-check | GL「At the bottom left, select Settings Usage Limits」 | 200 | CONFIRMED | |
| 59 | Codex 看用量儀表板 | n257, usage-check | LP「check your usage dashboard」 | 200 | CONFIRMED | |
| 60 | 標題、說明、標籤、縮圖（同樣 20 美元、兩百頁實算、2026 年 9 月、以登入後為準） | youtube, thumbnail | 同上各列 | — | CONFIRMED | |
| 61 | 意見句：9284、4cca、657t、txpz、w7rz、kp5n、h7wv、wall-case | 見下 | brief §站主觀點 | — | OUT OF SCOPE（意見，見對照） | |

## 摘要

- 查了 61 條：CONFIRMED 59、CHANGED 1（#14 i85v）、NOT FOUND 0、意見 1 組另外對照。事實修改 1 處，不需要第二輪。
- 修改：i85v 引用的是 AI Pro 卡「Google 搜尋」列（AI 模式），不是 Gemini 應用程式；改成常見問題的「解鎖更多權限，使用最強大的 Pro 模型」。claims.md 的 c6 同步；c16、c18、c26 補上今天新增的官方證據（GL 功能表、help.openai.com 的 Go／Plus／Pro 頁）。畫面資料、標題、縮圖都沒有數字要改。
- 站主點名的項目：Go 8／Plus 20／Pro 100 起都有兩個官方來源（LP 與 help.openai.com）；help.openai.com 明寫 Go、Plus、Pro 都沒有年繳。Sol、Luna 不寫版本號是安全的（Sol 各版本的有無一致；Luna 旁白只出現在 Codex 估計，LP 的 Plus Codex 是 GPT-6 Luna）。Codex 估計 15–160 是 GPT-6.1 Sol，GPT-6 Sol 是 15–150，「大約十五到一百六十」涵蓋兩者。上下文與頁數都對，48／192 頁是有標「照這個比例」的比例算術。AI Plus NT$165 與台灣只列月費都對。Claude Max 5x／20x 照官網。上一階價格都對。「免費版有沒有影片生成」今天在 GL 功能表上有官方支持（未訂閱欄非勾選）。
- 會過期的事實：ChatGPT 模型陣容正在輪替（LP：GPT-5.5 於 2026-10-14 下架；GPT-5.6 Sol 優惠價至少到 2026-11-21；HT：Pro 200 重新開放新訂，非沿用舊約的新訂閱用量較低）；Gemini 用量規則自 2026-05-17 起改為運算量計算、「可能不經通知變動」；GT 頂部橫幅寫台灣學生方案「優惠活動即將結束」（影片沒用）。
- 與 brief 衝突（來源優先，旁白沒有受影響）：brief 會過期事實表寫「Pro 100／200、200 美元 2026-09-10 起暫停新訂」，今天 HT 寫 Pro 200 已重新開放、另有 Pro 500，共三檔；旁白說「三檔」與今天官網一致。
- 意見對照 brief §站主觀點：4cca（用得到才付）、three-things 三步驟與 h7wv（先用滿兩週最重要）、wall-case（看撞到的牆而不是誰最強）、kkm9（以登入後為準）都一致且標為看法或情境。有兩處請站主確認：(a) 9284「二十美元這一級，這一格最容易差很多」出自大綱 B 的鉤子，不在 §站主觀點裡；(b) txpz／w7rz 說「每天大量用、常讀長文件、寫程式做影片的人才最可能需要二十美元這一級」「偶爾撞到額度先看入門方案」，而 §站主觀點寫的是「偶爾問問題三家免費版都夠；每天大量用才值得付，而且第一筆錢通常入門方案就夠」——重度使用者的第一筆錢，brief 指向入門方案，稿子指向二十美元這一級。沒有改寫。
- 聽感（只報告）：超過 40 字的句子三句：aphm（42）、kymt（42）、g28b（41）（含空白計）。沒有「經查證」「根據官方文件」「本影片」、括號或網址；「官網寫／官網說」出現十多次，是出處說明，不是查核口吻，但密度偏高。旁白裡的拉丁字詞都在 lexicon.json，沒有新增詞條。reveal 順序沒有發現先亮後講。
- lint：`node tools/video/cli.mjs lint --slug free-vs-paid-ai-plans-2026` → 0 errors, 0 warnings（估計 8.3 分鐘、103 句）。
- 懷疑但沒改：(1) wm8p 說 Plus 聊天「沒有數字」屬實，但 CP 同頁寫 Free 到 Pro 的日常文字聊天都是「Unlimited*」，觀眾可能誤以為免費版聊天次數較少；(2) context-table 把 ChatGPT 的「總視窗」和 Gemini／Claude 的上下文放同一欄，而 pages-example 用的是 ChatGPT 的「輸入上限」，兩種口徑並列，官網註明輸入空間比總視窗小；(3) 48／192 頁是依 Gemini 官網「最多約 1,500 頁」按比例推的，不是官網數字，「差一點」（192 對 200）落在誤差內，建議站主接受或改成「接近」；(4) LP 的 Plus 方案卡寫 Codex 模型是「GPT-6 Sol and GPT-6 Luna」，FAQ 估計表卻列 GPT-6.1 Sol，官網自己不一致；(5) 免費版其實也有 Flow（「可使用 AI 創意工作室」，含有限的 Nano Banana Pro），影片只說 AI Pro 多 1,000 點，沒有說免費版沒有 Flow，所以沒改；(6) gt6g「各家獨有的」裡的影片生成在 Google 自家從 AI Plus 就有，只在三家二十美元方案之間才算獨有。
- 第二輪：不需要（事實修改 1 處，未超過 3 處）。
