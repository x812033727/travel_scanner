---
id: 2026-11-08-curio-thumbnails-get-a-split-layout
title: Curio thumbnails get a split layout so the text never covers the subject
status: done
priority: P1
area: tools
owner: claude-opus-5-5-curio-redo-20
claimed_at: 2026-11-08T02:57:10Z
created_at: 2026-11-08T02:56:46Z
completed_at: 2026-11-08T03:00:43Z
branch: claude/curio-redo-20-episodes-ldnrq0
depends_on: []
scope:
  - tools/video/templates/templates.mjs
  - tools/video/templates/templates.test.mjs
  - .agents/skills/curio-episode
  - .claude/skills/curio-episode
---

# Curio thumbnails get a split layout so the text never covers the subject

## Why

The owner asked on 2026-11-08 that a curio thumbnail's subject not be covered by the words. The
bold layout (d) lays the headline over the left half of a full-frame picture, so a centred subject
(B01's boy on the motorcycle) is covered, and a long translated headline covers more. The split
layout (c) keeps a 40% column, too narrow for es/pt/vi headlines, and crops the subject. The owner
chose a new split like 原來如此事務所's: a solid text panel on the left, the picture on the right.

## Definition of done

- [x] `thumbnail.data.layout: "e"`: solid panel on the left (the bold yellow headline, white
      sub), the picture on the right, never under the text; long headlines shrink (fitText).
- [x] `thumbnail.data.focus` (0-100) sets where the picture sits horizontally in its panel.
- [x] No other video's thumbnail or frame changes: the CSS is inline and only layout "e" uses it;
      no default moves (the other curio conversation's W03/B02/B03 keep layout d).

## How to verify

`node --test tools/video/templates/templates.test.mjs`; render B01 and H24 thumbnails in zh-TW
and a long Spanish headline and look at them.

## Notes
- Claimed with --force on 2026-11-08: every overlapping claim was more than 24 hours old.
- Rendered with the real renderer (openRenderer + fitText): B01 and H24 in zh-TW, a long Spanish
  and a long Vietnamese headline; no fit problems, the words never reach the picture. H24 needs
  `focus: 80` to bring the candle into the panel's middle.
- Done in the PR that adds layout "e"; the redo episodes write it into their own video.json.
