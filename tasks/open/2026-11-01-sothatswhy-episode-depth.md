---
id: 2026-11-01-sothatswhy-episode-depth
title: So Thats Why: plan episodes by story depth and duration
status: review
priority: P1
area: docs
owner: codex-gpt6-7ba3
claimed_at: 2026-11-01T05:39:40Z
created_at: 2026-11-01T05:39:38Z
completed_at:
branch: codex/sothatswhy-refresh-20261101
depends_on:
  - 2026-11-01-sothatswhy-refresh
scope:
  - docs/videos/so-thats-why/refresh-20261101
  - docs/videos/so-thats-why/CURRENT.md
  - tools/video/so-thats-why
---

# So Thats Why: plan episodes by story depth and duration

## Why

站主要求再依片長和無聊風險篩題，相關題目可組成一支主題長片；接著提出十萬筆以上素材池，再從素材編成影片。第一輪的 100 題不得再被當作 100 支各 13 分鐘的影片。需把「問題素材」「單集企劃」「實測劇本／成片」分清楚，提供可逐支審閱的主線、時間估計與退場條件。

## Definition of done

- [x] 100 題每題有唯一第二輪去向：44 題組成 30 支候選，25 短片、26 補強後重評、5 暫緩。
- [x] 每支有核心問題、合題理由、章節秒數預算、證據缺口、無聊風險與刪減條件；明示尚無逐段稿或實測音訊。
- [x] 十萬筆以上素材池有分層、來源／去重／查核欄位、階段檢查點與評估規則；目前僅 313 筆來源，不宣稱已建成大池。
- [x] 本機 list/brief 改以單集為單位，素材 ID 導向母企劃，第二輪退題不可繞過；所有狀態仍非核准製作。
- [x] CURRENT、SPEC、README、生成表一致；舊題包、舊核准與共用產線未改。
- [x] 獨立編輯最後覆核、PR 更新與檢查證據入檔。

## Steps

- [x] 依 youtube-video 的獨立聽眾審閱要求請 science_sources 審內容厚度。
- [x] 完成 30 支企劃與 56 題退場理由，修正 P02／P06／P22 硬撐片長，以及 P08／P21／P26 標題前提。
- [x] 新增 POOL-STRATEGY.md，將大型索引與分階段擴庫列入後續票。
- [x] 4 項定向回歸通過：原判重與第二輪退題、合題來源／變長規格、來源與企劃漂移、重複／缺漏／預算錯配拒絕。
- [x] 更新 PR #1971，維持 draft / no-auto-merge，留正式同步與大池實作為獨立票。

## How to verify

使用內建 Node 24.19：`node --test tools/video/so-thats-why/catalog.test.mjs`、`node tools/video/so-thats-why/cli.mjs check`、`node tools/video/long-form/cli.mjs check`、`npm run check:tasks`、`git diff --check`。實際執行 `brief A68` 應為 P01 三素材，`brief S26` 應拒絕；檢查新增文件本機連結。完整 CI 狀態與定向通過分開記錄。

## Notes

- 所有片長是正文估計。現有四個主節拍不是已填滿的劇本；須補 45 秒內資訊節拍、試讀、當期逐主張查核，再計時與報價。
- P02 改午後大雨且縮至 14–16 分；P06 縮至 10–12 分；P22 先補硬水對照，8–10 分 conditional，證據不足即刪減／撤長片。
- 13 分鐘的 11 loops 基準按正文時長比例規劃，個別 brief 帶實際數量；共用 lint 尚未同步，不把規劃當 runtime 生效。
- 正式同步票 `2026-11-01-sothatswhy-production-rules-sync` 需依 CURRENT 指到的最新版執行，不能沿用票內舊固定 13 分鐘文字。
- 大池實作票 `2026-11-01-sothatswhy-candidate-pool`；沒有啟動大量抓取、付費研究或十萬筆生成。
- 獨立審閱見 REVIEW-EPISODES.md：44 素材全導母企劃、56 退題全拒絕；不等於完整稿盲評或全部事實重查。
- 本機定向 4/4、catalog/program check、既有 473 個 long-form 來源收據、2,286 個 task 格式、66 個本機連結與 diff whitespace 通過。完整 tools/docs-videos 本機未完成；最新完整 CI 以 PR 為準，不宣稱全套通過。
- PR：https://github.com/x812033727/travel_scanner/pull/1971。此票留 review；無合併、部署、付費生成或上架。
