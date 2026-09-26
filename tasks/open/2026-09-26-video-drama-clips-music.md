---
id: 2026-09-26-video-drama-clips-music
title: Video drama T5: clips (image-to-video with QC and retakes) and music stages
status: open
priority: P1
area: tools
owner:
claimed_at:
created_at: 2026-09-26T01:53:36Z
completed_at:
branch:
depends_on:
  - 2026-09-26-video-drama-media-client
  - 2026-09-26-video-drama-look-keyframes
scope:
  - tools/video/media/clips.mjs
  - tools/video/media/music.mjs
  - tools/video/media/clips.test.mjs
---

# Video drama T5: clips (image-to-video with QC and retakes) and music stages

## Why

片段是最貴的一步（一支 3 分鐘約 US$35–110），所以放在 look 核准、旁白、關鍵影格、render 都過之後，而且每段都要過自動品檢：時長、解析度、黑格、凍格、模型自己切鏡、第 0 格對關鍵影格的 PSNR、視覺模型評分；不過就換 seed 重做，最多 2 次；每次送出前用帳本對單支上限把關。音樂由 Lyria 生成（或站主給檔）。

## Definition of done

- [ ] `clips --slug S`：需要現行 `timeline.json` 與 `keyframes/manifest.json`；依 `start_frame.shot` 拓撲排序，接續鏡頭用上一鏡最後一格（`PUT files` 上傳後引用）；`duration_s = clamp(ceil(frames/30), 4, 10)` 對齊伺服器允許值；輪詢可續跑；下載驗 sha256；QC 全套（`media/qc.mjs`）；重做上限；`clips/manifest.json` 帶 `clips_hash`、每鏡 `qc` 與 `fit_plan`。
- [ ] 送出前 `ledger.total_usd + take_cost > max_usd_per_video` 就結束碼 3；`--dry-run` 印每鏡秒數、單價、估計、伺服器本月剩餘。
- [ ] `music --slug S`：`music.prompt` → 伺服器生成 ≥ 影片長度的曲子到 `music/`（快取鍵含提示詞與長度），`music.track` → 核對 `_music/` 檔案的 sha256；寫 `music/manifest.json`（`mix_hash`）。
- [ ] 測試用假 fetch 與假 ffmpeg 輸出：拓撲順序、對齊秒數、QC 判定、重做、預算擋、續跑。

## Steps

- [ ] `media/clips.mjs`（請求、輪詢、下載、QC、重做、帳本）→ `media/music.mjs` → 測試。

## How to verify

```bash
node --test tools/video/media/clips.test.mjs
node tools/video/cli.mjs clips --slug <SLUG> --dry-run
node tools/video/cli.mjs clips --slug <SLUG> --shot <第一個鏡頭>   # 第一次先單獨跑一鏡，確認主機地區不被 Gemini 擋
```

## Notes

設計全文在 `docs/videos/DRAMA.md`（跟 T1 一起合併）；供應商、價格、政策的研究依據也在那裡。 主機在歐洲時 Gemini 的部分影片功能不開放；第一鏡被擋就把 `clip_provider` 改成 minimax，並把結果記回 DRAMA.md。
