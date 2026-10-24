---
id: 2026-10-24-music-loop
title: 新影片的生成配樂比成片短時沒有出路：music --loop 要先有組好的成片，組片又要配樂
status: open
priority: P1
area: tools
owner:
claimed_at:
created_at: 2026-10-24T08:15:00Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/media/music.mjs
  - tools/video/core/music-loop.mjs
  - tools/video/assemble/music-loop.test.mjs
  - docs/videos/ILLUSTRATED.md
---

# 新影片的生成配樂比成片短時沒有出路：music --loop 要先有組好的成片，組片又要配樂

## Why

《系統說我是 BUG》第 1 集（`xitong-shuo-wo-shi-bug-e001`）2026-10-24 08:03Z 分鏡核准、畫面與片段做完後，卡在配樂：「music needs the owner: decoded track is shorter than the 171.833 s cut. Keep this paid file; arrange an explicit checked loop or another licensed track.」生成配樂（Gemini lyria-3.5）要了 177 秒，完整解碼只有 164.8 秒。

#1797 加的 `music --slug <slug> --loop` 是為已上架影片的配音做的：它要求「a current cut was assembled with these music settings」（`tools/video/media/music.mjs` 約 106 行），否則拒絕「assemble first」。新影片的組片又要先有配樂（`assemble/sound.mjs` 的 `musicInputs` 拒絕比成片短、沒有循環紀錄的配樂），所以新影片只剩「另一首授權音樂」一條路，工人只能停下來等站主。漫劇一集 130–175 秒，生成配樂常比要的短，這會一集一集重複。

## Definition of done

- [ ] 新影片的生成配樂比成片短、但 ≥ `MIN_LOOP_SECONDS` 時，有一條不花錢、經過檢查的路讓它循環：例如 `music --loop` 在還沒組片時改用 `timeline.json`（`speech_hash` 對得上）的長度當成片長度、並記下這是組片前的決定；`loopCovers` 照舊在換檔或成片變長時失效。
- [ ] 決定這一步是站主的指令還是工人在免關卡作品上可以自己做（BINGE.md：免關卡＝由檢查決定）；寫進 `docs/videos/ILLUSTRATED.md` §配樂與音效。
- [ ] 測試涵蓋：沒組片、時間軸對得上 → 寫入循環紀錄；時間軸過期或配樂太短 → 拒絕不寫入；之後 `musicInputs` 接受。
- [ ] e001 用這條路解開（工人或站主跑一次），往成片走。

## Steps

- [ ] 讀 #1797（`core/music-loop.mjs`、`media/music.mjs` 的 `--loop`、`assemble/sound.mjs` 的 `musicInputs`、`core/state.mjs`）與 #1669 的安全規則，確認「組片前循環」不會放過任何長度下限。
- [ ] 實作、測試（`node --test tools/video/assemble/music-loop.test.mjs` 等，需要 FFmpeg）、時長收據增量（改到 state.mjs／sound.mjs 時，見 docs 的收據規則）。
- [ ] 開 PR；部署由站主決定。

## How to verify

e001 的工人 log 出現 music 完成、組片；`music/manifest.json` 有 `loop` 紀錄。

## Notes

- 發現於票 2026-10-24-bug-1-4。e001 的配樂檔 `music/492fc5d7b55364a4.mp3` 已付費留存，不要重買。
