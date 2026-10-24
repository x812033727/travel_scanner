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
