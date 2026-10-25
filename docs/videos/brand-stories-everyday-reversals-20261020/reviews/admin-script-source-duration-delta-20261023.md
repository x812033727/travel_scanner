# Admin source-script display: independent duration delta review

Reviewer: `codex-independent-c-series-duration-review`
Date: 2026-10-23
Integration HEAD reviewed: `41b4607053981fcd24ce74c314dd1ed5f69f489e`
Baseline: `origin/main` at review time; inspected `git diff --unified=0 origin/main...HEAD` for the six paths below and confirmed no working-tree changes to them.

| Reviewed path | Current SHA-256 |
| --- | --- |
| `apps/web/components/admin-video-review-card.tsx` | `d2175914066087259a671b20bec3c79175a75c89ab240621d1a46bc07b95d87e` |
| `apps/web/messages/en/admin.json` | `36a759c2478924db3fbd163deaa7579b8d4897a2148b026cfe5f49f6e1dd242b` |
| `apps/web/messages/ja/admin.json` | `60133ff6562aeb37ff7b19548f30b315d0ffcc6d9f0eb14a64c525239304ec17` |
| `apps/web/messages/ko/admin.json` | `c7dfd04b60db1e5ef1330a7d04326da6885dfc67af7fc7a0c6872a6fddbb1cee` |
| `apps/web/messages/zh-CN/admin.json` | `5fc68116b39d6a598ff888f592685a351728d8a45c93f564e1fbfa56c9468f4f` |
| `apps/web/messages/zh-TW/admin.json` | `558ed16db8a1b7ebcc4c08aa799d183be83a2a4ff7750886fff91715d80c5f67` |

## Findings

The component adds `sourceMarkdown = text(review.payload.source_md)` at line 387 and conditionally renders that text in a collapsed `<details>` block at lines 403–406, before the existing script coverage. This reads and displays source material; it does not change the review payload, approvals, or runtime calculations. The five locale files each add one `scriptSourceMarkdown` label at line 2444. Existing duration labels and their arguments are unchanged.

The component's `minutes` display, per-scene `action.seconds` validation and display (lines 414, 419, 430), `RUNTIME_KEYS`, `measuredFrames`, `runtimeEvidence` and `RuntimeDuration` (lines 609–672) are unchanged. In particular, the body target range of 540–1800 seconds, measured proof and hash binding, body acceptance within target ±60 seconds, and OP/ED and presentation budgets retain their existing conditions. No duration target, floor, gate, measurement, or acceptance rule changes in these six files.

Verdict: **PASS — DURATION_ONLY** for this six-file delta. No duration correction is required before rebinding these exact current bytes in the global long-form review. This receipt is supporting evidence; it does not itself update `docs/videos/long-form/review.md` or `review.json`.

Scope limits: static source-diff review only. It does not validate the source-script display's usability, translations, backend import, other files, media, paid generation, deployment, publication, or live admin behavior. No tests or live operations were run for this receipt.
