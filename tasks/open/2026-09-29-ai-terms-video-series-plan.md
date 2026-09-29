---
id: 2026-09-29-ai-terms-video-series-plan
title: AI 名詞影片系列：系列規格與名詞庫
status: in-progress
priority: P2
area: docs
owner: claude-fable-5-1
claimed_at: 2026-09-29T23:43:23Z
created_at: 2026-09-29T23:43:22Z
completed_at:
branch: claude/ai-terms-video-series
depends_on: []
scope:
  - docs/videos/ai-terms
---

# AI 名詞影片系列：系列規格與名詞庫

## Why

站主 2026-09-29 要一個 YouTube 的 AI 教學影片系列，先做「名詞介紹」：不編集數，只要有新名詞就能直接出一集，每集約 10 分鐘。站上已經有 81 篇查核發布的 AI 名詞專文（`docs/ai-terms-series/ARTICLES.md`），是現成的題庫；全自動路線（skill `youtube-video`）本來就把「站上文章改成影片」當最省力的題材來源。缺的是系列層的規格：一集的骨架與長度、標題縮圖說明欄的格式、播放清單、不編集數時一個名詞怎麼發起與登記、怎麼避免被 YouTube 當成模板量產、跟原來如此事務所與既有長片的分工。

## Definition of done

- [x] `docs/videos/ai-terms/README.md`：系列規格（決定、各語系名稱、10 分鐘骨架、三種場景配方、每集必備、包裝規則、發起流程、分工、政策對策、Shorts、多語、查核、成本、站主要決定的事）。
- [x] `docs/videos/ai-terms/terms.json`：81 個名詞一列一集，含影片代號、文章 slug、分層、建議順序、鉤子、互連名詞、既有影片、狀態。
- [ ] 站主確認系列名稱、出片時段與立場第 8、9 條（README §站主要決定的事）；確認後把「提案」字樣拿掉。

## Steps

- [x] 讀 skill `youtube-video`、`docs/videos/README.md`、`ILLUSTRATED.md`、`AUTOMATION.md`、`HANDS-OFF.md`、`SHORTS.md`、`so-thats-why/README.md`、`docs/ai-terms-series/`。
- [x] 對照 `docs/videos/*/video.json` 的 `source_guide` 與原來如此事務所的 A 軸題目，標出已有影片的名詞（`existing_videos`、`notes`）。
- [x] 從 `catalogue.json` 生成 `terms.json`（產生腳本只在 session 的暫存區；之後直接手改 `terms.json`）。
- [x] 開試片票 `2026-09-29-ai-terms-video-pilot` 與 P3 票 `2026-09-29-video-worker-takes-next-ai-term`。
- [ ] 站主決定後更新 README 與 `terms.json` 的 `series.names`、`series.title_suffix`。

## How to verify

```bash
python3 -c "import json;d=json.load(open('docs/videos/ai-terms/terms.json'));print(len(d['terms']), sum(t['tier']==1 for t in d['terms']))"   # 81 21
python3 -c "import json,os;d=json.load(open('docs/videos/ai-terms/terms.json'));print([t['source_guide'] for t in d['terms'] if not os.path.exists('apps/api/app/guides/content/'+t['source_guide']+'.json')])"   # []
npm run check:tasks
```

## Notes

- 2026-09-29：規格與名詞庫在分支 `claude/ai-terms-video-series`。名稱「AI 名詞十分鐘」、週二五 20:00、立場第 8、9 條都是提案，等站主。
- 主機工人只挑最近 14 天的文章（`apps/api/app/video_automation/topics.py` 的 `SITE_DAYS`），名詞文章 9/14 發布已出窗口，所以第一批由 session 發起（README §一個名詞怎麼變成一集）；工人自己接名詞是 P3 票。
- 頻道立場 2026-09-29 仍空白（`docs/videos/SHORTS.md` 與英文第一季的紀錄）：立場空白時 Jev 不挑大綱、`qa` 的 `policy` 不過，第一集開工前站主要先存立場。
