# S54 R6 isolated narrative merge

The two frozen blind reviews examined the same `script.md` SHA-256: `33ae45c7addd0088918128a5711969c128bbe4b692743b71cc5703f16deb73ef`. Neither raw review was changed. Their SHA-256 values are:

| Review | SHA-256 |
|---|---|
| A | `607b93e8ebdcd637c9ddc3b89b98598fa59ea87274dcd4826aafd9b98b8ad36b` |
| B | `58c981f9b7bb67a1b83861c408a67d80c80e51c76ebcf4f8bb4cafa713222f44` |

Each review's 13 Yes/No cells was transcribed, with a verbatim line from the official CLI narration selected for each cell. `panelVerdict` validated each set of cited answers. `mergePanelVerdicts` then applied the panel's OR rule: an item passes if either reader says Yes. Both readers gave the same verdict for every item: **10 Yes, 3 No**. The optional `chapters_are_events` item is Yes.

| Required failure | Reader evidence | Reason |
|---|---|---|
| `payoffs` | A: `s54106`; B: `s54067` | The question about whether preprinted envelopes relieved the counter never gets that operational answer (`s54107–10`, `s54125–36`). The question about how uneven December rates were executed at the counter instead gets the trial's rationale (`s54068–73`). B also noted that `s54125–28` never identify who ultimately cut the envelope sheets. |
| `no_recap` | A: `s54099`; B: `s54079` | `s54087` and `s54099` repeat Hill's account of confused hall cash collection. `s54065` and `s54079` repeat Treasury approval of three forms; `s54039` and `s54046` repeat its rate-setting power. |
| `no_detour` | A: `s54016`; B: `s54048` | `s54009–16` stack several tariffs and a weight figure after the old-rate problem is established. `s54047–48` add Gazette and Parliament filing mechanics without a later narrative consequence. A also flagged the later reply-stamp aside at `s54147`. |

The isolated official command was:

```text
node tools/video/cli.mjs narrative --slug curio-s54 --answers docs/videos/curio-s54/review/r6-isolated-merged-answers.json --workdir /tmp/curio-s54-r6-isolated-merge-h4XAkp --json
```

It exited **1**, the expected result for failed required questions, and wrote round 1 with `passed: false` and exactly `payoffs`, `no_recap`, `no_detour` in `failed`. Panel rules SHA-256: `5d71fef2cf3831dc33c0c32b2b297f633c47bfe41fbad18865ae08ed0c91cb75`.

Archive files: `r6-isolated-merge-audit.json` contains both normalized reader answers and the full `mergePanelVerdicts` result; `r6-isolated-merged-answers.json` is the flattened CLI input; `r6-isolated-cli-verdict.json` is CLI stdout; `r6-isolated-cli-receipt.json` is a copy of the isolated workdir receipt. The CLI receipt contains the flattened answers, while the audit preserves the reader-level provenance.
