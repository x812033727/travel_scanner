---
id: 2026-09-26-video-hands-off-worker
title: 影片交給 AI 決定：工人套用頻道立場、Jev 挑大綱、送審帶品管結果與完整上傳包
status: done
priority: P1
area: tools
owner: claude-fable-5-1-video-worker
claimed_at: 2026-09-26T23:11:49Z
created_at: 2026-09-26T16:18:42Z
completed_at: 2026-09-26T23:39:11Z
branch: claude/video-hands-off-worker
depends_on:
  - 2026-09-26-video-hands-off-judge
  - 2026-09-26-video-hands-off-qa
scope:
  - tools/video/automation
  - tools/video/review
  - tools/video/package
  - tools/video/core/lint.mjs
  - tools/video/core/lint.test.mjs
  - tools/video/assemble/drama.test.mjs
  - .agents/skills/youtube-video
  - .claude/skills/youtube-video
  - docs/videos/AUTOMATION.md
---

# 影片交給 AI 決定：工人套用頻道立場、Jev 挑大綱、送審帶品管結果與完整上傳包

## Why

伺服器端的規則（judge 票）和 `qa` 指令做好之後，工人與本機工具要真的去用：企劃時套用頻道立場、送審大綱前先請 Jev 挑、送審成片時帶上品管結果、上傳包附上完整檔案（`docs/videos/HANDS-OFF.md`）。

## Definition of done

- [x] 企劃與撰稿的提示詞加上「## 頻道立場」，內容從工具設定讀。
  - `brief.md` 的站主觀點第一行寫「套用立場：N、M」；
  - lint 檢查這一行存在、引用的條號都存在；立場空白時不檢查。
- [x] 送審大綱前，先呼叫 `judge/outline`：
  - `passed`：payload 帶上 `pick` 送審；
  - 沒過：把沒過的原因當成退回意見，交給 `replan`，計入 `MAX_REPLANS`；
  - 端點回 409（沒有開）：照舊送審，等站主；
  - 外部服務失敗：交給 `later`，下一輪再試。
- [x] 本機的 `review-push --gate outline` 走同一條路。
- [x] `review-push --gate final` 先跑 `qa`，payload 帶上 `qa`。自動核准之後，工人照舊 `review-pull`。
- [x] `package` 之後：
  - 跑上傳包的檢查；
  - 「確認上架」的審核附上完整檔案：`final.mp4`、`thumbnail.jpg`、`captions/*.srt`、`description.*.txt`、`metadata.json`；
  - `UPLOAD.md` 只留操作步驟，揭露的答案寫進 `metadata.json`。
- [x] 讀回 `youtube_video_id`，寫進工作區 `video.json` 的 `youtube.video_id`，影片標成完成。
- [x] 更新文件：
  - skill 的 `references/automated.md` 關卡表；
  - `references/prompts/planner.md` 的站主觀點規則；
  - `AUTOMATION.md` 的「關卡」列，連到 HANDS-OFF.md。

## Steps

- [x] 提示詞與 lint。
- [x] 大綱：judge、送審、重寫。
- [x] 成片：`qa`、`review-push`。
- [x] 上傳包：完整檔案、`UPLOAD.md`。
- [x] 讀回影片 id。
- [x] skill 與文件；`.claude/skills` 的逐字複本。

## How to verify

```bash
node --test tools/video/automation/*.test.mjs tools/video/review/*.test.mjs tools/video/package/*.test.mjs tools/video/core/*.test.mjs
npm run test:tools
node tools/video/cli.mjs review-push --slug ai-agent-permissions --gate final   # 主機上，三支第二批成片補上品管結果
```

## Notes

- 工人的權杖本來就能送審，這張沒有擴大它能做的事。
- 上傳包裡的 mp4 約 90–100 MB，用既有的分段上傳送。
- 2026-09-27 claude-fable-5-1-video-worker 做完（分支 `claude/video-hands-off-worker`，從 `origin/main` 併入 qa 票的分支）。judge 票當時還沒 done，claim 用了 `--force`。`tools/video/core/lint.test.mjs` 加進 scope：`stanceProblems` 的單元測試放在它旁邊；`tools/video/assemble/drama.test.mjs` 也加進 scope：它斷言 `UPLOAD.md` 舊的自我檢查文字，改成新的揭露那一行。
- **實作的合約**（伺服器端在 judge 票 `apps/api/app/video_automation/judge.py`）：
  - `POST automation/judge/outline`：`{ slug, brief, options: [{ key, title, summary, hook }] }`，2–3 個選項，`summary`/`hook` 缺的送空字串（請求模型拒絕未知欄位）。回 `{ choice, probabilities, options: { key: { stance, demo } }, advice, passed, note }`。`client.judgeOutline`。
  - 大綱審核 `payload = { brief, options, pick? }`：Jev 過關（`passed`）就附 `pick`，伺服器收到時核准並設 `choice`；沒過就把 `note` 當退回意見給 `replan`（計入 `MAX_REPLANS`），重寫到上限仍不過，就附上最後一次的 `pick` 送審等站主（卡片顯示表）；409 `video_judge_not_enabled`（立場空白或開關關）不附 `pick`；404（站上還沒有這個端點）也走站主；429/502/連不上 → `later`，下一輪再問。本機 `review-push --gate outline` 走同一條，只是外部失敗時印出警告、照舊送審（再跑一次就會補上 pick）。
  - 成片審核 `payload.qa` = `review/qa.json`（`{ ok, final_sha256, items }`，`final_sha256` 就是 `final.mp4` 的 sha256，也就是這關的 `content_sha256`）。`review-push --gate final` 先跑 `qa`：結束碼 0/1 → 送審附報告（只附這份 `final.mp4` 的報告）；4 → 結束碼 4、不送審，工人 `later`；3 → 結束碼 3。摘要「成片 mm:ss，自動品管 11 項全過」或「…自動品管 N 項沒過：id、id」。
  - 上架審核 `payload = { package, minutes, chapters, locales, zh: { title, description, tags }, disclosure: { synthetic, reason }, checklist }`；`package = { ok, final_sha256: <upload/metadata.json 的 sha256>, items: [files, descriptions, captions, disclosure] }`（`tools/video/package/check.mjs`，純函式加 `readPackageReport`）。`files` 角色：`final`（video/mp4，分段）、`thumbnail`（image/jpeg）、`captions_<locale>`（text/plain，例如 `captions_zh-TW`）、`description_<locale>`（text/plain）、`metadata`（application/json）；`UPLOAD.md` 不送。
  - `package` 把 `contains_synthetic_media` 與 `disclosure_reason` 寫進 `metadata.json` 的最後兩個鍵（值來自 `qa/checks.mjs` 的 `disclosureDecision`，`qa` 再跑也是同樣的位元組）；`skipped_caption_locales` 對五個語系裡沒有 srt 的每一個寫原因（字幕階段跳過的句子 id，或「沒有翻譯檔」）。上傳包檢查以五個語系為準（和 `qa` 的 captions 項一樣），沒有 srt 的要有原因。
  - 工人的 `report()` 現在帶 `youtube_video_id`（`video.json` 的值）：伺服器的 `upsert_project` 會把沒帶的覆寫成 null。
- **讀回影片 id**：`step()` 每輪先看 `automation/videos` 帶回的 `youtube_video_id`（web 票加的欄位，`ProjectSummary` 本來就有），對 active／done 而 `video.json` 還沒有 id 的影片，寫進 `docs/videos/<slug>/video.json` 的 `youtube.video_id`（`flow.mjs` `recordVideoId`；主機上這個目錄是工人掛的 `video_docs` volume，`/opt/mokaair/docs/videos`），回報階段「on YouTube」，`status` 就全部打勾。`youtube-sync` 指令還沒有實作（`tools/video/youtube/` 不存在），所以沒有可以沿用的函式。
- **要伺服器端配合的地方**：`apps/api/app/video_reviews/schemas.py` 的 `ReviewFile` 目前只收 `role` `^[a-z][a-z0-9_]{0,39}$` 與 `content_type` mp4/m4a/png/jpeg；上架審核附的 `captions_zh-TW`（連字號、大寫）、`text/plain`、`application/json` 會被 422 擋下，要在 web 票或 judge 票放寬（角色允許 `[A-Za-z0-9_-]`，型別加 `text/plain`、`application/json`）。工人遇到 422 會 `later`，每輪重試，不會卡死。
- 還沒做：主機上跑第二批三支成片的 `review-push --gate final`（要等 judge、web 票合併部署）。
