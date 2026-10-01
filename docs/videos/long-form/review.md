# Long-form duration revision: independent review

Reviewer: review_longform. Author: codex-root and the implementation authors. Review date: 2026-10-02. Verdict: **PASS — DURATION_ONLY**. Required fixes remaining: **none** for the SHA-bound revision below.

The initial 21-file review and the integrated 70-file increment below independently inspected the implementation, planning records, original source bytes, duration guards and API/UI changes. It does not claim a fresh factual review of the underlying topics, completion of full long-video manuscripts, approval of rewritten manuscripts, human audio listening, image QA or verification of actual media. No real provider/model/media calls, production media generation, production writes, imports, activation, scheduling or publication were performed. Unit regressions use local synthetic and mocked fixtures.

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

## Initial 21-file independent review drift guard

A second independent increment inspected review.mjs, review.test.mjs, the CLI check call and the README review links. The initial receipt required an independent PASS with DURATION_ONLY scope, matched the then-current report hash, covered exactly all 21 implementation/plan/document/test paths, and agreed with both the report table and actual file hashes. check, plan and inputs enforce the guard before returning effective production inputs; build remains a neutral local rebuild. Missing files and malformed receipts fail closed through the CLI error path. No circular hash is introduced: the receipt hashes the report, while the report binds implementation, plans, documents and tests.

Before repository receipt installation, an independent outside-repository simulation exercised a valid 21-file receipt and six invalid revisions: self-review, missing author identity, a removed receipt binding, a removed report binding even after rehashing that report, a changed report and a later source-file hash. Each invalid revision was rejected. The 17 prior files outside this four-file increment retained their earlier independently reviewed SHA. No workspace files were modified by this reviewer. The new two shipped regression tests and the full CLI check require the author to install this genuine report and its receipt before a final execution.

## Initial local validation

Independently executed `node tools/video/long-form/cli.mjs check`: PASS for all 473 current plans. Independently executed `node --test tools/video/long-form/plans.test.mjs tools/video/core/duration.test.mjs tools/video/qa/duration.test.mjs`: **12 passed, 0 failed**, exit 0. These include actual QA command forwarding, precise frame boundaries, branded-body handling and malformed/stale evidence. A separate independent source audit recomputed record/file/package/Shorts hashes and compared preserved files with Git; it also checked chapter-content preservation and the exact description changes.

The three READMEs and KNOWLEDGE-STORIES entry state the revised production targets, preservation of historical fact-review packages, required effective inputs, pending manuscripts/media, and the distinction between a 600-second plan and a measured cut.

## Upstream character-look validation increment

After rebasing onto main commit eda3b60f, an independent increment reviewed the actual change from 8403523a to 4e8f633c in series.py and its upstream regression tests. The upstream addition validates optional character-look IDs, appearances, whole-number episode ranges, non-overlap and Gemini-only voice-style overrides when filing an ordinary setting book or story bible. An explainer bible still returns through its dedicated narrator-only validation before the character-look loop; brand stories still have no such documents. The new helper neither reads nor writes target_minutes. The complete patch_target_minutes, patch_problem and patch_series block is byte-identical to the prior independently reviewed version, so the default-10, whole-minute 8–20 bounds, bible style-crossing rule and legacy correction path remain unchanged. The other 20 reviewed file hashes are unchanged. Only series.py is rebound below after this actual increment review.

The genuine installed receipt passed an independent CLI check and all four targeted Node test files before this upstream increment: 14 passed, 0 failed. The refreshed receipt must be installed again and checked against the newly reviewed series.py bytes; the reviewer did not run or claim the API suite results reported by the author.

## Integrated peer and worker increment: 70 files

The reviewer read the complete 55-file change from peer commit 5851bd8b0fce16ff2efd0da055a8c099f329cfe0 against its common ancestor 874e70099444c7646ffaa0f55e1033aae61e5c12, then independently inspected the actual integrated workspace revisions and regression tests. The later peer increment 6523a44f0c89a82baaa844941d62afa4b7a61788 merges current main and adds only the same three-line short-fixture override to the landed dub freshness regression (plus its historical completed-ticket scope); the reviewer read that actual delta and the complete current test file. Its dub fingerprints, legacy clip-cache proof and changed-line-only re-take assertions remain verbatim. This increment includes the original 21 paths, the peer implementation/docs/tests excluding its completed-ticket historical record, the new integration regression and that freshness test. The final bindings below contain exactly 70 unique registry paths. It is a DURATION_ONLY review of planning data, runtime rules, inputs, fixtures, migration source and regressions; it is not a fresh topic fact check, manuscript approval, provider acceptance, actual video-duration measurement, browser acceptance, CI acceptance or production activation.

The integrated API/UI keeps the reviewed flat-explainer default of 10 and strict whole-minute 8–20 bounds. Ordinary drama keeps 1–8 and default 3. The peer's 8-default/12-maximum behavior and unconditional clamp on unrelated series edits were not retained. The existing bible crossing restriction and legacy pause/title behavior remain; the reviewed series.py and admin-video-series.tsx bytes are unchanged from the previous accepted revision. The peer API/UI duration expectations were reconciled with 10/8–20 and all five locale labels match 8–20; the later correction of one remaining stale test accessible-name literal is recorded below. General slides settings and their model constraint now require 8–30 with min <= max.

The new effectiveEpisodeMinutes helper is shared by every explainer planner/writer route. Missing or old integer targets below 8 become 10, while explicit 8–20 values remain. Invalid over-20, noninteger, string, Boolean and nonfinite explainer inputs raise before a paid model request. New requests, draft episodes, existing script writes, lint/script repair and replanning normalize and persist the state. Ordinary drama targets and the brand-story 13-minute target pass through unchanged. This repairs the peer's omission of existing auto.json, replan and writer payloads without rewriting approved manuscripts or claiming their new duration has been measured.

Both QA rules coexist: general non-drama cuts have an eight-minute final-cut floor, and the five knowledge/nonfiction catalogs independently require the current unwrapped body and final cut to reach 14,400 frames at 30 fps with matching speech/timeline/bookend evidence. General checked frames must be positive safe integers; a supplied FPS must be 30. The immutable knowledge/body guard runs first and never reads the fixture variable, so even minMinutes=0 cannot accept a 14,399-frame explainer or brand body padded to 15,000 final frames. Ordinary dramas, compilations and the separate Shorts QA route retain their existing duration rules. The brand-story producer emits category=story, so the peer's broader generic classifier does not exempt it from the catalog body rule.

The reviewer found that a first integration used NODE_TEST_CONTEXT alone to authorize short fixtures: an ordinary CLI inheriting child-v8 plus VIDEO_MIN_EPISODE_MINUTES=0 could then return a zero general floor. The author fixed this boundary. A fixture now requires exactly child-v8 and an entrypoint inside repository tools ending in .test.mjs, or the exact repository assemble/smoke.mjs entrypoint. Independent child-process regressions show that missing, child-v8 and arbitrary markers still yield floor=8 and reject 14,399 frames for an ordinary process; the real CLI path also cannot opt out. The reviewer additionally identified general final proof accepting string/fractional frames or non-30 FPS; the author added strict checks and corresponding regressions. These issues are resolved in the SHA-bound files below. The retained 20 test-only env assignments (including the later freshness test) and one smoke assignment now only relax fixture estimates/general final checks, never the fixed catalog body proof.

Migration 0117_video_min_8_minutes connects to the actual current chain's 0116_video_project_category. It raises both legacy settings bounds together using GREATEST(8), recreates the same named 8–30/min<=max check, and is idempotent; downgrade widens the check to 3 and deliberately preserves raised values. The reviewed PostgreSQL regression restores the old check and 3/5 data inside a rollback transaction and exercises both directions. Independently executed alembic heads returned exactly 0117_video_min_8_minutes (head), exit 0. This reviewer did not execute that PostgreSQL integration exercise. Pending PR #1097 independently proposes 0117_video_shorts_topics off the same 0116: it is not part of this workspace or receipt. Whichever PR lands second must rebase and renumber/reconnect to the actual landed head, followed by fresh migration review; blindly including both siblings would create two heads. No migration was applied to production.

The unchanged plans.json SHA remains 22023c15fa10a24e4a0141e3fc5930ff6925a84ff5ab5cb5a466a5baa15b7108. The reviewer reran the independent source audit after integration: all 473 record/package/source hashes, 307 preserved baseline files, 92 continuous 600-second chapter budgets, 184 original Shorts hashes and 460 allowed locale metadata revisions passed. No effective old 480-second six-chapter instruction remained; the eight duplicate rejections and covered ai-agent status remain intact. Brand targets remain 780 with 720–900; AI targets remain 600 with 540–660.

The registry now demands the exact 70-file binding set in both receipt and genuine report, in addition to independent author/reviewer identities and the report hash. check, plan and inputs still enforce it; build still only rebuilds the local manifest. An independent outside-repository pure-function simulation of this actual 70-file registry accepts a matching receipt and rejects self-review, missing identity, missing receipt binding, missing report binding even after report rehash, changed report and changed file SHA. The current repository receipt must be mechanically installed from this genuine report before the shipped receipt tests and CLI can pass. The reviewer wrote only outside-repository review artifacts and did not edit implementation files, stage, fetch, push, import or publish.

Independent executions before the final four-file gate/proof correction: the seven selected plans, body, QA, integration, lint, checks and automation test files passed 115/115, exit 0, including real mocked planner/writer/state-repair payload paths. After the final correction, the five affected core-duration/lint/integration/QA-checks/actual-QA test files passed 50/50, exit 0. A second independent read-only reviewer reran core-duration/integration/QA-checks/actual-QA tests after correction: 25/25, exit 0. The reviewer additionally executed the final freshness regression: 4/4, exit 0. The final two shipped receipt regression tests and CLI check are intentionally left for execution after the author installs this genuine 70-file report and receipt. API/UI and PostgreSQL suite outcomes reported by the author are not relabeled here as independently executed results.

The current READMEs, five locale labels and both byte-identical youtube-video SKILL.md copies explain the 10-minute target, 13-minute brands, general eight-minute final minimum, fixed catalog body minimum and the narrow fixture exceptions. They distinguish planned length from measured media and preserve the need to re-check revised manuscripts and actual audio/video. Required fixes remaining: none for these bound bytes.

## Admin reviews accessible-label regression increment

The full web suite exposed a remaining stale accessible-name literal at admin-video-reviews.test.tsx line 270 in the previous 70-file revision. The earlier integration source review missed this test literal. The author's deterministic reproduction log identifies expected “長度（分鐘：漫劇 1–8，解說 8–12）” and the actual rendered “長度（分鐘：漫劇 1–8，解說 8–20）”. The author corrected exactly that one test literal. This reviewer independently read the failure log and source delta, then reconstructed the previous file bytes by replacing the single 8–20 label back with 8–12: its SHA exactly equals the prior bound 9b5a45fbebd41941d264d817caa8bdeba47249a944de8cc32d3808999b7cff7b. The corrected file's SHA is 98a983a571dcc8ca9e1d5da5cc0bcac3f7d96c6bcd8ed0805c7ca9f55ff5f08d. Every other 69 accepted file hashes matches the previous independent table byte-for-byte.

The reviewer independently executed the complete corrected admin-video-reviews.test.tsx file through Vitest: 30 passed, zero failed, exit 0. The corrected accessible name agrees with the five-locale UI and strict API 8–20 explainer range; its scenario still submits an ordinary ink-wash drama at 2 minutes. Runtime input defaults, worker rules, measured-body/final QA, plans and all existing media evidence are unchanged. This increment revises only the genuine outside report and the one test binding; the author must reinstall the report/receipt and rerun the shipped review checks. The 70-file registry remains unchanged. Verdict remains PASS — DURATION_ONLY after this actual increment; required fixes remaining: none for the bound bytes.

## Reviewed SHA256 bindings

Any change to these bytes requires review of the affected revision before reusing this verdict. The earlier 21-file history above remains evidence of its own revision; this 70-file table is the current acceptance binding.

| File | SHA256 |
| --- | --- |
| `.agents/skills/youtube-video/SKILL.md` | `162ef6dc4ef7d4248afd8a9102575b725f5acf234a2127cee30b791b323db2ae` |
| `.agents/skills/youtube-video/references/automated.md` | `07c4bf0c63109e8f5eff1e8fa999659faf39e6d43f18f7a3d18b74010782f92f` |
| `.agents/skills/youtube-video/references/formats.md` | `17857aae0d529984f25a3360f69a60b4cc51bd715343eeecd051e6686f475875` |
| `.claude/skills/youtube-video/SKILL.md` | `162ef6dc4ef7d4248afd8a9102575b725f5acf234a2127cee30b791b323db2ae` |
| `apps/api/app/video_automation/models.py` | `58013e5f73d53f1968fd417ffddf6349c2223b7d1639070db8bb95a36cf166c2` |
| `apps/api/app/video_automation/schemas.py` | `6db7ffc536a05c990602255f4e7b4771fdb0f3d4c259990be4edc554c1d5144a` |
| `apps/api/app/video_automation/series.py` | `2b5d747a1cc4fd285c8722f41f91840af615711065727ae398e5ae84314815d8` |
| `apps/api/migrations/versions/0117_video_min_8_minutes.py` | `e1d7cf7166994ff700290c285a22e3708a150dde4c47c1bec78ed6a7fa078089` |
| `apps/api/tests/test_migration_0117_video_min_8_minutes.py` | `6ecd7ac554f79357f1cd92e5758eb7708660905912dd50caba18762b99aa71c3` |
| `apps/api/tests/test_video_automation_settings.py` | `b7f8a1853a7090d010a648ddb7c262c3c616256b4d6a8913410efab8d40a3707` |
| `apps/api/tests/test_video_drama_requests.py` | `07ddbcaadf668a13565969ca44e2542dee4f6ad83791bcc8f67d785302734c59` |
| `apps/api/tests/test_video_explainer_duration.py` | `fbd8aaca7171321dcbe7511f607f61bb21a147640f9e22920db87d2f872ab2fc` |
| `apps/api/tests/test_video_series.py` | `9c762fbef8eec2f9be92de461ca5434ca658e75cc20a22cbccf661b702d531b6` |
| `apps/web/components/admin-video-explainer-duration.test.tsx` | `bb888f17b3ef617d788fbed83f5fba280dfe06da008a6f80fca15b15c6916ca0` |
| `apps/web/components/admin-video-reviews.test.tsx` | `98a983a571dcc8ca9e1d5da5cc0bcac3f7d96c6bcd8ed0805c7ca9f55ff5f08d` |
| `apps/web/components/admin-video-series.test.tsx` | `f6b62a1802799e56cd8d64e003a2035b3b2e255a214e41335329ae25069eec8c` |
| `apps/web/components/admin-video-series.tsx` | `97980f007e7091dab343603c0bb1ada909decab950a5535c9ef50ee8fadba7a1` |
| `apps/web/components/admin-video-settings-tutorial.tsx` | `7aad8e5d88b67ebaf0b261a57482fb06044111e86af9cfa43157627c7e671957` |
| `apps/web/messages/en/admin.json` | `1999afbe94f289230b8491c884ea42e2508c65a79bc9e37e1d2ea07574478fa7` |
| `apps/web/messages/ja/admin.json` | `71b13a0819eb38d4917186edd56a94d58f249e7d105ef61b1832654d7e6b23db` |
| `apps/web/messages/ko/admin.json` | `d1960406d5839e61c178b08128f9080ac97a5a7d6ff6d67cc15c7747deda224a` |
| `apps/web/messages/zh-CN/admin.json` | `be21c3de63820628fc1d3b1f98b3d7904d9b6ade5c7722f01789011dcde05f00` |
| `apps/web/messages/zh-TW/admin.json` | `4cdb1979b25bebcc1a508b0aa0081b400e024cc6eb1f60a7f5bf07d2c607be70` |
| `docs/videos/DESIGN.md` | `299449c6c19a40a0e17868615a7d8442771449e0db6e63186ca9c57a0d57ab41` |
| `docs/videos/KNOWLEDGE-STORIES.md` | `ac08a33baedd84f282901594e55758f4b390ee1a8dc798e2c25c4b463081aa80` |
| `docs/videos/README.md` | `88a8fcb1e6019d279b790f089feb14abe5dc21d2b1c0624f4d0fe25c73346868` |
| `docs/videos/long-form/README.md` | `dd639c0c85595881d1bda64541d28f29e8d90f1067e541c08eb28dc9c4543c3b` |
| `docs/videos/long-form/plans.json` | `22023c15fa10a24e4a0141e3fc5930ff6925a84ff5ab5cb5a466a5baa15b7108` |
| `docs/videos/long-form/policy.json` | `6f08e7cd27b98710dc308bdb7ea44a6db4b1c8891d0731d5387d9b2245636bad` |
| `docs/videos/so-thats-why/README.md` | `00a0f0e5a56d7a492dec69263eab34668e0d334949878bd512b09edacaefd0de` |
| `docs/videos/so-thats-why/season2/README.md` | `e560411dc91f1928b2cf9506a044e55ae7f5f65450199118bd165464599f1218` |
| `tools/video/assemble/smoke.mjs` | `2d16bc9b09e7dd1efe97b0938fc5fcbdb78c322c000dbb9152e293d834dc046e` |
| `tools/video/automation/automation.test.mjs` | `762edc17b105e3986c950894d2e06d4e09dd44f065ba91288a55aba6b104eae8` |
| `tools/video/automation/flow.mjs` | `8204b2d10ca6350952e90f8cc7420a7814f709310e2b283b16aa6a337213c330` |
| `tools/video/automation/prompts.mjs` | `dd8a8530a0c44073e915c2092d27442bb5b6949019c5d0e7fd7d7b3321ab93d9` |
| `tools/video/automation/series.test.mjs` | `85aaf1f5dabc78058603ad3c1167d950d353731f02a160a5d17be82597e09925` |
| `tools/video/cli.test.mjs` | `e813be708f513a358f4eec561d5056377174a56c2a367a1ee97ad78b95de8379` |
| `tools/video/core/drama.mjs` | `08c881a09b0043eb6844c875c7d498dc9a5b99e0f569c36d76fb41081bee9b8e` |
| `tools/video/core/duration.mjs` | `406c61d2211781ae571f952cb6239ee7c808f7f603a4be3ed5d61622bfe65d9a` |
| `tools/video/core/duration.test.mjs` | `49290be2b3f58801532e225ecff8f8b9730746425e6527b50b0c03beee6adc94` |
| `tools/video/core/explainer.test.mjs` | `1b1d3a2add5373e8a91941150d4cf16abc501fb0724540005edb2abff247154e` |
| `tools/video/core/lint.mjs` | `a10cfdbd4361e62fbc264b6d312f466c9a3d0ae6d97baa3f4dc6288ca0d1ac12` |
| `tools/video/core/lint.test.mjs` | `61ee2e6d74564753c54312fd10d8151643dbb4c458f17e15e3679aef4df6d56a` |
| `tools/video/core/narration-locale.test.mjs` | `af0b899f0518ef0f652816a8d53908d002cb805514993ca24d6aca0004640595` |
| `tools/video/core/schema.mjs` | `d072cccea0eb2156d462225edf61cec6d732cb79d1b4d8e9caf2571bc830622e` |
| `tools/video/core/stages.test.mjs` | `0a409f7a88234c1823146ea65092a95ceb12b69c34ccf1910894712f34859a2e` |
| `tools/video/core/state.test.mjs` | `23e89658d92b99d0e7dbb64e8ad00f82016795deb38ef732ec9e76013d867522` |
| `tools/video/dubs/captions-package.test.mjs` | `7eb0a10630b447dd17ffeafe3d99059c0fe3f392d58838dffd10a59373734f28` |
| `tools/video/dubs/dubs.test.mjs` | `143f7bfa09d2a161c275186464ea2f27c55f37a1e9dc9d5e90dfab7ed69f373b` |
| `tools/video/dubs/freshness.test.mjs` | `c882af3d55bff72c410e930b0e0f187770782a937952bb9efba3ab40e44a5b30` |
| `tools/video/dubs/plan.test.mjs` | `94e61419eda766e722c07675f1f75a569f3eb07fdeecce5c03dc862db1a0d572` |
| `tools/video/long-form/cli.mjs` | `3a0b26f900daaf1a08f7ed210ad1239d7f172035fa1e14c6dafc28bf55dedfa4` |
| `tools/video/long-form/integration.test.mjs` | `aa69f38653fb7c6a7fd0c6daed93ccde1e031987e3169f6c8d9456f38c8b605c` |
| `tools/video/long-form/plans.mjs` | `9680960509931642c679a9db9a3a1d6e419280558f9eb431358bfd1ee781e103` |
| `tools/video/long-form/plans.test.mjs` | `5b7992649fa5384d1758664a2e9b6ccbb104004da499a3d5f73b6665e9f768a6` |
| `tools/video/long-form/review.mjs` | `9ccf5b14a178dbf80ee699b0b6ddfa6abeda240844845f005042806a2240ce27` |
| `tools/video/long-form/review.test.mjs` | `e753ccc616b589a321473336f71621cd46206edbc0fa4f2b1e59d2167217e06f` |
| `tools/video/media/clips.test.mjs` | `a7679d5b7a7224d5417201cc21bdb093f500cdc8aeeb1af043640200e13cf0ff` |
| `tools/video/media/look-keyframes.test.mjs` | `43311eb4248ea1504e853193f242455beaabb05c224abc6f51f5c6949619187b` |
| `tools/video/qa/checks.mjs` | `dc99682b29b674cfedc12ca67c8809e23c1d99d5635a1cd79970a8180d21cc83` |
| `tools/video/qa/checks.test.mjs` | `e93fe80fb6ef0366da6728e397f78e355e6000847836a0a7e31ae63615211317` |
| `tools/video/qa/cli.mjs` | `49d3b6813773cff589872d3952945879e6814b567806c0c0448c044277128b4e` |
| `tools/video/qa/duration.test.mjs` | `056e8f564c9952b025ea7736b43e41bfc47fcc75a847f840878a093ea61fc681` |
| `tools/video/qa/qa.test.mjs` | `6bab373f43da2cbc9ff469c771ea561e9075964b9e387340167ff42d8cd10aa5` |
| `tools/video/review/sync.test.mjs` | `ea897ad959288ec195f6a909172041174b1023d9dca0e78adf6ad34d4d9d8974` |
| `tools/video/screencast/screencast.test.mjs` | `9bbe23f554a93ee394ec4d0aed18fc030d61b284a42b68487f9c89b0e1ad7e6a` |
| `tools/video/templates/terminal/terminal.test.mjs` | `fc8c9ca5a76f336b545194a7a009630fe0d227544aa4e9b363c0d655fce4e38d` |
| `tools/video/tts/batch-recovery.test.mjs` | `7594fb398ddf15acec164492bf572ff370de48e656db69a420e5c711c18125dd` |
| `tools/video/tts/check.test.mjs` | `ad385d7df22fd297588dfef8a72b0b3f6261d0fb4619e4c538a30ef8464b1477` |
| `tools/video/tts/tts.test.mjs` | `cb2cc2508c4b394b43db21201a1efe44676a21a186621a18f5c0c2b5a9d983b3` |
