---
id: 2026-10-05-chatgpt-taiwan-currency-and-ads-lines
title: "ChatGPT now bills Taiwan in NT$: fix the USD-only and US-only-ads lines in two AI guides"
status: done
priority: P3
area: docs
owner: claude-opus-5-5-chatgpt-taiwan
claimed_at: 2026-10-06T01:07:45Z
created_at: 2026-10-05T14:20:00Z
completed_at: 2026-10-06T01:43:09Z
branch: claude/chatgpt-taiwan
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

- `ai-tools-2026-overview` (checked 9/13) says, above its comparison table, that "台灣有台幣定價的只有
  Google", and its diagram footnote says "Google 有台幣定價，其餘以美元計". OpenAI's Multi-currency
  billing help article lists "TWD (NT$) | Taiwan" (read 2026-10-05), and `chatgpt-plans-plus-pro-2026`
  / `ai-free-vs-paid-plans-2026` already quote the Taiwan pricing page in NT$ (9/30); for Claude,
  `claude-plans-free-pro-max-2026` quotes the help center as pricing supported regions in local
  currency. The ChatGPT and Claude paragraphs' own "付費以美元計" / "付費同樣以美元計" clauses were
  already deleted in the review round of PR #1291 (2026-10-06). The pack is at the 20-source limit.
- `chatgpt-beginner-guide` (checked 9/13) says ads may appear on Free "in some countries" and that
  "OpenAI 已宣布先在美國測試"; the table says Go ads are only a future test. Ads started rolling out in
  Taiwan for Free and Go on 2026-09-23 (`ai-news-chatgpt-ads-taiwan-20260923`), and the Ads in
  ChatGPT help article now says ads may appear on Free and Go. The pack is at the 20-source limit.

## Definition of done

- [x] Neither page says ChatGPT is billed only in USD in Taiwan or that ads are a US-only test; the
      replacement sentences cite a source read that day.
- [x] The ai-tools diagram footnote matches the text, with `image.description` a verbatim copy of
      the SVG `<desc>`.

## Steps

- [x] Re-read help.openai.com Multi-currency billing and Ads in ChatGPT (both answer `curl -sSL`
      with the editorial User-Agent; Node's `fetch` gets 403).
- [x] Pick which source each pack drops to stay at 20, and say why in the notes.
- [x] Edit the text, the table rows and the ai-tools diagram; run
      `pack_cli lint --kind life --slug ...` with `--render-dir` and look at the PNG.

## How to verify

`grep -nE "以美元計|台幣定價的只有|先在美國測試" apps/api/app/guides/content/{ai-tools-2026-overview,chatgpt-beginner-guide}.json`
returns nothing, and `PYTHONUTF8=1 uv run python -m app.guides.pack_cli lint --kind life --slug ai-tools-2026-overview --slug chatgpt-beginner-guide`
passes from `apps/api`.

## Notes

- Split from 2026-10-05-review-the-openai-and-cross-vendor; that PR already changed the beginner
  guide's currency sentence to "多幣別計費頁把新台幣（TWD）列為台灣的計費幣別" and left the ads lines.
- `chatgpt.com/zh-Hant/pricing/` returned 200 on 2026-10-05 but the NT$ amounts were not in the
  static HTML, so the static page cannot back a price figure; quote amounts only from a page that
  shows them.
- **Done 2026-10-06 (claude-opus-5-5-chatgpt-taiwan).** Pages re-read that day with `curl -sSL` and
  the editorial User-Agent, all HTTP 200: help.openai.com Multi-currency billing (10421635, lists
  "TWD (NT$) Taiwan"), Ads in ChatGPT (20001047, "Ads may appear for users on the Free and Go plans.
  Plus, Pro, Business, Enterprise, and Edu accounts will not have ads"; US testing began
  2026-02-09), ChatGPT Free Tier FAQ, What is ChatGPT Go, GPT-5.6 and GPT-6 Pro in ChatGPT, Is
  ChatGPT safe for all ages; openai.com/index/chatgpt-ads-expands-southeast-asia-taiwan (2026-09-23:
  rollout "across ... Taiwan", ads "only to users on the Free and Go plans", Plus, Pro and
  Enterprise ad-free), /introducing-chatgpt-go, /improving-gpt-5-6-sol-in-chatgpt,
  /policies/row-terms-of-use; developers.openai.com supported countries (Taiwan listed);
  learn.chatgpt.com/docs/pricing; minimax.io/blog/minimax-h3; hailuoai.video payment policy;
  platform.minimax.io Token Plan. No NT$ amount is quoted anywhere.
- ai-tools-2026-overview: the table intro now says the 9/13 prices are each site's listed currency
  (Google's Taiwan page in NT$, the others in USD), that the listed currency is not the billing
  currency, and that ChatGPT bills Taiwan in NT$ with the amount shown at checkout. The diagram
  footnote, the SVG `<desc>` and `image.description` say the same (description == `<desc>`, checked
  by script); the intro dates the currency re-check 10-06. Source swap: **dropped the MiniMax H3
  blog**, which backed only the clause "最新的模型 MiniMax H3 可以生成最長 15 秒、2K 解析度、帶原生
  立體聲的影片"; that clause was cut (the linked minimax-beginner-guide covers H3 in depth). The
  Speech 2.8 and Music 3.0 names it may also have backed are listed on the Token Plan page, re-read
  10-06, whose title and `checked_on` now say so. Not dropped: the OpenAI supported-countries page,
  the only source for "OpenAI 的支援地區名單有台灣" in the paragraph, the table and the diagram; every
  other source backs a fact nothing else in the pack carries. Added Multi-currency billing (10-06).
- chatgpt-beginner-guide: the ads list item now says OpenAI announced on 2026-09-23 that ChatGPT
  ads are rolling out in Taiwan, only on Free and Go, with Plus and Pro staying ad-free; the table's
  廣告 row reads Free "可能出現（台灣 2026 年 9 月 23 日起逐步推出）", Go "可能出現", Plus "沒有廣告"; the
  intro and the table caption date the ads re-check 10-06. Source swap: **dropped "Is ChatGPT safe
  for all ages" (8313401)**, because every age fact on the page (13+, under 18 needs a parent or
  guardian, in the text, the steps list and the diagram) is attributed to the Rest of World Terms
  of Use, re-read 10-06 (still "at least 13", "under 18 ... parent or legal guardian's permission",
  effective 2026-01-01), whose `checked_on` moved to 10-06. **Added the Taiwan announcement**
  rather than the Ads FAQ: one slot was free, and the announcement carries both the Taiwan start
  date and the Free/Go versus Plus/Pro split, while the FAQ (re-read the same day, it agrees) does
  not name Taiwan; the Free Tier FAQ already in the pack says ads may appear on Free "in certain
  countries" and links to the Ads FAQ. The Go launch post's source title no longer says 廣告測試,
  since no line rests on its January "US test soon" sentence any more.
- Conflict recorded: What is ChatGPT Go (11989085, "Updated: 2 hours ago" on 10-06) still says "We
  may start testing ads in ChatGPT Go in the future". The page follows the newer Ads FAQ and the
  Taiwan announcement; that source's title in the pack makes no ads claim.
- Checks (from `apps/api`): the How-to-verify grep (plus the SVG) returns nothing; `pack_cli lint
  --kind life` for both slugs with `--render-dir`: 0 errors, the same two `no_summary` warnings as
  origin/main, diagram PNG looked at (footnote on one line, clear of the credit); `intake_check.py
  --from-content` for both slugs: the same FAILs as origin/main (ai-tools 3, beginner 2: no summary
  first, a 6-column table, self-references), no new one; `pytest tests/test_guides_content_pack.py
  tests/test_guides_content_links.py`: 12 passed, 5 skipped (PostgreSQL). Both packs have 20
  sources with unique URLs.
- Left, filed as `2026-10-06-ai-tools-overview-gemini-s-has`: the ai-tools Gemini paragraph, table
  cell and diagram row still list "有台幣定價" as a Gemini strength, which now reads as "only
  Gemini"; outside the lines this ticket names.
- Publish after merge (coordinator, owner consent): `ai-tools-2026-overview`,
  `chatgpt-beginner-guide`.
