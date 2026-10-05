---
id: 2026-10-05-chatgpt-taiwan-currency-and-ads-lines
title: "ChatGPT now bills Taiwan in NT$: fix the USD-only and US-only-ads lines in two AI guides"
status: open
priority: P3
area: docs
owner:
claimed_at:
created_at: 2026-10-05T14:20:00Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/guides/content/ai-tools-2026-overview.json
  - apps/web/public/guides/ai-tools-2026-overview/diagram-1.svg
  - apps/api/app/guides/content/chatgpt-beginner-guide.json
---

# ChatGPT now bills Taiwan in NT$: fix the USD-only and US-only-ads lines in two AI guides

## Why

Found while doing `2026-10-05-review-the-openai-and-cross-vendor` (model and price pass), and left
because neither line is about the model line-up and each fix needs a source swap or an
out-of-scope diagram:

- `ai-tools-2026-overview` (checked 9/13) says ChatGPT's paid plans are billed in US dollars
  ("付費以美元計"), that "台灣有台幣定價的只有 Google", and its diagram footnote says "Google 有台幣定價，
  其餘以美元計". OpenAI's Multi-currency billing help article lists "TWD (NT$) | Taiwan" (read
  2026-10-05), and `chatgpt-plans-plus-pro-2026` / `ai-free-vs-paid-plans-2026` already quote the
  Taiwan pricing page in NT$ (9/30). The pack is at the 20-source limit.
- `chatgpt-beginner-guide` (checked 9/13) says ads may appear on Free "in some countries" and that
  "OpenAI 已宣布先在美國測試"; the table says Go ads are only a future test. Ads started rolling out in
  Taiwan for Free and Go on 2026-09-23 (`ai-news-chatgpt-ads-taiwan-20260923`), and the Ads in
  ChatGPT help article now says ads may appear on Free and Go. The pack is at the 20-source limit.

## Definition of done

- [ ] Neither page says ChatGPT is billed only in USD in Taiwan or that ads are a US-only test; the
      replacement sentences cite a source read that day.
- [ ] The ai-tools diagram footnote matches the text, with `image.description` a verbatim copy of
      the SVG `<desc>`.

## Steps

- [ ] Re-read help.openai.com Multi-currency billing and Ads in ChatGPT (both answer `curl -sSL`
      with the editorial User-Agent; Node's `fetch` gets 403).
- [ ] Pick which source each pack drops to stay at 20, and say why in the notes.
- [ ] Edit the text, the table rows and the ai-tools diagram; run
      `pack_cli lint --kind life --slug ...` with `--render-dir` and look at the PNG.

## How to verify

`grep -nE "付費以美元計|台幣定價的只有|先在美國測試" apps/api/app/guides/content/{ai-tools-2026-overview,chatgpt-beginner-guide}.json`
returns nothing, and `PYTHONUTF8=1 uv run python -m app.guides.pack_cli lint --kind life --slug ai-tools-2026-overview --slug chatgpt-beginner-guide`
passes from `apps/api`.

## Notes

- Split from 2026-10-05-review-the-openai-and-cross-vendor; that PR already changed the beginner
  guide's currency sentence to "多幣別計費頁把新台幣（TWD）列為台灣的計費幣別" and left the ads lines.
- `chatgpt.com/zh-Hant/pricing/` returned 200 on 2026-10-05 but the NT$ amounts were not in the
  static HTML, so the static page cannot back a price figure; quote amounts only from a page that
  shows them.
