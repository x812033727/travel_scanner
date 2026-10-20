---
id: 2026-10-20-brand-story-dominos-x02
title: 製作 Domino's 品牌故事本機試看片
status: review
priority: P1
area: docs
owner: codex-gpt6-dominos-x02
claimed_at: 2026-10-20T13:04:17Z
created_at: 2026-10-20T13:04:14Z
completed_at:
branch: codex/brand-story-dominos-x02
depends_on: []
scope:
  - docs/videos/story-everyday-dominos-pizza-x02
  - tasks/open/2026-10-20-brand-story-dominos-x02.md
---

# 製作 Domino's 品牌故事本機試看片

## Why

站主要求每支品牌故事做完後開 PR 並接續下一支，沿用奇聞檔案局規格。Adobe X01 本機概念試片的 PR #1619 已開，下一支為 X02 Domino’s。此集須用 2009–2011 SEC 原始申報說明核心披薩配方與後續同店銷售，區分季度、年度與管理層歸因；正式頻道動畫不在雲端工作區，因此交付明標概念版。

## Definition of done

- [x] 六章敘事、逐句來源與獨立審查、盲讀及零錯誤 lint 完成；四份 SEC 申報保留在說明欄。
- [x] 依單片 US$25 硬上限控制，完成至少八分鐘正文、30–60 秒濃縮開場、繁中旁白、MiniMax 插圖、配樂、5 秒概念片頭、21 秒概念片尾與 1080p 本機試片；未拆帳費用保留為待核，不能宣稱全額已審計。
- [x] 輸出可關閉繁中 SRT／VTT、縮圖、SHA 與重建說明；完成視覺、音訊與整檔影音技術 QA，將 14 張插圖、3 句旁白與正式素材／可點片尾待辦清楚交接。
- [x] 將完成的製作包開成獨立草稿 PR #1620；正式音訊與頻道品牌未核准前不宣稱已上架。

## Steps

- [x] 原件核查、稿件、視覺規格與預算乾跑；不付費的片頭片尾流程預驗。
- [x] 依序生成 TTS、逐句音訊複查、最多三次插圖選圖、資料卡與配樂，逐批核對成本；保留 3 句音訊及 14 鏡視覺待人工正式審查。
- [x] 合成本機試片與字幕，抽圖、整檔解碼、音量及字幕檢查；更新交接文件。
- [x] 跑 `npm run test:docs-videos`、`npm run check:tasks` 與檔案檢查；提交分支及開 PR。

## How to verify

在儲存庫根目錄跑 `node --use-env-proxy /workspace/dominos-video-tool-cli.mjs lint --slug story-everyday-dominos-pizza-x02`；已完成的 `tts`、`check-audio`、`keyframes --takes 3`、`render`、`music` 紀錄見工作區台帳。**不要重跑完整 `keyframes`**，以免改動人工待審旗標；只使用唯讀 `--dry-run` 查額度。嚴格 `local-preview.mjs --dry-run` 須列出 14 個待審，明標概念模式 `--allow-review-needed --dry-run` 須 ready；完成試片後以 `node docs/videos/story-everyday-dominos-pizza-x02/reviews/local-preview-qa-check.mjs --workdir /workspace/.brand-video-workdir` 核對整檔解碼、影格、音量、字幕、雜湊與台帳，並跑 `npm run test:docs-videos`、`npm run check:tasks`。

## Notes

2026-10-20：PR #1619 為前一支 Adobe X01；本分支基於 `origin/main` 且本集檔案獨立。站主已授權採建議選項、不逐項詢問，單片付費生成硬上限 US$25。正式主機片頭片尾與 YouTube Studio 可點元素無法在此工作區取得；明標概念版只供本機審片。初始媒體台帳 US$0，TTS 73 句／2,184 字，63 張插畫首輪乾跑約 US$0.85、至多三次約 US$2.55；配樂及其他未拆帳費用不得記零。

2026-10-20 13:34 UTC：現行稿 SHA-256 `8042f9fb33037b38e377bbc38914b14e278dd844d2ade26f4410615ec3fd7846`，lint 0／0；73 句語音完成，正文 15,583 格／8:39.43、首章 1,516 格／50.53 秒；音訊複查有 `x020103`、`x020406`、`x020504` 三句仍待人耳確認（`reviews/audio-revision.md`）。配樂已生成，主工作區可見台帳 US$0.08。63 張插圖分三個隔離工作區製作，完成後須驗證每張至多 3 take、未核准鏡頭保留 `needs_review`、逐張 SHA 與完整成本，再合併主工作區；`local-preview.mjs --allow-review-needed` 只產明標未核准概念片與證據 JSON，不寫正式成片／核准。概念片預期 16,363 格／9:05.43；正式品牌片頭片尾、音訊人耳驗收與 Studio 可點結束畫面仍待正式環境處理。

2026-10-20 13:52 UTC：63 張選圖已合併主工作區，manifest SHA-256 `62bd94e42972e1c0fd31a441f343c124c87e401a5f560ad8229e7961da70acc9`；63 個不同選圖檔皆驗 SHA、每鏡最多 3 次，無未結 jobs／預留。主工作區可見台帳 **US$1.7135**（圖片＋judge US$1.6335、配樂 US$0.08；未知語音／轉錄／複查／稅費另算）。獨立逐鏡 QA 見 `reviews/visual-qc.md`：14 張仍標 `needs_review`，`b04-s02` 和 `b05-s04` 尤有假字。嚴格預檢如實阻擋 14 張，明標概念模式預檢通過；10 張資訊卡及縮圖已渲染，概念片現正逐景編碼。**不要在此主工作區重跑完整 `keyframes`**：它可能重選已過 judge 的 take 而清除人工 QA 旗標；如需檢查只跑唯讀 `--dry-run`，聯絡表已有離線 `qc/contact-sheet-01..03.jpg`。

2026-10-20 14:11 UTC：修正版本機概念 MP4 與字幕已輸出到 `/workspace/brand-story-preview/dominos-x02/`，影片 SHA-256 `ba430870cad347ccdc6275d21dc6a9cf2c52c8ae433f81b4ffd5a3eec1f4452d`。實際 16,363 影格／545.433 秒、H.264 High／BT.709、AAC 48 kHz；全檔影音解碼與逐格時間戳通過、−14.0 LUFS／−1.0 dBTP，95 則繁中 CC 與現稿逐位元組相同。見 `reviews/local-preview-qa.md`、`local-preview.md`，另有唯讀 QA checker 及結果 JSON。技術 PASS，正式發布 HOLD：14 張插圖、3 句旁白、正式品牌動畫與 YouTube 可點片尾仍待處理。

2026-10-20 14:13 UTC：製作包已開[草稿 PR #1620](https://github.com/x812033727/travel_scanner/pull/1620)，task 轉為 review。`npm run test:docs-videos` 243／243、`npm run check:tasks` 通過；原始影音與交付副本的 SHA-256 相同。影片檔只在工作區交付目錄，PR 保留逐項待審旗標。
