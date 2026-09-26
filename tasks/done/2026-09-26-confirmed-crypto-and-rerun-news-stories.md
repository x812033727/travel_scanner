---
id: 2026-09-26-confirmed-crypto-and-rerun-news-stories
title: Confirmed crypto and rerun news stories stop on the disclaimer and on the last run's artwork
status: done
priority: P1
area: api
owner: claude-opus-5-5-news-final-editor
claimed_at: 2026-09-26T03:00:00Z
created_at: 2026-09-26T03:00:00Z
completed_at: 2026-09-26T03:10:00Z
branch: claude/news-crypto-disclaimer
depends_on:
  - 2026-09-26-news-reviewers-hold-translations-for-the
scope:
  - apps/api/app/news_automation/policy.py
  - apps/api/app/news_automation/ai.py
  - apps/api/app/news_automation/pipeline.py
  - apps/api/tests/test_news_automation.py
---

# Confirmed crypto and rerun news stories stop on the disclaimer and on the last run's artwork

## Why

After #780 was deployed on 2026-09-26, six confirmed stories were run again with Claude Opus
5.5 as the writer. Two of them stopped for reasons in the pipeline:

- **Bitget/Circle (crypto).** It failed the disclaimer hard checks in zh-TW, en and ja. The
  writer's zh-TW draft and two translations had no callout with the exact
  non-investment-advice phrase. The final editor added it in zh-CN and ko only. The
  safeguard from #780 only rejects problems an edit introduces, and these problems were
  already there.
- **Kalshi (rerun).** The zh-CN review held it for a "missing" hero image and diagram. The
  previous run had stored the zh-TW text with its artwork. The rerun gave that text to the
  translator, who is told to add no image, and then to the reviewer.

## Definition of done

- [x] Every crypto locale gets the site's own disclaimer callout
      (`policy.with_crypto_disclaimer`, five fixed texts carrying each `CRYPTO_MARKERS`
      phrase) wherever a model left none: after the draft, after a verifier correction,
      after translation, after a locale-review correction and after a final edit. The
      fingerprint ignores that callout, so adding it keeps a verification valid.
- [x] Stage two starts from `policy.site_additions_removed(zh-TW)`: no pipeline artwork and
      no topic link. Reviewers and the final editor see `policy.for_review` copies, which
      have neither.

## How to verify

`uv run pytest tests/test_news_automation.py tests/test_news_pipeline.py`
