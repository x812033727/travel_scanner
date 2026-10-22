---
id: 2026-10-22-c04-bubble-wrap-source-backed-curio
title: C04 Bubble Wrap source-backed Curio-format treatment
status: done
priority: P2
area: docs
owner: codex-gpt6-c04
claimed_at: 2026-10-22T02:05:47Z
created_at: 2026-10-22T02:05:40Z
completed_at: 2026-10-22T02:22:31Z
branch: codex/brand-story-bubble-wrap-c04
depends_on: []
scope:
  - docs/videos/story-everyday-bubble-wrap-c04
---

# C04 Bubble Wrap source-backed Curio-format treatment

## Why

「日用品的意外轉身」已把 C04 Bubble Wrap 排在下一集，但系列表只有題目與 Sealed Air／專利取證入口。把「失敗壁紙變包裝」當定論會混淆公司多年後的回顧、1957／1959 專利申請的當年文字與真正的銷售證據；同系列的 C03 也已確認必須沿用奇聞檔案局的敘事及畫面規則。C03 的本機試片授權不適用於 C04。先建立一份可供站主與另一代理審查的非付費企劃，再決定是否進逐字稿與整集報價。

## Definition of done

- [x] C04 有逐項一手來源矩陣，分清專利申請／核發、公司回顧、IBM 佐證與尚未證實的商業細節。
- [x] 六章 Treatment 有一條因果主線、30–60 秒濃縮開場、30–45 秒鉤子草圖、Curio 畫面／配樂／片頭片尾界線及整片未核准付費的狀態。
- [x] 另一代理獨立覆核主要事實並留下綁定內容雜湊的收據；退回點修訂後重新覆核。
- [x] 本輪只形成企劃與查核，不把它稱為逐字稿、試片、站主核准或 C04 付費生成。

## Steps

- [x] 從 Sealed Air、IBM 與原始美國專利查起，辨識可講及不可推定的事實。
- [x] 建立來源矩陣與六章 Treatment 作者初稿，將用途轉換與材料工程分開。
- [x] 取得獨立來源覆核並修訂有問題的句子，留下版本雜湊。
- [x] 跑文件與任務檢查，更新本票及草稿 PR 交接。

## How to verify

讀 `docs/videos/story-everyday-bubble-wrap-c04/source-matrix.md` 的 F01–F11 並逐條開其原始連結，確認 Treatment 的每個年份、人物與商業主張都有相符限制；核對另一代理收據的 SHA-256。跑 `npm run check:tasks`、`npm run test:docs-videos` 的相關文件檢查及 `git diff --check`。本階段沒有 `video.json`，所以不得以影片 lint 或媒體 status 假裝成片檢查。

## Notes

2026-10-22 已在獨立 `codex/brand-story-bubble-wrap-c04` worktree 認領。1957-12-23 牆面專利申請與 1959-11-27 包裝緩衝申請的文字可作主線；申請不代表產品上市。IBM 1401 包裝只見 Sealed Air 事後回顧，IBM 官方史頁目前僅佐證 1401 在 1959 年推出，沒有採購／包裝收據。溫室用途也只見公司回顧。暫未建立總鏡數、張數或價格；不得使用 C03 的 US$25 核准、配音或圖片。

另一代理的[來源審查收據](../../docs/videos/story-everyday-bubble-wrap-c04/reviews/source-review.md)只放行非付費 Treatment，並綁定來源矩陣 SHA-256 `05FC2AB1C1E4EF64DC71E27DE54343A9D765FA2B320AD6AB72A5FFA769DB9756`、Treatment SHA-256 `8504F4FFF7F535CA39E2D496163B8827D2E99162835E7B67A909FFB5D3EFE06C`；收據以 Git 儲存的 LF 換行計算 SHA-256 `8B9E76CCBDBA2B713B4D404F6CC637DF20C1521A45379BC46F46BFF313B698C3`。逐字稿、畫面與成本仍須下一階段查核。

驗證：`npm run check:tasks` 通過；Codex 內建 Node v24.19.0 跑完整 `docs/videos` 測試 236/236 通過。系統 Node v24.13.0 跑同一套 235/236，唯一失敗是已在 `tasks/open/2026-10-16-fix-windows-unicode-path-crash-in.md` 記載的 `package-runtime.mjs` 在非 ASCII Windows 路徑原生退出 `3221226505`，單獨重跑也重現。C04 無程式或媒體檔變更。
