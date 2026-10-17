# Independent offline review — A01 historical pronunciation pin

Reviewer: `codex-independent-a01-lexicon-1017`. Date: 2026-10-17 (Asia/Taipei).

Verdict: **PASS for the offline planner and synthetic transition readback only. 0 P1 / 0 P2 findings within that scope. Production remains HOLD.** This Markdown report is not the independent-review JSON accepted by `preparePinnedEvent`, an owner receipt, a release approval or proof of an installed transition.

## Reviewed bytes and behavior

Read `transition.mjs`, `snapshot-format.mjs`, `synthetic-fixture.mjs`, `transition.test.mjs`, the parent rebaseline validator and the candidate README. Reviewed file SHA-256 values:

| File | SHA-256 |
| --- | --- |
| transition.mjs | a2944f89e60f18a58d1c2b7b84dfa0cd75bfda2174b349d04cd654f65081929a |
| snapshot-format.mjs | a666d5e74b3ce450fc8d8bc52c97626c1a7eb3cd30b31ef0867442a6a6ed2b95 |
| synthetic-fixture.mjs | f401f0265c80a7294eeb9f6fa7de1ed0b942f8fc00813f3d1575eacdcddd0766 |
| transition.test.mjs | 034173c1e716fa10b91998ee9f4429e1532235d537b8916b820d22e453895eff |

The planner preserves the historical dictionary bytes as an immutable version. It adds only `story.lexicon_sha256` and `story.lexicon_head_event_sha256` to the parsed auto state, retaining chapter and retry state. Its resulting source tuple differs from every historical edge endpoint, preventing a new self-edge or connection back into the prior source graph. The verifier checks all old evidence hashes and the complete evidence file set, exactly one added audit/revision entry, exactly three snapshot files, unchanged shared lexicon, strict pinned reader output and the complete resulting source tuple. The module plans bytes and performs readback; it provides no host installer.

Evidence fields are structurally and cryptographically bound to the plan and the supplied evidence bytes. Reviewer/operator names and `owner_approval_ref` remain untrusted caller-supplied data. They cannot authenticate an independent person or establish owner authorization. Synthetic receipts deliberately exercise only data binding.

## Independently executed verification

Using bundled Node 24.19, ran `node --test transition.test.mjs`: **4 passed, 0 failed**. Cases cover intact 80-to-81 pin and original counters; mutation/addition of old evidence; incomplete snapshot publication, extra optional approval and shared drift; reused reviewer/operator identity and old state mutation. The test named “a changed review” does not separately mutate review bytes; review bytes and receipt hash binding were inspected in code, so this report does not claim a separate tampered-review fixture.

Also independently invoked `planPinnedTransition` against the existing read-only local capture `C:/Users/x8120/.codex/captures/A01-20261017-095816-2a72b1e1/snapshot-80`, with historical bytes from `A01-round10-candidate/evidence/round9-lexicon.json`. Results:

- Plan SHA-256: `f269a6337f6a7900a02b6a8b0860b055b4e19c203ecab85675026dd17455a41f`, matching the recorded summary.
- 80 historical events and 185 historical evidence files validated.
- Pinned lexicon: `ebfa590a69b4328ed9bc0141832bb73d27cba51963fca78778258d404c3bc4c9`.
- Observed shared lexicon: `e6403c824aac13b4c0a1ae737e8a597a8bf60c353e9faf0cc4915c3214114a30`.
- Before source: `cf39296d597d36db3cafedc1c2ca5ae730dd104a34b1d1868fb5b83fc089c56b`.
- Proposed after source: `766a83c237af95b14d7c23bde133c8362e6a2f140bd959b0c056719d53eb3502`.
- Returned `production_status: HOLD`, `installation_allowed: false`, `paid_work_allowed: false`.

## Release limitations

The actual-capture invocation only computed a plan. No genuine 81st event or production evidence JSON was prepared or installed. Tests wrote synthetic temporary fixtures only. This review performed no host, model, paid, merge or deployment action.

Before production adoption, independently review and implement the guarded publication protocol across docs/work volumes, pending intents and recovery; update the source inspector to resolve pinned lexicon bytes; use a fresh matching host capture; resolve the existing uncertain legacy job; and obtain the required action-specific authority. Standalone snapshot reading alone does not make partial cross-volume publication safe. This offline verifier rejecting a partial fixture is not a production transaction guarantee. A revised 81-to-82 narrative transition must bind the pinned source, and factual/listening/narrative/media gates still apply. This report does not approve a script or establish that any film is complete.
