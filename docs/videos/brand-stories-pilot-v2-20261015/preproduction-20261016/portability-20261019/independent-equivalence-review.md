# Independent packaging equivalence review — 2026-10-19

Reviewer: `codex-gpt6-a01` (root); correction authored by the separate
`a01_r45_handoff_review` agent. Verdict: **PASS for offline packaging equivalence**.
This review does not issue a new editorial, verifier, listener, production or
merge approval.

## Reviewed identity

- Baseline Git commit: `cd12083117f456935a94be45f7c9f5b020d253eb`.
- Correction receipt: [receipt.json](receipt.json), SHA-256
  `7a39964ad7558446ed7b617704f8fc373514da2d02e78e9bb320b0a4eaf83bb5`.
- The receipt's pending-review status records the author's handoff point.
  This separate report supplies the subsequent independent review without
  rewriting that receipt or creating a hash cycle.

## Independent checks

1. Read baseline blobs directly from Git, rather than relying on the author's
   backup. All 27 modified-file before/after SHA-256 pairs, all 76 unchanged
   original files, and all five saved historical manifests match the receipt.
   There were zero mismatches.
2. Independently compared the 67 protected content files with baseline Git
   blobs. Candidate narratives, scenes, prompts, claims, source maps, lexicons,
   composed video, all chapter files, semantic mappings and the owner's original
   direction receipt remain byte-identical.
3. Reviewed the locator redactions and build-pin changes. Historical review
   verdicts and reviewed identities remain historical. The portable package
   hashes bind the redacted copies. No check was weakened or whitelisted.
4. The r45 builder pins the preserved original owner-approved manifest and
   verifies equality of its complete output hash map with the portable r44
   output map before consuming the unchanged owner-direction receipt.
5. Reran r45 `build.mjs --check`: 51 scenes, 53 lines, zero errors and 40 warnings;
   current manifest `896615541683e620eb6e79468d8d304f146ad932700a7f044d5a1eb9784888f6`.
6. Reran canonical handoff `build.mjs --check`: six chapters, 51 scenes, 53 lines,
   55 PENDING claims (15 plan-linked, 40 passage-only), zero errors and 39 warnings;
   current manifest `73cf375736d13a899e261000d1ad694f876e4f1101e2e9454210c1063dd9e4e4`.

## Limits

Historical r44 retains its pre-existing validation warning-count drift on current
main; this correction does not claim that old checkout-specific check now passes.
The original rejected handoff remains superseded. Formal worker checks, fresh
consistent host evidence, actual TTS duration and final-media acceptance remain
outstanding. The changed PR head requires a new exact-version merge decision;
the original byte-identical-rebase authorization is not reused.
