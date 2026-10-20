# R15 isolated narrative OR merge

Script: `docs/videos/curio-s52/script.md` at raw SHA-256 `1764cc03aa5bb5ea402e89b7e21e163d676045c6e42611dfaa54fdc69fa62131`.

Blind A and B were frozen independently before this merge. A was moved from the mistaken repository-root `review/` directory into `docs/videos/curio-s52/review/` without editing its contents. This path correction did not change its decisions.

- Blind A: `r15-isolated-blind-a.json`, SHA-256 `aa73ac790422d290826d19971e18aa86fd248f0a717999af8da888a62c1ed0ea`.
- Blind B: `r15-isolated-blind-b.json`, SHA-256 `cdeb8468225bb2d55151c2017976ed89743f350843c9120e61c7b255a8900f43`.
- Official OR input: `r15-isolated-merged-answers.json`, SHA-256 `9ff01579a36578369db19dbf667d547bd7c43ca57767f1a96bbab48055e896b1`.

| Question | Blind A | Blind B | OR |
| --- | --- | --- | --- |
| `scene_first` | Yes | Yes | Yes |
| `no_spoiler` | Yes | Yes | Yes |
| `one_line` | Yes | Yes | Yes |
| `no_toc` | Yes | Yes | Yes |
| `chapters_link` | Yes | Yes | Yes |
| `open_loops` | Yes | Yes | Yes |
| `payoffs` | Yes | Yes | Yes |
| `no_recap` | Yes | Yes | Yes |
| `chapters_are_events` | Yes | Yes | Yes |
| `outro_no_next` | Yes | Yes | Yes |
| `opening_hooks` | Yes | Yes | Yes |
| `one_thread` | Yes | Yes | Yes |
| `no_detour` | Yes | Yes | Yes |

There were no disagreements. Both blind readers and the OR merge marked all 13 questions Yes. The merged evidence uses B’s quotes except for `chapters_are_events`, where it uses A’s line cited quotes. Neither blind file was changed for that adjustment.

## CLI validation

Ran `node tools/video/cli.mjs narrative --slug curio-s52 --answers /tmp/curio-s52-r15-isolated-le1arz61/merged-answers.json` with `VIDEO_WORKDIR=/tmp/curio-s52-r15-isolated-le1arz61`. The answer input and generated verdict were in that isolated writable `/tmp` directory.

Final exit code: `0`. Verdict: `passed=true`, `13/13` Yes, `failed=[]`, `advisory=[]`. The complete command output and verdict summary are saved in `r15-isolated-cli-receipt.json`.

An initial CLI run reported an advisory for the chapter headings because B’s evidence named headings without a line ID. The merged evidence was changed to A’s line cited evidence, then the CLI passed without advisories. The receipt retains the initial run and final rerun.

No script or media files were edited, and no paid calls were made.
