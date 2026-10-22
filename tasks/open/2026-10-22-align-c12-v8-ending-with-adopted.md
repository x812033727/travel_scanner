---
id: 2026-10-22-align-c12-v8-ending-with-adopted
title: Align C12 v8 ending with adopted treatment
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-22T17:33:16Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/story-everyday-pyrex-c12-script/script.md
  - docs/videos/story-everyday-pyrex-c12-script/visual-plan.md
  - docs/videos/story-everyday-pyrex-c12-script/visual-plan.json
  - docs/videos/story-everyday-pyrex-c12-script/reviews/author-ending-v8.md
---

# Align C12 v8 ending with adopted treatment

## Why

C12 v7 的獨立逐句來源與畫面差異 PASS，但整體結尾對齊 HOLD：站主採用的 Treatment 第 39 行指定最後三句要回答轉身、提醒看具體商品，再邀觀眾留言故事相關的問題；訂閱連結只放固定 21 秒片尾。現行 N16 是正文口播的泛用訂閱句，且沒有留言題。

## Definition of done

- [ ] N16 改成與燈罩／烤器轉身相關的口語留言題，固定片尾承擔訂閱連結；維持 N12–N14 的回答與提醒。
- [ ] 成對更新鏡頭文字、收據及稿件雜湊；新版獨立差異重核與兩位純旁白盲讀另行進行。

## Steps

- [ ] 等前一張 `2026-10-22-repair-c12-pyrex-blind-narration-a` 的持有者完成或釋出；不要 `--force` 搶 scope。
- [ ] 做 N16 的小修與成對畫面更新，保留全部舊版 PASS／HOLD 收據。

## How to verify

`npm run tasks -- claim` 無重疊後才編輯；核對 script／visual ID、SHA，跑受影響的本機檢查，讓新代理核對結尾與盲讀。

## Notes

2026-10-23：新的作者代理試 claim 時被仍在 `review` 的 `2026-10-22-repair-c12-pyrex-blind-narration-a` 拒絕；該票 owner `codex-c12-script-repair`，claim 時間 2026-10-22T15:36:13Z，最後任務檔提交 17:19:59Z。暫停改稿，不接管他人的活躍 scope。建議 N16：「說到燈罩和烤器，你家還有哪件熟悉的物品，也藏著意想不到的前身？留言告訴我。」
