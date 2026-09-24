---
id: 2026-09-24-video-assemble-package
title: 影片產線 T4：ffmpeg 合成、審看頁與上傳包
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-09-24T00:41:03Z
completed_at:
branch:
depends_on:
  - 2026-09-24-video-tooling-core
scope:
  - tools/video/assemble
  - tools/video/review
  - tools/video/package
  - .github/workflows/video-tooling.yml
---

# 影片產線 T4：ffmpeg 合成、審看頁與上傳包

## Why

把畫面與旁白組成符合 YouTube 建議的 MP4（H.264 High、bt709、closed GOP、2 個 B 幀、faststart；AAC-LC 立體聲 48 kHz 384 kbps；響度 −14 LUFS／−1 dBTP），並產出站主審看用的頁面與上傳包。ffmpeg 用 `winget install BtbN.FFmpeg.GPL`（原生 arm64，含 libx264），路徑由 `FFMPEG_PATH` 指定。設計全文在 `docs/videos/DESIGN.md`（T1 一起合併）；skill 是 `.agents/skills/youtube-video/`。

## Definition of done

- [ ] `assemble` 產生 `final.mp4`，並自動檢查：`nb_frames` 等於時間軸總格數、音軌與影片差 ≤ 1 格、每章開頭抽格與來源 PNG 的 PSNR 夠高、響度在目標 ±1 LU。
- [ ] 每場景一段、設定一致、`-c copy` 串接；改一個場景只重編那一段。
- [ ] `review` 產生審聽頁（每句文字＋音檔＋「唸錯」勾選，匯出 `flags.json`）與成片審看頁（字幕點選跳轉）。
- [ ] `package` 產生 `upload/`：mp4、縮圖、SRT、`metadata.json`、`UPLOAD.md` 檢查表；站主沒核准或 `final.mp4` 雜湊不符時拒絕。
- [ ] `.github/workflows/video-tooling.yml`（路徑過濾，仿 `.github/workflows/article-localization.yml`）跑 5 秒的 render＋assemble 煙霧測試。

## Steps

- [ ] `tools/video/assemble/`：concat 清單（最後一個 file 重複）、ffmpeg 參數組裝（純函式＋測試）、兩段式 loudnorm、影音自動檢查。
- [ ] `tools/video/review/`：兩個審看頁（靜態 HTML，不連外）。
- [ ] `tools/video/package/`：上傳包與 `UPLOAD.md`（含 AI 揭露判斷標準、非原創內容政策的自我檢查）。
- [ ] CI 煙霧測試 workflow（action 要用 SHA 釘版，`tools/workflow-pins.test.mjs` 會檢查）。

## How to verify

```bash
node --test tools/video/assemble/*.test.mjs
node tools/video/cli.mjs assemble --slug <slug> --workdir <VIDEO_WORKDIR>
```

## Notes

- 不用 Playwright 附帶的 ffmpeg（只有 VP8），也不用 `ffmpeg-static`。
- 裝 ffmpeg 前要先問站主（下載檔名、來源、大小）。
