---
id: 2026-11-01-ai-series-thumbnails-ai101-look
title: AI series thumbnails take the AI 101 look: full-frame picture, series label, one-line two-colour headline
status: open
priority: P1
area: tools
owner:
claimed_at:
created_at: 2026-11-01T12:22:45Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/templates/templates.mjs
  - tools/video/templates/theme.css
  - tools/video/templates/templates.test.mjs
  - tools/video/qa/thumbnail.mjs
  - tools/video/qa/thumbnail.test.mjs
  - tools/video/render/plan.mjs
  - tools/video/automation/register.mjs
  - tools/video/automation/flow.mjs
  - tools/video/automation/lead-picture.mjs
  - tools/video/automation/lead-picture.test.mjs
  - tools/video/automation/automation.test.mjs
  - .agents/skills/youtube-video/SKILL.md
  - .agents/skills/youtube-video/references/visuals.md
  - .agents/skills/youtube-video/references/daily-brief.md
  - .claude/skills/youtube-video/SKILL.md
  - .claude/skills/youtube-video/references/visuals.md
  - .claude/skills/youtube-video/references/daily-brief.md
---

# AI series thumbnails take the AI 101 look: full-frame picture, series label, one-line two-colour headline

## Why

The owner decided on 2026-11-01 that every AI video takes one thumbnail look from now on: the daily
brief (`daily-ai-`), AI 科技資訊 (`category: ai-news`), AI 名詞十分鐘 (`ai-terms`) and the hands-on
tutorials (`tutorial`). The model is the Taiwanese channel AI 101 (「AI新聞快報」, 3.6k–11.9k views
an episode). Other series (奇聞檔案局, 品牌故事, 原來如此事務所, the dramas) keep their own looks.

What the current thumbnails get wrong, seen on the channel on 2026-11-01:

- The daily briefs of 10/29 and 10/30 went out with the right 60% an empty tone (the lead picture
  landed on 10/31, after they were uploaded). When a picture is found it can be a generic site card:
  10/29's og:image reads "OpenAI Deployment Safety Hub" and says nothing about GPT-6 Luna.
- The headline does not name the subject: 「最強 不給你」「變短也變錯」「今天就更新」. The six-glyph limit
  (`THUMB_HEADLINE_MAX`) pushes writers to abstract phrases; every high-view AI news channel puts the
  product or company name in the largest type.
- The series tag is written by the model and changes every day (「AI 科技快報 10/28」「AI 快報」「科技快報」).
- The sub line and the picture-in-a-card do not read at 168 px (sidebar and search).
- Another channel is literally named 「AI科技快報」 and shows up in the same search.

## Definition of done

- [ ] An AI video's thumbnail is one full-frame picture with: the series label and (for a brief) the
      date in one line at the top left, filled by the template from a fixed table per locale, never by
      the model; one headline line at the bottom, the subject in white and the hook (`**...**`) in
      the accent colour; one white sub line under it; a dark gradient over the lower half.
- [ ] The headline is shrunk to fit one line (Latin locales may take two: subject, then hook) and the
      sub line likewise; nothing is clipped, and qa fails one that still does not fit.
- [ ] There is never an empty box: no picture, or a picture with its own words (a generic og:image),
      falls back to a word-free picture, then to a plain ground with the headline.
- [ ] The writer prompts ask for subject + hook (about nine CJK glyphs) and a sub line that says what
      the title does not.
- [ ] The skill docs record the decision, so a session making an AI video by hand follows it too.

## Steps

- [ ] New layout in `templates.mjs`/`theme.css` (e.g. `e`), chosen by category/slug for the four AI
      lines; series label table for zh-TW, en, ja, ko, es, pt, id, vi, th (dates MM/DD for zh/en/ja/ko,
      DD/MM for the rest).
- [ ] Headline rule in `qa/thumbnail.mjs`: subject + hook on one line instead of six glyphs on two.
- [ ] Picture per line: ai-terms and ai-news use the episode's own illustration (shot keyframe, full
      16:9, not the right-hand crop); the daily brief uses the lead picture when it carries no words,
      else a word-free fallback; tutorials: see the open question below.
- [ ] `register.mjs` writer/translator prompts; `lead-picture.mjs` rejects or flags a card with text.
- [ ] Docs: SKILL.md, `references/visuals.md` §縮圖, `references/daily-brief.md` (both skill copies).

## How to verify

- `npm run test:tools`.
- Render `daily-ai-20261028` (and an ai-terms and a tutorial fixture) with `render --thumbnails-only`;
  the nine thumbnails match the hand-made references below, and nothing reports "does not fit".

## Notes

- Owner choices so far (2026-11-01): the AI 101 structure; version A of the 10/30 brief
  (「金鑰只選了 **數字 4**」: the hook says what the title does not); accent `#ff8a1f` on the brief.
- Still open, ask the owner: one accent for all four lines or one each (proposed yellow for terms,
  orange for news, green for tutorials); tutorials on an illustration or on the real screen capture;
  about US$0.15 a day for one generated picture for the brief.
- Keep the channel's own illustration style (teal and ochre print look), not AI 101's watercolour or
  its red: the names are already close and the look should not be mistaken for theirs.
- SKILL.md rule 6 still holds: no AI-drawn logos; an official picture is credited in the description.
- Hand-made references, uploaded by the owner in Studio, not in the repo: 10/28 「Google 最強 **先不給你**」
  on Google's Carbon image; 10/29 「ChatGPT **少拍馬屁**」 on a word-free bubble drawing (the og:image was
  generic); 10/30 「金鑰只選了 **數字 4**」 on the right half of Cloudflare's og:image. Each in nine
  languages; Latin headlines needed 90–108 px to fit one line at 1280.
