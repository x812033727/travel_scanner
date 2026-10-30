---
id: 2026-10-30-three-brand-stories-move-to-curio
title: Twenty-two brand stories move to the curio W axis and are remade under the new rules
status: in-progress
priority: P2
area: ops
owner: claude-opus-5-5-curio-w-axis
claimed_at: 2026-10-30T19:47:23Z
created_at: 2026-10-30T18:06:50Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/curio-w01-dolby-licensing
  - docs/videos/curio-w02-michelin-guide-stars
  - docs/videos/curio-w03-garmin-smartphone-pivot
  - docs/videos/history-curiosity/brand-files-remake-20261031/codex-stop-and-abandon.md
  - docs/videos/history-curiosity/brand-files-remake-20261031/w01-w03-handoff.md
  - docs/videos/history-curiosity/topic-checks/W01.md
  - docs/videos/history-curiosity/topic-checks/W02.md
  - docs/videos/history-curiosity/topic-checks/W03.md
---

# Twenty-two brand stories move to the curio W axis and are remade under the new rules

## Why

站主 2026-10-31 要把杜比、米其林、Garmin 三支品牌故事移到奇聞檔案局，並依現行規則重製；同一天擴大成「重作的原本在品牌故事就都變成奇聞檔案局」，共 22 支，都不燒字幕。題目、規則差異、路線與預算在
`docs/videos/history-curiosity/brand-files-remake-20261031/README.md`；要站主決定的放棄清單與 Codex 停工說明在同資料夾的 `codex-stop-and-abandon.md`。

這張票的 `scope` 只管 W01–W03。W04 起每一批開自己的票，一批最多 5 支，**站主答覆放棄清單前不開工**。

## 其餘 19 支的代號與順序

代號照站主給的順序。slug 是預定的，開工時可改。舊企劃與查核只當來源，收據綁舊內容，新稿要重查。

| 批 | 代號 | 預定 slug | 題目 | 舊 slug |
| --- | --- | --- | --- | --- |
| 2 | W04 | `curio-w04-doraemon-after-fujiko` | 哆啦A夢 | `story-adapt-doraemon-after-fujiko-remake-20261025` |
| 2 | W05 | `curio-w05-seiko-quartz-astron` | Seiko | `story-adapt-seiko-quartz-astron-remake-20261025` |
| 2 | W06 | `curio-w06-dyson-japan-first` | Dyson | `story-dyson-japan-first-20261021-remake-20261025` |
| 2 | W07 | `curio-w07-bubble-wrap` | Bubble Wrap | `story-everyday-bubble-wrap-c04-remake-20261025` |
| 2 | W08 | `curio-w08-camelbak` | CamelBak | `story-everyday-camelbak-c14-remake-20261025` |
| 3 | W09 | `curio-w09-dr-martens` | Dr. Martens | `story-everyday-dr-martens-c07-remake-20261025` |
| 3 | W10 | `curio-w10-frixion` | FriXion | `story-everyday-frixion-c15-remake-20261025` |
| 3 | W11 | `curio-w11-kikkoman` | 龜甲萬 | `story-everyday-kikkoman-c08-remake-20261025` |
| 3 | W12 | `curio-w12-kincho` | 金鳥 | `story-everyday-kincho-c05-remake-20261025` |
| 3 | W13 | `curio-w13-moleskine` | Moleskine | `story-everyday-moleskine-c03-remake-20261025` |
| 4 | W14 | `curio-w14-oxo` | OXO | `story-everyday-oxo-c10-remake-20261025` |
| 4 | W15 | `curio-w15-patagonia` | Patagonia | `story-everyday-patagonia-c09-remake-20261025` |
| 4 | W16 | `curio-w16-play-doh` | Play-Doh | `story-everyday-play-doh-c06-remake-20261025` |
| 4 | W17 | `curio-w17-seven-bank` | Seven Bank | `story-everyday-seven-bank-c19-remake-20261025` |
| 4 | W18 | `curio-w18-ucc` | UCC | `story-everyday-ucc-c11-remake-20261025` |
| 5 | W19 | `curio-w19-zippo` | Zippo | `story-everyday-zippo-c20-remake-20261025` |
| 5 | W20 | `curio-w20-a4-paper-size` | A4 紙 | `story-adapt-a4-paper-size` |
| 5 | W21 | `curio-w21-pringles-vat-case` | 品客 | `story-five-pringles-vat-case` |
| 5 | W22 | `curio-w22-lego-legoland` | 樂高 | `story-five-lego-legoland` |

## Definition of done

- [ ] `curio-w01`、`curio-w02`、`curio-w03` 三集成片經站主核准，類別是 `explainer`，標題結尾是「｜奇聞檔案局」，`subtitles.burn_in` 是 false。
- [ ] 舊的三支 `story-` 影片已處理：沒上架的放棄，已上架的照站主決定。

## Steps

- [x] 讀舊片在網站上的狀態，放棄清單與 Codex 停工說明交給站主（`codex-stop-and-abandon.md`）。
- [ ] 站主答覆放棄清單。
- [x] 每集 brief 與大綱（各寫一個，站主還沒選過）。
- [x] 稿子 → 獨立查核 → 盲評 → lint 0 錯誤（W01 七輪、W02 十一輪、W03 七輪）。
- [x] `--dry-run` 報價（`w01-w03-handoff.md`）。
- [ ] 站主核准預算與五個決定。
- [ ] 旁白 → 站主聽 → 插圖 → 分鏡 → 配樂 → 成片 → 品管 → 上架包。
- [ ] 新片核准後處理舊片；Garmin 舊片不再解卡做語言。

## How to verify

`node tools/video/cli.mjs lint --slug curio-w01-dolby-licensing`（w02、w03 同樣）0 錯誤；`/admin/videos` 三集成片為已核准。

## Notes

- 後台 2026-10-31 讀到：杜比（uv-CQOKDMOI）、米其林（BSsyQ8HAVVg）、Garmin 舊片都已放棄；杜比、米其林沒有 remake，Garmin 有尚未開始的 `story-garmin-smartphone-pivot-worker-2026-remake-20261025`，W03 開工前要先處理，避免重複。
- 不走主機後台路線：主機單集的 slug 是 `one-off-…`，lint 與備份的系列判斷都靠 `curio-` slug；`MYSTERY` 也不認 W 軸。
- 查核收據綁舊企劃的雜湊，新稿要重查。Dolby 2026 財年 10-K 預計 2026 年 11 月公布。
- 2026-10-31 W01–W03 稿子、查核、盲評、lint 都完成，**沒有任何付費生成**。報價與要站主決定的事在 `docs/videos/history-curiosity/brand-files-remake-20261031/w01-w03-handoff.md`：插圖一輪合計 US$4.34，三輪上限 US$13.00（比計畫的 US$9.5 高），配樂約 US$0.45，旁白 9,744 字元。下一個接手的人從那份文件和各集 `NOTES.md` 開始。
- 這張票的工作疊在分支 `claude/video-reclassify-rules-44b738` 上（它帶來這張票與 `README.md`）。
- 2026-10-31 查到：Codex 分支 2026-10-26 10:00 UTC 後沒有推送，PR #1849 draft；後台 17 支 remake 還沒放棄，其中 Seiko、哆啦A夢、Dyson、Garmin 不受 `story-everyday-` 擋板管。
