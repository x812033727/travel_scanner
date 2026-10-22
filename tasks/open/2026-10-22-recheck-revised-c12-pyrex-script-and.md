---
id: 2026-10-22-recheck-revised-c12-pyrex-script-and
title: Recheck revised C12 Pyrex script and visual delta
status: review
priority: P1
area: docs
owner: codex-c12-source-review
claimed_at: 2026-10-22T15:07:57Z
created_at: 2026-10-22T15:07:51Z
completed_at:
branch: codex/brand-story-pyrex-c12-script
depends_on: []
scope:
  - docs/videos/story-everyday-pyrex-c12-script/reviews/independent-script-source-delta.md
---

# Recheck revised C12 Pyrex script and visual delta

## Why

作者已依 C12 前版獨立 HOLD 收據修改十句旁白及六鏡方向。前版審查綁舊雜湊，須對新位元差異再由另一位查核者簽收。

## Definition of done

- [x] 以新 script／visual SHA 綁定的差異收據列明逐 ID PASS／HOLD 與直接來源。
- [x] 確認未修改的 70 句、74 鏡在兩版間逐列相同，並審視相鄰鏡頭的敘事含義。
- [x] 將新發現的 O11 晚餐陶皿時序 HOLD 和 N14 製作註記交給作者。

## Steps

- [x] 重開 S1／S2／S7，查十句旁白和六鏡修改。
- [x] 用 Git 差異與 ID 列比對驗證變更集合及 hash。
- [x] 不改作者稿；寫收據並更新草稿 PR 的當前狀態。

## How to verify

`git diff acdfd7a7af5839bf234f6d076fcb0cce406aeb29..df3d24d75434d6c78eeffc4ee7fe47c8cc94c4d2 -- docs/videos/story-everyday-pyrex-c12-script/script.md docs/videos/story-everyday-pyrex-c12-script/visual-plan.md`；以逐列 ID 比較核 80／80 同序、十句與六鏡改動；`Get-FileHash` 確認新稿 hash。收據在 `docs/videos/story-everyday-pyrex-c12-script/reviews/independent-script-source-delta.md`。

## Notes

新旁白十句來源 PASS，但新 O11 畫面把完整陶皿放晚餐桌，再接 O12 破皿，與館方所述「先在烤箱碎裂、晚餐時 Bessie 提起」相反；整稿視覺 HOLD。N14 的「後製字卡」須釐清是圖上字幕還是另加卡。前版 `tasks/open/2026-10-22-independently-audit-c12-pyrex-script-and.md` 因 `blocked by policy` 留在本機，不碰；因此本機全域 `check:tasks` 仍會遇重複 ID。本票在草稿 PR 待作者修 O11，先標 review。
