---
id: 2026-10-24-prepare-c11-ucc-canonical-video-project
title: Prepare C11 UCC canonical video project
status: done
priority: P2
area: docs
owner: codex-c11-canonical
claimed_at: 2026-10-24T04:04:03Z
created_at: 2026-10-24T04:03:59Z
completed_at: 2026-10-24T04:08:47Z
branch: codex/c11-ucc-canonical-preflight-20261024
depends_on: []
scope:
  - docs/videos/story-everyday-ucc-c11
---

# Prepare C11 UCC canonical video project

## Why

C11 UCC 已有站主核准並綁定 SHA-256 的 78 句繁中稿與 78 鏡方向，但還沒有 `video.json` 等機器可讀專案檔。後台的企劃／原稿進度不代表本機試片、付費配音或成片已完成；需先保全核准原件，再建立可檢查的非付費轉檔。

## Definition of done

- [x] `video.json`、`series.json`、`brief.md`、`claims.md`、`verify-1.md` 與轉檔收據可供機器與人讀取；78／78 旁白及逐鏡對應原件，69 張插圖、9 張後製字卡。
- [x] 核准的 `script.md`、`visual-plan.md/json` 及來源說明雜湊保持不變，標註紙上時長與實際 TTS／付費關卡的差別。
- [x] 非作者獨立檢查轉檔，並將結果寫入同目錄收據。
- [x] 草稿 PR 附帶 `no-auto-merge`，不把轉檔當作後台匯入或上架。

## Steps

- [x] 查主幹、C11 既有任務與 PR、路徑占用，從最新 `origin/main` 建立共用 checkout 分支後認領本票。
- [x] 寫可重建且核對核准原件 SHA 的 `build-canonical.mjs`；新增六章專案、主張表與 QA 對接。
- [x] 跑非付費 lint、facts 與看板檢查；保留所有敘事和時長警告。
- [x] 獨立對照逐句與逐鏡，補收據；推草稿 PR 並在 PR 內搬到 `tasks/done`。

## How to verify

`node docs/videos/story-everyday-ucc-c11/build-canonical.mjs`；`node tools/video/cli.mjs lint --slug story-everyday-ucc-c11`；`npm run check:tasks`；`node --test tools/video/core/schema.test.mjs tools/video/core/lint.test.mjs tools/video/qa/facts.test.mjs`；讀回核准原件 SHA、78／78 句／鏡、圖片與字卡數、`say_for` 與 QA `factsChecks`。真正正文至少 480 秒與插圖時間至少 70% 待付費前路由和實際語音驗收，不能用紙上估算核准。

## Notes

2026-10-24：`reviews/owner-script-approval.md` 綁 `script.md` C55D7713…、`visual-plan.md` 74159C33…、`visual-plan.json` DF45CBEA…；三者與現行檔逐位元一致。C11 沒有整支 US$25 報價或付費核准，不得借用 C07／C10／C15 額度。現行 `category: explainer` 是靜態插圖加後製 `stats` 的 lint 相容值；品牌系列身分由 `series.json kind: story`、slug 和 episode 11 表示，正式匯入時仍須讀回。

本機 lint 0 errors、9 warnings：紙上總畫面 502 秒、扣開場後畫面 456.73 秒；候選 `say` 對應的正文純語音紙上僅 384.96 秒，完全未驗收 480 秒門檻。五段鉤子空檔、開場 loop 和同一日期反覆提及等警告來自站主已核准稿，本票不私改。原稿頁首的舊「待審／未核准」字樣仍在核准雜湊內，以 `reviews/owner-script-approval.md` 為後續決定。`factsChecks` 對衍生 `verify-1.md` PASS；看板檢查 exit 0。一次包含 `automation/story.test.mjs` 的定點測試有 67 PASS、1 個整檔子行程 exit 1 且無堆疊；其餘 schema/lint/facts 測試通過，待收據寫明，不宣稱整組 PASS。

非作者獨立轉檔覆核對 78／78 逐句、69／9 逐鏡、21 個 `say_for` 判 PASS；據其意見補上 H1 濱田市短頁及限制 YouTube 說明欄措辭，覆核者讀回兩處修正及四個原稿 SHA 後再次 PASS。詳見 `docs/videos/story-everyday-ucc-c11/reviews/canonical-video-preflight-20261024.md`。發音提示是候選，尚未經人耳聽審。

草稿 PR #1813：https://github.com/x812033727/travel_scanner/pull/1813；`no-auto-merge` 已讀回。這張票的「完成」只指非付費 canonical 轉檔，**不代表 C11 可付費、可匯入或可上架**。後續需另報整支 C11 費用並獲站主核准，且實測語音與畫面時間、完成媒體 QA。
