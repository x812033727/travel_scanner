# A01 round 11 — offline transaction candidate

**Status: local fixture test only. This is not production approval, a host installer, a narrative PASS, an independent script receipt, or permission to generate media.** `installer.mjs` has no CLI and refuses any checkout outside the OS temporary directory without an explicit `A01-ROUND11-OFFLINE-FIXTURE.json` marker. It does not connect to the host, database, admin API, model or media provider. A production adapter must undergo a separate source review and fresh host staging before use.

## Bound edit

The input is the exact six chapter files archived in [`A01-round10-candidate/source/chapters`](../A01-round10-candidate/source/chapters), not the old approved editorial Markdown or a newly imported story. The target is the combined [`A01-round11-candidate/candidate/chapters`](../A01-round11-candidate/candidate/chapters). The package verifier proves exactly these nine semantic changes:

| Chapter | Edit |
| --- | --- |
| `origin` | `origin-01 / zc7k` spoken sentence and `origin-01` image prompt |
| `idea` | `idea-01` and `idea-05` image prompts |
| `turn` | `turn-15` image prompt |
| `now` | `now-01 / 7asx` spoken sentence, claim `n1`, `now-01` and `now-02b` image prompts |

`hook` and `engine` remain byte identical. All six source and target chapter SHA-256 values are checked against the existing candidate manifests. A second, specified digest of the six ordered `key:sha256` lines is `b4d1eb3955f3d1f1db26cee70ad4c75c3b84a2c1e1fa03f1f90bdc7daeb3b821` before and `b0a5703742da75189a834f1c921b05099a54ab1685840afc8525ffa6fa54179f` after. This **chapter digest is distinct** from the historical 80-link host source composite `cf39296d597d36db3cafedc1c2ca5ae730dd104a34b1d1868fb5b83fc089c56b`, whose formula is absent from this offline package. The fixture requires the historical value in the safety evidence and audit tip but does not claim to recalculate that host composite.

The current `engine` chapter still contains stale `e11`/`e3` `NOT FOUND` claim references, and the 520.333-second text estimate is below the cute-story 540-second lower band. This round 11 installer deliberately does not clear those claims or expand the script. Any round 12 source-supported engine expansion and stale-claim cleanup needs a separate versioned target manifest, exact source/target hashes, independent fact/narrative review and new installer review; this tool must reject changed chapter bytes.

## Transaction behavior in the fixture

`planOfflineInstallation()` reads all files without writing. `installOfflineFixture()` requires a recent safety evidence file, an exact approved/observed release SHA and panel-rules SHA, the A01 project blocked after real round 9 (`chapters_link`, `payoffs`, `one_thread`), all six chapters checked/listened, `narrative_fixes=2`, no A01 stage lease, pending stage/media/journal work or pending retry, automatic final approval and series continuation off, and an empty US$25 ledger. The per-video `STOP` file **must already exist** and is neither created nor cleared by the installer. A prior `script-review.json`, timeline or final video is refused. The six chapters, `auto.json`, historic FAIL, generated documents, safety evidence and audit tip are hash-checked before any write and again immediately before commit.

The transaction makes byte-verified backups and an inverse manifest under `manual-revisions/`, replaces only the four changed chapter files plus `auto.json`, and reads back every file. It invalidates `origin` and `now` text checks/listener flags and the aggregate `verified`/`listener_done` flags while retaining all round/cost counters, the round 9 narrative FAIL, other chapters' text checks and old reports. `idea` and `turn` have prompt-only edits: their earlier text checker/listener inputs are unchanged, while old visual review is invalid. It appends an **offline fixture** audit linked to its simulated 80th tip; it does not touch the production audit. A failed write restores exact original bytes, verifies them and retains failure evidence. An unexpected concurrent file edit stops rollback with `MANUAL_RECOVERY_REQUIRED` rather than overwriting another writer.

Backup copying and inverse-manifest creation happen **before** the guarded live-write section. A failure in that setup can leave a partial `manual-revisions/<id>` directory without `failure.json` or a success receipt; the test fault hook exercises failures after the first backup file, before inverse creation and after inverse creation. In all three cases the chapter files, `auto.json`, old audit tip and scoped `STOP` retain their original bytes because no live write has begun. A partial backup or inverse file is **not** a usable rollback authorization. Keep the directory for incident review, independently read back the live source hashes and exact copied files, and decide any manual cleanup or recovery only after that inspection. The fixture never removes a partial revision automatically. A separately reviewed production adapter must explicitly handle and verify setup failures on the real host.

The safety evidence is simulated by tests. It is **not a trusted reading of the production database, lease service, project retry state, deployed worker, cost ledger or audit chain**. The production adapter must collect and independently verify those values, prove the real 80-link chain and its composite algorithm, acquire a safe scoped pause, create an exact backup, integrate with the real audit format, and be separately reviewed. Any mismatch or absent evidence stops installation. The current `#1517` rule change must be independently approved, merged, deployed and read back before a new A01 panel is requested; the fixture test does not establish that release state.

## After a separately reviewed live adaptation

Recheck the actual `origin` and `now` narration/claims through real chapter verifier and listener stages, inspecting their saved patches and keeping historical results. Run a **new** full-film narrative panel under the deployed rules and bind its rules hash to the actual script. A FAIL remains a HOLD; a PASS only reaches the pilot's missing `story/reviews/script-review.json` hold. An independent editor must then compare the actual six chapters, `video.json`, `script.md`, `claims.md`, `verify-1.md` and new narrative result with the frozen A01 reference and sources before signing that exact-file receipt. Only the subsequent explicit A01 retry may enter TTS or MiniMax generation under the existing US$25 all-in authority. Those checker, listener and panel calls may themselves incur model charges. The 520.333-second text estimate and six prompt descriptions do not prove measured length or visual quality.

## Local verification

```sh
node docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/A01-round10-candidate/verify.mjs
node docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/A01-round11-candidate/verify.mjs
node --test docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/A01-round11-offline-install/installer.test.mjs
```

The tests exercise exact success/readback, duplicate and drift refusal, STOP/lease/pending-journal/retry/auto-setting/cost/release/counter/audit-tip holds, precommit backup and inverse setup failures, mid-write rollback, post-audit rollback, backup corruption and concurrent-write recovery. Passing them proves this local fixture's behavior only.
