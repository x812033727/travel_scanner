# Verification round 1: openai-devday-2026-recap

Verifier: claude-fable-5-1, a separate agent session from the writer's and from the one that finished `claims.md` and `shorts.json`, 2026-10-03. I extracted every string of `video.json` (362) and `shorts.json` (37) first, then opened the source for each one. `openai.com`, `help.openai.com`, `chatgpt.com` and `learn.chatgpt.com` answer 403 to curl, so for those hosts the source is the coordinator's browser capture of 2026-10-03 (`_tools/sources/`, read line by line; I did not fetch those hosts and used no browser). `developers.openai.com` and `modelcontextprotocol.io` were fetched today with the editorial user agent, at least 1.2 s apart; the four captured developer pages came back byte-identical to the captures. Web searches used: 0 of 5. Three report-only checkers (numbers, availability, names and attribution) had already gone through the script; I used their findings as leads and re-read the source lines before applying anything.

Helper files are in `<VIDEO_WORKDIR>/openai-devday-2026-recap/_tools/verify/round1/`: `extract-before.tsv` (the claim list, written before checking), `apply.mjs` and `apply2.mjs` (every edit asserts the text it replaces), `applied.json` (59 edits, before and after), `table.mjs` (the verdict for every string; it stops when a string has none), `claims-doubts.mjs`, the pages fetched today, `video.before.json`, `shorts.before.json`, `claims.before.md` and the lint outputs.

## Pages opened

| key | URL or file | HTTP | How it was read |
| --- | --- | --- | --- |
| R | https://openai.com/zh-Hant/index/devday-2026-recap/ | 200 capture | `sources/devday-2026-recap.zh-Hant.md`; page dated 2026-09-29; 25 `###` items (4+7+4+7+3), the page itself says 「超過 20 項」; no 「免費」 or "Free" anywhere |
| SOL | https://openai.com/zh-Hant/index/introducing-gpt-6-1-sol/ | 200 capture | `sources/introducing-gpt-6-1-sol.zh-Hant.md`; 2026-09-29; never says 「即將推出」 |
| DOTS | https://openai.com/zh-Hant/index/introducing-dots/ | 200 capture | `sources/introducing-dots.zh-Hant.md`; 2026-09-29 |
| AG | https://openai.com/zh-Hant/index/introducing-the-agents-api/ | 200 capture | `sources/introducing-the-agents-api.zh-Hant.md`; 2026-09-10; 公開測試版 |
| PRO | https://help.openai.com/en/articles/9793128-about-chatgpt-pro-tiers | 200 capture | `sources/help-about-chatgpt-pro-tiers.en.md`; the page shows only "Updated: yesterday" |
| SIWC | https://help.openai.com/en/articles/20001410-sign-in-with-chatgpt | 200 capture | `sources/help-sign-in-with-chatgpt.en.md`; "Updated: yesterday" |
| SPEED | https://learn.chatgpt.com/docs/agent-configuration/speed | 200 capture | `sources/learn-chatgpt-speed-and-cloud.en.md` lines 5–32 |
| CLOUD | https://learn.chatgpt.com/docs/cloud | 200 capture | the same file, lines 34–54 |
| SEC | https://learn.chatgpt.com/docs/security/setup | 200 capture | `sources/chatgpt-space-and-codex-security-cloud.md` lines 33–45 |
| SPACE | https://chatgpt.com/zh-Hant/features/space/ | 200 capture | the same file, lines 5–31 |
| PRICE | https://developers.openai.com/api/docs/pricing | 200 curl | fetched today, byte-identical to the capture; line numbers are of `sources/developers_openai_com_api_docs_pricing.txt` |
| MODEL | https://developers.openai.com/api/docs/models/gpt-6.1-sol | 200 curl | fetched today, byte-identical; `…models_gpt-6_1-sol.txt` |
| UF | https://developers.openai.com/api/docs/guides/ultrafast-mode | 200 curl | fetched today, byte-identical; `…guides_ultrafast-mode.txt` |
| PSP | https://developers.openai.com/api/docs/guides/private-safety-processing | 200 curl | fetched today, byte-identical; `…guides_private-safety-processing.txt` |
| MCP | https://modelcontextprotocol.io/community/working-groups/triggers-events | 200 curl | H1 "Triggers and Events Charter"; "Charter for the MCP Triggers and Events Working Group"; its SEP is still "Ideating" |
| BED | https://developers.openai.com/api/docs/guides/agents-api/bedrock-managed-agents | 200 curl | an official page exists today (H1 "Bedrock Managed Agents"); no claim of the script rests on it |
| CU | https://developers.openai.com/api/docs/guides/agents-api/tools/computer-use | 200 curl | an official page exists today (H1 "Computer use"); the changelog has "Sep 29: Added computer use to the Agents API"; no claim rests on it |
| LLMS | https://developers.openai.com/api/docs/llms.txt (and `/api/reference/llms.txt`) | 200 curl | no entry with "Decisions" in either index; `/api/docs/guides/decisions` and `/decisions-api` answer 404 |
| CHG | https://developers.openai.com/api/docs/changelog | 200 curl | no "Decisions" entry up to today; Sep 29 entries for GPT-6.1 Sol, Astra Ultrafast and Agents API computer use |
| AOA | docs/videos/always-on-agent-explained/video.json | repo | title line 18; the only dots sentence line 730; `video_id` null |
| G6, G6V | docs/videos/gpt6-vs-opus55-worth-paying/claims.md (c8, line 12) and video.json (title line 18) | repo | $348 and $69.60 → $70 for an assumed monthly workload; `video_id` null |
| PW | docs/videos/ai-price-war-gpt-6-sol-vs-opus-5-5/video.json | repo | title line 20; chapter 「GPT-6 Sol 價目表八格怎麼讀」 line 162; `video_id` null |
| BRIEF | docs/videos/openai-devday-2026-recap/brief.md | repo | 站主觀點 lines 23–31; outline A lines 70–79; not edited |
| SELF | this video.json | — | the script's own cards and sums |

## Claim table

Every row is one string of `video.json` (1–362) or `shorts.json` (363–399) as it reads after this round; shot prompts are not claims and were not touched. Long strings are cut at 64 characters; `where` identifies them. The URL column gives the key from the table above and the line numbers in the captured file.

<!-- claim table: generated by _tools/verify/round1/table.mjs -->
| # | claim (as it reads now) | where | URL (key:lines of the capture) | HTTP | verdict | before → after 〔note〕 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | DevDay 2026 的 25 項，你今天碰得到幾項？照方案分五張清單，這週就能做 | youtube.title | R:15, 27–133 | 200 capture | CONFIRMED | 25 是回顧頁 ### 標題 4＋7＋4＋7＋3；頁面自述「超過 20 項」；五張清單是站主的分法 |
| 2 | OpenAI DevDay 2026 一口氣發表了 25 項，可是你今天打開 ChatGPT，碰得到的有幾項？這支把 25 項照… | youtube.description[line 1] | R:15, 27–133 | 200 capture | CONFIRMED | 同上；2026-10-03 是查閱日 |
| 3 | 給付 Plus、付 Pro、公司用 Business 或 Enterprise，以及接 API 的人：找到自己那一張清單就夠。影… | youtube.description[line 2] | SIWC:27–28, 31；DOTS:76 | 200 capture | NOT FOUND | （前面多一個空行）…設成「要先核准」。 → （空行拿掉）…設成要先核准。 〔三樣、訂閱共用、自訂規則都有來源；「要先核准」加引號當介面字樣沒有來源（頁面的字是「要求先取得核准」）；第 1、2 行之間的空行拿掉〕 |
| 4 | 會動到帳單的只有三個數字：五分之一（GPT-6.1 Sol 的 API 牌價是 Astra 的五分之一）、六倍（GPT-6 As… | youtube.description[line 4] | PRICE:913–914, 949；SPEED:15, 20；PRO:25, 49；R:47–48, 36–37, 97, 104；SOL:55；UF:927；SPACE:10, 18, 23, 31；G6:12；DOTS:94 | 200 curl；200 capture；repo | CHANGED | 同一頁寫得不一樣的地方（…協作投影片的多人編輯）…所有數字都是 OpenAI 自己頁面上的； → 官方頁之間寫得不一樣的地方（…協作投影片的多人編輯，加上空間的行動版）…價格、倍數和日期都是 OpenAI 自己頁面上的；25、9 這些項數是照回顧頁逐項數的，348 與 70 美元是本頻道另一支影片用假設用量算的估計； 〔三個數字都對；「同一頁」只有 Codex 雲端成立，另外三處是兩頁之間，空間的行動版是第五處；「所有數字都是 OpenAI 的」不成立：25、9 是數的，348／70 是本頻道算的〕 |
| 5 | 影片裡提到的上一支、另一支： | youtube.description[line 6] | SELF:a8fd, guna | — | CONFIRMED | 口播提到的是前兩支 |
| 6 | ・AI 代理怎麼運作、怎麼失敗（含 dots 一段）：〈聊天機器人時代結束了：AI 代理（AI Agent）實際怎麼運作、又怎麼… | youtube.description[line 7] | AOA:18, 701, 730 | repo | CHANGED | ・dots 怎麼運作、怎麼失敗：〈聊天機器人時代結束了〉 → ・AI 代理怎麼運作、怎麼失敗（含 dots 一段）：〈聊天機器人時代結束了：AI 代理（AI Agent）實際怎麼運作、又怎麼失敗〉 〔那支的標題與主題是 AI 代理，dots 只有一句〕 |
| 7 | ・Sol 對 Astra 的整月帳單公式：〈GPT-6 Astra vs Claude Opus 5.5 vs Gemini：到… | youtube.description[line 8] | G6V:18；G6:12 | repo | CHANGED | 〈GPT-6 vs Opus 5.5 值不值得付〉 → 〈GPT-6 Astra vs Claude Opus 5.5 vs Gemini：到底哪個值得付費？API 價格實際算給你看〉 〔標題照那支的 youtube.title〕 |
| 8 | ・同一個模型的八格價目表怎麼讀（延伸，影片裡沒提到）：〈GPT-6 Sol 與 Claude Opus 5.5 同一天降價，你的… | youtube.description[line 9] | PW:20, 162 | repo | CHANGED | ・同一個模型的八格價目表怎麼讀：〈AI 價格戰〉 → ・同一個模型的八格價目表怎麼讀（延伸，影片裡沒提到）：〈GPT-6 Sol 與 Claude Opus 5.5 同一天降價，你的 AI 帳單會少多少？〉 〔標題照那支的 youtube.title；這一支口播沒有提到，補「影片裡沒提到」〕 |
| 9 | 錄製日期：2026 年 10 月 3 日。價格、方案與可用範圍之後會變，以官方頁為準。 | youtube.description[line 11] | SELF | — | CONFIRMED | 錄製日＝查閱日 |
| 10 | DevDay 2026、OpenAI DevDay、GPT-6.1 Sol、ChatGPT Pro 500、Ultrafast、… | youtube.tags | R:27–133；PRO:21–25；SPEED:32 | 200 capture | CONFIRMED | 名稱都是官方寫法；每個標籤在影片裡都有內容 |
| 11 | DevDay 2026 | thumbnail.data.tag | R:11 | 200 capture | CONFIRMED |  |
| 12 | 25 項，你碰得到**幾項**？ | thumbnail.data.headline | R:27–133 | 200 capture | CONFIRMED | 25 同上 |
| 13 | 照方案分五張清單 | thumbnail.data.sub | SELF | — | CONFIRMED | 站主的分法 |
| 14 | hall | thumbnail.data.shot | SELF | — | OUT OF SCOPE | 版面設定（hall 是存在的 shot） |
| 15 | OpenAI：DevDay 2026 精彩回顧（2026-09-29）（2026-10-03） | sources[0] | R:3, 5 | 200 capture | CONFIRMED | 頁面日期 2026-09-29 |
| 16 | OpenAI：推出 GPT-6.1 Sol（2026-09-29）（2026-10-03） | sources[1] | SOL:3, 5 | 200 capture | CONFIRMED |  |
| 17 | OpenAI：dots 正式登場（2026-09-29）（2026-10-03） | sources[2] | DOTS:3, 5 | 200 capture | CONFIRMED |  |
| 18 | OpenAI 說明中心：About ChatGPT Pro tiers（2026-10-03） | sources[3] | PRO:3, 5 | 200 capture | NOT FOUND | OpenAI 說明中心：About ChatGPT Pro tiers（更新 2026-10-02） → OpenAI 說明中心：About ChatGPT Pro tiers 〔頁面只寫 Updated: yesterday，沒有日期；標題拿掉「（更新 2026-10-02）」〕 |
| 19 | OpenAI 說明中心：Sign in with ChatGPT（2026-10-03） | sources[4] | SIWC:3, 4 | 200 capture | NOT FOUND | OpenAI 說明中心：Sign in with ChatGPT（更新 2026-10-02） → OpenAI 說明中心：Sign in with ChatGPT 〔同上〕 |
| 20 | ChatGPT Learn：Speed（Fast、Ultrafast 的額度與點數倍數，GPT-5.5 退場日）（2026-10… | sources[5] | SPEED:7, 15, 20, 32 | 200 capture | CONFIRMED |  |
| 21 | ChatGPT Learn：Codex Cloud（2026-10-03） | sources[6] | CLOUD:36 | 200 capture | CONFIRMED |  |
| 22 | ChatGPT Learn：Codex Security Cloud setup（2026-10-03） | sources[7] | SEC:35 | 200 capture | CONFIRMED |  |
| 23 | ChatGPT：ChatGPT 空間（2026-10-03） | sources[8] | SPACE:7 | 200 capture | CONFIRMED | 轉址後的最終網址 |
| 24 | OpenAI API：Pricing（標準、Fast、Ultrafast 價目表）（2026-10-03） | sources[9] | PRICE:906–949 | 200 curl | CONFIRMED | 今天重抓，和擷取檔逐位元相同 |
| 25 | OpenAI API：gpt-6.1-sol 模型頁（2026-10-03） | sources[10] | MODEL:944–967 | 200 curl | CONFIRMED | 同上 |
| 26 | OpenAI API：Ultrafast mode 指南（2026-10-03） | sources[11] | UF:925–941 | 200 curl | CONFIRMED | 同上 |
| 27 | OpenAI API：Zero Data Retention with Private Safety Processing（20… | sources[12] | PSP:930, 971, 974 | 200 curl | CONFIRMED | 同上；頁名 ZDR with Private Safety Processing |
| 28 | OpenAI：Agents API 隆重登場（2026-09-10）（2026-10-03） | sources[13] | AG:3, 5 | 200 capture | CONFIRMED | 頁面日期 2026-09-10 |
| 29 | MCP：Triggers and Events Charter（工作小組章程，提議中的事件規格）（2026-10-03） | sources[14] | MCP | 200 curl | CHANGED | MCP：Triggers and Events Working Group（提議中的事件規格） → MCP：Triggers and Events Charter（工作小組章程，提議中的事件規格） 〔頁名是 Triggers and Events Charter（工作小組章程）；SEP 還在 Ideating〕 |
| 30 | 25 項裡，你今天碰得到幾項？ | hall.chapter | R:27–133 | 200 capture | CONFIRMED |  |
| 31 | DevDay 一口氣發表了二十幾樣東西。 | hall / 24pe | R:15 | 200 capture | CONFIRMED | 超過 20 項；實列 25 |
| 32 | 你今天打開 ChatGPT，碰得到幾樣？ | hall / 25u3 | SELF | — | OUT OF SCOPE | 提問 |
| 33 | AI 時事 | title.data.tag | SELF | — | OUT OF SCOPE | 分類標籤 |
| 34 | DevDay 2026 的 25 項，你今天**碰得到幾項**？ | title.data.title | R:27–133 | 200 capture | CONFIRMED |  |
| 35 | 照方案分五張清單：所有人、Plus、Pro、團隊、開發者 | title.data.subtitle | SELF | — | CONFIRMED | 站主的分法 |
| 36 | 答案不在新聞裡，在你付的是哪一種方案。 | title / 279j | BRIEF:27 | repo | OUT OF SCOPE | 站主的框架（站主觀點第一段） |
| 37 | 這集把回顧頁的 25 項分成五張清單：所有人、Plus、Pro、團隊、開發者。 | ticket-hand / 2bjg | R:27–133 | 200 capture | CONFIRMED |  |
| 38 | 先問一句 | chat-ask.data.title | BRIEF:72 | repo | OUT OF SCOPE | 企劃設計的問答卡 |
| 39 | right | chat-ask.data.messages[0].side | BRIEF:72 | repo | OUT OF SCOPE | 企劃設計的問答卡 |
| 40 | 觀眾 | chat-ask.data.messages[0].name | BRIEF:72 | repo | OUT OF SCOPE | 企劃設計的問答卡 |
| 41 | 25 項，我今天能用幾項？ | chat-ask.data.messages[0].text | BRIEF:72 | repo | OUT OF SCOPE | 企劃設計的問答卡 |
| 42 | left | chat-ask.data.messages[1].side | BRIEF:72 | repo | OUT OF SCOPE | 企劃設計的問答卡 |
| 43 | 站主 | chat-ask.data.messages[1].name | BRIEF:72 | repo | OUT OF SCOPE | 企劃設計的問答卡 |
| 44 | 先看你付的是哪一種。 | chat-ask.data.messages[1].text | BRIEF:72 | repo | OUT OF SCOPE | 企劃設計的問答卡 |
| 45 | 你可能會問，那我自己今天到底能用幾項？ | chat-ask / 2kju | BRIEF:72 | repo | CHANGED | 有人問我，那我自己今天到底能用幾項？ → 你可能會問，那我自己今天到底能用幾項？ 〔企劃設計的觀眾問題，沒有人真的問過（立場 6）〕 |
| 46 | 先看你付的是哪一種，再教你一個這週就能改的設定。 | chat-ask / 2mr4 | DOTS:76；SIWC:27 | 200 capture | CONFIRMED | week-steps 的設定動作 |
| 47 | 每一張只寫官網當天的寫法。 | queue-turn / 2pyt | SELF | — | CONFIRMED | 每張卡都標來源與 2026-10-03 |
| 48 | 先從每個人都有的那一張開始？ | queue-turn / 2xba | BRIEF:72 | repo | OUT OF SCOPE | 過場；「每個人都有」是企劃的清單名，見摘要 |
| 49 | 每個人都有的九項，和那顆登入按鈕 | ch2.chapter | R:48, 52, 56, 60, 79, 83, 91, 121, 127 | 200 capture | CONFIRMED | 九項成立；「每個人都有」是企劃的章名，比來源寬，沒動，見摘要 |
| 50 | 02 | ch2.data.number | SELF | — | OUT OF SCOPE | 版面 |
| 51 | 每個人都有的九項，和那顆登入按鈕 | ch2.data.title | R:48, 52, 56, 60, 79, 83, 91, 121, 127 | 200 capture | CONFIRMED | 同章名 |
| 52 | 回顧頁「適用於」那一行沒指定付費方案 | ch2.data.subtitle | R:48, 52, 56, 60, 79, 83, 91, 121, 127 | 200 capture | CHANGED | 官網寫「適用於所有方案」的那一行 → 回顧頁「適用於」那一行沒指定付費方案 〔只有六項寫「適用於所有方案」〕 |
| 53 | 你以為 DevDay 的東西，都要等開放、都要加錢。 | ch2 / 3a9f | SELF | — | OUT OF SCOPE | 鋪陳（你以為） |
| 54 | 其實回顧頁的 25 項裡，有 9 項的適用於那一行，沒有指定付費方案。 | pool-desk / 3qfi | R:48, 52, 56, 60, 79, 83, 91, 121, 127 | 200 capture | CHANGED | 其實回顧頁的 25 項裡，有 9 項的適用於那一行，寫的是登入就有。 → 其實回顧頁的 25 項裡，有 9 項的適用於那一行，沒有指定付費方案。 〔九行都沒有「登入就有」；共同點是沒點名付費方案〕 |
| 55 | 回顧頁「適用於」那一行怎麼寫 | nine-stats.data.title | R:48 | 200 capture | CONFIRMED |  |
| 56 | 6 項 | nine-stats.data.stats[0].value | R:48, 52, 56, 79, 83, 91 | 200 capture | CONFIRMED | 六項逐項對過 |
| 57 | 適用於所有方案 | nine-stats.data.stats[0].label | R:48, 52, 56, 79, 83, 91 | 200 capture | CONFIRMED | 六項逐項對過 |
| 58 | Codex 雲端、Codex CLI、程式碼審查、外掛程式擴充功能、外掛程式建立與提交、MCP 事件 | nine-stats.data.stats[0].note | R:48, 52, 56, 79, 83, 91 | 200 capture | CONFIRMED | 六項逐項對過 |
| 59 | 3 項 | nine-stats.data.stats[1].value | R:60, 121, 127 | 200 capture | CONFIRMED |  |
| 60 | 所有 Codex 使用者、所有其他方案、全球已登入使用者 | nine-stats.data.stats[1].label | R:60, 121, 127 | 200 capture | CONFIRMED |  |
| 61 | Codex Security Cloud、可分享的個人檔案、使用 ChatGPT 登入 | nine-stats.data.stats[1].note | R:60, 121, 127 | 200 capture | CONFIRMED |  |
| 62 | OpenAI DevDay 2026 回顧頁，2026-09-29。免費方案含哪些，頁上沒寫，以官網為準 | nine-stats.data.source | R:5 | 200 capture | CONFIRMED | 全文沒有「免費」「Free」 |
| 63 | 其中 6 項，官網寫的是適用於所有方案。 | nine-stats / 3v68 | R:48, 52, 56, 79, 83, 91 | 200 capture | CONFIRMED |  |
| 64 | 另外 3 項，寫給所有 Codex 使用者、其他方案、已登入使用者。 | nine-stats / 4ffb | R:60, 121, 127 | 200 capture | CONFIRMED |  |
| 65 | 免費方案含哪些，頁上沒寫；Codex 雲端那一段也寫 Plus 以上，都以官網為準。 | turnstile / 4fu7 | R:47–48 | 200 capture | CONFIRMED | 同一項兩種寫法 |
| 66 | 九項裡，Codex 的四項 | codex-four.data.title | R:48, 52, 56, 60 | 200 capture | CONFIRMED |  |
| 67 | **Codex 雲端**：任務在雲端跑；同一段也寫 Plus 以上，以官網為準 | codex-four.data.items[0] | R:47–48 | 200 capture | CONFIRMED |  |
| 68 | **Codex CLI**：語音聊天、/agents 檢視、worktree | codex-four.data.items[1] | R:51–52 | 200 capture | CONFIRMED |  |
| 69 | **程式碼審查**：桌面應用程式，GitHub 提取要求與 GitLab 合併要求 | codex-four.data.items[2] | R:55–56 | 200 capture | CONFIRMED |  |
| 70 | **Codex Security Cloud**：所有 Codex 使用者 | codex-four.data.items[3] | R:60 | 200 capture | CONFIRMED |  |
| 71 | 回顧頁「適用於」那一行的寫法，2026-09-29 | codex-four.data.note | R:5 | 200 capture | CONFIRMED |  |
| 72 | 寫程式的人拿到四項：Codex 雲端、Codex CLI、程式碼審查、Codex Security Cloud。 | codex-four / 4m64 | R:46–60 | 200 capture | CONFIRMED |  |
| 73 | CLI 能用講的，程式碼審查接 GitHub 和 GitLab；剩下五項，也沒指定付費方案。 | lane-wide / 4py7 | R:51, 55, 79, 83, 91, 121, 127 | 200 capture | CHANGED | CLI 能用講的，程式碼審查接 GitHub 和 GitLab；剩下五項，每個人都會碰到。 → CLI 能用講的，程式碼審查接 GitHub 和 GitLab；剩下五項，也沒指定付費方案。 〔五項裡三項是給開發者做的；個人檔案有三個方案還沒有〕 |
| 74 | 另外五項 | five-more.data.title | SELF | — | CONFIRMED | 9 − 4 |
| 75 | **外掛程式擴充功能**：側邊欄入口、互動面板、檔案檢視器 | five-more.data.items[0] | R:78–79 | 200 capture | CONFIRMED |  |
| 76 | **外掛程式建立與提交**：權限仍由你逐一核准 | five-more.data.items[1] | R:82–83 | 200 capture | CONFIRMED |  |
| 77 | **MCP 事件**：「正加入支援」，提議中的規格 | five-more.data.items[2] | R:90–91 | 200 capture | CONFIRMED |  |
| 78 | **可分享的個人檔案**：Enterprise、Edu、Healthcare 即將推出，其他方案已有 | five-more.data.items[3] | R:121 | 200 capture | CHANGED | **可分享的個人檔案**：所有其他方案已有 → **可分享的個人檔案**：Enterprise、Edu、Healthcare 即將推出，其他方案已有 〔補上還沒有的三個方案〕 |
| 79 | **使用 ChatGPT 登入**：全球已登入使用者，依組織設定 | five-more.data.items[4] | R:127；SIWC:15, 17 | 200 capture | CONFIRMED |  |
| 80 | 回顧頁「適用於」那一行的寫法，2026-09-29 | five-more.data.note | R:5 | 200 capture | CONFIRMED |  |
| 81 | 外掛程式的擴充功能，外掛程式的建立與提交，還有 MCP 事件，規格還在提議中。 | five-more / 4tzn | R:78, 82, 90 | 200 capture | CONFIRMED |  |
| 82 | 可分享的個人檔案，和使用 ChatGPT 登入。 | five-more / 4z24 | R:119, 125 | 200 capture | CONFIRMED |  |
| 83 | 這顆登入按鈕，是我最在意的一項，它交出去的只有三樣。 | card-closeup / 53vp | SIWC:31；BRIEF:29 | 200 capture；repo | CONFIRMED | 看法有標「我」，和站主觀點一致 |
| 84 | 使用 ChatGPT 登入，照說明頁的五步 | login-steps.data.title | SIWC:20–25 | 200 capture | CONFIRMED |  |
| 85 | 合作網站或外掛程式目錄 | login-steps.data.steps[0].title | SIWC:21 | 200 capture | CONFIRMED |  |
| 86 | 首批 Airtable、GitLab、HubSpot、Notion、Supabase、Vercel，以官網為準 | login-steps.data.steps[0].detail | SIWC:16 | 200 capture | CONFIRMED | 六家逐一對過 |
| 87 | 按「使用 ChatGPT 登入」 | login-steps.data.steps[1].title | SIWC:22；R:125 | 200 capture | CONFIRMED | 中文名出自回顧頁 |
| 88 | 或 Continue with ChatGPT | login-steps.data.steps[1].detail | SIWC:12, 22 | 200 capture | NOT FOUND | 或「以 ChatGPT 繼續」 → 或 Continue with ChatGPT 〔說明頁只有英文 Continue with ChatGPT；中文介面字樣沒有來源〕 |
| 89 | 讀畫面列的身分資訊 | login-steps.data.steps[2].title | SIWC:23, 31 | 200 capture | CONFIRMED |  |
| 90 | 姓名、電子郵件、個人檔案照片 | login-steps.data.steps[2].detail | SIWC:23, 31 | 200 capture | CONFIRMED |  |
| 91 | 想用再繼續 | login-steps.data.steps[3].title | SIWC:24 | 200 capture | CONFIRMED |  |
| 92 | 建立、連結或存取那個帳號 | login-steps.data.steps[3].detail | SIWC:24 | 200 capture | CONFIRMED |  |
| 93 | 其他權限另行核准 | login-steps.data.steps[4].title | SIWC:25, 27 | 200 capture | CONFIRMED |  |
| 94 | 訂閱共用是獨立的一個請求 | login-steps.data.steps[4].detail | SIWC:25, 27 | 200 capture | CONFIRMED |  |
| 95 | 第一步在合作網站找到它，第二步按下去，第三步讀畫面列的身分資訊。 | login-steps / 5iay | SIWC:21–23 | 200 capture | CONFIRMED |  |
| 96 | 第四步想用再繼續，第五步其他權限另外核准，重點在這一步。 | login-steps / 5mgv | SIWC:24–25 | 200 capture | CONFIRMED |  |
| 97 | 訂閱共用，是另外一把鑰匙，不是跟著登入一起給的。 | key-board / 63ta | SIWC:27–28 | 200 capture | CONFIRMED |  |
| 98 | 對方拿到的，和登入不給的 | three-vs.data.title | SIWC:32, 36 | 200 capture | CHANGED | 對方拿到的，和永遠不給的 → 對方拿到的，和登入不給的 〔does not independently share；應用程式可以另外請求〕 |
| 99 | 對方拿到的 | three-vs.data.left.heading | SIWC:31 | 200 capture | CONFIRMED |  |
| 100 | 姓名 | three-vs.data.left.points[0] | SIWC:31 | 200 capture | CONFIRMED |  |
| 101 | 電子郵件地址 | three-vs.data.left.points[1] | SIWC:31 | 200 capture | CONFIRMED |  |
| 102 | 個人檔案照片（如有） | three-vs.data.left.points[2] | SIWC:31 | 200 capture | CONFIRMED |  |
| 103 | 登入本身不給的 | three-vs.data.right.heading | SIWC:32, 36 | 200 capture | CHANGED | 永遠不給的 → 登入本身不給的 〔同標題〕 |
| 104 | 聊天內容與記憶 | three-vs.data.right.points[0] | SIWC:33–35 | 200 capture | CONFIRMED |  |
| 105 | 檔案與 token | three-vs.data.right.points[1] | SIWC:33–35 | 200 capture | CONFIRMED |  |
| 106 | 帳務與其他帳號資料 | three-vs.data.right.points[2] | SIWC:33–35 | 200 capture | CONFIRMED |  |
| 107 | 說明中心的寫法，2026-10-03 查閱 | three-vs.data.verdict | SIWC:4 | 200 capture | NOT FOUND | 說明中心 2026-10-02 的寫法 → 說明中心的寫法，2026-10-03 查閱 〔Updated: yesterday 推不出確切日期〕 |
| 108 | 對方拿到的，只有姓名、電子郵件、個人檔案照片。 | three-vs / 68xh | SIWC:31 | 200 capture | CONFIRMED |  |
| 109 | 聊天和記憶、檔案和 token、帳務，登入本身都不給。 | three-vs / 6bae | SIWC:32–36 | 200 capture | CHANGED | 聊天和記憶、檔案和 token、帳務，一律不給。 → 聊天和記憶、檔案和 token、帳務，登入本身都不給。 〔「一律」比來源強〕 |
| 110 | 訂閱共用可以不答應；答應了，也能自己設上限，像把水道繩拉到記號就停。 | lane-rope / 6fq4 | SIWC:27–28 | 200 capture | CONFIRMED |  |
| 111 | 公司帳號看不到按鈕，先問管理員；那是全域管理員管的，不是壞掉。 | office-bolt / 6grq | SIWC:44, 48 | 200 capture | CONFIRMED |  |
| 112 | 不核准共用，登入一樣完成。 | walk-past / 6jcw | SIWC:28 | 200 capture | CONFIRMED |  |
| 113 | 那付了 Plus 的人，多了哪幾樣？ | walk-past / 6mey | SELF | — | OUT OF SCOPE | 提問 |
| 114 | Plus 的清單：九項之上再加 Sol | ch3.chapter | SOL:53 | 200 capture | CONFIRMED |  |
| 115 | 03 | ch3.data.number | SELF | — | OUT OF SCOPE | 版面 |
| 116 | Plus 的清單：九項再加 Sol | ch3.data.title | SOL:53 | 200 capture | CONFIRMED |  |
| 117 | 順便看 Codex 的三項怎麼用 | ch3.data.subtitle | R:47, 51, 55 | 200 capture | CONFIRMED | 三項＝three-stands、shutter-wheel、spin-wheel |
| 118 | 付 Plus 的人，拿到的是這次對最多人有用的一項。 | ch3 / 6npj | BRIEF:31 | repo | OUT OF SCOPE | 看法，和站主觀點一致，沒有標成看法 |
| 119 | GPT-6.1 Sol，Plus 在 ChatGPT 工作和 Codex 裡就能選，對話裡還沒有。 | bike-talk / 6q7d | SOL:53 | 200 capture | CONFIRMED |  |
| 120 | Plus 多的那一項 | sol-big.data.kicker | SELF | — | CONFIRMED |  |
| 121 | GPT-6.1 Sol：ChatGPT 工作與 Codex **有了**，對話還沒有 | sol-big.data.text | SOL:53 | 200 capture | CONFIRMED |  |
| 122 | Plus、Pro、Business、Enterprise、Edu（Sol 頁 2026-09-29）。OpenAI 自己公布的評… | sol-big.data.sub | SOL:5, 14, 22, 53, 57 | 200 capture | CONFIRMED | 評測是 OpenAI 自己公布的 |
| 123 | Sol 頁寫 Plus 到 Edu 都能用，OpenAI 自己公布的評測說它接近 Astra。 | sol-big / 6tnm | SOL:14, 22, 53 | 200 capture | CONFIRMED |  |
| 124 | Codex 這邊也能同時架好幾台車：CLI 新的 agents 檢視，把工作分給多個智慧體。 | three-stands / 6urf | R:51 | 200 capture | CONFIRMED |  |
| 125 | Codex 雲端的意思是，你的電腦睡著了，任務還在跑，手機也能接著看。 | shutter-wheel / 6zff | CLOUD:39, 42；R:47 | 200 capture | CONFIRMED |  |
| 126 | Codex Cloud 頁原句 | cloud-quote.data.kicker | CLOUD:36 | 200 capture | CONFIRMED |  |
| 127 | Each task has its own workspace and can keep working while your … | cloud-quote.data.quote | CLOUD:42 | 200 capture | CONFIRMED | 一字不差 |
| 128 | 每個任務有自己的工作區，你的電腦睡著了也能繼續。 | cloud-quote.data.translation | CLOUD:42 | 200 capture | CONFIRMED |  |
| 129 | learn.chatgpt.com/docs/cloud，2026-10-03 | cloud-quote.data.source | CLOUD:36 | 200 capture | CONFIRMED |  |
| 130 | Codex Cloud 頁上的原句，是這樣寫的。 | cloud-quote / 79px | CLOUD:42 | 200 capture | CONFIRMED |  |
| 131 | 翻成中文，每個任務有自己的工作區，你的電腦睡著了也能繼續。 | cloud-quote / 7eac | CLOUD:42 | 200 capture | CONFIRMED |  |
| 132 | 程式碼審查先看摘要，再看差異，有問題再問 Codex；也可以開自動審查。 | spin-wheel / 7i9i | R:55 | 200 capture | CONFIRMED |  |
| 133 | 不過，有一把舊扳手要收起來了。 | old-wrench / 7ipw | SELF | — | OUT OF SCOPE | 比喻過場 |
| 134 | GPT-5.5 退場 | retire-stats.data.title | SPEED:31–32 | 200 capture | CONFIRMED |  |
| 135 | 10 月 14 日 | retire-stats.data.stats[0].value | SPEED:32 | 200 capture | CONFIRMED | October 14, 2026；all plans |
| 136 | 退出 ChatGPT、ChatGPT 工作與 Codex | retire-stats.data.stats[0].label | SPEED:32 | 200 capture | CONFIRMED | October 14, 2026；all plans |
| 137 | 2026 年，所有方案 | retire-stats.data.stats[0].note | SPEED:32 | 200 capture | CONFIRMED | October 14, 2026；all plans |
| 138 | API | retire-stats.data.stats[1].value | SPEED:32 | 200 capture | CONFIRMED | API 不受影響；那一節只有兩句 |
| 139 | 不受影響 | retire-stats.data.stats[1].label | SPEED:32 | 200 capture | CONFIRMED | API 不受影響；那一節只有兩句 |
| 140 | 頁上沒寫該換哪一個模型 | retire-stats.data.stats[1].note | SPEED:32 | 200 capture | CONFIRMED | API 不受影響；那一節只有兩句 |
| 141 | learn.chatgpt.com 的 Speed 頁，2026-10-03 | retire-stats.data.source | SPEED:7 | 200 capture | CONFIRMED |  |
| 142 | GPT-5.5 在 10 月 14 日，從 ChatGPT、ChatGPT 工作和 Codex 退場。 | retire-stats / 7vku | SPEED:32 | 200 capture | CONFIRMED |  |
| 143 | API 不受影響；Codex 裡改選一個還在的模型。 | retire-stats / 8v7m | SPEED:32 | 200 capture | CONFIRMED | 後半是給觀眾的動作，不指名模型 |
| 144 | Plus 的清單，九項加一個 Sol。 | test-ride / 8vrs | SOL:53 | 200 capture | CONFIRMED |  |
| 145 | 那 Pro 多付的那一份，換到什麼？ | test-ride / 8yd9 | SELF | — | OUT OF SCOPE | 提問 |
| 146 | Pro 的清單：四項、dots 看市場、三個級別 | ch4.chapter | R:97, 101, 105, 117；DOTS:94；PRO:21–25 | 200 capture | CONFIRMED |  |
| 147 | 04 | ch4.data.number | SELF | — | OUT OF SCOPE | 版面 |
| 148 | Pro 的清單：四項、dots 看市場、三個級別 | ch4.data.title | R:97, 101, 105, 117；DOTS:94；PRO:21–25 | 200 capture | CONFIRMED |  |
| 149 | Pro 100、Pro 200、Pro 500，和 Pro 200 舊用戶的四步 | ch4.data.subtitle | PRO:21–25, 37 | 200 capture | CONFIRMED |  |
| 150 | Pro 那一張清單，和你的帳單有關。 | ch4 / 977k | SELF:tally-stats | — | CHANGED | Pro 那一張清單最長，而且和你的帳單有關。 → Pro 那一張清單，和你的帳單有關。 〔照影片自己的加總，所有人 9 項比 Pro 6 項長〕 |
| 151 | 先看四項已經寫在 Pro 名下的，再加一項要看市場的，也就是 dots。 | pottery-wide / 99ep | R:97, 101, 105, 117；DOTS:94 | 200 capture | CONFIRMED |  |
| 152 | Pro 的清單 | pro-five.data.title | SELF | — | CONFIRMED |  |
| 153 | **dots**：符合資格的市場逐步推出，第一個不另收費；台灣有沒有以官網為準 | pro-five.data.items[0] | DOTS:94, 96 | 200 capture | CONFIRMED | 頁上沒列市場名 |
| 154 | **ChatGPT 空間**：網頁與桌面可編輯；行動版，空間頁寫只能看、回顧頁寫即將推出，以官網為準；分享頁面不分享私人對話與記… | pro-five.data.items[1] | R:97；SPACE:23, 26, 31 | 200 capture | CHANGED | **ChatGPT 空間**：網頁與桌面可編輯，行動版只能看；分享頁面不分享私人對話與記憶 → **ChatGPT 空間**：網頁與桌面可編輯；行動版，空間頁寫只能看、回顧頁寫即將推出，以官網為準；分享頁面不分享私人對話與記憶 〔行動版兩頁寫法不同（回顧頁：即將推出；空間頁：現在可檢視）〕 |
| 155 | **動態頁面**：和 dot 或 ChatGPT 一起做、會自己更新的文件 | pro-five.data.items[2] | R:100–101 | 200 capture | CONFIRMED |  |
| 156 | **協作投影片**：可匯出 PowerPoint 或 Google 簡報；多人同時編輯，兩頁寫法不同，以官網為準 | pro-five.data.items[3] | R:104–105；SPACE:10, 18 | 200 capture | CONFIRMED |  |
| 157 | **會議外掛程式 Beta**：Pro 與 Business，macOS 桌面應用程式 | pro-five.data.items[4] | R:117；SPACE:30 | 200 capture | CONFIRMED |  |
| 158 | 回顧頁、dots 頁、空間頁，2026-10-03 | pro-five.data.note | R:5；DOTS:5；SPACE:7 | 200 capture | CONFIRMED |  |
| 159 | dots，向符合資格的市場逐步推出，台灣有沒有，以官網為準。 | pro-five / 9rtc | DOTS:94 | 200 capture | CONFIRMED |  |
| 160 | ChatGPT 空間和動態頁面，網頁和桌面能編輯；行動版兩頁寫法不同，以官網為準。 | pro-five / a3tb | R:97；SPACE:23, 31 | 200 capture | CHANGED | ChatGPT 空間和動態頁面，網頁和桌面能編輯，行動版只能看。 → ChatGPT 空間和動態頁面，網頁和桌面能編輯；行動版兩頁寫法不同，以官網為準。 〔同字卡〕 |
| 161 | 協作投影片能匯出 PowerPoint；會議外掛程式是測試版，Pro 和 Business。 | pro-five / a4qu | R:104, 117 | 200 capture | CONFIRMED |  |
| 162 | AI 代理怎麼運作、怎麼失敗，上一支講過了；這裡只講 dots 的額度，和三條界線。 | wheel-alone / a8fd | AOA:18, 730 | repo | CHANGED | dots 怎麼運作、怎麼失敗，上一支講過了；這裡只講額度，和三條界線。 → AI 代理怎麼運作、怎麼失敗，上一支講過了；這裡只講 dots 的額度，和三條界線。 〔那一支講的是 AI 代理，dots 只有一句〕 |
| 163 | dots 頁 2026-09-29 | dot-big.data.kicker | DOTS:5 | 200 capture | CONFIRMED |  |
| 164 | 跟 dot 聊天**不算額度** ⏎ 叫它在 Codex 或 ChatGPT 工作裡跑任務才算 | dot-big.data.text | DOTS:98 | 200 capture | CONFIRMED |  |
| 165 | 第一個 dot 不另收費；推出後第一個月上限較高 | dot-big.data.sub | DOTS:96 | 200 capture | CONFIRMED |  |
| 166 | 跟 dot 聊天不算額度，叫它在 Codex 或 ChatGPT 工作裡跑任務才算。 | dot-big / aedk | DOTS:98 | 200 capture | CONFIRMED |  |
| 167 | 三條界線：主動研究唯讀，自訂規則能設先核准，改密碼一律你自己來。 | locked-cabinet / aeyf | DOTS:69, 76, 81 | 200 capture | CONFIRMED |  |
| 168 | 空間的頁面也一樣，你改一筆，同事接著改；分享頁面不會分享你的私人對話。 | two-hands-bowl / aiiz | SPACE:15, 26 | 200 capture | CONFIRMED | 同段的「頁上寫的都看得到」沒帶到，見摘要 |
| 169 | 會議外掛程式，就是旁邊記筆記的那個人，筆記存進空間，私人或分享都行。 | kiln-talk / akzj | R:116 | 200 capture | CONFIRMED |  |
| 170 | Pro 現在有三階（說明中心，2026-10-03 查閱） | pro-table.data.title | PRO:5, 19–25 | 200 capture | NOT FOUND | Pro 現在有三階（說明中心 2026-10-02） → Pro 現在有三階（說明中心，2026-10-03 查閱） 〔三階成立；Updated: yesterday 推不出確切日期〕 |
| 171 | 級別 | pro-table.data.columns[0] | PRO:21 | 200 capture | CONFIRMED |  |
| 172 | 月費 | pro-table.data.columns[1] | PRO:21 | 200 capture | CONFIRMED |  |
| 173 | Ultrafast | pro-table.data.columns[2] | PRO:21 | 200 capture | CONFIRMED |  |
| 174 | Pro 100 | pro-table.data.rows[0][0] | PRO:23–25 | 200 capture | CONFIRMED |  |
| 175 | $100 | pro-table.data.rows[0][1] | PRO:23–25 | 200 capture | CONFIRMED |  |
| 176 | 不含 | pro-table.data.rows[0][2] | PRO:23–25 | 200 capture | CONFIRMED |  |
| 177 | Pro 200 | pro-table.data.rows[1][0] | PRO:23–25 | 200 capture | CONFIRMED |  |
| 178 | $200 | pro-table.data.rows[1][1] | PRO:23–25 | 200 capture | CONFIRMED |  |
| 179 | 不含 | pro-table.data.rows[1][2] | PRO:23–25 | 200 capture | CONFIRMED |  |
| 180 | Pro 500 | pro-table.data.rows[2][0] | PRO:23–25 | 200 capture | CONFIRMED |  |
| 181 | $500 | pro-table.data.rows[2][1] | PRO:23–25 | 200 capture | CONFIRMED |  |
| 182 | 含 | pro-table.data.rows[2][2] | PRO:23–25 | 200 capture | CONFIRMED |  |
| 183 | 2 | pro-table.data.highlight | SELF | — | OUT OF SCOPE | 版面 |
| 184 | Pro 只能月繳；點數適用 Codex、ChatGPT 工作、ChatGPT for Word／Excel／PowerPoint… | pro-table.data.note | PRO:50, 58, 71 | 200 capture | CONFIRMED |  |
| 185 | Pro 現在有三階，Pro 100 和 Pro 200 都不含 Ultrafast。 | pro-table / am8b | PRO:23–24 | 200 capture | CONFIRMED |  |
| 186 | 只有每月五百美元的 Pro 500 含；推出時，低階買點數也開不了。 | pro-table / apbg | PRO:25, 49–50 | 200 capture | CONFIRMED |  |
| 187 | 所以 Pro 500 買到的是速度和最高額度，不是更聰明的模型。 | three-kilns / b3ja | PRO:27；R:130；SPEED:18；BRIEF:31 | 200 capture；repo | CONFIRMED | 事實部分成立；結論是站主的看法，沒有標成看法 |
| 188 | Pro 200 舊用戶的四步 | pro200-steps.data.title | PRO:36–44 | 200 capture | CONFIRMED |  |
| 189 | 9/22 到 9/29 上午 10 點之間訂閱有效過 | pro200-steps.data.steps[0].title | PRO:37 | 200 capture | CHANGED | 9/22 到 9/29 上午 10 點之間訂過 → 9/22 到 9/29 上午 10 點之間訂閱有效過 〔條件是窗口內訂閱有效過，不是在窗口內下訂〕 |
| 190 | 太平洋時間；之後再訂回來也算 | pro200-steps.data.steps[0].detail | PRO:37, 44 | 200 capture | CONFIRMED |  |
| 191 | 舊額度留到 10/29 | pro200-steps.data.steps[1].title | PRO:37 | 200 capture | CONFIRMED |  |
| 192 | 2026-10-29，訂閱維持中才有 | pro200-steps.data.steps[1].detail | PRO:37 | 200 capture | CONFIRMED |  |
| 193 | 之後換新額度 | pro200-steps.data.steps[2].title | PRO:38 | 200 capture | CONFIRMED |  |
| 194 | 月費不變，仍是 $200 | pro200-steps.data.steps[2].detail | PRO:38 | 200 capture | CONFIRMED |  |
| 195 | 留舊額度不等於升級 | pro200-steps.data.steps[3].title | PRO:41 | 200 capture | CONFIRMED |  |
| 196 | 不會多出 Ultrafast | pro200-steps.data.steps[3].detail | PRO:41 | 200 capture | CONFIRMED |  |
| 197 | 說明中心，2026-10-03 查閱；受影響的人會收到 email | pro200-steps.data.note | PRO:5, 38 | 200 capture | NOT FOUND | 說明中心 2026-10-02；受影響的人會收到 email → 說明中心，2026-10-03 查閱；受影響的人會收到 email 〔email 成立；日期同上〕 |
| 198 | 9 月 22 日到 29 日上午 10 點之間有訂閱的，舊額度留到 10 月 29 日。 | pro200-steps / bdwn | PRO:37 | 200 capture | CHANGED | 9 月 22 日到 29 日上午 10 點之間訂過的，舊額度留到 10 月 29 日。 → 9 月 22 日到 29 日上午 10 點之間有訂閱的，舊額度留到 10 月 29 日。 〔同字卡；太平洋時間留在字卡〕 |
| 199 | 之後換成新額度，月費不變；留著舊額度不等於升級，不會多出 Ultrafast。 | pro200-steps / bekc | PRO:38, 41 | 200 capture | CONFIRMED |  |
| 200 | 一把舊鑰匙、一把新鑰匙；先打開設定裡的我的方案，看自己是哪一階。 | two-keys / bk3e | PRO:69 | 200 capture | CONFIRMED | 「我的方案」是 My Plan 的中譯，中文介面字樣沒有來源，見摘要 |
| 201 | 同一件事，吃掉多少方案額度 | rate-stats.data.title | PRO:66 | 200 capture | CONFIRMED |  |
| 202 | 8 份 | rate-stats.data.stats[0].value | PRO:66；SPEED:15, 20 | 200 capture | CONFIRMED |  |
| 203 | GPT-6 Astra Ultrafast | rate-stats.data.stats[0].label | PRO:66；SPEED:15, 20 | 200 capture | CONFIRMED |  |
| 204 | 標準 1 份、Fast 2.5 份 | rate-stats.data.stats[0].note | PRO:66；SPEED:15, 20 | 200 capture | CONFIRMED |  |
| 205 | 80 件 | rate-stats.data.stats[1].value | PRO:66 | 200 capture | CONFIRMED | 10 × 8 是影片的算術 |
| 206 | 每天用 Ultrafast 跑 10 件，等於標準模式幾件的額度 | rate-stats.data.stats[1].label | PRO:66 | 200 capture | CONFIRMED | 10 × 8 是影片的算術 |
| 207 | 算得出來的只有這個 | rate-stats.data.stats[1].note | PRO:66 | 200 capture | CONFIRMED | 10 × 8 是影片的算術 |
| 208 | 說明中心與 Speed 頁 2026-10-03：額度消耗率，不是速度保證；每階能跑幾件，這兩頁沒寫，以官網的方案比較頁為準 | rate-stats.data.source | PRO:27–28, 66；SPEED:24 | 200 capture | NOT FOUND | 說明中心與 Speed 頁 2026-10-03：額度消耗率，不是速度保證；每階能跑幾件，官方沒有數字，以官網為準 → 說明中心與 Speed 頁 2026-10-03：額度消耗率，不是速度保證；每階能跑幾件，這兩頁沒寫，以官網的方案比較頁為準 〔兩頁都把件數指到沒抓到的方案比較頁；「官方沒有」沒有證據，收窄成「這兩頁沒寫」〕 |
| 209 | 同一件事，標準算 1 份額度，Fast 算 2.5 份，Astra Ultrafast 算 8 份。 | rate-stats / bmwj | PRO:66；SPEED:15, 20 | 200 capture | CONFIRMED |  |
| 210 | 每天跑 10 件就是標準 80 件的額度；每階能跑幾件，這兩頁沒寫，以官網為準。 | rate-stats / bra3 | PRO:27–28, 66；SPEED:24 | 200 capture | NOT FOUND | 每天跑 10 件就是標準 80 件的額度；每階能跑幾件，官方沒數字。 → 每天跑 10 件就是標準 80 件的額度；每階能跑幾件，這兩頁沒寫，以官網為準。 〔同字卡〕 |
| 211 | 你可能會問，我每天用 Codex 兩三個小時，該選哪一階？ | glaze-shelf / bswh | BRIEF:76 | repo | CHANGED | 有人問，我每天用 Codex 兩三個小時，該選哪一階？ → 你可能會問，我每天用 Codex 兩三個小時，該選哪一階？ 〔企劃設計的觀眾問題，沒有人真的問過〕 |
| 212 | 我的回答是，先數你一天有幾件事，是坐著等它跑完的。 | kiln-door / bsx5 | BRIEF:31 | repo | OUT OF SCOPE | 看法，有標「我的回答」 |
| 213 | 等的時間值不值這八倍，只有你的量算得出來。 | cat-step / bzus | PRO:66 | 200 capture | CONFIRMED | 八倍＝8 份額度；結論是看法 |
| 214 | 公司帳號呢？團隊多了哪幾樣？ | cat-step / ckeq | SELF | — | OUT OF SCOPE | 提問 |
| 215 | 團隊的清單：公司帳號多的五項 | ch5.chapter | R:41–42, 87, 109, 113, 134–135 | 200 capture | CONFIRMED |  |
| 216 | 05 | ch5.data.number | SELF | — | OUT OF SCOPE | 版面 |
| 217 | 團隊的清單 | ch5.data.title | SELF | — | CONFIRMED |  |
| 218 | 公司帳號多的五項，和 Codex Security Cloud 的五步 | ch5.data.subtitle | R:41–42, 87, 109, 113, 134–135 | 200 capture | CHANGED | Business、Enterprise 多的五項，和 Codex Security Cloud 的五步 → 公司帳號多的五項，和 Codex Security Cloud 的五步 〔五項裡只有兩項寫 Business 和 Enterprise〕 |
| 219 | 公司或團隊的帳號，多了五項。 | ch5 / d4k8 | R:41–42, 87, 109, 113, 134–135 | 200 capture | CHANGED | 公司或團隊用 Business、Enterprise 的人，多了五項。 → 公司或團隊的帳號，多了五項。 〔同副標〕 |
| 220 | 在 Slack 或 Teams 裡提到 ChatGPT，它就接手，像主廚隔著出菜口喊一聲。 | kitchen-wide / d5ct | R:112 | 200 capture | CONFIRMED |  |
| 221 | 團隊的清單 | team-five.data.title | SELF | — | CONFIRMED |  |
| 222 | **建立團隊並共用任務**：依排程，或情況有變化時動 | team-five.data.items[0] | R:108–109 | 200 capture | CONFIRMED |  |
| 223 | **Slack 與 Microsoft Teams 的 @ChatGPT**：沒有授權的同事也能補背景 | team-five.data.items[1] | R:112–113 | 200 capture | CONFIRMED |  |
| 224 | **可連結外掛程式的工作站**：各自的權限登入 | team-five.data.items[2] | R:86–87 | 200 capture | CONFIRMED |  |
| 225 | **私密智慧**：API 的零資料保留搭配私密安全處理，按專案開、先取得 ZDR 核准；私密推論是預覽版 | team-five.data.items[3] | R:41；PSP:971, 974 | 200 capture；200 curl | CHANGED | **私密智慧**：零資料保留搭配私密安全處理，按專案開、先取得 ZDR 核准；私密推論是預覽版 → **私密智慧**：API 的零資料保留搭配私密安全處理，按專案開、先取得 ZDR 核准；私密推論是預覽版 〔專案是 API 的專案（API console）〕 |
| 226 | **OpenAI 市集 Beta**：符合資格的企業客戶 | team-five.data.items[4] | R:135 | 200 capture | CONFIRMED |  |
| 227 | 回顧頁與 API 指南的寫法，2026-10-03；細節以官網為準 | team-five.data.note | R:5；PSP:930 | 200 capture；200 curl | CONFIRMED |  |
| 228 | 建立團隊並共用任務，和 Slack、Teams 裡的 ChatGPT。 | team-five / dcuh | R:107, 111 | 200 capture | CONFIRMED |  |
| 229 | 可連結外掛程式的工作站、私密智慧，和 OpenAI 市集的測試版。 | team-five / dg29 | R:85, 40, 133 | 200 capture | CONFIRMED |  |
| 230 | 工作站的意思是，同一個應用程式，每個人帶自己的刀，用自己的權限登入。 | own-knife / dhff | R:86 | 200 capture | CONFIRMED |  |
| 231 | 團隊任務像出菜鈴，時間到了，或情況變了，就往下一站送。 | bell-tray / dw68 | R:108 | 200 capture | CONFIRMED |  |
| 232 | 沒有授權的同事也能補一張單子；私密智慧按 API 專案開，細節以官網為準。 | blank-board / dyna | R:112；PSP:971, 974 | 200 capture；200 curl | CHANGED | 沒有授權的同事也能補一張單子；私密智慧按專案開，細節以官網為準。 → 沒有授權的同事也能補一張單子；私密智慧按 API 專案開，細節以官網為準。 〔同字卡〕 |
| 233 | Codex Security Cloud：所有 Codex 使用者都有 | security-steps.data.title | R:60 | 200 capture | CONFIRMED |  |
| 234 | 安裝外掛程式 | security-steps.data.steps[0].title | SEC:41 | 200 capture | CONFIRMED |  |
| 235 | 網頁版或桌面應用程式的外掛程式市集 | security-steps.data.steps[0].detail | SEC:41 | 200 capture | CONFIRMED |  |
| 236 | 連 GitHub | security-steps.data.steps[1].title | SEC:42 | 200 capture | CONFIRMED |  |
| 237 | 授權要掃的存放庫 | security-steps.data.steps[1].detail | SEC:42 | 200 capture | CONFIRMED |  |
| 238 | 一次性掃描 | security-steps.data.steps[2].title | SEC:43 | 200 capture | CONFIRMED |  |
| 239 | One-Time Scan，雲端環境自動建 | security-steps.data.steps[2].detail | SEC:43 | 200 capture | CONFIRMED |  |
| 240 | 看發現，Fix with Codex | security-steps.data.steps[3].title | SEC:44 | 200 capture | CONFIRMED |  |
| 241 | 先看補丁，再出草稿提取要求 | security-steps.data.steps[3].detail | SEC:44 | 200 capture | CONFIRMED |  |
| 242 | 持續掃描 | security-steps.data.steps[4].title | SEC:45 | 200 capture | CONFIRMED |  |
| 243 | 持續檢查新的提交；整個存放庫也能隨需或依排程掃 | security-steps.data.steps[4].detail | R:59–60；SEC:45 | 200 capture | CHANGED | 公司多的是把整個存放庫排程掃 → 持續檢查新的提交；整個存放庫也能隨需或依排程掃 〔沒有來源說排程掃是公司帳號才有；整項適用於所有 Codex 使用者〕 |
| 244 | learn.chatgpt.com/docs/security/setup，2026-10-03 | security-steps.data.note | SEC:35 | 200 capture | CONFIRMED |  |
| 245 | Codex Security Cloud 的五步：裝外掛程式，連 GitHub，跑一次性掃描。 | security-steps / e4t5 | SEC:41–43 | 200 capture | CONFIRMED |  |
| 246 | 看發現，看過再出草稿提取要求；再開持續掃描，整個存放庫也能排程掃。 | security-steps / e5gx | SEC:44–45；R:59 | 200 capture | CHANGED | 看發現，按一下出草稿提取要求；再開持續掃描，整個存放庫也能排程掃。 → 看發現，看過再出草稿提取要求；再開持續掃描，整個存放庫也能排程掃。 〔Fix with Codex 出補丁、看過再按 Create draft pull request，不是按一下〕 |
| 247 | 人走了，掃描沒停，這就是雲端掃描的意思；公司帳號還要多看兩件事。 | shutter-light / ejnp | R:59 | 200 capture | CONFIRMED |  |
| 248 | 公司要多看的兩件事 | company-two.data.title | SELF | — | CONFIRMED |  |
| 249 | 資料駐留端點：2026-03-05 起發布、且符合資格的模型，**加價 10%** | company-two.data.items[0] | PRICE:951–953, 1069 | 200 curl | CONFIRMED |  |
| 250 | Enterprise 的 Ultrafast **預設關**；要美國以外推論駐留的工作區不開放 | company-two.data.items[1] | SPEED:21, 26 | 200 capture | CONFIRMED |  |
| 251 | API 價目表與 Speed 頁，2026-10-03 | company-two.data.note | PRICE:951；SPEED:7 | 200 curl；200 capture | CONFIRMED |  |
| 252 | 第一件，資料駐留端點，對今年 3 月 5 日起發布的模型加價一成。 | company-two / emau | PRICE:951–953, 1069 | 200 curl | CONFIRMED | 口播省了「符合資格」，字卡有 |
| 253 | 第二件，Enterprise 的 Ultrafast 預設關；要美國以外推論駐留的不開放。 | company-two / ewnp | SPEED:21, 26 | 200 capture | CONFIRMED |  |
| 254 | 市集，用既有合約的承諾支出買夥伴的軟體；首批 32 家是 OpenAI 自己的數字。 | back-door / exwz | R:134 | 200 capture | CONFIRMED | 32 家說明是 OpenAI 的數字 |
| 255 | 市集現在是測試版，誰符合資格以官網為準。 | pass-window / ey9z | R:135 | 200 capture | CONFIRMED |  |
| 256 | 接 API 的人，牌價到底變了多少？ | pass-window / fctp | SELF | — | OUT OF SCOPE | 提問 |
| 257 | 開發者的清單：三個數字，和 Ultrafast 的三種付法 | ch6.chapter | PRICE:913–914, 949；PRO:25；SPEED:20 | 200 curl；200 capture | CONFIRMED |  |
| 258 | 06 | ch6.data.number | SELF | — | OUT OF SCOPE | 版面 |
| 259 | 開發者的清單：三個數字 | ch6.data.title | BRIEF:31 | repo | CONFIRMED |  |
| 260 | 五分之一、六倍、五百美元，和 Ultrafast 的三種付法 | ch6.data.subtitle | PRICE:913–914, 949；PRO:25；SPEED:20 | 200 curl；200 capture | CONFIRMED | 三種付法＝API 牌價、方案額度、點數 |
| 261 | 開發者的清單，只要記三個數字。 | ch6 / fdmt | BRIEF:31 | repo | OUT OF SCOPE | 站主的框架 |
| 262 | 五分之一、六倍、五百美元，這三個數字，就是會動到帳單的全部。 | night-market / fezv | BRIEF:31 | repo | OUT OF SCOPE | 看法（站主觀點第三段），沒有標；和第 5 章的加價 10% 有出入，留給聽感階段 |
| 263 | 會動到帳單的只有 | three-numbers.data.kicker | BRIEF:31 | repo | OUT OF SCOPE | 同上 |
| 264 | 五分之一・**六倍**・五百美元 | three-numbers.data.text | PRICE:913–914, 949；PRO:25 | 200 curl；200 capture | CONFIRMED |  |
| 265 | Sol 的牌價・Ultrafast 的牌價・Pro 500 的月費 | three-numbers.data.sub | PRICE:913–914, 949；PRO:25 | 200 curl；200 capture | CONFIRMED |  |
| 266 | Sol 的牌價、Ultrafast 的牌價，和 Pro 500 的月費。 | three-numbers / fgw6 | PRICE:913–914, 949；PRO:25 | 200 curl；200 capture | CONFIRMED |  |
| 267 | 先看六倍。Ultrafast 在 API 價目表上，每一欄都是標準的六倍。 | price-board / fidp | PRICE:913, 949 | 200 curl | CONFIRMED | 八格都是 6 倍，重算過 |
| 268 | GPT-6 Astra 標準 → Ultrafast，每百萬 token | uf-stats.data.title | PRICE:906–949 | 200 curl | CONFIRMED |  |
| 269 | $10 → $60 | uf-stats.data.stats[0].value | PRICE:913, 949 | 200 curl | CONFIRMED | 10→60、1→6、50→300 |
| 270 | 輸入 | uf-stats.data.stats[0].label | PRICE:913, 949 | 200 curl | CONFIRMED | 10→60、1→6、50→300 |
| 271 | $1 → $6 | uf-stats.data.stats[1].value | PRICE:913, 949 | 200 curl | CONFIRMED | 10→60、1→6、50→300 |
| 272 | 快取輸入 | uf-stats.data.stats[1].label | PRICE:913, 949 | 200 curl | CONFIRMED | 10→60、1→6、50→300 |
| 273 | $50 → $300 | uf-stats.data.stats[2].value | PRICE:913, 949 | 200 curl | CONFIRMED | 10→60、1→6、50→300 |
| 274 | 輸出 | uf-stats.data.stats[2].label | PRICE:913, 949 | 200 curl | CONFIRMED | 10→60、1→6、50→300 |
| 275 | developers.openai.com 價目表 2026-10-03；長脈絡 $120／$12／$450；Ultrafast… | uf-stats.data.source | PRICE:946–949 | 200 curl | CONFIRMED | 長脈絡 120／12／450；表裡只有 gpt-6-astra |
| 276 | 輸入，每百萬 token，從 10 美元變成 60 美元。 | uf-stats / fkad | PRICE:913, 949 | 200 curl | CONFIRMED |  |
| 277 | 快取輸入從 1 美元變 6，輸出從 50 美元變 300。 | uf-stats / fn6g | PRICE:913, 949 | 200 curl | CONFIRMED |  |
| 278 | 它賣的是速度；OpenAI 說 Codex 裡最高八倍，API 的倍數兩頁不同，以官網為準。 | scooter / fzis | R:36；UF:927 | 200 capture；200 curl | CONFIRMED | 速度說明是 OpenAI 的說法 |
| 279 | 它賣的，和它收的 | speed-vs-money.data.title | SELF | — | CONFIRMED |  |
| 280 | 它賣的是速度（OpenAI 的說法） | speed-vs-money.data.left.heading | R:36 | 200 capture | CONFIRMED |  |
| 281 | Codex 最高 8 倍、每秒 300 token | speed-vs-money.data.left.points[0] | R:36 | 200 capture | CONFIRMED |  |
| 282 | API：回顧頁寫 6 倍、指南寫 up to 8x，以官網為準 | speed-vs-money.data.left.points[1] | R:36；UF:927 | 200 capture；200 curl | CONFIRMED |  |
| 283 | 量的是生成速度，不是整件任務的完成時間 | speed-vs-money.data.left.points[2] | SPEED:18 | 200 capture | CONFIRMED |  |
| 284 | 它收的是錢 | speed-vs-money.data.right.heading | SELF | — | CONFIRMED |  |
| 285 | API 牌價每欄 6 倍 | speed-vs-money.data.right.points[0] | PRICE:913, 949 | 200 curl | CONFIRMED |  |
| 286 | 方案額度 8 份、買的點數 6 倍 | speed-vs-money.data.right.points[1] | SPEED:20；PRO:66 | 200 capture | CONFIRMED |  |
| 287 | Fast 是 2.5 份／2 倍 | speed-vs-money.data.right.points[2] | SPEED:15；PRO:66 | 200 capture | CONFIRMED |  |
| 288 | 官方頁寫明倍數是計費率，不是速度保證 | speed-vs-money.data.verdict | PRO:66；SPEED:15, 20 | 200 capture | CONFIRMED |  |
| 289 | 左邊是它賣的，速度，量的是生成速度，不是整件任務。 | speed-vs-money / gqvg | SPEED:18 | 200 capture | CONFIRMED |  |
| 290 | 右邊是它收的，牌價六倍、方案額度八份、點數六倍。 | speed-vs-money / grgg | PRICE:949；SPEED:20 | 200 curl；200 capture | CONFIRMED |  |
| 291 | 再看五分之一。另一支算過整月帳單，Astra 約 348 美元，GPT-6 Sol 約 70。 | scale-hands / guna | G6:12 | repo | CHANGED | 再看五分之一。上一支算過整月帳單，Astra 約 348 美元，GPT-6 Sol 約 70。 → 再看五分之一。另一支算過整月帳單，Astra 約 348 美元，GPT-6 Sol 約 70。 〔348 與 69.60 是那一支用假設用量算的；「上一支」已經指另一支影片〕 |
| 292 | GPT-6.1 Sol 的牌價，每百萬 token，2026-10-03 | sol-price.data.kicker | PRICE:914 | 200 curl | CONFIRMED |  |
| 293 | 輸入 $2、輸出 $10 ⏎ Astra 的**五分之一** | sol-price.data.text | PRICE:913–914；MODEL:957–967 | 200 curl | CONFIRMED |  |
| 294 | 快取輸入 $0.10 是十分之一・脈絡 1,050,000、知識截止 2026-04-30・不做任務算術 | sol-price.data.sub | PRICE:913–914；MODEL:944, 948 | 200 curl | CONFIRMED | 0.10 ÷ 1.00；1,050,000；Apr 30, 2026 |
| 295 | GPT-6.1 Sol 的牌價是 Astra 的五分之一，快取輸入是十分之一。 | sol-price / gyue | PRICE:913–914 | 200 curl | CONFIRMED |  |
| 296 | 該不該換 Sol？那一支的公式改一個數字；不是我替你選，是你的帳單替你選。 | coins-count / gznr | G6:12；PRICE:914 | repo；200 curl | CHANGED | 該不該換 Sol？上一支的公式改一個數字；不是我替你選，是你的帳單替你選。 → 該不該換 Sol？那一支的公式改一個數字；不是我替你選，是你的帳單替你選。 〔同 guna；只有快取輸入的價不同（0.20 → 0.10）；看法有標「我」〕 |
| 297 | 再來三件事，API 的人直接用得到；Agents API 像把攤子交給幫手，底層由 OpenAI 代管。 | hand-over / h2gh | R:66–69；AG:39 | 200 capture | CHANGED | 再來三項，API 的人直接用得到；Agents API 像把攤子交給幫手，底層由 OpenAI 代管。 → 再來三件事，API 的人直接用得到；Agents API 像把攤子交給幫手，底層由 OpenAI 代管。 〔Agents API 的電腦操作在回顧頁是一項，三個條目是三件事不是三項〕 |
| 298 | API 直接用得到的三件事 | api-three.data.title | R:66–69 | 200 capture | CHANGED | API 直接用得到的三項 → API 直接用得到的三件事 〔同上〕 |
| 299 | GPT-6 Astra 的 **service_tier: ultrafast**：所有 API 使用者，速率上限低 | api-three.data.items[0] | UF:934–935, 941 | 200 curl | CONFIRMED |  |
| 300 | **Agents API**：不另收費，只付 token 與工具 | api-three.data.items[1] | AG:57 | 200 capture | CONFIRMED | 沒寫是公開測試版（AG:15），見摘要 |
| 301 | **Agents API 的電腦操作**：API；Pro 500 與符合資格的 Enterprise 在 Codex 與 Cha… | api-three.data.items[2] | R:67–68；CU | 200 capture；200 curl | CONFIRMED |  |
| 302 | Ultrafast 指南、Agents API 頁、回顧頁，2026-10-03 | api-three.data.note | UF:925；AG:3；R:5 | 200 curl；200 capture | CONFIRMED |  |
| 303 | Astra 的 Ultrafast 在 API 所有人能開；Agents API 只付 token 和工具。 | api-three / h6xm | UF:934–935；AG:57 | 200 curl；200 capture | CONFIRMED |  |
| 304 | 新加的電腦操作，API 能用，Pro 500 在 Codex 裡也能用。 | api-three / h9w3 | R:67–68 | 200 capture | CONFIRMED | 口播只說 Pro 500 與 Codex；字卡完整 |
| 305 | Decisions API 像射氣球，答案只有幾個固定的位置，現在是限量預覽。 | balloon-stall / hh5s | R:63–64；LLMS；CHG | 200 capture；200 curl | CONFIRMED | 今天的文件索引與 changelog 沒有 Decisions 項目，看不出已全面開放；會過期 |
| 306 | 三項以官網為準 | dev-three.data.title | SELF | — | CONFIRMED |  |
| 307 | **Decisions API**：Luna，有限的預設答案；限量預覽 | dev-three.data.items[0] | R:63–64 | 200 capture | CONFIRMED | 會過期 |
| 308 | **Amazon Bedrock Managed Agents**：給在 AWS 上開發的團隊 | dev-three.data.items[1] | R:72；BED | 200 capture；200 curl | CONFIRMED |  |
| 309 | **MCP 事件**：提議中的規格；回顧頁寫適用於所有方案 | dev-three.data.items[2] | R:90–91；MCP | 200 capture；200 curl | CONFIRMED |  |
| 310 | 回顧頁 2026-09-29；回顧頁沒附 Decisions API 與 Bedrock 的文件連結 | dev-three.data.note | R:64, 73；BED；LLMS | 200 capture；200 curl | CHANGED | 回顧頁 2026-09-29；Decisions API 與 Bedrock 沒有正式文件連結 → 回顧頁 2026-09-29；回顧頁沒附 Decisions API 與 Bedrock 的文件連結 〔Bedrock 今天有正式文件頁（200）；回顧頁沒附連結才是事實〕 |
| 311 | Decisions API 和 Bedrock 的細節，都以官網為準。 | dev-three / hhwj | R:64, 73 | 200 capture | CONFIRMED |  |
| 312 | MCP 事件，規格還在提議中，放這裡只因為它是給開發者接的。 | dev-three / i9h6 | R:90；MCP | 200 capture；200 curl | CONFIRMED |  |
| 313 | 開發者的清單就這些，照回顧頁算是四項，看牌價。 | lights-off / ier5 | R:35, 62, 66, 71 | 200 capture | CHANGED | 開發者的清單就這些，四項看牌價。 → 開發者的清單就這些，照回顧頁算是四項，看牌價。 〔卡片上看到五個條目，回顧頁算四項〕 |
| 314 | 這週該先做哪件事？ | lights-off / ik64 | SELF:week-steps | — | CHANGED | 這週，每一張清單的人該先做哪件事？ → 這週該先做哪件事？ 〔week-steps 只有四步，沒有團隊那一步〕 |
| 315 | 這週做的一件事，和還不能碰的 | home-table.chapter | SELF | — | CONFIRMED |  |
| 316 | 最後，這週先做一件事。 | home-table / imik | SELF:week-steps | — | CHANGED | 最後，每一張清單的人，這週先做一件事。 → 最後，這週先做一件事。 〔同 ik64〕 |
| 317 | 這週做的一件事 | week-steps.data.title | SELF | — | CONFIRMED |  |
| 318 | 所有人：登入按鈕先讀三樣 | week-steps.data.steps[0].title | SIWC:27, 31 | 200 capture | CONFIRMED |  |
| 319 | 姓名、電子郵件、個人檔案照片；第二個請求要就設上限 | week-steps.data.steps[0].detail | SIWC:27, 31 | 200 capture | CONFIRMED |  |
| 320 | Plus：10/14 前在 Codex 改選一個還在的模型 | week-steps.data.steps[1].title | SPEED:32 | 200 capture | CONFIRMED |  |
| 321 | 哪一個合用，拿自己的任務算一次再定 | week-steps.data.steps[1].detail | SPEED:32 | 200 capture | CONFIRMED |  |
| 322 | Pro：有 dot 的人設一件要先核准；Pro 200 看我的方案 | week-steps.data.steps[2].title | DOTS:76；PRO:69 | 200 capture | NOT FOUND | Pro：有 dot 的人設一件「要先核准」；Pro 200 看「我的方案」 → Pro：有 dot 的人設一件要先核准；Pro 200 看我的方案 〔「要先核准」「我的方案」加引號當介面字樣沒有來源；拿掉引號〕 |
| 323 | dots 的自訂規則挑一件會動到別人的操作；再翻信箱找 OpenAI 的通知 | week-steps.data.steps[2].detail | DOTS:76；PRO:38 | 200 capture | CONFIRMED |  |
| 324 | 開發者：要速度，才套 ×6 或 8 份 | week-steps.data.steps[3].title | PRICE:949；PRO:66 | 200 curl；200 capture | CONFIRMED |  |
| 325 | Sol 對 Astra 的月帳單，用另一支的公式 | week-steps.data.steps[3].detail | G6:12 | repo | CHANGED | Sol 對 Astra 的月帳單，用上一支的公式 → Sol 對 Astra 的月帳單，用另一支的公式 〔同 guna〕 |
| 326 | 所有人，下次看到登入按鈕，先讀那三樣，再決定要不要勾第二個。 | week-steps / imw5 | SIWC:27, 31 | 200 capture | CONFIRMED |  |
| 327 | Plus，10 月 14 日前，在 Codex 改選一個還在的模型，自己試一次。 | week-steps / iq7s | SPEED:32 | 200 capture | CONFIRMED |  |
| 328 | Pro，有 dot 的設一件要先核准；Pro 200 看我的方案，再翻信箱找通知。 | week-steps / it7b | DOTS:76；PRO:38, 69 | 200 capture | CONFIRMED |  |
| 329 | 開發者，先問要不要速度；要，才把六倍或八份套到自己的用量上。 | week-steps / ive6 | PRICE:949；PRO:66 | 200 curl；200 capture | CONFIRMED |  |
| 330 | 這些都是設定上的界線，不是寫在提示裡的不要。 | door-chain / jr8w | BRIEF:25 | repo | OUT OF SCOPE | 立場 5；只有登入與 dots 兩步是設定上的界線 |
| 331 | 還有幾項，官網寫著即將推出，今天還碰不到，先不用等。 | pencil-pass / j39w | R:37, 97, 117, 121；DOTS:60；SPACE:10, 23 | 200 capture | CONFIRMED |  |
| 332 | 還不能碰的 | not-yet.data.title | SELF | — | CONFIRMED |  |
| 333 | **GPT-6.1 Sol Ultrafast**：回顧頁寫即將推出、Sol 頁寫一併推出，以官網為準 | not-yet.data.items[0] | R:37；SOL:55 | 200 capture | CONFIRMED |  |
| 334 | **空間的行動版編輯、投影片多人協作**：空間頁寫即將推出 | not-yet.data.items[1] | SPACE:10, 18, 23 | 200 capture | CONFIRMED |  |
| 335 | **會議外掛程式的 Enterprise** | not-yet.data.items[2] | R:117 | 200 capture | CONFIRMED |  |
| 336 | **Decisions API 全面開放** | not-yet.data.items[3] | R:64 | 200 capture | CONFIRMED | 會過期 |
| 337 | **dots 的簡訊** | not-yet.data.items[4] | DOTS:60 | 200 capture | CONFIRMED |  |
| 338 | **個人檔案的 Enterprise／Edu／Healthcare** | not-yet.data.items[5] | R:121 | 200 capture | CONFIRMED |  |
| 339 | 回顧頁、空間頁、dots 頁寫「即將推出」的，2026-10-03；Sol 頁寫法不同 | not-yet.data.note | SOL:55 | 200 capture | CHANGED | 回顧頁、Sol 頁、空間頁、dots 頁寫「即將推出」的，2026-10-03 → 回顧頁、空間頁、dots 頁寫「即將推出」的，2026-10-03；Sol 頁寫法不同 〔Sol 頁全文沒有「即將推出」，它寫的是一併推出〕 |
| 340 | Sol 的 Ultrafast 以官網為準；空間的行動版編輯和投影片協作；會議外掛程式的 Enterprise 版。 | not-yet / j8df | R:37, 117；SOL:55；SPACE:10, 23 | 200 capture | CONFIRMED |  |
| 341 | Decisions API 的全面開放，dots 的簡訊，個人檔案的 Enterprise、Edu、Healthcare 版。 | not-yet / j8m9 | R:64, 121；DOTS:60 | 200 capture | CONFIRMED |  |
| 342 | 加起來，25 項，每一項都有它的位置。 | window-street / j9ty | R:27–133 | 200 capture | CONFIRMED |  |
| 343 | 25 項，照清單加總 | tally-stats.data.title | SELF | — | CONFIRMED |  |
| 344 | 9 | tally-stats.data.stats[0].value | R:48, 52, 56, 60, 79, 83, 91, 121, 127 | 200 capture | CONFIRMED |  |
| 345 | 所有人：沒指定付費方案 | tally-stats.data.stats[0].label | R:48, 52, 56, 60, 79, 83, 91, 121, 127 | 200 capture | CHANGED | 所有人：登入就有 → 所有人：沒指定付費方案 〔同 3qfi〕 |
| 346 | +1 | tally-stats.data.stats[1].value | SOL:53 | 200 capture | CONFIRMED |  |
| 347 | Plus：GPT-6.1 Sol | tally-stats.data.stats[1].label | SOL:53 | 200 capture | CONFIRMED |  |
| 348 | +6 | tally-stats.data.stats[2].value | R:97, 101, 105, 117, 29, 130 | 200 capture | CONFIRMED | 4＋1＋1 |
| 349 | Pro：4 項、dots 看市場、Pro 500 一階 | tally-stats.data.stats[2].label | R:97, 101, 105, 117, 29, 130 | 200 capture | CONFIRMED | 4＋1＋1 |
| 350 | +9 | tally-stats.data.stats[3].value | R:41, 87, 109, 113, 135, 35, 62, 66, 71 | 200 capture | CONFIRMED | 5＋4；9＋1＋6＋9＝25 |
| 351 | 團隊 5 項、開發者 4 項看牌價 | tally-stats.data.stats[3].label | R:41, 87, 109, 113, 135, 35, 62, 66, 71 | 200 capture | CONFIRMED | 5＋4；9＋1＋6＋9＝25 |
| 352 | Codex Security Cloud 與 MCP 事件只算在所有人的九項裡；Agents API 和它的電腦操作在回顧頁是同… | tally-stats.data.source | R:60, 91, 66–69 | 200 capture | CHANGED | Codex Security Cloud 與 MCP 事件只算在所有人的九項裡 → Codex Security Cloud 與 MCP 事件只算在所有人的九項裡；Agents API 和它的電腦操作在回顧頁是同一項 〔補上 Agents API 那一項的算法〕 |
| 353 | 官網沒指定付費方案的有 9 項，Plus 再加 Sol 一項。 | tally-stats / ja8a | R:48, 52, 56, 60, 79, 83, 91, 121, 127 | 200 capture | CHANGED | 官網說登入就有 9 項，Plus 再加 Sol 一項。 → 官網沒指定付費方案的有 9 項，Plus 再加 Sol 一項。 〔同 3qfi〕 |
| 354 | Pro 加 4 項、dots 看市場、Pro 500 算一項；團隊 5、開發者 4，一共 25。 | tally-stats / jg96 | R:27–133 | 200 capture | CONFIRMED | 9＋1＋6＋5＋4＝25 |
| 355 | 不是新聞說了幾項，是你付的那種方案裡，今天打開就有的那幾項。 | hall-light / jne3 | BRIEF:27 | repo | OUT OF SCOPE | 站主的框架 |
| 356 | 25 項裡，你今天碰得到幾項？ | outro.data.title | R:27–133 | 200 capture | CONFIRMED |  |
| 357 | 沒指定付費方案的 9 項 | outro.data.lines[0] | R:48, 52, 56, 60, 79, 83, 91, 121, 127 | 200 capture | CHANGED | 登入就有 9 項 → 沒指定付費方案的 9 項 〔同 3qfi〕 |
| 358 | Plus 再加 Sol | outro.data.lines[1] | SOL:53 | 200 capture | CONFIRMED |  |
| 359 | Pro 再加 4 項、dots 看市場、Pro 500 一階 | outro.data.lines[2] | R:97, 101, 105, 117, 29, 130 | 200 capture | CONFIRMED |  |
| 360 | 團隊 5 項・開發者 4 項看牌價 | outro.data.lines[3] | R:41, 87, 109, 113, 135, 35, 62, 66, 71 | 200 capture | CONFIRMED |  |
| 361 | 留言告訴我你是哪一張清單的人，這週先碰哪一項 | outro.data.cta | SELF | — | OUT OF SCOPE | 呼籲留言 |
| 362 | 要不要多付，三個數字算完再說；留言告訴我，你是哪一張清單的人。 | outro / jpxt | BRIEF:31 | repo | OUT OF SCOPE | 看法與呼籲（立場 1） |
| 363 | DevDay 2026 的 25 項，你今天碰得到幾項？答案在你付的是哪一種方案 | shorts[0].titles[0] | R:27–133 | 200 capture | CONFIRMED |  |
| 364 | DevDay 發表了二十幾樣，官網沒指定付費方案的有 9 項：照方案分五張清單 | shorts[0].titles[1] | R:15, 48, 52, 56, 60, 79, 83, 91, 121, 127 | 200 capture | CHANGED | DevDay 發表了二十幾樣，官網說登入就有的是 9 項：照方案分五張清單 → DevDay 發表了二十幾樣，官網沒指定付費方案的有 9 項：照方案分五張清單 〔同 3qfi〕 |
| 365 | DevDay 2026 的回顧頁列了 25 項，你今天打開 ChatGPT 碰得到幾項？答案在你付的是哪一種方案：官網沒指定付費… | shorts[0].description | R:27–133；SOL:53 | 200 capture | CHANGED | 官網說登入就有 9 項…每一張清單這週先做哪件事，完整的在長片。 → 官網沒指定付費方案的有 9 項…這週先做哪件事，完整的在長片。 〔同 3qfi、ik64〕 |
| 366 | 25 項，你今天碰得到幾項？ | shorts[0].scenes[0].headline | R:15 | 200 capture | CONFIRMED |  |
| 367 | DevDay 一口氣發表了二十幾樣東西。 | shorts[0].scenes[0].narration[0] | R:15 | 200 capture | CONFIRMED |  |
| 368 | 你今天打開 ChatGPT，碰得到幾樣？ | shorts[0].scenes[0].narration[1] | R:15 | 200 capture | CONFIRMED |  |
| 369 | 答案在你付的是哪一種方案 | shorts[0].scenes[1].headline | R:27–133 | 200 capture | CONFIRMED |  |
| 370 | 答案不在新聞裡，在你付的是哪一種方案。 | shorts[0].scenes[1].narration[0] | R:27–133 | 200 capture | CONFIRMED |  |
| 371 | 回顧頁的 25 項，照方案分成五張清單。 | shorts[0].scenes[1].narration[1] | R:27–133 | 200 capture | CONFIRMED |  |
| 372 | 沒指定付費方案的 9 項，Plus 再加 Sol | shorts[0].scenes[2].headline | R:48, 52, 56, 60, 79, 83, 91, 121, 127 | 200 capture | CHANGED | 登入就有 9 項，Plus 再加 Sol → 沒指定付費方案的 9 項，Plus 再加 Sol 〔同 3qfi〕 |
| 373 | 9 項 | shorts[0].scenes[2].big | R:48, 52, 56, 60, 79, 83, 91, 121, 127 | 200 capture | CONFIRMED |  |
| 374 | 官網沒指定付費方案的有 9 項，Plus 再加 Sol 一項。 | shorts[0].scenes[2].narration[0] | R:48, 52, 56, 60, 79, 83, 91, 121, 127 | 200 capture | CHANGED | 官網說登入就有 9 項，Plus 再加 Sol 一項。 → 官網沒指定付費方案的有 9 項，Plus 再加 Sol 一項。 〔同 ja8a〕 |
| 375 | Sol 在 ChatGPT 工作和 Codex 裡能選，對話裡還沒有。 | shorts[0].scenes[2].narration[1] | SOL:53 | 200 capture | CONFIRMED |  |
| 376 | Pro、團隊、開發者，加起來 25 | shorts[0].scenes[3].headline | R:27–133 | 200 capture | CONFIRMED | 4＋1＋1、5、4，一共 25 |
| 377 | Pro 加 4 項、dots 看市場、Pro 500 算一項。 | shorts[0].scenes[3].narration[0] | R:27–133 | 200 capture | CONFIRMED | 4＋1＋1、5、4，一共 25 |
| 378 | 團隊 5 項、開發者 4 項，一共 25。 | shorts[0].scenes[3].narration[1] | R:27–133 | 200 capture | CONFIRMED | 4＋1＋1、5、4，一共 25 |
| 379 | 你是哪一張清單？完整的在長片 | shorts[0].scenes[4].headline | SELF | — | OUT OF SCOPE | 呼籲 |
| 380 | 這週先做哪件事，完整的在長片。 | shorts[0].scenes[4].narration[0] | SELF:week-steps | — | CHANGED | 每一張清單這週先做哪件事，完整的在長片。 → 這週先做哪件事，完整的在長片。 〔同 ik64〕 |
| 381 | 每月五百美元的 Pro 500，買到的不是更聰明的模型 | shorts[1].titles[0] | PRO:25, 27；BRIEF:31 | 200 capture；repo | CONFIRMED | 看法，和站主觀點一致 |
| 382 | 同一件事，Ultrafast 算 8 份額度：Pro 500 買到的是速度 | shorts[1].titles[1] | PRO:66 | 200 capture | CONFIRMED |  |
| 383 | ChatGPT Pro 現在有三階，只有每月五百美元的 Pro 500 含 Ultrafast。它買到的是速度和最高額度，不是更… | shorts[1].description | PRO:21–25, 49, 66 | 200 capture | CONFIRMED |  |
| 384 | 五百美元，買到的不是更聰明 | shorts[1].scenes[0].headline | PRO:25, 27；R:130；BRIEF:31 | 200 capture；repo | CONFIRMED | 事實部分成立；結論是看法 |
| 385 | 每月五百美元的 Pro 500，買到的不是更聰明的模型。 | shorts[1].scenes[0].narration[0] | PRO:25, 27；R:130；BRIEF:31 | 200 capture；repo | CONFIRMED | 事實部分成立；結論是看法 |
| 386 | 買到的是速度和最高額度。 | shorts[1].scenes[0].narration[1] | PRO:25, 27；R:130；BRIEF:31 | 200 capture；repo | CONFIRMED | 事實部分成立；結論是看法 |
| 387 | Pro 三階，只有 Pro 500 含 Ultrafast | shorts[1].scenes[1].headline | PRO:21–25 | 200 capture | CONFIRMED |  |
| 388 | $500 | shorts[1].scenes[1].big | PRO:21–25 | 200 capture | CONFIRMED |  |
| 389 | Pro 現在有三階。 | shorts[1].scenes[1].narration[0] | PRO:21–25 | 200 capture | CONFIRMED |  |
| 390 | Pro 100 和 Pro 200，都不含 Ultrafast。 | shorts[1].scenes[1].narration[1] | PRO:21–25 | 200 capture | CONFIRMED |  |
| 391 | 同一件事，Ultrafast 算 8 份額度 | shorts[1].scenes[2].headline | PRO:66 | 200 capture | CONFIRMED | 10 × 8 |
| 392 | 8 份 | shorts[1].scenes[2].big | PRO:66 | 200 capture | CONFIRMED | 10 × 8 |
| 393 | 同一件事，標準算 1 份額度，Astra Ultrafast 算 8 份。 | shorts[1].scenes[2].narration[0] | PRO:66 | 200 capture | CONFIRMED | 10 × 8 |
| 394 | 每天跑 10 件，就是標準 80 件的額度。 | shorts[1].scenes[2].narration[1] | PRO:66 | 200 capture | CONFIRMED | 10 × 8 |
| 395 | 值不值這八倍，先數你在等的事 | shorts[1].scenes[3].headline | BRIEF:31 | repo | OUT OF SCOPE | 看法 |
| 396 | 先數你一天有幾件事，是坐著等它跑完的。 | shorts[1].scenes[3].narration[0] | BRIEF:31 | repo | OUT OF SCOPE | 看法 |
| 397 | 等的時間值不值這八倍，只有你的量算得出來。 | shorts[1].scenes[3].narration[1] | BRIEF:31 | repo | OUT OF SCOPE | 看法 |
| 398 | Pro 三階怎麼對號，完整的在長片 | shorts[1].scenes[4].headline | SELF | — | OUT OF SCOPE | 呼籲 |
| 399 | Pro 三階怎麼對號，舊用戶的四步，完整的在長片。 | shorts[1].scenes[4].narration[0] | SELF | — | OUT OF SCOPE | 呼籲 |
<!-- end of claim table -->

## Summary

**Claims checked:** 399 strings (362 in `video.json`, 37 in `shorts.json`). **Confirmed:** 305. **Changed:** 45 strings, which are 23 facts and their dependants. **Not found:** 10 strings, which are 4 claims; each was rewritten without the unsupported part. **Out of scope:** 39 (questions, layout values, the owner's framing and opinions). Every price, multiplier, plan price, context size, percentage and calendar date matches its source; the ratios and sums were recomputed (Sol ÷ Astra = 0.2 on input, output and cache writes and 0.1 on cached input; Ultrafast ×6 in all eight columns; 10 × 8 = 80; 4+7+4+7+3 = 25; 9+1+6+5+4 = 25; 348 and 69.60). What changed is how counts, availability and earlier videos are described.

**Fact changes (where | before → after):**

1. pool-desk/3qfi, tally-stats/ja8a, tally-stats.stats[0].label, outro.lines[0], ch2.subtitle, Short 1 (title 2, description, scene 2 headline and narration) | 「寫的是登入就有」「官網說登入就有 9 項」「登入就有 9 項」「官網寫「適用於所有方案」的那一行」 → 「沒有指定付費方案」「官網沒指定付費方案的有 9 項」「沒指定付費方案的 9 項」「回顧頁「適用於」那一行沒指定付費方案」 (R:48, 52, 56, 60, 79, 83, 91, 121, 127: no line says 登入就有; only six say 適用於所有方案).
2. lane-wide/4py7 | 「剩下五項，每個人都會碰到。」 → 「剩下五項，也沒指定付費方案。」 (three of the five are things developers build; R:121).
3. five-more.items[3] | 「所有其他方案已有」 → 「Enterprise、Edu、Healthcare 即將推出，其他方案已有」 (R:121).
4. three-vs.title, three-vs.right.heading, three-vs/6bae | 「和永遠不給的」「永遠不給的」「一律不給。」 → 「和登入不給的」「登入本身不給的」「登入本身都不給。」 (SIWC:32 "does not independently share", SIWC:36 "An application can separately request delegated access").
5. ch4/977k | 「Pro 那一張清單最長，而且和你的帳單有關。」 → 「Pro 那一張清單，和你的帳單有關。」 (the script's own tally: 所有人 9, Pro 6).
6. pro-five.items[1], pro-five/a3tb, description | 「行動版只能看」 → 「行動版，空間頁寫只能看、回顧頁寫即將推出，以官網為準」／「行動版兩頁寫法不同，以官網為準。」 (R:97 against SPACE:23, 31).
7. wheel-alone/a8fd, description bullet 1 | 「dots 怎麼運作、怎麼失敗，上一支講過了；這裡只講額度，和三條界線。」 → 「AI 代理怎麼運作、怎麼失敗，上一支講過了；這裡只講 dots 的額度，和三條界線。」 (AOA:18, 730).
8. pro200-steps.steps[0].title, pro200-steps/bdwn | 「…之間訂過」「…之間訂過的，」 → 「…之間訂閱有效過」「…之間有訂閱的，」 (PRO:37 "had an active Pro 200 subscription at any point").
9. ch5/d4k8, ch5.subtitle | 「公司或團隊用 Business、Enterprise 的人，多了五項。」「Business、Enterprise 多的五項，…」 → 「公司或團隊的帳號，多了五項。」「公司帳號多的五項，…」 (only R:109 and R:113 name those two plans).
10. team-five.items[3], blank-board/dyna | 「零資料保留搭配私密安全處理，按專案開」「私密智慧按專案開」 → 「API 的零資料保留搭配私密安全處理，按專案開」「私密智慧按 API 專案開」 (PSP:971, 974).
11. security-steps.steps[4].detail | 「公司多的是把整個存放庫排程掃」 → 「持續檢查新的提交；整個存放庫也能隨需或依排程掃」 (R:59–60: the item is for all Codex users).
12. security-steps/e5gx | 「按一下出草稿提取要求」 → 「看過再出草稿提取要求」 (SEC:44: Fix with Codex makes a patch; "Review the patch before selecting Create draft pull request").
13. scale-hands/guna, coins-count/gznr, week-steps.steps[3].detail | 「上一支算過」「上一支的公式」「用上一支的公式」 → 「另一支算過」「那一支的公式」「用另一支的公式」 (上一支 already points at another video in a8fd).
14. hand-over/h2gh, api-three.title, lights-off/ier5, tally-stats.source | 「再來三項」「API 直接用得到的三項」「四項看牌價。」 → 「再來三件事」「API 直接用得到的三件事」「照回顧頁算是四項，看牌價。」, and the tally card's small print gains 「Agents API 和它的電腦操作在回顧頁是同一項」 (R:66–69).
15. dev-three.note | 「Decisions API 與 Bedrock 沒有正式文件連結」 → 「回顧頁沒附 Decisions API 與 Bedrock 的文件連結」 (BED answers 200 today).
16. lights-off/ik64, home-table/imik, Short 1 (description, scene 5) | 「這週，每一張清單的人該先做哪件事？」「最後，每一張清單的人，這週先做一件事。」 → 「這週該先做哪件事？」「最後，這週先做一件事。」 (week-steps has four steps for five lists; there is no step for 團隊).
17. chat-ask/2kju, glaze-shelf/bswh | 「有人問我，」「有人問，」 → 「你可能會問，」 (the questions are the brief's; nobody asked them; stance 6).
18. youtube.description | 「同一頁寫得不一樣的地方（…）」 → 「官方頁之間寫得不一樣的地方（…，加上空間的行動版）」.
19. youtube.description | 「所有數字都是 OpenAI 自己頁面上的；」 → 「價格、倍數和日期都是 OpenAI 自己頁面上的；25、9 這些項數是照回顧頁逐項數的，348 與 70 美元是本頻道另一支影片用假設用量算的估計；」 (R:15; G6:12).
20. youtube.description, the three earlier videos | 〈聊天機器人時代結束了〉, 〈GPT-6 vs Opus 5.5 值不值得付〉, 〈AI 價格戰〉 → each video's real `youtube.title` (AOA:18, G6V:18, PW:20).
21. youtube.description, third bullet | (listed under 「影片裡提到的」) → marked 「（延伸，影片裡沒提到）」: the narration never mentions that video.
22. sources[14].title | 「MCP：Triggers and Events Working Group（提議中的事件規格）」 → 「MCP：Triggers and Events Charter（工作小組章程，提議中的事件規格）」.
23. not-yet.note | 「回顧頁、Sol 頁、空間頁、dots 頁寫「即將推出」的，2026-10-03」 → 「回顧頁、空間頁、dots 頁寫「即將推出」的，2026-10-03；Sol 頁寫法不同」 (the Sol page never says 即將推出; it says 一併推出, SOL:55).

**Not found (the claim, and what replaced it):**

1. 「說明中心 2026-10-02」 as the pages' update date (three-vs.verdict, pro-table.title, pro200-steps.note, sources[3].title, sources[4].title): both pages show only "Updated: yesterday" → 「說明中心，2026-10-03 查閱」 on the cards (「說明中心的寫法，2026-10-03 查閱」 on three-vs) and no date in the two source titles.
2. 「每階能跑幾件，官方沒數字」 (rate-stats/bra3, rate-stats.source): PRO:28 and SPEED:24 send the reader to pricing pages that were not captured, so an absence from all official pages is not shown → 「每階能跑幾件，這兩頁沒寫，以官網為準。」 and 「…這兩頁沒寫，以官網的方案比較頁為準」.
3. The Chinese button label 「以 ChatGPT 繼續」 (login-steps.steps[1].detail): only the English help page was captured → 「或 Continue with ChatGPT」 (card only).
4. 「要先核准」 and 「我的方案」 written in 「」 as interface labels (week-steps.steps[2].title, description): DOTS:76 says 「要求先取得核准」 and PRO:69 says "Settings → My Plan" → the 「」 are gone; the narration (bk3e, it7b) never had them and is unchanged.

Also in the description: the empty line between its first two lines is gone, so the second line is the "for whom" line (publish.md). The description body is 2,299 bytes, about 4,370 with the chapters and sources the tool adds (estimate), and has no angle brackets.

**Checker proposals not applied as written:**

- Numbers lens 2, narration half (bdwn → 「太平洋時間 9 月 22 日到 29 日…，訂閱有效過的，…」): the eligibility fix is applied in a shorter form (「有訂閱的」), the time zone is not added to the narration. The card on screen during that line says 「太平洋時間」, the narration is not false without it, and the proposed line would hold one card state for about nine seconds.
- The coordinator's wording for 4py7 (「也不分方案」) was conditional on the five items carrying no plan restriction. One does: 可分享的個人檔案 is not yet on Enterprise, Edu or Healthcare (R:121). I used 「也沒指定付費方案」, the same claim as 3qfi.
- Numbers lens 1 (「最複雜」): I took its other option and dropped 「最長」; 「最複雜」 would be a new opinion that is not in the brief.
- Numbers lens 3, the heavier alternative (merge the two Agents API bullets and change the reveals): not applied; it restructures a card. The 「三件事」 wording and the tally note settle the count.
- Availability lens 4 (dyna 「私密智慧在 API 按專案開」): applied as 「私密智慧按 API 專案開」, one unit shorter.
- Names lens, not-found 2 (use the pages' own words 要求先取得核准／My Plan): I took its other option and removed the 「」.
- Where two lenses proposed different wording for one place (3qfi, ja8a, d4k8, bra3, the description, api-three, ier5), the finding is applied in the coordinator's wording.
- Availability S5: confirmed today (BED and CU both 200); the note on dev-three is corrected. Neither page was added to `sources`, because no claim rests on them.

**Brief conflicts (the source wins; `brief.md` is untouched; the owner should know):** brief.md:29 says sign-in 「一律不給」 chats, memory, files, tokens and billing, and brief.md:74 names the card 「永遠不給的」 (the help page: not shared by sign-in itself, separately requestable); brief.md:31 and :157 say the earlier video explained how dots works and fails (it explains AI agents; dots gets one sentence); brief.md:79 has 「官網說登入就有 9 項」; brief.md:27 calls all four contradictions 「同一頁」 (only Codex 雲端 is one page), and 空間 on mobile is a fifth; brief.md:76 has 「訂過」 for the Pro 200 window; brief.md:77 says scheduled whole-repository scans are what company accounts get extra (「…多的是把整個存放庫排程掃」); brief.md:78 asks what every list should do first and brief.md:79 gives four steps, none for 團隊. The outline itself still holds: no chapter, card or number depends on these.

**Facts that expire soon (the official date I saw):**

- GPT-5.5 leaves ChatGPT, ChatGPT 工作 and Codex on 2026-10-14 (SPEED:32); the Plus step of week-steps reads as past after that day.
- Pro 200: the old allowance lasts through 2026-10-29 (PRO:37).
- Decisions API: 「今日起限量開放預覽，預計未來幾天內全面推出」 on a page dated 2026-09-29 (R:64). Today the API guide index, the reference index and the changelog have no Decisions entry, so I could not show a change and kept 「限量預覽」. Re-open before upload.
- dots: the higher cap is for the first month after 2026-09-29 (DOTS:96); the rollout is 「逐步」 by market (DOTS:94).
- GPT-6.1 Sol Ultrafast: 「即將推出」 (R:37); the Ultrafast price table lists only gpt-6-astra today (PRICE:946–949).
- 空間 mobile editing and slide collaboration (SPACE:10, 23), the meeting plugin for Enterprise (R:117), profiles for Enterprise, Edu and Healthcare (R:121) and dots by SMS (DOTS:60) are all 「即將推出」.
- "At launch" wording: credits on Pro 100 and 200 do not unlock Ultrafast (PRO:50); the six sign-in partners are the "initial" ones (SIWC:16).
- All prices are the list prices of 2026-10-03; the three earlier videos have `video_id` null, so the description shows their slugs where links belong.

**Opinion mismatches:** none against 站主觀點. Marked as the owner's and consistent: 53vp, bsx5, gznr, 2mr4, jpxt. Consistent but not marked as opinion: 6npj (對最多人有用的一項), b3ja (不是更聰明的模型), fezv and the three-numbers kicker (會動到帳單的全部／只有), jr8w (設定上的界線). No upgrade or model recommendation anywhere.

**Listener findings (report only, left for the listener stage):**

- No line is over 40 spoken units (longest j8df, 34); 26 lines are over 40 raw characters, the hardest to hear being j8m9 (six Latin terms), j8df and h2gh.
- No 經查證／根據官方文件／本影片, no parentheses or URLs in the narration, every Latin term is in the dictionary (lint), no reveal comes before its sentence, no `say` fields.
- 「以官網為準」 is now spoken nine times (4fu7, 9rtc, a3tb, bra3, dyna, ey9z, fzis, hhwj, j8df); two of them are from this round.
- bra3 says 「這兩頁」; the listener has only the card's small print to know which two.
- fezv says the three numbers are 「會動到帳單的全部」 while emau adds a 10% uplift and bmwj an 8-fold rate.
- The narration is narrower than its card in three places: emau drops 「符合資格」, bdwn drops 「太平洋時間」, h9w3 drops the eligible Enterprise customers and ChatGPT 工作. Agents API is a 公開測試版 (AG:15, 57) and the script never says so.
- One thing, two names: 「Codex Cloud」 (79px) and 「Codex 雲端」; 「智慧體」 (6urf) and 「AI 代理」 (a8fd, since this round); 「GPT-6 Sol」 (guna) two lines before 「GPT-6.1 Sol」 (gyue); the recap's 「極速」 is never said; 「外掛程式市集」 sits in the same chapter as 「OpenAI 市集」.
- week-steps has no step for the 團隊 list; the narration no longer promises one.
- About 30 lines join two clauses with 「；」.

**Lint after the edits:** `node tools/video/cli.mjs lint --slug openai-devday-2026-recap` → `0 errors, 21 warnings`; `Estimate: 11.7 min, 111 lines, 2550 spoken units` (before: 19 warnings, 2,532 units). All warnings are cadence: 18 card or shot states at 8.2–8.9 s, a new picture every 6.8 s on average, illustrations at 49% of the runtime, an opening chapter of 38 s. Three states are new from this round's wording (wheel-alone 8.7 s, rate-stats state 1 8.7 s, blank-board 8.5 s) and one cleared (lights-off). `shorts.json` passes the worker's check (`episodeShortsProblems`) and stays within 110–220 spoken characters; `claims.md` has 61 claims for 61 ids and all 48 quoted English sentences are verbatim in the captures. Scene ids, line ids, reveals and shot prompts are unchanged (46 leaf values of `video.json` and 5 of `shorts.json` differ from before).

**Suspected, not changed:**

- (a) The chapter name 「每個人都有的九項」 (ch2) and 2xba 「每個人都有的那一張」 are the brief's name for the first list. It is wider than the source: profiles are not on Enterprise, Edu or Healthcare yet, sign-in depends on the organization, the free plan is not named anywhere, and Codex 雲端's own paragraph says Plus and up. The chapter's cards carry those hedges; renaming a chapter is the owner's call.
- (b) The description now says 「官方頁之間寫得不一樣」 for five places; for Codex 雲端 the two wordings are two lines of one page (R:47–48). The wording is the coordinator's.
- (c) guna's $348 and $70 rest on another video's 2026-09-28 prices and an assumed workload; today's price table no longer has a gpt-6-sol row, so GPT-6 Sol's $0.20 cached price cannot be re-read on an official page. The description now says whose estimate it is; the narration does not name the workload.
- (d) 「上一支」 for always-on-agent-explained assumes that video is published first; all three earlier videos have `video_id` null.
- (e) bk3e and it7b say 「我的方案」 for "My Plan"; the Chinese interface label has no source.
- (f) aiiz and the 空間 card say sharing a page does not share private chats or memory, which is right, and leave out the same paragraph's caveat that anything written on the page, including personal details drawn from memory, is visible to everyone with access (SPACE:26).
- (g) 6grq gives one reason a company account may not see the button (global-admin policy); the help page lists three (SIWC:48).
- (h) 「隨需或依排程掃整個存放庫」 rests on the recap only (R:59); the setup page's Scan Method lists One-Time Scan and Continuous Scanning.
- (i) The Ultrafast guide has a third wording for Sol ("preview access for GPT-5.6 Sol", UF:930) that the script does not quote.
- (j) Help Center pages should be opened in a browser once more before upload: they change without a dated changelog.

**SECOND ROUND required: yes.** This round changed 23 facts, more than three.
