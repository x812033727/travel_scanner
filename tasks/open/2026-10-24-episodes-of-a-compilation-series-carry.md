---
id: 2026-10-24-episodes-of-a-compilation-series-carry
title: 合集作品的每一集不放頻道片頭片尾，只有合集放：站主 10-24「一集一集做，每集不用片頭片尾，合集先合再加片頭片尾、分章節」
status: review
priority: P2
area: tools
owner: claude-fable
claimed_at: 2026-10-24T15:54:58Z
created_at: 2026-10-24T15:30:00Z
completed_at:
branch: claude/interesting-cerf-519b43
depends_on: []
scope:
  - tools/video/core/branding.mjs
  - tools/video/core/branding.test.mjs
  - docs/videos/BINGE.md
  - docs/videos/BRANDING.md
---

# 合集作品的每一集不放頻道片頭片尾，只有合集放

## Why

站主 2026-10-24：「一集一集製作，但每一集就不用放片頭跟片尾；用一個合集把所有的先合再一起加片頭片尾，合集分章節就好，我每次看合集就好。」

現況：`compile/cli.mjs` 已經這樣做——每集用留存的 `build/body.mp4`（去掉片頭片尾的本體），整部合集只包一次頻道片頭（5 秒）與片尾（21 秒結束畫面），每集前一張 2 秒章節卡、最後一張 4 秒 outro 卡，YouTube 章節一集一個。所以合集的形狀不用改。

但每一集自己的 `final.mp4` 仍帶片頭片尾：`core/branding.mjs` 的 `selectBrandingForBuild` 對長片一律套預設品牌包（`assemble/cli.mjs` 有傳 `series: project.series`，但沒看 `compilation`）。e001 的成片 308 秒＝172 秒本體＋26 秒品牌，站主在成片審核看到的是帶片頭片尾的版本，720p 預覽與審核檔案區也多存 26 秒，每集多跑一次品牌串接。

## Definition of done

- [x] `series.json` 的 `compilation` 為真、而且不是合集影片本身（`isCompilation(doc)` 為假）的集：`selectBrandingForBuild` 回 null，成片＝本體；`checks.json` 沒有 `branding`，`compile` 走「沒有 branding 就用 final」那條（已存在）。
- [x] 合集影片、單集漫劇、品牌故事、教學片、解說的品牌行為不變。
- [x] 已經做好的集（e001–e004）不重做；它們的 body 已留存，compile 照舊用 body。
- [x] BINGE.md §合集寫明：集沒有頻道片頭片尾，合集包一次。

## Steps

- [x] `branding.mjs selectBrandingForBuild`：在 `LONG_FORMATS` 檢查之後加 `if (series?.compilation && !isCompilation(doc)) return null`；`--adopt-branding` 對這種集也拒絕（adoptionRefusal 加一句）。
- [x] 測試：合集作品的集 → null；合集本身 → 預設品牌；單集 → 預設品牌。
- [x] 時長收據增量（改到 core 檔）。

## How to verify

e005 起（部署後組的集）`checks.json` 沒有 `branding`、成片秒數＝timeline；`compile --dry-run` 印 `branding <id>: one intro and outro around the complete body`、每集沒有 intro_frames。

## Notes

- 合集的章節卡要不要留：參考片（花影、桃桃）都沒有卡，但站主只說「分章節就好」，`chapter_cards` 預設 true 先保留；要關就在合集 video.json 的 `compilation.chapter_cards: false`。
- 發現於票 2026-10-24-bug-1-4。
- 2026-10-25 claude-fable：認領用了 `--force`，因為 `2026-10-04-fault-checks-for-the-drama-judges`（claude-fable-5.1-elated-lamarr，10-23 認領）的範圍也列了 `docs/videos/BINGE.md`；那條分支不在 origin 上，這裡只在 §合集加一段，合併時若衝突以兩段都留為準。
- 做法：`episodeOfCompilation(doc, series)` ＝ `series?.compilation === true && !isCompilation(doc)`，放在 `LONG_FORMATS` 檢查之後、**讀 pin 之前**：e001–e004 的工作區已有 `branding.json`，若日後 `--force` 重組也不會把片頭片尾帶回來。`adoptionRefusal` 與 `replacementRefusal` 多收 `series`，對這種集回同一句拒絕；`compile/cli.mjs` 呼叫時不傳 series，合集影片本身不受影響（`isCompilation` 為真）。
- `compile` 已能混用：沒有 `checks.branding` 的集直接用 `final.mp4`（核准雜湊），有的照舊用 `build/body.mp4`。沒改 compile。
- 範圍多加 `docs/videos/BRANDING.md`（片頭位置表多一列）。
- PR：https://github.com/x812033727/travel_scanner/pull/1835（2026-10-25）。
