---
id: 2026-10-01-google-vids-article-still-calls-the
title: Google Vids article still calls the Gemini 3.8 Flash-Lite voiceover Coming soon
status: in-progress
priority: P3
area: docs
owner: claude-opus-5-5-vids-voiceover
claimed_at: 2026-10-01T12:36:43Z
created_at: 2026-10-01T04:14:03Z
completed_at:
branch: claude/google-vids-voiceover-available
depends_on: []
scope:
  - apps/api/app/guides/content/ai-news-google-vids-omni-free-20260924.json
---

# Google Vids article still calls the Gemini 3.8 Flash-Lite voiceover Coming soon

## Why

The article `ai-news-google-vids-omni-free-20260924` says, in all five locales (summary
item 4, the voiceover paragraph and the voiceover FAQ; check the feature table too), that the
Gemini 3.8 Flash-Lite text-to-speech voiceover in Google Vids is "Coming soon" with no
launch date. That was right for the 2026-09-23 blog announcement, but the Google
Workspace Updates post of 2026-09-29 ("Create more natural, expressive AI voiceovers in
Google Vids with upgraded Gemini 3.8 Flash Lite TTS") says the upgraded engine is
available now for Rapid and Scheduled Release domains, on the plans it lists (Business,
Enterprise, Education Plus, Google AI Pro and Ultra, Essentials, Individual, Nonprofits,
education add-ons; no free personal accounts). The video fact-check
(`docs/videos/google-vids-free-ai-video-omni-1-1/verify-1.md` group 4 and `verify-2.md`
row 4) found this; it also notes the 2026-09-23 TTS blog says "For everyone: In Google
Vids", which conflicts with the plan list.

## Definition of done

- [x] Every locale says what the 2026-09-29 Workspace Updates post says about the voiceover's availability and plans, attributed to Google, with that post in the sources and the conflict with the 2026-09-23 TTS blog stated rather than resolved.

## Steps

- [x] Re-open the 2026-09-29 Workspace Updates post and the 2026-09-23 TTS blog the same day.
- [x] Edit the five locales through the `content-pipeline` skill; publishing is a separate owner-approved step.

## How to verify

`pack_cli lint --slug ai-news-google-vids-omni-free-20260924` is clean apart from the existing length warnings, and no locale still says the voiceover has no launch date.

## Notes

- Filed on 2026-10-01 by claude-opus-5-5-vids-article while fixing the age and language sentences (ticket 2026-09-30-google-vids-zh-cn-article-still), which was told to change nothing else.
- 2026-10-01, claude-opus-5-5-vids-voiceover: re-read three Google pages with WebFetch on
  2026-10-01, all fetched. (1) The 2026-09-29 Workspace Updates post: rollout pace "Available
  now" for Rapid and Scheduled Release domains; availability lists Business and Enterprise
  Starter/Standard/Plus, Education Plus, Google AI Pro and Ultra, Essentials Starter,
  Enterprise Essentials (Plus), Individual, Nonprofits, and the Google AI Pro for Education,
  Teaching and Learning and AI Expanded Access add-ons; no free personal accounts; no language
  count. (2) The 2026-09-23 blog.google post "Gemini 3.8 text-to-speech says hello"
  (gemini-3-8-text-to-speech): Flash-Lite TTS available starting that day, with Google Vids
  under "For everyone". (3) The Vids announcement (G1) still says "Coming soon" with 100+
  languages and no date.
- What changed, in all five locales: summary item 4 lost its voiceover clause and a new fifth
  summary item states the conflict (the schema caps an item at 300 characters, so it would not
  fit in item 4 for en and ko); the voiceover paragraph became two paragraphs (the 09-23
  announcement and blog, then the 09-29 post with its plan list), ending by saying the two are
  both Google's own posts and the article does not pick one; the table row's status now cites
  the 09-29 post; the caption adds "voiceover row checked Oct 1" (the en caption was reworded
  to stay under its 200-character cap); the FAQ answer says the same; the 09-29 post and the
  09-23 TTS blog are new sources with `checked_on` 2026-10-01. The "Coming soon" wording is kept
  only as what the 09-23 Vids announcement said.
- Not decided here: which engine free personal accounts use. AI voiceover itself already
  existed for personal accounts (help page 15609411, 1 credit per voiceover, per the video's
  verify-1), but no Google page says whether they get the upgraded engine; the article tells
  readers to check after signing in.
- Checks: `pack_cli lint --slug` has no errors; length warnings for en and ja as before, plus
  a new ko one (6724 characters against the 6000 guideline) from the added text.
  `intake_check.py --from-content` fails only on "first block is not summary", which is how
  the article was already built (two intro paragraphs before the summary). Repo change only:
  nothing is published or imported to the production site; that is a separate owner-approved
  step.
