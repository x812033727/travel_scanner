---
id: 2026-11-17-gemini-key-pool
title: Gemini key pool across Google AI Ultra accounts
status: review
priority: P1
area: api
owner: claude-opus-5.5-gemini-pool
claimed_at: 2026-11-17T09:52:15Z
created_at: 2026-11-17T09:51:18Z
completed_at:
branch: claude/google-ai-ultra-quota-plan-2ae705
depends_on: []
scope:
  - apps/api/app/ai/gemini_pool.py
  - apps/api/app/ai/gemini.py
  - apps/api/app/config.py
  - apps/api/app/admin/service.py
  - apps/api/app/admin/router.py
  - apps/api/app/catalog_review/provider.py
  - apps/api/app/hotspots/guides.py
  - apps/api/app/video_speech/gemini.py
  - apps/api/app/video_speech/checking.py
  - apps/api/app/video_media/providers/__init__.py
  - apps/api/app/video_media/jobs.py
  - apps/api/tests/test_gemini_pool.py
  - apps/web/components/admin-gemini-pool.tsx
  - apps/web/components/admin-gemini-pool.test.tsx
  - apps/web/components/admin-settings-panel.tsx
  - apps/web/lib/gemini-pool-copy.ts
  - apps/web/lib/gemini-pool-messages
  - .env.example
---

# Gemini key pool across Google AI Ultra accounts

## Why

The owner has two Google AI Ultra accounts, each with US$100 of Google Cloud credit a month
that the Gemini API can spend. The site had one Gemini key, and when its project hit the
monthly spending cap on 2026-10-31 every Gemini feature stopped at once. The owner asked
(2026-11-17) for the site to read what is left and pick which key to use.

## Definition of done

- [x] Extra Gemini keys can be entered in admin → AI settings, and are used up in order before
      the site's own key.
- [x] A key Google refuses for money (429 spending cap, 402 prepay) rests, and the next call
      goes out with the next key; a plain rate-limit 429 only rests it a minute.
- [x] The admin page lists each key (fingerprint tail), which one is in use, which rest and until
      when, and this month's estimated spend.
- [ ] Deployed, and the owner has pasted the two Ultra keys.

## Steps

- [x] `app/ai/gemini_pool.py`: order, rest, spend tally, `note_response` classifier.
- [x] `load_runtime_settings` swaps in the chosen key (no call site had to change).
- [x] `note_response` on every Gemini answer: structured text, grounded guide search, catalog
      review, TTS, transcription check, video media (`raise_for_status`, which judge and locate
      also use).
- [x] Media jobs: a submitted clip is pinned to the key that sent it (`gemini_key_fp`), and its
      `usd_estimate` is tallied to that key when ready.
- [x] `GET /admin/provider-settings/ai_vendors/gemini-pool` and the admin table.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_gemini_pool.py
cd apps/web && npx vitest run components/admin-gemini-pool.test.tsx components/admin-settings-panel.test.tsx
```

After deploy: admin → AI settings → AI vendors shows the "Gemini key pool" table once the extra
keys are saved, with the first Ultra key "In use".

## Notes

- Google publishes no API for the remaining credit (only aistudio.google.com/billing shows it),
  so "reading the quota" is Google's refusal plus the site's own estimate. The refusal is the
  real switch. The owner's Ultra accounts are on prepay billing (2026-11-17), so Google refuses
  with 402 once nothing is left and never bills past it; no spending cap is needed. Google
  applies promotional credit only while the prepaid balance is above zero.
- Ultra credit renews on the subscription's billing day, not the 1st, so an exhausted key rests
  at most 12 hours (never past the month) and is then tried once again. The local tally is per
  Pacific calendar month and is display-only unless a budget is written for the key.
- Grounding (Google Search) request fees are not in the estimate; only tokens are.
- Copy lives in `lib/gemini-pool-messages/`, not `messages/*/admin.json`, which is SHA-bound by a
  video duration review (same reason as `lib/runpod-copy.ts`).
- Claimed with `--force`: the overlapping claims (MiniMax pool, MiniMax speech, dubs) were all
  older than 24 hours.
