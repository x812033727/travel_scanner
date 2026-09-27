---
id: 2026-09-27-the-chat-slide-allows-five-messages
title: The chat slide allows five messages but four named bubbles overflow at 1080p
status: done
priority: P2
area: tools
owner: codex-video-chat
claimed_at: 2026-09-27T15:23:41Z
created_at: 2026-09-27T07:32:10Z
completed_at: 2026-09-27T15:38:05Z
branch: codex/video-chat-layout
depends_on: []
scope:
  - tools/video/templates/templates.mjs
  - tools/video/templates/templates.test.mjs
  - tools/video/templates/theme.css
  - tools/video/templates/fixtures/showcase/video.json
  - .agents/skills/youtube-video/references/prompts/writer-video.md
---

# The chat slide allows five messages but four named bubbles overflow at 1080p

## Why

At about 06:12Z on 2026-09-27 the host worker blocked `openai-academy-learning-paths` at `render`:
`render failed: 4 layout problems; frames are cached, fix the scenes and rerun`. All four
problems were in one scene, `paths-chat` (template `chat`), and every state was too tall:
`the slide's content is 60px taller than its area` in states 0 to 2, and 88px in state 3. The
scene had four short messages, each with a `name` label (你 and 我的對照), so the texts were
not the problem. Hidden messages still hold their place, and four named bubbles do not fit
under a title on a 1080p slide.

`lint` passed the scene: `TEMPLATE_SPECS.chat.check` accepts 1 to 5 messages with an optional
`name`, and the writer prompt only describes chat as "a question and its answer". The showcase
fixture uses two messages, so nothing in the tests exercises the upper limit. A writer that
follows the schema can block a video that has already spent its narration and fact-check.

Later that day the scene was hot-fixed on the host by removing the four `name` labels. After
that, render redrew 4 states and reused 56 with no problem, and the video was unblocked.
The original is at
`/var/lib/mokaair/video-work/openai-academy-learning-paths/video.json.before-chat-fix-20260927`
in the `video_work` volume.

## Definition of done

- [x] `lint` rejects a chat scene that `render` cannot fit, or the chat layout fits everything
      `lint` accepts. Either way, lint and render agree on the upper limit, with and without
      `name`.
- [x] A test renders the largest chat scene `lint` accepts, with names and the longest texts
      the writers use, and gets no layout problem.

## Steps

- [x] Measure how many named and unnamed bubbles fit under a title at 1080p, with one-line
      and two-line texts.
- [x] Then choose: lower the limit in `TEMPLATE_SPECS.chat` (a named message could count
      more than an unnamed one), or tighten the thread's spacing in `theme.css`. Per
      `references/automated.md`, content fixes do not change the theme CSS; this is a template
      fix, so it may.
- [x] Add the test in `templates.test.mjs`.

## How to verify

```bash
node --test tools/video/templates/templates.test.mjs
node tools/video/cli.mjs render --slug <a video with a 4- or 5-message chat scene> --channel msedge   # no layout problems
```

## Notes

- If the limit goes down, say so in the writer prompt
  (`.agents/skills/youtube-video/references/prompts/writer-video.md` and its byte-identical
  `.claude/skills/` copy). Add those two paths to the scope first.
- Found while clearing the stuck reviews on 2026-09-27, together with
  `2026-09-27-video-drafts-read-their-source-article`.
- 2026-09-27: Limited chat to two named or three unnamed messages, a one-line title of at most
  20 visible characters, and message text of at most 44 visible characters without manual
  breaks. Added lint tests and both maximum layouts to the showcase fixture. The 1080p browser
  render drew all 27 showcase states with no layout problems; the contact sheet was inspected.
  The skill's writer prompt lives only under `.agents/skills/` in this checkout; there is no
  separate `.claude/skills/youtube-video/references/` copy to edit.
