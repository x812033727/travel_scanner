# Independent collector backup-directory increment review

Reviewer: codex-independent-a01-lexicon-1017, 2026-10-17 (Asia/Taipei).

Static scope: 0 P1/P2 identified. adopt-pinned.mjs SHA 4d0e27e5515e5f27cfc70c56b13d08d8dc75c5c6fdfb74bcc4395f82e12a2335 and adopt-pinned.test.mjs SHA 1d2e96e3556bcd222c338460addae60ddf5eb7e7c14aa086f18f24046189d447.

Read the precise collector change: manual-revisions entries remain safe checked directories; only absent installation-receipt files are skipped as backup-only, while existing receipts are lstat-checked regular/nonsymlink before copying. Historical referenced receipts remain mandatory through exact source-plan validation, so absence cannot silently authorize a weaker baseline. A missing receipt is distinct from an existing dangling link: the latter now fails the explicit lstat symlink check. Existing backup files are preserved in place; this function copies an allowlisted source projection, not every backup artifact.

Read three regressions covering backup preservation, required receipt removal and external revision junction refusal. Recommended symlink regression was added by the author. Parent reports focused3 PASS; this reviewer's focused/full reruns are pending and no independent final green result is claimed here. Publication/crash/recovery behavior is unchanged. No host/apply or implementation edit was performed. Production remains held. See the repo-external host-caller-r4-review.md in the afternoon capture directory for exact bundle/caller bindings and limitations.

## Independent focused-test completion supplement

After writing the preceding report, this reviewer observed its independently launched final focused run complete: backup-only preservation, missing referenced receipt refusal and external revision junction refusal all PASS (3/3, zero failed; 61.09 seconds). API/test hashes match the bound values above. Full-suite runs remain pending; no full-suite PASS is inferred. The r4 archive hash was also independently recomputed as c5fa4c2477714384bb61bae12b81e31ca30fe8f44f491d008f4dfa4c0b2bf1c0.

## Independent full-suite completion supplement

The final independently launched suite has now completed: 6/6 PASS, zero failed, including all seven simulated crash boundaries and committed recovery plus all three collector regressions (275.69 seconds). Returned API/test hashes remain 4d0e27e5515e5f27cfc70c56b13d08d8dc75c5c6fdfb74bcc4395f82e12a2335 / 1d2e96e3556bcd222c338460addae60ddf5eb7e7c14aa086f18f24046189d447. The previously pending statement is historical; no independent run remains pending in this reviewer. An earlier 5-test run also completed green, but only the final 6-test run includes the junction regression.
