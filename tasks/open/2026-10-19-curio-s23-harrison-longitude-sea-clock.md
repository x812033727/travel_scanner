---
id: 2026-10-19-curio-s23-harrison-longitude-sea-clock
title: Curio S23 Harrison longitude sea clock history episode
status: in-progress
priority: P2
area: docs
owner: codex-gpt6-s23
claimed_at: 2026-10-19T18:24:16Z
created_at: 2026-10-19T18:24:14Z
completed_at:
branch: codex/curio-s34-endurance-20261019
depends_on: []
scope:
  - docs/videos/curio-s23
---

# Curio S23 Harrison longitude sea clock history episode

## Why

站主要求在 S34 後繼續製作新歷史系列影片。S23「一個木匠，怎麼贏過全英國的天文學家？」牽涉 1714 年經度法、H4 航海試驗、經度委員會支付獎金的條件與國王介入；題庫只是候選敘述，須依原始文書辨明時間、試驗誤差與付款過程，再寫成有懸念而不誇大的歷史故事。

## Definition of done

- [x] `docs/videos/curio-s23` 有 8–10 分鐘的劇本、來源筆記、逐句事實表及 75–100 張靜圖分鏡。
- [x] 獨立史料覆核與最新版盲讀故事關卡通過，lint 零錯誤；語音審核、圖像報價與製作續行中。

## Steps

- [x] 檢查 S23 無其他認領或 PR，建立窄 scope。
- [x] 固定可讀的 1765 年法案對 1714 年經度獎的追述、1773 年法案及 Harrison 1767 年當事人紀錄；核對 H4 航試與獎金，未有原件支持的 George III 介入不入片。
- [x] 完成 brief、research、claims、video.json、script.md、verify-1.md；最新版盲讀 r9 通過 13/13，見 blind-9.md。
- [ ] 跑 lint、敘事盲讀與文件測試，寫下交接。

## How to verify

`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s23`；`node tools/video/cli.mjs narrative --slug curio-s23`；`npm run test:docs-videos`；`npm run check:tasks`。逐句與固定的原始史料對照。

## Notes

- 與其他集共用分支 `codex/curio-s34-endurance-20261019`，本票只改 `docs/videos/curio-s23`，不動題庫或其他集。
- 最新劇本 hash `c07c8d03a8969aa9`：79 句、77 張靜圖、lint 0 錯誤／0 警告。獨立逐句來源覆核與後續增補抽查見 `verify-1.md`。r7 在較早稿 `f9ce606978455200` 通過 13/13；依其核准合成的第一版旁白實長 7:56，故加入兩個有史料增量的鏡頭。r8 在 hash `f9188104f5456564` 評 12/13，唯一阻礙是 `hs073`／`hs074` 重述。現稿已將 `hs074` 改為新獎無法倒推舊獎實付額；r9 在目前 hash 通過 13/13。只重合成三句、其餘 75 段語音沿用快取，**旁白實長 8:12**。`check-audio` 進行中；新圖仍未開畫，待語音清潔後報整集 77 張插圖上限。
- 固定來源：1765 年《5 Geo. III c.20》、Harrison 1767 年《Remarks》、1773 年《13 Geo. III c.77》，網址與 OCR 限制見 `research.md`。沒有讀到 H4 原始航海日誌、Maskelyne 原版全文或王室介入原件；旁白沒有寫入這些未核細節。
