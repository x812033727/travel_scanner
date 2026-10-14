---
id: 2026-10-14-five-curio-style-brand-story-video
title: Five Curio-style brand story video production packages
status: in-progress
priority: P1
area: docs
owner: codex-8a78
claimed_at: 2026-10-14T13:52:51Z
created_at: 2026-10-14T13:52:35Z
completed_at:
branch: codex/brand-stories-five-20261014
depends_on:
  - 2026-10-14-correct-a21-pringles-patent-fact-and
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
- [ ] The five films are rendered, audio/visual/narrative QA passes, and the owner's acceptance and any private upload are recorded separately.

## Steps

- [x] Check existing Curio cut, brand-story worker, approved bank, active ownership and current branch.
- [x] Select five reviewed stories and write individual production treatments.
- [x] Verify cited primary facts, title boundaries and setup/payoff logic across the batch; note source-plan corrections that still need a new independent review.
- [x] Preflight brand assets, local production route and expected image cost; live host state and media budget remain unverified.
- [ ] Produce five media packages, review complete cuts, and prepare private upload metadata and Studio end-screen instructions.

## How to verify

Run `node tools/video/story-plans/validate.mjs` to confirm the original plan bank still validates, `npm run check:tasks`, and editorially check each treatment against its `stories/<id>.json` and `reviews/<id>.json`. Media acceptance later requires measured duration, full decode, TTS and subtitle checks, scene contact sheet review, `qa`, actual owner viewing and Studio clickable-element confirmation; a markdown file or a generated thumbnail is not video completion.

## Notes

- Initial five: A16 Costco, A21 Pringles, A29 LEGO, B14 Ajinomoto, A37 Adidas/Puma. Excludes the existing A01/B18 pilot subjects. The September 28 bank review is routing evidence; video-specific narration still needs fact and story review.
- The current v4 full-channel assets are a five-second bumper after the 30–60 second cold open, and a 21-second end-screen animation/background. The v4 timing correction in `tasks/open/2026-10-12-correct-v4-youtube-end-screen-timing.md` places Studio's real clickable cards in the **final 16 seconds**; `docs/videos/BRANDING.md` still says 17 seconds and has its own correction ticket.
- No production host import, media spend, upload or owner playback has been performed for this batch as of task creation. Keep the original 100-story schedule and SHA-bound reviews unchanged while writing treatments.
- 2026-10-14: Seven files in `docs/videos/brand-stories-five-20261014/` give the five treatments, batch index and `PREFLIGHT.md`; the preflight records local hashes, missing workspaces, cost assumption and worker-input gap. The original bank still validates (100 stories, 0 problems, 4 pre-existing thumbnail warnings for these five); `npm run check:tasks` passes with unrelated stale-claim warnings.
- Independent QA found A21's original approved plan misreads the patent's raw-slice/dough alternatives and might cause the worker to regenerate a false claim. The local treatment corrects it; task `2026-10-14-correct-a21-pringles-patent-fact-and` covers the source-plan/review correction before production. No new five-episode payload or server-side dry-run has been made. The five-film queue position relative to A01/B18 and the original 50-day schedule awaits the owner's choice.
- Local `npm ci` completed. With the repo-documented bundled Node 24.19.0, `npm run test:docs-videos` passed 215/215; system Node 24.13.0 first hit its documented native `cpSync` crash on the Unicode worktree path. The video CLI now reads v4 branding, but reports `series: null`, `installed: false`: no episode has branding installed. Read-only relative-link check across the seven new Markdown files found zero broken links.
