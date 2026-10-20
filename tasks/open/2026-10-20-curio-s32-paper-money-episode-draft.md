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
- [ ] 另一位讀者只讀劇本作敘事盲評；若有實質問題修稿並重跑檢查。
- [ ] 本票完成時只提交有來源的前製檔，不呼叫付費語音、插圖或配樂，也不假稱站台關卡已核准。

## Steps

- [x] 承接已固定 P1、P2、Y93、Y94 四份原文，補清尤爾十九世紀導論與 Cordier 1903 修訂第三版的作者／年代層次，以及方括號中的 Ramusio 特有段落。
- [x] 編寫 A 案企劃、83 句正文、3 句片尾、逐句來源與 12 組開放懸念，場景以卡通插圖為主。
- [x] 改正威尼斯銀幣與其他金幣的泛稱、來自印度等地商人所售的金銀寶物、鈔幣貶值與工墨後又調回原額等精度問題。
- [x] 依獨立來源／畫面覆核修正尤爾年代、貨幣與兩張卡面的出處精度，保存 `verify-1.md` 精確 SHA 與 PASS 紀錄。
- [ ] 待獨立劇本盲讀完成，再視結果完成本票。

## How to verify

在 repo 根目錄執行：

```sh
NODE_USE_ENV_PROXY=1 NODE_NO_WARNINGS=1 VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s32
NODE_USE_ENV_PROXY=1 NODE_NO_WARNINGS=1 VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs script --slug curio-s32
npm run check:tasks
```

`tools/video/review/sync.mjs` 的 `outlineOptions` 對 `brief.md` 應解析出 A、B 兩個選項。`lint` 目標 0 errors／0 warnings；配音和成片後再量實際長度，此階段只有估算。

## Notes

截至 2026-10-20：本地預估總旁白 9:34、開場濃縮 0:52、正文 8:22、片尾旁白約 0:20；75 張 `shot`、8 張來源與原文短引卡、1 個 `outro`，正文插圖占 75／83。頻道 5 秒片頭與 21 秒品牌片尾是在後製套用，尚未合成。獨立來源／畫面覆核 **PASS**；劇本盲讀待排。封版 `video.json` SHA-256 `e30355ea28b111edaee5973c18e6257cee3252f577c1f76b54d9ff9c2215bce3`、`script.md` `ed6b4c49807c18b3b80eeaac5000df27c45f36221798eec3943461de57de71bf`，其餘固定雜湊詳見 [`verify-1.md`](../../docs/videos/curio-s32/verify-1.md)。沒有付費請求、沒有網站送審或任何已完成影片。前製檔的來源邊界詳見 [`research.md`](../../docs/videos/curio-s32/research.md)。
