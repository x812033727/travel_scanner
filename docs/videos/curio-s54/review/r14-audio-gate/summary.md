# S54 R14 audio gate — HOLD

The exact S54 script (`483558f1617939d109c453ec35f09840ed3de9bcbf0455aa1598433f9b74448f`) stayed unchanged. Before synthesis, the formal merged narrative receipt passed 13/13 questions and the single exact Jev policy request returned PASS against the current script, `video.json`, and `brief.md` hashes.

| Stage | New billable characters | Full check | Approx. wall time |
| --- | ---: | --- | ---: |
| Initial cached TTS | 3,111; five requests reused | 30/148 flagged | TTS 645 s; check 1,060 s |
| Retake 1: exactly the initial 30 flags | 645 | 19/148 flagged | TTS 144 s; check 219 s |
| Retake 2: `s54005`, `s54095`, `s54119`, `s54122`, `s54126`, `s54138` | 124 | **17/148 flagged** | TTS 34 s; check 55 s |

Total new synthesis: **3,880 billable characters**. Final narration: **13:45**. No 429 surfaced. Both retake scope audits confirm that only their listed WAVs changed. The S54 workdir `STOP` file was restored. No script, brief, or `video.json` edits were made, and no human listening result is claimed.

The final check completed all 148 lines: 99 exact matches, 23 same-sound or filler differences, nine accepted by Jev, and **17 flags**. The exact IDs are in [check-flags-final.json](check-flags-final.json); [check-final.json](check-final.json) preserves the full transcripts and scores. [run-receipt.json](run-receipt.json) binds input hashes, gates, timing, costs, checks, and the HOLD state. The three check logs, timing files, pre/post WAV manifests, and scope audits remain in this directory.

The [17-line oral wording handoff](oral-wording-handoff.md) quotes each current line and final ASR text, with proposed wording or an independent-audio check and guards for names, units, dates, source attribution, and office roles. A separate R15 author can evaluate those proposals, then renew the narrative, policy, and audio gates if the script changes. Audio approval remains **HOLD** while any flagged line remains.
