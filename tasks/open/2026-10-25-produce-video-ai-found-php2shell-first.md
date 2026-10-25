---
id: 2026-10-25-produce-video-ai-found-php2shell-first
title: Produce video: AI found PHP2Shell first, the leak that beat the patch, and the version check every site owner can run
status: in-progress
priority: P1
area: docs
owner: claude-fable-5-1-php2shell
claimed_at: 2026-10-25T06:20:47Z
created_at: 2026-10-25T06:13:24Z
completed_at:
branch: claude/focused-hopper-zq70n8
depends_on: []
scope:
  - docs/videos/php2shell-ai-found-it-first
  - docs/videos/lexicon.json
  - docs/videos/reference-study-20261025-ai-news
  - .agents/skills/youtube-video/references/news-flow.md
  - .agents/skills/youtube-video/SKILL.md
  - .claude/skills/youtube-video/SKILL.md
---

# Produce video: AI found PHP2Shell first, the leak that beat the patch, and the version check every site owner can run

## Why

The owner asked on 2026-10-25 for a new AI/tech current-events video, picked from the foreign videos with the highest views this week, and for whatever those videos teach to be folded into the skill. The week's most-covered AI story (BBC 2.25M, CBC 630K, Sky 620K, BBC 360K, plus Indian and Polish channels) is PHP2Shell: two PHP engine flaws (CVE-2026-109618, CVE-2026-109619, CVSS 9.2) found with AI in August (Calif under OpenAI's Patch the Planet on 8/11, OpenAI, Wiz), patched 2026-10-21 a day early after a Hacker News leak on 10/20, exploited before disclosure (AWS honeypot 10/17), with governments and services worldwide taking sites offline. The research record is `docs/videos/reference-study-20261025-ai-news/README.md`; the rules learned are `.agents/skills/youtube-video/references/news-flow.md`.

Route: teaching-card short (teaching-flow §十 one concept, §十二 picture rules, PAPER.md), `category: "ai-news"`, `theme: "paper"`, cards zh-TW with English nouns, quotes, numbers and commands (SKILL.md rule 14, PR #1843), 8-minute floor. One concept: the flaw is in the engine (PHP) not the car body (your site code), so the fix is a chain and the version string cannot tell you whether it landed. The one RUN is this machine's own check on 2026-10-25 (Ubuntu 24.04.5, PHP 8.3.6 (cli), dpkg 1.22.6): `php -v` says 8.3.6, `dpkg-query` says `8.3.6-0ubuntu0.24.04.13`, the changelog's first four lines name the CVE patch, and Ubuntu's CVE page lists that version as fixed.

## Definition of done

- [ ] `docs/videos/php2shell-ai-found-it-first/` holds brief.md (three outlines, A recommended), video.json (41 scenes), claims.md, verify-1.md (and verify-2.md when round 1 changes more than three facts); lint has zero errors (the one-sentence outro warning is intentional, as on PR #1833); the storytelling panel is recorded with `narrative --answers` and its misses noted.
- [ ] `docs/videos/lexicon.json` carries the new terms (PHP, PHP2Shell, CVE, Ubuntu, WordPress and the names; all appended, none changed).
- [ ] `docs/videos/reference-study-20261025-ai-news/README.md` (this week's table, how the news channels cut the story, what we do differently, what was not measured) and `.agents/skills/youtube-video/references/news-flow.md` with its SKILL.md row (both copies byte-identical; `node --test tools/skills.test.mjs` passes).
- [ ] Owner-side: outline gate (standing word: take A), `tts`, `check-audio`, audio gate, `render`, `assemble`, `captions`, `qa`, final gate, `package`, publish gate, upload per `UPLOAD.md`, then the eight languages ticked on the video page. These need the host token and the site, so they are not done from this cloud session.

## Steps

- [x] YouTube search pages (four queries, this week, by views) fetched with the Mokaair UA and parsed; watch pages return 429, so no transcripts (noted in the study).
- [x] Sources fetched 2026-10-25 and saved under the scratchpad (php.net archive and supported-versions, PHP Foundation post, Wiz, Cloudflare, AWS, watchTowr, Ubuntu CVE, Debian tracker, W3Techs, NCSC, CSA Singapore, 資安署 新聞稿 21134, iThome 179861/179870/179889/179891, BBC ×3, Japan Cyber Watch, TechTarget, Wikipedia, Brockman on X, HN Algolia timestamp). openai.com/index/php2shell, nsa.gov and cisa.gov answer 403 to curl and WebFetch.
- [x] The three terminal commands run on this machine 2026-10-25 06:52 UTC and copied byte for byte into the cards.
- [x] brief.md written (eight sections, 先搜 table, three outlines); video.json generated (41 scenes, 92 lines, est. 10.6 min, 86 of 92 lines cued, 11 loops); claims.md with 33 claims; lint 0 errors / 1 intentional warning.
- [x] Verifier round 1 (independent agent, re-ran the three commands here, byte-identical): 58 claims, 45 confirmed, 11 changed (the Japanese PM's X post was 64 minutes before the 14:00 UTC release, not the night before; the 2024 audit was the first 「in years」; Prince's millions came within half a day; NCSC's own wording; 8.1 以下), one not found (Internet Archive, dropped) → verify-1.md. Round 2 (a second agent): 34 rows re-checked, one change (the NCSC offline advice follows the temporary mitigations) → verify-2.md.
- [x] Blind read round 1 (narration only): 9/13 (no_spoiler and no_toc are the five-sentence teaching opening by design; no_recap and no_detour fixed: four repeats became named callbacks, three names fewer read aloud, the 8.3.36 vs 8.3.6 contrast spoken as 小版本 36 對 6, first-hearing terms get a clause, the 10/23 advisory tied back to 緩解不是修補). Listener pass applied 22 rewordings and 4 splits (100 lines). Round 2 blind read recorded with `narrative --answers` (see Notes).
- [x] Quotes get `translation` on the three quote cards, revealed on the sentence that says it in Chinese.
- [ ] Commit and push to `claude/focused-hopper-zq70n8`; open the PR; the owner runs the gates from a machine with the video token.

## How to verify

```bash
node tools/video/cli.mjs lint --slug php2shell-ai-found-it-first
node tools/video/cli.mjs status --slug php2shell-ai-found-it-first
node --test tools/skills.test.mjs
npm run check:tasks
```

## Notes

- Outline gate: `review-push --gate outline` 2026-10-25 07:3x; Jev picked B (0.74, 有示範 0.15, below 0.6, so not auto-approved); the owner approved the card on /admin/videos with Jev's pre-selected B. Asked in chat the same hour, the owner chose **A** (the script as written); the site's record still says B and a re-push shows 「approved」 unchanged, so the decision is recorded here and in claims.md, not on the site.
- Pairing: `login --name cloud-php2shell-20261025` allowed by the owner 2026-10-25 07:33 UTC (token in this container only); tts dry-run 3,185 characters; first synthesis 96 lines, 3,232 characters, narration 10:45; re-synthesis after the listener pass reuses the unchanged lines.

- Claimed with `--force`: `docs/videos/lexicon.json` is append-only and shared with four stale video tickets; `.agents/skills/youtube-video/SKILL.md` is also in the scope of PR #1843's ticket (`2026-10-25-record-the-english-card-eight-language`, rule 14) and of stale `2026-10-14-ai-and-tech-videos-tell-one` / `2026-10-20-tutorial-flow-and-hooks-rules-learned`; this ticket only adds one row to the reference table and a new reference file, so a later merge should not collide.
- References live only under `.agents/skills/youtube-video/references/` (the skills test refuses copies under `.claude/`); the SKILL.md row names the file by repository-root path.
- Card language follows PR #1843's final wording (c31d1bfec): zh-TW cards, English nouns and quotes; `google-ai-search-ads-exception` was remade with zh-TW cards and `quote.translation`, so this video does the same.
- The brief's 「先搜」 table has no subscriber counts (watch pages 429); the study records that gap.
- The lint estimate is 10.6 min against `target_minutes` [8, 9]; the owner's rule is 8 minutes or more, so nothing was cut.
