---
id: 2026-09-26-news-reviewers-hold-translations-for-the
title: News reviewers hold translations for the per-locale topic link the pipeline adds
status: done
priority: P1
area: api
owner: claude-opus-5-5-news-final-editor
claimed_at: 2026-09-26T02:05:00Z
created_at: 2026-09-26T02:04:00Z
completed_at: 2026-09-26T02:05:00Z
branch: claude/news-review-ignores-topic-link
depends_on: []
scope:
  - apps/api/app/news_automation/policy.py
  - apps/api/app/news_automation/ai.py
  - apps/api/app/news_automation/pipeline.py
  - apps/api/tests/test_news_automation.py
  - apps/api/tests/test_news_pipeline.py
---

# News reviewers hold translations for the per-locale topic link the pipeline adds

## Why

On 2026-09-26 the owner confirmed seven zh-TW drafts. The Japanese locale review of the
Bitget/Circle story came back `manual` with one issue: the Japanese article links to
`https://mokaair.com/ja/life/topics/crypto` while the zh-TW source links to
`/zh-TW/life/topics/crypto`. That link is not the article's; the pipeline appends it to
each locale with that locale in the URL (`_topic_linked`). The reviewer reported the
intended difference as a mismatch, and the article stopped at
`news_locale_review_failed`. It can happen to any locale of any article, and to the final
editor.

## Definition of done

- [x] The locale reviewer and the final editor get both documents without the topic link
      (`policy.without_topic_links`).
- [x] A translation the reviewer corrects gets its topic link back before the hard checks.
- [x] `document_fingerprint` shares the one topic-link rule (`policy.is_topic_link`).
- [x] A final edit may not break a site check the translation passed. The editor gets one
      more call with the broken checks (`mechanical_problems`); if they are still broken, the
      locale keeps its reviewed translation. The prompt names the exact disclaimer phrase for
      each locale. On 2026-09-26 the Kalshi story lost its crypto disclaimer callout in all
      five locales this way.

## How to verify

`uv run pytest tests/test_news_automation.py tests/test_news_pipeline.py`

## Notes

- Outcome of the seven stories confirmed on 2026-09-26: Microsoft stopped at Jev's last call,
  set at 0.9 at the time; the owner lowered it to 0.55 afterwards. Bitget stopped on the topic
  link and Kalshi on the disclaimer; both are fixed here. The other four stopped on MiniMax
  translations.
- The same run showed the ways MiniMax stops a confirmed story:
  - an English translation whose JSON is broken twice (`expected , or }`), seen on KelpDAO
    and Anthropic;
  - a Korean translation that keeps Chinese words, seen on Sony/Suno.
- Both come from the writer model, which also translates. They are the owner's call (switch
  the writer to Claude on the subscription accounts), not a code bug.
