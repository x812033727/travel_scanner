# Route B rehearsal, 2026-10-07

The reviewed T1 wave passed an isolated PostgreSQL rehearsal using the actual
deployed API image. Eight missing language documents were drafted and published
in the synthetic database; replay made no further writes. Production data was
unchanged. This record does not authorize production publication.

The sanitized [record](20261007-t1.json) has SHA-256
`eaea56580f83ff71090ecdb8393f38ebc39bdc338abcc3936c34eda17bb41502`.
Raw evidence and the synthetic restore dump are preserved outside the repository.

- API image: `sha256:18584ecf2c9d143c00e72d30c69ec4db8cfad5db804c5f1d961e1a2c342f6d2d`.
- Runtime commit: `2024304170c6b43ecb4259e6b4fb0ce8a60d9893`.
- Prospective content commit: `280f28fdb096a7f4dae95cd9306306705dddf5b6`.
- Articles: `marketing-mix-models`, `brand-tone-vibe-marketing`.
- Target languages: en, ja, ko, zh-CN; eight documents and 24 localized assets.
- Independent review: `47a93efa3792e93cf9965a3c5cd69f7b51c4800e83595d8013669f3a06e6ec48`.
- Isolated manifest: `00c64b40dce0ae70faa858bafc2c843b69fdbc18c0e1696ee772c4ea5ded47c3`.

Thirteen cases passed: setup, successful publication/replay, source conflicts
before and after dry-run, hide/expiry, a late hold, row/advisory locks,
interruptions before commit and after a lost response, and version-guarded locale
withdrawal. Recovery used the same journal and reconciled uncertain intents
without duplicate writes. Source locales, article roots and an unselected
sentinel remained intact. Recompilation was deterministic.

The database used synthetic identities, no production credentials or mounts, an
internal network and no published ports. Images were unchanged and needed no
package installation. Fault injection used temporary process-local wrappers
around the deployed service. An initial external seed harness error was preserved
and corrected before a fresh migration and all passing cases.

Both articles are life articles, so `publish-hubs` completed with zero operations.
This does not verify a real travel-hub dependency write. The isolated manifest
differs from the production-snapshot bundle because it binds synthetic identities.
Any changed deployed image or baseline requires fresh preflight, backup, holds
and the release ticket's owner gate.
