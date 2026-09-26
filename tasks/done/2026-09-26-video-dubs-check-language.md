---
id: 2026-09-26-video-dubs-check-language
title: Video dubs: transcribe in the dub's language so check-audio can judge en, ja, ko and zh-CN tracks
status: done
priority: P2
area: api
owner: claude-fable-5-1-video-dubs-check
claimed_at: 2026-09-26T18:23:49Z
created_at: 2026-09-26T17:58:54Z
completed_at: 2026-09-26T19:48:02Z
branch: claude/video-dubs-check-language
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

- [x] `TranscribeIn` 多一個選填的 `language`，只收 zh-TW、en、ja、ko、zh-CN，預設 zh-TW；其他值 422。
- [x] 轉寫提示依語言：zh-TW 照現在；zh-CN 是簡體字；en、ja、ko 是「逐字轉寫成該語言」；英文詞的提示清單（`terms`）每種語言都照傳。
- [x] Jev 的 `state.language` 跟著語言走（現在寫死 `"zh-TW"`）。
- [x] `check-audio --locale L`：讀 `dubs/<locale>/audio/*.wav` 與 `dubs/<locale>/timeline.json`，比對 `i18n/<locale>.json` 的句子（口語形式只套全拉丁字母的別名，和 `dub` 一致）；轉寫快取與旗標檔各語系分開（`review/check.<locale>.json`、`review/check-flags.<locale>.json`），旗標檔的形狀是 `dub --redo` 能直接吃的。
- [x] 拼音「同音」規則與語助詞規則只在 zh-TW、zh-CN 用；en 比對前小寫、去標點；ja、ko 做 NFKC、去空白與標點，其餘交給 Jev。
- [x] `recordStage` 的 `check-audio` 記錄帶 `locale`，不覆蓋 zh-TW 那一筆。
- [x] 兩側測試：伺服器每種語言的提示與 422；工具的 `--locale` 解析、各語系的 comparable、檔名。

## Steps

- [x] `schemas.py`、`checking.py`、`admin_api.py`：語言欄位、提示、Jev 的 state。
- [x] `client.mjs` 的 `transcribeClip` 帶 `language`。
- [x] `check.mjs`：`--locale`、來源目錄、比對規則、檔名、記錄。
- [x] 測試；`cd apps/api && uv run ruff check . && uv run mypy app && uv run mypy tests`。

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
- 2026-09-27 claude-fable-5-1-video-dubs-check 做完，決定與沒做的：
  - 伺服器：`TrackLanguage` Literal 在 `schemas.py`；`TranscribeIn.language` 與 `JudgeIn.language` 都收（Jev 的 state 要知道語言，所以 judge 端點也帶，工具的 `judgeLines` 一樣只在不是 zh-TW 時送）。提示表 `TRANSCRIBE_INSTRUCTIONS_BY_LANGUAGE` 與 `transcribe_instructions()` 在 `checking.py`。en、ja、ko 的提示不要求「數字照唸法寫」：翻譯稿寫阿拉伯數字，轉寫也寫數字最容易直接相等，不同的交給 Jev（Jev 的提示本來就忽略數字寫法）；zh-CN 照 zh-TW 的規則。`TERMS_HINT` 的「而不是同音的中文字」依語言換成 kana、Hangul、other words。
  - 工具：`transcribeClip`、`judgeLines` 只在 locale 不是 zh-TW 時帶 `language`（舊伺服器 `extra="forbid"`）。來源目錄在 `trackFiles()`，快取與旗標在 `checkFiles()`；旗標檔多 `locale` 與 `translation_hash`（從 timeline 抄），`flags` 形狀不變。
  - 英文配音的提示詞只給字典裡的詞（`hintTerms(line, { locale: "en", lexicon })`）：整句都是拉丁字母，否則前 20 個字都會被當成提示。ja、ko、zh-CN 照 zh-TW 的規則給句子裡所有拉丁字。
  - 別名過濾 `dubLexicon()`：含 Han、kana、Hangul 的別名不用（`p95 → P 九十五` 照原字唸），註解標明鏡射 `tools/video/dubs/` 的規則；`video-dubs-command` 落地後對一次兩邊是否一致。
  - 語助詞集合加了簡體 诶、馁 給 zh-CN；pinyin-pro 對簡體字同樣算得出讀音（測試有 级联／吉莲）。
  - 超過 400 字元的句子送 Jev 前截斷（`fit()`，以 code point 計，和 pydantic 一樣），輸出列出被截的句子；沒有 422 整批。
  - 沒動 `tools/video/cli.mjs` 的 HELP（不在 scope）：`check-audio` 那行還沒寫 `--locale`，`video-dubs-command` 改 cli.mjs 時順手補。`ARTIFACTS` 也沒有 dubs 的路徑，`dub` 落地後可以把 `trackFiles()` 改成讀它。
  - 沒驗證 `timeline.translation_hash` 是否等於現在的翻譯檔（雜湊怎麼算是 `dub` 那張定的）；翻譯改了沒重錄的話，check-audio 只會看到句子不同而交給 Jev。
  - Windows 本機：`npm run test:tools` 偶爾在 `atomicWrite` 的 rename 撞 EPERM（一輪 4 個 media 測試、一次 check.test 的 dub 測試），是已開的票 `2026-09-26-atomicwrite-fails-on-windows-when-the`，重跑就過；`uv run mypy tests` 在 Windows 報 `tests/support/e2e_deploy_agent.py` 的 `UnixStreamServer`，與這張無關。
  - `node tools/video/cli.mjs check-audio --slug chatgpt-ads-upgrade --locale en` 沒跑：這個 checkout 沒有 `docs/videos/chatgpt-ads-upgrade/`，也還沒有 dub 產物；`dub` 落地後在主機上跑。
