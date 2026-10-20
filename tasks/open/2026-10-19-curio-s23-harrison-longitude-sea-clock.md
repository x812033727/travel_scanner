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
- [x] 獨立史料覆核與最新版盲讀故事關卡通過，lint 零錯誤；旁白 79/79 句通過 `check-audio`、正文超過 8 分鐘，插圖已取得整集上限報價。
- [ ] 完成 77 張插圖、配樂、組片、字幕及成片品管。

## Steps

- [x] 檢查 S23 無其他認領或 PR，建立窄 scope。
- [x] 固定可讀的 1765 年法案對 1714 年經度獎的追述、1773 年法案及 Harrison 1767 年當事人紀錄；核對 H4 航試與獎金，未有原件支持的 George III 介入不入片。
- [x] 完成 brief、research、claims、video.json、script.md、verify-1.md；最新版盲讀 r10 通過 13/13，見 blind-10.md。
- [x] 跑 lint、敘事盲讀與文件測試，寫下交接。
- [x] 完成旁白重錄、語音品管、旁白審核紀錄及插圖估價。
- [ ] 完成媒體製作與最終品管。

## How to verify

`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s23`；`node tools/video/cli.mjs narrative --slug curio-s23`；`npm run test:docs-videos`；`npm run check:tasks`。逐句與固定的原始史料對照。

## Notes

- 與其他集共用分支 `codex/curio-s34-endurance-20261019`，本票只改 `docs/videos/curio-s23`，不動題庫或其他集。
- 最新劇本 hash `f6be3017488b475d`：79 句、77 張靜圖，lint 0 錯誤／0 警告。獨立逐句來源覆核與後續增補抽查見 `verify-1.md`。r7 在較早稿 `f9ce606978455200` 通過 13/13；第一版旁白實長 7:56，故加入兩個有史料增量的鏡頭。r8 在 hash `f9188104f5456564` 評 12/13，唯一阻礙是 `hs073`／`hs074` 重述；r9 在 `c07c8d03a8969aa9` 通過 13/13，該版合成後正文 8:02.67、全片 8:12.97。語音檢查首輪標出 20 句，重錄後減至 11 句；現稿只把這 11 句改成史料同義、易辨的說法，增量來源見 `verify-1.md`，**r10 在現稿通過 13/13**。
- 最新合成與重錄完成後，`check-audio` 查核 79/79 句、0 句標記；正文 486.47 秒（8:06.47）、全片 496.77 秒（8:16.77）。已送出 audio 審核並依站主本次對話的持續製作委託記錄代理核准；紀錄明示站主未親自聆聽這一版。時間軸 SHA-256 前綴 `90c01807708c`。工作目錄 `/workspace/.video-work/curio-s23` 存有音檔與 QA 報告，未進 repo。
- `keyframes --dry-run` 報價：MiniMax image-01、1K、77 張靜圖，一次試畫約 US$1.04、全圖每張最多三試約 US$3.12。製作時採用的**整集插圖加既有配樂上限同為 US$3.12**，所以重試額度少於全圖三試；此額度在站主本次對話的廣泛委託內。2026-10-20 已生圖 223 次、圖像判定 224 次、含既有配樂累計 **US$3.1005**；77 張皆有圖，**76／77 自動判定通過**，`hs013` 因圖中多出羅馬數字鐘面仍未過，已停止付費生圖。`keyframes` 回傳失敗，分鏡、剪輯和成片關卡未啟動。獨立接觸表審查又標出 `hs039`、`hs054`、`hs071` 等年代錯置的硬阻礙；本集既有上限不足以完成所需重畫。證據與精確雜湊見 `docs/videos/curio-s23/verify-2.md`。
- 固定來源：1765 年《5 Geo. III c.20》、Harrison 1767 年《Remarks》、1773 年《13 Geo. III c.77》，網址與 OCR 限制見 `research.md`。沒有讀到 H4 原始航海日誌、Maskelyne 原版全文或王室介入原件；旁白沒有寫入這些未核細節。
