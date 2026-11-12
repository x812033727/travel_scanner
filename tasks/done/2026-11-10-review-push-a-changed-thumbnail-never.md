---
id: 2026-11-10-review-push-a-changed-thumbnail-never
title: review-push: a changed thumbnail never reaches an approved publish review
status: done
priority: P2
area: tools
owner: claude-opus-5.5-p06-p18-handoff
claimed_at: 2026-11-12T06:38:12Z
created_at: 2026-11-10T23:48:58Z
completed_at: 2026-11-12T06:56:08Z
branch:
depends_on: []
scope:
  - tools/video/package/cli.mjs
  - tools/video/package/package.test.mjs
  - docs/videos/long-form/review.json
  - docs/videos/long-form/review.md
  - apps/api/tests/fixtures/video_language_contract
---

# review-push: a changed thumbnail never reaches an approved publish review

## Why

2026-11-10，sothatswhy-p06-bubble-film：上架包核准之後，站主發現縮圖的人被字擋住，縮圖換了一張（`thumbnail.data.shot`），
`package` 重做，四項檢查都過，但 `metadata.json` 的雜湊沒變（063341314fd0，縮圖不算在裡面）。再跑 `review-push --gate publish`，站上回
`publish submitted for review (approved)`，`review-files --gate publish --dry-run` 顯示站上的 `publish/thumbnail.jpg` 仍是舊檔
（55114e4c…，本機 `upload/thumbnail.jpg` 是 60aa1a8a…），八個 `publish/thumbnail_<locale>.jpg` 也是舊的。`languages` 那關有換成新縮圖（狀態回到 pending）。
結果是站主照站上的上架包上傳時，會拿到舊縮圖；這次是把新縮圖直接傳給站主繞過。

## Definition of done

- [x] 上架包核准後縮圖檔變了：`review-push --gate publish` 會把新檔送上站，並讓 publish 回到待核准（或明確說明站上檔案過期、要怎麼重送），不會默默維持舊檔的「已核准」。

## Steps

- [x] 查 `tools/video/review/sync.mjs` 的 publish 送審與站上 `/api/video` 對同一個 metadata 雜湊的處理（看起來是以 metadata 雜湊當作同一份）。
- [x] 決定綁定要不要納入縮圖檔的雜湊，加測試。

## How to verify

核准一個上架包 → 改縮圖 → `render` → `package` → `review-push --gate publish` → `review-files --gate publish --dry-run` 的 thumbnail 雜湊等於本機 `upload/thumbnail.jpg`。

## Notes

Findings, decisions and dead ends, so the next agent does not repeat them.
- 2026-11-12（claude-opus-5.5-p06-p18-handoff）：伺服器 `apps/api/app/video_reviews/admin_service.py` 的 `submit_review` 找到同 gate、同 `content_sha256`（＝`upload/metadata.json` 的 sha256，`sync.mjs` `publishSubmission`）且狀態不是 pending 的審核時直接回傳那一筆（approved 的 publish 只多掛備份檔），新上傳的縮圖不會換上去；退回（rejected）也一樣不會重開。
  最小的修法是 `tools/video/package/cli.mjs` 在 metadata.json 加一個 `thumbnail_sha256`（thumbnail.jpg、thumbnails/<locale>.jpg、variants 的 sha256），縮圖一變雜湊就變，站上自然開一筆新的 pending；`qa/cli.mjs` 寫 disclosure 時會保留其他欄位。但 `package/cli.mjs` 在片長審查的雜湊綁定裡（`tools/video/long-form/review.mjs` REVIEW_FILES、`docs/videos/long-form/review.json`），要獨立審查代理出 DURATION_ONLY 增量收據，而 review.json／review.md 正在 2026-10-29-daily-brief-on-the-host-worker、2026-10-30-admin-video-delete-dropped 的 scope 裡，所以沒做。scope 已從 `tools/video/review` 改成 package 兩支檔；做這張票的人還要把 review.json 加進 scope。
  繞法：`languages` 關卡會換八張語言縮圖（P06 2026-11-12 重送後 pending，雜湊等於新檔）；主縮圖 `publish/thumbnail.jpg` 只能另外交給站主。
- 2026-11-12：站主授權接手（「授權你修工具，P06 P18 重送」），以 `--force` 認領；review.json／review.md 同時在 2026-10-29-daily-brief-on-the-host-worker、2026-10-30-admin-video-delete-dropped 的 scope，合併時要對齊綁定表（各自只改自己的列）。
- 2026-11-12 完成： 在 metadata.json 加 （8a7448cff），片長審查收據由  獨立審過（PASS — DURATION_ONLY）；語言合約檔重產，API 合約測試 52 passed。實測：P06 metadata 8a589e6aca80、P18 fb23b89f4307， 都開出新的 pending，站上  等於本機新縮圖（P06 a0bd3ba2b9f3、P18 33c245bc36fc）。副作用：任何已核准的集數重新 package 都會多這一欄、開一筆新的 publish 待審。
