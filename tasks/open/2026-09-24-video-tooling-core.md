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

- [ ] `node tools/video/cli.mjs lint --slug <slug>` 對範例 `video.json` 零錯誤，對故意寫壞的範例指出場景與句子 id。
- [ ] `node tools/video/cli.mjs status --slug <slug> --workdir <dir>` 印出下一個該跑的指令；還沒做的子指令印「not built yet」並以固定結束碼結束。
- [ ] 時間軸換算在 48 kHz／30 fps 下以絕對時間取整，單元測試證明 2,000 段不會累積漂移。
- [ ] zh-TW SRT 由時間軸產生；章節清單符合 YouTube 規則（第一個 0:00、至少 3 個、每段 ≥10 秒）。
- [ ] `npm run test:tools` 會跑 `tools/video/**/*.test.mjs`，全綠；全是純函式測試，不需要 Chromium 或 ffmpeg。

## Steps

- [ ] `docs/videos/DESIGN.md`：設計全文。
- [ ] `tools/video/core/schema.mjs`：`video.json` 驗證（schema_version、場景、句子 id 唯一且穩定、`say`／`say_for`、`reveal`、youtube 欄位、assets）。
- [ ] `tools/video/core/lint.mjs`：句長、禁用說法、拉丁字詞要在發音字典或白名單、`say` 過期、YouTube 上限（標題 100 字元、說明 5,000 位元組、標籤 500 字元、不含 `<` `>`）、估計總長、`brief.md` 必填欄。
- [ ] `tools/video/core/timeline.mjs`：畫格網格、停頓、字幕分段（依唸出來的長度加權）、章節。
- [ ] `tools/video/core/captions.mjs`：SRT／WebVTT 輸出與解析。
- [ ] `tools/video/core/state.mjs`、`approvals.mjs`、`paths.mjs`：狀態檔、STOP 檔、原子寫入、核准綁雜湊、工作區不得在 repo 內。
- [ ] `tools/video/cli.mjs`：子指令分派、結束碼（1 lint、3 需要站主、4 外部服務或額度、5 缺工具）。
- [ ] 根目錄 `package.json` 的 `test:tools` 加 `tools/video/**/*.test.mjs`；devDependencies 加字型套件。

## How to verify

```bash
node --test tools/video/**/*.test.mjs
npm run test:tools
node tools/video/cli.mjs lint --file tools/video/core/fixtures/minimal.video.json
```

## Notes

- 字型套件（`@fontsource` 的 Noto Sans TC 與等寬字型）在這張一起加到根目錄 devDependencies：這張持有 `package.json`，T3 就不用再動它。
- `--text` 之類的中文參數一律改用檔案：PowerShell 5.1 會弄壞非 ASCII 的命令列參數。
