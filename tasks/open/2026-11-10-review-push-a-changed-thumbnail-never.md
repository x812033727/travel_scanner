---
id: 2026-11-10-review-push-a-changed-thumbnail-never
title: review-push: a changed thumbnail never reaches an approved publish review
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-11-10T23:48:58Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/review
---

# review-push: a changed thumbnail never reaches an approved publish review

## Why

2026-11-10，sothatswhy-p06-bubble-film：上架包核准之後，站主發現縮圖的人被字擋住，縮圖換了一張（`thumbnail.data.shot`），
`package` 重做，四項檢查都過，但 `metadata.json` 的雜湊沒變（063341314fd0，縮圖不算在裡面）。再跑 `review-push --gate publish`，站上回
`publish submitted for review (approved)`，`review-files --gate publish --dry-run` 顯示站上的 `publish/thumbnail.jpg` 仍是舊檔
（55114e4c…，本機 `upload/thumbnail.jpg` 是 60aa1a8a…），八個 `publish/thumbnail_<locale>.jpg` 也是舊的。`languages` 那關有換成新縮圖（狀態回到 pending）。
結果是站主照站上的上架包上傳時，會拿到舊縮圖；這次是把新縮圖直接傳給站主繞過。

## Definition of done

- [ ] 上架包核准後縮圖檔變了：`review-push --gate publish` 會把新檔送上站，並讓 publish 回到待核准（或明確說明站上檔案過期、要怎麼重送），不會默默維持舊檔的「已核准」。

## Steps

- [ ] 查 `tools/video/review/sync.mjs` 的 publish 送審與站上 `/api/video` 對同一個 metadata 雜湊的處理（看起來是以 metadata 雜湊當作同一份）。
- [ ] 決定綁定要不要納入縮圖檔的雜湊，加測試。

## How to verify

核准一個上架包 → 改縮圖 → `render` → `package` → `review-push --gate publish` → `review-files --gate publish --dry-run` 的 thumbnail 雜湊等於本機 `upload/thumbnail.jpg`。

## Notes

Findings, decisions and dead ends, so the next agent does not repeat them.
