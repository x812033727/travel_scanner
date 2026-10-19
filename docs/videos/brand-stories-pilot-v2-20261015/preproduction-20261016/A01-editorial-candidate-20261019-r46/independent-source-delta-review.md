# r46 independent source-delta review — 2026-10-19

Reviewer: root `codex-gpt6-a01`; r46 was authored by a separate agent.
Reviewed manifest SHA-256:
`d6b9e59358d7616a97c333368b6533f5f45745f5625887276e91a2095df6d794`.

**PASS for the bounded narrative/source delta.** This compares the revision
against the previously reviewed source material; it is not a new retrieval of
the public sources or a formal worker fact-check receipt.

## Exact change boundary

An independent recursive comparison of the two candidate videos found exactly
five changed narration text fields and changes within the eight-entry loop table.
Every other video field, including scene/line identities, claim rows, scene claim
references, image prompts, source URLs, voice, music, subtitles, title and
thumbnail, is identical. `claims.md`, lexicon, source alignment and source map
also compare byte-for-byte with r45. Historical r44/r45 packages, handoffs and
the portability evidence remain identical to approved Git head `f43fef783`.

| Revised line | Evidence retained | Source-bound reading |
| --- | --- | --- |
| `r44l011` | q014–q017 | The screw-attached cart returns to security; the narrator asks how the officer responds. It does not say the object was cleared, boarded, or became the later integrated product. |
| `r44l023` | q027–q029 | The company-attributed crew adoption leads to a question about garage capacity, answered by the existing warehouse move. No sales number, relocation date or new causal evidence is asserted. |
| `r44l028` | q033–q034 | A reported airport observation leads to the separate early sales-channel question. It does not identify the observed travelers as particular mail-order customers or date both accounts to one event. |
| `r44l035` | q040–q042 | Past waiting under a load is explicitly separated from the reporter's current test. The following four-brand result answers the curb/stairs question without inventing their locations or order. |
| `r44l047` | q047, q050, q052, q054 | The pocket-related size explanation remains; the new question concerns the reporter's final preference. The later answer remains one of her preferred cases, not an exclusive winner or purchase decision. |

The unchanged q028 row retains its historical editorial description of the old
second sentence as a visual transition. That descriptor does not describe the
new garage-capacity question. The r46 narration delta explicitly supplies the
new question and q029 payoff; no independent historical assertion is drawn from
that old descriptor. Retained source maps and dates remain historical provenance.

## Loops and checks

Four opening promises and the crew-adoption loop remain. Garage capacity,
mail-order sales and the final favorable verdict replace three weaker or
duplicated entries. The undated screw-cart anecdote is not treated as the same
object as the reporter's 1993 commercial case. The security and curb questions
reinforce earlier promises rather than adding duplicate loop counts.

Root reran `build.mjs --check`: 51 scenes, 53 lines, eight loops, zero lint
errors and 40 retained warnings. The tight-cadence check passes at 250, 275 and
300 CPM. The 275-CPM body estimate is 425.6 seconds; actual TTS remains unmeasured,
and the 300-CPM estimate is below the owner's seven-minute floor.

All 55 claims remain PENDING. This report does not authorize host adoption,
provider calls, media generation, deployment or publication. Formal source,
listener, script and final-media gates remain separate.
