---
id: 2026-09-28-video-story-pilot
title: 試作兩支品牌故事並記錄數字
status: blocked
priority: P1
area: docs
owner: codex-8a78-pilot
claimed_at: 2026-10-14T16:31:34Z
created_at: 2026-09-28T03:31:15Z
completed_at:
branch: codex/brand-stories-five-20261014
depends_on:
  - 2026-09-28-video-story-worker
  - 2026-09-28-video-story-backlog
  - 2026-09-28-video-story-api-policy-languages
  - 2026-10-14-enforce-usd-25-all-in-cap
scope:
  - docs/videos/STORY.md
  - docs/videos/brand-stories-pilot-v2-20261015
  - tasks/open/2026-09-28-video-story-pilot.md
---

# 試作兩支品牌故事並記錄數字

## Why

`docs/videos/STORY.md` 裡的時間、張數、花費都是從程式常數估的，沒有量過。每天兩支之前要先知道：一支實際要多久、花多少、1K 的圖放大到 1080p 夠不夠清楚、訂閱帳號撐不撐得住、自動關卡會不會卡住。

## Definition of done

- [ ] 兩支試作（A01 輪子行李箱、B18 迴轉壽司）在正式主機上從清單開始做到「可以上架」，站主看過成片。
- [ ] `docs/videos/STORY.md` §試作紀錄 填了：每支的長度、鏡數、圖片張數與重做率、各階段秒數、帳本花費、訂閱帳號的 token 用量、`final.mp4` 的大小。
- [ ] MiniMax 可愛插畫放到 1080p 成片的清晰度有結論；需要提高圖像規格時，附成本差額交站主決定。
- [ ] 卡住的地方都開了票或當場修掉；`STORY.md` 的上限表依量到的數字更新。

## Steps

- [ ] 站主先做 `STORY.md` §站主要先做的事 列的幾件事：開「AI 漫劇」、寫頻道立場、勾選字幕語系、看一遍各階段的常設指示、確認帳號的權限。
- [ ] 部署（要站主同意，走 skill `deploy`）。
- [ ] 調上限：每月圖片與 judge 次數、作品每月集數、同時進行數、旁白每月字數、Jev 每日次數、審核單檔大小。
- [ ] [獨立 A01／B18 新版包](../../docs/videos/brand-stories-pilot-v2-20261015/README.md)先完成新內容的來源覆核與 hash 綁定審稿，再編譯兩集匯入檔；正式機先唯讀核對兩個 `-v2` slug、系列、工作目錄與鎖，之後才對**此兩集檔**試跑與評估套用。不拿舊 100 題檔 `--limit 2` 匯入。
- [ ] 確認主機 nginx 的 `client_max_body_size` 放得過實際新版兩集匯入檔；舊 100 題檔約 1.2 MB 的估算不代表新版大小。
- [ ] 看工人日誌與後台，兩支做完後記錄數字。

## How to verify

成片用 ffprobe 確認 1920×1080、30 fps；新版旁白正文由 TTS 量得約 10 分鐘，依 worker 的 9–11 分鐘驗收帶，不拿片頭／片尾湊正文；再量 5 秒片頭與 21 秒片尾的完整成片。`review/qa.json` 全過；正文全為 `visual: "still"` 的插畫／卡片並用緩慢運鏡，沒有付費生成 clip；帳本含文字、音訊、圖像、judge、必要配樂與重試，每支總額在 US$25 以內，站主看過成片。

## Notes

- 前幾支成片請站主親自看過，再開「自動品管全過就核准成片」給故事用。
- 任何對正式站的操作都要站主同意；這張票不是授權。
- 做各張票時留下、試作要觀察的事（2026-09-28）：
  - 舊稿的語速估算曾以每分鐘 250 字計，實測約 300 字；新版 10 分鐘稿須量 TTS 實際秒數，必要時調整各章，不能沿用舊 3,250 字／13 分鐘目標。
  - 新版畫風固定 MiniMax `image-01`、精確 `{"preset":"cute-mystery"}`；看聯絡表及整片檢查是否漂移，不另加自訂 `style`／`negative` 或未核定的風格錨定圖。
  - 旁白長度修兩輪仍不合格時影片會卡住，沒有「接受這個長度」的選項。試作遇到就記下來，決定要不要加。
  - 每支花費以伺服器帳本為準。工人日誌的估計值在票 `2026-09-28-video-story-image-model-pricing` 做完之前用的是設定分頁的模型單價，會偏高。
  - 被放棄的故事目前不能重做（票 `2026-09-28-video-story-redo-dropped`）。試作的兩支如果做壞了，先不要按放棄，留著讓人看原因；放棄之後那個故事就不能再做。

### 2026-09-29 看板盤點與站主決定

站主回覆「依賴就緒後準備試作／上傳驗收方案」。目前依賴與可執行步驟見docs/work-status-2026-09-29-video-acceptance-plan.md；未部署、生成、登入或上傳。

本次僅追加交接證據，不改既有owner、scope、branch或執行狀態。

### 2026-09-29 dependency-ready follow-up

PR #933 merged at 02:49:56 UTC as 157cca889a169ebf9f0af4f609be69388b8f6d2e;
PR #938 is also merged. In response to the owner's conditional request, a concrete
A01/B18 preparation plan is recorded in docs/work-status-2026-09-29-story-pilot-plan.md.
No production preflight, deployment, setting change, job import or paid generation was
performed. This pilot task and its media/owner acceptance remain open; code dependency
completion does not satisfy those checks.

Concrete pre-generation gates discovered during plan preparation:

- The worker accepts narration at 690–930 seconds; the original final-media
  acceptance remains 720–900 seconds and must be measured on the actual cut.
- `drama.max_usd_per_video` covers media estimates; TTS/text costs and judge
  calls are not fully bounded by it. Reconcile all ledgers/provider receipts and
  validate worst-case reserves before paid work. The original total of at most
  US$25 per finished video remains binding; stop at dry-run if it cannot be bounded.
- Use `drama.drama_auto_approve_final=false` for owner viewing. Caption locales
  are en/ja/ko/zh-CN, with zh-TW automatically included; a replay can legitimately
  report started/leave_alone without creating another A01.

### 2026-10-15 owner order and read-only preflight

The owner explicitly chose A01/B18 first, then the five new MiniMax/10-minute brand stories. The original Gemini/13-minute A01/B18 source rows and reviews still hash-match and validate **as historical material**. The pilot now uses isolated `story-rolling-suitcase-v2` and `story-conveyor-belt-sushi-v2` source rows with MiniMax/10-minute specifications, while keeping the US$25 **all-in** cost cap per film. Neither new treatment may use the old review hash as its approval. In this checkout, neither the old `docs/videos/story-rolling-suitcase/video.json` nor `docs/videos/story-conveyor-belt-sushi/video.json`, nor their default local media workdirs, exists; that says nothing about the host or the new `-v2` slugs. The current 100-story compiled file is 1,415,413 bytes, SHA-256 `c8fb18102634459c62f556022139e0bdc733ef432321c412ff810faed0ac0194`, so the 2026-09-29 import-file SHA in the old plan is stale even though the original A01/B18 source files are unchanged.

Production **UI observation only** on 2026-10-15 (`/zh-TW/admin/videos?tab=drama`): AI drama is shown enabled and the `kind=story` list showed no cards, but this is not a full database/media/slug reconciliation. The settings UI showed `drama_auto_approve_final=true`, generic `max_usd_per_video=US$200`, concurrent episodes=1, monthly starts=30, image and judge monthly maxima=20,000 each, music=60, clip seconds=3,000, channel voice enabled, and en/ja/ko language pre-checks false. Generic image model was MiniMax `image-01`; the original A01/B18 series specifies Gemini, so actual per-series routing remains unverified. Provider balances and account availability remain unknown.

The deployments UI showed no live release SHA/CI history. A single read-only host preflight through the saved PuTTY `hostinger2` session returned exit 1, `Cannot answer interactive prompts in batch mode`; no retry or alternate connection was attempted. Therefore live Git/image SHA, hold/locks, exact A01/B18 database or media state, balances and ongoing paid jobs are **unknown**. No deploy, settings change, import, paid generation, upload or owner playback occurred. Before any apply/spend, obtain the approved host readback, disable automatic final approval for human viewing, reconcile media and non-media cost reserves to the US$25 all-in cap, then run `video-story-import --series brand-stories --limit 2 --episodes-per-day 1` without `--apply` against the current SHA and inspect its create/update/leave-along/refused/problems output. A01 owner playback and ledger precede B18 production.

The owner chose the authorized admin UI for further readback. On retry, the formerly logged-in Chrome browser reported `Browser is not available: chrome`; opening the in-app browser to the same admin page timed out before its webview attached. These are browser-tool availability failures, not proof of an empty live database. No SSH fallback, cookie/API workaround, settings edit or paid call followed. The next agent can resume at `/zh-TW/admin/videos?tab=drama&series=brand-stories` when the authorized browser is available, open the exact A01/B18 episodes, and reconcile their persisted states. The UI has not shown provider cash balance or a release SHA, so those remain separate preflight needs.

### 2026-10-15 authorized admin UI retry

The owner selected the already authorized admin UI as the next read-only entry. A newly opened, logged-in Chrome admin tab showed `環境 PRODUCTION`. The brand-story list rendered the import form without a work card, and the exact `/zh-TW/admin/videos?tab=drama&series=brand-stories` page returned `作品讀不到 / 找不到這部作品`. This is a current UI response for that series slug, not a direct database or host-media inventory; an orphan or differently named work is not excluded. No A01/B18 project was opened or started.

The deployments UI showed `尚無 → 尚無`, `尚未取得最新 main commit 摘要`, CI `unknown`, no deployment history, and deployment disabled on this UI, so it did not establish the live release SHA. The AI provider UI showed MiniMax and Gemini keys configured, but its last connection test was 2026-09-28 13:31 and it showed no provider credit balance. The browser then became intermittently unattached during further navigation; current drama media settings, Azure voice state, ledger reserves, host holds/locks, and existing media remain unverified. The PR with the new five-story route is still draft and is not deployed. No preflight POST, import, setting change, paid generation, upload, or publication was performed.

The same authenticated browser subsequently read two exact, read-only same-origin admin GET responses: `/api/travel/admin/video-automation/series?kind=story` returned `{"series":[]}`; `/api/travel/admin/deployments/overview` returned `enabled:false`, `agent_connected:false`, `deployed_sha:null`, `target_sha:null`, `ci_status:"unknown"`, and no active or last-success run. The former establishes that the registered story-series list was empty in the reached database at read time; the latter confirms the deployment UI cannot establish a release SHA. Direct admin video-detail GETs for `story-rolling-suitcase` (A01) and `story-conveyor-belt-sushi` (B18) each returned nginx `502 Bad Gateway`, which is not a missing-video verdict. Independent admin browse GETs with `q=` set to each exact slug returned `{"items":[],"total":0}` for both; the current admin index thus has no matching A01/B18 video-project rows. None of these queries inventories host media files or proves no unregistered worker work exists. The admin GETs do not disclose vendor credit balances or worker-code SHA. No mutations were made.

`GET /api/travel/admin/video-automation/settings` returned `enabled:true`, global voice Gemini `Sulafat`, global caption locales `en/ja/ko`, and drama image defaults MiniMax `image-01`. The current drama settings still have `drama_auto_approve_final:true`, `max_usd_per_video:200`, `series_max_in_flight:1`, monthly starts 30, and image/judge monthly ceilings 20,000 each. These are settings values, not an all-in US$25 cost reservation or the original A01/B18 series row's actual model route. Before import, turn off automatic final approval for owner viewing, resolve the caption choice, prove live release/worker version and bounded spend, and then rerun the exact cohort dry-run. No setting was changed.

Read-only cost-path audit on 2026-10-15 confirmed that media estimates, text tokens, speech characters, transcription and Jev calls do not share a durable per-film USD reservation. The [pilot budget gate](2026-10-14-enforce-usd-25-all-in-cap.md) is now an explicit prerequisite; the production setting of USD 200 cannot prove the USD 25 all-in limit. No paid pilot was started.

### 2026-10-15 pilot source spot check

The sandboxed source fetch failed for all 16 A01/B18 URLs, so it gave no verdict about the sources. A separate read-only web check reached these primary pages and rechecked the central timeline: [Sadow's patent](https://patents.google.com/patent/US3653474A/en) shows the 1970-02-16 filing, 1972-04-04 publication, earlier rolling-luggage citation and large-terminal problem; [NASA's Apollo 11 page](https://www.nasa.gov/mission/apollo-11/) places the lunar landing on 1969-07-20; [Travelpro's company history](https://travelpro.com/pages/our-history) and [rolling-luggage history](https://travelpro.com/blogs/the-travelpro-blog/the-history-of-rolling-luggage) support Plath's 1987 upright two-wheel design and the 1989/1991 business milestones. For B18, [the Japan Society of Mechanical Engineers](https://www.jsme.or.jp/kikaiisan/heritage_112_jp.html) places the first Genroku conveyor-sushi shop in Fuse in April 1958 and describes the beer-factory inspiration and preserved conveyor; [the Japan Institute of Invention and Innovation](https://koueki.jiii.or.jp/innovation100/innovation_detail.php?eid=00026&age=high-growth&page=keii) supports the staffing problem, fan-shaped turn, 1962 utility-model registration and 1978 expiry. These six page readbacks are a source spot check, not a complete 16-URL fetch, independent review of a final script, or permission to import or generate media.

### 2026-10-15 authorized PuTTY host readback

The owner directed a check of saved PuTTY sessions. The `hostinger` session reached a machine without `/root/travel_scanner`, so it was not used as evidence for this deployment. The `hostinger2` session succeeded when the known root login was specified explicitly. A single read-only preflight on `hostinger2` at 2026-10-15 00:01 UTC found `/root/travel_scanner` clean at `c4911a0598944b9a4409584b3fa6a069f4d8a70a` (same as its `origin/main`), no deploy hold, a free deploy lock, no recently incomplete release directory, and the last deploy log reporting that SHA at 2026-10-14 23:58 UTC. API and both video workers were up; Alembic reported `0131_video_dub_retries (head)`. The host reported six globally `uncertain` video stage jobs and one globally `queued` media job; those counts have no demonstrated A01/B18 relationship. Provider credit balances and exact image contents remain unverified.

At 2026-10-15 00:03 UTC, exact read-only PostgreSQL queries on the same host returned **zero `kind=story` series**, zero A01/B18 episode or drama-request rows, zero exact `video_projects` rows, and zero exact media-job rows. The video-worker volume had neither `story-rolling-suitcase` nor `story-conveyor-belt-sushi` work directory. These query and directory results supersede the earlier admin UI uncertainty for the exact slugs, but do not rule out differently named or unregistered work. No import, setting change, paid call, deployment or upload occurred. The live SHA is main's current release, not this draft PR's code. The USD 25 all-in gate remains blocked on active audio-file scopes, and the live setting still auto-approves final cuts; preserve the owner-viewing gate before any paid pilot.

### 2026-10-15 container and internal-usage readback

Using the same authorized PuTTY session, a read-only container check matched the production host's `c4911a059` source bytes: API and `video-ai-worker` `series.py` SHA-256 `cb9d3e01465a6f072d44fdcedae659f538686a634a03351171f8f67d8bfaa155`, API `stories.py` `a79e09e37fa42143d345bfd64fc07a7b601a424def9d1fb8f30a8dd5207fa610`, and `video-worker` `story.mjs` `5fec3daefd27e1dd0d54a3fe0d2935bf8ef1ea1b8c14e2776110aabf653e37e8`. API and AI worker share image ID `sha256:6f80dfb28df9916b57db62dfe7ad01c3653992a7b66a1c5f0a3d730407c5a02a`; video-worker uses `sha256:19b55fff62da360cd8bc08ab9326477c4af50c31a054b9b6d9b0cecc772eed0c`. All started at 2026-10-14 23:58 UTC. This verifies those running code files, not the entire image or the draft PR's deployment.

Read-only PostgreSQL `SELECT` and Redis `HGET` (no provider request) showed `drama_enabled=true`, global `minimax/image-01`, monthly image and judge limits of 20,000 each, and media estimate cap US$200 per video. Raw `2026-10` app counters: `video-media-images=9767`, `video-media-judge-calls=10642`, `azure_speech=40`, `gemini_speech=883936`. These are internal counts and limits, not a MiniMax wallet balance, a Gemini/Azure external quota, or a USD 25 all-in reservation. The repository has no supported zero-cost MiniMax balance reader. Do not spend for a balance probe. No production mutation, import or paid call occurred.

### 2026-10-15 revised pilot source

The owner's MiniMax/approximately 10-minute decision applies to A01/B18 as well as the following five films. The original 100-bank and its A01/B18 reviews remain historical and unchanged. A separate [two-film v2 source package](../../docs/videos/brand-stories-pilot-v2-20261015/README.md) now has new episode slugs, six-beat story arcs, cold opens, existing v4 intro/outro timing, still illustrations only, and a builder that refuses to emit an import file until **new independent hash-bound reviews** exist. Those new reviews, an exact host readback for both `-v2` slugs, all-in budget release, vendor balance evidence, script/audio/visual QA and owner viewing remain outstanding. The earlier host readback covered only the original A01/B18 slugs, so it cannot be reused as a collision check for v2. No live import or paid generation has happened.

An independent source readback found corrections needed in both v2 rows. A01 now follows Samsonite's 2011 prospectus rather than the conflicting 2004 claim: Ultra Transporter in 1997 and four-wheel Spinners in 2000; ABC's 2010 interview attributes immediate 1970 customer acceptance to Sadow, while his patent's airport-terminal problem is not treated as independent sales causation. The 1928 trip proves Anita Willets-Burnham had the wheeled case by departure, not its exact making year. B18 distinguishes inspiration at a beer factory from the later turn-design work, says 1962 utility model rather than patent, and keeps Expo exposure, original-chain growth and the 1978 expiry separate. Both rows' cast is now anonymous visual illustration. After these revisions `build.mjs --draft` passes; A01 source hash is `c247eba081af44e183549d26f34bcdd0d9d98c3e9205672641c8a58b9ebd424d`, B18 is `38a03584367c4f890cc149004f5559e5e1376ae4c3471e007d8b3ea0127bba02`. **Both require a new independent review bound to these exact hashes**; no import file has been written.

### 2026-10-15 new-hash review and current preflight

The independent reviewer re-opened the source evidence, confirmed the corrected A01/B18 canonical hashes above, and wrote separate `episodes/reviews/A01.json` and `B18.json` receipts. Both are `pass` on the new hashes. The v2 builder now emits its isolated two-row `stories.json`; Python `check_story_file` returned two stories with zero problems, refusals or ignored rows. These are reviewed story plans, not final narration, shots, media, approval, or an imported production row. Complete narration drafts are being prepared separately; each sentence and actual TTS duration still need their own review.

At 2026-10-15 02:12–02:14 UTC, an authorized PuTTY `hostinger2` read-only preflight still found live `c4911a0` and zero exact old/v2 pilot slug rows in the inspected series, episode, request, project, media, AI-run and stage-job tables. No deploy hold or active deploy lock appeared. The six unrelated uncertain stage jobs and one unrelated queued media job must not be reset. Live settings still had `drama_auto_approve_final=true`, `series_auto_continue=true` and the generic US$200 media estimate cap. The separate per-pilot US$25 code is [draft PR #1508](https://github.com/x812033727/travel_scanner/pull/1508), unmerged and absent from live. The host entrance disclosed no vendor wallet balances or billing receipts. A further batch to inspect workdirs and key-validity booleans was blocked by automatic policy; those facts remain unverified and no alternate command was used. No host write, import, vendor call, paid generation, deployment or upload occurred.

### 2026-10-15 script and visual preproduction

The two isolated scripts in `docs/videos/brand-stories-pilot-v2-20261015/scripts/` now have **independent, hash-bound text fact and narrative PASS** receipts: A01 `f91816021ebea28e1957199a5c73ccc588748e988730efc92e0486d09d5215c6`, B18 `5326bd6633ad69931fe542badd6cddd2378324ff0bcc4b0f05652941642dc724`. Their spoken-body estimates from prior TTS speed are 9:02 and 9:06, respectively; neither voice has been synthesized or timed. Both scripts use a cold-open setup/payoff, the existing 5-second intro after chapter one, a causal six-chapter line, three closing sentences and a 21-second outro cue. Text review does not approve audio, pictures, a final cut or playable end-screen links.

The A01 and B18 `*-shot-plan.md` files are **preproduction estimates**: 95 still illustrations plus 11 cards for A01 (89.6% illustrated), and 91 stills plus 17 cards for B18 (84.3% illustrated); no generated clips. Each includes anonymous one-person neutral-light sample prompts, source-sensitive visual boundaries and an all-in US$25 stop rule. MiniMax's 2026-10-15 official `image-01` list price is US$0.0035 per generated image; judge, TTS and text use their own routes and actual ledger. The A01 plan allocates US$18.45 and leaves US$6.55 unassigned under the US$25 ceiling; B18 allocates all US$25 including contingency. These are planning envelopes, not provider balances, incurred costs or authority to spend. [PR #1508](https://github.com/x812033727/travel_scanner/pull/1508) merged into main as `42fbfb40d` on 2026-10-15; its per-slug shared reservation gate still requires production deployment and live readback before an import can start a paid episode. The first episode can start as soon as an imported series is available. `kind: story` may start B18 whenever its row is `ready` even with `series_auto_continue=false`, so **A01's first import must use the reviewed two-row input with `--limit 1`** and a dry-run whose `stories_imported` is 1 and whose only changed ID is `A01`. After apply, read back that B18's exact slug has no episode row. Set `drama_auto_approve_final=false` so A01's final cut waits for owner viewing; this setting is not a B18 start guard. Only after A01's ledger, playback and owner acceptance may a separate dry-run and authorized `--limit 2` import introduce B18. Provider balances, current host workdirs and live post-deploy schema remain unknown; no production mutation or vendor call occurred at the time of this note.

The reviewed `scripts/A01.md` and `scripts/B18.md` do **not** enter the worker through the compiled `stories.json`. Import transfers six chapter beats; the worker writes its own `story/chapters/*.json`, then merges them into `video.json` and `script.md`. The two independent script PASS receipts bind only the local Markdown. Before paying for TTS or images, the actual chapter files and merged script must be compared against those editorial baselines, independently checked for fact and narrative flow, and bound to their own hashes; shot counts and cost plan must be recalculated if the worker's text differs. Editing only `video.json` is ineffective because the worker rebuilds it from chapter files. The new A01/B18-v2-only worker gate requires an independent hash-bound `story/reviews/script-review.json` on the **actual** chapter and merged output; a missing or stale receipt holds that video before TTS until an explicit admin retry. The receipt format and operator handoff are in the [10-minute story route ticket](2026-10-14-support-10-minute-minimax-cute-brand.md). This is local unmerged code pending CI, not evidence that the reviewed Markdown has been spoken or that the runtime gate is deployed.
