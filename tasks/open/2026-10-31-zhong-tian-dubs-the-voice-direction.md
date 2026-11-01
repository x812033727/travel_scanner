---
id: 2026-10-31-zhong-tian-dubs-the-voice-direction
title: Zhong-tian dubs: the voice direction is cut at 400 characters before the emotion reaches it
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-31T17:10:53Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/local/dub-lines.mjs
---

# Zhong-tian dubs: the voice direction is cut at 400 characters before the emotion reaches it

## Why

`dub-lines.mjs` builds each line's Gemini style as lead + character persona + 「direction: emotion」 and cut the
whole string at 400 characters (the site's limit). For the longest personas the emotion fell off the end: Qin Shuang
in id (402 characters before the emotion) and th (399) never got any emotion, and Xu Yan in id/th kept only the first
16-19 characters of it. Changing `emotion` in dub.<l>.json did nothing for those lines (found fitting e037, id a19).

## Definition of done

- [x] Over 400 characters, the persona is shortened instead of the emotion; a style within 400 is byte-identical to
      before, so no already-recorded take is invalidated.
- [ ] The next dub run of an episode re-records only the lines whose style changed (id/th lines of Qin Shuang and
      Xu Yan); check their emotion is now audible.

## How to verify

`node --check dub-lines.mjs`; a standalone check of the new styleOf: a 380-character persona keeps the full emotion
at 400 characters; a short persona gives the same string as before.

## Notes

- Also from e037 vi: Gemini refused (422 video_speech_rejected) 「Tiểu Đường, phụ nữ trẻ em giao nàng.」 every time;
  「phụ nữ và trẻ em」 was accepted. Same family as the zh 「婦孺交給你」 refusal in e037. Probe one line alone with a
  script that writes nothing into the episode before changing a whole locale.
