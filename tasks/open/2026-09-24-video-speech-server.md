---
id: 2026-09-24-video-speech-server
title: 影片旁白：後台 Azure 語音卡、伺服器代為合成、影片工具權杖
status: in-progress
priority: P2
area: api
owner: claude-opus-5-5
claimed_at: 2026-09-24T02:00:00Z
created_at: 2026-09-24T02:00:00Z
completed_at:
branch: claude/video-speech-server
depends_on: []
scope:
  - apps/api/app/video_speech
  - apps/api/app/models.py
  - apps/api/app/config.py
  - apps/api/app/admin/service.py
  - apps/api/app/providers/usage_meter.py
  - apps/api/app/main.py
  - apps/api/migrations/versions/0085_video_tool_tokens.py
  - apps/api/tests/test_video_speech.py
  - apps/api/tests/test_admin_provider_settings.py
  - apps/web/app/api/video
  - apps/web/components/admin-settings-panel.tsx
  - apps/web/components/admin-settings-panel.test.tsx
  - apps/web/components/video-tool-tokens.tsx
  - apps/web/components/video-tool-tokens.test.tsx
  - apps/web/messages/zh-TW/admin.json
  - apps/web/messages/zh-CN/admin.json
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - .env.example
  - docs/videos/DESIGN.md
---

# 影片旁白：後台 Azure 語音卡、伺服器代為合成、影片工具權杖

## Why

全自動 YouTube 影片產線（`docs/videos/DESIGN.md`）的旁白用 Azure AI Speech。原本的設計是站主在本機設環境變數 `AZURE_SPEECH_KEY`／`AZURE_SPEECH_REGION`。2026-09-24 站主要求改成「在網站後台輸入」，並從三個選項中選了「後台存金鑰，伺服器代為合成」：

- 金鑰只存在正式站的加密供應商設定，永遠不離開伺服器。
- 本機的影片工具帶著「影片工具權杖」送句子過去，伺服器呼叫 Azure 後把音檔傳回。
- 另外兩個選項沒選：本機工具自己的設定頁（不在後台）、讓工具從伺服器讀回金鑰（會開一個讀出秘密的口，後台的金鑰目前都是只能寫、不能讀回）。

限制與因應：

- 正式站只對外開放 Next.js（`ops/nginx/mokaair.conf.example`）。現有的 `/api/travel` 代理會丟掉 `Authorization`、而且把回應當文字解碼，WAV 會壞。所以仿照 `apps/web/app/api/line/webhook/route.ts` 另開專用路由。
- Azure 每個中文字算兩個計費字元，SSML 標記也計費。預算要以字元計，現有的用量計數器每次只能加 1。

## Definition of done

- [x] 後台「API 與供應商設定 → AI 服務」有「Azure 語音（影片旁白）」卡：金鑰（加密、遮罩）、區域、允許的聲音、每月計費字元上限、逾時；連線測試會列出該區域的聲音，並確認白名單裡的聲音都存在；卡上有本月計費字元用量。
- [x] 同一張卡上可以建立影片工具權杖（只顯示一次、可複製）、列出（只顯示開頭）、撤銷（要點兩次）；建立與撤銷都記在稽核紀錄。
- [x] `POST /api/video/speech`（網頁路由轉給 `POST /api/v1/video/speech`）：
  - 收結構化的句子（文字、唸法替換、句後停頓），由伺服器組 SSML。
  - 驗證權杖；聲音必須在白名單內；每次最多 1,500 字。
  - 先向每月預算預留計費字元，Azure 拒絕就退回。
  - 回傳 48 kHz 16-bit mono WAV，附 `X-Billable-Characters`。
- [x] `GET /api/video/speech/status`：回傳是否已設定、允許的聲音、上限與本月用量，給本機工具的 `--dry-run` 用。
- [ ] 部署到正式站後，站主在後台填好金鑰、連線測試通過、建立一組權杖（要站主同意部署）。

## Steps

- [x] `apps/api/app/video_speech/`：`ssml.py`（組 SSML、計費字元）、`azure.py`（合成、列出聲音）、`tokens.py`（產生、雜湊、驗證）、`schemas.py`、`admin_api.py`（兩個 router）。
- [x] `VideoToolToken` 模型與遷移 `0085_video_tool_tokens`（只存 SHA-256，撤銷只寫時間戳）。
- [x] `config.py`：`azure_speech_*` 欄位。區域同時用 before-validator 和 pattern 檢查，因為主機名稱由區域組成；空字串視為「未設定」，所以 `.env.example` 的空值不會讓 API 起不來。
- [x] `usage_meter.py`：`reserve_azure_speech_characters`（一次預留 N 個字元，超過預算就拒絕，Redis 失敗時也拒絕）、`release_…`、`azure_speech_usage_snapshot`（以 UTC 按月）。
- [x] `admin/service.py`：卡片定義、區域與聲音的欄位檢查、就緒狀態、連線測試、用量、稽核動作篩選。
- [x] 網頁：`apps/web/app/api/video/speech/`（只轉送 `Bearer mkv_…` 權杖，從不轉 cookie）、`video-tool-tokens.tsx`、設定面板接線（分類、欄位、秘密欄位、用量面板加上「計費字元」單位）、五語系字串。
- [x] 測試：API 16 項、網頁 3 個檔。

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run pytest tests/test_video_speech.py tests/test_admin_provider_settings.py tests/test_error_localization.py -q
npm run lint:web && npm run check:i18n && npm run typecheck:web
npx vitest run --root apps/web components/video-tool-tokens.test.tsx app/api/video/speech/route.test.ts components/admin-settings-panel.test.tsx
```

部署後（站主同意）：後台 → API 與供應商設定 → AI 服務 → Azure 語音。填金鑰與區域、儲存、按連線測試，然後建立一組權杖。

## Notes

- **權限**：權杖管理的端點放在 `/admin/provider-settings/azure_speech/video-tool-tokens`，所以 `_admin_path_capability` 已經套用 `settings.read`／`settings.manage`，沒有改動 `auth/service.py`。
- **錯誤代碼翻譯**：語音端點只給站主的本機工具用，屬於後台端點。AppError 都寫在 `video_speech/admin_api.py`（路徑含 `admin`），`test_error_localization` 就把它們當作不需五語系翻譯的後台錯誤。
- **為什麼不讓工具送 SSML**：伺服器能完整控制送出的內容（不會有 `<audio src>` 之類連外的元素），計費字元也能從伺服器自己組的字串精確算出。
- **一次最多 1,500 字**：48 kHz PCM 每分鐘約 5.8 MB，1,500 字大約 5.5 分鐘、32 MB。較長的場景由 T2 的本機工具拆開送。
- **速率限制**：每組權杖每分鐘 120 次；每位管理員每小時最多建立 10 組權杖；同時有效的權杖最多 10 組。
- **T2（`2026-09-24-video-tts-azure`）要改的地方**：
  - 不再直接呼叫 Azure，改送 `POST {site}/api/video/speech`，body 是 `{voice, rate, segments:[{parts:[{text, alias?}], break_after_ms}]}`。
  - 權杖用 `cli.mjs login` 存在工作區的 `.secrets/`。
  - 字數與費用估計用 `GET /api/video/speech/status`。
