---
id: 2026-10-01-google-vids-article-still-calls-the
title: Google Vids article still calls the Gemini 3.8 Flash-Lite voiceover Coming soon
status: open
priority: P3
area: docs
owner:
claimed_at:
created_at: 2026-10-01T04:14:03Z
completed_at:
branch:
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

- [ ] Every locale says what the 2026-09-29 Workspace Updates post says about the voiceover's availability and plans, attributed to Google, with that post in the sources and the conflict with the 2026-09-23 TTS blog stated rather than resolved.

## Steps

- [ ] Re-open the 2026-09-29 Workspace Updates post and the 2026-09-23 TTS blog the same day.
- [ ] Edit the five locales through the `content-pipeline` skill; publishing is a separate owner-approved step.

## How to verify

`pack_cli lint --slug ai-news-google-vids-omni-free-20260924` is clean apart from the existing length warnings, and no locale still says the voiceover has no launch date.

## Notes

- Filed on 2026-10-01 by claude-opus-5-5-vids-article while fixing the age and language sentences (ticket 2026-09-30-google-vids-zh-cn-article-still), which was told to change nothing else.
