---
id: 2026-09-26-video-dubs-command
title: Video dubs: the dub command lays translated narration into the slide windows and writes the audio tracks
status: done
priority: P2
area: tools
owner: claude-fable-5-1-video-dubs
claimed_at: 2026-09-26T18:16:47Z
created_at: 2026-09-26T17:58:41Z
completed_at: 2026-09-26T19:36:29Z
branch: claude/video-dubs-command
depends_on: []
scope:
  - tools/video/dubs
  - tools/video/cli.mjs
  - tools/video/core/state.mjs
  - tools/video/i18n
---

# Video dubs: the dub command lays translated narration into the slide windows and writes the audio tracks

## Why

YouTube 的多語言音軌讓一支影片多掛幾條配音，觀眾依語言偏好自動聽到自己的語言（設計與 2026-09-27 查到的規則在 `docs/videos/DUBS.md`）。對繁中原片，YouTube 自動配音只會給英文，而且不能改；日、韓、簡中只能自己做。這張票做整個功能的核心：用同一個頻道聲音唸出字幕的翻譯，塞回 zh-TW 決定的畫面時間軸，輸出可以直接上傳的音軌。做完就能對第二批的任何一支先做一條英文音軌給站主聽，再決定要不要往下做其他票。

## Definition of done

- [x] `node tools/video/cli.mjs dub --slug S --locale L[,L] [--format m4a|mp3|wav] [--dry-run] [--redo <flags file>] [--force] [--style T] [--workdir D]` 存在，登記在 `cli.mjs` 的模組表（附這張票的 id）與 `--help`。
- [x] 前置條件與 `captions` 相同：lint 零錯誤、`timeline.json` 的 `speech_hash` 是現在這份稿子的、該語系每一句都有當前的翻譯（`source_hash` 相符）。缺句或過期就列出來，結束碼 1，不寫半條音軌。另外只收 Gemini 聲音（結束碼 3）與投影片格式（漫劇自己混音）。
- [x] 視窗與對齊照 DUBS.md：
  - 視窗 = 同一個場景、同一個投影片狀態（`timeline.scenes[].states[]`）裡的連續句子，長度取自 zh-TW 時間軸；
  - 先保留原本節奏（每句配音的開始 = max(原句開始, 上一句配音結束 + 250 ms)），塞不下再緊排（只留 250 ms 間隔）；
  - 仍超出 → 整個視窗等比例 `atempo`，從 1.01 起每 0.01 試到 1.15；實際拉完再排一次，還差就 +0.02 再拉；
  - 仍超出 → `fit.json` 列出這個視窗的句子與每句的 `max_chars`、實測秒數、視窗超出秒數，結束碼 1（其餘語系照常寫出）；
  - 每條音軌的取樣數恰等於 `timeline.total_frames × 1600`；視窗結尾留 100 ms 保護。
- [x] 合成沿用 `tts/client.mjs`、`tts/synthesis.mjs`、`tts/wav.mjs`：聲音是 `doc.voice`，style 換成該語系的預設（`tools/video/dubs/plan.mjs` 的 `DUB_STYLES`，語氣同 zh-TW 的 style、語言改掉；`--style` 可覆蓋）；發音字典只套用不含中日韓字的別名（`dubLexicon`）；每句的快取鍵 = 聲音欄位 + 那句的 parts，改一句只重錄一句；拉過速的檔 `<id>.x<tempo>.wav` 另外快取；`--redo` 吃 `check-audio` 的 flags 檔。
- [x] `--dry-run` 印字元數、Gemini 本月剩餘額度、每個語系的視窗估計（會加速幾個、塞不下幾個）；額度不夠時和 `tts` 一樣以 `video_speech_budget_exhausted` 停下。
- [x] 寫出：`dubs/<locale>/audio/<id>.wav`、`dubs/<locale>/timeline.json`（每句 `start_frame`、`end_frame`、`audio_samples`、`tempo`；`speech_hash`、`translation_hash`、`total_frames`、`format`、`file`、`voice`、`windows`）、`dubs/<locale>/fit.json`（每個視窗的倍率與餘裕、預設與量到的語速、塞不下的句子與預算）、`dubs/<locale>.m4a`（兩段式 loudnorm −14 LUFS／−1 dBTP，AAC-LC 立體聲 48 kHz 384 kbps；`--format mp3` 是 libmp3lame 320 kbps，`wav` 是 PCM 16-bit）。
- [x] `i18n-sheet` 在 `timeline.json` 存在時，每句多一個 `max_chars`（DUBS.md 的預算公式；語速先用 zh-TW 旁白實測值乘上語系倍率，該語系有 `fit.json` 就用量到的值），`note` 說明它的意思。
- [x] `status --slug S` 多印一行 dubs：每個語系 current／stale／over／skipped，全是 missing 時不印。
- [x] `state.mjs` 的 `ARTIFACTS` 加上 dubs 目錄與 `dubArtifacts(workdir, locale)`、`dubsStatus`；不加進 `SLIDES_STEPS`（配音是選配，不能讓沒開配音的影片卡在這一步）。
- [x] 單元測試（純函式加假伺服器、假 ffmpeg，不用網路）：視窗切法、保留節奏／緊排／加速／超出、預算與語速、音軌組裝、ffmpeg 參數、整條指令（en 塞得下、ko 加速、ja 超出、快取、`--redo`、`status`、`i18n-sheet` 的 `max_chars`、各種拒絕）；`npm run test:tools` 過。

## Steps

- [x] `tools/video/dubs/plan.mjs`：視窗、對齊、倍率、預算、`fit.json` 的形狀。
- [x] `tools/video/dubs/cli.mjs`：前置檢查、合成與快取、`--redo`、`--dry-run`。
- [x] `tools/video/dubs/encode.mjs`：`atempo`、loudnorm 兩段、m4a／mp3／wav。
- [x] `i18n-sheet` 的 `max_chars`；`status` 的 dubs 行；`ARTIFACTS`。
- [x] 測試；`cli.mjs` 登記與 `--help`。
- [x] 本機對第二批一支做一條英文音軌，量過長度，結果寫進 Notes（聽要站主聽）。

## How to verify

```bash
npm run test:tools
node tools/video/cli.mjs dub --slug chatgpt-ads-upgrade --locale en --dry-run
node tools/video/cli.mjs dub --slug chatgpt-ads-upgrade --locale en
ffprobe -v error -show_entries stream=codec_name,sample_rate,channels:format=duration "<workdir>/chatgpt-ads-upgrade/dubs/en.m4a"
```

音軌長度要等於 `final.mp4` 的長度（差 0 格）；`fit.json` 沒有 over 的視窗，或列出的句子都有 `max_chars`。

## Notes

- **2026-09-27 本機實測**（〈ChatGPT 廣告〉`chatgpt-ads-upgrade`，10:36，170 句，用 `--file` 指向從 `claude/video-batch-2` 取出的 video.json 與 i18n，工作區是本機既有的 `mokaair-work/videos/chatgpt-ads-upgrade`）：
  - zh-TW 旁白實測 5.80 字元／秒，說話佔時間軸 87%。翻譯字元數：en 2.66×、ja 1.27×、ko 1.48×、zh-CN 0.98×。
  - `--dry-run` 四語系共 27,445 個 Gemini 字元（en 10,261），主機額度剩 265,009。
  - en 第一輪：44 個請求、13,291 計費字元；實測英文 15.17 字元／秒（預設 15）；83 個視窗裡 57 個保留原節奏、15 個加速（1.01–1.14）、**11 個塞不下**（18 句要縮）。照 `fit.json` 的 `max_chars` 縮短 18 句（數字、名稱不動）再跑：只重錄 18 句，剩 1 個視窗塞不下（`q3-code`：三句裡兩句有 NT$ 金額，"With tax, that's about NT$268." 30 字元唸了 4.9 秒）。第三輪把金額旁邊的字再砍才過。
  - 成品 `dubs/en.m4a`：25.4 MB、AAC 48 kHz 立體聲、長度 635.700 s 與 `final.mp4` 相同、−14.0 LUFS、峰值 −0.9 dBFS；64 個視窗原節奏、19 個加速（最快 1.15）、0 個超出；英文說話佔 84%。
  - 學到的：(1) 每句有約 0.5 秒的固定起收音（英文回歸 `秒 = 0.51 + 0.055 × 字元`），預算公式已扣 `LINE_OVERHEAD_MS = 400`；(2) 數字與貨幣代碼唸得比字元數慢很多，`fit.json` 的 `over` 現在附每句實測秒數與視窗超出秒數，翻譯提示要寫「砍數字旁邊的字」；(3) 預設語速改成以 zh-TW 旁白實測值為錨（`RATE_RATIOS`），否則 dry-run 把 zh-CN 判成塞不下。
  - 還沒做：站主聽（同一個聲音 Sulafat 講英文像不像）、Studio 實測收不收 m4a（`video-dubs-captions-package` 的票）。
- 第二批的稿子與翻譯在分支 `claude/video-batch-2`（`docs/videos/chatgpt-ads-upgrade` 等）；本機工具副本要自己補 `apps/api/app/guides/content/<source_guide>.json`，否則 lint 報「no content pack」。
- 先用 `audition --text-file en.txt --voices gemini:Sulafat --style "<DUB_STYLES.en>"` 聽 Sulafat 講英文像不像；Gemini 文件說內建聲音跨語言、語言自動判斷，但沒有逐個聲音保證。不像就換一個內建聲音當「外語聲音」，記在 DUBS.md。
- `atempo` 一次 0.5–100 倍都收；整個視窗同一個倍率，不要逐句不同。
- 格式：官方頁只寫「支援的純音訊檔案格式」，第三方一致列 MP3、WAV、AAC。先出 m4a（和 `final.mp4` 同一條編碼鏈），Studio 不收才換；結果由 `video-dubs-captions-package` 寫進 skill。
- `tools/video/cli.mjs` 也在 `2026-09-26-video-hands-off-qa` 的 scope 裡：後落地的那張 rebase。
- 伺服器的 Gemini 月額度預設 300,000 字元；四條配音一支約 20,600 字元。試做前看 `--dry-run` 的剩餘額度，需要時請站主在後台調高 `video_speech_gemini_monthly_character_limit`。
