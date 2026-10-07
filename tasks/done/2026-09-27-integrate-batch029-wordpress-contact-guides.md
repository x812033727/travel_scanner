---
id: 2026-09-27-integrate-batch029-wordpress-contact-guides
title: Integrate Batch029 WordPress contact guides
status: done
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-09-27T10:17:36Z
completed_at: 2026-10-07T01:43:01Z
branch: codex/article-localization-batch029-contact
depends_on: []
scope:
  - apps/api/app/guides/content/wordpress-contact-forms.json
  - apps/api/app/guides/content/wordpress-smtp-delivery.json
  - apps/api/app/guides/content/wordpress-chat-contact-buttons.json
  - apps/api/app/guides/content/wordpress-booking-system.json
  - apps/web/public/guides/wordpress-contact-forms
  - apps/web/public/guides/wordpress-smtp-delivery
  - apps/web/public/guides/wordpress-chat-contact-buttons
  - apps/web/public/guides/wordpress-booking-system
  - tasks/open/2026-09-27-localize-wordpress-contact-forms-and-smtp.md
  - tasks/open/2026-09-27-localize-wordpress-chat-and-booking-batch029.md
---

# Integrate Batch029 WordPress contact guides

## Why

Four published WordPress guides about contact forms, SMTP delivery, chat/contact buttons and booking systems currently have only Traditional Chinese documents. This batch adds complete English, Japanese, Korean and Simplified Chinese documents and language-specific text-bearing figures, while leaving existing Traditional Chinese publication and article metadata unchanged. The two pairs were authored and reviewed in disjoint worktrees; this task owns their integration and reviewable PR preparation. Production import, publication and browser QA are separate release work.

## Definition of done

- [x] All four packs contain the same five locales: 20 complete documents in total, including 16 newly authored translations; translated metadata, body blocks, tables, callouts, links, image descriptions and source titles match the original scope.
- [x] The 48 new localized image assets comprise 32 SVGs and 16 rendered JPG covers, with no reported browser-layout issue or missing glyph; 12 original assets are preserved.
- [x] Source zh-TW documents, root metadata, source URLs/dates, technical terms and conditional internal-link targets remain unchanged; all 52 new/modified content blobs match their reviewed Pair A/B commits exactly.
- [x] Both pairs have reciprocal independent editorial/structural review and the combined integration has an independent source and image check.
- [ ] Relevant API, tools, frontend, task and CI checks pass or any limitation is recorded precisely; push the rebased branch and open a reviewable PR, leaving merge disabled until the coordinator finishes the Batch028 release.

## Steps

- [x] Claim exact four-pack/two-pair-task scope after both original owners release their tasks; create a separate worktree from current `origin/main`.
- [x] Cherry-pick the two content commits plus each pair's review/release handoff commits without conflicts; compare each integrated content blob with its author commit.
- [x] Run four-pack lint and inspect browser layout receipts and all 48 target assets.
- [x] Finish combined scoped checks, rebase onto latest `origin/main`, review the 52 content blobs and PR copy, then push, open the PR and attach it to the task without enabling auto-merge.

## How to verify

From `apps/api`, run `uv run python -m app.guides.pack_cli lint --slug <slug>` for each of the four slugs, `uv run ruff check .`, `uv run mypy app` and `uv run pytest -q`. From the root run `npm run check:tasks`, `npm run check:i18n`, `npm run lint:web`, `npm run typecheck:web`, `npm run test:web` and `npm run test:tools`. Inspect `C:/Users/x8120/.codex/article-localization-release/batch029-contact/integration-review.json` for 52 exact blob hashes and preserved sources, and `integration-image-review.json` for all 48 images and the two author browser-render receipts. Recheck production versions and statuses separately before any release operation.

## Notes

Base: `origin/main` `6f66eebd49039d81735ca6658df8e804c4d59a80` at integration creation, cleanly rebased onto `f44555bb97153fa05cf3ca565ffa28db473e86d3` before PR. The four scoped article/asset paths did not change from the Pair A/B author base `bd98f4678ddc786ef1b058d30a950b36e11ec586`. Pair A original commits `0fd90e79` content and `e5e99822` task release; Pair B original commits `e52cc806` content, `927b5577` review and `872e2662` task release. The pairs' changed path sets have no overlap. Pair A/B tasks are open and unclaimed in this branch; this integration task is the only active claimant of the four target paths.

Fresh production source was captured in a `REPEATABLE READ, READ ONLY` transaction on 2026-09-27T09:29:15Z. All four articles were published, active and unexpired at article version 2; their zh-TW draft/published locale version was 4, with no en/ja/ko/zh-CN locale row. Snapshot SHA-256 `2557112824db91c3eff0365927d48230d42aee65c7c3a09f13c5d8a0ac6b731d`, inventory SHA-256 `3331a9013922e6549c7c399075d27d760135c9f30590d4634eda2b887d0ef850`; all twelve production source assets matched Git. This historical snapshot is an authorship pin, not authorization to skip a fresh release-time conflict check.

Pair A author receipt SHA-256 `b5e8f41578988d98e1c657034936ba79aef7ddf400cc738ed15d1d61fafc7e2b` and Edge layout review SHA-256 `452d2fb2107873b928c3898bd5fe7fcc0d9aa129c8ba9b548e96df62c5715b1b`; Pair B independently reviewed Pair A (SHA-256 `e46950db6f336ffb6e6778ef56b14b1aa1b8363451481134e5f7da54c9f8b1eb`). Pair B author render receipt and Pair A independent Pair B review are in the same external evidence directory; Pair A review SHA-256 `4081a3bc726ce2d0f3421d826dff21ff61b88b283dee3ae44c0ffbd38fdf8524`. Integration exact-byte/source receipt after rebase SHA-256 `751e0770ae2a0fec9b83c4f6664cfba08c445642beb680d24b13cc49f91fbdae`; integration image receipt SHA-256 `6fcea5276769e2447ba2965837d9a24beb7b058481459c7b77133c538eb2ff9d`. The coordinator independently checked all 20 document structures, links, sources, target abstracts/openings and all eight five-locale hero/diagram contact sheets; no omissions or visible layout defects were found. After rebase, the PR diff still contains only the 52 scoped content files and three task records; `check:tasks` passes.

All four scoped pack lints pass with only inherited `no_summary` and English text-length advisories. Focused API tests `test_guides_pack_ingest.py`, `test_guides_content_links.py`, `test_guide_rich_blocks.py` and `test_guides_publish_bundle.py`: 72 passed, 2 skipped. `test_guides_content_pack.py` independently: 9 passed, 5 skipped. API Ruff and mypy pass. Root checks `check:tasks` and `check:i18n` pass, web lint and typecheck pass. The full tools suite passes under installed Node v24.19.0: 411 passed, 1 skipped; system Node v24.13.0 silently fails 17 unrelated video-tool test files because its version is below the runtime requirement. No repository change was needed to fix the environment.

Full Windows `test:web` ran for over 18 minutes without a final summary; the coordinator directed us to stop only this worktree's Vitest process and leave the complete suite to PR CI. A broad API pytest run reached about 42% and printed `EEEF` before it was stopped; the exact failing test names were not emitted. A separate `-x` diagnostic run and same-main API baseline worktree were prepared but stopped at the coordinator's direction to avoid delaying PR review; its partial progress log is `C:/Users/x8120/.codex/article-localization-release/batch029-contact/full-api-first-failure.log`. These broad suites are **not** claimed as passed; PR CI must validate them before merge, and any red check must be investigated against the same-main baseline. All scoped content/guide checks above passed.

The coordinator has authorized a PR after validation and rebase, but explicitly deferred merge until the Batch028 production release finishes. This does not authorize any production import or publication. No content has been imported, published or deployed by this integration task.

Review PR: https://github.com/x812033727/travel_scanner/pull/857. It was opened after the `f44555bb97153fa05cf3ca565ffa28db473e86d3` rebase and attached to the Codex task; auto-merge is off. The broad API/web checks above remain CI gates before merge. Keep this task in `review` until the PR is merged and do not mistake the review branch for a production release.
- 2026-10-04 board sweep (claude-opus-5-5-incomplete-tickets, approved by the owner): the claim by codex-batch029-integrator (since 2026-09-27T10:17:43Z) was stale and is released so it stops locking its scope. Landed: #857. Still open: Relevant API/tools/web/CI checks pass; push rebased branch and open PR (done via #857, CI passed to merge).

## 2026-10-07 看板總整理（由站主授權，非原持有者）

標記完成。依據：PR #857 merged 2026-09-27 (25da6c3c) after CI; wordpress-contact-forms/smtp-delivery/chat-contact-buttons/booking-system.json on origin/main all have zh-TW,en,ja,ko,zh-CN + hero-<loc>.jpg/diagram-1-<loc>.svg assets; published per tasks/done/2026-09-27-record-batch029-five-language-wordpress-contact.md
