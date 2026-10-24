---
id: 2026-10-24-c20-zippo-v5r2-visual-review
title: Repair C20 Zippo v5r2 visual cue and independent checks
status: in-progress
priority: P1
area: docs
owner: codex-c-series-integration
claimed_at: 2026-10-24T02:56:27Z
created_at: 2026-10-24T02:55:46Z
completed_at:
branch: codex/c20-zippo-v5r2-20261024
depends_on: []
scope:
  - docs/videos/story-everyday-zippo-c20
---

# Repair C20 Zippo v5r2 visual cue and independent checks

## Why

C20 v5r1 的兩位旁白盲讀都指出日期碼支線或英國寄件路線打斷「送修時到底修什麼」的主線。v5r2 已刪英國寄件路線，`c200401` 畫面也已限縮，但兩份新版盲讀仍一致指出日期碼段落是可移除的繞路。v5r3 將九句改為修理範圍與原件去留的連續問題；須重新獨立來源／配鏡查核與兩份盲讀，保留原企劃核准界線。

## Definition of done

- [x] v5r3 的 59 句與 59 鏡逐項對齊；現行旁白與分鏡沒有日期碼段落，v5r2 檔案與審查鎖定仍保留作歷史證據。
- [ ] 非作者逐句來源／配鏡覆核綁定新版確切檔案雜湊；兩位只讀旁白讀者各自在讀其他材料前鎖定 13 題判定。
- [ ] 將 PASS／HOLD 和未完成的站主劇本核准、付費、實測配音、匯入及上架界線寫進 PR，不冒稱本機試片完成。

## Steps

- [x] 沿用既有 v5r2 本機修稿；不重寫已改過的 59 句。
- [x] `c200401` 文字分鏡與 JSON 同步縮小到日期碼，重算視覺檔雜湊；旁白投影保留原 SHA。
- [x] 鎖定 v5r2 獨立來源／配鏡 PASS 與兩份 `no_detour=No` 盲讀，沒有將任何舊結論轉移到 v5r3。
- [x] v5r3 改九句及其配鏡，重生純旁白投影；59/59 機械配對與紙上正文 2,180 單位已核對。
- [ ] 獨立來源／配鏡覆核及雙盲只讀旁白判定，逐項處理實質 HOLD。
- [x] 跑機械配對、`npm run check:tasks` 與 `git diff --check`。
- [ ] 推送草稿 PR；如有新 HOLD，先修訂再提站主核稿。

## How to verify

- `Get-FileHash` 核對作者五檔與旁白投影；機械比對 59 個 ID、原文、來源標籤、畫面類型、MD／JSON 提示詞。
- 逐項讀原發行者來源，查核鉸鏈、外觀、內膽及各地維修條款的歸屬；獨立查核收據須記錄 HOLD。
- 兩份新盲讀只開 `reviews/narration-v5r3-only.txt`，SHA-256 `CA1C2F11D718A62E0AF91434E352CA8AE0B4D1497E700A5CCD5B9227148F178C`，13 題各有 ID 與句子依據。v5r2 投影及兩份鎖定保留，不能沿用其結論。
- `npm run check:tasks`、`git diff --check` 與草稿 PR CI。

## Notes

- 舊分支曾重現已在主分支移除的廣範圍保全任務，造成 claim 衝突；先將 C20 分支變基到最新 `origin/main`，再以本票正常 claim，沒有使用 `--force`。
- v5r3 正文 2,180 個 UTF-16 紙上單位約 523.2 秒，只是估算；實際正文配音必須至少 480 秒，插圖須占成片正文畫面時間至少 70%。站主目前只採用 C20 企劃，未核准 v5r3 劇本或付費試片。
