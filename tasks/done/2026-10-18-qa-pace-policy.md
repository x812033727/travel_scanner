---
id: 2026-10-18-qa-pace-policy
title: 品牌故事配音解鎖：QA 字幕循環與 pace/policy 不擋配音
status: done
priority: P2
area: api
owner: claude-opus-5.5-story-dub
claimed_at: 2026-10-18T07:09:52Z
created_at: 2026-10-18T07:09:21Z
completed_at: 2026-10-18T07:37:59Z
branch: claude/story-dub-unlock
depends_on: []
scope:
  - apps/api/app/video_reviews/admin_service.py
  - apps/api/tests/test_video_reviews.py
  - tools/video/qa/checks.mjs
  - tools/video/qa/cli.mjs
  - tools/video/qa/checks.test.mjs
---

# 品牌故事配音解鎖：QA 字幕循環與 pace/policy 不擋配音

## Why

正式站 2026-10-18：品牌故事 `story-adapt-seiko-quartz-astron` 成片已由站主核准、上傳包也做好，
`locales` 勾了 en/ja/ko 的標題說明＋CC＋配音，但後台三種語言永遠停在「製作中」。
`_story_dub_ready` 要求成片 QA 全部 11 項過，而這支的 `review/qa.json` 有三項沒過：

- `captions`：「en: no caption file; ja: no caption file; ko: no caption file」。這是循環：
  外語字幕要等 `dub_allowed` 之後的語言步驟才翻譯，所以勾了外語的影片在成片關卡永遠過不了。
  教學影片也一樣（成片 QA 時還沒有 languages.json，所有語系都被要求），只是站主手動核准成片蓋過去。
- `pace`、`policy`：站主看過片已判斷，不擋配音。

## Definition of done

- [x] QA 的 `captions` 在成片關卡對「勾了但還沒有翻譯」的外語只警告；繁中與旁白語言照舊必須有檔且正確；
      已有翻譯（含過期的）的外語照舊檢查；語言關卡的上傳包檢查（`package/check.mjs`）不變，仍要外語檔。
- [x] 伺服器的品牌故事配音判定：成片站主核准、QA 綁定成片雜湊、`subtitles_burned_in is False`、
      十一項都有回報，沒過的只限 {pace, policy}，或 captions 只因外語缺檔失敗（相容舊報告）。
      `final_qa_passed`（自動核准等處）不變。

## Steps

- [x] `tools/video/qa/checks.mjs` `captionsItem` 加 `untranslated`；`cli.mjs` 算出沒有任何翻譯的已選外語。
- [x] `admin_service.py` 加 `STORY_DUB_WAIVED_QA_ITEMS` 與 `_story_dub_qa_passed`。
- [x] pytest 與 node 測試。

## How to verify

```bash
node --test tools/video/qa/checks.test.mjs
cd apps/api && uv run pytest tests/test_video_reviews.py -q -k story
```

## Notes

- 既有的 B25 報告（captions 只缺 en/ja/ko、pace、policy）部署後直接被新判定接受，不用重跑 QA
  或重送成片：`dub_allowed` 每次都從目前成片審核的 payload 重新算。
- captions 的相容判斷只接受 detail 每一段都剛好是「<en|ja|ko>: no caption file」；
  「zh-TW: no caption file」、過期翻譯「…, N lines missing…」、舊旁白等都仍然擋。
