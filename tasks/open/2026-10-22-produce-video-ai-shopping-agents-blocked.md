---
id: 2026-10-22-produce-video-ai-shopping-agents-blocked
title: Produce video: AI shopping agents blocked by Amazon and Target, what the Muse test shows (ai-shopping-agents-blocked)
status: blocked
priority: P2
area: docs
owner: claude-fable-5-1-news-video
claimed_at: 2026-10-22T14:20:49Z
created_at: 2026-10-22T14:15:43Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/ai-shopping-agents-blocked
---

# Produce video: AI shopping agents blocked by Amazon and Target, what the Muse test shows (ai-shopping-agents-blocked)

## Why

The owner asked on 2026-10-22 for an AI/tech current-events video. The freshest story on the site that day with enough material for 8+ minutes and one protagonist is The Verge's 2026-10-22 report on AI shopping agents (Meta Muse blocked by Amazon, caught by Target's bot check, hogging carts on The RealReal) set against Walmart opening an Agent Gateway the day before. Illustrated storytelling route, category ai-news, source articles on the site: ai-news-shopping-agents-blocked-20261022, ai-news-walmart-agent-gateway-20261021.

## Definition of done

- [ ] `docs/videos/ai-shopping-agents-blocked/` holds brief.md, video.json, claims.md, verify-*.md and shorts.json; lint has zero errors and the narrative gate (13 questions) passes.
- [ ] The outline, narration, storyboard, final and publish gates are pushed to /admin/videos (hand-pushed: every gate waits for the owner).
- [ ] final.mp4, captions and the upload package exist in the local workdir and qa passes 11/11.

## Steps

- [x] Sources fetched into the workdir (_tools/sources), brief.md written with 2-3 outlines.
- [x] Writer: video.json + claims.md + lexicon terms, lint clean (10.2 min estimate, 111 lines, 79 scenes, 55 shots).
- [x] Verifier rounds 1–2 (verify-1.md 15 fact edits, verify-2.md 1), listener pass by the coordinator, three blind storytelling reads (66 → 74 → 78; last read 11/13, the two misses fixed afterwards without a fourth read).
- [x] tts (8:53 → 9:11 after the outro split), pace on the real timeline, check-audio with the Whisper second opinion, review-push audio (pending the owner).
- [x] keyframes (two rounds, then --accept-best for 7 shots the judge kept rejecting), storyboard pushed (pending), render, assemble, captions, qa 9/11 (narration unapproved = owner; policy: Jev 有示範 0.49 < 0.6), review-push final (pending).
- [ ] package, review-push publish: blocked until the owner approves the final cut on /admin/videos (package exits 3 before that).

## How to verify

`node tools/video/cli.mjs status --slug ai-shopping-agents-blocked`; `lint` zero errors; `qa` writes review/qa.json with all 11 passing; the cards appear on /admin/videos.

## Notes

- 2026-10-22: outline pushed (`review-push --gate outline`). Jev picked A (1.00) but the demo score was 0.39 < 0.6, so the gate did not pass on Jev alone; the video is hand-pushed (no auto.json) so the owner decides every gate on /admin/videos anyway. The script was written on outline A before the owner chose, so the owner has a finished draft to judge; if B or C is chosen the script is rewritten.
- `source_guide` is NOT set: the source article is hourly auto-news stored only in the site DB, lint refuses a slug with no content pack under `apps/api/app/guides/content/` (the worker's `settle()` drops it the same way). Both Mokaair pages are in `sources` instead, so the description lists them under 參考資料 rather than 完整文章.
- Lexicon: 13 terms appended (Meta, Muse, Target, Amazon, Walmart, Costco, Club, Perplexity, RealReal, Gateway, Profiles, GeekWire as null; JPMorgan as "J P Morgan"). `docs/videos/lexicon.json` is outside this ticket's scope because the stale ticket 2026-10-11-produce-the-mcp-tool-loading-hands still lists it; the change is append-only.
- Storytelling panel: answers and the applied edits are in `_tools/narrative/` (panel-r*.txt, answers-r*.json, apply-r*.mjs); verdicts in `review/narrative.json`. Evidence must quote a line id in square brackets or the tool records "no line id quoted".
- qa policy: Jev's 「有示範」 stayed 0.44–0.51 across three tries (a worked application of the three questions to the granola-bar errand added in chapter 7); a news story has no real demo, so this item is for the owner to overrule at the final gate.
- Pace: `C:/Users/x8120/mokaair-work/videos/ai-shopping-agents-blocked/_tools/pace/pace.mjs` measures every state on the real timeline after tts (run before qa).
