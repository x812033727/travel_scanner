# Independent X10 manual lexicon adoption review

**Verdict: PASS for the accessible local no-known-prior-speech check and the patched X10-only adoption gate.** I found no X10 speech, worker state, or lexicon transaction artifacts in the accessible `/workspace` and `/tmp` evidence. The planned media workbase is `/workspace/.brand-video-workdir`; its X10 project directory is absent. This review cannot inspect an inaccessible external host or establish whether unrecorded speech was synthesized there. The receipt's `confirmed_no_prior_speech: true` records this scoped independent finding.

Reviewer: Codex X10 independent post-fix reviewer. Reviewed at `2026-10-20T20:01:43.540Z` against commit `b7f0b48b416c911e91628a26d29f9f445a2ba4c4` plus the symlink fix and test described below. The filled fields are in [manual-lexicon-adoption-review.json](manual-lexicon-adoption-review.json), byte-identical to `/tmp/x10-manual-lexicon-review.json`. Both have SHA-256 `d4e9f40c4979f403afbde6737fd1f31a70c4c1ab458d0bfd951cc84d1fc22898`. I created the receipt from a fresh real X10 `story-lexicon-adopt --json` template, then set only `confirmed_no_prior_speech`, `independent`, `reviewer`, and `reviewed_at`.

## Local provenance and workbase

`/workspace/.brand-video-workdir` is a real directory whose `realpath` is the same path. Its top level contains other story workspaces, including X01, X02, X03, X04, X05, X06, X08, and X09, but no `story-everyday-ebay-paypal-x10` directory or symlink. The base has no `STOP`. The X10 repository story directory has no `story-lexicon` directory or `pending.json`; the planned X10 media path has no `auto.json`, chapters, intents, receipts, timeline, audio directory, narration, approvals, or other work files because that path is absent. All real checks in this review passed `--workdir /workspace/.brand-video-workdir` explicitly.

I searched accessible `/workspace` and `/tmp` names for X10/eBay/PayPal and searched local JSON, Markdown, and logs for the full X10 slug. I also searched media/state artifact paths for X10 narration, timeline, worker state, pending intent, and lexicon transactions. The matches were story source documents, reviews, task and tool text, source research, PR material, and the review receipt; no X10 media or speech state was found. This is an evidence-based local confirmation, subject to any inaccessible or unrecorded external work and to later filesystem changes.

## Exact bytes and proposed snapshot

| Input or output | SHA-256 |
| --- | --- |
| X10 `video.json` | `f5c7ec99142c4508d06ef58c8e5e0c136bd7e556a4254dba940d4328f804757c` |
| X10 `series.json` | `185699cef1019f2ef5db15d57575c12405f00f1e2211aced17def0245deab75e` |
| Shared `docs/videos/lexicon.json` | `95abdb67972cac70fe7c16b51faf4d94fe671e55aba9a1c3114fddb5a6cc613a` |
| Proposed X10 lexicon version | `98e669afe61ea000fd85f7d1a329e63c11dc5a073d04ef9f290a5b45147ece7e` |
| Proposed genesis event | `7164d4e7624f6dd9ecaf9d1f2a9ff0354db286a74942971669d918c87de1d505` |

I computed the first three hashes directly from file bytes and matched them to the real CLI template. The parsed series is a story naming `eBay` and `PayPal`, and `video.json` names the exact X10 slug. The shared dictionary lacks both names; the planned snapshot seeds them as `null`. The review receipt binds all four source/version hashes and the absolute workbase.

## Gate verification

`story-lexicon-adopt` is wired only through the explicit CLI command. The implementation restricts admission to X10, requires the manual story documents, and checks pending transactions, STOP, worker chapters or `auto.json`, audit, timeline, audio, approvals, and other work artifacts. The template starts with both confirmation fields false. A filled review must match the current template's exact hashes and workbase. The write path repeats admission under the project and shared dictionary leases, records intents on both volumes, publishes immutable version/event/review/adoption files, reads the chain and source hashes back, then writes a committed receipt before clearing intents. The independent flag and no-prior-speech field are attestations; the code cannot authenticate human independence or inspect a different media host.

The patch changes `workbaseProof` to inspect the story workdir with `lstatSync(..., { throwIfNoEntry: false })`. I independently built a disposable fixture with a real media base and an X10 workdir symlink pointing to a missing target. The actual `story-lexicon-adopt --json` CLI exited 1 with status `refused`; `explicit_real_workbase` failed with `STORY_LEXICON_ADOPTION_WORKBASE_UNPROVEN`, and the symlink remained untouched. The new focused regression test passed, and the complete `node --test tools/video/core/lexicon-adoption.test.mjs` suite passed 19/19.

The real X10 `--json` dry run exited 0 with status `needs_review`, 11/11 admission checks passing, `allowed: false`, and `apply: false`. It supplied the template and proposed hashes above without creating an X10 workdir or changing the three input hashes. After I wrote the receipt, the read-only `--review /tmp/x10-manual-lexicon-review.json --json` command exited 0 with status `allowed`, 12/12 checks passing, `allowed: true`, and `apply: false`; its four bound hashes and proposed event hash matched the table above. The command limits admission to X10, checks for existing speech/worker/transaction artifacts, requires an exact-byte independent review, and rechecks under its leases before publishing. A review receipt is an attestation; the tool cannot independently discover speech on another host or authenticate the reviewer's identity.

No real X10 pin, TTS, push, PR, or paid call was made in this review. Before any apply, rerun the read-only `--review` check against the same workbase. Any changed source bytes, workbase, or newly discovered speech requires a new independent review.
