---
id: 2026-10-06-ai-tools-overview-gemini-s-has
title: "ai-tools overview: Gemini's NT$-pricing strength no longer sets it apart"
status: open
priority: P3
area: docs
owner:
claimed_at:
created_at: 2026-10-06T01:41:08Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/guides/content/ai-tools-2026-overview.json
  - apps/web/public/guides/ai-tools-2026-overview/diagram-1.svg
---

# ai-tools overview: Gemini's NT$-pricing strength no longer sets it apart

## Why

`ai-tools-2026-overview` still sells NT$ pricing as something only Gemini has, in three places:

- the Gemini paragraph (zh-TW block 11): "優勢是跟 Gmail、Google 文件、YouTube、地圖綁在一起，而且有台幣定價";
- the comparison table's 強項 cell for Gemini: "跟 Gmail、文件、YouTube 整合；有台幣定價";
- the diagram's Gemini row ("有台幣定價", line 57 of `diagram-1.svg`), repeated in the SVG `<desc>`
  and `image.description` ("強項是與 Gmail、文件、YouTube 整合並有台幣定價").

Each line is still true about Gemini. But the sentence above the table now says ChatGPT bills
Taiwan in NT$ (OpenAI's Multi-currency billing page lists "TWD (NT$) Taiwan", read 2026-10-06), and
`chatgpt-plans-plus-pro-2026` quotes ChatGPT's Taiwan pricing page in NT$ (2026-09-30). Calling NT$
pricing a Gemini strength therefore reads as "only Gemini", which is the claim
`2026-10-05-chatgpt-taiwan-currency-and-ads-lines` removed from the table intro and the diagram
footnote. That ticket was told to fix only the lines it named, so these were left.

## Definition of done

- [ ] No line in the pack presents NT$ pricing as something that sets Gemini apart from ChatGPT;
      if a Gemini line keeps it, it says what differs (for example that Google's Taiwan plan page
      shows fixed NT$ prices), backed by a source read that day.
- [ ] The diagram's Gemini row, the SVG `<desc>` and `image.description` match the text, with
      `image.description` a verbatim copy of the `<desc>`.

## Steps

- [ ] Re-read gemini.google/tw/subscriptions/ (it geolocates to the Taiwan page) and decide whether
      the strength keeps a currency clause at all.
- [ ] Edit block 11, the table's Gemini 強項 cell, the diagram row (line 57), the `<desc>` and
      `image.description`; keep the pack at 20 sources or fewer.
- [ ] Run `pack_cli lint --kind life --slug ai-tools-2026-overview --render-dir <dir>` and look at
      the PNG; run `intake_check.py --slug ai-tools-2026-overview --from-content` and compare with
      origin/main (it has three FAILs that predate this ticket: no summary first, a 6-column table,
      two self-references).

## How to verify

From `apps/api`: `PYTHONUTF8=1 uv run python -m app.guides.pack_cli lint --kind life --slug ai-tools-2026-overview`
passes, and `git grep -n "有台幣定價" -- apps/api/app/guides/content/ai-tools-2026-overview.json apps/web/public/guides/ai-tools-2026-overview/diagram-1.svg`
returns only lines that say what differs, if any.

## Notes

- Noticed while doing `2026-10-05-chatgpt-taiwan-currency-and-ads-lines` (2026-10-06). The pack is
  at the 20-source limit after that ticket (it swapped the MiniMax H3 blog for OpenAI's
  Multi-currency billing page).
- Republish after merge: `ai-tools-2026-overview` (coordinator, owner consent).
