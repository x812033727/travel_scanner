# C20 Zippo v4 — independent narrator-only reader B

## Blind lock

- **Verdict: HOLD.** A HOLD on any required item makes this reader's verdict HOLD.
- The reader saw only the 64 ID-tagged narration lines in `c20-zippo-narration-v4-only.txt` before locking the verdict. No author script, treatment, source matrix, visual plan, reviews, PR, task notes, or prior reader verdict was consulted before the lock.
- Narration SHA-256: `0AB3EE39F253B19604618BDF70424DBEEDA51711561673B3120A06563697F761`.
- Local blind lock: `C:\Users\x8120\.codex\worktrees\b16f\travel_scanㄐ\c20-zippo-v4-reader2-blind-locked.json`, read-only after creation. Its SHA-256 is `DD5C0EE29C121D32BCDBE62B6EC302898AC474BE4BBF7444EF2C9FDDA7659BF5`.
- A byte-identical copy of that lock is [reader2-v4-blind-lock.json](reader2-v4-blind-lock.json). The lock records all twelve binary answers and cited line IDs.

| Required item | Reader B | Narration evidence |
| --- | --- | --- |
| `scene_first` | PASS | `c200101`, `c200103`: repair desk, worn case, patent drawing. |
| `no_spoiler` | **HOLD** | `c200105` states the UK form condition for retrieving the original insert before `c200502`–`c200503` reveal the replacement practice. |
| `one_line` | PASS | `c200106`–`c200107` to `c200514`: what the free repair promise preserves. |
| `no_toc` | PASS | `c200101`–`c200107`: scene and question, no narrated chapter list. |
| `chapters_link` | PASS | `c200213`→`c200301`, `c200311`→`c200401`, `c200412`→`c200501`, `c200515`→`c200601`. |
| `open_loops` | PASS | `c200106`, `c200209`, `c200213`, `c200412`, `c200515`. |
| `payoffs` | PASS | `c200301`, `c200406`, `c200501`–`c200514`, `c200601`. |
| `outro_no_next` | PASS | `c200609`–`c200610`: viewer question and subscription invitation, no next episode. |
| `opening_hooks` | PASS | `c200101`–`c200107`: visible wear, repair promise, patent, date mark, and repair question. |
| `one_thread` | PASS | `c200107`, `c200209`, `c200412`, `c200514`: one lighter and its repair promise. |
| `no_detour` | **HOLD** | `c200401`–`c200404` devote four lines to wartime production/materials, while `c200403` says this history does not explain wartime repair; `c200410` adds a museum stop. |
| `no_recap` | **HOLD** | `c200607` repeats the hinge/finish distinction in `c200508`–`c200509`; `c200608` repeats the traditional-function conclusion of `c200514`. |

## Cadence and listening

The 30–45 second hook cadence is **HOLD on paper**: explicit open questions are unevenly spaced. The span from `c200106` to `c200209` is about 397 narration characters; `c200412` to `c200515` is about 576, with interim revelations but no new explicit question. Character count is a routing signal, not a timed voice measurement. A normal-speed TTS playback has **not** been produced or timed here.

One-pass oral comprehension is **PASS with a note**: the UK and US policies and Double Arc insert are named when introduced (`c200501`, `c200505`, `c200512`, `c200601`), but `c200501`–`c200513` packs many service distinctions into one stretch. Actual delivery and pauses need listening review.

## Exact-head parity, checked after lock

- Author PR: [#1728](https://github.com/x812033727/travel_scanner/pull/1728), draft and open at the check; PR base `codex/brand-story-zippo-c20` at `0058e61d06224c797a514116d76364fa5bab9b0b`; author head `codex/brand-story-zippo-c20-script` at **`3b27a5af392acfe88a168850aa57d2f27cb2f84d`**.
- This reader branch started from that exact author head, without editing the author branch or script.
- The 64 tab-separated blind narration IDs were compared with the `旁白` column of `docs/videos/story-everyday-zippo-c20/script.md` in the exact author commit using ordinal string equality. Result: **64/64 exact matches**, zero missing IDs, zero extra IDs, zero duplicate IDs, zero text mismatches.
- Exact author script Git blob: `ecc1b0dd6ce065f6951dbb354b5e3a999de2b89a`.
- This is a narrative review of text only. It does not approve facts, visuals, TTS duration, paid production, import, upload, publication, or owner acceptance.

## Checks on the isolated reader branch

- `git diff --cached --check`: PASS.
- Blind-lock JSON readback: all 12 required keys have PASS/HOLD and cited IDs; the copied lock SHA-256 still matches the pre-context local lock.
- `npm run check:tasks`: PASS, 2,079 task files validated; existing stale/overlapping-claim warnings are unrelated to this narrow review scope.
- `npm run test:docs-videos`: 131/137 tests passed; 6 failed because this fresh worktree has no `node_modules/pinyin-pro` installed (`ERR_MODULE_NOT_FOUND` in `tools/video/tts/check.mjs`). No script or runtime source file was changed in this reader branch. This suite is **not reported green**.
