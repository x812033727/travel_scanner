# S53 R8 isolated narrative panel merge

**Script SHA-256:** `209c65b528aed2c36083588ed11c5be2869434571d405367bef2e1f1ef4a0d8d`
**Decision:** **HOLD.** The official `mergePanelVerdicts` OR rule passes an item when either reader cites a line and answers yes. Both readers answered no on required `no_recap`, so the merged panel fails. The official narrative CLI wrote a bound failed record in an isolated `/tmp` work directory and exited 1 as expected. No script or media was changed.

| Item | A | B | Official OR merge | Evidence |
| --- | --- | --- | --- | --- |
| `scene_first` | Yes | Yes | Yes | The first four lines establish June 1907 cottages, clearance, land and payment [s53001–s53004]. |
| `no_spoiler` | Yes | Yes | Yes | The opening withholds the deadline's outcome and later survey finding [s53002; s53008; s53071; s53105]. |
| `one_line` | Yes | No | **Yes** | B flags an undated later refund [s53062] followed by a return to March 1907 construction completion [s53038]. A treats the body as a forward cottage sequence [s53028; s53057–s53060; s53071; s53101]. The OR rule resolves this disagreement to yes; B's concern remains in its frozen review. |
| `no_toc` | Yes | Yes | Yes | The forward lines ask story questions [s53006–s53009]. |
| `chapters_link` | Yes | Yes | Yes | Chapter bridges carry forward construction, ownership, move proof, departed cottages and survey [s53027–s53028; s53048–s53049; s53068–s53069; s53083–s53084; s53100–s53101]. |
| `open_loops` | Yes | Yes | Yes | The recurring questions include site permission, moving conditions, survey yield and rent loss [s53023; s53068; s53104; s53116]. |
| `payoffs` | Yes | Yes | Yes | Sale replaces rent [s53057–s53060], move costs get payer details [s53089–s53092], and the rent loss question gets an explicit callback and 23 known cases [s53116; s53129–s53131]. B records a caveat about the survey changing from cottage addresses to family records [s53097; s53103–s53109]. |
| `no_recap` | **No** | **No** | **No — blocking** | Both readers independently identify the same repeated land prerequisite: find land for the cottage [s53003] and find the next plot after construction [s53041], without a named callback to the opening. B also flags the rented/bought alternatives repeated [s53069; s53093]. |
| `chapters_are_events` (advisory) | Yes | Yes | Yes | Headings describe the fire, construction, sale change, clearance, movement and partial visit [s53010; s53028; s53049; s53071; s53084; s53101]. |
| `outro_no_next` | Yes | Yes | Yes | The outro mentions no next episode or file [outro]. |
| `opening_hooks` | Yes | Yes | Yes | Ownership, moving fee, later visit and park origin remain open [s53006–s53009]. |
| `one_thread` | Yes | Yes | Yes | The cottage's need for a lawful, affordable place to stand runs through the story [s53003; s53060; s53069; s53130]. |
| `no_detour` | Yes | Yes | Yes | Allocation, contracts, moving and later conditions track the same cottages [s53033–s53037; s53049–s53063; s53084–s53096; s53118–s53130]. |

**Minimal repair:** Replace or remove the repeated land statement at [s53041], or make it explicitly recall [s53003] and add a new consequence of construction. Recheck [s53069] against [s53093] for an unnecessary second statement of the land alternatives. The frozen blind reads remain unchanged; any script revision needs another blind panel on its new hash.

## Provenance

- Reader A raw: `r8-isolated-blind-a.json`, SHA-256 `47459df5ccd6b171e4ad617e27e2c67915571aedcc970d19b461d09ffa0922dc`; markdown SHA-256 `a9f814018001aaaa40984ac6ab9046f900221dd150654842d771493f4e3a8af2`.
- Reader B raw: `r8-isolated-blind-b.json`, SHA-256 `91c6dc9586b560630b43c323e17003e7b5d488792835fd8000305b50de72087a`; markdown SHA-256 `38dd0007496426584bba4088ec2803380c2ee8bb6e7664d8f1425c8e8c7c0712`. B was frozen before A and the merge references were read.
- CLI adapters: `r8-isolated-panel-answers-a.json`, SHA-256 `9095c30a43766486bc5bf3a0cee0c8119ae5ac33bf5363d22866755769d72e9c`; `r8-isolated-panel-answers-b.json`, SHA-256 `d720a6744c07206450c29641b4cdd937ea1b8ed097d4acc1667faeb6850235ad`.
- Official OR output: `r8-isolated-merged-verdict.json`, SHA-256 `e22c96aaeb79fd56fa015a2fee3a596a4cb5dfc3151f512e90b7089bf8e698b1`; CLI answer payload: `r8-isolated-merged-answers.json`, SHA-256 `1e99aa390c7b3efe534ad8f2092230c36c7c1ceebfdac1715ff7479a999e62ab`.
- CLI receipt: `r8-isolated-merge.cli.txt`. The official record is `/tmp/s53-r8-panel-AP4kak/curio-s53/review/narrative.json`, SHA-256 `4b64613eb398c8008865a208eee40b68df17349ac2bf1e7ee39e7bbf4783110c`, round 1, `passed=false`, `failed=["no_recap"]`.
