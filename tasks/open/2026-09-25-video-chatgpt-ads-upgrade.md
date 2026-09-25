---
id: 2026-09-25-video-chatgpt-ads-upgrade
title: 影片：ChatGPT 開始有廣告了，免費版、Go、Plus 要不要升級
status: in-progress
priority: P2
area: docs
owner: claude-opus-5-5
claimed_at: 2026-09-25T01:23:37Z
created_at: 2026-09-25T01:22:59Z
completed_at:
branch: claude/video-batch-2
depends_on: []
scope:
  - docs/videos/chatgpt-ads-upgrade
---

# 影片：ChatGPT 開始有廣告了，免費版、Go、Plus 要不要升級

## Why

2026-09-24 熱門話題研究的第一名：ChatGPT 廣告 9 月 24 日在台灣上線（OpenAI 9/23 公告），受影響的是免費版與 Go 的使用者。站主 2026-09-25 選了這個題目與大綱 A（判斷方法框架）。企劃書在 `docs/videos/chatgpt-ads-upgrade/brief.md`，來源文章 `ai-free-vs-paid-plans-2026`。

## Definition of done

- [ ] `docs/videos/chatgpt-ads-upgrade/` 有 `brief.md`、`video.json`、`claims.md`、`verify-1.md`（必要時 `verify-2.md`），`lint` 零錯誤。
- [ ] 旁白通過 `check-audio`，站主核准旁白、看完成片（`approvals.json` 三筆，雜湊與成品一致）。
- [ ] 站主在 Studio 上傳成私人，影片 ID 寫回 `video.json`。

## Steps

- [x] 企劃代理寫 brief，站主選大綱（2026-09-25，選項 A）。
- [ ] 撰稿（sonnet）→ 查核（opus，換人）→ 聽眾優先審稿。新詞列在 `lexicon-additions.json`，由協調者併進共用字典。
- [ ] tts → check-audio → 核准旁白 → render → assemble → CC → package。
- [ ] 站主截一張 ChatGPT「設定 → 廣告控制」的畫面，存成 `docs/videos/chatgpt-ads-upgrade/screenshot-ad-controls.png`（代理不登入站主帳號）。
- [ ] Go 與 Plus 的台灣台幣價格，只有登入後的結帳頁看得到；片中以美元官方價換算，並標示為「估計」。

## How to verify

```bash
node tools/video/cli.mjs lint --slug chatgpt-ads-upgrade
node tools/video/cli.mjs status --slug chatgpt-ads-upgrade
```

## Notes

- 2026-09-25 claude-opus-5-5 認領；分支 `claude/video-batch-2`，疊在試作片分支 `claude/video-pilot-audio` 上（要用它的 `docs/videos/lexicon.json`）。
