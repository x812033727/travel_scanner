---
id: 2026-09-28-video-shorts-tools-push
title: Video shorts T1: the Shorts tool speaks to the site: server narration, check-audio, qa, package and push
status: open
priority: P1
area: tools
owner:
claimed_at:
created_at: 2026-09-28T03:20:00Z
completed_at:
branch:
depends_on:
  - 2026-09-28-video-shorts-api
scope:
  - tools/video/shorts
  - tools/video/automation/cli.mjs
  - tools/video/automation/client.mjs
  - tools/video/automation/automation.test.mjs
  - .github/workflows/video-tooling.yml
---

# Video shorts T1: the Shorts tool speaks to the site: server narration, check-audio, qa, package and push

## Why

`tools/video/shorts`（PR #871）是一支獨立的本機指令：不發任何網路請求、旁白只能用 Windows 的本機語音合成、沒有旁白檢查、沒有品管報告、沒有 `metadata.json`，做好的成片只存在這台電腦的工作區。站主要在後台的 Shorts 分頁看片、排程、上架，而且之後要由主機工人（Linux）自己做，所以這支工具要能：用頻道聲音經伺服器合成旁白、檢查旁白、跑自動品管、把上傳包送上站。

設計全文在 `docs/videos/SHORTS.md`（§自動品管、§工具端、§三條內容線）。

## Definition of done

- [ ] 腳本格式第 2 版：多 `line`（`lab`、`cut`、`drama`）、`source`（來源影片與範圍）、`hashtags`（最多 3 個）、`links`；`evidence`、`experiment_summary`、`limitations` 只有 `lab` 必填；`series` 依 `line` 檢查。**第 1 版的三支試片（`docs/videos/ai-shorts/pilots/*.json`）不改一個位元組仍然通過 `validate`**（`core.test.mjs` 綁著它們的雜湊）。
- [ ] 版面：現在所有 Shorts 共用同一個版面（`core.mjs` 的 `sceneHtml`）。三個實測系列與長片精華各有自己的版面（配色的重點色、頁首、字卡的排法），安全區與檢查不變；三支試片用各自系列的版面重做後，聯絡表上一眼分得出是哪個系列。YouTube 的營利政策把「看起來像用模板做的、連看幾支覺得重複」列為不能營利的內容，這是對策之一。
- [ ] `build --speech server|windows|files`：`server` 經 `/api/video/speech` 合成（沿用 `tools/video/tts/client.mjs` 的 `synthesize` 與權杖），聲音與 style 來自站上的 Shorts 設定，沒有設定時用頻道聲音；逐句快取，鍵是聲音加那一句的字；Gemini 回來的 24 kHz 用 `toNarrationRate` 升到 48 kHz。`windows` 是現在的 `speech.ps1`，`files` 是現在的 `--audio-dir`。在 Linux 上預設 `server`。
- [ ] `check-audio --dir <成片目錄>`：每句送 `speech/transcribe`，完全相同的直接過，其餘送 `speech/judge`；寫 `check.json` 與被標的句子；`build --redo` 只重錄被標的句子。
- [ ] `qa --dir <成片目錄>` 寫 `qa.json`：`{ ok, final_sha256, kind: "shorts", line, items }`，項目與順序等於伺服器的 `SHORTS_QA_ITEMS`（12 項，`SHORTS.md` §自動品管）。`profile`、`loudness` 用 ffprobe 與 ffmpeg 從 `final.mp4` 重新量，不讀舊的 `checks.json` 當結論。
- [ ] `package --dir <成片目錄>` 寫 `upload/metadata.json`（`title`、`titles`、`description`、`tags`、`category_id`、`made_for_kids`、`contains_synthetic_media`、`disclosure_reason`、`default_language`、`final_sha256`、`line`、`series`、`source`）與四項上傳包檢查；`manifest.status` 不再寫死 `owner-review-required`，改成反映品管結果。
- [ ] `push --dir <成片目錄>`：`PUT reviews/<slug>`（`format: "shorts"`、`shorts_line`、`shorts_series`、`source_slug`、檢查清單）→ 分段上傳檔案（4 MiB 一段）→ 送 `final` 審核（檔案角色 `preview`＝`final.mp4`、`thumbnail`＝`cover.png`、`contact_sheet`，實測線另有 `evidence_*`；`payload.qa`、`payload.usage`）→ 成片核准後送 `publish` 審核（`metadata`、`final`、`captions_zh-TW`、`description_zh-TW`；`payload.package`）。同一份成片再 `push` 一次是安全的。
- [ ] `import --from <目錄>`：讀一支外來的 Shorts（`final.mp4`、`zh-TW.srt`、`meta.json`），包成同一種成片目錄；之後照常 `check-audio`、`qa`、`package`、`push`。外來的檢查結果一律不採用。
- [ ] 工人敲門：`auto` 每一輪一開始先 `POST /api/video/automation/shorts/tick`，排在「自動產線有沒有開」的檢查之前（教學影片的自動草稿關著時 Shorts 的排程照走）；敲門失敗只記一行，不擋住這一輪。第一期沒有這一步的話，時段不會自己鎖定、成效也不會讀（伺服器的 `tick` 在 Y1）。`shortsStep()` 在第二期的 T2。
- [ ] `video-tooling.yml` 的煙霧測試多一支 Shorts：用程式產生的音檔走 `files` 來源，從腳本做到 `package`，不碰任何服務。
- [ ] `node --test tools/video/shorts/*.test.mjs` 全過；新增的純函式（格式檢查、品管項目、上傳包、送審的 body）都有測試，網路用注入的 `fetch`。

## Steps

- [ ] 先讀 `docs/videos/SHORTS.md`、`docs/videos/ai-shorts/README.md` 與 `review/implementation-review.md`（四個已修的缺陷不要改回去）。
- [ ] 格式第 2 版與相容性測試。
- [ ] 旁白來源抽成三種，加快取。
- [ ] `check-audio`、`qa`、`package`。
- [ ] `push` 與 `import`；送審的 body 對照 A1 的 schema。
- [ ] CI 的煙霧測試。
- [ ] 用三支試片各跑一次 `build --speech server` → `check-audio` → `qa` → `package`（`push` 要等 A1 部署）。

## How to verify

```bash
node --test tools/video/shorts/*.test.mjs
node tools/video/shorts/cli.mjs validate --file docs/videos/ai-shorts/pilots/shorts-receipt-total.json
npm run test:tools
```

`push` 的實機驗證在 `2026-09-28-video-shorts-pilot-launch`。

## Notes

- 共用的核心檔（`tools/video/core`、`tools/video/tts`、`tools/video/review`）只匯入、不修改；缺的函式先在 `tools/video/shorts` 裡包一層。`tools/video/automation` 只加敲門那幾行。
- A1 定下來的送審內容（`apps/api/app/video_shorts/schemas.py` 的 `UsageReport`、`apps/api/app/video_automation/judge.py` 的 `SHORTS_QA_ITEMS`）：`payload.qa` 與 `payload.package` 都要帶 `kind: "shorts"`，`final_sha256` 等於那一筆審核的 `content_sha256`；`payload.usage` 是 `{ narration: { seconds, characters, calls, provider, model }, stages: { <階段>: { calls, input_tokens, output_tokens, provider, model } }, checks: { transcribe, judge, policy } }`。本機語音的 `provider` 寫 `windows`（記 0 元）。
- 聲音與長度範圍讀 `GET /api/video/automation/shorts/settings`。
- 工具每個請求都算在同一個權杖的每分鐘 120 次裡；一支 Shorts 約 14 句，逐句轉寫沒問題，但不要平行送。
- Jev 每天 200 次是全站共用的（新聞、景點、影片）；一支 Shorts 一輪旁白檢查 1 次、政策判斷 1 次。
- 審核的檔案類型沒有 `image/webp`；封面與聯絡表用 PNG 或 JPEG。
- 旁白的花費伺服器算不到單支影片上（`/video/speech` 不收影片代號），所以 `payload.usage` 要帶旁白的秒數、字數與呼叫次數。
