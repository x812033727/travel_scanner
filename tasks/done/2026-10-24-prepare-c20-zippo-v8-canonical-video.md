---
id: 2026-10-24-prepare-c20-zippo-v8-canonical-video
title: Prepare C20 Zippo approved v8 canonical video project
status: done
priority: P1
area: docs
owner: codex-open-task-reconcile-510e
claimed_at: 2026-10-24T13:16:15Z
created_at: 2026-10-24T05:24:54Z
completed_at: 2026-10-24T13:16:29Z
branch: codex/open-tasks-reconcile-20261024
depends_on: []
scope:
  - docs/videos/story-everyday-zippo-c20-short-v8
---

# Prepare C20 Zippo approved v8 canonical video project

## Why

C20 原根目錄仍是歷史 v5r4 的 42 句機器稿；站主已另核准 v8 約六分鐘的 36 句、36 鏡和整支 US$25 本機試片上限。須在不覆寫歷史原件、不啟動付費的情況下，讓新版有可重建、可檢查的獨立機器專案。

## Definition of done

- [x] 新的頂層資料夾從三個核准 SHA-256 鎖定的 v8 原件，產生 36 句、36 鏡、六章的有效 `video.json`、`series.json` 與非付費查核對接；原 42 句根目錄不動。
- [x] 33 插圖及 3 後製字卡與核准逐鏡逐字配對，MiniMax `image-01`、精確 cute-mystery、無 logo／火焰／吸菸或真實專利重建的方向保留。
- [x] 機械檢查與未過製作關卡具體可見，沒有宣稱實際配音、成片、後台匯入或上架。
- [x] 草稿 PR #1808 CI 與整合審查完成後合併；本票在 PR 待審期間留在 review。

## Steps

- [x] 在既有稀疏 checkout 建置；未建立新 worktree 或 clone。
- [x] 用固定 hash 與 ID／旁白／來源註記對照產生六個機器／說明檔，再用 `build.mjs --check` 讀回。
- [x] 跑 schema、奇聞畫面規則、紙上時間軸、lint 與聚焦測試。
- [x] 保留約六分鐘短版與讀音、預算路由及後台同集 identity HOLD。

## How to verify

從 repo 根目錄：

- `node docs/videos/story-everyday-zippo-c20-short-v8/build.mjs --check` → 36 exact lines／36 scenes。
- `node docs/videos/story-everyday-zippo-c20-short-v8/preflight.mjs` → schema 0、visual 0、33 shot／3 card，紙上 9,995 frames 與 91.10% 插圖；預期 exit 3／HOLD，見下方。
- `node tools/video/cli.mjs lint --file docs/videos/story-everyday-zippo-c20-short-v8/video.json` → 現行 2 errors／12 warnings；不得說已過片長關卡。
- `node --test tools/video/core/schema.test.mjs tools/video/core/curio.test.mjs` → 21/21 PASS。
- `npm run check:tasks` → exit 0；其他舊票警告非本票衝突。

## Notes

- 前製來源／畫面 36／36 獨立 PASS、兩位只讀旁白各 12／12 Yes；站主 v8 精確劇本與分鏡核准、整支本機試片 US$25 上限核准均已記在舊專案 `reviews/owner-v8-*`。轉檔沒有修改旁白或原核准 prompt。
- `c200102` 只在 `say` 暫把 Zippo 讀作「之寶」，顯示逐字稿 text 不變，`say_for` 綁原句雜湊；依據為 Zippo 中國官網的「之宝」別名。仍須獨立文字覆核及實際人耳聽驗。現行 lint 兩個明確 blocker：`target_minutes` 的五分鐘下緣及紙上 5.6 分鐘估時撞通用八分鐘門檻。另有中文景別誤判 33 個的聚合警告、兩句逾 40 單位及九個紙上 >10 秒鏡頭。須等 C20 專屬實測短版時間政策與語音聽驗，不得把片頭片尾湊正文。已核准購買上限不代表預算帳本／實價就緒。
- `node --test tools/video/core/story.test.mjs ...` 在這份稀疏 checkout 唯一失敗是測試 fixture `docs/videos/story-everyday-moleskine-c03/video.json` 未檢出（ENOENT）；另外 schema/curio 21/21 全過。不要為此複製完整 repo。
- 新 slug `story-everyday-zippo-c20-short-v8` 指向第 20 集；現行後台是否能安全以同集版本取代舊 intake 尚待獨立確認，勿直接匯入造成同集重複。


### 2026-10-24 owner-directed reconciliation

站主要求處理全部open任務：不再需要或已有完成證據的項目結案。此為純任務紀錄接手；不接管其他live producer、不改產品scope檔、不發起付費、正式站寫入或YouTube操作。

Disposition: close_completed.

- Open requirement: 草稿 PR #1808 CI 與整合審查完成後合併；本票在 PR 待審期間留在 review。
- 最後未勾項只有 PR #1808 合併；live gh pr view confirms MERGED at 2026-10-24T08:22:49Z, commit 0f166b266f46da55464a27ed8a83d6d7d43f2db2 already on origin/main。

只結案 v8 canonical preparation；短版實測、語音、成本帳本、後台匯入和媒體交付均保留。
