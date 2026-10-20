---
id: 2026-10-20-prepare-meta-brand-story-x05
title: Prepare Meta brand story X05
status: done
priority: P2
area: docs
owner: codex-meta-x05
claimed_at: 2026-10-20T15:47:49Z
created_at: 2026-10-20T15:47:46Z
completed_at: 2026-10-20T17:15:11Z
branch: codex/brand-story-meta-x05
depends_on: []
scope:
  - docs/videos/story-everyday-meta-x05
---

# Prepare Meta brand story X05

## Why

站主要求 Netflix X03 交付後繼續下一個缺的品牌題材，沿用奇聞檔案局的濃縮開場、旁白、插圖、配樂、字幕、5 秒片頭與 21 秒片尾規格。Beats 已占 X04 的隔離分支，Meta 排 X05；四份 SEC 原始年報能支持「Reality Labs 虧損，但 Meta 營業利益仍為正」的反常問題。本票先完成不付費的前製與獨立查核，避免 X03 工作樹互相污染。

## Definition of done

- [x] X05 有來源可追、符合敘事與影片 schema 的繁中六章逐句稿、視覺指示與上架文案，數字口徑正確；另有兩支離線 Shorts 稿。
- [x] 獨立來源與兩份敘事審閱、Shorts 來源審查、lint 和免費乾跑留下結果；未啟動付費媒體，未把概念片當正式發布。

## Steps

- [x] 核對 FY2021／FY2022／FY2023／FY2025 SEC 10-K 原文與下載雜湊，整理主張邊界。
- [x] 寫 treatment、逐句稿、source matrix、series/video JSON、發音與畫面指示。
- [x] 跨代理來源和聽眾審查，修訂後執行 lint、TTS／關鍵影格／配樂乾跑及文件測試；配樂等待真實 TTS 時間軸。

## How to verify

在本工作樹根目錄執行 `node docs/videos/story-everyday-meta-x05/compose-video.mjs`、`node tools/video/cli.mjs lint --slug story-everyday-meta-x05`、`node tools/video/cli.mjs tts --slug story-everyday-meta-x05 --workdir /workspace/.brand-video-workdir --dry-run`、`node tools/video/cli.mjs keyframes --slug story-everyday-meta-x05 --workdir /workspace/.brand-video-workdir --dry-run --takes 3`、`node tools/video/cli.mjs music --slug story-everyday-meta-x05 --workdir /workspace/.brand-video-workdir --dry-run`、`npm run test:docs-videos`、`npm run check:tasks`、`git diff --check`。

## Notes

現有隔離工作樹 `/workspace/travel_scanner_beats` 已有完整的 Beats X04 前製稿，故 Meta 題號改為 X05。四份 SEC HTML 原始 URL、SHA 與會計分母見本目錄的 `source-notes.md`。原始文件及 FY2022 重新下載的位元驗證記於 `reviews/source-audit.md`；2026-10-20 的出站讀取已成功，成片前仍需重核原件。X05 目前零付費呼叫。

2026-10-20：最終 `video.json` SHA-256 `9ec57716a952185ef4ba17b50493b851c8b60223145a0606a40d07deaabab85c`，84 句、66 鏡、18 張原生數字卡；兩份獨立敘事盲讀 12/12 PASS，來源查核 84/84 與 18 卡 PASS。兩支 Shorts 原生 schema/鏡頭檢查 0 錯誤且獨立來源 PASS。發音手動草稿釘選零付費完成，`tts --dry-run` 列 84 句、2,393 計費字元；沒有實際 TTS、圖、片、字幕或 YouTube 連結，正文實測 8 分鐘仍是後續硬關卡。全組 US$25 上限維持。
