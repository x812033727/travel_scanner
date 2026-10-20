---
id: 2026-10-20-curio-s41-gate-readiness
title: Curio S41 gate readiness after audited preproduction
status: blocked
priority: P2
area: docs
owner: codex-s41-qin-feasibility
claimed_at: 2026-10-20T10:45:33Z
created_at: 2026-10-20T10:45:32Z
completed_at:
branch: codex/curio-s34-endurance-20261019
depends_on: []
scope:
  - docs/videos/curio-s41
---

# Curio S41 gate readiness after audited preproduction

## Why

S41 R5h 書面前製在 `a3063691` 推送並經獨立 source/visual 與雙盲讀通過；站台影片流程只把 `verify-1.md` 視為已查核，原本的完整報告在 `reviews/source-visual.md`。大綱也須送真實 A/B 並記錄站台判定，不可把本機 Jev 挑選冒充站主核准。

## Definition of done

- [x] 站台收到現版 A/B 大綱，回覆的挑選與實際核准狀態被準確記錄。
- [x] `verify-1.md` 把獨立逐景查核接到流程，保留 R5h 的五個 frozen 審閱檔原樣。
- [x] 站台確實核准 A 案後，送出經 R7 史料及獨立盲讀核對的劇本關卡，準確標明站台 `pending` 與本機委任決定。
- [x] R12 片尾修訂稿完成獨立史料覆核、兩位全新盲讀與政策預檢，重送精確劇本關卡，準確記錄站台仍 pending。
- [ ] 只對 R7→R12 更改的句子補錄並逐句查核；仍有未核清旗標時不進付費插圖。

## Steps

- [x] 讀取站台 S41 狀態與企劃 A/B parser 輸出。
- [x] 送大綱並以 `review-pull` 查詢，不製造人工核准。
- [x] 將已有獨立報告對接 `verify-1.md`，重跑本機狀態與查核。
- [x] 在站台大綱核准後送 R7 script gate，更新交接紀錄；站台回 `pending`。
- [x] R7 111 句 TTS 完成並保留工作樹，第一輪音檢 30 flags 已如實分類，未核准 audio gate。
- [ ] R12 史料、故事面板、政策、劇本及音訊關卡逐項通過後交接插圖預算與三景原圖 pilot。

## How to verify

`node tools/video/cli.mjs lint --slug curio-s41`；`node tools/video/cli.mjs status --slug curio-s41 --workdir /tmp/s41-review`；`NODE_USE_ENV_PROXY=1 NODE_NO_WARNINGS=1 node tools/video/cli.mjs review-pull --slug curio-s41 --gate outline --workdir /tmp/s41-review`。`review-pull` 的 `pending` 是等待站主，並非核准。

## Notes

2026-10-20: 站台原先沒有 S41 紀錄。`review-push --gate outline` 已把當前 `brief.md` SHA-256 `f1b37142edd09fc7a7d29e003f7be9e4f1a852525218211128a749a6f24db1ff` 的 A/B 送到站台；Jev 選 A（機率 1.00、立場 0.88、建議 0.01），但這是手動推送影片，沒有 worker `auto.json`，站台回 `pending`。立即 `review-pull` 回 `outline: waiting for the owner`。不得用本機 `approve` 或虛構 worker 檔把 pending 寫成核准。S41 工作目錄在 `/tmp/s41-review/curio-s41`，合併盲讀 `review/narrative.json` 是有效的現版；無付費媒體。

2026-10-20 後續：站台於 10:49:43 UTC 真實核准 A 案，`review-pull` 於 11:00:51 UTC 記錄精確 brief hash。R7 script SHA-256 `c19c7a3705a6df5273d06b201446ed4da633efd00dc60f536b3009c4e5fdc6e5` 經新盲讀 13/13、Jev 政策一次 PASS，送站台仍是 `pending`。使用者的常設委任容許另在本機核准該 R7 hash 供語音製作，note 明記**不是站台核准**；這不改寫上述早期 pending 歷史。R7 合成 111 WAV（2,639 billable characters），正文 11:25；持久 workdir `/workspace/.video-work/curio-s41`。第一次音檢 111/111、30 flags、exit 1，未批准 audio gate；全套 R7 舊 take 備份在 `.video-work/.snapshots/curio-s41-r7-voice`。詳見 `verify-2.md`、`reviews/audio-first-pass-r7.md`。

2026-10-20 當時 R8：僅 17 條口播及對應 claims 列窄改，`video.json` SHA-256 `14097e7a20768fcfa87e6bf1d83ba29ef23a90940272e231d691f2ab692a5e10`、`script.md` `755e0b0566b10a438cc5640c1df63be072d11b9a870688cfcfd30dd3c45a731b`；舊 R7 site/local script gate 對 R8 已過期。R8 當時仍待全新盲讀和 Jev；該稿已由 R9–R11 取代。史料與書面畫面差分見 `reviews/source-visual-r8-delta.md`。

2026-10-20 當時 R11：R10 雙盲皆判 `no_detour` 未過，已壓短罰則與漢代一般藏書支線，具體傳續答案補到片尾。精確稿與來源／書面畫面差分見 `reviews/source-visual-r11-delta.md`。R11 獨立史料覆核通過，但兩位全新盲讀者都判 `no_recap` 未過；舊 R7 站台／本機劇本 gate、政策與音檢不得沿用。未做 R11 TTS、插圖或站台推送。

2026-10-20 R12 凍結時：僅 `qb999a` 換為「可教讀、可互校的篇章」與「秦前原卷完整存留不能由後世記錄證明」的證據界線，正文不動；精確稿與來源／書面畫面差分見 `reviews/source-visual-r12-delta.md`。當時尚待兩位全新獨立盲讀及獨立史料覆核，未做 R12 政策、TTS、插圖或站台推送。

2026-10-20 R12 續辦與阻塞：上述「尚待」已由 [verify-3.md](../../docs/videos/curio-s41/verify-3.md) 取代。兩位新盲讀合併 PASS，獨立史料／書面畫面 PASS，一次 Jev 政策 PASS；R12 站台 script 送審仍 **pending**，本機委任精確稿核准另記。R12 語音 19 句新合成（489 字元）、77 句沿用，`qb006` 一次定點重錄（31 字元），實測開場 59.07 秒、正文 9:02.70。全片音檢兩輪均 **16/96 flags**；具體轉寫風險與兩版 WAV 見 `reviews/audio-r12-gate.md`。環境無可靠原音輸入或獨立 ASR，不能證實音檔已唸對。**本任務 blocked 在音訊驗收，不推 audio gate、不買插圖；後續需獨立聆聽／轉寫確認，或來源安全的窄改後以新 hash 重走劇本關卡。**
