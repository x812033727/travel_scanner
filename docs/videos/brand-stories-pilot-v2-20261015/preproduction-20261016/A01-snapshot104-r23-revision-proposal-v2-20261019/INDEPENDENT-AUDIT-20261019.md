# A01 r23 v2 independent offline audit — 2026-10-19

Reviewer: codex-gpt6-a01-1510-integration-audit
Review instant: 2026-10-18 17:46 UTC (2026-10-19 01:46 Asia/Taipei)
Verdict: PASS for the exact offline replay and ID/source mapping; PRODUCTION HOLD. No new P0/P1 was found in this bounded offline proposal. This is not a formal six-chapter script review, host installation review, or approval to spend.

## Bound inputs

| Input | SHA-256 |
| --- | --- |
| This v2 manifest.json | 66BADCE86165704FED0AAE53FFE650F8A948B977B5A07A261BF088B3E1FED0A0 |
| This v2 build.mjs | D44F7BD8A642C978FA77DF482FBB790EF4ABBA3B4CC1F33F80E6014B7B252BFE |
| This v2 fixture.mjs | B5F5DA1559FB1A61C86ED17879C80FE472768A152798132585E681A7FD88DCCC |
| This v2 fixture.test.mjs | 96B99269BF7DC3E3B57923D08B756AC6EAD6DE987FE2B2DF78B5A78E8AB4419D |
| r23 editorial manifest.json | A5978F8318C87E62F48D9E00330FCDC45FFAF50161601D99017922F4AF888CF4 |
| r23 limited fact review | 565D7B49CFFA1506185C5D55DB9543DE26BF42533A134F26F6D9149F5DA82E6F |
| r23 blind story review | EE12FE08E7DA2B2BD0CF1B1096B3BEE19E19925A15CEFABFFDB486E3DD4F2D44 |
| r12 bridge manifest.json | 17E44CDF2CDD8361D218B58B4574A7D52ACF4898BA9C86FD64B58A59336982DC |
| Current tracked 104-chain checker | 3D4FA7A891244A7E0C0CA620FB6A01D9E967B4FC3B4C6C8CEE3CF0E156B3415D |
| Private verified-review104.json | 29DDBE75E849F09FED508B3C1405FD533445AA8ADEE337539CB11EA9287460AA |
| Historical host capture-manifest.json | 0CDB7DE8877C3049A11D95695818E44A43CD216B6A90D68EBD0055463106F6D2 |
| Historical host tar | 13FEDB2BCDB44BD2DD1BF484EA5557C2D217A0DDF71E6C1B57E33B2BA46912ED |
| Local #1563 story.mjs used for replay | DB7AFDDC854F6F106FB7198D8F2634AD15F9E6EB5FE8C295EFC604413C8ED179 |
| This v2 mapping.json | 8A6EFA278B1DBBFBCE9B89F9E6374BD678FDDAD5F2CEE3C63D031CB0ECE10373 |
| This v2 gates.json | 922D0579F4C327A3DF2BD6AB99ACCFC8D50B25AF7D08C50238320E4D5EBE3F78 |
| This v2 event-proposal.json | 6F62DAA5F13272EB53D403A1CFEF950F8B45B0B3326496F8E069B7E0A911D208 |

The private capture and its raw host output remain outside Git. This receipt contains hashes and counts, no private paths, host credentials, or raw manuscript extracted from the host.

## Independent checks

1. The historical readback manifest is byte- and hash-matched; all seven listed files have their declared byte length and SHA-256. The tar SHA-256 matches the manifest. All 254 regular tar files match the separate temporary extraction byte for byte; the tar has no special members, absolute paths, or parent traversal.
2. Independently traversed 104 unique source edges from the sole root to the tip. Every before/after tuple hashes to its recorded source SHA and joins the next tuple; 90 referenced journal files match their indexed SHA-256. The tip is E1499CD695F2F414D9379A8917B6B5B36E50EA0D046DE495938157D8FF97ADD7, and the tip index is F2628D894D6907F64733325581E0116C1D7B297B45FEC0D9D63C4AFF82D09288. The 222 immutable audit files reproduce inventory SHA-256 0E51A4FA51220EC0E92B1044CDB0887DFA8E33EF8C825EF5FFCEF9034B619E53. The tracked checker also returns ACTUAL_REVIEW_PROGRESS_CHAIN_PASS, 104 links, 22 events after 82, and HOLD.
3. Replayed this exact build.mjs with --check against the private 104 snapshot, verified receipt, captured 254-file tree, pinned #1563 worker, and historical host readback. Result: PROPOSAL_ONLY_HOLD, 13 bound output files, 104 to proposed 105, six chapters, 65 scenes, 76 lines, 74 claims, 25 current composed sources versus 18 required public sources, writes 0. Every stored output byte matches its manifest hash.
4. Ran fixture.test.mjs: 9 passed, 0 failed, 0 skipped. These are synthetic OS Temp tests for STOP/LEASE, stale source, jobs/budget drift, four crash points, marker/root safety and a junction escape. They do not establish a production two-mount transaction.
5. Independently reconstructed old and proposed scene, line and claim maps: 79/108/85 becomes 65/76/74; every ID is unique. The 104-to-r23 claim map has 66 retired, 55 added and 19 retained; all retained before/proposed object SHA values and chapter locations match mapping.json. The r12 bridge comparison separately retires n60 and n64–n67 and adds t46. All 74 proposed claim texts, scene IDs, chapter assignments, plan source indices, public source indices and URLs match the r23 PENDING rows and 74-row alignment. Each proposed claim is fact:null and UNCHECKED. All 65 composed scenes preserve the r23 line text, visual data and claim references.
6. The 25 internal plan URLs include exactly the 18 r23 public URLs and seven research-only URLs. The current candidate/video.json still has 25 sources, and gates.json explicitly records that the A01 public-source filter is neither implemented nor deployed. All six checked/listened chapter flags are false; formal script-review issuance, installation and paid work are false. A filename-only leak scan of this v2 package found no concrete local user path or saved PuTTY session string.

A deprecated private independent checker returned JOURNAL_SCOPE_INVALID because its old journal whitelist omitted a now-chapter writer event. The current tracked checker accepts that constrained historical event and passed; the separate edge/journal-hash traversal above also passed. The obsolete checker result is not treated as source drift or as a passing check.

## Adoption holds

- **P1 adoption gate — public sources:** Installing the current candidate/video.json would expose 25 plan sources while the r23 reviewed public list has 18. Implement and independently review the A01-only 25-to-18 public filter, rebuild hashes against the deployed worker, then re-review before any installation or script-review receipt.
- **P1 adoption gate — production transaction and freshness:** This package has no production installer or durable two-store recovery driver. The historical 2026-10-18 host preflight saw one running and three queued global paid stage jobs; their present state, A01 STOP/LEASE, release, worker, source, budget and locks need a fresh same-window readback. No historical receipt authorizes a current host write.
- The t7b claim ID is provisional until the formal verifier saves and renumbers the exact chapter bytes. Old claims.md, script.md, verify-1.md and narrative.json are intentionally stale; no new formal verifier, listener, two-reader narrative verdict, hash-bound script-review receipt, measured TTS, image contact sheet, final film or owner acceptance exists.
- The r23 blind-story review's one P2 pacing concern remains editorial work. This audit checks mapping and replay integrity, not whether the film is enjoyable or 7–8 minutes by actual audio.

The earlier same-level non-v2 r23 proposal is superseded and was not adopted or modified. No candidate file, formal review, host state, PR, supplier account or paid media was changed in this audit.
