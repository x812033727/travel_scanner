# Batch036 measurement source-link corrections

The four published zh-TW source guides matched their repository packs at the
2026-09-28 read-only inventory (article v2, source published v4). Seven ordinary
analytics words linked to unrelated AI term guides. This patch keeps the visible
prose and all other pack data identical while changing exactly those seven
inline nodes from `article` to `text`. It must be followed by a guarded new
zh-TW draft and publication before translations bind to the corrected source.

| Source guide | Wrong links removed | Original pack SHA-256 | Corrected pack SHA-256 |
| --- | ---: | --- | --- |
| `ga4-site-measurement` | 2 | `1f4bd09d085efda48b48ce368d1f316ceb7129e6669cf36476d7cf3eabb58af0` | `3b367d128b1e94844742edc2eb8704c2573c624def14fd037d441b5cb59ce428` |
| `ga4-sessions-engagement` | 1 | `0867dc0196146367d543ae9610e04ee0b6e6ab237e499f849ffb9d00b567bba7` | `c7b0a7efaa13b75d2b72badba865894765788103e3a0cc35611b2041a0818682` |
| `google-search-console-workflow` | 2 | `31518bfc865f97b0b343d354dc4d0a6980e3800a09643d713d82f7f82e62bd4f` | `ec573e1b2fa0213e1c2773bc43b0a562e3a2c230315773369ec4d4a79124c18c` |
| `utm-link-conventions` | 2 | `035b90f6a33f43886b619312516eccb661c9baff8dc9290df0ddf145ce490a45` | `7eec1797e970f002434b829c880814a6db1e50d608b3c2c566aa259e8a006e30` |

The pinned [inventory finding](../../tasks/open/2026-09-28-correct-measurement-guide-source-links-before.md)
is backed by the external read-only finding receipt, SHA-256
`8275fb90b6f812c519d90f30fd80d2920b33c10a432a2548fe9dd441f800ed75`.
An exact JSON comparison to `origin/main` passed after applying only the seven
specified link-to-text substitutions. Each pack's scoped lint passed with only
its existing `no_summary` advisory. No images, article metadata, sources,
dates, URLs, or other links changed. This PR does not deploy or publish content.

Validation: four targeted pack lints exited 0 (only existing `no_summary`
advisories); `tests/test_guides_content_pack.py` and
`tests/test_guides_content_links.py` reported 12 passed, 5 skipped;
`npm run check:tasks` and `git diff --check` passed. The task checker reports
unrelated aged claims and existing overlap warnings.
