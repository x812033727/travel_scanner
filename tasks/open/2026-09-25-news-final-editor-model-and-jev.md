---
id: 2026-09-25-news-final-editor-model-and-jev
title: News final editor model and Jev final gate, auto-publish without the shadow gate
status: in-progress
priority: P1
area: api
owner: claude-opus-5-5-news-final-editor
claimed_at: 2026-09-25T13:48:47Z
created_at: 2026-09-25T13:48:39Z
completed_at:
branch: claude/news-final-editor
depends_on: []
scope:
  - apps/api/app/news_automation
  - apps/api/migrations/versions/0094_news_final_editor.py
  - apps/api/tests/test_news_pipeline.py
  - apps/api/tests/test_news_review_actions.py
  - apps/api/tests/test_news_admin.py
  - apps/api/tests/test_news_automation.py
  - apps/api/tests/test_migration_0094_news_final_editor.py
  - apps/web/components/admin-news-workspace.tsx
  - apps/web/components/admin-news-workspace.test.tsx
  - apps/web/lib/admin-news.ts
  - apps/web/lib/admin-news-messages
  - docs/news-automation.md
---

# News final editor model and Jev final gate, auto-publish without the shadow gate

## Why

The owner wants news to go all the way from discovery to publication on its own. Today every
candidate stops at "zh-TW draft waiting for confirmation". Automatic publication needs a
14-day, 50-label, 95%-agreement shadow gate (every vertical is at 0), and evidence from two
websites, which almost no official announcement has. Also, after translation no model checks
the final five-language version against the evidence, and Jev only judges the zh-TW draft.

Owner decisions, 2026-09-25:

- A third model, the final editor, checks each of the five translated locales against the
  evidence for readers, and may not add facts. Jev then judges all five as the final gate.
- The shadow gate is removed. If the final editor and Jev both pass, the article is
  published. The owner accepted that Jev publishes no accuracy numbers for CJK text.
- A single website is enough for automatic publication when the evidence has a first-party
  page.
- The final editor defaults to Claude Opus 5.5 on the subscription accounts (PR #761).

## Definition of done

- [x] Settings have an editor vendor and model, default anthropic / claude-opus-5-5.
- [x] Stage two runs final-edit-<locale> for all five locales, then jev-final. Five acts
      publish. Anything else stops at news_jev_final_hold (or news_final_edit_hold) with the
      article saved, and the publish button works from there.
- [x] Auto-publish can be switched on without the gate, and a model change no longer turns
      it off.
- [x] A single first-party website lets a candidate go on to stage two automatically.
- [x] /admin/news shows the editor model and the two new holds, and the gate card is for
      reference only.

## Steps

- [x] Migration, model, schemas, settings_cli.
- [x] ai.final_edit, pipeline, service.
- [x] Web settings, holds, copy in five languages.
- [x] Tests and docs.

## How to verify

Pipeline tests for automatic publish, final hold, owner-confirmed publish, and first-party
single source. After deploy: automatic mode on, confirm a zh-TW draft, and the runs show
final-edit-* and jev-final.

## Notes

- Migration number: PR #759 took 0093; this one is 0094 on top of it.
