---
id: 2026-10-02-sothatswhy-series-branding-default
title: Apply approved So Thats Why intro only to its series
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-02T13:39:56Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/core/branding.mjs
  - tools/video/core/branding.test.mjs
  - tools/video/branding/cli.mjs
  - tools/video/branding/branding.test.mjs
  - docs/videos/BRANDING.md
---

# Apply approved So Thats Why intro only to its series

## Why

站主已選定原來如此系列的 6.9 秒片頭，應接在原有 5 秒 Mokaair 開場後。現有品牌選擇器只有全頻道 current；直接替換會讓其他系列也加入這段。需建立系列專用預設，讓新的原來如此長片使用已選定的 11.9 秒合併開場。

## Definition of done

- [ ] 新的原來如此長片首次建置採用已選定 357 影格開場與既有 90 影格片尾；其他系列沿用全頻道預設，Shorts 保留原行為。
- [ ] 系列識別與既有 `isExplainer(doc)`／縮圖 `sothatswhy` 的定義一致，不以標題猜測。
- [ ] 既有品牌 pin、舊版未 pin 成片、final/publish 核准與已上傳影片保留原有保護，不自動重製或大量 renew。
- [ ] 合成、字幕、章節與外語音軌皆正確使用 11.9 秒開場偏移，且不重複 prepend 原開場。
- [ ] 安裝工具可隔離系列預設，驗證 SHA-256、357/90 影格與音軌；無效素材不能改寫 current。
- [ ] 本機適當測試通過，說明安裝／部署與正式影片驗收仍需各自的實際證據。

## Steps

- [ ] 先查同範圍活躍任務、PR 與 worktree，再認領；核對已選素材包與文件。
- [ ] 在品牌讀取與安裝工具加入系列 registry，保留全頻道 fallback 與 pin 優先序。
- [ ] 驗證 assemble/compile 入口共同選擇，以及 caption/dub/章節共用 presentation timeline 的正確偏移。
- [ ] 加入會驗出路由、pin 與時間偏移錯誤的測試，更新 BRANDING.md。

## How to verify

測試：原來如此新長片選到 357/90；其他系列仍為全頻道 150/90；Shorts 不套用；既有 pin 不變；受保護影片不採用新版本；竄改素材安裝失敗且 registry 不變；字幕／章節／外語音軌只位移一次。
依 dev-and-ci skill 跑變更相關 branding tests、`npm run test:tools` 與 `npm run check:tasks`。
若需要修改額外檔案，先核對碰撞並擴充 task scope，不越界直接改。

## Notes

定案與雜湊：[2026-10-02 素材選用紀錄](../../docs/videos/branding-release/2026-10-02-sothatswhy-intro-approval.md)。
素材包位於 git 外 `~/mokaair-work/so-thats-why-intro-20261002/v2-7s-interleaved/approved/`，schema 1 manifest 可由既有 packageSelection 讀取；intro 已含原開場。
intro SHA-256：`208ff0300b463f6f71f9c059586837accbeb22e28a8eccc7dfad0af6145c5337`。
series-intro SHA-256：`2d4d21618d9519eaa17c47c68e0f9bd9384167ed8348d77001c509c907a61930`。
素材已經站主選用，但尚未部署／安裝系列預設。本待辦不授權重新生成語音、付費生成、啟動 uploader 或排入影片工作；需要的正式安裝與驗收另以實際行動及證據確認。
