---
id: 2026-09-25-offer-gpt-6-sol-and-luna
title: Offer GPT-6 Sol and Luna in the admin model dropdowns
status: done
priority: P2
area: api
owner: claude-opus-5-5
claimed_at: 2026-09-25T12:34:41Z
created_at: 2026-09-25T12:34:35Z
completed_at: 2026-09-25T12:36:48Z
branch: claude/chatgpt-sol6-update-43e8c9
depends_on: []
scope:
  - apps/api/app/ai/catalog.py
  - apps/api/tests/test_ai_catalog.py
  - apps/api/app/config.py
  - .env.example
  - apps/api/tests/test_admin_provider_settings.py
---

# Offer GPT-6 Sol and Luna in the admin model dropdowns

## Why

On 2026-09-25, right after Claude Opus 5.5 was added (#741), the site owner noticed the
OpenAI dropdowns still stop at GPT-6 Astra and the GPT-5.6 family. OpenAI launched
GPT-6 Sol (`gpt-6-sol`, $2 / $10 per MTok) and GPT-6 Luna (`gpt-6-luna`, $0.10 / $0.50)
on 2026-09-22 at half the price of GPT-5.6 Sol and Luna. Every OpenAI dropdown in the
admin is built from `apps/api/app/ai/catalog.py`.

## Definition of done

- [x] `gpt-6-sol` and `gpt-6-luna` are offered under OpenAI right after GPT-6 Astra,
      with the GPT-5.6 models kept.
- [x] A test pins that both are offered wherever the OpenAI catalog feeds a dropdown.

## Steps

- [x] Check the models against the code path: both list Structured Outputs and the
      Responses API on developers.openai.com; the OpenAI paths send no temperature.
- [x] Add the catalog entries and a test.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_ai_catalog.py -q
```

After deploying, `/admin/news` settings: choose OpenAI and GPT-6 Sol and GPT-6 Luna
follow GPT-6 Astra.

## Notes

- There is no GPT-6 Terra. On 2026-09-25 the owner chose GPT-6 Sol as the new shipped
  default (`OPENAI_MODEL`, was GPT-5.6 Terra): same input price, cheaper output. A value
  saved on `/admin/settings` or set in the host's `.env` still wins over the code default.
- `gpt-5.6-cyber` exists too but is a cybersecurity model and is left out.
