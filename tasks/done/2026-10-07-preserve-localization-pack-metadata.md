---
id: 2026-10-07-preserve-localization-pack-metadata
title: Preserve article aliases and related links in localization assembly
status: done
priority: P1
area: tools
owner: codex-article-localization-4e16
claimed_at: 2026-10-07T05:32:24Z
created_at: 2026-10-07T05:32:23Z
completed_at: 2026-10-07T06:11:03Z
branch: codex/article-missing-locales-20261007
depends_on: []
scope:
  - docs/article-localization/assemble_bundle.py
  - docs/article-localization/test_assemble_bundle.py
  - docs/article-localization/README.md
---

# Preserve article aliases and related links in localization assembly

## Why

The official assembler drops aliases, ordered related-article picks and news_date
when an older baseline omits them. Golden Week installation exposed the loss in
a local content pack; production was unchanged and the exact source was restored.

## Definition of done

- [x] Preserve every hash-verified repository root field omitted from baseline metadata.
- [x] Keep explicit baseline metadata authoritative and preserve all source/review guards.
- [x] Demonstrate the loss before the fix and pass assembler/installer regression tests.
- [ ] Reassemble/reinstall the real reviewed wave and include the fix in reviewed PR.

## Steps

- [x] Preserve failed candidate, original bytes, journal and obsolete admission receipt.
- [x] Add real assembly/publication/source-correction metadata regression cases.
- [x] Merge pinned repository root fields before explicit baseline metadata and reviewed locales.
- [x] Run 40 assembler/installer tests plus scoped ruff and independent code review.
- [x] Verify real restored Golden Week root metadata and official replay.
- [ ] Merge and close this tool task.

## How to verify

Run test_assemble_bundle.py and test_install_bundle.py in the API environment.
Check aliases, related and news_date preservation; deliberate conflicts must use
explicit baseline values, including empty/null. Tampered pack bytes must refuse
without output. Validate all original metadata and documents in the real bundle.

## Notes

- Regression before fix: 1 failed, 2 passed (aliases/related/news_date were lost).
- After fix: 40 passed; scoped ruff passed.
- Independent six-case assembly review PASS SHA
  `b395d261a20d5291cdcd37bde5c18023b9672127498fb36bf2b4ba786138dbc4`.
- Root/core metadata from official baseline retains precedence. Locale/source-correction
  guards and publisher remain unchanged; no production metadata mutation is added.
- Real Golden Week independent metadata review PASS SHA
  cab59f541698e4bf5eead16b1ae6a1eec2634d92445e906f23783726a71eeb78.
- Final real manifest eb0ad09738c593b7a2a16fbb4e098aae531bcf5b49153c52cf0121e7fe9a6cec
  preserves both aliases and four ordered related picks. Official replay is unchanged.

### Content PR handoff

PR: https://github.com/x812033727/travel_scanner/pull/1365.
Authoring, exact independent review, local validation and local installation/replay
are complete for this ticket's selected scope. Required GitHub checks and merge
remain enforced PR gates; marking this authoring ticket done does not claim those
checks are green. The PR remains draft pending owner approval.
Production deployment, publication and public desktop/mobile verification remain
open in 2026-10-07-release-localized-travel-life-wave-20261007.
Any unchecked CI/merge/publication lines above are handed to those explicit gates,
not waived or reported as completed.
