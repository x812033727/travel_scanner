---
id: 2026-10-24-music-loop
title: 新影片的生成配樂比成片短時沒有出路：music --loop 要先有組好的成片，組片又要配樂
status: review
priority: P1
area: tools
owner: claude-opus-5-5-music-loop
claimed_at: 2026-10-24T08:28:28Z
created_at: 2026-10-24T08:15:00Z
completed_at:
branch: claude/hungry-nobel-8bb756
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

- [x] 新影片的生成配樂比成片短、但 ≥ `MIN_LOOP_SECONDS` 時，有一條不花錢、經過檢查的路讓它循環：`music --loop` 不再要求先組片，成片長度一律取 `speech_hash` 對得上的 `timeline.json`，循環紀錄多記 `basis`（`assembled_cut`／`timeline`）與 `decided_by`；新增檢查 manifest 是為現在的配樂設定買的（`requested_mix_hash ?? mix_hash`）。`loopCovers` 沒改，照舊在換檔、長度不同或成片變長時失效。
- [x] 決定：免關卡的漫劇作品由檢查決定，`music` 這一步自己記錄（`decided_by: "hands_off"`），限至少 30 秒、最多播兩次（`HANDS_OFF_MAX_PLAYS`）；品牌故事（`kind: "story"`）、長篇動畫（照網站 `hands_off_series` 排除）、關卡開著的作品、沒有 `series.json` 的影片仍由站主跑 `--loop`。寫在 `docs/videos/ILLUSTRATED.md` §配樂與音效。
- [x] 測試涵蓋：沒組片、時間軸對得上 → 寫入循環紀錄；時間軸過期、配樂設定不符或配樂太短 → 拒絕不寫入；之後 `musicInputs` 接受、成片變長又擋；免關卡自己記、重跑保留、播三次停下等站主；品牌故事不自己記。
- [ ] e001 用這條路解開（工人或站主跑一次），往成片走。**等站主部署**；部署後 e001 在後台重試 `music` 即可（播兩次，免關卡會自己記），不用重買。

## Steps

- [x] 讀 #1797（`core/music-loop.mjs`、`media/music.mjs` 的 `--loop`、`assemble/sound.mjs` 的 `musicInputs`、`core/state.mjs`）與 #1669 的安全規則，確認「組片前循環」不會放過任何長度下限。
- [x] 實作、測試（`node --test tools/video/assemble/music-loop.test.mjs` 7 項全過，需要 FFmpeg）。沒改 `state.mjs`／`sound.mjs`，不需要時長收據增量（`node tools/video/long-form/cli.mjs check` PASS）。
- [x] 開 PR；部署由站主決定。

## How to verify

e001 的工人 log 出現 music 完成、組片；`music/manifest.json` 有 `loop` 紀錄。

## Notes

- 發現於票 2026-10-24-bug-1-4。e001 的配樂檔 `music/492fc5d7b55364a4.mp3` 已付費留存，不要重買。
- 2026-10-24 認領用了 `--force`：範圍與兩張票重疊——`2026-10-23-explicit-checked-loop-for-a-generated`（#1797 已合併，只剩主機上的 A4 工作）與 `2026-10-04-fault-checks-for-the-drama-judges`（只重疊 `ILLUSTRATED.md`，#1791 已合併；這張只改 §配樂與音效）。這張票原本只在 #1798 的分支上（commit 2e14cfb3a），摘過來才能認領。
- 為什麼舊的「先組片」檢查拿掉而不是另開一條路：混音一律照時間軸剪配樂（`-t <成片秒數>`、`atrim`），#1797 的循環紀錄本來就用 `timeline.total_frames / FPS` 當成片秒數，`checks.json` 只證明「已經有一支這樣混過的成片」。留著它，新影片會在「用舊設定組過一次、配樂設定又改了」的時候再卡一次同樣的死結。
- 順手修的：之前重跑 `music` 會把 manifest 整個重寫、洗掉 `loop`，讓有循環紀錄的影片又被擋；現在同一個檔、同一個長度、成片沒變長就保留。
- 免關卡旗標讀集的 `series.json`（`series.hands_off`，開集時的快照）。工人自己的狀態檔 `auto.json` 的 `series.hands_off` 不含單支（one-off），`series.json` 的會照作品列寫；單支作品建立時不是免關卡；網站的 `hands_off_series`（`settings.py`）只看作品列的 `hands_off`，排除長篇動畫與 planning-only（後者開不了集），這裡照同樣的排除。
