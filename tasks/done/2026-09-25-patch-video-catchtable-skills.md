---
id: 2026-09-25-patch-video-catchtable-skills
title: Fill the youtube-video and catchtable-discovery skills with what only memory knew
status: done
priority: P2
area: tools
owner: claude-opus-5-5-patch-video-catchtable-skills
claimed_at: 2026-09-25T15:21:17Z
created_at: 2026-09-25T15:20:37Z
completed_at: 2026-09-25T15:21:35Z
branch: claude/patch-video-catchtable-skills
depends_on: []
scope:
  - .agents/skills/youtube-video
  - .claude/skills/youtube-video
  - .agents/skills/catchtable-discovery
  - .claude/skills/catchtable-discovery
---

# Fill the youtube-video and catchtable-discovery skills with what only memory knew

## Why

The youtube-video and catchtable-discovery skills lagged behind what earlier sessions learned and kept only in personal memory. The video skill still described Azure as the only narration voice and told the owner to paste a token into `login`, although the channel voice is Gemini (Sulafat, PR #725) and `login` now pairs through the admin card (RFC 8628 device flow). Operational facts about the host video worker, ffmpeg and local-tool pitfalls, and CatchTable batch gotchas (locale URLs, stderr output, `would_update` rows, coordinate sources, admin UI quirks, unreachable Busan sites) were not written anywhere a new agent would read.

## Definition of done

- [x] `references/automated.md` describes Gemini as the channel voice, the pairing flow, the Gemini character cap, measured speaking rate, narration convergence, ffmpeg and local pitfalls, and a new host-worker section.
- [x] youtube-video SKILL.md rule 9 describes pairing instead of pasting; the `description:` line is untouched (PR #767 owns it).
- [x] catchtable-discovery SKILL.md, `references/browser.md` and `references/admin.md` carry items 73–84 of the coverage report.
- [x] `.claude/skills/` copies are byte-identical.

## Steps

- [x] Verify the voice provider and pairing flow against `apps/api/app/video_speech/` and `tools/video/tts/`.
- [x] Verify the CatchTable facts against `apps/api/app/foods/router.py`, `platform_review_import.py` and `docs/catchtable-ranking-discovery.md`.
- [x] Edit `.agents/skills/...`, copy to `.claude/skills/...`.

## How to verify

`node --test tools/skills.test.mjs` passes. `grep -n "Gemini" .agents/skills/youtube-video/references/automated.md` shows the voice setup row.

## Notes

- The youtube-video `description:` still says 伺服器用 Azure 合成台灣口音旁白 and "server-side Azure Taiwanese Mandarin narration"; it should say the server synthesizes the narration with Gemini (or Azure). Left for PR #767, which rewrites the descriptions.
- `docs/videos/README.md` 聲音 table still says the channel voice is 還沒選 and the provider is Azure; out of this task's scope.
- The Gemini code does send `<long pause>`/`<short pause>` tags (apps/api/app/video_speech/gemini.py), so the skill says pauses are tags with imprecise length rather than "pause tags don't work".
- Items 67, 68, 71, 85 target task-board/deploy and were left to that agent.
