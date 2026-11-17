---
id: 2026-11-17-gemini-pool-ordinary-rate-limit-429
title: Gemini pool: ordinary rate-limit 429 mentions billing and rests the Ultra keys 12h
status: in-progress
priority: P2
area: api
owner: claude-opus-5-5
claimed_at: 2026-11-17T13:39:14Z
created_at: 2026-11-17T13:39:00Z
completed_at:
branch: claude/gemini-pool-rate-limit-billing
depends_on: []
scope:
  - apps/api/app/ai/gemini_pool.py
  - apps/api/tests/test_gemini_pool.py
---

# Gemini pool: ordinary rate-limit 429 mentions billing and rests the Ultra keys 12h

## Why

The owner saw admin zh-TW narration still spending the site's own Gemini key after the key pool
(#2137) went live. `gemini_pool._EXHAUSTED` matched a bare `billing`, and Google's ordinary
per-minute refusal reads "You exceeded your current quota, please check your plan and billing
details". So a speed limit was classed as out of money and the key rested 12 hours. Gemini TTS on a
Tier 1 project has a low RPM limit, so a narration batch put both Ultra keys to sleep almost at
once, and every call after that went to the site key.

## Definition of done

- [x] A rate-limit 429 rests a key only briefly (60 s, or Google's longer `retryDelay`, capped at 12 h).
- [x] Spending cap / prepay depleted are still read as exhausted.
- [ ] Deployed; the admin pool card shows spend on the Ultra keys after a narration run.

## How to verify

`cd apps/api && uv run pytest tests/test_gemini_pool.py`

## Notes

- Exhausted rests already written in production Redis (`gmpool:rest:*`) last up to 12 h after
  deploy; they can be deleted to start using the Ultra keys at once.
