---
id: 2026-09-28-video-story-redo-dropped
title: 放棄的故事可以重做一次
status: open
priority: P3
area: api
owner:
claimed_at:
created_at: 2026-09-28T14:30:22Z
completed_at:
branch:
depends_on:
  - 2026-09-28-video-story-admin-import-api
  - 2026-09-28-video-story-api-policy-languages
scope:
  - apps/api/app/video_automation/series.py
  - apps/api/app/video_automation/stories.py
  - apps/api/app/video_automation/admin_api.py
  - apps/api/tests/test_video_story_redo.py
---

# 放棄的故事可以重做一次

## Why

站主放棄一支品牌故事的影片時，那一集會變成 `skipped`，名額才會釋放（票 `2026-09-28-video-story-api-policy-languages`，PR #938）。但這一集已經開始過，所以不能恢復（恢復只給從沒開始過的故事，票 `2026-09-28-video-story-admin-import-api`，PR #936），重新匯入同一個代號也只會被當成「已開始，不動」。

結果是：一個故事只要做壞一次、被放棄，就再也做不了。100 個故事都是查核過的企劃，做壞的原因多半是圖片或旁白，不是故事本身；站主應該可以叫它重做。

## Definition of done

- [ ] 站主可以對一個被放棄的故事要求重做：它回到 `ready`，下一次輪到時工人從頭做一支新的影片。
- [ ] 舊的那支影片與它的紀錄都留著，不會被新的蓋掉；新影片的代號怎麼定（同一個 slug 加序號，或別的做法）寫在 Notes，而且不撞 `video_drama_episodes.slug` 的唯一鍵。
- [ ] 重做有次數上限（常數），超過就拒絕並說明，免得同一個故事一直重做一直花錢。
- [ ] 每日配額、同時進行數與緩衝照算；有稽核紀錄。
- [ ] 還沒被放棄的故事、其他類型的作品，行為不變。

## Steps

- [ ] 讀 `start_episode` 怎麼檢查 slug（故事的影片代號必須是匯入時定好的集數 slug），決定新影片的代號規則。
- [ ] `series.py` 加重做的函式，`admin_api.py` 加端點，權限照 `/skip` 與 `/restore`。
- [ ] 測試：重做一次、超過上限、沒被放棄的故事拒絕、其他類型拒絕。
- [ ] 後台頁面的按鈕另開票，或加進票 `2026-09-28-video-story-admin` 的後續。

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run pytest tests/test_video_story_redo.py tests/test_video_story.py tests/test_video_story_admin.py
```

## Notes

- 這是做伺服器票時回報的（2026-09-28）。在這張票做完之前的權宜做法：把那個故事用新的代號與 slug 加進企劃清單（例如 `A01` 之外另加一筆），重新匯入。
- 工人那一側：工作區是照影片代號開的，新代號就是新的工作區，舊的照清理工作檔的規則處理。
