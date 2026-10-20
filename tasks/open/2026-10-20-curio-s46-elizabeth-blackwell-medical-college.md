---
id: 2026-10-20-curio-s46-elizabeth-blackwell-medical-college
title: Curio S46 Elizabeth Blackwell medical college episode preproduction
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-20T12:59:56Z
completed_at:
branch: codex/curio-s34-endurance-20261019
depends_on: []
scope:
  - docs/videos/curio-s46
---

# Curio S46 Elizabeth Blackwell medical college episode preproduction

## Why

為新的奇聞檔案局歷史長片選獨立題目，避免與 S45 Blackwell Island 混淆；把 Elizabeth Blackwell 1847 年醫學院入學票的流行「玩笑」說法縮到原文可證範圍，準備可獨立審核的 8 分鐘以上劇本。

## Definition of done

- [x] 固定可重開的原著版本，記錄轉錄信件、學生決議與晚年回憶的證據界線。
- [x] A／B 選案與推薦 A、來源主張表、8 分鐘以上正文及可畫的 `video.json`／`script.md` 可供獨立覆核。
- [ ] 獨立逐句史料／分鏡覆核與兩名新讀者盲讀通過，交主工作者安排後續媒體關卡。

## Steps

- [x] 領取狹窄檔案範圍，固定 1895 原書與 P01–P14。
- [x] 完成 `research.md`、`brief.md`、`claims.md`、`video.json`、`script.md` 及 `verify-1.md`。
- [ ] 按獨立覆核意見修正並重新凍結；後續 TTS／插圖／組片由主工作者安排。

## How to verify

`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s46 --json`：0 error／0 warning。`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs script --slug curio-s46`：可重生定稿。`npm run test:docs-videos`：236/236；`npm run check:tasks`：2116 張通過。版本與其餘細節見 [S46 前製驗證](../../docs/videos/curio-s46/verify-1.md)。

## Notes

站主已給「採推薦、持續完成」方向；本地選 A，但網站大綱／劇本仍未核准。未做付費媒體、站台推送或 Git commit。不能把晚年「申請被懷疑是騙局」寫成學生開玩笑表決；不能以 1895 書中轉錄冒稱已查獨立校方原件。R1 的史料旁白 PASS、畫面 HOLD 及兩名盲讀問題已記在 `verify-2.md` 與本地盲讀收據；R2 新稿固定雜湊與修正表見 [verify-3.md](../../docs/videos/curio-s46/verify-3.md)，需以此**新版**重新獨立覆核與全新盲讀，不沿用 R1 通過結果。

R2 獨立史料與書面畫面覆核見 [verify-4.md](../../docs/videos/curio-s46/verify-4.md)：兩項均 HOLD。指出 `bkw019` 教授歸屬、`bkw090–096` 醫院董事程序誇述與 P12 說明；`bkw067–068, bkw113, bkw127–128` 原書行號缺口；`bkw102` 入院前畫面及多處提早／過晚使用的醫師／學生提示詞。這些是 verify-3 所記的 **R2 舊版** 問題，不可沿用 R1／R2 的通過項。

2026-10-20 R4：`bkw008` 1849 文憑典禮畫面改稱成人女性，唯一書面畫面 HOLD 已由另一位[獨立差分覆核](../../docs/videos/curio-s46/verify-8.md)判 PASS；R3 的 131 句史料 PASS 維持。R4 精確 `video.json` SHA `af80b750d864fdd634ce0d6002f0edcf484b78959ae2ccee97d31c6863dd2061`、`script.md` SHA `6db66fc2bc2f671c76d28982162d6c7c304c9722bbde41aed8a67e58c607c918`。兩名真正全新的敘事盲讀仍待回報；不得宣稱影片或站台通過。

2026-10-20 R4 雙盲已回：[A 9/13、B 8/13](../../docs/videos/curio-s46/verify-9.md)，共同必答 No 為 `one_line`、`no_toc`、`chapters_link`、`no_recap`，故正式敘事 **FAIL**。R5 要對時序、`bkw010` 目錄式承接、`bkw059/061` 重述做集中修正；再獨立覆核並用兩名新讀者重審。R4 的來源／畫面 PASS 不轉移到改稿；付費媒體及網站核准仍無。

2026-10-20 R5：[作者改稿](../../docs/videos/curio-s46/verify-10.md)凍結後，另一位覆核者按固定自傳與 R4 基線核對[史料及書面畫面差分 PASS](../../docs/videos/curio-s46/verify-11.md)。R5 新雙盲仍未完成；網站、音訊、圖像與成片都未開始。

以上 HOLD 已依 [R3 製作人修補紀錄](../../docs/videos/curio-s46/verify-5.md)修改並重凍結；`verify-5.md` 列新的精確 SHA-256 與待核項。R3 仍待獨立來源／書面畫面覆核及兩名全新盲讀者對同一版原旁白的裁決，未開始付費媒體。

R3 獨立差分覆核結果見 [verify-6.md](../../docs/videos/curio-s46/verify-6.md)：**史料旁白 PASS、書面畫面 HOLD**。R2 的史料歸屬、Blockley 程序、引文範圍和大部分提示問題已修；但 `bkw008` 是倒敘至 1849 年教堂畢業典禮，R3 新提示卻稱她 `medical applicant`。請把該景改成女醫學生或成年女子，重算版本雜湊、重跑 lint 並重審畫面。R3 原旁白史料 PASS 僅適用於 verify-6 所列精確旁白版本。

R4 僅把 `bkw008` 畫面角色改稱 `one adult woman in plain 1840s clothing`；結構比對確認除此 `data.prompt` 外無變動，五檔精確雜湊及 lint 0／0 見 [verify-7.md](../../docs/videos/curio-s46/verify-7.md)。`script.md` 仍是 R3 同一 SHA，史料旁白 PASS 適用；**R4 畫面尚待獨立確認，兩名全新敘事盲讀者尚未評定**。無付費媒體。

R4 書面畫面獨立覆核 [verify-8.md](../../docs/videos/curio-s46/verify-8.md) 已 PASS；但兩名新讀者對同一 R4 劇本在 [verify-9.md](../../docs/videos/curio-s46/verify-9.md) 共同否決時序、目錄式轉場、章節銜接與重述，故 **R4 敘事 FAIL**。R5 按五月二十四日→二十七日→六月二日重排、把晚年「申請被疑騙局」回憶嵌回到校脈絡、刪鑰匙孔岔題並修正重述／伏筆 payoff；新五檔 SHA、逐項來源、45.37 秒開場、8:44 保守正文及 lint 0／0 見 [verify-10.md](../../docs/videos/curio-s46/verify-10.md)。R5 是**作者自查版**，史料／畫面須重新獨立覆核，敘事須另兩名全新讀者盲讀；不得沿用 R4 PASS 開始媒體製作。無付費媒體或站台推送。
