# C20 Zippo v5r1 — independent source and paired-visual delta

Reviewed 2026-10-23 (Taipei). **PASS on the five repaired rows.** This receipt is stacked on author draft PR #1728 at exact commit `7eac4c6b9689532f7246c00d6fd1408992d0cf27`. The previous full independent v5 audit is draft PR #1766 at old author commit `836e2c8c1bf2d0f72e320892a2ddd50638d4088b`; it found 59/60 spoken rows and 56/60 visuals PASS. The present author diff changes only its one spoken HOLD (`c200608`), four visual HOLDs (`c200201`, `c200406`, `c200601`, `c200609`), their paired JSON/source text, and the author receipt. I did not edit the author files.

## Bound current inputs

| Author file | SHA-256 |
| --- | --- |
| `script.md` | `F5ADDA705E67E8C3300642D5E16A9CE63C05640DFDB11289A892D794CE56289D` |
| `script-source-notes.md` | `6117154F1773CE8C1D7DE3E2AB8EA51026DB5241691EA45CF323A849DA2F7A4B` |
| `visual-plan.md` | `296F1E4FCAC9261A0F5AB2745D946B1C49A1923D21988EA7F4C3E4E090C978B9` |
| `visual-plan.json` | `92C5245EF942BB81C3FCFEBC8837B7AB34EDB4C2055F21575E041390765BD007` |

The current plan has 60 unique, same-order IDs in script, source notes, visual Markdown, and JSON. All 60 JSON spoken texts/source tags and all 60 prompts/card texts match their Markdown rows exactly. It retains 53 illustration prompts, 7 postproduction cards, `MiniMax image-01`, exactly `{"preset":"cute-mystery"}`, a 5-second intro after `c200107`, and a 21-second v4 outro after `c200610`. This is text and configuration parity, not rendered-media QA.

## Primary evidence reopened

- [Zippo UK windproof-lighter repair page](https://www.zippo.co.uk/pages/zippo-repairs-windproof-lighter): UK case-only repair should omit the insert; when an insert needs repair, the normal procedure is replacement, and the original is returned only if requested on the form. The page confines its shipping process to UK customers.
- [Zippo US warranty and repair page](https://kb.zippo.com/warranty-repair) and [broken-hinge page](https://kb.zippo.com/zippo-lighter/hinge-broke): the traditional windproof pocket lighter's lifetime functional guarantee and a covered mechanical example.
- [Zippo US worn-decoration page](https://kb.zippo.com/zippo-lighter/worn-deco): finish and decoration are outside that lifetime guarantee; contact options for a newer product are separate.
- [Zippo US Double Arc insert FAQ](https://kb.zippo.com/arc-repair-faqs-and-guidance): the separately discussed rechargeable insert has a two-year warranty window in this US-facing document.
- Repository [Curio illustration rule](../../../../.agents/skills/curio-episode/SKILL.md), “插圖提示詞怎麼寫”: one person performing one action in an image prompt; no two-person interaction. The author's visual contract also bars logos, readable text, real likenesses, and historical-document reconstruction.

## Five changed-row decisions

| ID and field | Independent decision | Reason |
| --- | --- | --- |
| `c200608` narration and source note | **PASS** | The new final answer expressly separates the UK insert-replacement process from the US exclusion of finish/decoration. “可能換內膽” is conservative beside the UK page's normal replacement procedure. It does not universalize the UK repair route or promise that every original part remains. The source note preserves M09 UK and M10 US scope. |
| `c200201` image prompt | **PASS** | One fictional adult examines one generic unmarked old metal object at a period-style table. This meets the one-person/one-action visual rule and, paired with the narration's retrospective-company attribution, does not purport to reproduce an identified historic encounter. |
| `c200406` image prompt | **PASS** | One anonymous collector looks at a generic bottom mark; the blank quality-control card supplies context without a second person, readable marking, or invented documentary record. |
| `c200601` postproduction card | **PASS** | “美國站” now appears on the visible card with “Double Arc 內膽 · 兩年保固”, matching the US-facing FAQ and the oral line's “美國維修說明” scope. It does not present two years as a worldwide term. |
| `c200609` image prompt | **PASS** | The frame now has one pensive fictional adult, a worn generic case, and one indistinct separated component; it removes the side-by-side old/new choices and promises no repair outcome. The spoken audience question remains a value question, not a warranty election. |

The unchanged 59 spoken and 56 visual rows retain the exact bytes independently passed in PR #1766; the Git diff and complete current mirror comparison establish that scope. Combining that earlier full audit with these five new decisions yields **60/60 oral-source PASS and 60/60 paired-visual PASS on the exact v5r1 author files above**. This delta receipt does not re-audit unchanged rows from scratch.

## Remaining gates

The current narrator-only projection must receive two fresh, isolated blind narrative reads because `c200608` changed; older v5 blind conclusions do not carry forward. No owner script/shot approval, measured postintro TTS duration ≥480 seconds, rendered illustration-time ≥70%, paid-media authorization, import, upload, merge, or publication is implied. The paper character estimate in the author receipt is not measured speech.
