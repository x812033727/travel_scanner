---
id: 2026-10-24-prepare-c08-kikkoman-canonical-video-project
title: Prepare C08 Kikkoman canonical video project without paid calls
status: in-progress
priority: P1
area: docs
owner: codex-c-series-integration
claimed_at: 2026-10-24T03:36:03Z
created_at: 2026-10-24T03:36:00Z
completed_at:
branch: codex/c08-kikkoman-canonical-preflight-20261024
depends_on: []
scope:
  - docs/videos/story-everyday-kikkoman-c08
---

# Prepare C08 Kikkoman canonical video project without paid calls

## Why

C08 的 84 句／84 鏡雖已獲站主核准，仍只有 Markdown 前製材料；影片工具需要一份可讀、可對回核准原文的 canonical 專案。保留稿件原件與付費停線，不能把紙上時長或其他集的 US$25 上限移轉到 C08。

## Definition of done

- [x] 以核准原稿建立 84 場景、73 still、11 後製字卡及六章專案檔，原件五個 SHA-256 不變。
- [x] 84／84 旁白與逐鏡同序、逐字／逐 prompt 可還原；留下卡片圖文差異與付費／時長 HOLD 收據。
- [x] 非付費 lint、facts、check:tasks、針對性測試皆實跑並記錄結果，不把 lint error 說成通過。
- [x] 另一位代理獨立只讀覆核轉檔，結果見 reviews/independent-canonical-conversion-20261024.md。
- [ ] c080611 片尾規則衝突須經新版差異查核、盲讀和站主核准後才可解。
- [ ] 實際語音 480 秒、插圖時間至少 70%、C08 整支報價與付費核准、單集預算路由、匯入及成片驗收由後續工作處理。

## Steps

- [x] 讀回 owner-script-approval.md、owner-treatment-approval.md、來源與 v5.3 差異收據；固定五個核准來源雜湊。
- [x] 建立 video.json、series.json、visual-plan.json、brief.md、claims.md、verify-1.md 及 reviews/canonical-video-preflight-20261024.md。
- [x] 84／84 text、ID、shot prompt、運鏡與完整卡片文字對回原稿；五句 GK 的 say 僅候選且與 text 雜湊綁定。
- [x] 記錄唯一 lint error c080611 與兩個僅供站主審閱的最小改句候選，沒有改寫核准稿或機器 text。
- [x] 獨立轉檔審查 PASS，維持 lint／媒體 HOLD。
- [ ] 等後續 C08 改稿決定。

## How to verify

node tools/video/cli.mjs lint --slug story-everyday-kikkoman-c08（現況預期 exit 1：c080611 真實片尾規則衝突；13 warnings）。

node --test tools/video/core/schema.test.mjs tools/video/core/lint.test.mjs tools/video/qa/facts.test.mjs（67／67 PASS）。

npm run check:tasks（exit 0；其他舊票警告）。逐列與五份原件 hash、factsChecks、生成檔 hash 詳見 reviews/canonical-video-preflight-20261024.md。

## Notes

2026-10-24：由共用 checkout 的 codex/c08-kikkoman-canonical-preflight-20261024 分支進行，沒有再開工作樹、付費呼叫、後台匯入或上傳。c080407 核准的是泛用瓶嘴側面示意，機器 stats 預覽只顯示文字，必須在正式後製補圖並獨立驗收。C08 沒有 production-quote.md 或站主專屬付費上限；原文正文 462.48 秒、採五處候選 GK say 後 464.88 秒都只是紙上代理量，不能當作 TTS 實長。PR #1681 已關閉而未合併，本分支沿 main 已保留的同雜湊原件工作。

候選 B 只改 c080611 的片尾文句，單句來源／配鏡差異 PASS，但兩位獨立盲讀對 one_line、no_toc、chapters_link、no_recap、one_thread、no_detour 都判 No；詳見 reviews/c080611-proposed-b-blind-20261024.md。依雙讀規則整集 HOLD，不能只替換結尾便說稿件已通過。下一輪須提出單線敘事修稿，並按精確新版重新查核、盲讀、請站主核准；不以填字灌到 480 秒。

## 2026-10-24 short-v8 接續

站主已在本次任務核准 v8 **精確 36 句旁白與 36 列畫面方向**（SHA-256 `040d9a499ddb864f62ebf0edcc948cc58439ffa13d0dae0ce5a9475297ee5d69`／`0676e76a4c9d49b12ece74df1835a72ce264eabb24a3158635921f57244dd241`）。此前候選稿頁首 HOLD 是歷史狀態；來源 36／36、畫面 36／36 及雙盲讀無共同必要題否決見 `docs/videos/story-everyday-kikkoman-c08/reviews/v8-short-independent-review-20261024.md`。

- [x] 原 84 句專案和核准原件位元組保留，另建 `docs/videos/story-everyday-kikkoman-c08/short-v8/` 非付費機器投影；36 ID 同序一對一、六章、30 插圖／6 後製卡。
- [x] 凍結兩個來源雜湊，提供可重跑 `build.mjs`、逐字稿／逐鏡 JSON、QA 對接與收據 `short-v8/preflight-20261024.md`。
- [x] 已跑 schema/facts/畫面比例靜態檢查、67 個針對性測試、task-board check；lint 3 errors／5 warnings 如收據，沒有宣稱 PASS。
- [x] `test:docs-videos` 全套 235／236 PASS；未修改的 imported-long-languages runtime freezing 測項在 Windows 子行程以 `3221226505` 退出，單獨重跑同樣失敗，詳見 v8 收據；不宣稱完整 gate 綠燈。
- [ ] `MoMA` 念法需獨立審核與真人聲音驗收；短版 480 秒共用長片 guard 待 C15 路由整合，不改全域規則。
- [ ] nested `short-v8/` 只有 `lint --file` 可讀；worker 及其他 `--slug` 指令未選取它。短版政策和 episode identity 明確後，依 README 將整包推進頂層同 slug 目錄，重新 lint、同 slug 工作目錄及後台 `stories.json` 精確 dry-run／apply 條件讀回。
- [ ] 實際 TTS 時長、按秒插圖 70%、`v7e03` 平面功能圖、整支 C08 可歸因報價／付費核准、匯入、上傳與成片驗收仍待後續；本輪沒有付費或後台寫入。
