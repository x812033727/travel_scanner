---
id: 2026-09-24-video-tool-pairing
title: 影片工具在後台按允許就配對，不必複製權杖
status: in-progress
priority: P1
area: api
owner: claude-opus-5-5
claimed_at: 2026-09-24T04:27:55Z
created_at: 2026-09-24T04:27:47Z
completed_at:
branch: claude/video-pairing
depends_on: []
scope:
  - apps/api/app/video_speech
  - apps/api/tests/test_video_pairing.py
  - apps/web/app/api/video/pairings
  - apps/web/components/video-tool-tokens.tsx
  - apps/web/components/video-tool-tokens.test.tsx
  - apps/web/messages/zh-TW/admin.json
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - apps/web/messages/zh-CN/admin.json
  - tools/video/tts
  - tools/video/cli.mjs
  - docs/videos/DESIGN.md
---

# 影片工具在後台按允許就配對，不必複製權杖

## Why

影片產線的本機工具要一組「影片工具權杖」，才能請正式站用後台存的 Azure 金鑰合成旁白（#709）。原本的做法是：站主在後台建立權杖、複製，再在自己的終端機執行 `login` 貼上。

這一步卡住了。代理不能經手權杖，而站主不熟終端機，2026-09-24 甚至把權杖貼進了和代理的對話裡（那一組要撤銷）。站主的要求是「應該要在網站可以存然後你可以用」，所以選了「網站按允許的配對」：誰跑 `login` 都可以，站主只要在後台按一次「允許」，權杖由伺服器直接交給本機程式，不經過任何人的眼睛。

## Definition of done

- [x] `node tools/video/cli.mjs login` 印出驗證碼和後台卡片的連結，等站主按「允許」後把權杖存進 `~/.mokaair/video-tool.json`；權杖從不印出。
- [x] 後台「Azure 語音（影片旁白）」卡有「配對本機工具」：從連結進來會自動帶入驗證碼，並顯示電腦名稱、來源 IP、時間，提醒只允許自己剛剛看到的驗證碼。
- [x] 拒絕、過期（10 分鐘）、重複領取都拿不到權杖；權杖數達上限時不能允許。
- [x] 明文權杖不落地：Redis 只存配對狀態，權杖在工具來領時才產生，`GETDEL` 保證只領一次。
- [x] 允許、拒絕、產生權杖都寫進稽核紀錄。
- [ ] 部署後，由代理在本機跑 `login`，站主按「允許」，`tts --dry-run` 讀得到本月用量。

## Steps

- [x] API：`app/video_speech/pairing.py`（Redis 流程）與 `admin_api.py` 的五個端點（開配對、輪詢；後台查詢、允許、拒絕）。
- [x] Web：`/api/video/pairings` 與 `/api/video/pairings/poll` 轉送（不帶 cookie、帶來源位址）；權杖卡片的配對區塊與五語系文字。
- [x] 本機：`login` 預設走配對；`--paste`、`--token-file` 保留。
- [x] 測試：API 8 項、Web 路由 3 項與卡片 4 項、本機 3 項。
- [ ] 合併、部署、實際配對一次。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_video_pairing.py tests/test_video_speech.py
cd apps/web && npx vitest run app/api/video components/video-tool-tokens.test.tsx
node --test tools/video/tts/tts.test.mjs
node tools/video/cli.mjs login        # 部署後：站主在後台按「允許」
```

## Notes

- 後台連結用 `/zh-TW/admin/settings?provider=azure_speech&video_pairing=<code>`。`provider` 參數讓設定頁直接打開 Azure 語音卡，不用新增後台頁面（新後台頁要改四處，見記憶 guides-admin-visibility）。
- 驗證碼只用 20 個子音字母、8 碼（不會拼出單字，也沒有 0/O、1/I 的混淆）。開配對以來源 IP 限制每小時 10 次，輪詢以 device code 限制每分鐘 30 次。
- 釣魚風險：別人可以開一個配對，再傳連結給站主。對策是卡片上顯示電腦名稱、IP 和時間，並提醒「只允許你自己剛剛在終端機上看到的驗證碼」。和 RFC 8628 的做法相同。
- `check:i18n` 在 `CI=1` 時比對 `HEAD^..HEAD`。CI 是淺層 clone，拿不到 `HEAD^`，所以那邊等於沒檢查。本機在分支還沒有自己的 commit 時跑，會把上一個合併（#709）的中文字串報出來，這不是這張票造成的。新的轉送路由錯誤訊息是給本機工具讀的，所以寫英文。
