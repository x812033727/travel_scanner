---
id: 2026-09-28-video-shorts-worker-cut
title: Video shorts T3: highlights cut from the published tutorials, rewritten for the vertical frame
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-09-28T03:50:00Z
completed_at:
branch:
depends_on:
  - 2026-09-28-video-shorts-worker-lab
scope:
  - tools/video/shorts/cut.mjs
  - tools/video/shorts/cut.test.mjs
  - .agents/skills/youtube-video/references/prompts/shorts-cut.md
---

# Video shorts T3: highlights cut from the published tutorials, rewritten for the vertical frame

## Why

站主選的第二條內容線是「長片精華」：每支教學長片切 1–2 支直式短片，把觀眾導回完整影片與文章。長片是 16:9 的投影片、一句可以很長、字幕不燒錄；直接裁成直式會看不到字。所以精華不是剪片，是用同一份查核過的內容重寫成直式字卡，旁白用同一個頻道聲音。

設計全文在 `docs/videos/SHORTS.md`（§三條內容線）。

## Definition of done

- [ ] `make` 在題目的 `line` 是 `cut` 時走 `cut.mjs`：輸入是來源長片的 `video.json`（由伺服器在 `shorts/next` 的脈絡裡給，或從工人自己的工作區讀）、它的查核報告、它在 YouTube 上的影片 id。
- [ ] 挑段落（`planner`、`variant: shorts-cut`）：一支長片挑 1–2 段，每段有自己的鉤子與結論、不需要前文就聽得懂、估計 25–55 秒；兩段不能講同一件事。
- [ ] 改寫（`writer`、`variant: shorts-cut`）：字卡照 Shorts 腳本的限制（標題 36 字、每句 38 字、最多 5 列）；**只能用來源長片裡已經查核過的事實與數字**，不准加新的說法；第一句是鉤子，最後一句把觀眾導回完整影片。
- [ ] lint：腳本裡出現的每個數字與拉丁字詞都要在來源長片的稿子裡找得到（沿用 `rewrite.mjs` 比對數字與拉丁字詞的做法）；找不到就是錯誤。
- [ ] `source` 記下來源影片的代號、影片 id 與用到的句子 id；說明欄第一行是完整影片的連結，第二行是對應文章的連結（帶 `utm_source=youtube&utm_medium=shorts&utm_campaign=<Shorts 代號>`）。
- [ ] 品管的 `evidence` 項：來源影片存在、已公開、沒有被放棄；`links` 項：兩個連結都回 200。
- [ ] 句子跟長片一字不差、聲音相同時，旁白快取命中，不重新合成。
- [ ] 測試：挑段落的檢查、數字與拉丁字詞的比對、連結的組法、來源不符時的拒絕。

## Steps

- [ ] 讀 `tools/video/automation/rewrite.mjs` 與 `tools/video/core/metadata.mjs` 的 `articleUrl`。
- [ ] `cut.mjs` 與提示詞。
- [ ] 測試。
- [ ] 拿第二批的一支長片（已核准的）在本機試做一支，放進票的 Notes。

## How to verify

```bash
node --test tools/video/shorts/cut.test.mjs
npm run test:tools
```

## Notes

- 「相關影片」（Shorts 連回完整影片的欄位）能不能用 API 寫，要等 `2026-09-28-video-shorts-pilot-launch` 實測；在那之前連結只放說明欄。
- 長片還沒公開時不做它的精華：精華要連得回去。
- 文章頁曾經會把網址的查詢字串（含 UTM）轉址拿掉；組連結之前先確認那個問題修了沒有，沒修就在 Notes 記下並另開票。
- PR #880 的 12 支是同一種內容（六集長片各切兩支），它們用 `import` 進來，不走這裡。
