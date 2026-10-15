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
---

# 試作兩支品牌故事並記錄數字

## Why

`docs/videos/STORY.md` 裡的時間、張數、花費都是從程式常數估的，沒有量過。每天兩支之前要先知道：一支實際要多久、花多少、1K 的圖放大到 1080p 夠不夠清楚、訂閱帳號撐不撐得住、自動關卡會不會卡住。

## Definition of done

- [ ] 兩支試作（A01 輪子行李箱、B18 迴轉壽司）在正式主機上從清單開始做到「可以上架」，站主看過成片。
- [ ] `docs/videos/STORY.md` §試作紀錄 填了：每支的長度、鏡數、圖片張數與重做率、各階段秒數、帳本花費、訂閱帳號的 token 用量、`final.mp4` 的大小。
- [ ] 1K 圖片的清晰度有結論：維持 1K，或建議改 2K（附每支成本差額，由站主決定）。
- [ ] 卡住的地方都開了票或當場修掉；`STORY.md` 的上限表依量到的數字更新。

## Steps

- [ ] 站主先做 `STORY.md` §站主要先做的事 列的幾件事：開「AI 漫劇」、寫頻道立場、勾選字幕語系、看一遍各階段的常設指示、確認帳號的權限。
- [ ] 部署（要站主同意，走 skill `deploy`）。
- [ ] 調上限：每月圖片與 judge 次數、作品每月集數、同時進行數、旁白每月字數、Jev 每日次數、審核單檔大小。
- [ ] 匯入清單：先試跑，再套用前兩個（`--apply --limit 2 --episodes-per-day 1`，或後台的匯入表單）。排程的前兩個就是 A01 與 B18。
- [ ] 確認主機 nginx 的 `client_max_body_size` 放得過匯入的請求（約 1.2 MB；repo 的範例是 6 MB，主機上的實際設定沒有查過）。
- [ ] 看工人日誌與後台，兩支做完後記錄數字。

## How to verify

成片用 ffprobe 確認 1920×1080、30 fps、長度 720–900 秒；`review/qa.json` 全過；`checks.json` 的每個鏡頭都是 `motion`；帳本的花費在每支 US$25 以內。

## Notes

- 前幾支成片請站主親自看過，再開「自動品管全過就核准成片」給故事用。
- 任何對正式站的操作都要站主同意；這張票不是授權。
- 做各張票時留下、試作要觀察的事（2026-09-28）：
  - 合成的語速實測約每分鐘 300 字，工具估的是 250 字。13 分鐘的稿子（3,250 字）實際可能只有 11 分鐘左右；量到的長度寫進紀錄，必要時調整每章的字數。
  - 作品的畫風沒有參考圖（`look` 沒有 `style_frames`），90 張圖一致與否只靠提示詞。看聯絡表判斷夠不夠一致；不夠的話要不要加風格錨定圖，另開票。
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

The owner explicitly chose A01/B18 first, then the five new MiniMax/10-minute brand stories. This pilot retains its original Gemini/13-minute format and US$25 **all-in** actual cost cap per film. Local A01/B18 source rows and reviews still hash-match and validate. In this checkout, neither `docs/videos/story-rolling-suitcase/video.json` nor `docs/videos/story-conveyor-belt-sushi/video.json`, nor their default local media workdirs, exists; that says nothing about the host. The current 100-story compiled file is 1,415,413 bytes, SHA-256 `c8fb18102634459c62f556022139e0bdc733ef432321c412ff810faed0ac0194`, so the 2026-09-29 import-file SHA in the old plan is stale even though the original A01/B18 source files are unchanged.

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
