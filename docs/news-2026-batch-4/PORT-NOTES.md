# Porting the batch-3 authoring tooling to news batch 4

Source: `docs/ai-news-2026-09-mid/` (batch 3, one vertical, one workspace, one index).
Target: `docs/news-2026-batch-4/`, serving three verticals whose workspaces are
`docs/crypto-news-2026/`, `docs/tech-news-2026/` and `docs/ai-news-2026-09-late/`.

Spec read: `docs/news-2026-batch-4/BRIEF.md`, `crypto.md`, `tech.md`, `ai.md`.
Code read: `apps/api/app/guides/schemas.py`, `pack_ingest.py`, `content_pack.py`,
`taxonomy.py`, plus `apps/api/app/guides/content/ai-news-siri-ai-ios-27-20260914.json`
and `docs/ai-news-2026-09-mid/research/ai-news-openai-agents-api-20260910.json`.

## The one thing that is not in the brief, and changes every script

Batch 3's checker no longer passes batch 3's own shipped articles. Run today:

```
$ cd apps/api && uv run python ../../docs/ai-news-2026-09-mid/check_article.py \
      ai-news-siri-ai-ios-27-20260914 --full
FAIL
 - topics ['ai', 'gadgets', 'ai-news']
 - event date not in the opening paragraphs
 - blocks must end callout, link, link
 - two opening paragraphs
 - en block types differ from zh-TW
 - ja block types differ from zh-TW
 - ko block types differ from zh-TW
 - zh-CN block types differ from zh-TW
```

Nothing is wrong with the article. Two things moved under the scripts:

1. **`pack_cli relink` / `autolink` ran after publication.** A paragraph that gained an
   `article` inline is now a `rich_paragraph`, and the two closing `link` blocks are
   `rich_paragraph`s holding one `article` inline. It happens per locale, so zh-TW block 0
   is a `rich_paragraph` while the same block in en is still a `paragraph` — which is why
   the four "block types differ from zh-TW" lines appear. `BRIEF.md` tells batch 4 to run
   both tools, so batch 4's finished packs have exactly this shape.
2. **The topic taxonomy grew.** `ai-news` is a real subtopic (`LIFE_SEED_SUBTOPICS`), but
   batch 3 hardcoded the eight hubs and rejects it.

So every script here compares a block's **role**, not its stored type
(`verticals.block_kind`), and reads the taxonomy from `app.guides.taxonomy`. A port that
kept batch 3's assumptions would have failed on the first article of batch 4.

## New file: `verticals.py`

The vertical-awareness change cuts across all five scripts — each one needs the same answer
to "which vertical is this slug, which workspace, which index". One shared module instead of
five copies. It is not a package: the scripts sit beside it and Python puts a script's own
directory on `sys.path` first, so `import verticals` works from any working directory, the
way batch 3's `_load()` worked for the art modules. It also does the
`sys.path.insert(ROOT / "apps/api")` every script needed.

It holds the `Vertical` table (prefix, workspace, index, required topics, hero eyebrow,
accent, `display_order` base), the role-aware block helpers, and the per-locale disclaimer
markers. It does **not** hold a callout count: how many callouts an article carries follows
from the pack's own topics, the way `pack_ingest._finance_problems` keys on them, so an
ai-news article that carries `finance` needs the disclaimer and the second callout too.

`MOKAAIR_ROOT` overrides the repository root. It is one documented line and it is how the
tooling is exercised from a scratchpad: every test below ran against a sandbox root whose
`apps/api/app` is a copy, so nothing here has ever written to the real content directory.

The scripts' own directory carries a `.gitignore` with `renders/` and `__pycache__/`, copied
from `docs/ai-news-2026-09-mid/.gitignore`. Five of the six scripts `import verticals`, so a
`__pycache__/` appears beside them the first time any of them runs.

## `check_article.py`

**New checks, as specified**

| | |
| --- | --- |
| a | a `summary` exists **per locale**, carries 2–5 sentences, and sits before the first heading. Also: it must not simply repeat `description`, and every number in it must appear in the body — `BRIEF.md` is explicit that an answer engine must not be able to quote a number the article never states. "The body" is `pack_ingest._body_parts`, the site's own idea of running text: paragraphs, lists, tables, callouts and the FAQ, but **not** the title or the description, so a figure the writer states only in the 120–200 character description does not stand in for the article stating it. |
| b | a `faq` exists **per locale** with 2–10 question/answer pairs, and no answer contains a URL (`BRIEF.md`: answers are plain text). |
| c | a finance/investing/crypto article carries a callout with a disclaimer marker, **per locale**, in that locale's own wording. |
| d | `news_date` is present and equals the slug's date suffix. |

The bounds in (a) and (b) are not retyped either: they are read off `SummaryBlock.items` and
`FaqBlock.items` as `annotated_types` metadata, the way `update_index.MAX_SOURCES` reads the
source cap, and `HERO_SIZE` is imported for the hero dimensions. Those three rules sit behind
`ArticlePack.model_validate`, which refuses a sixth summary sentence first, so a copy of the
numbers would have drifted without anything ever failing.

For (c) the constants are imported, not retyped: `FINANCE_TOPICS` and
`FINANCE_DISCLAIMER_MARKERS` come from `pack_ingest`, and `verticals.locale_markers()`
asserts its locale→marker map covers exactly that tuple, so a marker edited there cannot
silently disagree here. The stricter per-locale rule exists because `lint_document` lints
one document at a time and is **not told which locale it is reading** — a translation that
kept the zh-TW sentence passes the linter and still reads as untranslated boilerplate, which
is the failure `crypto.md` is warning about.

Batch 3 also called `lint_document(zh, "life")` **without `topics`**, so `finance_no_disclaimer`
never ran at all. It is now called with `topics=pack.topics` in every locale.

**Other changes**

- Vertical-aware: workspace, index slug, required topics and `display_order` band all come
  from the slug prefix. The expected callout count does **not**: it follows the pack's own
  topics (one callout, or two when a `finance`/`investing`/`crypto` topic brings the
  disclaimer), which is what the site keys on. `crypto.md` and the AI ticket's B8
  (「ChatGPT for Financial Services（帶 finance，必附免責）」) disagree with `ai.md`'s
  「AI 篇不帶 `finance` 主題」 about whether an ai-news article may carry `finance`; the rule
  here is right under either reading, and the editorial decision is filed as
  `tasks/open/2026-09-16-ai-md-and-b8-disagree-about.md`.
- Block order follows `BRIEF.md`'s new list: `paragraph, paragraph, summary, …, faq,
  callout[, callout], link, link`, compared by role. Sections must hold 2–4 paragraphs.
- Topics validated against `LIFE_SEED_TOPICS`/`LIFE_SEED_SUBTOPICS`, including "a subtopic
  needs its parent hub in the list".
- `checked_on` is no longer a frozen batch constant. `BRIEF.md` says it is the day the
  writer actually verified, and batch 4 runs over weeks, so the research record is the
  source of truth: every source in every locale must match it, it must fall between the
  event date and today, and it must appear in the opening paragraphs.
- `description` 120–200 (batch 3 checked 100–220; `BRIEF.md` moved it).
- A missing research record, an unwritten index and a model validation error are reported
  as a `FAIL` line instead of a traceback.
- `--assets` now also runs `check_svg` and `missing_diagram_numbers` from `pack_ingest` on
  the published SVGs — batch 3 only checked existence and a hardcoded 300 KB. The byte caps
  are `pack_ingest`'s own two levels: over `IMAGE_HARD_CAP` (300 KB) is a failure, a hero over
  the editorial `HERO_MAX_BYTES` (200 KB) is a `WARN` line and exit 0, exactly as
  `image_too_large` and `hero_over_guideline` are graded there. Failing a hero at 200 KB, as
  batch 3 did, is stricter than the site itself and stricter than `build_assets.py`, which
  `fit_bytes` lets write up to the hard cap rather than lose 1600×900.
- The research record is checked for everything `build_assets.py` reads from it, not a part of
  it: per locale, `hero_label`, the diagram's `title`, its four nodes and its `caption`, with
  the translated title held to the same 21 CJK units as zh-TW times the locale's slack. A
  record missing `translations[locale].diagram.title` used to pass the check and then kill the
  drawing step with a bare `KeyError`.
- `research.unverified_or_excluded` must be non-empty (`BRIEF.md`: a blank one is suspect,
  not clean).
- Batch 3's exact locale comparison is kept: without `--full` the pack must carry **only**
  zh-TW, so once the translations are merged the run is `--full` and a bare run reports
  `locales ['zh-TW', 'en', …] != ['zh-TW']`. Mid-article that is the right answer — the writer
  is told which locales are there — but it does mean `--full` is not optional at the end.

**Deliberately kept, unchanged:** structure and word counts, the simplified-Chinese scan,
event date vs checked date in the opening paragraphs, tables at most 4 columns and 3–6 rows,
link text equal to the target's title in that locale, five-locale correspondence (block
roles, source URLs, table shape, heading levels, the translation-length floor), the research
record cross-checks, the artwork-number rule, and the `cjk_units` limits 13/21/9/15. Those
last four are one unit looser than the brief's 12/20/8/14 — that slack was already in batch
3's code and is calibrated to the drawing width, so it stays.

**`RELATED` is empty.** It is the batch's roster and the articles are not chosen yet; the
usage message says so. `display_order` is the vertical's base plus the position in that
roster. Only the AI vertical has a base (149, continuing from 148 per `ai.md`). Nobody has
assigned a band to crypto or tech, and inventing one is how two series end up interleaved,
so for those the check only insists the field was set deliberately (`!= 100`).

## `build_assets.py`

- **Browser discovery deleted.** Batch 3 carries its own, inherited from a Windows
  workstation: it globs `%LOCALAPPDATA%\ms-playwright` and otherwise falls back to
  `C:\Program Files (x86)\Microsoft\Edge\...`, so on this container it finds nothing.
  Rendering now goes through `pack_ingest.chromium_binary()` and `render_svg()`. The binary is
  resolved on **first use** and kept for the rest of the run, not at import: `chromium_binary()`
  raises when it finds nothing, and at import that refusal reaches a machine with no browser
  before `main()` has read the `--svg-only` flag that says it needs none. Verified:
  `/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell`.
- The published JPEG goes through `pack_ingest.fit_bytes(..., HERO_MAX_BYTES, "JPEG",
  hard_cap=IMAGE_HARD_CAP)` instead of a bare `save(quality=88)`, so a hero cannot ship over
  the hard cap. Batch 3 never checked the byte size it wrote. A hero that only reaches the
  200 KB guideline at the quality floor is kept at 1600×900 and reported as a `WARN` line —
  the same grading `pack_ingest` gives it and the same one `check_article.py --assets` gives
  it. It was a refusal until the checker's semantics were settled; the writer refusing what
  the checker accepts is how the two come to disagree.
- Every SVG is passed through `pack_ingest.check_svg` before it is written — the same rules
  the import would fail on, found at drawing time.
- Vertical-aware: the eyebrow (`MOKAAIR / CRYPTO NEWS` etc.) and its accent come from the
  `Vertical`. The accents are the album's own `TEAL`/`BLUE`/`ORANGE` and an assertion holds
  them to the real palette constants. The 2×2 layout, the cream ground, the credit line and
  the drawing primitives are untouched; only the two card colours follow the vertical, and the
  AI vertical's accent is `TEAL`, so its diagram is byte-for-byte what batch 3 shipped. Batch
  3 drew every card `TEAL`/`BLUE`, which would have drawn every crypto and tech diagram in the
  AI vertical's colour — and half of this batch's published images are that drawing.
- Per-vertical output: research, `renders/`, `manifest.json` and the contact sheets all live
  in that vertical's own workspace. `build()` writes that workspace's `.gitignore` when it is
  missing, with `renders/` and `__pycache__/`, the two lines
  `docs/ai-news-2026-09-mid/.gitignore` carries. `build_assets.py [crypto|tech|ai]... [--svg-only]`.
- **Kept:** every drawing primitive and the palette. Added four in the same vocabulary for
  the two new verticals — `chain` (a ledger or protocol sequence), `scales` (a regulator),
  `certificate` (a licence or filing), `tower` (spectrum or a network). No trademarks,
  wordmarks, icons or interfaces, per `BRIEF.md`.
- `drawing()` still refuses an unknown slug rather than reusing another article's picture;
  the per-article branches are added as the articles are written.

## `merge_locale.py`

Same job and the same zh-TW hash assertion. Three refusals added, all from `BRIEF.md`'s
translation rules, because this is the gate a bad translation hits first: the `summary`
sentence count and `faq` question count must match zh-TW; the hero and diagram must point at
this locale's own files (`hero-ja.jpg`, `diagram-1-zh-cn.svg`); and a finance/crypto article's
disclaimer must carry this locale's own marker. Source `checked_on` must match zh-TW too.
Block comparison is role-based for the reason at the top of this file.

Every way in is a `REFUSED:` line rather than a traceback: a translation file that is not
valid JSON, a slug whose pack is not written yet, a pack with no zh-TW to compare against, and
a translation with no `sources` key at all — `GuideDocument.sources` has a `default_factory`,
so that last one validates cleanly and then used to die on `document["sources"]`, for the one
array that is identical to zh-TW and therefore easiest to leave out.

## `apply_corrections.py`

- The research record is looked up in the slug's workspace, not beside the script.
- `slug`, `kind`, `language`, `partner`, `event_date` and `news_date` join the list of keys a
  replacement never enters. `slug` and `kind` are the new hazard: after relink the closing
  links are `article` inlines carrying both, and a correction to a title that happens to read
  like a slug would otherwise repoint the link.
- A corrected pack document is validated against `GuideDocument` before it is written, and a
  correction that removes a crypto article's disclaimer marker is skipped. A reviewer
  rewording that callout is exactly how the marker gets paraphrased away, and a skipped
  correction is a better place to find out than a red CI run.
- The corrections file's own shape is checked the way its entries are, because it is written
  by hand: a file that is not JSON or is not a list, and an entry missing `slug`/`locale`/
  `old`/`new` or naming zh-TW, are each a `SKIPPED` line and a non-zero exit. All four used to
  be tracebacks, which also dropped every entry after them — the one thing `locate()`'s
  docstring says this script does not do. The zh-TW case was a bare `assert`, so under
  `python -O` it did not run at all and the original was silently editable.

## `update_index.py`

- Three indexes, keyed by vertical. The AI index keeps its slug forever
  (`docs/article-architecture.md`), so it is retitled in place, never renamed.
- **Anchors and paragraphs are relinked.** The index's month lists are `article` inlines now,
  not `link` blocks, and its opening paragraphs are `rich_paragraph`s. Batch 3 looked up
  anchors by URL (`next(...)` → `StopIteration`) and asserted `block["type"] == "paragraph"`.
  `find_link` matches by target slug whatever the form, `edit_block` edits a rich paragraph's
  text nodes in place — never its `article` inlines, whose text is a link label owned by the
  target's title — and new links are inserted already relinked.
- Table edits address a row by its **label**, not its index, so an index that grows a month
  still works. Where an index *is* addressed by number — a block index in `EDITS`, a column
  index in `TABLE` — it is bounds-checked and named (`there is no block 99; the index has 73`),
  because a hand-written block index is exactly what shifts when the index grows a link.
- `retitle()` implements `ai.md`'s third trap: after the index title changes it walks every
  pack's JSON structure and rewrites only the inlines whose `slug` is the index. Never a
  regular expression over the file — the batches do not agree on field order.
- `COUNT` refuses to finish while a number of articles survives anywhere a reader sees it
  (`ai.md`: the fix is to remove the count, not to raise it to 42). What makes a number a
  count is the unit or the noun beside it: `則 则 篇 편 本` count written pieces and stand on
  their own — simplified `则` as well as traditional `則`, since zh-CN is one of the five
  locales — while `條 条 件 건` also count legal clauses and enforcement actions, which is
  `crypto.md`'s own vocabulary (「第 5 條」,「3件の行政処分」), so those count only beside a
  word that says so. `reader_text` walks every block a reader sees, and asserts it reads
  everything `pack_ingest._document_text` reads, so a block type added to the schema cannot
  fall out of the guard.
- The finished index is validated — each locale as a `GuideDocument`, the whole file as an
  `ArticlePack` — **before** it is written, so an index the importer would refuse is a refusal
  here rather than a red CI run tomorrow.
- **Dropped:** batch 3's one-off repair of the Japanese month headings. That was batch #497's
  damage; the headings now read `2026年N月のニュース解説`.
- Pre-filled for the AI vertical: the five new titles and the five description edits, both of
  which are deletions of the day range and the count from the strings that are in the index
  today. Every other sentence that carries a reader-visible count is wired as a `TODO` entry
  quoted exactly as the index reads today — seven or eight per locale, including blocks 3 of
  zh-TW and zh-CN (「一月的三則消息」/「一月的三则消息」), which count January's own items.
  They need the new checked date written into the same sentence, which is an editorial
  decision rather than a deletion, so the pre-flight **names each one** and stops the run
  before anything is touched, instead of the run dying inside `update()` on the count rule.
  The parallel en/ja/ko sentences say "updates"/「3つのニュース」/「3가지 소식」 and carry no
  article unit, so `COUNT` does not demand them; a comment in `EDITS` says to keep the five
  locales in step by hand.

## What I could not verify

- **The batch's own content.** No article, research record or index exists for any of the
  three verticals yet, so `RELATED`, `NEW`, `CITED`, `TABLE` and `CAPTION` are empty and the
  hero compositions are unwritten. Everything below was exercised against batch-3 articles,
  sandbox copies and synthetic records.
- **`update_index.py` end to end.** It cannot run until the packs carry five locales. The
  edit machinery, the refusals and `retitle()` were exercised against a sandbox copy of the
  real AI index; the write path itself was not reached.
- **The Japanese and Korean copy in `RETITLE`/`EDITS`.** `2026年1月から9月まで…` and
  `2026년 1월부터 9월까지…` are deletions of the day tokens, and the Korean also drops a
  particle (`38건을` → `를`). They read correctly to me but should have a native check before
  the run, the same review every other translated sentence in this batch gets.
- **`COUNT` against the two new indexes**, which do not exist. It was written against the
  phrasings in the AI index and then checked the other way round, against `crypto.md`'s clause
  vocabulary and against version numbers, dates and determiners, which it must not match. A
  false positive that survives that is still visible — the refusal prints what it matched —
  rather than silent.
- **How the crypto and tech accents look in print.** An agent cannot see what it draws;
  the contact sheets exist for that and `BRIEF.md` requires a person to read them.
- **`display_order` for crypto and tech** — the owner has not assigned a band.
- `ruff` reports five `B905` (`zip()` without `strict=`) across these files, and `E501` on the
  long table rows. `docs/` is outside the configured lint scope (`uv run ruff check .` from
  `apps/api` does not reach it) and the batch-3 originals trip the same two rules — B905 three
  times and E501 more often than this batch does. The `zip()` pairs are deliberately ragged,
  which is what the surrounding length checks are for.

## Evidence

Commands and their real output are in the task report. The second round of fixes — the ones
this file now describes — was proved the same way: every finding's own evidence command re-run
against a sandbox root, plus a negative case for each, plus `build_assets` rendering five
locales through headless Chromium and `check_article --full --assets` passing over what it
wrote.

From the first round: In short: `py_compile` on all six
files; the ported checker run against `ai-news-siri-ai-ios-27-20260914 --full --assets`,
where the only failures left are the batch-4-only requirements (summary, faq, the new
`display_order` band); eleven one-at-a-time mutations of that article, all caught, including
both directions of the crypto disclaimer rule; `merge_locale` accepting a clean re-merge and
refusing four bad ones; `apply_corrections` applying one correction and skipping three with
accurate reasons; `build_assets` rendering five locales of a synthetic crypto article through
headless Chromium to heroes of 60–66 KB plus per-vertical manifest and contact sheets; and
`update_index`'s refusals, in-place rich-paragraph edit and `retitle()` over 30 packs.
