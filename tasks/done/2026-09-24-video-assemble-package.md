---
id: 2026-09-24-video-assemble-package
title: 影片產線 T4：ffmpeg 合成、審看頁與上傳包
status: done
priority: P2
area: tools
owner: claude-opus-5-5
claimed_at: 2026-09-24T03:08:01Z
created_at: 2026-09-24T00:41:03Z
completed_at: 2026-09-24T03:27:58Z
branch: claude/video-assemble
depends_on:
  - 2026-09-24-video-tooling-core
scope:
  - tools/video/assemble
  - tools/video/review
  - tools/video/package
  - .github/workflows/video-tooling.yml
  - tools/video/core/stages.mjs
---

# 影片產線 T4：ffmpeg 合成、審看頁與上傳包

## Why

把畫面與旁白組成符合 YouTube 建議的 MP4（H.264 High、bt709、closed GOP、2 個 B 幀、faststart；AAC-LC 立體聲 48 kHz 384 kbps；響度 −14 LUFS／−1 dBTP），並產出站主審看用的頁面與上傳包。ffmpeg 用 `winget install BtbN.FFmpeg.GPL`（原生 arm64，含 libx264），路徑由 `FFMPEG_PATH` 指定。設計全文在 `docs/videos/DESIGN.md`（T1 一起合併）；skill 是 `.agents/skills/youtube-video/`。

## Definition of done

- [x] `assemble` 產生 `final.mp4` 並自動檢查，結果寫進 `checks.json`。檢查項目：
  - 影格數（`nb_read_packets`）等於時間軸總格數。
  - H.264 High、1920×1080、30 fps、yuv420p、BT.709 三項標記都在。
  - AAC-LC 立體聲 48 kHz，音軌與影片長度差 ≤ 1 格。
  - 響度在 −14 ±1 LUFS、峰值 ≤ −0.5 dBFS。
  - **每個場景的第一、第二與最後一格**按格號和來源 PNG 比對，PSNR ≥ 40 dB。
- [x] 每場景一段、設定一致、`-c copy` 串接；改一個場景只重編那一段（依內容與編碼設定雜湊快取，舊片段自動清掉）。
- [x] `review` 產生兩個頁面：
  - 審聽頁：每句的文字、唸法、音檔、「唸錯」勾選與備註，匯出的 `flags.json` 帶時間軸版本。
  - 成片審看頁：影片、章節、每一句，點了會跳過去，播放時會標出目前這句。
- [x] `package` 產生 `upload/`：
  - 內容：mp4、縮圖、各語系 SRT、各語系 `description.<locale>.txt`、`metadata.json`（帶 `final_sha256`）、`UPLOAD.md` 檢查表。
  - 站主沒核准、或核准後 `final.mp4` 改過，就以結束碼 3 拒絕。
  - 說明欄超過 YouTube 位元組上限時，以結束碼 1 拒絕。
- [x] `.github/workflows/video-tooling.yml`（路徑過濾）：裝 Chromium 與 apt 的 ffmpeg，跑純函式測試，再用範例影片跑完整的 render → assemble → review → package。

## Steps

- [x] `tools/video/assemble/`：
  - `ffmpeg.mjs`：依序找 `FFMPEG_PATH`、PATH、winget 的安裝資料夾，必須有 libx264。
  - `plan.mjs`：純函式，負責版面、concat 清單、所有 ffmpeg 參數、輸出解析與檢查。
  - `cli.mjs`、`synthetic.mjs`（替身旁白）、`smoke.mjs`。
- [x] `tools/video/review/`：兩個審看頁（靜態 HTML，不連外，直接從磁碟開）。
- [x] `tools/video/package/`：組出各語系中繼資料、`UPLOAD.md`。
- [x] `tools/video/core/stages.mjs`：`runCaptions` 接受 `--file`，給範例影片用。
- [x] CI workflow（action 用 SHA 釘版）。

## How to verify

```bash
npm run test:tools
node tools/video/assemble/smoke.mjs --workdir <dir> --channel msedge   # Windows 本機；CI 不帶 --channel
```

## Notes

- **本機 ffmpeg**：`winget install BtbN.FFmpeg.GPL`，版本 N-125875-g5d4d3bdc61-20260731，原生 ARM64，SHA256 `4FBD8C3D57188AE4AB0F91D02883CE83F774AFB294D824E098A10C02AC6995AD`。
  - 裝完後，已經開著的 shell 看不到新的 PATH，所以 `locateFfmpeg` 會直接去 winget 的資料夾找。
- **試跑時自動檢查抓到三個真問題**，都已修好：
  1. concat 讀 PNG 預設用 1/25 秒的時間基準，1/30 秒的長度落在 40 ms 的格子上，fps 濾鏡就會丟格、補格。總格數仍然正確，但內容錯位。每個檔案加上 `option framerate 30` 修正。
  2. PNG 影格沒有色彩資訊，x264 只寫了矩陣，原色與轉換曲線是 unknown。濾鏡鏈最後加 `setparams`，並加 `-x264-params colorprim/transfer/colormatrix` 修正。
  3. 單聲道先正規化再複製成立體聲，EBU R128 會加總兩個聲道，結果多 3 LU（實測 −10.9 LUFS）。改成先轉立體聲再正規化，兩段都這樣做，之後量到 −13.9 LUFS。
- **不要用時間跳轉抽格**：在串接後的檔案上，`-ss` 跳轉拿到的格子不可靠，有時是別的格，會讓正確的影片被判失敗。所以改在每個場景的片段上用 `select=eq(n,N)` 按格號抽。片段以 `-c copy` 串接，內容不會改變，所以驗證片段就等於驗證成片。正確的格子約 46–48 dB，錯一格的在 34 dB 以下，門檻設 40。
- **實測（範例影片，41.6 秒，3 個場景）**：畫面 35 秒（Edge）；三段編碼共 11 秒，快取全中時 6 秒；自動檢查含在內。
- **`assemble` 不要求先核准旁白**，這樣站主可以先看成片；要求核准的是 `package`（成片）和之後的 `youtube-sync`。
