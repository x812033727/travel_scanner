---
id: 2026-10-24-episodes-of-a-compilation-series-carry
title: 合集作品的每一集不放頻道片頭片尾，只有合集放：站主 10-24「一集一集做，每集不用片頭片尾，合集先合再加片頭片尾、分章節」
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-24T15:30:00Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/core/branding.mjs
  - tools/video/core/branding.test.mjs
  - docs/videos/BINGE.md
---

# 合集作品的每一集不放頻道片頭片尾，只有合集放

## Why

站主 2026-10-24：「一集一集製作，但每一集就不用放片頭跟片尾；用一個合集把所有的先合再一起加片頭片尾，合集分章節就好，我每次看合集就好。」

現況：`compile/cli.mjs` 已經這樣做——每集用留存的 `build/body.mp4`（去掉片頭片尾的本體），整部合集只包一次頻道片頭（5 秒）與片尾（21 秒結束畫面），每集前一張 2 秒章節卡、最後一張 4 秒 outro 卡，YouTube 章節一集一個。所以合集的形狀不用改。

但每一集自己的 `final.mp4` 仍帶片頭片尾：`core/branding.mjs` 的 `selectBrandingForBuild` 對長片一律套預設品牌包（`assemble/cli.mjs` 有傳 `series: project.series`，但沒看 `compilation`）。e001 的成片 308 秒＝172 秒本體＋26 秒品牌，站主在成片審核看到的是帶片頭片尾的版本，720p 預覽與審核檔案區也多存 26 秒，每集多跑一次品牌串接。

## Definition of done

- [ ] `series.json` 的 `compilation` 為真、而且不是合集影片本身（`isCompilation(doc)` 為假）的集：`selectBrandingForBuild` 回 null，成片＝本體；`checks.json` 沒有 `branding`，`compile` 走「沒有 branding 就用 final」那條（已存在）。
- [ ] 合集影片、單集漫劇、品牌故事、教學片、解說的品牌行為不變。
- [ ] 已經做好的集（e001–e004）不重做；它們的 body 已留存，compile 照舊用 body。
- [ ] BINGE.md §合集寫明：集沒有頻道片頭片尾，合集包一次。

## Steps

- [ ] `branding.mjs selectBrandingForBuild`：在 `LONG_FORMATS` 檢查之後加 `if (series?.compilation && !isCompilation(doc)) return null`；`--adopt-branding` 對這種集也拒絕（adoptionRefusal 加一句）。
- [ ] 測試：合集作品的集 → null；合集本身 → 預設品牌；單集 → 預設品牌。
- [ ] 時長收據增量（改到 core 檔）。

## How to verify

e005 起（部署後組的集）`checks.json` 沒有 `branding`、成片秒數＝timeline；`compile --dry-run` 印 `branding <id>: one intro and outro around the complete body`、每集沒有 intro_frames。

## Notes

- 合集的章節卡要不要留：參考片（花影、桃桃）都沒有卡，但站主只說「分章節就好」，`chapter_cards` 預設 true 先保留；要關就在合集 video.json 的 `compilation.chapter_cards: false`。
- 發現於票 2026-10-24-bug-1-4。
