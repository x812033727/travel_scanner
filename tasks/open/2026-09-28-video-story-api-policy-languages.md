---
id: 2026-09-28-video-story-api-policy-languages
title: 故事版立場檢查、自動語系、釋放名額、媒體每小時上限與 Flash 單價
status: in-progress
priority: P1
area: api
owner: claude-opus-5-5-video-story-policy
claimed_at: 2026-09-28T11:46:43Z
created_at: 2026-09-28T03:31:13Z
completed_at:
branch: claude/video-story-api-policy-languages
depends_on:
  - 2026-09-28-video-story-api-series-kind
scope:
  - apps/api/app/video_automation/judge.py
  - apps/api/app/video_reviews/admin_service.py
  - apps/api/app/video_media/admin_api.py
  - apps/api/app/video_media/catalog.py
  - apps/api/app/video_media/jobs.py
  - apps/api/tests/test_video_story_policy.py
---

# 故事版立場檢查、自動語系、釋放名額、媒體每小時上限與 Flash 單價

## Why

品牌故事要全自動（`docs/videos/STORY.md`），但伺服器有五個地方會讓它停下來或算錯：

1. 成片品管的立場檢查要求「有示範或實算」（`apps/api/app/video_automation/judge.py` 的 policy 題組），那是教學影片的標準；故事沒有示範，每一支都會不過而落回站主。
2. PR #870 之後每支影片都等站主選語系；免關卡的故事沒有人會去選。
3. 站主放棄一支影片時，那一集仍是 `started`，同時進行的名額永遠不釋放。
4. 送圖每小時上限 60、judge 120（`apps/api/app/video_media/admin_api.py`）：一支故事約 120 張圖，光圖片就要兩小時以上。
5. 目錄把 Gemini 3.1 Flash Image 登記成每張 US$0.045（`apps/api/app/video_media/catalog.py`），那是 0.5K 的價格；adapter 只送 `aspectRatio`，實際輸出 1K，官方價目是 US$0.067。帳本與每支上限都會少算三成。

## Definition of done

- [ ] 影片屬於 `kind: "story"` 的作品時，立場檢查用故事版題組：照頻道立場寫、留給觀眾一個觀察、沒有投資醫療法律政治建議、沒有業配、沒有貶損特定人；門檻與規則寫成常數並有測試。題組由伺服器從影片所屬的作品決定，工人不能指定。
- [ ] 免關卡的故事在開始時由伺服器照設定的字幕語系寫入語系決定，不等站主。
- [ ] 放棄一支屬於作品的影片時，那一集標成 `skipped`。
- [ ] 送圖與 judge 的每小時上限提高到 240 與 360。
- [ ] 媒體工作依影片所屬作品的 `image_model` 決定圖片模型；沒有覆寫時照設定。
- [ ] 目錄的 Flash 單價是實際輸出尺寸的價格，備註寫明尺寸與查價日期；`/video/media/status` 的估計跟著對。
- [ ] `ruff`、`mypy`、`pytest` 通過。

## Steps

- [ ] `judge.py`：故事版題組與過關規則；`judge_video_policy` 依作品類型選題組。
- [ ] `video_reviews/admin_service.py`：語系自動決定；放棄時釋放名額。
- [ ] `video_media`：每小時上限、作品的圖片模型覆寫、目錄單價。
- [ ] 測試。

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run mypy tests && uv run pytest tests/test_video_story_policy.py tests/test_video_automation_judge.py tests/test_video_media_api.py tests/test_video_reviews.py
```

## Notes

- Jev 只讀文字、不會算數也讀不準日期（`apps/api/app/ai/jev.py` 開頭），題組只問文字判斷；事實對不對是查核階段的事。
- 改單價前再讀一次官方價目頁，數字與日期寫進目錄的備註。2026-09-28 讀到的是：Flash 0.5K US$0.045、1K US$0.067、2K US$0.101、4K US$0.151；Pro 1K–2K US$0.134。
- 如果試作發現 1K 放大後不夠清楚，要在 adapter 送尺寸參數改成 2K；那會讓每支成本從約 US$9 變成約 US$13，改之前先問站主。
- 2026-09-28 認領（claude-opus-5-5-video-story-policy）：`claim` 因為相依的 `2026-09-28-video-story-api-series-kind` 還沒結案而拒絕。那張票的工作已經做完並推上去（PR #910，草稿），它的代理只在等整套測試跑完才 `done`；這個分支從 `origin/claude/video-story-api-series-kind`（`20a5af61`）開出、再併入 main（`5b35df86`），所以用 `--force` 認領。認領前查過：沒有 `policy-languages` 的遠端分支與開著的 PR。
