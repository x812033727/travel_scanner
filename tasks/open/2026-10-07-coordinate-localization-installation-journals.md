---
id: 2026-10-07-coordinate-localization-installation-journals
title: Coordinate reviewed localization installation journals
status: in-progress
priority: P1
area: tools
owner: codex-article-localization-4e16
claimed_at: 2026-10-07T06:02:38Z
created_at: 2026-10-07T05:40:05Z
completed_at:
branch: codex/article-missing-locales-20261007
depends_on: []
scope:
  - docs/article-localization/installations/.lock
  - docs/article-localization/installations/.gitignore
  - .codex/localization-staging/cherry-korea-20261007
  - .codex/localization-staging/entry-powerbank-20261007
  - docs/article-localization/installations/bundles/c96737f04540a86d
---

# Coordinate reviewed localization installation journals

## Why

Independent reviewed article jobs need a coordinated installer lock and durable
per-bundle journals. These journals include private runtime identities and copied
inputs and must remain recoverable without entering Git.

## Definition of done

- [x] Official installs and replay use one coordinated lock and exact pinned inputs.
- [x] Preserve historical failed candidates and journals outside Git.
- [x] Ignore private runtime journals while tracking their privacy rule.
- [ ] Include the rule and installation handoff in a reviewed content PR.

## Steps

- [x] Claim the shared lock separately from individual article scopes.
- [x] Stage exact-byte inputs inside the repository as the installer requires.
- [x] Install/replay Cherry and Korea without changing original job inputs.
- [x] Preserve the superseded Cherry 14px candidate before correcting/reinstalling.

## How to verify

Run the official installer with the same manifest hash and byte-identical staged
baseline/work inputs. Verify the completed receipt and journal, unchanged original
source/photo hashes, and `git check-ignore` for runtime files. Replay must leave
installed bytes and journals unchanged.

## Notes

- Runtime journals and private staged inputs remain on the owner's persistent storage.
- The tracked installations/.gitignore ignores everything except itself.
- Cherry final manifest: 78d78b438488a1f94e231ec2786bd767f5216005f5e3c647300781d787f9f48a.
- Korea manifest: 6503955dcf7b6e4c41665199d1557a119800b613d7b0c0008c28b4bba803810e.
- Both completed official replay with preserved source/photo bytes. No production
  write or publication is authorized by this local installation evidence.
