---
id: 2026-10-06-timeline-gaps-before-0915
title: Fill the gaps the 2026 release timeline has before 15 September
status: open
priority: P3
area: docs
owner:
claimed_at:
created_at: 2026-10-06T02:17:51Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/guides/content/ai-model-release-timeline-2026.json
  - apps/web/public/guides/ai-model-release-timeline-2026/diagram-1.svg
---

# Fill the gaps the 2026 release timeline has before 15 September

## Why

`ai-model-release-timeline-2026` says it lists every model the nine vendors announced on their
own pages in 2026. Ticket `2026-10-05-multi-vendor-ai-price-pages-late` extended it from
15 September to 30 September and only read the vendors' feeds for 16–30 September. While doing
that it ran into announcements from earlier months that the timeline does not carry:

- Meta, 2026-07-09: Muse Spark 1.1 and the public preview of the Meta Model API
  (`https://ai.meta.com/blog/introducing-muse-spark-meta-model-api/`, page dated July 9, 2026).
  The July paragraph has Muse Image and Muse Video (7/7) but not this.
- Meta: the open-weight Muse Glimmer 30B (`https://huggingface.co/meta-models/Muse-Glimmer-30B`,
  repository created 2026-08-09). `ai-model-comparison-table-2026` lists it in its open-weight
  table; the timeline's August paragraph does not mention it. An official announcement date
  still has to be found (the HF creation date is not one).
- MiniMax-M3.1-Flash-Preview appears on `https://platform.minimax.io/docs/guides/text-generation`
  (subscription plans and MiniMax Code only). MiniMax's release-notes page
  (`https://platform.minimax.io/docs/release-notes/models.md`) did not list it on 2026-10-06, so it
  has no date yet.

The timeline's own rule leaves out speech, TTS, live-voice and image models (Gemini 3.8 Live on
9/15, Gemini 3.8 TTS on 9/23, Grok Voice Transcribe 2.0 on 9/17, Qwen-Image-2.1 on 9/20 were left
out on that basis); the gaps above are language or multimodal models it does include elsewhere.

## Definition of done

- [ ] Each gap above is either added (prose, table row and diagram month line, with the date the
      vendor's own page gives) or written down in this ticket as deliberately left out.
- [ ] The pack stays inside the life body guideline (6,000 characters as `_body_length` counts
      them; it was 5,982 after the 9/30 extension) and `sources` stays at 20 or fewer.
- [ ] `image.description` stays a verbatim copy of the SVG `<desc>` and every diagram number is in the text.

## Steps

- [ ] Re-open the Meta AI blog, the Meta HF organisation and MiniMax's release notes on the day of the edit.
- [ ] Decide what to trim to stay under 6,000 characters before adding prose (the two September
      paragraphs were already folded into one for that reason).
- [ ] Update the July/August paragraphs, the 7–9 月 table and the diagram's 7/8 月 lines.

## How to verify

From `apps/api`: `PYTHONUTF8=1 uv run python -m app.guides.pack_cli lint --kind life --slug ai-model-release-timeline-2026 --render-dir <scratch>`
(no new warnings; look at the PNG) and
`PYTHONUTF8=1 uv run python ../../.agents/skills/content-pipeline/scripts/intake_check.py --slug ai-model-release-timeline-2026 --from-content`
(no FAIL beyond the ones listed in the parent ticket's notes).

## Notes

- Split from 2026-10-05-multi-vendor-ai-price-pages-late, which noticed these while reading
  the 16–30 September feeds and kept its own change to that window.
- The sources list is at the 20-item cap. That ticket dropped the Opus 4.6, 4.7, 4.8 and
  Gemini 3.7 Flash announcement pages to make room; any new source here means dropping another.
