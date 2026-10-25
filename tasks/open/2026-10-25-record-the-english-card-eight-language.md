---
id: 2026-10-25-record-the-english-card-eight-language
title: Record the English-card, eight-language and paper-layout lessons from the October news videos in the shared youtube-video skill
status: in-progress
priority: P2
area: docs
owner: claude-fable-5-1-news-video
claimed_at: 2026-10-25T06:26:24Z
created_at: 2026-10-25T06:24:11Z
completed_at:
branch:
depends_on: []
scope:
  - .agents/skills/youtube-video
  - .claude/skills/youtube-video/SKILL.md
  - docs/videos/PAPER.md
  - docs/videos/DUBS.md
---

# Record the English-card, eight-language and paper-layout lessons from the October news videos in the shared youtube-video skill

## Why

The three AI/tech news videos of 2026-10-22..25 (ai-shopping-agents-blocked, claude-duet-proactive-agent, google-ai-search-ads-exception; PRs #1700, #1833) taught rules that so far live only in one account's local memory and in those videos' tickets. Agents on other accounts and Codex read only the shared skill under `.agents/skills/youtube-video/` (SKILL.md mirrored to `.claude/skills/`) and `docs/videos/*.md`, so the rules go there: card language: zh-TW main language with English proper nouns and quotes, full-English cards only per video for international topics (owner proposed English cards 2026-10-24, settled on zh-TW-first 2026-10-25 after weighing the zh-TW audience's retention against dubbed viewers), eight languages instead of three (owner 2026-10-24; pipeline since 2026-10-20), the paper layout limits render does not flag, the dub chain discipline (one lease per video, detached chains, reword not retake, per-language transcription traps), captions after assemble, composed title length per locale.

## Definition of done

- [ ] SKILL.md 不變的規矩 has the card-language (zh-TW first, English nouns, per-video English cards) and eight-language rule; automated.md step 13 says eight languages and §坑 holds the layout, captions-after-assemble, dub-chain and title-length lessons; PAPER.md has the measured English limits; DUBS.md and caption-translate.md carry the per-language mishearing list; writer-video.md tells the writer the card language and when the brief switches it to English; `.claude/skills/youtube-video/SKILL.md` is byte-identical; `npm run test:tools` passes.

## Steps

- [ ] Edit the files (append-only sections where possible: five older tickets also touch this skill, claimed with --force).
- [ ] Mirror SKILL.md, run test:tools, open a PR separate from the video PR.

## How to verify

`npm run test:tools`; `diff .agents/skills/youtube-video/SKILL.md .claude/skills/youtube-video/SKILL.md` prints nothing.

## Notes

- 2026-10-25: the owner asked whether a main language is needed and whether English cards are a bad idea; the answer recorded in rule 14 is zh-TW first (narration audience and recommendation retention), English kept for proper nouns, quotes, numbers and commands, full-English cards per video for international topics only; `google-ai-search-ads-exception` stays as the one experiment to measure.
- Claimed with `--force`: 2026-10-14-ai-and-tech-videos-tell-one, 2026-10-14-curio-episodes-keep-the-series-look, 2026-10-17-story-narrative-panel-asks-two-independent, 2026-10-18-story-thumbnail-brand and 2026-10-20-tutorial-flow-and-hooks-rules-learned list the same skill in scope and are stale; this ticket only appends sections and one rule number, so a later merge of theirs should not collide.
