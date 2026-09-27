---
id: 2026-09-26-video-dubs-worker
title: Video languages worker: the worker makes only the parts the owner chose (metadata, captions, dubs), packages them and sends the languages review
status: open
priority: P1
area: tools
owner:
claimed_at:
created_at: 2026-09-26T17:59:41Z
completed_at:
branch:
depends_on:
  - 2026-09-26-video-dubs-command
  - 2026-09-26-video-dubs-check-language
  - 2026-09-26-video-dubs-captions-package
  - 2026-09-27-video-languages-api
scope:
  - tools/video/automation
  - tools/video/i18n
  - tools/video/core/stages.mjs
  - tools/video/core/stages.test.mjs
  - tools/video/qa
  - tools/video/package
  - tools/video/review
  - docs/videos/AUTOMATION.md
  - .agents/skills/youtube-video/references/prompts/caption-translate.md
  - .agents/skills/youtube-video/references/prompts/caption-review.md
---

# Video languages worker: the worker makes only the parts the owner chose (metadata, captions, dubs), packages them and sends the languages review

## Why

**2026-09-27 改寫。** 原本這張只做配音：站主勾了語言，工人做音軌、送 `dubs` 審核。站主 2026-09-27 把它擴成「多國語言」：每支影片先只做繁體中文，成片核准後站主決定加哪些語言、每種加什麼（標題與說明、CC、配音），決定並做好才排上架。設計在 `docs/videos/LANGUAGES.md`（配音的細節仍在 `docs/videos/DUBS.md`）；每支影片的選擇與 `languages` 關卡在 `2026-09-27-video-languages-api`。這張做工人：只做勾了的部件，包進上傳包，送一筆 `languages` 審核；`qa` 與上傳包檢查縮到選了的語系。原本的內容在 git 歷史。

## Definition of done

- [ ] 工人每一輪從既有的影片清單（`ProjectSummary.locales`、`locales_decided_at`、`languages`）看每支成片已核准的影片勾了什麼；有勾了還沒做（不是 ready／skipped／uploaded）的部件時，一輪做一個語言：
  - `i18n-sheet --slug <slug> --locale <l> --parts metadata,captions`（新旗標：只出勾了的部件；勾配音時句子帶 `max_chars`）→ 翻譯模型 → 字幕審稿模型 → `i18n-merge`；
  - 勾配音：`dub --locale <l>`；結束碼 1 → 翻譯模型的「縮短」模式（只給 `fit.json` 的句子與 `max_chars`；數字、專有名詞、說法不能改；字幕跟著用縮短後的句子）→ `i18n-merge` → 再 `dub`，最多 2 輪；`check-audio --locale <l>` → Jev 標記 → `dub --redo`，最多 2 輪；仍不行寫 `dubs/<l>/skipped.json`，不擋。
- [ ] 全部語言做完：`captions` 只寫 zh-TW 與勾了 CC 的語系（有配音的跟配音時間軸）；`package` 的 `upload/` 只放 zh-TW 與勾了的（`description.<l>.txt`、`captions/<l>.srt`、`dubs/<l>.m4a`），`metadata.json` 的 `locales` 照決定；`review-push --gate languages`（payload 每語三部件的狀態與跳過原因，檔案 role `description_<l>`、`captions_<l>`、`dub_<l>`）。之後多勾的部件再做一批、再送一筆（舊的 superseded）。
- [ ] `captions(state)` 不再迴圈 `settings.caption_locales`；沒勾語言或「只出繁體中文」的影片，`captions` 與 `package` 只有 zh-TW，其餘一個位元組都不變（測試比對）；語言不擋成片核准，也不擋站主上傳 mp4。
- [ ] `qa` 的 `captions` 與 `metadata` 項、`package/check.mjs` 的 `captionsItem` 與 `descriptionsItem` 都改成「zh-TW 加勾了的」；跳過的算過、列成警告；缺的算沒過。
- [ ] `caption-translate.md` 說明 `--parts`、`max_chars` 與縮短模式；`caption-review.md` 檢查預算。
- [ ] `AUTOMATION.md`：工人的一輪多一段「語言」（取代原本要寫的「配音」），輪數常數，成本連到 LANGUAGES.md 與 DUBS.md。
- [ ] `automation.test.mjs` 用假的 runner 走：只勾標題說明；勾 CC 與配音一次成功；縮短一輪後成功；兩輪後跳過；沒決定語言不跑；只出繁中不跑；已做過的部件不重做；上架後多勾一語再做一批。

## Steps

- [ ] `i18n-sheet --parts` 與 `captions`／`package` 的語系來源。
- [ ] `flow.mjs` 的語言段（翻譯、配音兩個迴圈、送審）。
- [ ] `qa` 與上傳包檢查。
- [ ] 提示詞、`AUTOMATION.md`、測試；主機上對一支已核准的影片勾 en 三個部件，看它跑完。

## How to verify

```bash
npm run test:tools
```

主機：在 `/admin/videos` 對一支成片已核准的影片按「只出繁體中文」，確認工人不做任何語言、影片進「可以上架」；再對另一支勾 en 的三個部件，等工人日誌出現語言那一段；影片頁的 `languages` 卡片列出 en 的說明欄、字幕與 `en.m4a`；`qa.json` 的 `captions` 與 `metadata` 項只看 zh-TW 與 en。

## Notes

- 工人在容器裡跑 `tools/video`，ffmpeg 是 `assemble` 用的那一個；要用 `--format mp3` 時先確認容器的 ffmpeg 有 libmp3lame。
- 每條音軌約 28 MB（m4a），送審的分段上傳與 `video_review_max_total_bytes` 要夠。
- 伺服器的 Gemini 月額度（`video_speech_gemini_monthly_character_limit`，預設 300,000 字元）先調高再勾配音：四條配音一支約 20,600 字元。
- 檔案角色慣例：`dub_<locale>` 語系小寫、連字號改底線（`dub_zh_cn`），`ReviewFile.role` 不收連字號；說明欄與字幕沿用上傳包的 `description_<l>`、`captions_<l>`。
