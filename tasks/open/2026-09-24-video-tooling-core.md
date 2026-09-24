---
id: 2026-09-24-video-tooling-core
title: 影片產線 T1：tools/video 核心（schema、lint、時間軸、字幕、狀態）
status: in-progress
priority: P2
area: tools
owner: claude-opus-5-5
claimed_at: 2026-09-24T00:43:30Z
created_at: 2026-09-24T00:41:01Z
completed_at:
branch: claude/youtube-tutorial-video-workflow-b12539
depends_on: []
scope:
  - tools/video/cli.mjs
  - tools/video/core
  - package.json
  - package-lock.json
  - docs/videos/DESIGN.md
---

# 影片產線 T1：tools/video 核心（schema、lint、時間軸、字幕、狀態）

## Why

站主要一條全自動的 YouTube 教學影片產線：AI 撰稿 → 查核 → Azure 台灣口音 TTS → Mokaair 深色投影片畫面 → ffmpeg 合成 → 五語系 CC → 在 Studio 上傳成私人、API 補上五語系中繼資料與 CC（2026-09-24 決定，形式參考 Gary Chen 的投影片＋旁白解說片，不燒錄字幕）。repo 裡原本沒有任何影片、TTS、字幕或上傳程式。設計全文在 `docs/videos/DESIGN.md`（T1 一起合併）；skill 是 `.agents/skills/youtube-video/`。

這張是地基：`video.json` 的格式、檢查、時間軸與畫格換算、字幕檔、狀態檔與站主核准紀錄。其他工具票（T2–T4、T7–T11）都依賴它。

## Definition of done

- [x] `node tools/video/cli.mjs lint --file tools/video/core/fixtures/minimal/video.json` 零錯誤零警告；寫壞的稿子（測試裡十幾種）錯誤訊息都指出場景與句子 id。
- [x] `node tools/video/cli.mjs status --slug <slug> --workdir <dir>` 列出 12 步的清單並印出下一個該跑的指令；還沒做的子指令印出負責的票並以結束碼 5 結束。
- [x] 時間軸：每句音檔加句後停頓補靜音到整格（48 kHz／30 fps，一格 1,600 取樣），所以根本沒有捨入；單元測試用 2,000 句隨機長度證明每句都從 `start_frame × 1600` 開始、總長剛好是總格數。
- [x] 字幕由時間軸產生（zh-TW＋任何翻譯完整且沒過期的語系），SRT／WebVTT 可讀回；章節檢查照 YouTube 規則（第一個 00:00、至少 3 個、每段 ≥10 秒）。
- [x] `npm run test:tools` 會跑 `tools/video/**/*.test.mjs`：158 項全綠（其中 video 71 項），都是純函式或暫存目錄，不需要 Chromium 或 ffmpeg。

## Steps

- [x] `docs/videos/DESIGN.md`：設計全文，含 2026-09-24 查的 YouTube／Azure 官方規則與工作區檔案約定。
- [x] `tools/video/core/schema.mjs`：`video.json` 驗證（未知欄位也算錯，擋錯字）。
- [x] `tools/video/core/lexicon.mjs`：發音字典；`GPT-5.5` 這類組合字由各部分判斷。
- [x] `tools/video/core/lint.mjs`：句長、書面語（與 `video_kit.py` 同一份清單）、查證過程進旁白、網址、括號、發音字典、`say` 過期、reveal 超過項目數、YouTube 上限（說明以**組好之後**的位元組算）、章節、長度、`brief.md` 必填兩節、過期翻譯、版型序列和其他支太像。
- [x] `tools/video/core/timeline.mjs`：畫格網格、狀態（reveal）、章節、`speechHash`／`visualHash`。
- [x] `tools/video/core/captions.mjs`：分段、換行、時間分配、SRT／WebVTT、讀回、檢查。
- [x] `tools/video/core/paths.mjs`、`state.mjs`、`approvals.mjs`、`stages.mjs`：工作區、原子寫入、STOP、狀態、核准綁 SHA-256、`captions` 階段。
- [x] `tools/video/cli.mjs`：`status`、`lint`、`ids`、`approve`、`captions`；媒體階段延遲載入 `tools/video/<area>/cli.mjs`。
- [x] 根目錄 `package.json`：`test:tools` 加 `"tools/video/**/*.test.mjs"`（加引號讓 Node 自己展開，Linux 的 sh 不認 `**`）；devDependencies 加 `@fontsource-variable/noto-sans-tc`、`@fontsource-variable/jetbrains-mono`（OFL，可變字型版，合計約 4.8 MB；靜態版的 Noto Sans TC 有 68 MB）。

## How to verify

```bash
npm run test:tools
node tools/video/cli.mjs lint --file tools/video/core/fixtures/minimal/video.json
node tools/video/cli.mjs render --slug x          # exit 5，印出負責的票
```

## Notes

- 範例在 `tools/video/core/fixtures/`：`minimal/video.json`、`minimal/brief.md`、`lexicon.json`，`fixtures/load.mjs` 另外提供建假 repo 用的 `sandbox()`。發音字典與「其他影片」一律從 `video.json` 所在目錄的上一層找，所以正式影片用 `docs/videos/lexicon.json`，範例用 fixtures 的那份。
- 結束碼 3（需要站主）目前沒有核心指令會回：擋在核准之後的是 `package`、`youtube-sync`，它們要用 `approvalState()` 檢查並回 3。
- 中文字幕每行 16 字、每段兩行（常見字幕規範）；一句 32 字以內是一段，斷行優先在逗號，兩半都放得下時才用，否則斷在中間。英文等語系的數字是起始值，T7 調。
- `package-lock.json` 是手動插入兩個字型套件的 22 行：本機 npm 11.6.2 的 `--package-lock-only` 會順手刪掉其他套件的 `libc` 欄位（CI 在 Linux 靠它分 glibc／musl），所以沒有用它的輸出。
- 字型只寫進 lockfile；這個 worktree 沒有 `node_modules`（依賴從主 checkout 解析）。T3 開工前在自己的 worktree 跑 `npm ci`。
- 中文參數一律改用檔案：PowerShell 5.1 會弄壞非 ASCII 的命令列參數。
