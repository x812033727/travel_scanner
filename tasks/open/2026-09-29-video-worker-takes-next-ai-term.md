---
id: 2026-09-29-video-worker-takes-next-ai-term
title: 影片工人沒有新題目時，從 AI 名詞庫接下一個名詞
status: open
priority: P3
area: api
owner:
claimed_at:
created_at: 2026-09-29T23:43:23Z
completed_at:
branch:
depends_on:
  - 2026-09-29-ai-terms-video-pilot
scope:
  - apps/api/app/video_automation/topics.py
  - apps/api/tests/test_video_automation_topics.py
  - docs/videos/AUTOMATION.md
---

# 影片工人沒有新題目時，從 AI 名詞庫接下一個名詞

## Why

`docs/videos/ai-terms/` 是一個 81 集、不編集數的名詞系列，題庫在 `terms.json`。主機工人排程草稿時只從最近 14 天發布的生活類文章與 Brave 搜尋挑題（`apps/api/app/video_automation/topics.py` 的 `site_topics`，`SITE_DAYS = 14`），名詞文章 2026-09-14 發布之後就不在候選裡，所以每一集都要有人發起。要讓系列自己往前走，工人在候選題目不夠（或站主在設定分頁勾了「沒有新題目時做名詞」）時，可以從名詞庫拿 `tier` 最低、`suggested_order` 最前、`status: backlog` 的一個名詞當題目，`source_guide` 填那一列的文章。

要先做完試片票 `2026-09-29-ai-terms-video-pilot`，確定系列規格可行再自動化；站主也可以決定永遠手動發起，那就關掉這張票。

## Definition of done

- [ ] `gather_topics` 在站上與搜尋的候選都空（或設定開關打開）時，回傳名詞庫的下一個名詞（`TopicView` 的 `slug` 是文章 slug、標題是 `article_title`、備註帶影片代號與 README 的骨架連結）；已做過的（`docs/videos/ai-term-*` 或審核頁有同 `source_guide`）跳過。
- [ ] 名詞庫讀不到或格式錯時只寫 notes，不影響原本的挑題。
- [ ] 測試涵蓋：候選夠時不拿名詞、候選空時拿第一個 backlog、跳過已做過的。
- [ ] `docs/videos/AUTOMATION.md` §一支影片的自動流程 補一句「沒有新題目時從名詞庫接」。

## Steps

- [ ] 決定名詞庫怎麼進工人：API 容器讀 repo 的 `docs/videos/ai-terms/terms.json`（跟 `docs/videos` 一樣掛進工人的 volume）或站上設定貼一份；寫進 Notes。
- [ ] `topics.py` 加 `glossary_topics(...)`，在 `gather_topics` 最後接上；不動既有的排序。
- [ ] 新測試檔 `apps/api/tests/test_video_automation_topics.py`。
- [ ] 更新 `AUTOMATION.md`。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_video_automation_topics.py -q && uv run ruff check app/video_automation/topics.py && uv run mypy app
```

## Notes

- 企劃模型收到名詞題目時，要一併拿到 `docs/videos/ai-terms/README.md` 的 §一集長什麼樣 與 §三種場景配方，否則寫出來的骨架跟新聞影片一樣；怎麼把 README 塞進工人的提示詞（`tools/video/automation/prompts.mjs`）不在這張票的 scope，做的時候另開 tools 的票。
