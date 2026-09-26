---
id: 2026-09-26-video-drama-clips-music
title: Video drama T5: clips (image-to-video with QC and retakes) and music stages
status: done
priority: P1
area: tools
owner: claude-fable-5-1-video-drama
claimed_at: 2026-09-26T06:46:09Z
created_at: 2026-09-26T01:53:36Z
completed_at: 2026-09-26T06:55:49Z
branch:
depends_on:
  - 2026-09-26-video-drama-media-client
  - 2026-09-26-video-drama-look-keyframes
scope:
  - tools/video/media/clips.mjs
  - tools/video/media/music.mjs
  - tools/video/media/clips.test.mjs
  - tools/video/media/stages.mjs
---

# Video drama T5: clips (image-to-video with QC and retakes) and music stages

## Why

片段是最貴的一步（一支 3 分鐘約 US$35–110），所以放在 look 核准、旁白、關鍵影格、render 都過之後，而且每段都要過自動品檢：時長、解析度、黑格、凍格、模型自己切鏡、第 0 格對關鍵影格的 PSNR、視覺模型評分；不過就換 seed 重做，最多 2 次；每次送出前用帳本對單支上限把關。音樂由 Lyria 生成（或站主給檔）。

## Definition of done

- [x] `clips --slug S`：需要現行 `timeline.json`、`keyframes/manifest.json`（全過）與已核准的 storyboard；文件順序就是拓撲順序（lint 只允許接續更早的鏡），接續鏡頭把上一鏡最後一格（ffmpeg 抽出、`PUT files` 上傳）當 `previous_frame` 參考；`duration_s = clamp(ceil(frames/30), 4, 10)` 往上取到模型允許值；輪詢可續跑；下載驗 sha256；QC 全套（`media/qc.mjs`＋judge）；重做上限 2；`clips/manifest.json` 帶 `clips_hash`、每鏡 `qc`、`takes`、`first_frame`、`continues`（fit 由 assemble 自己量，不寫 `fit_plan`）。
- [x] 送出前 `ledger.total_usd + take_cost > max_usd_per_video` 就結束碼 3（`Stage.spend`）；`--dry-run` 印每鏡秒數、單價、估計、伺服器本月剩餘片段秒。
- [x] `music --slug S`：`music.prompt` → 伺服器生成影片長度＋5 秒的曲子到 `music/`（快取鍵含提示詞與長度），`music.track` → 核對 `_music/` 檔案的 sha256；寫 `music/manifest.json`（`mix_hash`）。
- [x] 測試用假 fetch 與假 ffmpeg 輸出（`ctx.clipQc`／`ctx.extractFrame`／`ctx.makeProxy`）：順序、對齊秒數、QC 判定、重做、judge 太大走 proxy、帳本、續跑（快取）、STOP、music 兩種來源。

## Steps

- [x] `media/stages.mjs` 通用化 → `media/clips.mjs`（請求、輪詢、下載、QC、重做、帳本）→ `media/music.mjs` → 測試。

## How to verify

```bash
node --test tools/video/media/clips.test.mjs
node tools/video/cli.mjs clips --slug <SLUG> --dry-run
node tools/video/cli.mjs clips --slug <SLUG> --shot <第一個鏡頭>   # 第一次先單獨跑一鏡，確認主機地區不被 Gemini 擋
```

## Notes

設計全文在 `docs/videos/DRAMA.md`（跟 T1 一起合併）；供應商、價格、政策的研究依據也在那裡。 主機在歐洲時 Gemini 的部分影片功能不開放；第一鏡被擋就把 `clip_provider` 改成 minimax，並把結果記回 DRAMA.md。

2026-09-26 做法（claude-fable-5-1-video-drama）：

- `media/stages.mjs` 的 `Stage.generate()` 通用化（image／clip／music 共用快取、續跑、帳本、上限），`Stage.clip()`／`Stage.music()`；片段等最多 30 分鐘。
- `clips` 的前提：timeline 是現行的、`keyframes/manifest.json` 現行且要做的鏡都通過、**storyboard 已核准**（`approve --gate storyboard` 或站上核准／自動核准）。每鏡：秒數＝`clipSeconds(句子格數, 模型允許的秒數)`（4–10，往上取到模型有的秒數；再長由 assemble 的 fit 補），`first_frame`＝關鍵影格（每次跑都 `putFile` 回媒體庫），`last_frame`＝`end_frame` 圖（有的話），參考圖＝選定設定圖（role character）＋上一鏡最後一格（role `previous_frame`，只在 `start_frame.shot` 時，由 ffmpeg 抽 `clips/<prev>-last.png`），提示詞＝`motion. camera. look.motion`，negative＝`look.negative`，seed＝take 次數，`idempotency_key`＝`clipKey`。
- **接續鏡頭的第 0 格仍是自己的關鍵影格**（上一鏡最後一格只當參考），所以 assemble（T7）拿關鍵影格比第 0 格的 PSNR 仍成立；真正「從上一格接下去」要等供應商支援，屆時要同時改 T7 的比對來源。
- QC：ffmpeg（probe、blackdetect、freezedetect、切鏡、第 0 格對關鍵影格與相鄰關鍵影格的 PSNR）＋ judge（rubric：每角色最後一格 identity、motion、prompt、clean、no_text）→ `clipVerdict`；judge 回 413 `video_media_judge_too_large` 就做 720p proxy 上傳再判。不過就換 seed，最多 `MAX_CLIP_TAKES = 2`（`--takes` 可調）；仍不過 `needs_review` 進 manifest、結束碼 1。測試用 `ctx.clipQc`／`ctx.extractFrame`／`ctx.makeProxy` 取代 ffmpeg。
- `clips/manifest.json`：`{ speech_hash, visual_hash, look_hash, clips_hash（依鏡頭順序的 clipsHash）, clip: {provider, model, resolution}, shots[<id>]: { file, sha256, key, seed, seconds, frames, needed_s, first_frame, end_frame?, continues?, qc, judge, takes, needs_review, problems? } }`，正是 T7 讀的形狀。
- `music`：`track` → 核對 `<工作目錄底>/_music/<track>`（與 `music.sha256`）並寫 `{ mix_hash, source: "track", track, sha256 }`；`prompt` → 秒數＝影片長度＋5（10–600），`mediaKey("music", …)` 快取，寫 `{ mix_hash, source: "generated", file, sha256, seconds }`（T7 讀 `file`）。
