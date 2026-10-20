# R7 isolated narrative merge

**Official OR verdict: FAIL, 12/13 yes.** Both independent readers answered No to the required `no_recap` question. The other 12 questions passed. This is bound to `script.md` SHA-256 `a5931c83a5fcd448b83a8be9d2865c904672fa09ce4f5bec6388d74fad3a58ec`.

The two raw reports were frozen before either reader saw the other's answers. Their unchanged files are [A JSON](r7-isolated-blind-a.json), [A Markdown](r7-isolated-blind-a.md), [B JSON](r7-isolated-blind-b.json), and [B Markdown](r7-isolated-blind-b.md). Raw JSON SHA-256: A `7e379ccd79f9ca4c4f83ba5e6af503a8335c24191284478363c1d128c809d337`; B `3400f05047f3474ea12d96e0ebb78edd56add26e295ec694d9552d641d27510b`.

| Question | A | B | Official OR |
|---|---|---|---|
| `scene_first` | Yes | Yes | Yes |
| `no_spoiler` | Yes | Yes | Yes |
| `one_line` | Yes | Yes | Yes |
| `no_toc` | Yes | Yes | Yes |
| `chapters_link` | Yes | Yes | Yes |
| `open_loops` | Yes | Yes | Yes |
| `payoffs` | Yes | Yes | Yes |
| `no_recap` | **No** | **No** | **No** |
| `chapters_are_events` | Yes | Yes | Yes |
| `outro_no_next` | Yes | Yes | Yes |
| `opening_hooks` | Yes | Yes | Yes |
| `one_thread` | Yes | Yes | Yes |
| `no_detour` | Yes | Yes | Yes |

Reader A found that [s53001] and [s53003] both say cottages remain in the square, while [s53003] also restates the deadline just given at [s53002]. Reader B independently found that [s53105] gives **680** complete household records and [s53110] repeats **680** when introducing a subset. These are distinct examples of the same required-question failure; both repairs should be considered before a new exact-script review.

The raw responses were mapped without changing yes/no decisions into the panel's `{id, yes, evidence}` format. The official `panelVerdict` validated each cited answer, then the official `mergePanelVerdicts` applied its any-reader-yes rule. The exact normalized inputs, complete verdicts, merge result, and command summary are preserved in [A panel answers](r7-isolated-panel-answers-a.json), [B panel answers](r7-isolated-panel-answers-b.json), [merge JSON](r7-isolated-merge.json), and [CLI receipt](r7-isolated-merge.cli.txt). No script or media was changed for this review.
