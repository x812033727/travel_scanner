# S29 R6 audio-listener wording handoff

2026-10-20. The R5 independent story/source/still review passed on the hashes in [verify-8.md](verify-8.md). R5 TTS made 93 clips and measured an 8:39.8 story body. The native full `check-audio` flagged 22 of 94 lines; a targeted retake of those 22 (526 billable characters, 71 cached clips) left 13 flags; a second targeted retake of those 13 (314 billable characters, 80 cached clips) left **8**. Both full passes still completed 94/94, and the 8 persistent flags are `boat026`, `boat034`, `boat068`, `boat069`, `boat078`, `boat094`, `boat101`, `boat104`. Some involve same-sound transcription of historical terms; the native gate still reports them, so R5 audio is **not** approved. No image or music was ordered.

R6 rewrites only those eight spoken lines and the corresponding first column in [claims.md](claims.md). `boat068`, `boat069`, `boat078` paraphrase the exact Sanguozhi/CBETA words in speech while the claim notes retain the original phrases `量石著中`, `即以此船`, and `即施行焉`. The other five replace ambiguous compressed sounds with ordinary wording, without changing the answer, source boundary or scene order. All 94 IDs and 92 still prompts are unchanged.

| Frozen R6 file | SHA-256 |
| --- | --- |
| `video.json` | `c9f2275359a01768164b63cd9362912541ef50052ac7ebf3aaaee7d305c4889a` |
| `script.md` | `46b78be5d790a0bc3c760db2883c6a0dcafc4931519ccc4e6d91d1bcfd38d540` |
| `claims.md` | `fe45ff1878e9aa2d5f293bdfdc57a16ed7256e6596640cd186a3325600281921` |

`script --slug curio-s29` regenerated the markdown from this JSON. `lint --slug curio-s29 --json` reports **0 errors and 0 warnings**, 94 lines, about 9:24 estimated total. This is an **author revision, not an independent R6 pass**. An unrelated reader must first seal the official 13-question narrative answers against this exact script, then recheck all eight revised claims and static prompt alignment against the pinned sources. R5 script approval is stale by hash. Only after R6 passes may the coordinating agent approve this exact script locally under the user's standing delegation, synthesize eight changed clips and rerun full audio verification. Re-measure the body on the new timeline before art; the recorded image-plus-music cap remains US$3.81.
