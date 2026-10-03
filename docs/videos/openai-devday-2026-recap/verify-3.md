# Verification round 3: openai-devday-2026-recap

Verifier: claude-fable-5-1, a separate agent session from the writer's, from both earlier verifiers' and from the fixers', working on 2026-10-04. The evidence is the coordinator's browser captures of 2026-10-03 (`_tools/sources/`), so every `checked_on` stays 2026-10-03. `openai.com`, `help.openai.com`, `chatgpt.com` and `learn.chatgpt.com` were not fetched and no browser was used. `developers.openai.com` was fetched on 2026-10-04 with the editorial user agent, 1.5 s apart: `api/docs/pricing`, `api/docs/guides/ultrafast-mode` and `api/docs/models/gpt-6.1-sol` all answered 200 and are byte-identical to the 2026-10-03 captures (580,801, 420,344 and 443,094 bytes). Web searches used: 0 of 5.

Why a third round: after `verify-2.md` (state in `_tools/snapshots/video.after-verify-2.json`, 80 scenes, 111 lines) a listener and several fixers reworded 133 strings, added 62 (15 new shot scenes, 36 new line ids, 3 lines removed) and shortened card bullets and titles. This round re-read the polished script (`_tools/snapshots/video.after-polish.json`, 94 scenes, 144 lines) against the source lines, with the reports of three report-only lenses (numbers, availability, names) and a completeness critic as leads. Each proposal was re-read against the source file before it was applied or rejected.

Helper files are in `<VIDEO_WORKDIR>/openai-devday-2026-recap/_tools/verify/round3/`: `dump.mjs` and `dump.txt` (every scene's data and lines), `apply-video.mjs`, `fix-short.mjs` and `apply-claims.mjs` (every edit asserts the text it replaces exactly once), `check-claims.mjs` (claim ids and scene lists of `claims.md` against `video.json`, and quoted narration against the current lines), `measure.mjs` (estimate in seconds, longest picture or card state, the worker's Shorts check), and the three pages fetched on 2026-10-04.

## Pages opened

| key | URL or file | HTTP | How it was read |
| --- | --- | --- | --- |
| R | https://openai.com/zh-Hant/index/devday-2026-recap/ | 200 capture | `sources/devday-2026-recap.zh-Hant.md`, L20–L135 read in full |
| SOL | https://openai.com/zh-Hant/index/introducing-gpt-6-1-sol/ | 200 capture | `sources/introducing-gpt-6-1-sol.zh-Hant.md` L50–L56 |
| DOTS | https://openai.com/zh-Hant/index/introducing-dots/ | 200 capture | `sources/introducing-dots.zh-Hant.md` L21, L27, L60, L69, L76, L81, L94–L98 |
| AG | https://openai.com/zh-Hant/index/introducing-the-agents-api/ | 200 capture | `sources/introducing-the-agents-api.zh-Hant.md` L15, L39, L57 |
| PRO | https://help.openai.com/en/articles/9793128-about-chatgpt-pro-tiers | 200 capture | `sources/help-about-chatgpt-pro-tiers.en.md` L11–L71 read in full |
| SIWC | https://help.openai.com/en/articles/20001410-sign-in-with-chatgpt | 200 capture | `sources/help-sign-in-with-chatgpt.en.md` L11–L51 read in full |
| SPEED | https://learn.chatgpt.com/docs/agent-configuration/speed | 200 capture | `sources/learn-chatgpt-speed-and-cloud.en.md` L10–L30 |
| SPACE | https://chatgpt.com/zh-Hant/features/space/ | 200 capture | `sources/chatgpt-space-and-codex-security-cloud.md` L1–L32 |
| PRICE | https://developers.openai.com/api/docs/pricing | 200 (2026-10-04, identical) | `.txt` L944–L953, L1067–L1070 |
| UF | https://developers.openai.com/api/docs/guides/ultrafast-mode | 200 (2026-10-04, identical) | `.txt` L925–L937 |
| MODEL | https://developers.openai.com/api/docs/models/gpt-6.1-sol | 200 (2026-10-04, identical) | re-fetched and compared only |
| OTHER | `docs/videos/gpt6-vs-opus55-worth-paying/video.json`, `docs/videos/always-on-agent-explained/video.json` | repo files | $348 and $70 at L463, L470; the always-on title at L18; every `video_id` is null |

## What was re-checked after the polish

| # | what | where | source | verdict |
| --- | --- | --- | --- | --- |
| 1 | 25 items = 4+7+4+7+3, and the channel's split 9+1+6+5+4 uses every item once | title, ticket-hand, nine-stats, tally-stats, outro, Short 1 | R L26–L135 | CONFIRMED |
| 2 | 6 items say 「適用於所有方案」; 3 say all Codex users / all other plans / signed-in users | nine-stats, pool-desk, kickboards | R L48, L52, L56, L60, L79, L83, L91, L121, L127 | CONFIRMED |
| 3 | Codex 雲端 is written two ways in one paragraph | pool-door `hcvv`, codex-four note | R L47–L48 | CONFIRMED |
| 4 | Sign-in: five steps, six first partners, three identity fields, three things not shared, subscription sharing separate and limitable, global admins | login-steps, three-vs, key-board, lane-rope, office-bolt, walk-past | SIWC L16, L21–L25, L27–L28, L31–L36, L44, L48 | CONFIRMED |
| 5 | GPT-6.1 Sol: Plus to Edu, in ChatGPT 工作 and Codex, not in 對話 | bike-talk `6q7d` + `n5cz`, sol-big | SOL L53; R L33 | CONFIRMED |
| 6 | GPT-5.5 retires 2026-10-14 from ChatGPT, ChatGPT Work and Codex; API not affected | retire-stats, week-steps | SPEED (Retirement section) | CONFIRMED |
| 7 | Pro list: dots markets, 空間 web and desktop, 動態頁面, 協作投影片 export, meeting plugin Beta for Pro and Business | pro-five and its five lines | R L29, L97, L101, L104–L105, L116–L117; SPACE L10, L18, L23, L30–L31; DOTS L27, L94 | CONFIRMED |
| 8 | dot chats not counted, tasks counted; first dot included; three boundaries | dot-big, look-only, locked-cabinet | DOTS L69, L76, L81, L96, L98 | CONFIRMED |
| 9 | Pro 100 / 200 / 500 = $100 / $200 / $500; Ultrafast only on Pro 500 among Pro plans; credits do not unlock it at launch | pro-table `am8b`, `j86r`, `apbg` | PRO L21–L25, L49–L50 | CONFIRMED |
| 10 | 「中文頁叫極速」 (added by the polish, had no claim) | pro-table `j86r` | R L35–L37 (heading 「### 極速」) | CONFIRMED; evidence added to c32 |
| 11 | Pro 200 grandfathering: 2026-09-22 to 10 a.m. PT 2026-09-29, old allowance to 2026-10-29, still $200, no Ultrafast | pro200-steps | PRO L37–L38, L41, L44 | CONFIRMED |
| 12 | Allowance rates 1 / 2.5 / 8; 10 × 8 = 80; credits ×6 (Fast ×2) | rate-stats, speed-vs-money | PRO L66; SPEED Fast and Ultrafast sections | CONFIRMED |
| 13 | Team list: tasks, @ChatGPT without a licence, workstations, private intelligence per API project, marketplace Beta, 32 first partners | team-five, own-knife, bell-tray, blank-board, clean-counter, back-door, crates-count, pass-window | R L41, L86–L87, L108–L109, L112–L113, L134–L135 | CONFIRMED |
| 14 | Data residency +10% for eligible models released on or after 2026-03-05; Enterprise Ultrafast off by default; no Ultrafast with non-US inference residency | company-two, roped-room | PRICE L1069; SPEED Ultrafast and Availability sections | CONFIRMED |
| 15 | Ultrafast price table: every cell ×6; $10→$60, $1→$6, $50→$300; long context $120 / $12 / $450; only gpt-6-astra listed | price-board, uf-stats | PRICE L913, L946–L949 | CONFIRMED |
| 16 | Speed: Codex up to 8x and 300 tokens/s; API 6x on the recap and up to 8x in the guide | scooter, two-ladles, speed-vs-money | R L36; UF L927 | CONFIRMED |
| 17 | Astra about $348, the GPT-6 Sol of that video about $70 | scale-hands, two-bags, coins-count | the other video's job2-table | CONFIRMED (the channel's own estimate) |
| 18 | Astra Ultrafast open to all API users at low rate limits | api-three item 1, `h6xm` | UF L930, L934–L936 | CHANGED: the bullet had lost the model name |
| 19 | Agents API: hosted by OpenAI, no extra charge, public beta; computer use on the API and for Pro 500 and eligible Enterprise | hand-over, api-three, helper-woks | AG L15, L39, L57; R L67–L68 | CONFIRMED; 「公開測試版」 added to the card note |
| 20 | Decisions API limited preview; Bedrock Managed Agents for teams on AWS; MCP events a proposed spec | balloon-stall, dev-three | R L63–L64, L72, L90–L91 | CONFIRMED |
| 21 | 「還不能碰的」 six items | pencil-pass, not-yet | R L37, L64, L97, L117, L121; SPACE L10, L18, L23; DOTS L60 | CHANGED: slides co-editing lost its attribution |
| 22 | The five lists are the recap page's own grouping | ticket-hand `2bjg` | R L25, L44, L75, L93, L123 | CHANGED: the page has five other groups |
| 23 | always-on-agent-explained is 「上一支」 | wheel-alone `a8fd`, description | repo only | NOT FOUND: scoped to 「之前講過」 |
| 24 | Short 1 and Short 2, every sentence | `shorts.json` | same lines as the long script | CONFIRMED; Short 1 now says the full model name once |

## Changes

Fact and attribution changes:

| # | where | before → after | source |
| --- | --- | --- | --- |
| F1 | `video.json` scenes[api-three].data.items[0] | 「**Ultrafast**：所有 API 使用者」 → 「**Astra 極速**：所有 API 使用者」 | UF L930, L934–L936 (broadly available for GPT-6 Astra, preview only for GPT-5.6 Sol); R L37 「GPT‑6 Astra 極速版即日起在 API 推出」. The proposed 「**Astra Ultrafast**：所有 API 使用者」 is 26 characters, over the 20 a bullet may have, so the bullet uses the recap's Chinese name, which `j86r` introduces aloud. 19 characters |
| F2 | `video.json` scenes[not-yet].data.items[1] | 「**空間行動版編輯、投影片多人協作**」 → 「**空間行動版編輯、投影片多人協作**：空間頁」 | SPACE L10, L18, L23 say 即將推出; R L104–L105 gives multi-person editing to Pro, Business and Enterprise. The proposed 「：空間頁寫即將推出」 is 25 characters; this is 19 |
| F3 | `video.json` scenes[not-yet].data.note | 「…Sol 頁寫一併推出」 → 「…Sol 頁寫一併推出；投影片多人編輯，回顧頁寫 Pro、Business、Enterprise 適用」 | R L104–L105 |
| F4 | `video.json` line `2bjg` | 「回顧頁 25 項，分五張清單，像五個售票口：所有人、Plus、Pro、團隊、開發者。」 → 「回顧頁 25 項，我分五張清單，五個售票口：所有人、Plus、Pro、團隊、開發者。」 | R L25, L44, L75, L93, L123: the page's five groups are not these five. 29 spoken units before and after |
| F5 | `video.json` line `a8fd` | 「AI 代理怎麼運作和失敗，上一支講過；這裡只講 dots 的額度和界線。」 → 「AI 代理怎麼運作和失敗，之前講過；這裡只講 dots 的額度和界線。」 | Nothing in the repo shows always-on-agent-explained is the upload right before this one. 28 → 27 spoken units |
| F6 | `video.json` youtube.description | 「影片裡提到的上一支、另一支：」 → 「影片裡提到的前幾支：」 | dependant of F5 |

Other changes:

| # | where | before → after | why |
| --- | --- | --- | --- |
| O1 | `video.json` line `8vrs` | 「Plus 的清單，九項加一個 Sol。」 → 「Plus 的清單，九項加 Sol。」 | The estimate was 720.13 s, over the 12-minute ceiling, and lint printed a second warning. Now 719.40 s |
| O2 | `video.json` scenes[api-three].data.note | 「Agents API 只付 token 與工具」 → 「Agents API 是公開測試版，只付 token 與工具」 | AG L15, L57: a public beta; no string of the script said so |
| O3 | `shorts.json` [0].scenes[2].narration[0] | 「官網沒限定付費方案的有 9 項，Plus 再加 Sol 一項。」 → 「官網沒限定付費方案的有 9 項，Plus 再加 GPT-6.1 Sol。」 | SOL L53: the claim is sourced for GPT-6.1 Sol only, and Short 1 never said the full name. The proposal put the name in narration[1], which made that phrase 43 characters and failed the worker's check (38 at most); narration[1] is unchanged |
| O4 | `shorts.json` [0].description | 「Plus 再加 Sol，Pro、團隊…」 → 「Plus 再加 GPT-6.1 Sol，Pro、團隊…」 | same |
| O5 | `claims.md` | scene lists equal `video.json` (61 ids, 0 mismatches); the quoted narration and card text of 44 entries moved to the current wording; c32 gains the evidence for 「中文頁叫極速」 and the recap URL; c56 gains R L37 and the recap URL; c1, c24, c28, c53, c55 record this round's changes; the three closing sections describe the 94-scene script | the entries still quoted the round-2 sentences |

Nothing else was touched: no scene, order, line id, reveal, shot prompt, camera or `pause_after_ms`; `sources[]` needed no change (the recap, the Ultrafast guide and the Agents API page were already listed, all checked_on 2026-10-03); `brief.md` was not edited; the pronunciation dictionary was not edited (no new Latin term).

## Rejected proposals

| proposal | why it was not applied |
| --- | --- |
| company-two items[1] 「Enterprise 極速：**預設關**」 → 「Enterprise 的 Ultrafast：**預設關**」 | The fact is confirmed either way (SPEED: off by default for Enterprise workspaces). The replacement is 26 characters against a limit of 20, and no shorter wording keeps both 「Enterprise」 and 「Ultrafast」. 「極速」 is the recap's own Chinese name (R L35) and `j86r` says 「中文頁叫極速」 before this card |
| dev-three items[1] 「**Bedrock**：給 AWS 上的團隊」 → 「**Bedrock Managed Agents**：給 AWS 上的團隊」 | 33 characters against 20; the name alone is 22. The full name 「Amazon Bedrock Managed Agents」 is in the same card's note |
| api-three items[0] as 「**Astra Ultrafast**：所有 API 使用者」 | applied in substance as F1, with 「極速」 because of the 20-character limit |
| not-yet items[1] with 「：空間頁寫即將推出」 | applied in substance as F2 and F3, shortened to fit |
| Short 1 scenes[2].narration[1] with 「GPT-6.1 Sol 在…」 | applied in substance as O3 on the sentence before, because of the 38-character phrase limit |
| company-two items[0] 「資料駐留端點：3/5 起的新模型**加價 10%**」 (optional) | The scope is in the same card's note and in `emau`; the card as a whole is true |

## Facts that expire soon

- GPT-5.5 leaves ChatGPT, ChatGPT 工作 and Codex on 2026-10-14 (SPEED): the Plus step of week-steps and the retire-stats card are stale after that day.
- Pro 200 old allowance ends 2026-10-29 (PRO L37); dots' higher first-month limit ends about 2026-10-29 (DOTS L96).
- Decisions API: 「今日起限量開放預覽，預計未來幾天內全面推出」 was written on 2026-09-29 (R L64). If it is generally available at upload, `hh5s`, dev-three items[0], not-yet items[3] and `j8m9` are wrong.
- GPT-6.1 Sol Ultrafast: the recap says 即將推出, the Sol page says 一併推出, and the Ultrafast price table lists only gpt-6-astra on 2026-10-04.
- 「即將推出」 items that can flip any day: 空間 mobile editing, slides collaboration, the meeting plugin for Enterprise, dots SMS, profiles for Enterprise, Edu and Healthcare.
- Both help-center pages show only "Updated: yesterday" and may change again; 「首批 32 家」 and the six sign-in partners are launch lists.

## Summary

- Strings re-checked: the whole polished script (94 scenes, 144 lines, 32 cards, title, description, tags, thumbnail) and both Shorts, in 24 groups above. Confirmed: 20 groups. Changed: 3 (F1, F2 with F3, F4). Not found: 1 (F5 with F6, scoped without a number).
- Fact and attribution changes: 6 strings in 4 places. Other changes: 5.
- Opinion check: no opinion was added or changed; `2bjg` now says the split is the channel's (「我分」).
- Listener pass: no line over 40 spoken units, no verification narration, no parentheses or URLs in narration, no new Latin term.
- Lint after the edits: 0 errors, 1 warning (the opening chapter runs about 38 s). Estimate 719.40 s = 11.99 minutes, 144 lines, 2,505 spoken units; the longest picture or card state is 8.00 s; the worker's Shorts check returns no problem.
- Suspected, not changed: the two rejected card names above; not-yet 「Sol Ultrafast」 without 「GPT-6.1」 (27 characters with it); `bdwn` without the time zone (2026-09-30 01:00 in Taipei); ch5 `d4k8` broader than private intelligence and the marketplace; the description's 「五分之一」 without 「標準輸入與輸出」; five-more 「三種方案即將推出」 reads alone as if the whole item were coming soon; Decisions API under 「官網寫即將推出」 though the page's words are 「預計未來幾天內全面推出」. All are listed in `claims.md` under 「我懷疑但沒動的事」.
- For the owner: (1) is always-on-agent-explained really the last long video published before this one? If so `a8fd` can go back to 「上一支」; the brief calls two different videos 「上一支」. (2) Two cards say 「極速」 where the narration says 「Ultrafast」 because the bullet limit is 20 characters; decide whether the limit or the single name wins. (3) Open the recap page again on upload day for Decisions API and for the GPT-5.5 date. (4) The three videos the description points at still have `video_id` null in the repo.
- A fourth round under the "more than three fact changes" rule: the four places changed here are one restored model name, one restored attribution, one ownership word and one scoped reference; no number, price, date or plan changed. The call is the owner's or the coordinator's.

## After the confirm round

A drift critic read the round-3 strings against the narration around them and found that F2 and F3 reached the card but not the sentence spoken before it.

| # | where | before → after | source |
| --- | --- | --- | --- |
| C1 | `video.json` line `j39w` (scene pencil-pass) | 「還有幾項，官網寫即將推出，今天還碰不到。」 → 「還有幾項，官網寫即將推出。」 | R L104–L105 gives 「邀請多位團隊成員同時直接編輯簡報」 to Pro, Business and Enterprise today; only SPACE L10, L18 say 即將推出. 「今天還碰不到」 was wider than the sources and contradicted the not-yet note, the pro-five note and the description's 「以官網為準」. 「官網寫即將推出」 stays true for all six items. 17 → 11 spoken units |
| C2 | `claims.md` c24 | the quoted previous sentence 「還有幾項，官網寫即將推出，今天還碰不到」 → 「還有幾項，官網寫即將推出」, with a note that the confirm round dropped 「今天還碰不到」 because R L104–L105 lists multi-person editing as available | dependant of C1 |
| C3 | `shorts.json` [0].scenes[1].narration[1] (Short 1, shot ticket-hand) | 「回顧頁的 25 項，照方案分成五張清單。」 → 「回顧頁的 25 項，我照方案分成五張清單。」 | dependant of F4, applied after the confirm round (A1 in the last section): R L25, L44, L75, L93, L123, the page's five groups are not the by-plan five, and no other string of Short 1 said the split is the channel's. 20 characters, under the worker's 38-character phrase limit |

Nothing else was touched: no line id, scene, order, shot prompt, camera or `pause_after_ms`; `shorts.json`, `sources[]`, `brief.md` and the pronunciation dictionary are unchanged. The no-claims paragraph and the doubts bullet of `claims.md` quote only 「官網寫即將推出」 and needed no change.

Lint after the edit: 0 errors, 1 warning (the opening chapter runs about 38 s). Estimate 717.97 s = 11.97 minutes, 144 lines, 2,499 spoken units; the longest picture or card state is 8.00 s; the worker's Shorts check returns no problem. The figures in the Summary above (719.40 s, 2,505 units) are the state before this edit.

## After the confirm round: the second drift pass

A second drift pass found two things the confirm round left behind; a fixer applied both. `video.json` was not touched.

| # | where | before → after | why |
| --- | --- | --- | --- |
| A1 | `shorts.json` [0].scenes[1].narration[1] (Short 1, shot ticket-hand) | 「回顧頁的 25 項，照方案分成五張清單。」 → 「回顧頁的 25 項，我照方案分成五張清單。」 | F4 did not reach its Shorts dependant: the sentence had no agent and read as if the recap page split its items by plan (R L25, L44, L75, L93, L123 are five other groups). Listed as C3 in the table above. 20 characters |
| A2 | `claims.md` c1 | records the Short 1 sentence beside `2bjg` | dependant of A1 |
| A3 | `claims.md` 「與企劃不同的地方」, 張數與長度 | 「lint 估 11.99 分鐘（719.4 秒，…）、2,505 個口播單位」 → 「lint 估 11.97 分鐘（717.97 秒，…）、2,499 個口播單位」 | the line gave the state before C1 as the current state |
| A4 | `claims.md` 進度, 查核第三輪 | 「估 11.99 分鐘（719.4 秒）、2,505 個口播單位」 → 「估 11.97 分鐘（717.97 秒）、2,499 個口播單位」; two new sub-bullets: 確認輪 (the `j39w` change, C1) and 確認輪之後 (A1) | the entry never mentioned C1 and its counts were stale |

Lint after these edits: 0 errors, 1 warning (the opening chapter runs about 38 s). Estimate 717.97 s = 11.97 minutes (lint prints the rounded 「12.0 min」), 144 lines, 2,499 spoken units, 94 scenes; the longest picture or card state is 8.00 s; `episodeShortsProblems` returns no problem for both Shorts. Short 1's second title 「…照方案分五張清單」 names no one as the splitter and was left as it is.
