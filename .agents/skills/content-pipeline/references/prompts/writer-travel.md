# Writer prompt: travel or food batch, one article per agent

Fill the placeholders before dispatch: `<ROOT>` (absolute path of the repo or worktree), `<WORKDIR>` (the batch working directory, outside the repo), `<BATCH_DOCS>` (the batch's docs directory, e.g. `<ROOT>/docs/travel-guides-batch-8`), `<SLUG>`, `<PY>` (that worktree's venv python) and `<CHROMIUM>` (the browser binary `render_svg` uses). The launch message adds an IDENTITY block: slug, kind, destination_id, word band, the two example packs, the sibling slugs that share numbers, and the spec path. Commands are written for a POSIX shell; translate them for your shell if needed. Everything below the rule is the prompt.

---

You are writing ONE zh-TW (Traditional Chinese, Taiwan) travel article for Mokaair (mokaair.com) as a content pack. This is a DRAFT: an independent verifier re-checks every claim afterwards, so record your evidence.

REPO (read-only; never run git, never write inside it): `<ROOT>`
WORKDIR (write here and ONLY here): `<WORKDIR>/<SLUG>/`. Helper scripts go in `<WORKDIR>/_tools/<SLUG>/`.

## Read, in this order

1. The spec, all of it: `<BATCH_DOCS>/<SLUG>.md`. Its 「撰稿時要小心」 or 「容易寫錯的事實」 section overrides the rest of the spec; the spec overrides the READMEs. Its 「官方來源」 section already quotes the URLs and the text read on the planning day: start from those URLs.
2. `<BATCH_DOCS>/README.md`: the batch rules (the section on what differs from the previous batch, the table of time-sensitive facts to re-check on writing day, the list of official sites that cannot be read and how to read them).
3. The rulebook the batch README defers to: `<ROOT>/docs/travel-guides-batch-7/README.md` §給撰稿者 (workdir files, pack.json shape, allowed blocks, fact-checking, offers, links, photos, diagrams) and `<ROOT>/docs/travel-guides-batch-7/ERRATA.md`; `<ROOT>/docs/travel-guides-batch-6/README.md` §pack.json for field details.
4. Reader-first rules, mandatory: `<ROOT>/docs/korea-food-specials/README.md` §讀者優先. In short: title and description name the destination, never the method; 「本文」「這篇」 at most ONCE in the whole article and only in the opening scope sentence; at most ONE attribution phrase (「官方頁寫」「官網寫」「依…公告」) per paragraph, other sentences state facts directly, provenance lives in table evidence columns and in `sources`; no verification narration in the body (no 「查證時」「我們查不到」「官方頁沒寫所以」); every foreign name carries Chinese on first use; no untranslated foreign block quotes; official-page field names never appear in prose; no counts in title, description or summary (「這幾條」 not 「六條」); do not present a side effect of your own selection as a finding.
5. The two example packs named in the launch message, for shape and tone only (do not copy text).

## Hard rules

- Every price, time, opening hour and rule is re-opened on the official page TODAY; `checked_on` is the day you actually opened it. Not found on an official page → write 「以官網為準」, never a third-party number. Web search at most 5 calls.
- Fetching: `curl -sSL -A 'Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)' <url>`. Always `-L`; at least 1 s between requests to one host; NO personal name, email or any personal data of anyone anywhere (UA, headers, query strings, notes). Check HTTP status codes; a 200 shell page is not a source.
- Strip HTML comments before quoting: python `re.sub(r'<!--.*?-->', '', html, flags=re.S)`. Dead content inside `<!-- -->` is NOT on the page; past batches nearly shipped closed hours, cancelled routes and old quotas that only lived in comments.
- Domains the batch README lists as no longer official (squatted, parked, redirected to social media) are forbidden as sources. `sources` carry the final URL after redirects.
- Two official sources disagree: pick one (default the operator; a stale, self-contradicting or outsourced site → the government tourism body), disclose the other in one clause, never two options; use the narrower time window for planning.
- Site links: article links are `article` inlines with the target's kind; targets must exist in `<ROOT>/apps/api/app/guides/content/` with a zh-TW locale, or be one of this batch's slugs (the README's 清單). City page and food catalogue are `link` blocks `https://mokaair.com/zh-TW/destinations/<id>` and `https://mokaair.com/zh-TW/foods?destination_id=<id>`; never `?city=`. Offers at most 3, module and position exactly as the spec, never before the first H2, never adjacent to another offer, generic heading, no brand or amount.
- destination_id null → NO offer block at all; city links only as the spec says; no foods link.
- Names follow the batch README's rulings; catalogue spellings win (`<ROOT>/apps/api/app/destinations/catalog.py`, `<ROOT>/apps/api/app/hotspots/areas.py`, `<ROOT>/apps/api/app/foods/area_catalog.py`), alternatives go to `aliases`. Local currency, full dates in digits (2026 年 9 月 22 日), no NT$ conversions.
- Photos: Wikimedia Commons only, licence CC0, PD, CC BY or CC BY-SA (open each File: page and check), hero landscape at least 1600 px wide, no banknotes, logos, screenshots or recognisable faces; do not reuse files the spec lists as already used; list all candidates in notes.md so the coordinator can dedupe heroes across articles. Search Commons only AFTER the body is written. `images.json` = {"hero": {"title": "File:…"}, "photos": {"photo-1": {"title": "File:…"}}}; the ingest tool downloads and checks licences. In pack.json the hero `src` is `/guides/<SLUG>/hero.jpg`, width and height 1, no credit.
- Diagram: diagram-1.svg, viewBox="0 0 1600 900", role="img", `<title>`, `<desc>`, every font-size at least 15, system fonts, no external references, 「© Mokaair 製圖 2026」 bottom-right, Traditional Chinese labels (plus local script where useful). Every number drawn on the diagram must appear verbatim in the body.
- Blocks: plain text only (no HTML, Markdown, emoji or entities); summary block first (2 to 5 sentences, numbers verbatim from the body, no meta sentence), then the opening paragraph; at least 3 H2; at least 1 table (at most 4 columns); at least 1 callout; exactly 1 diagram; 1 to 2 photos; FAQ only if the spec lists it.
- Word band per the launch message; each H2's figure in the spec is a CAP. `pack_ingest._body_length` counts summary items, every table cell, callouts, FAQ and link sentences; headings excluded. Do not pad a deliberately short article.
- If an official source contradicts any rule above or in the spec, the source wins: follow it and report the conflict.

## Workdir files

    pack.json      write it FIRST with the skeleton and save after every section (a cut-off session keeps files, not chat)
    diagram-1.svg
    images.json
    notes.md       one line per claim: 主張｜來源網址｜查證日; then three sections at the end: ## 與規格不同的地方 / ## 我懷疑但沒動的事 / ## 進度 (which H2s are done; keep it updated)
    report.md      your final report (also paste it as your reply)

## Self-checks before reporting

Run from `<ROOT>/apps/api` with `PYTHONIOENCODING=utf-8`; `<PY>` is that worktree's venv python.

    <PY> -m app.guides.pack_cli ingest --from <WORKDIR> --slug <SLUG> --dry-run
    CHROMIUM_BIN="<CHROMIUM>" <PY> -c "from pathlib import Path; from app.guides.pack_ingest import render_svg; render_svg(Path('<WORKDIR>/<SLUG>/diagram-1.svg'), Path('<WORKDIR>/<SLUG>/diagram-1.png'))"
    → open the PNG with your image-viewing tool and fix overlaps and clipping; repeat until clean.
    <PY> -c "import json; from app.guides.content_pack import ArticlePack; from app.guides.pack_ingest import _body_length; p=ArticlePack.model_validate(json.load(open('<WORKDIR>/<SLUG>/pack.json', encoding='utf-8'))); print(_body_length(p.locales['zh-TW']))"
    <PY> <ROOT>/.agents/skills/content-pipeline/scripts/intake_check.py --slug <SLUG> --workdir <WORKDIR> --manifest <BATCH_DOCS>/batch.json
    (the coordinator's mechanical checks; fix every FAIL, read every WARN; drop --manifest if the batch has none)

Manual: every summary number appears verbatim in the body; every article inline's slug and kind exist; table columns at most 4; offers placed per the spec; every source has checked_on = today. Write helper scripts as files into `<WORKDIR>/_tools/<SLUG>/` and run them; do not paste non-ASCII text into shell heredocs, Windows mangles it.

## Report (at most 40 lines, saved as report.md and pasted back)

status; body_length; counts (H2, table, callout, offer, image, FAQ); the state of each time-sensitive row as of today with the notice date you saw; numbers that differ from the spec; claims written as 「以官網為準」 and why; Commons file names used with licence; dry-run and intake_check output summary (warnings verbatim); things you suspected but did not change; open questions for the coordinator. Do not touch any other article's workdir. Do not modify the repo.
