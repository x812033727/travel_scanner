---
id: 2026-09-17-commons-non-ascii-filename-ingest
title: 非 ASCII 檔名的 Commons 圖片 ingest 不進來：UnicodeEncodeError
status: in-progress
priority: P2
area: api
owner: claude-fable-5-1
claimed_at: 2026-09-19T08:40:29Z
created_at: 2026-09-17T00:56:16Z
completed_at:
branch: claude/travel-scanner-pr-552-rpq36m
depends_on: []
scope:
  - apps/api/app/guides/pack_ingest.py
  - apps/api/tests/test_guides_content_pack.py
---

# 非 ASCII 檔名的 Commons 圖片 ingest 不進來：UnicodeEncodeError

## Why

`pack_ingest` 透過 Commons API 抓圖時，檔名含非 ASCII 字元（日文、韓文、泰文、越南文）的圖片會丟
`UnicodeEncodeError`，整個 ingest 失敗。第六批有一位撰稿者回報過，當時的查核者重現不出來所以沒追；
第七批寫仙台松島篇時再次撞到，而且這次知道是怎麼回事：**Commons 的回應標頭帶非 ASCII 內容**，
httpx 或底層的 urllib 在處理時炸掉。

實際代價是選圖被限縮：那位撰稿者說構圖最好的瑞鳳殿照片檔名含日文，只能改用純 ASCII 檔名的同主題照片。
日本、韓國、泰國、越南的景點在 Commons 上很多是當地文字檔名，這個限制會一直咬。

## Definition of done

- [ ] 用一個檔名含日文的 Commons 圖片重現（例如 `File:瑞鳳殿…jpg` 這類），寫成一個會紅的測試。
- [ ] 修掉：抓圖與讀 metadata 的路徑都要能處理非 ASCII 的檔名與回應標頭。
- [ ] 測試轉綠，`uv run pytest tests/test_guides_content_pack.py -q` 全綠。
- [ ] 在 `docs/travel-guides.md` 的內容包那一節拿掉（或修正）任何「檔名用 ASCII」的暗示，如果有的話。

## Steps

- [ ] 先重現：`app/guides/pack_ingest.py` 的 `commons_file_info` 與 `fetch_image` 兩條路徑都試。
- [ ] 看是 httpx 的 header 解碼、還是 URL 編碼沒做。工具本來就有一個 `UrllibTransport`（票
      `2026-09-13-life-ai-series-tooling` 提到 httpx 的連線被 Wikimedia 擋 403 才改走 urllib），
      問題可能在那一層。
- [ ] 修完用第七批仙台松島篇原本想用的那張瑞鳳殿照片實測一次。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_guides_content_pack.py -q
```

再用一個非 ASCII 檔名的 Commons 圖跑一次 `pack_cli ingest --dry-run`，要能通過。

## Notes

- 第七批因此換過照片的是 `sendai-matsushima-2-day-itinerary`；修好之後可以回頭換成構圖較好的那張。
- 這不影響已上線的文章，只影響之後的撰稿。
