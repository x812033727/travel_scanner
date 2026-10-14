---
id: 2026-10-14-five-curio-style-brand-story-video
title: Five Curio-style brand story video production packages
status: blocked
priority: P1
area: docs
owner: codex-8a78
claimed_at: 2026-10-14T13:52:51Z
created_at: 2026-10-14T13:52:35Z
completed_at:
branch: codex/brand-stories-five-20261014
depends_on:
  - 2026-10-14-correct-a21-pringles-patent-fact-and
  - 2026-10-14-support-10-minute-minimax-cute-brand
  - 2026-10-14-align-brand-story-cute-prompt-lint
  - 2026-09-28-video-story-pilot
scope:
  - docs/videos/brand-stories-five-20261014
---

# Five Curio-style brand story video production packages

## Why

The owner requested five brand-story films with potential to attract a broad audience. They should use the same story-first structure as 奇聞檔案局: a condensed cold open, animation, one coherent chronological account, a channel outro and clickable next-video elements. The existing owner-approved 100-story bank is the source of checked topics, but each selected film still needs a production-specific causal arc and bookend plan before media is purchased or uploaded.

## Definition of done

- [x] Five distinct, source-bound treatments are available for editorial review, each with a click hypothesis, narrated cold open, six causal beats, open/payoff questions, visual direction, outro and end-screen setup.
- [x] A batch index identifies source plans and review hashes, episode order, technical format, existing media dependencies, and production state without presenting a treatment as a finished MP4.
- [x] A local media and cost preflight identifies the actual route, the worker-input gap, and owner/account/host gates before paid generation; the live-host import dry-run is a later gate.
- [x] Five source-bound, independently reviewed worker-input rows and a compiled five-story dry-run payload use the new MiniMax/10-minute spec without changing the approved 100-story bank.
- [ ] The five films are rendered, audio/visual/narrative QA passes, and the owner's acceptance and any private upload are recorded separately.

## Steps

- [x] Check existing Curio cut, brand-story worker, approved bank, active ownership and current branch.
- [x] Select five reviewed stories and write individual production treatments.
- [x] Verify cited primary facts, title boundaries and setup/payoff logic across the batch; note source-plan corrections that still need a new independent review.
- [x] Preflight brand assets, local production route and expected image cost; live host state and media budget remain unverified.
- [ ] Finish A01/B18 pilot and owner viewing first; then dry-run the reviewed five-story payload, with live slug/state collision checks.
- [ ] Produce five media packages, review complete cuts, and prepare private upload metadata and Studio end-screen instructions.

## How to verify

Run `node tools/video/story-plans/validate.mjs` to confirm the original plan bank still validates; run `node docs/videos/brand-stories-five-20261014/build.mjs` to require five matching new reviews; run Python `check_story_file` on the compiled `stories.json`. `npm run check:tasks` is a required gate after the unrelated A21 duplicate task file is resolved. Media acceptance later requires measured duration, full decode, TTS and subtitle checks, scene contact sheet review, `qa`, actual owner viewing and Studio clickable-element confirmation; a markdown file or generated thumbnail is not video completion.

## Notes

- Initial five: A16 Costco, A21 Pringles, A29 LEGO, B14 Ajinomoto, A37 Adidas/Puma. Excludes the existing A01/B18 pilot subjects. The September 28 bank review is routing evidence; video-specific narration still needs fact and story review.
- The current v4 full-channel assets are a five-second bumper after the 30–60 second cold open, and a 21-second end-screen animation/background. The v4 timing correction in `tasks/open/2026-10-12-correct-v4-youtube-end-screen-timing.md` places Studio's real clickable cards in the **final 16 seconds**; `docs/videos/BRANDING.md` still says 17 seconds and has its own correction ticket.
- No production host import, media spend, upload or owner playback has been performed for this batch as of task creation. Keep the original 100-story schedule and SHA-bound reviews unchanged while writing treatments.
- 2026-10-14: Seven files in `docs/videos/brand-stories-five-20261014/` give the five treatments, batch index and `PREFLIGHT.md`; the preflight records local hashes, missing workspaces, cost assumption and worker-input gap. The original bank still validates (100 stories, 0 problems, 4 pre-existing thumbnail warnings for these five); `npm run check:tasks` passes with unrelated stale-claim warnings.
- Independent QA found A21's original approved plan misreads the patent's raw-slice/dough alternatives and might cause the worker to regenerate a false claim. The local treatment corrects it; task `2026-10-14-correct-a21-pringles-patent-fact-and` covers the source-plan/review correction before production. No new five-episode payload or server-side dry-run has been made. The five-film queue position relative to A01/B18 and the original 50-day schedule awaits the owner's choice.
- Local `npm ci` completed. With the repo-documented bundled Node 24.19.0, `npm run test:docs-videos` passed 215/215; system Node 24.13.0 first hit its documented native `cpSync` crash on the Unicode worktree path. The video CLI now reads v4 branding, but reports `series: null`, `installed: false`: no episode has branding installed. Read-only relative-link check across the seven new Markdown files found zero broken links.
- 2026-10-15 owner decision resolved the former scheduling and visual questions: **complete A01/B18 pilot first, then the five**; use MiniMax `image-01`, exact `look: {"preset":"cute-mystery"}` and about 10 minutes for these five only. The old 100-story and A01/B18 Gemini/13-minute settings remain in their own route. A separate five-story draft series with new `story-five-*` slugs avoids immediate duplication of source-bank slugs; before any wider 100-story rollout, reconcile the five subjects so it cannot publish duplicate versions.
- Draft PR #1499 remains unmerged. The A21 source-plan correction is complete; its ticket still has a Windows filesystem cleanup problem described in that ticket. The five-series code route, new independent reviews and five-row local payload are now complete in this PR; A01/B18 production and owner acceptance, live host/account/spend preflight, five-film media and Studio checks remain open. Do not treat draft PR checks as film acceptance.
- 2026-10-14 follow-up: the separate A21 source-plan correction is complete with independent review SHA `35f8de6e6f2c5ecbd56931a801aec89d58f663168a9f335882ba5d21e3eec34b`; `stories.json` was regenerated and the schedule did not change. This resolves the A21 dependency, while the five-film queue/series decision, production-host preflight, reviewed worker input, media work and owner acceptance remain open.
- 2026-10-15: Owner chose A01/B18 first, then five MiniMax `image-01` / exact `cute-mystery` / about-ten-minute stories. Five rows A29, A16, A37, B14, A21 each have a new hash-bound independent review under `episodes/reviews/`; `build.mjs` compiled `stories.json`, and local JS/Python validation found zero import-shape problems. A29's six annual-report PDFs cannot be read as text by the worker; the reviewer recorded page references and the distinct HTML source coverage. The new route's synthetic A29-with-cast `video.json` passes validation/lint, and original 13-minute custom route tests remain green. None of this creates narration or media. The next five-film gate is the A01/B18 pilot, then live slug/state dry-run and whole-film cost approval.
- 2026-10-15 independent package review found compiled `caveats` had replaced the editor's source boundaries with reviewer notes. `build.mjs` now retains both within the API 800-character limit; the A29 row gives an explicit PDF/manual-number gate and reserves the asset-sale ratio for the final spoken answer. B14/A37 visual wording now matches the 75–120 shot, 5–8 second, preset-only spec. Rebuilt five-story file: 5 rows, 0 Python import problems/refusals. The owner chose the admin UI for pilot readback, but Chrome became unavailable and the in-app webview timed out; the original pilot task records the exact unresolved live and cost gates.
