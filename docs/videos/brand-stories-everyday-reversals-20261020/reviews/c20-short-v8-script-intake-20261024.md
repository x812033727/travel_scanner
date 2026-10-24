# C20 Zippo short-v8 backend script intake

## Approval and exact source

- The owner approved the precise C20 v8 36-line narration and 36-scene direction in PR #1808, then separately approved a local pilot capped at US$25. These are distinct from backend review, payment execution, upload and publication.
- The approved candidate is `docs/videos/story-everyday-zippo-c20/reviews/v8-short-script-candidate-20261024.md`, SHA-256 `8bf33f7f733d5acb8c7ac64186b5932c43e6bb06867a6ffbf2ecc6bf0e68d82d`. Its historical HOLD label predates the owner's approval. The generated `story-everyday-zippo-c20-short-v8/script.md` projection has SHA-256 `f02b94989765eadff8661f73b2c59a0ba8c3950b4bddd2cdfc0a1a2ad9fffa65`. The canonical `video.json` has SHA-256 `b97a36bf3247804e579ec00595a210b3e077cfecc0691b70e16eac7a115e5b62`.
- The original six-chapter candidate, one-table projection and canonical video match on all 36 narration IDs and visible text in the same order. Chapter labels are taken from the approved candidate; the generated projection is left byte-for-byte intact. The historical 42-line C20 source remains separate.

## Guard and backend sequence

- `approved-scripts.json` adds C20 only under the exact `story-everyday-zippo-c20-short-v8` slug, 36 lines, and frozen projection hash. `script-intake.mjs` accepts the generated one-table format only for this exact C20 header/slug/hash, validates the candidate and video hashes, and compares their 36 ID/text pairs before any network call.
- The script intake requires the series paused and episode 20 planned at the exact new slug. A request while production still has the old `story-everyday-zippo-c20` row is refused after one context GET and zero writes. First run the compiled 20-row plan through the host importer as a dry run, require an update of the existing C20 row only, then apply and read back the same row ID. C08 has a separate same-row transition in the same bundle.
- After the new slug is live, `node tools/video/review/script-intake.mjs --id C20 --apply` may create a new project and **pending** script card. It does not approve the card, start a worker, purchase media, upload or publish. The old source/project history is retained; a retry with the same pending card is idempotent.

## Verification before production

`node tools/video/review/script-intake.mjs --id C20` returned 36 lines, the frozen projection SHA and `dry-run-local-only`, without transport. `node --test tools/video/review/script-intake.test.mjs` passed 15/15, including changed file/manifest/source/video/nearby slug, damaged single-table format, old backend slug with zero writes, new pending card and retry behavior. `node docs/videos/brand-stories-everyday-reversals-20261020/build.mjs --check` passed 20 reviewed rows; `git diff --check` passed. These are local checks, not evidence of a production import.
