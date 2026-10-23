# C20 Zippo v4 — blind reader A parity receipt

Recorded: 2026-10-23T15:04:47.9678992+08:00

## Locked review

The narrator-only judgment was frozen before any author-file or PR inspection. The external local source lock at `C:\Users\x8120\.codex\blind-locks\c20-zippo-v4\reader-a-20261023T1502+0800.md` remains read-only. Its repository copy is [independent-blind-v4-reader-a.md](independent-blind-v4-reader-a.md). Both have SHA-256 `F7BBCAA2BC1410E4F226EB0D6488710B0FE60E77DA52BE163EC4C798A628219B`; the lock records `2026-10-23T15:00:12.3932917+08:00` and the projection SHA below.

The 12-item result is **HOLD** (5 required HOLD, 7 PASS). The five actionable holds are:

| Item | Narration IDs | Narrative problem to fix |
| --- | --- | --- |
| no_spoiler | c200105 → c200501–c200503 | The opening tells the listener the original-insert return-form rule before the later repair reveal. Keep that exact rule for the repair scene; open on the uncertainty instead. |
| payoffs | c200213 → c200301; c200105 → c200501–c200503 | “他是誰？” earns only a name and no reason the co-inventor matters. Either give his documented role and why it changes the story, or remove that question. The insert payoff also loses force because c200105 pre-discloses it. |
| opening_hooks | c200101–c200107, especially c200103–c200105 | The first ~30–45 seconds pass through patent parts, a bottom stamp, and a UK form before c200106–c200107 state the central conflict. Put one concrete repair consequence and the single driving question earlier. The time window is a character-count estimate, not TTS. |
| no_detour | c200401–c200404, c200410–c200411 | Wartime production and the museum stop do not change the repair decision on screen. Compress them to only facts that cause the later batch-code or service distinction, or remove them. |
| no_recap | c200607–c200608 versus c200508–c200509 and c200514 | The finale repeats hinge/cosmetic and functional-promise explanations. Move directly from the Double Arc exception to a new concrete consequence and c200609's audience choice. |

Spoken one-pass comprehension is also HOLD: c200105 uses “內膽” before c200303–c200304 makes the inner assembly tangible, and c200103–c200105 requires the listener to track three artifacts without a causal bridge. Paper body length and cadence estimates are not TTS or playback evidence.

## Exact-head narration parity

- Author PR: [#1728](https://github.com/x812033727/travel_scanner/pull/1728), draft at read time.
- Author PR head and this review branch's starting commit: `3b27a5af392acfe88a168850aa57d2f27cb2f84d`.
- Author PR base at read time: `codex/brand-story-zippo-c20` (`0058e61d06224c797a514116d76364fa5bab9b0b`).
- Script checked: `docs/videos/story-everyday-zippo-c20/script.md`, SHA-256 `F954A0AB9893D6C7087F9D71C8337CB2826F72ABA9FEA1A45C638E16EBDA8C2E` at the exact head.
- Narrator-only projection: `c20-zippo-narration-v4-only.txt`, SHA-256 `0AB3EE39F253B19604618BDF70424DBEEDA51711561673B3120A06563697F761`.
- Method: read every projection TSV row and every `script.md` Markdown table row whose first cell is a `c20` line ID; remove only table-cell boundary spacing, then compare ID, order, and spoken text using case-sensitive string comparison.
- Result: **64 projection rows; 64 script rows; 64 unique script IDs; 64/64 ordered exact matches; 0 missing, extra, reordered, or text-different rows.**

This receipt verifies narration parity only. It does not validate cited facts, visuals, source notes, TTS duration, audio, video, upload, or owner approval. No author file was changed in this review branch.