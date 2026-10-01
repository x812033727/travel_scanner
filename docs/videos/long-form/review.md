# Long-form duration revision: independent review

Reviewer: review_longform. Author: codex-root and the implementation authors. Review date: 2026-10-02. Verdict: **PASS — DURATION_ONLY**. Required fixes remaining: **none** for the SHA-bound revision below.

This review independently inspected the implementation, planning records, original source bytes, duration guards and API/UI changes. It does not claim a fresh factual review of the underlying topics, completion of full long-video manuscripts, approval of rewritten manuscripts, human audio listening, image QA or verification of actual media. No network calls, media generation, production writes, imports, activation, scheduling or publication were performed.

## Findings and fixes

1. The initial effective backend notes still instructed 480-second six-chapter outlines despite target_minutes=10. The author corrected only explicit outline-duration statements and preserved minimum-480-second requirements, factual numbers and source URLs. Independent reinspection found no operative old 480-second outline instructions in the effective requests. Historical packages and receipts remain unchanged.
2. T28 and T33 initially retained the original eight-minute chapter time ranges in their effective headings. The author removed those stale heading suffixes and rebuilt the manifest. All 92 effective chapter sets now have continuous budgets totaling 600 seconds and no old MM:SS heading ranges. T33's factual UTC and time-offset examples remain unchanged in the chapter content.

## Independent planning and source audit

- 473 unique catalog/ID records: first season 100, second season 92, third season 100, brand stories 100 and AI terms 81. Every current source_record_sha256 was recomputed from its source record; all source-file and package SHA256 values matched the current bytes.
- 307 historical planning-source files were compared byte-for-byte against Git commit `282a7b1160b3a561d8fe89596ff1a0f595c30d65`. All are preserved. The added policy is separately bound below.
- First- and second-season effective requests use flat-explainer and target_minutes=10, stay within the 4000-character premise and 2000-character note limits, and preserve the original premises.
- All 92 second-season proposed chapter budgets sum to 600 seconds. Their chapter content remains present verbatim in the original Markdown after whitespace normalization. Only budget allocations and stale heading timestamps change.
- All 184 second-season Shorts are hash-identical to their original bundles. The 460 effective long-video locale titles are unchanged; long descriptions differ only in the explicit outline-duration digits 480 to 600. Shorts packaging remains in the preserved source bundles.
- The eight duplicate rejections B30/B32/B33/B38/T39/A26/A27/A30 remain absent from the effective adopted catalog. AI term ai-agent remains COVERED_DO_NOT_REMAKE; production lookup rejects it.
- Brand stories retain 780-second targets and the 720–900-second range. AI terms retain a 600-second target and the 540–660-second range. Third-season items remain checked candidates requiring outlines; they do not acquire fabricated one-off inputs or media acceptance.

## Runtime and input review

The QA assemble item now checks the current unwrapped TTS timeline, checked final-frame count and their speech hash. It requires at least 14,400 frames at 30 fps for both body and final cut. One frame below the minimum fails; intro/outro frames cannot make a short body pass. Brand selections must match the body and presentation timeline. Missing or stale proof cannot use target_minutes or an earlier passing checks.json as measured acceptance. Ordinary drama, compilations and Shorts keep their existing rules.

Catalog slugs, the flat-explainer look and explicit knowledge/story categories cover the requested producers. The story worker explicitly emits format=drama and category=story. A missing format or unknown category is already a lint error before QA, so it cannot use classifier fallback as a legal bypass. The final-review push runs QA again for the current final cut.

API and UI source review confirms flat-explainer requests default to 10 minutes and accept only whole minutes in the 8–20 range. Ordinary drama retains the 1–8 range and default 3. Style-only patches preserve the rule about an existing bible, choose the appropriate format default and repair a legacy short explainer when its style is explicitly reselected; unrelated edits can still pause or rename it. This independent review did not execute a browser acceptance run or the API/UI suites.

## Independent review drift guard

A second independent increment inspected review.mjs, review.test.mjs, the CLI check call and the README review links. The receipt must declare an independent PASS with DURATION_ONLY scope, match the current report hash, cover exactly all 21 implementation/plan/document/test paths, and agree with both the report table and actual file hashes. check, plan and inputs enforce the guard before returning effective production inputs; build remains a neutral local rebuild. Missing files and malformed receipts fail closed through the CLI error path. No circular hash is introduced: the receipt hashes the report, while the report binds implementation, plans, documents and tests.

Before repository receipt installation, an independent outside-repository simulation exercised a valid 21-file receipt and six invalid revisions: self-review, missing author identity, a removed receipt binding, a removed report binding even after rehashing that report, a changed report and a later source-file hash. Each invalid revision was rejected. The 17 prior files outside this four-file increment retained their earlier independently reviewed SHA. No workspace files were modified by this reviewer. The new two shipped regression tests and the full CLI check require the author to install this genuine report and its receipt before a final execution.

## Local validation

Independently executed `node tools/video/long-form/cli.mjs check`: PASS for all 473 current plans. Independently executed `node --test tools/video/long-form/plans.test.mjs tools/video/core/duration.test.mjs tools/video/qa/duration.test.mjs`: **12 passed, 0 failed**, exit 0. These include actual QA command forwarding, precise frame boundaries, branded-body handling and malformed/stale evidence. A separate independent source audit recomputed record/file/package/Shorts hashes and compared preserved files with Git; it also checked chapter-content preservation and the exact description changes.

The three READMEs and KNOWLEDGE-STORIES entry state the revised production targets, preservation of historical fact-review packages, required effective inputs, pending manuscripts/media, and the distinction between a 600-second plan and a measured cut.

## Upstream character-look validation increment

After rebasing onto main commit eda3b60f, an independent increment reviewed the actual change from 8403523a to 4e8f633c in series.py and its upstream regression tests. The upstream addition validates optional character-look IDs, appearances, whole-number episode ranges, non-overlap and Gemini-only voice-style overrides when filing an ordinary setting book or story bible. An explainer bible still returns through its dedicated narrator-only validation before the character-look loop; brand stories still have no such documents. The new helper neither reads nor writes target_minutes. The complete patch_target_minutes, patch_problem and patch_series block is byte-identical to the prior independently reviewed version, so the default-10, whole-minute 8–20 bounds, bible style-crossing rule and legacy correction path remain unchanged. The other 20 reviewed file hashes are unchanged. Only series.py is rebound below after this actual increment review.

The genuine installed receipt passed an independent CLI check and all four targeted Node test files before this upstream increment: 14 passed, 0 failed. The refreshed receipt must be installed again and checked against the newly reviewed series.py bytes; the reviewer did not run or claim the API suite results reported by the author.

## Reviewed SHA256 bindings

Any change to these bytes requires review of the affected revision before reusing this verdict.

| File | SHA256 |
| --- | --- |
| `tools/video/long-form/plans.mjs` | `9680960509931642c679a9db9a3a1d6e419280558f9eb431358bfd1ee781e103` |
| `tools/video/long-form/cli.mjs` | `3a0b26f900daaf1a08f7ed210ad1239d7f172035fa1e14c6dafc28bf55dedfa4` |
| `tools/video/long-form/review.mjs` | `37c0367a1b1dfa52dc6f375b18975071088c24acaaaee2e96efd359b6b601dca` |
| `docs/videos/long-form/policy.json` | `6f08e7cd27b98710dc308bdb7ea44a6db4b1c8891d0731d5387d9b2245636bad` |
| `docs/videos/long-form/plans.json` | `22023c15fa10a24e4a0141e3fc5930ff6925a84ff5ab5cb5a466a5baa15b7108` |
| `tools/video/core/duration.mjs` | `3b4f82bce6f9188b6565a532d8d3be98f7187a779dbb8d692b4dfebf4cdfa232` |
| `tools/video/qa/checks.mjs` | `fed542d7915d2aa84fd0290f7016787dac177195b9a5b999d872365534f28a50` |
| `tools/video/qa/cli.mjs` | `f2c753158a584a82757f25a60023c37d2449ce72852d9c3b554f8eeafd3b509b` |
| `apps/api/app/video_automation/schemas.py` | `d175d2815a205598fa8baf88c914c67d33d36dfbd0a93003db4429b0e569fdfb` |
| `apps/api/app/video_automation/series.py` | `2b5d747a1cc4fd285c8722f41f91840af615711065727ae398e5ae84314815d8` |
| `apps/web/components/admin-video-series.tsx` | `97980f007e7091dab343603c0bb1ada909decab950a5535c9ef50ee8fadba7a1` |
| `docs/videos/long-form/README.md` | `323a0a35ee8a52cc41f7b3925524ceed8a3b54fa3a5fc4f4b0e1344a45e1472f` |
| `docs/videos/so-thats-why/README.md` | `19e157f16f9c4007bce509590c443641f24ea637b257e54993ae03aaa1a332c8` |
| `docs/videos/so-thats-why/season2/README.md` | `e560411dc91f1928b2cf9506a044e55ae7f5f65450199118bd165464599f1218` |
| `docs/videos/KNOWLEDGE-STORIES.md` | `ac08a33baedd84f282901594e55758f4b390ee1a8dc798e2c25c4b463081aa80` |
| `tools/video/long-form/plans.test.mjs` | `5b7992649fa5384d1758664a2e9b6ccbb104004da499a3d5f73b6665e9f768a6` |
| `tools/video/long-form/review.test.mjs` | `e753ccc616b589a321473336f71621cd46206edbc0fa4f2b1e59d2167217e06f` |
| `tools/video/core/duration.test.mjs` | `c10da1b7d453c057bb8e0355e65e05df0b76b8677f280d1af6c943b4f915bde4` |
| `tools/video/qa/duration.test.mjs` | `d9f17a00903531bf378a86fa5491319fc5406616f9a1eedb66969e775691db90` |
| `apps/api/tests/test_video_explainer_duration.py` | `fbd8aaca7171321dcbe7511f607f61bb21a147640f9e22920db87d2f872ab2fc` |
| `apps/web/components/admin-video-explainer-duration.test.tsx` | `bb888f17b3ef617d788fbed83f5fba280dfe06da008a6f80fca15b15c6916ca0` |
