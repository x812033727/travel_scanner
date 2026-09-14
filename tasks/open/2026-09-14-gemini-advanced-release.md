---
id: 2026-09-14-gemini-advanced-release
title: Gemini 深入系列：36 篇整套驗收與目錄開放
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-09-14T11:11:05Z
completed_at:
branch:
depends_on:
  - 2026-09-14-gemini-advanced-platform
  - 2026-09-14-gemini-advanced-work
  - 2026-09-14-gemini-advanced-research
  - 2026-09-14-gemini-advanced-creative
  - 2026-09-14-gemini-advanced-md
  - 2026-09-14-gemini-advanced-automation
  - 2026-09-14-gemini-advanced-api
scope:
  - apps/web/lib/guide-series.json
  - apps/api/app/guides/content/gemini-guide.json
  - apps/api/app/guides/content/gemini-plans-ai-pro-ultra-2026.json
  - apps/api/app/guides/content/gemini-api-cost-errors-guide.json
  - docs/gemini-series/lessons/00.md
  - docs/gemini-series/lessons/02.md
  - docs/gemini-series/lessons/49.md
  - docs/gemini-series/sources.json
  - docs/gemini-series/README.md
  - docs/gemini-series/advanced/release
  - docs/life-ai-series.md
---

# Gemini 深入系列：36 篇整套驗收與目錄開放

## Why

第二階段六個內容批次全部完成後，把 36 篇整合進既有 Gemini 總目錄，確保 1 hub＋86 篇完整可讀。此票涵蓋凍結清單、驗收、整合與受控開放；不能以部分內容替代整套完成。

## Definition of done

- [ ] 核對六批共 36 個唯一 slug、完整素材與逐篇驗證紀錄；必要真實執行沒有被 fixture 或官方文件整理冒充。
- [ ] 將 51–86 的資料一次加入正式 guide-series.json，保留 01–50 的 slug／篇序、八類、原五路線，新增 stage 與六條深入路線。
- [ ] hub 文案、導覽及第 02／49 篇價格與新計費構成依發布日重查；僅修改明列篇章，保留既有 section-N 連結。
- [ ] 全部 87 頁連結、錨點、先修 DAG、搜尋、手機／桌面、無 JS、複製、sitemap 與至少 72 張新增圖解／封面驗收。
- [ ] 完成相關前後端、工具、型別、i18n 與任務檢查；保存確切 Git SHA 與證據。
- [ ] 確認本次對正式環境的發布授權仍適用；正式變更依既有發布流程，預設深入可見性關閉，先 dry-run 再限定 slug 逐篇匯入。
- [ ] 發布任一步失敗即停，按 starting/verified 記錄核對已完成部分；所有新舊子文章均可讀後才更新 hub 及開放深入目錄。
- [ ] 公開瀏覽器和 sitemap 驗證後記錄完整推出；第一階段 2026-09-14 的歷史收據保留不覆寫。

## Steps

- [ ] 閱讀各依賴任務的驗證與限制，取得經審查的發布 manifest。
- [ ] 整合單一 catalogue、hub 與必要計費說明；來源資料逐篇保存查證日。
- [ ] 用 platform 提供的開關驗證不開放與全開放狀態，特別測舊第 50 篇的下一篇與既有 hub 的 SSR。
- [ ] 在 advanced/release/ 保存 dry-run、發布日誌、逐篇公開比對、資產與瀏覽器證據。
- [ ] 更新系列 README 與 AI 編輯總表的真正狀態；不把課綱或本機完成寫成上線。

## How to verify

使用 platform 任務交付的白名單發布命令及原有內容包／前後端／E2E 檢查。總數須為 87 頁，第二階段為 36 篇，全部通過且沒有重複或不明 slug；發布前後對照現有 51 頁與收據。實際命令與完成時間寫入本票。

## Notes

第二階段開關是必要順序保護：舊 hub 已發布，不能再沿用「hub 是否發布」作為新增連結的唯一條件。子文章逐篇匯入不具有原子性，發現失敗先核對而非整批盲目重送。
