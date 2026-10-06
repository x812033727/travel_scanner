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

## Review round (independent, 2026-10-06)

- **Applied 2026-10-06** (claude-opus-5-5, apply pass; I wrote neither the PR nor the report
  below). The report's one finding was applied as suggested.
  - Block 22 of `ai-tools-2026-overview` now reads:
    「價格是 2026 年 9 月 13 日各家官網的數字：Google 用台灣方案頁的新台幣價，ChatGPT 寫的是美國定價，其他有標價的幾家也都用美元；ChatGPT 在台灣以新台幣計費，實際金額以官網為準。」
  - The diagram footnote (line 103), the SVG `<desc>` (after 「底注：」) and `image.description` now
    carry the new footnote verbatim (`image.description` == `<desc>`, checked by script):
    「價格為 2026 年 9 月 13 日各家官網數字：Google 是台灣頁的台幣價，ChatGPT 是美國定價，其餘是美元；ChatGPT 在台灣以新台幣計費，金額以官網為準；海螺 AI 各方案價格以官網為準。」
  - The report's headings are nested two levels down so they sit under this section; its text is
    otherwise unchanged.
  - No source added or dropped; the pack stays at 20. This supersedes the Done note's account of
    the table intro ("listed currency ... the others in USD ... not the billing currency").
- **Source re-opened for this pass** (`curl -sSL`, editorial UA): chatgpt.com/zh-Hant/pricing/,
  chatgpt.com/pricing/, openai.com/chatgpt/pricing/ and help.openai.com Multi-currency billing all
  returned 403 (Cloudflare challenge). archive.org has no capture of the zh-Hant pricing page.
  learn.chatgpt.com/docs/pricing (200) lists Go $8 and Plus $20 in USD and names no Taiwan or local
  currency. So the NT$ listing on ChatGPT's Taiwan page still rests on the 2026-09-30 reads in
  `chatgpt-plans-plus-pro-2026` and `ai-free-vs-paid-plans-2026`. The fix was applied anyway because
  the new wording asserts nothing about that page's listing currency: it labels the ChatGPT figures
  as US prices, as the table and the diagram already did, and keeps the NT$ billing fact the pack
  already sources.
- **Checks after the edit** (from `apps/api`): `pack_cli lint --kind life --slug
  ai-tools-2026-overview --slug chatgpt-beginner-guide --render-dir`: 0 errors, the same two
  `no_summary` warnings; diagram PNG looked at (footnote on one line, ending near x=1335, clear of
  the credit). `intake_check.py --from-content` for both slugs: the same FAILs as origin/main
  (ai-tools 3, beginner 2), none new. Both packs are zh-TW only, so no translation checks apply.

### verify-1: PR #1329 (claude/chatgpt-taiwan): ChatGPT bills Taiwan in NT$, ads on Free and Go

- Checker: independent round-1 fact-checker (claude-opus-5-5). I did not write this PR. Read-only: no edits, commits or comments.
- Date: 2026-10-06. All fetches used `curl -sSL` with UA `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`, at least 1 s apart per host, with no personal data. I did not use WebFetch or third-party readers, so every request carried the required UA.
- Diff: `git diff origin/main...origin/claude/chatgpt-taiwan`.
  - Changed: `ai-tools-2026-overview.json`, `chatgpt-beginner-guide.json`, `ai-tools-2026-overview/diagram-1.svg` and three ticket files.
  - Both packs are **zh-TW only**, so no per-locale review applies.

#### Fetch log

| URL | HTTP | Notes |
| --- | --- | --- |
| help.openai.com/en/articles/10421635-multicurrency-billing | 403 ×4 | Cloudflare challenge page (about 10 KB) |
| help.openai.com/en/articles/20001047-ads-in-chatgpt | 403 ×4 | Cloudflare challenge |
| help.openai.com/en/articles/11989085 (What is ChatGPT Go) | 403 | Cloudflare challenge |
| help.openai.com/en/articles/9275245-chatgpt-free-tier-faq | 403 | Cloudflare challenge |
| openai.com/index/chatgpt-ads-expands-southeast-asia-taiwan/ (+ zh-Hant) | 403 ×4 | Cloudflare challenge |
| openai.com/policies/row-terms-of-use/ | 403 | |
| openai.com/index/introducing-chatgpt-go/ | 403 | |
| chatgpt.com/zh-Hant/pricing/, chatgpt.com/pricing/ | 403 | |
| openai.com/news/rss.xml | 200 | 1,247 items; Taiwan item pubDate Wed, 23 Sep 2026 02:00:00 GMT |
| openai.com/sitemap.xml/product/ | 200 | Taiwan announcement lastmod 2026-10-06T11:40:05.728Z; the page now has hreflang alternates |
| archive.org/wayback/available | 200 | Captures exist: Ads FAQ 2026-10-04, Go 2026-09-11, Free Tier FAQ 2026-09-23. None for Multi-currency billing, the Taiwan announcement or ROW ToU |
| web.archive.org (snapshots, CDX) | — | HTTPS connection reset ×5; HTTP "Blocked by egress policy" |
| platform.minimax.io/docs/guides/pricing-token-plan | 200 | |
| hailuoai.video/doc/payment-policy.html | 200 | |
| gemini.google/tw/subscriptions/ | 200 | Redirects to ?hl=zh-TW |
| claude.com/pricing | 200 | |
| support.claude.com/en/articles/8325606-what-is-the-pro-plan | 200 | |
| learn.chatgpt.com/docs/pricing | 200 | |

#### Claim table

| # | Claim (location) | Source | HTTP | Verdict |
| --- | --- | --- | --- | --- |
| 1 | Overview intro: ChatGPT billing currency re-checked 10-06 | — | — | OUT OF SCOPE: a dating line. Adds verification narration (see reader-first) |
| 2 | Overview MiniMax: free users can generate videos; downloads carry a watermark | Hailuo payment policy | 200 | CONFIRMED: "Free Users … download videos that include a watermark" |
| 3 | Overview MiniMax: H3 clause and its source removed; nothing else in the pack or SVG mentions H3, 15 秒, 2K or 立體聲 | grep of pack and SVG | — | CONFIRMED: no orphaned dependants. H3 is still listed on MiniMax's site, so this is only a cut, not a correction |
| 4 | Overview MiniMax: Speech 2.8 and Music 3.0 names, now backed by the Token Plan page | Token Plan | 200 | CONFIRMED: the site navigation lists "MiniMax Speech 2.8" and "MiniMax Music 3.0" (also M3, H3) |
| 5 | Token Plan Plus $22 / Max $55 / Ultra $132 (body, diagram; checked_on moved to 10-06) | Token Plan | 200 | CONFIRMED: "Plus Max Ultra Price $22 /month $55 /month $132 /month" |
| 6 | Token Plan source title: "頁面列出 M3、Speech 2.8、Music 3.0 等模型" | Token Plan | 200 | CONFIRMED |
| 7 | Table intro: "Google 的台灣方案頁直接以新台幣標價" | gemini.google/tw/subscriptions | 200 | CONFIRMED: 每月 NT$ 165 元, NT$ 650 元, NT$ 3300 or 6500 元 |
| 8 | Table intro: "其他有標價的幾家都用美元" | claude.com/pricing; learn.chatgpt.com; Token Plan | 200 | PARTLY CONFIRMED. Claude ($20/$17), the ChatGPT US doc ($8/$20) and Token Plan are in USD. But **ChatGPT's Taiwan pricing page lists NT$** according to two packs on main (checked 2026-09-30), so ChatGPT does not belong in "lists in USD". **CONSISTENCY finding**, see below |
| 9 | Table intro: "標價幣別不等於扣款幣別，ChatGPT 在台灣就以新台幣計費" | Multi-currency billing | 403 | NOT CHECKED FIRST-HAND. The NT$ billing fact agrees with three packs that read it on 09-30 and 10-05. The "listed ≠ billed" example is part of the consistency finding |
| 10 | "實際金額以結帳頁為準" | — | — | OUT OF SCOPE (hedge) |
| 11 | Diagram footnote says the same as the table intro | SVG line 103 | — | CONFIRMED (same consistency issue as #8) |
| 12 | image.description equals the SVG `<desc>` verbatim | script | — | CONFIRMED (True) |
| 13 | Multi-currency billing source title "含台灣的新台幣 TWD", checked_on 10-06 | help.openai.com | 403 | NOT CHECKED FIRST-HAND |
| 14 | Overview: 20 sources, all URLs unique | script | — | CONFIRMED |
| 15 | Beginner list: "OpenAI 在 2026 年 9 月 23 日宣布" | OpenAI RSS | 200 | CONFIRMED: pubDate 23 Sep 2026 02:00 GMT (10:00 Taipei, 9/23) |
| 16 | Beginner list: ads "開始在台灣逐步推出" | RSS; announcement | 200 / 403 | PARTLY CONFIRMED: RSS says "expanding to Southeast Asia and Taiwan". The "begin rolling out" wording could not be read today; it matches the 2026-09-26 verbatim record |
| 17 | Beginner list: "只會出現在 Free 與 Go 方案" | announcement | 403 | NOT CHECKED FIRST-HAND. Matches the 09-26 record: "ads will be shown only to users on the Free and Go plans" |
| 18 | Beginner list: "Plus、Pro 維持沒有廣告" | announcement | 403 | NOT CHECKED FIRST-HAND. Matches the 09-26 record: "Plus, Pro, and Enterprise subscriptions will remain ad-free" |
| 19 | Table Free: "可能出現（台灣 2026 年 9 月 23 日起逐步推出）" | RSS; Ads FAQ | 200 / 403 | Date CONFIRMED; the rest as #16 and #17 |
| 20 | Table Go: "可能出現" | Ads FAQ; Go help page | 403 / 403 | NOT CHECKED FIRST-HAND. Handling of the conflict judged fair (below) |
| 21 | Table Plus: "沒有廣告" | announcement | 403 | As #18 |
| 22 | Intro and caption: ads re-checked 10-06 | — | — | OUT OF SCOPE (dating). The announcement page changed after the writer's read (#31) |
| 23 | Taiwan announcement source title (date, Free/Go, Plus/Pro ad-free) | RSS; page | 200 / 403 | Title and date CONFIRMED; the rest as #17 and #18 |
| 24 | Go launch post title: "廣告測試" removed | — | — | CONFIRMED: no remaining line relies on it |
| 25 | ROW ToU checked_on moved to 10-06; age facts 13+, under 18 needs parental consent, effective 2026-01-01 | openai.com | 403 | NOT CHECKED FIRST-HAND |
| 26 | Dropping 8313401 leaves no age fact without a source: the text attributes ages to the ToU, and the diagram repeats the same facts | pack text | — | CONFIRMED |
| 27 | Beginner: 20 sources, all URLs unique | script | — | CONFIRMED |
| 28 | The beginner diagram has no stale ads text | SVG grep | — | CONFIRMED (none) |
| 29 | The overview has no other ChatGPT ads line that could be stale | pack grep | — | CONFIRMED (only DeepSeek "無廣告") |
| 30 | Go ads source conflict handled fairly | see below | — | JUDGED FAIR |
| 31 | Time-sensitive: the Taiwan announcement page changed 2026-10-06T11:40Z, after the writer's read (ticket closed 01:43Z) | sitemap | 200 | NOTE: re-read before publishing |

#### Finding (1, consistency)

**ai-tools-2026-overview: the table intro and the diagram footnote still say, in effect, that only Google lists NT$.**

- **Where:** block 22, plus the diagram footnote, the SVG `<desc>` and `image.description`.
- **What it says:** 「Google 的台灣方案頁直接以新台幣標價，其他有標價的幾家都用美元。標價幣別不等於扣款幣別，ChatGPT 在台灣就以新台幣計費」.
- **Why it is wrong:** it groups ChatGPT with the sites that list in USD. It then uses ChatGPT as the example of a listed price that differs from the billing currency. Other sources disagree:
  - chatgpt-plans-plus-pro-2026: 「台灣定價頁以新台幣標價：Go 每月 NT$270、Plus 每月 NT$690」.
  - ai-free-vs-paid-plans-2026: 「台幣為 ChatGPT 與 Gemini 的台灣定價頁標價」.
  - Both cite https://chatgpt.com/zh-Hant/pricing/ (checked 2026-09-30). The writer's own follow-up ticket also says ChatGPT's Taiwan pricing page shows NT$.
- **Where the USD figure comes from:** this pack's ChatGPT figure is the US price, already labelled 「（美國定價）」.
- **Suggested fix:**
  - Text: 「價格是 2026 年 9 月 13 日各家官網的數字：Google 用台灣方案頁的新台幣價，ChatGPT 寫的是美國定價，其他有標價的幾家也都用美元；ChatGPT 在台灣以新台幣計費，實際金額以官網為準。」
  - Footnote, `<desc>` and `image.description`, kept verbatim-equal: 「價格為 2026 年 9 月 13 日各家官網數字：Google 是台灣頁的台幣價，ChatGPT 是美國定價，其餘是美元；ChatGPT 在台灣以新台幣計費，金額以官網為準；海螺 AI 各方案價格以官網為準。」
  - This matches chatgpt-beginner-guide's 月費 row and needs no new source.
- **Severity:** consistency, not fact. ChatGPT's pricing page returned 403 today, so I could not confirm today's NT$ listing first-hand.

#### Go ads source conflict: judgement

- **The conflict:** according to the writer, What is ChatGPT Go (11989085) still says Go ads are a possible future test. The 2026-09-23 Taiwan announcement and the Ads FAQ (updated 2026-09-26 per the repo record) both say ads appear on Free and Go.
- **How the article handles it:**
  - The list item attributes the Free/Go statement to the 9/23 announcement by name. That attribution is correct: the date and title are confirmed via RSS, and the wording matches the verbatim 09-26 record.
  - The table cell for Go is hedged as 「可能出現」, which matches the FAQ's "may appear".
  - The Go help page stays in `sources`, but its title makes no ads claim.
- **Verdict:** fair. The article follows the newer, more specific Taiwan source, does not overstate (no "every Go user sees ads"), and does not lean on the stale page. I could not read the Go page or the FAQ today, so the conflict itself rests on the writer's note.
- **Minor, not filed:** the table gives the Taiwan start date only in the Free cell; the Go cell is bare 「可能出現」, although the rollout covers both. The list item above makes this clear.

#### Reader-first (report only)

- **Dating in prose:** the PR adds more verification dating to the body.
  - Overview intro: 「ChatGPT 的計費幣別在 10 月 6 日重新查過」.
  - Beginner intro: 「廣告在 10 月 6 日重新查過」.
  - Beginner caption: 「廣告列 10 月 6 日重查」.
  - The intros already carried 10-05 dating lines.
- **Self-references:** 這篇/本文 appears 2 times in each pack. Both predate this PR.
- **New sentences:** no untranslated foreign quotes, and the new zh-TW sentences read naturally.

#### Self-checks

- Not run: the clone has no `apps/api/.venv`, and creating one or a worktree would write into the repo, which this read-only task forbids.
- Checked by script instead: `<desc>` == `image.description` (True), 20 unique sources per pack, and no H3 or 15 秒 / 2K leftovers.
- Footnote fit, estimated: about 75 CJK characters × 15 px from x=60 is about 1,185 px, clear of the credit at y=870.

#### Unverifiable today

- **OpenAI pages:** every help.openai.com, openai.com and chatgpt.com page cited for the PR's core claims returned 403. That covers NT$ billing, Free/Go only, Plus/Pro ad-free, the Go conflict, and the ToU ages.
- **Wayback:** the archive copies exist but web.archive.org is unreachable from this environment.
- **RSS:** confirms only the title, date and "expanding to … Taiwan".

#### Summary

- **Claims:** 30 checked. 14 confirmed (some partly), 0 changed, 1 consistency finding, 9 not checked first-hand (403 on official pages), 5 out of scope (dating lines and hedges), 1 judgement (Go conflict: fair).
- **Second round:** not required by the rule (0 fact changes). However, the central OpenAI claims could not be read first-hand today, and the Taiwan announcement page changed at 2026-10-06T11:40Z, after the writer's read. Before publishing, someone should re-read the announcement, the Ads FAQ and Multi-currency billing from an environment where help.openai.com and openai.com return 200, or in a real browser.
- **Suspected but not filed (outside this PR's lines):**
  - The overview's Gemini 「有台幣定價」 strength (the writer filed a ticket for it).
  - Claude also bills in local currency where supported ("$20 per month (US), with pricing in your local currency where supported"). Whether that includes TWD is unknown, so I left it alone.
  - ai-free-vs-paid-plans-2026 contradicts itself: 「Gemini 是三家裡唯一在台灣頁直接標台幣的」 vs 「台幣為 ChatGPT 與 Gemini 的台灣定價頁標價」. Outside this PR's scope; worth a ticket.

### verify-2: PR #1329 (claude/chatgpt-taiwan): ChatGPT bills Taiwan in NT$, ads on Free and Go

#### Scope and method

- **Checker:** independent round-2 fact-checker (claude-opus-5-5). I wrote neither the PR, round 1, nor the fix. This was a read-only pass: no edits, commits or comments.
- **Date:** 2026-10-06.
- **Branch head:** fetched again: `ec1635fe` ("content: apply independent fact-check round 1 for #1329").
- **Diff:** `git diff origin/main...origin/claude/chatgpt-taiwan`.
  - Content files: `ai-tools-2026-overview.json`, `chatgpt-beginner-guide.json`, `ai-tools-2026-overview/diagram-1.svg`.
  - Plus three ticket files.
  - Both packs are **zh-TW only**, so there is no other locale to check.
- **Fetching:** every fetch used `curl -sSL` with UA `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`, at least 1.2 s apart per host. No personal data went into any header, query or form.
  - I stripped `<!-- -->`, `<script>` and `<style>` before reading.
  - I made no WebFetch or third-party reader calls.
  - I made 3 WebSearch calls (domains limited to help.openai.com or openai.com). I used them only as hints, never as confirmation.
- **What round 2 covered:** every round-1 correction, plus **all** other changed claims I could reach. That is more than the required random third, because of the PR-specific instruction to check every changed sentence.

#### Fetch log

| URL | HTTP | Notes |
| --- | --- | --- |
| help.openai.com: 10421635 Multi-currency billing (en and zh-hant), 20001047 Ads in ChatGPT, 11989085 What is ChatGPT Go, 9275245 Free Tier FAQ, 6825453 release notes | 403 | Cloudflare challenge page (about 10 KB) |
| openai.com/index/chatgpt-ads-expands-southeast-asia-taiwan/ (en and zh-Hant), /index/introducing-chatgpt-go/, /policies/row-terms-of-use/ | 403 | Cloudflare |
| chatgpt.com/zh-Hant/pricing/, /pricing/, /plans/free/, /plans/go | 403 | Cloudflare |
| ads.openai.com, ads.openai.com/assets/openai-geotargets.csv | 403 | Cloudflare |
| openai.com/news/rss.xml | 200 | 1,248 items |
| openai.com/sitemap.xml/product/ | 200 | Taiwan announcement lastmod is now **2026-10-06T16:52:07Z**; round 1 saw 11:40Z |
| archive.org/wayback/available | 200 | Captures exist (Ads FAQ and Taiwan post 2026-10-04, Multi-currency 2026-09-18, Go page 2026-09-11) |
| web.archive.org id_ snapshots, archive.ph | — | Connection reset |
| learn.chatgpt.com/docs/pricing, /ads, /ads/campaign-targeting, /ads/location-targeting, /ads/account-management, /ads/troubleshooting | 200 | Advertiser docs; nothing on which user plans see ads |
| gemini.google/tw/subscriptions/ | 200 | Redirects to ?hl=zh-TW |
| claude.com/pricing | 200 | |
| hailuoai.video/doc/payment-policy.html | 200 | |
| platform.minimax.io/docs/guides/pricing-token-plan | 200 | |
| developers.openai.com/api/docs/supported-countries | 200 | |

#### A. Round-1 correction, re-checked on ec1635fe

The fix commit changed only four lines plus the ticket:

- block 22 of the overview pack;
- `image.description` (block 24);
- SVG line 3 (`<desc>`);
- SVG line 103 (the footnote).

The SVG `<desc>` text before 「底注：」 is byte-identical to origin/main. No source was added or removed, so the pack still has 20 unique URLs.

| # | Claim | Source | HTTP | Verdict |
| --- | --- | --- | --- | --- |
| 1 | Block 22 now reads 「價格是 2026 年 9 月 13 日各家官網的數字：Google 用台灣方案頁的新台幣價，ChatGPT 寫的是美國定價，其他有標價的幾家也都用美元；ChatGPT 在台灣以新台幣計費，實際金額以官網為準。」 | script compare | — | CONFIRMED: matches the round-1 suggestion verbatim. It no longer says ChatGPT lists prices in USD |
| 2 | "Google 用台灣方案頁的新台幣價" (table: AI Plus 165 元, AI Pro 650 元) | gemini.google/tw/subscriptions | 200 | CONFIRMED: 「每月 NT$ 165 元」, 「每月 NT$ 650 元」 (Ultra NT$ 3300 / 6500) |
| 3 | "ChatGPT 寫的是美國定價" (Go 8 美元, Plus 20 美元; table and diagram already say 「（美國定價）」) | learn.chatgpt.com/docs/pricing | 200 | CONFIRMED: "Go … $8 /month", "Plus … $20 /month" |
| 4 | "其他有標價的幾家也都用美元" (Claude Pro $20 / $17 annual, Codex via Plus $20, Token Plan Plus $22) | claude.com/pricing; learn.chatgpt.com; Token Plan page | 200 | CONFIRMED: "$17 Per month with annual subscription discount … $20 if billed monthly"; "$22 /month" |
| 5 | "ChatGPT 在台灣以新台幣計費" | Multi-currency billing | 403 | UNVERIFIABLE first-hand. Consistent with chatgpt-beginner-guide (10-05), chatgpt-plans-plus-pro-2026 and ai-free-vs-paid-plans-2026 (09-30). A search-index summary of the page also lists "TWD (NT$)" for Taiwan |
| 6 | Footnote (line 103) equals the round-1 suggestion; the `<desc>` tail after 底注 equals the footnote; `image.description` equals `<desc>` | script | — | CONFIRMED (all three True) |
| 7 | Footnote fits | width estimate | — | CONFIRMED (estimate). 105 characters at 15 px end near x≈1325 of 1600, matching the fixer's render (≈1335). The footnote baseline is y=850 and the credit's is y=870, so they do not collide. There is no Chromium or CJK font here, so I did not re-render |
| 8 | Fix adds no number missing from the body | script | — | CONFIRMED: footnote numbers {2026, 9, 13} all appear in the body. No `diagram_number_not_in_text` risk |

- **Verdict on the round-1 fix:** correct. It matches chatgpt-beginner-guide's own 月費 row (「美國 8 美元；台灣以新台幣計費，金額以官網為準」) and the three sibling packs.
- **Nothing new introduced:** I found no new problem.

#### B. Other changed claims

##### ai-tools-2026-overview

| # | Claim | Source | HTTP | Verdict |
| --- | --- | --- | --- | --- |
| 9 | Intro: 「ChatGPT 的計費幣別在 10 月 6 日重新查過」 | — | — | OUT OF SCOPE: a dating line (reader-first note below) |
| 10 | 「免費使用者可以生成影片，但下載的影片會有浮水印」 | Hailuo payment policy | 200 | CONFIRMED: "Free Users: … download videos that include a watermark" |
| 11 | Paid tiers from low to high: Standard, Pro, Master, Ultra, Max | Hailuo payment policy | 200 | CONFIRMED: $14.99 / $54.99 / $119.99 / $124.99 / $199.99. The legacy Unlimited plan is omitted, which is fine |
| 12 | 「每月配給的點數月底歸零」 | Hailuo payment policy | 200 | CONFIRMED in substance: "valid for one month and expire thereafter. Unused credits do not roll over". This wording predates the PR |
| 13 | H3 clause and the minimax.io/blog/minimax-h3 source removed; nothing left depends on them | grep of pack and SVG | — | CONFIRMED: H3, 15 秒, 2K and 立體聲 each appear 0 times. H3 is still current on MiniMax's site, so this is a cut, not a correction |
| 14 | Speech 2.8, Music 3.0 and M3 names, now backed by the Token Plan page | Token Plan page | 200 | CONFIRMED: navigation lists "MiniMax M3 … MiniMax Speech 2.8 MiniMax H3 MiniMax Music 3.0" |
| 15 | Token Plan Plus $22 / Max $55 / Ultra $132; checked_on 2026-10-06; new title text | Token Plan page | 200 | CONFIRMED: "Plus Max Ultra Price $22 /month $55 /month $132 /month" |
| 16 | New source: Multi-currency billing (「含台灣的新台幣 TWD」, checked_on 10-06) | help.openai.com | 403 | UNVERIFIABLE first-hand |
| 17 | 20 sources, all URLs unique | script | — | CONFIRMED |

##### chatgpt-beginner-guide

| # | Claim | Source | HTTP | Verdict |
| --- | --- | --- | --- | --- |
| 18 | Intro: 「廣告在 10 月 6 日重新查過」 | — | — | OUT OF SCOPE: dating |
| 19 | 「OpenAI 在 2026 年 9 月 23 日宣布」 | OpenAI RSS | 200 | CONFIRMED: pubDate "Wed, 23 Sep 2026 02:00:00 GMT" (10:00 Taipei) |
| 20 | 「ChatGPT 廣告開始在台灣逐步推出」 | RSS; announcement | 200 / 403 | PARTLY CONFIRMED. RSS: "ChatGPT Ads is expanding to Southeast Asia and Taiwan". The "begin rolling out" wording matches the repo's 2026-09-26 verbatim record (docs/ai-news-2026-09-late/research/…20260923.json) but could not be read today |
| 21 | 「只會出現在 Free 與 Go 方案」 | announcement | 403 | UNVERIFIABLE first-hand. The 09-26 record has "ads will be shown only to users on the Free and Go plans". The official RSS description of OpenAI's 2026-01-16 post ("test advertising in the U.S. for ChatGPT's free and Go tiers") independently shows the Go tier was in scope from the start |
| 22 | 「Plus、Pro 維持沒有廣告」 | announcement | 403 | UNVERIFIABLE first-hand. The 09-26 record has "Plus, Pro, and Enterprise subscriptions will remain ad-free" |
| 23 | Table, Free: 「可能出現（台灣 2026 年 9 月 23 日起逐步推出）」 | RSS | 200 | Date CONFIRMED; the rest as #20 and #21 |
| 24 | Table, Go: 「可能出現」 | Ads FAQ; Go page | 403 / 403 | UNVERIFIABLE first-hand. Conflict judged below |
| 25 | Table, Plus: 「沒有廣告」 | announcement | 403 | As #22 |
| 26 | Caption: 「廣告列 10 月 6 日重查」 | — | — | OUT OF SCOPE: dating |
| 27 | Taiwan announcement source title (date, Free/Go, Plus/Pro ad-free) | RSS | 200 | Title and date CONFIRMED; the rest as #21 and #22 |
| 28 | ROW ToU: checked_on moved to 10-06; ages 13+, under 18 needs a parent or guardian, effective 2026-01-01 | openai.com | 403 | UNVERIFIABLE first-hand |
| 29 | Dropping "Is ChatGPT safe for all ages" (8313401) leaves no orphaned fact | pack text | — | CONFIRMED: block 4, the steps list and the diagram attribute ages to the ToU; the age-prediction sentences keep their own source |
| 30 | Go launch-post source title loses 「廣告測試」; no line relies on it | pack text | — | CONFIRMED: blocks 11 and 12 cite that post only for the $8 price and 10× limits |
| 31 | No stale ads text left (both packs, both diagrams) | grep | — | CONFIRMED: none of 以美元計, 台幣定價的只有, 先在美國測試, 部分國家, 未來可能測試 or 官網未提及; the beginner SVG has no ads text |
| 32 | 20 sources, all URLs unique | script | — | CONFIRMED |
| 33 | Go ads source conflict handled fairly | see below | — | JUDGED FAIR |
| 34 | Matches sibling packs | packs on the branch | — | CONSISTENT: chatgpt-ads-status, ai-news-chatgpt-ads-taiwan-20260923 (5 locales), chatgpt-plans-plus-pro-2026 and ai-free-vs-paid-plans-2026 all say Free and Go may see ads, Plus and above do not, and Taiwan rollout began 9/23 |

#### Go ads conflict: judgement

- **The conflict:**
  - What is ChatGPT Go (11989085) still says Go ads may be tested "in the future". The writer read this on 10-06, and today's search-index summary of the page agrees.
  - Against it stand the 2026-09-23 Taiwan announcement ("only to users on the Free and Go plans") and the Ads FAQ ("Ads may appear for users on the Free and Go plans"). Both are recorded verbatim in the repo on 09-26, and the writer re-read them on 10-06.
  - OpenAI's own RSS also describes the January plan as testing ads "for ChatGPT's free and Go tiers".
- **How the article handles it:**
  - The list item ties the Free/Go statement to the dated 9/23 announcement, by name.
  - The Go table cell is hedged as 「可能出現」, which mirrors the FAQ's "may appear".
  - The stale Go page stays in `sources` with a title that makes no ads claim.
- **Verdict:** fair. The article follows the newer, Taiwan-specific sources, does not overstate (it never says every Go user sees ads), and matches four sibling packs.
- **Minor, not filed:** the Taiwan start date appears only in the Free cell, although the rollout covers Go too. The list item directly above makes this clear.

#### Reader-first (report only, unchanged from round 1)

- The PR adds three more verification-dating phrases:
  - overview intro: 「ChatGPT 的計費幣別在 10 月 6 日重新查過」;
  - beginner intro: 「廣告在 10 月 6 日重新查過」;
  - beginner caption: 「廣告列 10 月 6 日重查」.
- 這篇/本文 appears twice in each pack. Both predate this PR.

#### Self-checks

These ran on a scratchpad copy of the branch head made with `git archive`; nothing was written in the repo. Dependencies were installed with `uv sync --frozen`.

- **`pack_cli lint --kind life --slug ai-tools-2026-overview --slug chatgpt-beginner-guide`:** exit 0, 0 errors. Two `no_summary` warnings, the same as origin/main.
- **`intake_check.py --from-content`:**
  - ai-tools: 3 FAILs (no summary first, 6-column table, self-reference ×2).
  - beginner: 2 FAILs (no summary first, self-reference ×2).
  - Both are **identical to origin/main**, which I ran the same way. No new FAIL.
- **pytest `tests/test_guides_content_pack.py`:** 7 passed, 5 skipped, 2 failed. The failures are environmental only: the partial extraction lacks other slugs' hero images (for example `accident-insurance-basics/hero.jpg`). Neither failure involves the two PR slugs.

#### Summary

- **Totals:** 34 claims checked.
  - 20 confirmed (1 of them partly).
  - 0 errors.
  - 9 unverifiable first-hand: OpenAI, help center and chatgpt.com all return 403, and archives are unreachable.
  - 4 out of scope (dating lines).
  - 1 judgement: the Go conflict is handled fairly.
- **Round-1 correction:** applied exactly as suggested, correct, and nothing new introduced.
- **Time-sensitive:**
  - The Taiwan announcement's sitemap lastmod moved again today, to 2026-10-06T16:52Z. Eight other openai.com pages were also modified today, so this is likely a rebuild.
  - OpenAI also published a new ads-format post on 2026-10-05 (RSS). Its description is about advertisers and does not touch which plans see ads.
  - Before publishing, re-read the Taiwan announcement, the Ads FAQ and Multi-currency billing from a place where openai.com and help.openai.com return 200, or in a real browser.
- **Suspected but not changed** (no first-hand source, or outside the changed lines):
  1. **Existing subscribers:** a search-index summary of Multi-currency billing says existing subscribers keep being billed in their current currency until they re-subscribe. 「ChatGPT 在台灣以新台幣計費」 is therefore a simplification for people who subscribed before TWD support. I could not read the page, so this is not filed as an error.
  2. **Loose currency wording:** the overview table caption 「價格為官網幣別」 and the intro 「文中價格寫的是官網當天的幣別」 are loose now that the ChatGPT row is explicitly a US price. The cell itself says 「（美國定價）」. Both lines predate the PR.
  3. **Hailuo credits:** 「點數月底歸零」 against the policy's "valid for one month" is wording that predates the PR; the substance agrees.
  4. **Gemini 「有台幣定價」 strength:** already filed as tasks/open/2026-10-06-ai-tools-overview-gemini-s-has.md.

#### Sources read today (HTTP 200)

- https://openai.com/news/rss.xml
- https://openai.com/sitemap.xml/product/
- https://learn.chatgpt.com/docs/pricing
- https://learn.chatgpt.com/ads/location-targeting
- https://gemini.google/tw/subscriptions/
- https://claude.com/pricing
- https://hailuoai.video/doc/payment-policy.html
- https://platform.minimax.io/docs/guides/pricing-token-plan
- https://developers.openai.com/api/docs/supported-countries
- https://archive.org/wayback/available
