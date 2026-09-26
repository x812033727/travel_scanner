---
id: 2026-09-26-video-dubs-check-language
title: Video dubs: transcribe in the dub's language so check-audio can judge en, ja, ko and zh-CN tracks
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-09-26T17:58:54Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/video_speech
  - apps/api/tests/test_video_speech_check.py
  - tools/video/tts/check.mjs
  - tools/video/tts/client.mjs
  - tools/video/tts/check.test.mjs
---

# Video dubs: transcribe in the dub's language so check-audio can judge en, ja, ko and zh-CN tracks

## Why

`check-audio` 是站主交給 Jev 的旁白品管：伺服器逐句轉寫，工具比對稿子，不同的交給 Jev。轉寫提示寫死了「台灣國語、繁體字」（`apps/api/app/video_speech/checking.py`），拼音同音與語助詞兩條規則也只對中文有意義。配音音軌（`docs/videos/DUBS.md`）是英、日、韓、簡中，用現在的檢查會把每一句都判成不同。這張票讓轉寫知道語言，讓 `check-audio` 能對 `dubs/<locale>/` 的音檔做同一套檢查。

## Definition of done

- [ ] `TranscribeIn` 多一個選填的 `language`，只收 zh-TW、en、ja、ko、zh-CN，預設 zh-TW；其他值 422。
- [ ] 轉寫提示依語言：zh-TW 照現在；zh-CN 是簡體字；en、ja、ko 是「逐字轉寫成該語言」；英文詞的提示清單（`terms`）每種語言都照傳。
- [ ] Jev 的 `state.language` 跟著語言走（現在寫死 `"zh-TW"`）。
- [ ] `check-audio --locale L`：讀 `dubs/<locale>/audio/*.wav` 與 `dubs/<locale>/timeline.json`，比對 `i18n/<locale>.json` 的句子（口語形式只套全拉丁字母的別名，和 `dub` 一致）；轉寫快取與旗標檔各語系分開（`review/check.<locale>.json`、`review/check-flags.<locale>.json`），旗標檔的形狀是 `dub --redo` 能直接吃的。
- [ ] 拼音「同音」規則與語助詞規則只在 zh-TW、zh-CN 用；en 比對前小寫、去標點；ja、ko 做 NFKC、去空白與標點，其餘交給 Jev。
- [ ] `recordStage` 的 `check-audio` 記錄帶 `locale`，不覆蓋 zh-TW 那一筆。
- [ ] 兩側測試：伺服器每種語言的提示與 422；工具的 `--locale` 解析、各語系的 comparable、檔名。

## Steps

- [ ] `schemas.py`、`checking.py`、`admin_api.py`：語言欄位、提示、Jev 的 state。
- [ ] `client.mjs` 的 `transcribeClip` 帶 `language`。
- [ ] `check.mjs`：`--locale`、來源目錄、比對規則、檔名、記錄。
- [ ] 測試；`cd apps/api && uv run ruff check . && uv run mypy app && uv run mypy tests`。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_video_speech_check.py
npm run test:tools
node tools/video/cli.mjs check-audio --slug chatgpt-ads-upgrade --locale en
```

## Notes

- Jev 只讀文字，文件上的準確度是英文的；日文轉寫常把數字、假名寫法正規化，預期 Jev 的呼叫會比中文多，門檻先不動（`DEFAULT_THRESHOLD`）。
- `JudgeLineIn.intended` 上限 400 字元；英文句子平均 50 字元左右，但要防超長句（截斷並記錄，不要 422 整批）。
- 這張不依賴 `video-dubs-command`：沒有 `dubs/` 目錄時 `--locale` 印「先跑 dub」結束碼 2 即可，測試用假目錄。
