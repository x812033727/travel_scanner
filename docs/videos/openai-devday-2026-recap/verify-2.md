# Verification round 2: openai-devday-2026-recap

Verifier: claude-fable-5-1, a separate agent session from the writer's and from round 1's, 2026-10-03. I read `verify-1.md` and round 1's edit log (`_tools/verify/round1/applied.json`, 59 edits) first, numbered every string of `video.json` (1–362) and `shorts.json` (363–399) the same way round 1 did, and re-checked two groups against the sources: every string round 1 changed or narrowed (55), and a random third of the strings it confirmed (102 of 305). For `openai.com`, `help.openai.com`, `chatgpt.com` and `learn.chatgpt.com` the source is the coordinator's browser capture of 2026-10-03 (`_tools/sources/`, read line by line; I did not fetch those hosts and used no browser). `developers.openai.com` (eleven URLs) and `modelcontextprotocol.io` (one) were fetched again today with the editorial user agent, 1.5 s apart per host: every URL answers as it did in round 1 (two guessed Decisions paths are still 404), and the ten pages that exist are byte-identical to the captures or to round 1's copies. Web searches used: 0 of 5.

Helper files are in `<VIDEO_WORKDIR>/openai-devday-2026-recap/_tools/verify/round2/`: `extract.mjs` (the numbered list, with round 1's verdict for each row), `sample.mjs` and `sample.json` (which rows were picked), `fetch.mjs` and `fetch-report.json` (today's fetches and their hashes), `check.mjs` (85 mechanical checks against the capture files: counts, ratios, verbatim strings, sums, reveals, leftovers of old wording; all pass before and after my edits), `apply.mjs` and `applied.json` (13 edits, each asserts the text it replaces), `claims-update.mjs`, `table.mjs` (the table below; it stops when a picked row has no verdict or an edited row is not marked CHANGED), the `*.before.*` copies and the lint outputs.

## Pages opened

| key | URL or file | HTTP | How it was read in round 2 |
| --- | --- | --- | --- |
| R | https://openai.com/zh-Hant/index/devday-2026-recap/ | 200 capture | `sources/devday-2026-recap.zh-Hant.md`; 25 `###` items in 5 sections (4+7+4+7+3, counted by script); the nine availability lines read one by one |
| SOL | https://openai.com/zh-Hant/index/introducing-gpt-6-1-sol/ | 200 capture | `sources/introducing-gpt-6-1-sol.zh-Hant.md` |
| DOTS | https://openai.com/zh-Hant/index/introducing-dots/ | 200 capture | `sources/introducing-dots.zh-Hant.md` |
| AG | https://openai.com/zh-Hant/index/introducing-the-agents-api/ | 200 capture | `sources/introducing-the-agents-api.zh-Hant.md` |
| PRO | https://help.openai.com/en/articles/9793128-about-chatgpt-pro-tiers | 200 capture | `sources/help-about-chatgpt-pro-tiers.en.md`; only "Updated: yesterday" |
| SIWC | https://help.openai.com/en/articles/20001410-sign-in-with-chatgpt | 200 capture | `sources/help-sign-in-with-chatgpt.en.md`; only "Updated: yesterday" |
| SPEED | https://learn.chatgpt.com/docs/agent-configuration/speed | 200 capture | `sources/learn-chatgpt-speed-and-cloud.en.md` lines 5–32 |
| CLOUD | https://learn.chatgpt.com/docs/cloud | 200 capture | the same file, lines 34–54 |
| SEC | https://learn.chatgpt.com/docs/security/setup | 200 capture | `sources/chatgpt-space-and-codex-security-cloud.md` lines 33–45 |
| SPACE | https://chatgpt.com/zh-Hant/features/space/ | 200 capture | the same file, lines 5–31 |
| PRICE | https://developers.openai.com/api/docs/pricing | 200 curl | fetched today, byte-identical to the capture; line numbers are of `sources/developers_openai_com_api_docs_pricing.txt` |
| MODEL | https://developers.openai.com/api/docs/models/gpt-6.1-sol | 200 curl | fetched today, byte-identical |
| UF | https://developers.openai.com/api/docs/guides/ultrafast-mode | 200 curl | fetched today, byte-identical |
| PSP | https://developers.openai.com/api/docs/guides/private-safety-processing | 200 curl | fetched today, byte-identical; the page never mentions Private Inference |
| MCP | https://modelcontextprotocol.io/community/working-groups/triggers-events | 200 curl | fetched today, byte-identical to round 1's copy; H1 "Triggers and Events Charter" |
| BED | https://developers.openai.com/api/docs/guides/agents-api/bedrock-managed-agents | 200 curl | fetched today, byte-identical to round 1's copy; no claim rests on it |
| CU | https://developers.openai.com/api/docs/guides/agents-api/tools/computer-use | 200 curl | fetched today, byte-identical to round 1's copy; no claim rests on it |
| LLMS | https://developers.openai.com/api/docs/llms.txt (and `/api/reference/llms.txt`) | 200 curl | fetched today, byte-identical to round 1's copies; still no entry with "Decisions"; `/api/docs/guides/decisions` and `/decisions-api` still answer 404 |
| CHG | https://developers.openai.com/api/docs/changelog | 200 curl | fetched today, byte-identical to round 1's copy; no "Decisions" entry |
| AOA | docs/videos/always-on-agent-explained/video.json | repo | title line 18; the dots card line 701 and its one sentence line 730 |
| G6, G6V | docs/videos/gpt6-vs-opus55-worth-paying/claims.md (c8, line 12) and video.json (title line 18) | repo | $348 and $69.60, recomputed |
| PW | docs/videos/ai-price-war-gpt-6-sol-vs-opus-5-5/video.json | repo | title line 20; chapter line 162 |
| BRIEF | docs/videos/openai-devday-2026-recap/brief.md | repo | read only; not edited |
| SELF | this video.json | — | the script's own cards and sums |

## Which rows were re-checked

- **Changed or narrowed by round 1 (55 rows):** the 45 it marked CHANGED and the 10 it marked NOT FOUND (3, 18, 19, 88, 107, 170, 197, 208, 210, 322; in the table these read "narrowed").
- **A random third of its 305 CONFIRMED rows (102 rows),** picked by `sample.mjs`: mulberry32 with seed 20261003, a Fisher–Yates shuffle of the confirmed row numbers in ascending order, the first ⌈305 ÷ 3⌉. The rows: 1, 9, 20, 24, 27, 28, 34, 35, 47, 55, 59, 60, 61, 63, 64, 68, 80, 84, 86, 92, 97, 99, 105, 110, 111, 120, 125, 127, 130, 139, 144, 146, 148, 151, 152, 153, 159, 161, 163, 165, 168, 171, 175, 179, 184, 187, 191, 192, 193, 194, 203, 206, 213, 220, 226, 227, 229, 230, 231, 234, 238, 240, 241, 245, 250, 253, 254, 255, 259, 264, 266, 273, 275, 278, 281, 284, 292, 293, 295, 302, 303, 308, 309, 315, 317, 319, 320, 332, 336, 341, 342, 346, 347, 349, 350, 354, 360, 373, 375, 381, 387, 389.

The other 203 confirmed rows and the 39 out-of-scope rows were read for contradictions with the rows above (cards against narration, one scene against another) and are not in the table.

## Claim table

Row numbers are round 1's. Long strings are cut at 64 characters; `where` identifies them. "round 1" says which group the row is in; the verdict is this round's.

<!-- claim table: generated by _tools/verify/round2/table.mjs -->
| # | claim (as it reads now) | where | URL (key:lines of the capture) | HTTP | round 1 | verdict | before → after 〔note〕 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | DevDay 2026 的 25 項，你今天碰得到幾項？照方案分五張清單，這週就能做 | youtube.title | R:15, 27–133 | 200 capture | confirmed (sampled) | CONFIRMED | ### 標題 4＋7＋4＋7＋3＝25（腳本重數）；頁面自述「超過 20 項」 |
| 3 | 給付 Plus、付 Pro、公司用 Business 或 Enterprise，以及接 API 的人：找到自己那一張清單就夠。影… | youtube.description[line 2] | SIWC:27–28, 31；DOTS:76 | 200 capture | narrowed | CONFIRMED | 空行與「要先核准」的引號已拿掉；三樣、訂閱共用是另一個可以不答應的請求、自訂規則「要求先取得核准」都對得上。「訂閱共用」還在引號裡（subscription sharing 的中譯，不是介面字樣），沒動，見摘要 |
| 4 | 會動到帳單的只有三個數字：五分之一（GPT-6.1 Sol 的 API 牌價是 Astra 的五分之一）、六倍（GPT-6 As… | youtube.description[line 4] | PRICE:913–914, 949；SPEED:15, 20；PRO:25, 49；R:47–48, 36–37, 97, 104；SOL:55；UF:927；SPACE:10, 18, 23, 31；G6:12；DOTS:94 | 200 curl；200 capture；repo | changed | CHANGED | 官方頁之間寫得不一樣的地方（… → 官方頁寫得不一樣的地方（… 〔三個數字與五處不一致逐一重對，都成立；Codex 雲端那一處是同一頁的兩行（R:47–48），字卡與口播也說「同一段」「那一段」，「官方頁之間」只對另外四處成立。項數與 348／70 的歸屬成立；「倍數是 OpenAI 頁面上的」裡 API 的六倍是價目表兩列的比值，沒動，見摘要〕 |
| 6 | ・AI 代理怎麼運作、怎麼失敗（含 dots 一段）：〈聊天機器人時代結束了：AI 代理（AI Agent）實際怎麼運作、又怎麼… | youtube.description[line 7] | AOA:18, 701, 730 | repo | changed | CONFIRMED | 標題逐字相同（腳本比對）；dots 在那一支是一張字卡加一句口播 |
| 7 | ・Sol 對 Astra 的整月帳單公式：〈GPT-6 Astra vs Claude Opus 5.5 vs Gemini：到… | youtube.description[line 8] | G6V:18；G6:12 | repo | changed | CONFIRMED | 標題逐字相同；c8 的 $348、$69.60 |
| 8 | ・同一個模型的八格價目表怎麼讀（延伸，影片裡沒提到）：〈GPT-6 Sol 與 Claude Opus 5.5 同一天降價，你的… | youtube.description[line 9] | PW:20, 162 | repo | changed | CONFIRMED | 標題逐字相同；口播沒有提到這一支，「影片裡沒提到」成立 |
| 9 | 錄製日期：2026 年 10 月 3 日。價格、方案與可用範圍之後會變，以官方頁為準。 | youtube.description[line 11] | SELF | — | confirmed (sampled) | CONFIRMED | 查閱日 2026-10-03 |
| 18 | OpenAI 說明中心：About ChatGPT Pro tiers（2026-10-03） | sources[3] | PRO:3–5 | 200 capture | narrowed | CONFIRMED | 擷取檔只有 Updated: yesterday；標題不帶更新日，checked_on 2026-10-03 |
| 19 | OpenAI 說明中心：Sign in with ChatGPT（2026-10-03） | sources[4] | SIWC:3–4 | 200 capture | narrowed | CONFIRMED | 同上 |
| 20 | ChatGPT Learn：Speed（Fast、Ultrafast 的額度與點數倍數，GPT-5.5 退場日）（2026-10… | sources[5] | SPEED:7, 15, 20, 32 | 200 capture | confirmed (sampled) | CONFIRMED | 標題說的三件事都在那一頁 |
| 24 | OpenAI API：Pricing（標準、Fast、Ultrafast 價目表）（2026-10-03） | sources[9] | PRICE:906–949 | 200 curl | confirmed (sampled) | CONFIRMED | 今天重抓，和擷取檔逐位元相同 |
| 27 | OpenAI API：Zero Data Retention with Private Safety Processing（20… | sources[12] | PSP:927–930 | 200 curl | confirmed (sampled) | CONFIRMED | 今天重抓，逐位元相同；頁內全名 Zero Data Retention with Private Safety Processing |
| 28 | OpenAI：Agents API 隆重登場（2026-09-10）（2026-10-03） | sources[13] | AG:3, 5, 10 | 200 capture | confirmed (sampled) | CONFIRMED | 頁面日期 2026-09-10 |
| 29 | MCP：Triggers and Events Charter（工作小組章程，提議中的事件規格）（2026-10-03） | sources[14] | MCP | 200 curl | changed | CONFIRMED | 今天重抓（200，和第一輪抓的逐位元相同）；H1 是 Triggers and Events Charter |
| 34 | DevDay 2026 的 25 項，你今天**碰得到幾項**？ | title.data.title | R:27–133 | 200 capture | confirmed (sampled) | CONFIRMED | 25 同上 |
| 35 | 照方案分五張清單：所有人、Plus、Pro、團隊、開發者 | title.data.subtitle | SELF | — | confirmed (sampled) | CONFIRMED | 站主的分法；五張和 tally 的五個名稱一致 |
| 45 | 你可能會問，那我自己今天到底能用幾項？ | chat-ask / 2kju | BRIEF:72 | repo | changed | CONFIRMED | 企劃 chat 卡設計的問題；「你可能會問」不再宣稱有人問過 |
| 47 | 每一張只寫官網當天的寫法。 | queue-turn / 2pyt | SELF | — | confirmed (sampled) | CONFIRMED | 每張卡都標來源頁與日期 |
| 52 | 回顧頁「適用於」那一行沒限定付費方案 | ch2.data.subtitle | R:48, 52, 56, 60, 79, 83, 91, 121, 127 | 200 capture | changed | CHANGED | 回顧頁「適用於」那一行沒指定付費方案 → 回顧頁「適用於」那一行沒限定付費方案 〔九行裡 R:121 點名了 Enterprise、Edu、Healthcare（寫的是還沒有）；「沒指定」照字面對這一行不成立，「沒限定」九行都成立〕 |
| 54 | 其實回顧頁的 25 項裡，有 9 項的適用於那一行，沒有限定付費方案。 | pool-desk / 3qfi | R:48, 52, 56, 60, 79, 83, 91, 121, 127 | 200 capture | changed | CHANGED | 其實回顧頁的 25 項裡，有 9 項的適用於那一行，沒有指定付費方案。 → 其實回顧頁的 25 項裡，有 9 項的適用於那一行，沒有限定付費方案。 〔九行裡 R:121 點名了 Enterprise、Edu、Healthcare（寫的是還沒有）；「沒指定」照字面對這一行不成立，「沒限定」九行都成立；Codex 雲端同一段的另一句（R:47）下一句口播 4fu7 有交代〕 |
| 55 | 回顧頁「適用於」那一行怎麼寫 | nine-stats.data.title | R:48 | 200 capture | confirmed (sampled) | CONFIRMED |  |
| 59 | 3 項 | nine-stats.data.stats[1].value | R:60, 121, 127 | 200 capture | confirmed (sampled) | CONFIRMED | 三行逐一對過 |
| 60 | 所有 Codex 使用者、所有其他方案、全球已登入使用者 | nine-stats.data.stats[1].label | R:60, 121, 127 | 200 capture | confirmed (sampled) | CONFIRMED | 三行的寫法：所有 Codex 使用者、所有其他 ChatGPT 方案、全球已登入的 ChatGPT 使用者 |
| 61 | Codex Security Cloud、可分享的個人檔案、使用 ChatGPT 登入 | nine-stats.data.stats[1].note | R:60, 121, 127 | 200 capture | confirmed (sampled) | CONFIRMED |  |
| 63 | 其中 6 項，官網寫的是適用於所有方案。 | nine-stats / 3v68 | R:48, 52, 56, 79, 83, 91 | 200 capture | confirmed (sampled) | CONFIRMED | 六行都是「適用於所有方案。」（腳本比對） |
| 64 | 另外 3 項，寫給所有 Codex 使用者、其他方案、已登入使用者。 | nine-stats / 4ffb | R:60, 121, 127 | 200 capture | confirmed (sampled) | CONFIRMED |  |
| 68 | **Codex CLI**：語音聊天、/agents 檢視、worktree | codex-four.data.items[1] | R:51 | 200 capture | confirmed (sampled) | CONFIRMED | 語音聊天、/agents 檢視畫面、內建 worktree |
| 73 | CLI 能用講的，程式碼審查接 GitHub 和 GitLab；剩下五項，也沒限定付費方案。 | lane-wide / 4py7 | R:51, 55, 79, 83, 91, 121, 127 | 200 capture | changed | CHANGED | CLI 能用講的，程式碼審查接 GitHub 和 GitLab；剩下五項，也沒指定付費方案。 → CLI 能用講的，程式碼審查接 GitHub 和 GitLab；剩下五項，也沒限定付費方案。 〔下一張字卡 five-more 的個人檔案那一條就點名三個方案（第一輪補上的），口播說「沒指定」和字卡對不上；「沒限定」五項都成立〕 |
| 78 | **可分享的個人檔案**：Enterprise、Edu、Healthcare 即將推出，其他方案已有 | five-more.data.items[3] | R:121 | 200 capture | changed | CONFIRMED | 和那一行逐項相同；nine-stats 的「所有其他方案」、not-yet 第 6 條一致 |
| 80 | 回顧頁「適用於」那一行的寫法，2026-09-29 | five-more.data.note | R:5 | 200 capture | confirmed (sampled) | CONFIRMED |  |
| 84 | 使用 ChatGPT 登入，照說明頁的五步 | login-steps.data.title | SIWC:20–25 | 200 capture | confirmed (sampled) | CONFIRMED | 五步 |
| 86 | 首批 Airtable、GitLab、HubSpot、Notion、Supabase、Vercel，以官網為準 | login-steps.data.steps[0].detail | SIWC:16 | 200 capture | confirmed (sampled) | CONFIRMED | 六家逐一對過；Initial |
| 88 | 或 Continue with ChatGPT | login-steps.data.steps[1].detail | SIWC:12, 22 | 200 capture | narrowed | CONFIRMED | 說明頁的英文原文 |
| 92 | 建立、連結或存取那個帳號 | login-steps.data.steps[3].detail | SIWC:24 | 200 capture | confirmed (sampled) | CONFIRMED | create, link, or access an account |
| 97 | 訂閱共用，是另外一把鑰匙，不是跟著登入一起給的。 | key-board / 63ta | SIWC:27–28 | 200 capture | confirmed (sampled) | CONFIRMED | separately request permission |
| 98 | 對方拿到的，和登入不給的 | three-vs.data.title | SIWC:32, 36 | 200 capture | changed | CONFIRMED | does not independently share；應用程式可以另外請求 |
| 99 | 對方拿到的 | three-vs.data.left.heading | SIWC:31 | 200 capture | confirmed (sampled) | CONFIRMED |  |
| 103 | 登入本身不給的 | three-vs.data.right.heading | SIWC:32, 36 | 200 capture | changed | CONFIRMED | 同標題 |
| 105 | 檔案與 token | three-vs.data.right.points[1] | SIWC:34 | 200 capture | confirmed (sampled) | CONFIRMED | Your files or tokens |
| 107 | 說明中心的寫法，2026-10-03 查閱 | three-vs.data.verdict | SIWC:4 | 200 capture | narrowed | CONFIRMED | 不帶更新日；查閱日是今天 |
| 109 | 聊天和記憶、檔案和 token、帳務，登入本身都不給。 | three-vs / 6bae | SIWC:32–36 | 200 capture | changed | CONFIRMED | 三條逐一對過；標題、欄名、口播三處寫法一致，card-closeup「只有三樣」不衝突 |
| 110 | 訂閱共用可以不答應；答應了，也能自己設上限，像把水道繩拉到記號就停。 | lane-rope / 6fq4 | SIWC:27–28 | 200 capture | confirmed (sampled) | CONFIRMED | 可以不核准；can control and set limits |
| 111 | 公司帳號看不到按鈕，先問管理員；那是全域管理員管的，不是壞掉。 | office-bolt / 6grq | SIWC:44, 48 | 200 capture | confirmed (sampled) | CONFIRMED | 全域管理員成立；說明頁列了三種看不到按鈕的原因，口播只講一種（第一輪已列） |
| 120 | Plus 多的那一項 | sol-big.data.kicker | SOL:53 | 200 capture | confirmed (sampled) | CONFIRMED |  |
| 125 | Codex 雲端的意思是，你的電腦睡著了，任務還在跑，手機也能接著看。 | shutter-wheel / 6zff | CLOUD:39, 42；R:47 | 200 capture | confirmed (sampled) | CONFIRMED | web, mobile, or desktop |
| 127 | Each task has its own workspace and can keep working while your … | cloud-quote.data.quote | CLOUD:42 | 200 capture | confirmed (sampled) | CONFIRMED | 一字不差（腳本比對） |
| 130 | Codex Cloud 頁上的原句，是這樣寫的。 | cloud-quote / 79px | CLOUD:42 | 200 capture | confirmed (sampled) | CONFIRMED |  |
| 139 | 不受影響 | retire-stats.data.stats[1].label | SPEED:32 | 200 capture | confirmed (sampled) | CONFIRMED | The OpenAI API isn't affected |
| 144 | Plus 的清單，九項加一個 Sol。 | test-ride / 8vrs | SOL:53；SELF | 200 capture；— | confirmed (sampled) | CONFIRMED | 9＋1 |
| 146 | Pro 的清單：四項、dots 看市場、三個級別 | ch4.chapter | R:97, 101, 105, 117；DOTS:94；PRO:21–25 | 200 capture | confirmed (sampled) | CONFIRMED |  |
| 148 | Pro 的清單：四項、dots 看市場、三個級別 | ch4.data.title | R:97, 101, 105, 117；DOTS:94；PRO:21–25 | 200 capture | confirmed (sampled) | CONFIRMED | 同章名 |
| 150 | Pro 那一張清單，和你的帳單有關。 | ch4 / 977k | SELF:tally-stats | — | changed | CONFIRMED | 只剩「和帳單有關」；所有人 9、Pro 6 |
| 151 | 先看四項已經寫在 Pro 名下的，再加一項要看市場的，也就是 dots。 | pottery-wide / 99ep | R:97, 101, 105, 117；DOTS:94 | 200 capture | confirmed (sampled) | CONFIRMED | 四項的那一行都寫 Pro；dots 看市場 |
| 152 | Pro 的清單 | pro-five.data.title | SELF | — | confirmed (sampled) | CONFIRMED |  |
| 153 | **dots**：符合資格的市場逐步推出，第一個不另收費；台灣有沒有以官網為準 | pro-five.data.items[0] | DOTS:94, 96 | 200 capture | confirmed (sampled) | CONFIRMED | 頁上沒列市場名 |
| 154 | **ChatGPT 空間**：網頁與桌面可編輯；行動版，空間頁寫可檢視、回顧頁寫即將推出，以官網為準；分享頁面不分享私人對話與記… | pro-five.data.items[1] | R:97；SPACE:23, 26, 31 | 200 capture | changed | CHANGED | **ChatGPT 空間**：網頁與桌面可編輯；行動版，空間頁寫只能看、回顧頁寫即將推出，以官網為準；分享頁面不分享私人對話與記憶 → **ChatGPT 空間**：網頁與桌面可編輯；行動版，空間頁寫可檢視、回顧頁寫即將推出，以官網為準；分享頁面不分享私人對話與記憶 〔兩頁不一致成立；空間頁對行動版寫的是「檢視」（SPACE:23）與「尋找、閱讀及分享」（SPACE:31），「只能看」比來源窄〕 |
| 159 | dots，向符合資格的市場逐步推出，台灣有沒有，以官網為準。 | pro-five / 9rtc | DOTS:94 | 200 capture | confirmed (sampled) | CONFIRMED |  |
| 160 | ChatGPT 空間和動態頁面，網頁和桌面能編輯；行動版兩頁寫法不同，以官網為準。 | pro-five / a3tb | R:97；SPACE:23, 31 | 200 capture | changed | CONFIRMED | 口播只說兩頁寫法不同；not-yet 的「行動版編輯：空間頁寫即將推出」一致 |
| 161 | 協作投影片能匯出 PowerPoint；會議外掛程式是測試版，Pro 和 Business。 | pro-five / a4qu | R:104, 117 | 200 capture | confirmed (sampled) | CONFIRMED | Beta 版開放 Pro 和 Business |
| 162 | AI 代理怎麼運作、怎麼失敗，上一支講過了；這裡只講 dots 的額度，和三條界線。 | wheel-alone / a8fd | AOA:18, 730 | repo | changed | CONFIRMED | 「上一支」全片只在這一句，指 AI 代理那一支；額度＝dot-big，三條界線＝locked-cabinet |
| 163 | dots 頁 2026-09-29 | dot-big.data.kicker | DOTS:5 | 200 capture | confirmed (sampled) | CONFIRMED |  |
| 165 | 第一個 dot 不另收費；推出後第一個月上限較高 | dot-big.data.sub | DOTS:96 | 200 capture | confirmed (sampled) | CONFIRMED |  |
| 168 | 空間的頁面也一樣，你改一筆，同事接著改；分享頁面不會分享你的私人對話。 | two-hands-bowl / aiiz | SPACE:15, 26 | 200 capture | confirmed (sampled) | CONFIRMED | 同段「頁上寫的都看得到」沒帶到（第一輪已列） |
| 170 | Pro 現在有三階（說明中心，2026-10-03 查閱） | pro-table.data.title | PRO:5, 19–25 | 200 capture | narrowed | CONFIRMED | 三階成立；不帶更新日 |
| 171 | 級別 | pro-table.data.columns[0] | PRO:21 | 200 capture | confirmed (sampled) | CONFIRMED |  |
| 175 | $100 | pro-table.data.rows[0][1] | PRO:23 | 200 capture | confirmed (sampled) | CONFIRMED |  |
| 179 | 不含 | pro-table.data.rows[1][2] | PRO:24 | 200 capture | confirmed (sampled) | CONFIRMED | Not included |
| 184 | Pro 只能月繳；點數適用 Codex、ChatGPT 工作、ChatGPT for Word／Excel／PowerPoint… | pro-table.data.note | PRO:50, 58, 71 | 200 capture | confirmed (sampled) | CONFIRMED | 三句都在 |
| 187 | 所以 Pro 500 買到的是速度和最高額度，不是更聰明的模型。 | three-kilns / b3ja | PRO:27；R:130；SPEED:18；BRIEF:31 | 200 capture；repo | confirmed (sampled) | CONFIRMED | 事實部分成立；結論是站主的看法 |
| 189 | 9/22 到 9/29 上午 10 點之間訂閱有效過 | pro200-steps.data.steps[0].title | PRO:37, 44 | 200 capture | changed | CONFIRMED | had an active Pro 200 subscription at any point |
| 191 | 舊額度留到 10/29 | pro200-steps.data.steps[1].title | PRO:37 | 200 capture | confirmed (sampled) | CONFIRMED | through October 29, 2026 |
| 192 | 2026-10-29，訂閱維持中才有 | pro200-steps.data.steps[1].detail | PRO:37 | 200 capture | confirmed (sampled) | CONFIRMED | while their Pro 200 subscription is active |
| 193 | 之後換新額度 | pro200-steps.data.steps[2].title | PRO:38 | 200 capture | confirmed (sampled) | CONFIRMED | the lower included usage allowance |
| 194 | 月費不變，仍是 $200 | pro200-steps.data.steps[2].detail | PRO:38 | 200 capture | confirmed (sampled) | CONFIRMED | stays at $200/month |
| 197 | 說明中心，2026-10-03 查閱；受影響的人會收到 email | pro200-steps.data.note | PRO:5, 38 | 200 capture | narrowed | CONFIRMED | email 成立；不帶更新日 |
| 198 | 9 月 22 日到 29 日上午 10 點之間有訂閱的，舊額度留到 10 月 29 日。 | pro200-steps / bdwn | PRO:37 | 200 capture | changed | CONFIRMED | 同字卡；「訂閱維持中才有」在字卡第 2 步，太平洋時間在第 1 步 |
| 203 | GPT-6 Astra Ultrafast | rate-stats.data.stats[0].label | PRO:66；SPEED:20 | 200 capture | confirmed (sampled) | CONFIRMED |  |
| 206 | 每天用 Ultrafast 跑 10 件，等於標準模式幾件的額度 | rate-stats.data.stats[1].label | PRO:66 | 200 capture | confirmed (sampled) | CONFIRMED | 10 × 8＝80 是影片的算術 |
| 208 | 說明中心與 Speed 頁 2026-10-03：額度消耗率，不是速度保證；每階能跑幾件，這兩頁沒寫，以官網的方案比較頁為準 | rate-stats.data.source | PRO:27–28, 66；SPEED:24 | 200 capture | narrowed | CONFIRMED | 兩頁都把件數指到沒擷取的價格頁；「這兩頁沒寫」剛好是來源撐得住的範圍 |
| 210 | 每天跑 10 件就是標準 80 件的額度；每階能跑幾件，這兩頁沒寫，以官網為準。 | rate-stats / bra3 | PRO:27–28, 66；SPEED:24 | 200 capture | narrowed | CONFIRMED | 同字卡；10 × 8＝80 |
| 211 | 你可能會問，我每天用 Codex 兩三個小時，該選哪一階？ | glaze-shelf / bswh | BRIEF:76 | repo | changed | CONFIRMED | 企劃設計的問題 |
| 213 | 等的時間值不值這八倍，只有你的量算得出來。 | cat-step / bzus | PRO:66 | 200 capture | confirmed (sampled) | CONFIRMED | 八倍＝8 份額度；結論是看法 |
| 218 | 公司帳號多的五項，和 Codex Security Cloud 的五步 | ch5.data.subtitle | R:41, 87, 109, 113, 135 | 200 capture | changed | CONFIRMED | 五項的那一行逐一重對：只有兩項寫 Business 和 Enterprise |
| 219 | 公司或團隊的帳號，多了五項。 | ch5 / d4k8 | R:41, 87, 109, 113, 135 | 200 capture | changed | CONFIRMED | 同副標 |
| 220 | 在 Slack 或 Teams 裡提到 ChatGPT，它就接手，像主廚隔著出菜口喊一聲。 | kitchen-wide / d5ct | R:112 | 200 capture | confirmed (sampled) | CONFIRMED |  |
| 225 | **私密智慧**：API 的零資料保留搭配私密安全處理，按專案開、先取得 ZDR 核准；私密推論是預覽版 | team-five.data.items[3] | R:41；PSP:971, 974 | 200 capture；200 curl | changed | CONFIRMED | 今天重抓 PSP 指南（200，逐位元相同）：per project、API console、先有 ZDR 核准都在 |
| 226 | **OpenAI 市集 Beta**：符合資格的企業客戶 | team-five.data.items[4] | R:135 | 200 capture | confirmed (sampled) | CONFIRMED |  |
| 227 | 回顧頁與 API 指南的寫法，2026-10-03；細節以官網為準 | team-five.data.note | R:5；PSP:930 | 200 capture；200 curl | confirmed (sampled) | CONFIRMED |  |
| 229 | 可連結外掛程式的工作站、私密智慧，和 OpenAI 市集的測試版。 | team-five / dg29 | R:85, 40, 133 | 200 capture | confirmed (sampled) | CONFIRMED |  |
| 230 | 工作站的意思是，同一個應用程式，每個人帶自己的刀，用自己的權限登入。 | own-knife / dhff | R:86 | 200 capture | confirmed (sampled) | CONFIRMED | 以各自的權限登入…操作同一個應用程式 |
| 231 | 團隊任務像出菜鈴，時間到了，或情況變了，就往下一站送。 | bell-tray / dw68 | R:108 | 200 capture | confirmed (sampled) | CONFIRMED | 依排程或在情況有變化時 |
| 232 | 沒有授權的同事也能補一張單子；零資料保留按 API 專案開，細節以官網為準。 | blank-board / dyna | R:112；PSP:971 | 200 capture；200 curl | changed | CHANGED | 沒有授權的同事也能補一張單子；私密智慧按 API 專案開，細節以官網為準。 → 沒有授權的同事也能補一張單子；零資料保留按 API 專案開，細節以官網為準。 〔「按專案開」是指南對 ZDR with PSP 說的（PSP:971）；私密智慧的另一半（私密推論預覽版）怎麼開沒有來源，口播比來源和字卡寬。改完多 1 個口播單位〕 |
| 234 | 安裝外掛程式 | security-steps.data.steps[0].title | SEC:41 | 200 capture | confirmed (sampled) | CONFIRMED |  |
| 238 | 一次性掃描 | security-steps.data.steps[2].title | SEC:43 | 200 capture | confirmed (sampled) | CONFIRMED | One-Time Scan |
| 240 | 看發現，Fix with Codex | security-steps.data.steps[3].title | SEC:44 | 200 capture | confirmed (sampled) | CONFIRMED |  |
| 241 | 先看補丁，再出草稿提取要求 | security-steps.data.steps[3].detail | SEC:44 | 200 capture | confirmed (sampled) | CONFIRMED | Review the patch before selecting Create draft pull request |
| 243 | 持續檢查新的提交；整個存放庫也能隨需或依排程掃 | security-steps.data.steps[4].detail | R:59–60；SEC:45 | 200 capture | changed | CONFIRMED | 整項適用於所有 Codex 使用者 |
| 245 | Codex Security Cloud 的五步：裝外掛程式，連 GitHub，跑一次性掃描。 | security-steps / e4t5 | SEC:41–43 | 200 capture | confirmed (sampled) | CONFIRMED |  |
| 246 | 看發現，看過再出草稿提取要求；再開持續掃描，整個存放庫也能排程掃。 | security-steps / e5gx | SEC:44–45；R:59 | 200 capture | changed | CONFIRMED | Review the patch before selecting Create draft pull request |
| 250 | Enterprise 的 Ultrafast **預設關**；要美國以外推論駐留的工作區不開放 | company-two.data.items[1] | SPEED:21, 26 | 200 capture | confirmed (sampled) | CONFIRMED |  |
| 253 | 第二件，Enterprise 的 Ultrafast 預設關；要美國以外推論駐留的不開放。 | company-two / ewnp | SPEED:21, 26 | 200 capture | confirmed (sampled) | CONFIRMED |  |
| 254 | 市集，用既有合約的承諾支出買夥伴的軟體；首批 32 家是 OpenAI 自己的數字。 | back-door / exwz | R:134 | 200 capture | confirmed (sampled) | CONFIRMED | 32 家標明是 OpenAI 的數字；原文是承諾支出的「一部分」、買「已核准的」夥伴軟體，口播省了這兩個詞，見摘要 |
| 255 | 市集現在是測試版，誰符合資格以官網為準。 | pass-window / ey9z | R:135 | 200 capture | confirmed (sampled) | CONFIRMED |  |
| 259 | 開發者的清單：三個數字 | ch6.data.title | BRIEF:31；SELF | repo；— | confirmed (sampled) | CONFIRMED |  |
| 264 | 五分之一・**六倍**・五百美元 | three-numbers.data.text | PRICE:913–914, 949；PRO:25 | 200 curl；200 capture | confirmed (sampled) | CONFIRMED | 2÷10、60÷10、$500 |
| 266 | Sol 的牌價、Ultrafast 的牌價，和 Pro 500 的月費。 | three-numbers / fgw6 | PRICE:913–914, 949；PRO:25 | 200 curl；200 capture | confirmed (sampled) | CONFIRMED |  |
| 273 | $50 → $300 | uf-stats.data.stats[2].value | PRICE:913, 949 | 200 curl | confirmed (sampled) | CONFIRMED |  |
| 275 | developers.openai.com 價目表 2026-10-03；長脈絡 $120／$12／$450；Ultrafast… | uf-stats.data.source | PRICE:946–949 | 200 curl | confirmed (sampled) | CONFIRMED | 長脈絡 120／12／450；表裡只有 gpt-6-astra（腳本比對） |
| 278 | 它賣的是速度；OpenAI 說 Codex 裡最高八倍，API 的倍數兩頁不同，以官網為準。 | scooter / fzis | R:36；UF:927 | 200 capture；200 curl | confirmed (sampled) | CONFIRMED | 8 倍是 OpenAI 的說法；6 倍對 up to 8x |
| 281 | Codex 最高 8 倍、每秒 300 token | speed-vs-money.data.left.points[0] | R:36 | 200 capture | confirmed (sampled) | CONFIRMED |  |
| 284 | 它收的是錢 | speed-vs-money.data.right.heading | SELF | — | confirmed (sampled) | CONFIRMED |  |
| 291 | 再看五分之一。另一支算過整月帳單，Astra 約 348 美元，GPT-6 Sol 約 70。 | scale-hands / guna | G6:12 | repo | changed | CONFIRMED | 「另一支」＝gpt6-vs-opus55-worth-paying；12×12.5＋48×1＋3×50＝348、12×2.5＋48×0.2＋3×10＝69.6 重算過 |
| 292 | GPT-6.1 Sol 的牌價，每百萬 token，2026-10-03 | sol-price.data.kicker | PRICE:914 | 200 curl | confirmed (sampled) | CONFIRMED |  |
| 293 | 輸入 $2、輸出 $10 ⏎ Astra 的**五分之一** | sol-price.data.text | PRICE:913–914；MODEL:957–967 | 200 curl | confirmed (sampled) | CONFIRMED | 2÷10＝10÷50＝0.2 |
| 295 | GPT-6.1 Sol 的牌價是 Astra 的五分之一，快取輸入是十分之一。 | sol-price / gyue | PRICE:913–914 | 200 curl | confirmed (sampled) | CONFIRMED | 0.10÷1.00＝0.1 |
| 296 | 該不該換 Sol？那一支的公式改一個數字；不是我替你選，是你的帳單替你選。 | coins-count / gznr | G6:12；PRICE:914 | repo；200 curl | changed | CONFIRMED | 只差快取輸入（0.20 → 0.10），「改一個數字」成立：12×2.5＋48×0.1＋3×10＝64.8 |
| 297 | 再來三件事，API 的人直接用得到；Agents API 像把攤子交給幫手，底層由 OpenAI 代管。 | hand-over / h2gh | R:66–69；AG:39 | 200 capture | changed | CONFIRMED | 三件事＝卡上三條 |
| 298 | API 直接用得到的三件事 | api-three.data.title | R:66–69 | 200 capture | changed | CONFIRMED | Agents API 與它的電腦操作在回顧頁是同一個標題 |
| 302 | Ultrafast 指南、Agents API 頁、回顧頁，2026-10-03 | api-three.data.note | UF:925；AG:3；R:5 | 200 curl；200 capture | confirmed (sampled) | CONFIRMED |  |
| 303 | Astra 的 Ultrafast 在 API 所有人能開；Agents API 只付 token 和工具。 | api-three / h6xm | UF:934–935；AG:57 | 200 curl；200 capture | confirmed (sampled) | CONFIRMED | 口播省了「速率上限低」，字卡有 |
| 308 | **Amazon Bedrock Managed Agents**：給在 AWS 上開發的團隊 | dev-three.data.items[1] | R:72；BED | 200 capture；200 curl | confirmed (sampled) | CONFIRMED |  |
| 309 | **MCP 事件**：提議中的規格；回顧頁寫適用於所有方案 | dev-three.data.items[2] | R:90–91；MCP | 200 capture；200 curl | confirmed (sampled) | CONFIRMED |  |
| 310 | 回顧頁 2026-09-29；回顧頁沒附 Decisions API 與 Bedrock 的文件連結 | dev-three.data.note | R:64, 73；BED | 200 capture；200 curl | changed | CONFIRMED | Bedrock 文件頁今天仍是 200；回顧頁兩項都「無連結」 |
| 313 | 開發者的清單就這些，照回顧頁算是四項，看牌價。 | lights-off / ier5 | R:35, 62, 66, 71 | 200 capture | changed | CONFIRMED | 極速、Decisions API、Agents API 中的電腦操作功能、Bedrock |
| 314 | 這週該先做哪件事？ | lights-off / ik64 | SELF:week-steps | — | changed | CONFIRMED | 四步，沒有團隊那一步 |
| 315 | 這週做的一件事，和還不能碰的 | home-table.chapter | SELF | — | confirmed (sampled) | CONFIRMED |  |
| 316 | 最後，這週先做一件事。 | home-table / imik | SELF:week-steps | — | changed | CONFIRMED | 同 ik64 |
| 317 | 這週做的一件事 | week-steps.data.title | SELF | — | confirmed (sampled) | CONFIRMED |  |
| 319 | 姓名、電子郵件、個人檔案照片；第二個請求要就設上限 | week-steps.data.steps[0].detail | SIWC:27, 31 | 200 capture | confirmed (sampled) | CONFIRMED |  |
| 320 | Plus：10/14 前在 Codex 改選一個還在的模型 | week-steps.data.steps[1].title | SPEED:32 | 200 capture | confirmed (sampled) | CONFIRMED | October 14, 2026，all plans；會過期 |
| 322 | Pro：有 dot 的人設一件要先核准；Pro 200 看我的方案 | week-steps.data.steps[2].title | DOTS:76；PRO:69 | 200 capture | narrowed | CONFIRMED | 沒有引號；頁面的字是「要求先取得核准」與 My Plan |
| 325 | Sol 對 Astra 的月帳單，用另一支的公式 | week-steps.data.steps[3].detail | G6:12 | repo | changed | CONFIRMED | 同 guna |
| 332 | 還不能碰的 | not-yet.data.title | SELF | — | confirmed (sampled) | CONFIRMED |  |
| 336 | **Decisions API 全面開放** | not-yet.data.items[3] | R:64；LLMS；CHG | 200 capture；200 curl | confirmed (sampled) | CONFIRMED | 今天重抓文件索引與 changelog（和第一輪逐位元相同），仍沒有 Decisions 項目；/guides/decisions 與 /guides/decisions-api 仍是 404；會過期 |
| 339 | 回顧頁、空間頁、dots 頁寫「即將推出」的，2026-10-03；Sol 頁寫法不同 | not-yet.data.note | R:37, 117, 121；SPACE:10, 23；DOTS:60；SOL:55 | 200 capture | changed | CONFIRMED | Sol 頁全文沒有「即將推出」（腳本比對）；Decisions API 那一項回顧頁寫的是「預計未來幾天內全面推出」（R:64），意思相同，沒動，見摘要 |
| 341 | Decisions API 的全面開放，dots 的簡訊，個人檔案的 Enterprise、Edu、Healthcare 版。 | not-yet / j8m9 | R:64, 121；DOTS:60 | 200 capture | confirmed (sampled) | CONFIRMED |  |
| 342 | 加起來，25 項，每一項都有它的位置。 | window-street / j9ty | R:27–133 | 200 capture | confirmed (sampled) | CONFIRMED |  |
| 345 | 所有人：沒限定付費方案 | tally-stats.data.stats[0].label | R:48, 52, 56, 60, 79, 83, 91, 121, 127 | 200 capture | changed | CHANGED | 所有人：沒指定付費方案 → 所有人：沒限定付費方案 〔同 3qfi〕 |
| 346 | +1 | tally-stats.data.stats[1].value | SOL:53 | 200 capture | confirmed (sampled) | CONFIRMED |  |
| 347 | Plus：GPT-6.1 Sol | tally-stats.data.stats[1].label | SOL:53 | 200 capture | confirmed (sampled) | CONFIRMED |  |
| 349 | Pro：4 項、dots 看市場、Pro 500 一階 | tally-stats.data.stats[2].label | R:97, 101, 105, 117, 29, 130 | 200 capture | confirmed (sampled) | CONFIRMED | 4＋1＋1 |
| 350 | +9 | tally-stats.data.stats[3].value | R:41, 87, 109, 113, 135, 35, 62, 66, 71 | 200 capture | confirmed (sampled) | CONFIRMED | 5＋4；9＋1＋6＋9＝25 |
| 352 | Codex Security Cloud 與 MCP 事件只算在所有人的九項裡；Agents API 和它的電腦操作在回顧頁是同… | tally-stats.data.source | R:60, 91, 66–69 | 200 capture | changed | CONFIRMED | 9＋1＋6＋9＝25 的算法寫清楚了 |
| 353 | 官網沒限定付費方案的有 9 項，Plus 再加 Sol 一項。 | tally-stats / ja8a | R:48, 52, 56, 60, 79, 83, 91, 121, 127 | 200 capture | changed | CHANGED | 官網沒指定付費方案的有 9 項，Plus 再加 Sol 一項。 → 官網沒限定付費方案的有 9 項，Plus 再加 Sol 一項。 〔同 3qfi；和 Short 1 的同一句逐字相同〕 |
| 354 | Pro 加 4 項、dots 看市場、Pro 500 算一項；團隊 5、開發者 4，一共 25。 | tally-stats / jg96 | R:27–133 | 200 capture | confirmed (sampled) | CONFIRMED | 9＋1＋4＋1＋1＋5＋4＝25 |
| 357 | 沒限定付費方案的 9 項 | outro.data.lines[0] | R:48, 52, 56, 60, 79, 83, 91, 121, 127 | 200 capture | changed | CHANGED | 沒指定付費方案的 9 項 → 沒限定付費方案的 9 項 〔同 3qfi〕 |
| 360 | 團隊 5 項・開發者 4 項看牌價 | outro.data.lines[3] | R:41, 87, 109, 113, 135, 35, 62, 66, 71 | 200 capture | confirmed (sampled) | CONFIRMED |  |
| 364 | DevDay 發表了二十幾樣，官網沒限定付費方案的有 9 項：照方案分五張清單 | shorts[0].titles[1] | R:15, 48, 52, 56, 60, 79, 83, 91, 121, 127 | 200 capture | changed | CHANGED | DevDay 發表了二十幾樣，官網沒指定付費方案的有 9 項：照方案分五張清單 → DevDay 發表了二十幾樣，官網沒限定付費方案的有 9 項：照方案分五張清單 〔同 3qfi〕 |
| 365 | DevDay 2026 的回顧頁列了 25 項，你今天打開 ChatGPT 碰得到幾項？答案在你付的是哪一種方案：官網沒限定付費… | shorts[0].description | R:27–133；SOL:53 | 200 capture | changed | CHANGED | …官網沒指定付費方案的有 9 項… → …官網沒限定付費方案的有 9 項… 〔同 3qfi；「這週先做哪件事」成立〕 |
| 372 | 沒限定付費方案的 9 項，Plus 再加 Sol | shorts[0].scenes[2].headline | R:48, 52, 56, 60, 79, 83, 91, 121, 127 | 200 capture | changed | CHANGED | 沒指定付費方案的 9 項，Plus 再加 Sol → 沒限定付費方案的 9 項，Plus 再加 Sol 〔同 3qfi〕 |
| 373 | 9 項 | shorts[0].scenes[2].big | R:48, 52, 56, 60, 79, 83, 91, 121, 127 | 200 capture | confirmed (sampled) | CONFIRMED |  |
| 374 | 官網沒限定付費方案的有 9 項，Plus 再加 Sol 一項。 | shorts[0].scenes[2].narration[0] | R:48, 52, 56, 60, 79, 83, 91, 121, 127 | 200 capture | changed | CHANGED | 官網沒指定付費方案的有 9 項，Plus 再加 Sol 一項。 → 官網沒限定付費方案的有 9 項，Plus 再加 Sol 一項。 〔同 ja8a〕 |
| 375 | Sol 在 ChatGPT 工作和 Codex 裡能選，對話裡還沒有。 | shorts[0].scenes[2].narration[1] | SOL:53 | 200 capture | confirmed (sampled) | CONFIRMED |  |
| 380 | 這週先做哪件事，完整的在長片。 | shorts[0].scenes[4].narration[0] | SELF:week-steps | — | changed | CONFIRMED | 同 ik64 |
| 381 | 每月五百美元的 Pro 500，買到的不是更聰明的模型 | shorts[1].titles[0] | PRO:25, 27；BRIEF:31 | 200 capture；repo | confirmed (sampled) | CONFIRMED | 看法，和站主觀點一致 |
| 387 | Pro 三階，只有 Pro 500 含 Ultrafast | shorts[1].scenes[1].headline | PRO:21–25 | 200 capture | confirmed (sampled) | CONFIRMED |  |
| 389 | Pro 現在有三階。 | shorts[1].scenes[1].narration[0] | PRO:21–25 | 200 capture | confirmed (sampled) | CONFIRMED |  |
<!-- end of claim table -->

## Summary

**Claims re-checked:** 157 strings (55 changed or narrowed by round 1 + 102 sampled from its confirmed rows). **Confirmed:** 144 (42 of the 55, and all 102 sampled). **Changed:** 13 strings, which are 4 facts and their dependants; all 13 are strings round 1 had rewritten. **Not found:** 0. No number, price, multiplier, date, plan name or count changed in this round: the four fixes narrow wording round 1 introduced or left that still said a little more, or a little less, than the source.

**Further fact changes (where | before → after | source):**

1. ch2.subtitle, pool-desk/3qfi, lane-wide/4py7, tally-stats.stats[0].label, tally-stats/ja8a, outro.lines[0], Short 1 (title 2, description, scene 2 headline and narration) | 「沒指定付費方案」「沒有指定付費方案」「也沒指定付費方案」 → 「沒限定付費方案」「沒有限定付費方案」「也沒限定付費方案」 | R:121: the availability line of 可分享的個人檔案 names three plans (「即將向 ChatGPT Enterprise、Edu 和 Healthcare 逐步推出，目前已適用於所有其他 ChatGPT 方案」). Round 1 put those three names on the five-more card and, one line earlier, had 4py7 say the five items' lines 「也沒指定付費方案」: narration and card no longer agreed. What the nine lines have in common is that none restricts its item to a paid plan (R:48, 52, 56, 60, 79, 83, 91, 121, 127), which 「沒限定」 says and the profile line does not contradict. Same spoken units in all three lines.
2. blank-board/dyna | 「…；私密智慧按 API 專案開，細節以官網為準。」 → 「…；零資料保留按 API 專案開，細節以官網為準。」 | PSP:971 "ZDR with PSP is enabled per project." The guide says this of zero data retention with Private Safety Processing only; 私密智慧 is that plus the Private Inference preview (R:41), and no captured or fetched page says how Private Inference is enabled. The team-five card already scopes it correctly (「API 的零資料保留搭配私密安全處理，按專案開」) and so does brief.md:140. 31 → 32 spoken units.
3. youtube.description | 「官方頁之間寫得不一樣的地方（Codex 雲端的適用方案、…）」 → 「官方頁寫得不一樣的地方（Codex 雲端的適用方案、…）」 | R:47–48: the two wordings for Codex 雲端 are two lines of one page, as the script itself says (codex-four 「同一段也寫 Plus 以上」, 4fu7 「Codex 雲端那一段」); "between pages" is true of the other four places only.
4. pro-five.items[1] | 「行動版，空間頁寫只能看、回顧頁寫即將推出」 → 「行動版，空間頁寫可檢視、回顧頁寫即將推出」 | SPACE:23 「並在行動版上檢視」, SPACE:31 「在行動版上，你可以尋找、閱讀及分享頁面；推出時尚不支援建立及編輯頁面」: the page allows more than viewing on mobile, so 「只能看」 was narrower than the page. The narration (a3tb) never said it and is unchanged.

`claims.md` follows all four (c2, c24, c42, the three closing sections); `sources[]`, the thumbnail and the title are not affected.

**Round 1's fixes, re-checked:**

- *Wording against the source.* The other 42 changed or narrowed strings say what their source lines say: sign-in 「登入本身不給」 (SIWC:32, 36), Pro 200 「訂閱有效過」「有訂閱的」 (PRO:37), 「這兩頁沒寫」 (PRO:27–28, SPEED:24), 「公司帳號多的五項」 (R:41, 87, 109, 113, 135), the security card and line (R:59–60, SEC:44–45), 「三件事」 and 「照回顧頁算是四項」 (R:35, 62, 66–69, 71), the not-yet note (the Sol page never says 「即將推出」), the three source titles, the three earlier videos' titles (identical to each `youtube.title`), and the dateless 「說明中心，2026-10-03 查閱」.
- *Dependants.* None of the wordings round 1 removed is left anywhere in `video.json` or `shorts.json` (checked by script: 登入就有, 永遠不給, 一律不給, 訂過, 同一頁, 每個人都會碰到, 每一張清單, 2026-10-02, 有人問, 按一下, 官方沒, Working Group, 清單最長, 以 ChatGPT 繼續). The thumbnail and the title carry none of the changed claims. `claims.md` has 61 claims for 61 ids, all 48 quoted English sentences verbatim in the captures, and quotes the lines as they now read. All 15 sources are https and checked 2026-10-03.
- *Counts.* 4+7+4+7+3 = 25 on the recap; 9+1+6+9 = 25 on the tally card and 9+1+4+1+1+5+4 = 25 in jg96; 6+3 and 4+5 make the nine; every list card has as many items as its lines reveal (five-more 5, pro-five 5, team-five 5, api-three 3, dev-three 3, not-yet 6, week-steps 4, login 5, security 5, Pro 200 4); 「三件事」 has three bullets and 「四項」 is 極速, Decisions API, Agents API 中的電腦操作功能, Bedrock; nothing promises a fifth step in week-steps any more.
- *「上一支／另一支」.* 「上一支」 is said once (a8fd) and points at always-on-agent-explained, whose subject is AI agents; 「另一支」 (guna), 「那一支」 (gznr) and the week-steps card point at gpt6-vs-opus55-worth-paying, where $348 and $69.60 are (c8); 「改一個數字」 holds (only cached input differs, 0.20 → 0.10). The description's header names both and marks the third video as not mentioned.
- *Cards against narration, scene against scene.* Apart from fix 1 and fix 2 above I found no pair that disagrees: three-vs (title, heading, 6bae) against card-closeup 「只有三樣」; pro-five against not-yet on mobile and on slides; pro200-steps card against bdwn and bekc; security-steps card against e4t5 and e5gx; nine-stats against codex-four and five-more.

**Brief conflicts (the source wins; `brief.md` is untouched):** in addition to round 1's list, brief.md:76, :96 and :138 say 「行動版只能看」 (the space page: view, find, read and share; the recap: mobile coming soon). The narrowed dyna agrees with brief.md:77 and :140. The outline still holds.

**Facts that expire soon (the official date I saw):** unchanged from round 1 and re-read today. GPT-5.5 leaves ChatGPT, ChatGPT 工作 and Codex on 2026-10-14 (SPEED:32). Pro 200's old allowance lasts through 2026-10-29 (PRO:37). Decisions API: 「今日起限量開放預覽，預計未來幾天內全面推出」 on a page dated 2026-09-29 (R:64); today the two documentation indexes and the changelog are byte-identical to round 1's copies and still have no Decisions entry, so 「限量預覽」 stays; re-open before upload. dots: higher cap in the first month after 2026-09-29, rollout by market (DOTS:94, 96). GPT-6.1 Sol Ultrafast 「即將推出」 (R:37); the Ultrafast price table lists only gpt-6-astra today. Mobile editing and slide collaboration in 空間, the meeting plugin for Enterprise, profiles for Enterprise, Edu and Healthcare and dots by SMS are all 「即將推出」. The Help Center pages carry no dated changelog. All three earlier videos still have `video_id` null.

**Opinion mismatches:** none; nothing in this round touched an opinion. Round 1's list stands (marked: 53vp, bsx5, gznr, 2mr4, jpxt; consistent with 站主觀點 but not marked: 6npj, b3ja, fezv and the three-numbers kicker, jr8w).

**Listener findings (report only):**

- No line is over 40 spoken units (longest j8df, 34); 26 lines are over 40 raw characters. No 經查證／根據官方文件／本影片, no parentheses or URLs in the narration, no `say` fields, every Latin term in the dictionary (lint), no reveal before its sentence.
- After fix 2, dyna says 「零資料保留」 and no longer repeats 「私密智慧」; the link is the team-five card three scenes earlier (dg29 names the item). A wording that keeps both (「私密智慧的零資料保留按 API 專案開」) is 37 units and would hold the blank-board picture about 10 s on the estimate, so I did not use it.
- 「以官網為準」 is still spoken nine times.
- Round 1's other findings stand (bra3 「這兩頁」; fezv 「全部」 against the 10% uplift; emau, bdwn, h9w3 narrower than their cards; Codex Cloud／Codex 雲端, 智慧體／AI 代理, GPT-6 Sol two lines before GPT-6.1 Sol).

**Lint after the edits:** `node tools/video/cli.mjs lint --slug openai-devday-2026-recap` → `openai-devday-2026-recap: 0 errors, 21 warnings`; `Estimate: 11.7 min, 111 lines, 2551 spoken units` (before this round: 2550). The warnings are the same 21 cadence warnings; one figure moved (blank-board state 0: 8.5 → 8.7 s). `shorts.json` passes the worker's check (`episodeShortsProblems`) and stays within 110–220 spoken characters. Scene ids, templates, line ids, reveals and shot data are unchanged (9 leaf values of `video.json` and 4 of `shorts.json` differ from before this round).

**Suspected, not changed:**

- (a) Short 1 says 「官網沒限定付費方案的有 9 項」 without the long video's caveat for Codex 雲端, whose paragraph also lists Plus to Enterprise (R:47; the long video says so in 4fu7 and on codex-four). The Short names no item, so I left it; a sixth scene or a longer line would be a rewrite.
- (b) The description says 「價格、倍數和日期都是 OpenAI 自己頁面上的」. The allowance and credit multipliers (8, 6, 2.5, 2) and 五分之一 are printed on OpenAI's pages; the API 六倍 and the cached-input 十分之一 are ratios of two printed prices (the pricing page never writes "6x"; claims.md c49 and c54 say so). The description's own parenthesis defines 六倍 as a reading of the price table, so I left the sentence.
- (c) The description still writes 「訂閱共用」 in 「」. It is the help page's term "subscription sharing" translated, not an interface label; round 1 removed 「」 only where they read as interface labels.
- (d) The not-yet card's small print says its items are what the pages call 「即將推出」; for Decisions API the recap's words are 「預計未來幾天內全面推出」 (R:64), and for profiles 「即將向…逐步推出」 (R:121). Same meaning.
- (e) five-more.items[2] quotes 「正加入支援」; the recap's sentence is 「我們正加入對提議中的 MCP 事件規格的支援」 (R:90), so the quotation is a contraction.
- (f) exwz says committed spend buys partners' software; the recap says 「承諾支出的一部分」 and 「已核准的合作夥伴軟體」 (R:134).
- (g) imw5 「要不要勾第二個」 pictures a checkbox; the help page only says a tool "can separately request permission" (SIWC:27).
- (h) Round 1's items (a), (c), (d), (e), (f), (g), (h), (i) and (j) still stand: the chapter name 「每個人都有的九項」; $348 and $70 resting on another video's 2026-09-28 prices; 「上一支」 assuming that video is published first; 「我的方案」 for "My Plan"; the space page's caveat that everything written on a shared page is visible; one of three reasons for a missing button; scheduled whole-repository scans resting on the recap only; the guide's "preview access for GPT-5.6 Sol"; re-opening the Help Center pages before upload. Its item (b) is fixed (fix 3).

**A FURTHER ROUND:** by the rule's letter (more than three fact changes in a round) yes: this round made four. None of them changes a number, a price, a date, a plan or an availability statement; each replaces one word or one subject in wording round 1 wrote or kept. No claim is unresolved; the facts that will expire are listed above.
