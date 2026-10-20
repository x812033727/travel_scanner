---
id: 2026-10-20-curio-s32-paper-money-episode-draft
title: Curio S32 paper money evidence episode draft
status: in-progress
priority: P2
area: docs
owner: codex-gpt6-s32-draft
claimed_at: 2026-10-20T06:29:32Z
created_at: 2026-10-20T06:29:29Z
completed_at:
branch: codex/curio-s34-endurance-20261019
depends_on: []
scope:
  - docs/videos/curio-s32
---

# Curio S32 paper money evidence episode draft

## Why

站主要持續做新的歷史系列，並採推薦方案。S32 的「馬可波羅有沒有到中國」原題過大且易把紙鈔制度相符誤寫成本人在場。上一張已完成的來源可行性票找到可固定重開的《遊記》英譯校注與《元史》原文；此票把安全的 A 案做成可獨立覆核的九分多鐘前製稿。

## Definition of done

- [x] `brief.md` 有後台可辨識的 A、B 選項，A 案縮題為「紙鈔制度相符能證明到訪嗎」。
- [x] `video.json`、`claims.md` 和產生的 `script.md` 可逐句對照固定原文，估計正文至少八分鐘；Curio 插畫、卡片、音樂、開場濃縮和片尾格式符合本系列。
- [x] 另一位工作者獨立逐句核史料與畫面；審查結果與固定雜湊見 [`verify-1.md`](../../docs/videos/curio-s32/verify-1.md)。
- [x] 第二位只讀劇本的盲評者指出 `mp061` 有報告章節順序的語句；已改成杭州章內的具體發現，且獨立來源單句差分覆核通過，見 [`verify-2.md`](../../docs/videos/curio-s32/verify-2.md)。
- [x] 新鮮盲讀 C 對 R2 劇本答 10／13，指出括號來源沒有說出版本名、3% 重提沒有明示回呼、首章章名不像事件；完整回條見 [`verify-blind-c-r2.md`](../../docs/videos/curio-s32/verify-blind-c-r2.md)。R3 已逐項修稿並通過獨立來源／畫面差分核，見 [`verify-3.md`](../../docs/videos/curio-s32/verify-3.md)。
- [x] R3 精確 SHA 的新鮮盲讀 D 與舊稿問題發現者 C 的重讀均為 13／13；兩份逐題回條見 [`verify-blind-d-r3.md`](../../docs/videos/curio-s32/verify-blind-d-r3.md) 與 [`verify-recheck-c-r3.md`](../../docs/videos/curio-s32/verify-recheck-c-r3.md)。
- [x] 只提交有來源的前製檔；企劃和劇本已由官方 CLI 送站台，讀回均為 `pending`、等待站主審核，見 [`verify-site-gates.md`](../../docs/videos/curio-s32/verify-site-gates.md)。沒有呼叫付費語音、插圖或配樂，也沒有假稱站台關卡已核准。
- [ ] 等站主對同一份 `brief.md` 與 `script.md` 作出決定，再由後續製作票處理語音、插圖和成片。

## Steps

- [x] 承接已固定 P1、P2、Y93、Y94 四份原文，補清尤爾十九世紀導論與 Cordier 1903 修訂第三版的作者／年代層次，以及方括號中的 Ramusio 特有段落。
- [x] 編寫 A 案企劃、83 句正文、3 句片尾、逐句來源與 12 組開放懸念，場景以卡通插圖為主。
- [x] 改正威尼斯銀幣與其他金幣的泛稱、來自印度等地商人所售的金銀寶物、鈔幣貶值與工墨後又調回原額等精度問題。
- [x] 依獨立來源／畫面覆核修正尤爾年代、貨幣與兩張卡面的出處精度，保存 `verify-1.md` 精確 SHA 與 PASS 紀錄。
- [x] 兩位獨立盲讀者先後回報舊劇本 13／13 與 12／13；後者的 `no_toc` 問題已以單句修稿處理並重跑 `lint` 及 `narrative` 題目清單。
- [x] 新 SHA 的來源差分覆核 PASS；前後只改 `mp061` 一句、劇本自動雜湊尾碼與任務記錄。
- [x] R3 僅調整第一章章名、`mp048`、`mp077`；獨立複核 `video.json` 恰三個 leaf 變動且史料支持，`lint` 仍 0 錯誤／0 警告。
- [x] R3 精確 SHA 劇本新鮮盲讀 D 與 C 重讀均 13／13，逐題紀錄已歸檔；送審後的 `script.md` SHA 不變。
- [x] 依手動影片關卡流程送出企劃與劇本卡，各自立即 `review-pull`；兩卡均為等待站主審核。
- [ ] 後續依站主審核結果續製；目前不合成任何付費素材。

## How to verify

在 repo 根目錄執行：

```sh
NODE_USE_ENV_PROXY=1 NODE_NO_WARNINGS=1 VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s32
NODE_USE_ENV_PROXY=1 NODE_NO_WARNINGS=1 VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs script --slug curio-s32
npm run check:tasks
```

`tools/video/review/sync.mjs` 的 `outlineOptions` 對 `brief.md` 應解析出 A、B 兩個選項。`lint` 目標 0 errors／0 warnings；配音和成片後再量實際長度，此階段只有估算。

## Notes

截至 2026-10-20：R3 本地預估總旁白 9:36、開場濃縮 0:52、正文 8:24、片尾旁白約 0:20；75 張 `shot`、8 張來源與原文短引卡、1 個 `outro`，正文插圖占 75／83。頻道 5 秒片頭與 21 秒品牌片尾是在後製套用，尚未合成。獨立來源／畫面全稿覆核對初稿 PASS，之後兩次小幅改稿均有精確差分 PASS，分別見 [`verify-1.md`](../../docs/videos/curio-s32/verify-1.md)、[`verify-2.md`](../../docs/videos/curio-s32/verify-2.md)、[`verify-3.md`](../../docs/videos/curio-s32/verify-3.md)。R3 精確 SHA 的盲讀 D 與重讀 C 均 13／13。當前 `video.json` SHA-256 `1e85570c510b1f14a69f0c1f7791decffc9356622071d157eef1efcbd71f251d`、`script.md` `d1c91eb102319d8ec78a92e1faa8c8b3f3596e9ba8132815b2d26212b45a6731`、`claims.md` `9532776025ac622a31a2ba033f8198eff1be230fcc757445f0f6010ab39ce53b`、`brief.md` `8445f3277c38e8712cde24481445e1e9f0e8a199c096c220c55d164d190eab82`。企劃與劇本站台卡均已送審且讀回為等待站主審核；無付費請求，未完成影片。前製檔的來源邊界詳見 [`research.md`](../../docs/videos/curio-s32/research.md)。
