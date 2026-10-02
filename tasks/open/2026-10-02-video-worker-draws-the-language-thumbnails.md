---
id: 2026-10-02-video-worker-draws-the-language-thumbnails
title: Video worker draws the language thumbnails before it packages a language batch
status: in-progress
priority: P2
area: tools
owner: claude-opus-5-5-worker-thumbs
claimed_at: 2026-10-02T04:18:04Z
created_at: 2026-10-02T00:29:59Z
completed_at:
branch: claude/worker-draws-thumbnails
depends_on:
  - 2026-10-01-video-worker-translator-fills-the-thumbnail
scope:
  - tools/video/automation/flow.mjs
  - tools/video/automation/automation.test.mjs
  - tools/video/render/cli.mjs
  - tools/video/render/render.test.mjs
---

# Video worker draws the language thumbnails before it packages a language batch

## Why

`2026-10-01-video-worker-translator-fills-the-thumbnail` 讓全自動工人的翻譯員把縮圖字寫進 `i18n/<locale>.json`（`thumbnail` 與 `source_hashes.thumbnail`）。但語言縮圖 `thumbnails/<locale>.jpg` 只有 `render` 會畫，而工人的 `languages()`（`tools/video/automation/flow.mjs`）在翻譯完只跑 `captions` 與 `package`，`render` 只在「frames rendered」那一步跑過一次，那時還沒有任何翻譯。結果 `package` 對每個語言都寫 `skipped_thumbnail_locales.<locale> = "not drawn yet; run render"`（`tools/video/package/cli.mjs` 的 `localeThumbnails`），全自動影片的上傳包永遠沒有語言縮圖，即使縮圖字已經翻好。

## Definition of done

- [x] 一支全自動影片的語言批次送出前，翻好縮圖字的語言在 `upload/thumbnails/<locale>.jpg` 有自己的縮圖，`metadata.json` 的 `thumbnails` 列出它。
- [x] 重畫只畫縮圖（畫格快取命中，不重畫場景），不讓已核准的 final（`visual_hash`、`final.mp4`）失效；如果會，寫明怎麼避開。
- [x] 縮圖畫不出來（字型缺字、版面塞不下）仍只是 note，語言批次照送，不重試。
- [x] 清理過工作區（`tidied_at`）的影片不跑 render。

## Steps

- [x] 讀 `tools/video/render/cli.mjs` 的 `localizedThumbnails` 與快取、`tools/video/core/state.mjs` 怎麼判斷 render 過期，確認在 final 核准後重跑 render 的影響。
- [x] 在 `languages()` 的 `captions`／`package` 前，只在有語言的縮圖字是最新但沒畫（或畫的時候字不同）時跑 `render`。
- [x] 補 `tools/video/automation/automation.test.mjs`：假的 `render` 寫 `thumbnail_locales`，上傳包帶著 `thumbnails/en.jpg`。

## How to verify

`node --test tools/video/automation/automation.test.mjs`，`npm run test:tools`；一支全自動影片勾了某語言的標題說明，語言批次送出後 `upload/metadata.json` 的 `thumbnails` 有那個語言。

## Notes

- 2026-10-02 由 `2026-10-01-video-worker-translator-fills-the-thumbnail` 的代理發現：那張票只讓縮圖字進到 `i18n`，畫圖不在它的 Definition of done 裡。
- 2026-10-02 claude-opus-5-5-worker-thumbs：認領時被 `2026-09-28-drama-listener-stale-check`（codex-ten-drama，PR #978 已合併）、`2026-09-28-sothatswhy-shorts-from-episode`（PR #904/#950/#962 已合併）、`2026-09-30-video-worker-moves-two-videos-at`（PR #999 已合併）的過期認領擋住，依交接說明用 `--force`。
- 判斷：final 核准綁的是 `final.mp4` 的 sha256，`visual_hash` 只看 `video.json`（不含 i18n），所以完整的 `render` 不會讓 final 失效；但它會重畫 `thumbnail.jpg`、聯絡表，部署後主題（`themeHash`）一變，快取鍵全變，所有場景都會重畫，螢幕錄影場景也可能重拍。所以不跑完整的 `render`，在 `tools/video/render/cli.mjs` 加 `--thumbnails-only`（因此把它和 `render.test.mjs` 加進 scope）：要求 `frames/manifest.json` 的 `visual_hash` 是這份腳本的，否則 exit 2；只畫各語言縮圖，只改 manifest 的 `thumbnail_locales`／`thumbnail_locale_gaps`，場景、`cache.json`、`thumbnail.jpg`、變體、聯絡表都不碰；螢幕錄影場景不進計畫，所以不開擷取瀏覽器。
- 工人（`languages()` 的 `drawLanguageThumbnails`）只在某語言目前的縮圖字雜湊（`localizedThumbnailHash`，package 比的同一個）和 manifest 記的不同、或檔案不在時跑它；zh-TW 補譯那條路也一樣。render 非 0 結束或丟例外只記一行 log，批次照送；送出後沒有待做的部件，下一輪不會再跑。清理過的影片在 `tidiedLanguages` 就回傳，不會到這裡。
- 驗證：automation 測試用真的 `render --thumbnails-only`（假瀏覽器）走完語言批次，證明只畫一張、`final.mp4`／`thumbnail.jpg` 位元組不變、`pipelineStatus` 前後一樣、上傳包有 `thumbnails/en.jpg`；畫不下與沒有瀏覽器兩種都只是 note、不重試；清理過的影片不跑 render。實機：`vibe-coding-first-website-2026` 的工作區複本（去掉 mp4/wav/m4a/build），只在複本的 `i18n/en.json` 加縮圖字，用 Edge 跑 `--thumbnails-only`：新增 `thumbnails/en.jpg`，只有 `frames/manifest.json`（加了語言欄位、`visual_hash` 不變）與 `state.json`（執行紀錄）變了，`status` 前後一字不差。第一次用較長的標題字時，真的版面檢查回報 sub 撞到 MOKAAIR 字樣，走的就是 note 路徑（exit 0）。複本已刪。
- 本機注意：共用的 node_modules 連結沒有 `@fontsource-variable/noto-sans-kr`／`-sc`，`render.test.mjs` 會有四個與這張票無關的失敗；這個 worktree 改成自己 `npm ci`。
- 未完成：`tools/video/long-form/review.test.mjs` 的獨立時長審查綁定（`docs/videos/long-form/review.json`／`review.md`）綁著 `flow.mjs` 與 `automation.test.mjs` 的雜湊，這個 PR 改了它們，所以會報 stale。依慣例由另一個獨立的審查代理讀這次的差異後重新綁定（作者不能自己審），這裡沒有動那兩個檔。
