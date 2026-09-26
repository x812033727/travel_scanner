---
id: 2026-09-26-videos-learn-from-a-reference-chapter
title: Videos learn from a reference: chapter map on screen, article-first description, four more templates
status: done
priority: P1
area: tools
owner: claude-opus-5-5
claimed_at: 2026-09-26T03:24:09Z
created_at: 2026-09-26T03:24:02Z
completed_at: 2026-09-26T03:24:38Z
branch: claude/video-reference-learnings
depends_on: []
scope:
  - tools/video/templates
  - tools/video/render/plan.mjs
  - tools/video/render/render.test.mjs
  - tools/video/core/metadata.mjs
  - tools/video/core/metadata.test.mjs
  - tools/video/core/schema.mjs
  - tools/video/package/metadata.mjs
  - tools/video/automation/prompts.mjs
  - .agents/skills/youtube-video/references
---

# Videos learn from a reference: chapter map on screen, article-first description, four more templates

## Why

On 2026-09-26 the owner sent a reference video: Gary Chen's 「爆紅新模型 Jev 解析」, youtube.com/watch?v=2mtn-Qp59y4, 13:39 long. They asked for its selectable chapters and for anything else worth learning. I read its description and chapter list on the page and looked through its storyboard frames (320×180, one every 5 s) in the in-app browser. Compared with our three batch 2 videos:

- **Chapters.** It has 7, each named for its content ("它能回答的三種題型"). Ours also come from the description's timestamps, but they open with 「開場」 and close with 「結論」.
- **Where you are.** Every frame shows "02 / 06 chapter" in the corner and a segmented progress line across the top. Ours shows only the chapter name.
- **Description.** It puts the link to the full write-up on the first line, visible before "more". Then a two-sentence summary, 📌 timestamps, sources with credits, and hashtags. Ours opens with the body and buries the article link near the end, with no hashtags.
- **Pace.** A new visual every 5–10 s: chat bubbles, customer data cards, official posts quoted with their source, stat callouts. Ours can leave one bullet slide up for 30–60 s.
- **Mid-video card** pointing to the full write-up. Ours only mentions it at the end.
- It burns subtitles into the picture. The owner chose again to keep CC only.

The owner chose all four improvements for the batch 2 videos and for the tools.

## Definition of done

- [x] Every slide except the title card shows "NN / MM chapter" and a bar with one segment per chapter: the seen ones teal, the current one orange. Chapter cards read "02 / 06".
- [x] The composed description opens with 🔗 and the article, then the body, 📌 chapters, 📚 sources, and three hashtags made from the first tags, per locale.
- [x] New templates `chat`, `quote`, `stats` and `cta`, with data checks and reveals. Each has a showcase scene.
- [x] The writer's instructions (automation prompts and the skill's writer prompt) name the new templates, the pace rule (no state much over 15 s), content chapter names and one mid-video `cta`. The skill's `automated.md` says the same.

## Steps

- [x] `render/plan.mjs` passes `chapterCount`; `templates.mjs` draws the chrome; `theme.css`.
- [x] `core/metadata.mjs`: `composeDescription` order and `hashtagsFrom`; `package/metadata.mjs` passes each locale's tags.
- [x] `core/schema.mjs` `TEMPLATES` gains the four names.
- [x] Prompts and docs.

## How to verify

- `npm run test:tools`.
- `node tools/video/cli.mjs render --file tools/video/templates/fixtures/showcase/video.json --workdir <dir> --channel msedge` draws 24 states with no layout problems. On its contact sheet, check the progress bar, "04 / 05", the chat bubbles, the quote, the stats and the cta card.

## Notes

- The drama route (#781, and its open ticket `video-drama-render` with scope `tools/video/render` and `tools/video/templates`) will build on these files. Only one small overlap is expected: `schema.mjs` `TEMPLATES`, 4 added lines, which #781 does not touch.
- Not done, on purpose: a lint warning for slides that stay up too long. It belongs in `core/lint.mjs`, which #781 is rewriting, so the rule lives in the prompts for now.
- Hashtags come from the first three tags, so the writer's tag order matters. No new schema field.
