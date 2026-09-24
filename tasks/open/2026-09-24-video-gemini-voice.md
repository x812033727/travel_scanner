---
id: 2026-09-24-video-gemini-voice
title: 影片旁白加上 Gemini 語音：用網站的 Gemini 金鑰合成、可指定語氣
status: in-progress
priority: P1
area: api
owner: claude-opus-5-5
claimed_at: 2026-09-24T07:31:27Z
created_at: 2026-09-24T07:31:25Z
completed_at:
branch: claude/video-gemini
depends_on: []
scope:
  - apps/api/app/video_speech
  - apps/api/app/providers/usage_meter.py
  - apps/api/app/config.py
  - apps/api/tests/test_video_speech_gemini.py
  - tools/video/tts
  - tools/video/core/schema.mjs
  - docs/videos/DESIGN.md
---

# 影片旁白加上 Gemini 語音：用網站的 Gemini 金鑰合成、可指定語氣

## Why

2026-09-24 站主試聽了 Azure 的 7 個聲音（同一段 101 字的樣稿），最好的是 Ava（多語，講台灣國語），語速 +5%。但站主嫌它「語調太平、像在念稿」，要試更自然的聲音。

研究代理查了 Azure HD、Gemini、Google Cloud、OpenAI、ElevenLabs 五家，站主選了 Gemini 和 Google Cloud 兩條路：
- **Google Cloud 的 Gemini 語音**：官方文件只收服務帳戶，不收 API 金鑰，而且 `cmn-tw`、聲音和停頓標記都還是預覽版，所以先擱著。
- **Gemini API 的 `gemini-3.8-flash-tts`**：2026-09-22 轉正式版，可以用一句文字指定語氣，而且能用網站已經存著的 Gemini 金鑰。

在 AI Studio 直接試聽行不通：那把金鑰（名稱「hostinger」）限了伺服器的 IP，AI Studio 呼叫會拿到 403。所以只能照原本的架構，讓伺服器代為合成。

## Definition of done

- [x] `POST /video/speech` 收 `gemini:<聲音>`，另外可帶 `style` 與 `model`，用網站的 Gemini 金鑰合成，回傳 WAV。
- [x] Gemini 的月用量和 Azure 分開計，有上限，超過就用 429 拒絕、不送出；Gemini 拒絕的請求會把字數退回。
- [x] 狀態端點回報 Gemini 是否可用、30 個內建聲音、模型、本月用量。
- [x] 本機工具：`video.json` 可以寫 Gemini 聲音；`audition --voices gemini:Sulafat --style "…"` 可以用；24 kHz 升頻到 48 kHz，後續步驟不用改。
- [ ] 部署後，用同一段樣稿產生幾個 Gemini 聲音給站主，和 Ava 比較。

## Steps

- [x] API：`app/video_speech/gemini.py`、`admin_api.py` 的 Gemini 分支、`usage_meter` 加上 provider 參數、兩個 Settings。
- [x] 本機：`wav.mjs` 的 `upsample`／`toNarrationRate`、`requests.mjs` 的 `voiceFields`／`geminiText`、`cli.mjs` 的 `voiceProblem`、`schema.mjs` 的 Gemini 欄位。
- [x] 測試：API 9 項（`tests/test_video_speech_gemini.py`）、本機 6 項（`tools/video/tts/gemini.test.mjs`）。
- [ ] 合併、部署、試聽。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_video_speech_gemini.py tests/test_video_speech.py
node --test tools/video/tts/gemini.test.mjs tools/video/tts/tts.test.mjs
node tools/video/cli.mjs audition --text-file <樣稿> --voices gemini:Sulafat,gemini:Achird --style "Relaxed, conversational tech explainer…"
```

## Notes

- **停頓**：用的是 Gemini 文件寫的 `<long pause>`（800 ms 的句間停頓）與 `<short pause>`。長度沒有官方數字，第一次用整場景合成時，要看切段是否可靠。不可靠的話，現有的逐句重合成會接手。
- **沒有 `<sub alias>`**：術語的唸法直接換進文字。英文縮寫寫成「L L M」這種字母間加空格的形式，實際效果要試聽確認。
- **後台卡片還沒有 Gemini 上限的欄位**，上限只能用環境變數 `VIDEO_SPEECH_GEMINI_MONTHLY_CHARACTER_LIMIT` 調，預設 30 萬字，約 100 支 10 分鐘的片、13 美元。要讓站主在後台調，得加欄位和五語系文字，另開一張票。
- **Gemini 的聲音不用列進允許清單**：內建聲音一律允許。聲音庫或「聲音設計」產生的 `voice_…` id，只要格式對也接受。
- 付費層的資料不會拿去訓練。免費層的資料會被 Google 用來改進產品；網站的金鑰是付費專案的。
