---
id: 2026-10-12-shorten-five-english-titles-too-long
title: Shorten five English titles too long for the captions tag
status: in-progress
priority: P2
area: api
owner: claude-opus-5-5-cc-captions
claimed_at: 2026-10-12T06:45:47Z
created_at: 2026-10-12T06:42:00Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/video_youtube/retitle.py
  - apps/api/app/cli.py
  - apps/api/tests/test_video_youtube_retitle.py
---

# Shorten five English titles too long for the captions tag

## Why

After the 2026-10-12 backfill five videos kept an English title without the captions tag: each
was 97-100 characters, too long even for 「｜CC」. The owner asked for them to be shortened.

## Definition of done

- [x] `video-youtube-caption-titles --set-title VIDEO_ID LANGUAGE TITLE` gives a title new words
      before the tag goes on; the audit log keeps the old title.
- [ ] Run on the host with the five shortened titles below; the report after shows too_long 0.

## The five titles (each at most 86 characters, so 「｜CC Subtitles」 fits)

- htv6rUYkVkE en: Knowledge Cutoff: Check This Date Before Asking AI About News | AI Terms in 10 Minutes
- jSTz6qnilmk en: Temperature: Lower Isn't More Accurate; 0 Isn't Deterministic | AI Terms in 10 Minutes
- UWYoO3JfOK0 en: Firewall On, Skip Plugin Updates? Cloudflare's AI vs Its WAF: 1,107 Tries, 49 Findings
- KurEPz5z7hA en: GPT-6 Is Out but Not in ChatGPT? Where Sol and Luna Run, What the API Cut Compares To
- itKTQl3ehQE en: Blocked AI Agents Finding Another Way In? 3 Incidents, 3 Permissions to Set First

## Notes

- The approved upload packages still hold the long English titles; a later re-send from the card
  would send them again. Public videos are not re-sent by the site, so this is left as it is.
