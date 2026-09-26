---
id: 2026-09-26-video-drama-look-keyframes
title: Video drama T4: look (character sheets) and keyframes stages with the look review gate
status: open
priority: P1
area: tools
owner:
claimed_at:
created_at: 2026-09-26T01:53:34Z
completed_at:
branch:
depends_on:
  - 2026-09-26-video-drama-core
  - 2026-09-26-video-drama-media-client
scope:
  - tools/video/media/look.mjs
  - tools/video/media/keyframes.mjs
  - tools/video/media/look-keyframes.test.mjs
  - tools/video/review
---

# Video drama T4: look (character sheets) and keyframes stages with the look review gate

## Why

角色跨鏡頭一致是漫劇品質的第一件事。做法：先為每個角色生幾張設定圖讓站主選（`look` 關卡），之後每個鏡頭的關鍵影格都以選定的設定圖當參考生成，並用視覺模型打分、不合格自動換 seed 重做。這張票做 `look` 與 `keyframes` 兩個階段，以及它們的送審與讀回。

## Definition of done

- [ ] `look --slug S`：每角色 `candidates` 張（預設 3）、judge 評分、`suggested`、聯絡表 `characters/contact-sheet.png`、`characters/manifest.json`（含 `look_hash`）；全部不及格再補一輪（最多 2 輪）仍不過就結束碼 1 並列出評語；`--choose` 直接寫 `characters/choice.json`。
- [ ] `review-push --gate look` 每角色送一張審核（`subject`＝角色 id）；`review-pull` 收齊後寫 `choice.json` 並記核准（綁 manifest 雜湊）；`STEP_LABELS` 涵蓋兩種格式的每一步（有測試）。
- [ ] `keyframes --slug S`：需 look 已核准；每鏡提示詞＋選定設定圖（＋風格圖）出 1920×1080 關鍵影格；judge（identity、prompt、style、artifacts、無文字、主體避開字幕帶）不過換 seed，最多 3 次；`needs_review` 與評語進 manifest；相鄰鏡頭 dHash 太近警告；`keyframes/contact-sheet.png`；`thumbnail.data.shot` 記 `thumbnail_source`。
- [ ] `review-push --gate storyboard` 送聯絡表與關鍵影格；成片送審附最低的 10 個 identity 分數。
- [ ] 所有遠端呼叫之間看 STOP 檔；中斷後重跑不重付。

## Steps

- [ ] `media/look.mjs` → `review/sync.mjs` 的 look 送審與讀回 → `media/keyframes.mjs` → storyboard 送審 → 本機 `review/look.html` → 測試。

## How to verify

```bash
node --test tools/video/media/look-keyframes.test.mjs tools/video/review/*.test.mjs
node tools/video/cli.mjs look --slug <SLUG> --dry-run
```

## Notes

設計全文在 `docs/videos/DRAMA.md`（跟 T1 一起合併）；供應商、價格、政策的研究依據也在那裡。
