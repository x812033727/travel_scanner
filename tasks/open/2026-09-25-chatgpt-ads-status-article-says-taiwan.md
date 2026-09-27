---
id: 2026-09-25-chatgpt-ads-status-article-says-taiwan
title: chatgpt-ads-status 還寫台灣未列入廣告市場
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-09-25T06:01:28Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/guides/content/chatgpt-ads-status.json
---

# chatgpt-ads-status 還寫台灣未列入廣告市場

## Why

`chatgpt-ads-status`（2026-09-14 查證）寫台灣未列在自助可用名單中。OpenAI 2026-09-23 公告〈ChatGPT Ads expands to Southeast Asia and Taiwan〉：台灣的 Free 與 Go 會看到廣告，Plus 以上不會；Ads Manager 也開放自助。影片〈ChatGPT 開始有廣告了〉的查核（`docs/videos/chatgpt-ads-upgrade/verify-1.md`，分支 `claude/video-batch-2`）與 2026-09-24 的熱門話題研究都發現這篇過時了。

## Definition of done

- [ ] 文章寫明台灣自 2026-09-23 起列入（附官方公告網址與查證日），哪些方案會看到、18 歲以上、廣告控制在哪。
- [ ] 五語系一致（走 skill `content-pipeline`）。

## Steps

- [ ] 重查 https://openai.com/index/chatgpt-ads-expands-southeast-asia-taiwan/ 與 https://help.openai.com/en/articles/20001047-ads-in-chatgpt。
- [ ] 改寫、ingest、部署後匯入。

## How to verify

正式站 `/zh-TW/guides/chatgpt-ads-status` 顯示台灣已列入與新的查證日。

## Notes

- 公告日期：OpenAI 貼文日期 2026-09-23（RSS 為 23 日 02:00 GMT），台灣媒體寫 24 日上線；以官方為準寫 23 日公告。
