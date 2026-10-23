# H12 second-pass keyframe audit and targeted prompt repair

2026-10-16. Media root: `<home>/mokaair-work/videos/curio-h12`. The second-pass keyframe command exited after drawing all 86 illustrated shots. Its final manifest has 83 judge PASS and three judge held. Every current selected image was checked against its approved narrated line and scene intent; high-risk frames and every alternate take for the held shots were opened at full size. Six of the judge-PASS images directly conflict with the narration or the 1900 setting, leaving 77 visually accepted, three held, and six human-failed shots.

## Exact third-pass set

| Gate | Shot and current selected file | Reason for repair | Prompt-only revision |
| --- | --- | --- | --- |
| Human fail | `landing-no-reply` — `landing-no-reply-1.jpg` | A red flag flies beside the lighthouse while the line says the normal flag was absent. | Tight keeper portrait with only tender rail, open water and sky behind him. |
| Human fail | `lamp-ready` — `lamp-ready-1-trim.jpg` | Modern electric fixture, laboratory cupboards and glassware replace a 1900 lighthouse oil burner. | Close view of unlit brass oil burner, dark wick, full metal reservoir, hand and stone shelf. |
| Human fail | `slate-entry` — `slate-entry-1.jpg` | A white tablet in a modern office replaces the separate black chalk slate described in the report. | Object close-up of matte-black framed slate beside a bound paper log on a wooden desk. |
| Human fail | `kitchen-work` — `kitchen-work-2-trim.jpg` | Modern gas range and kitchen appliances place the documented clean pots in the wrong period. | Washed, cold iron pots on a plain shelf in a stone-walled lighthouse kitchen; omit stove. |
| Held | `work-date-inference` — `work-date-inference-1-trim.jpg` | Three takes show a desk placard/group or a child interrogation rather than separate routine-work clues. | Overhead slate and washed pot on a weathered desk, one adult hand comparing them; camera changed from `tilt up` to `push in` to fit the overhead close-up. |
| Held | `crane-safe` — `crane-safe-3.jpg` | Three takes show a disembodied head, a worker tethered to a modern crane, or a suspended box rather than an intact lowered landing derrick. | Object close-up of short iron arm lowered against rock, with chain attached to a rock anchor and no cargo/person. |
| Human fail | `railings-twisted` — `railings-twisted-1.jpg` | The iron rails remain straight although the narration says platform and walkway rails were deformed. | Center a sharply kinked top rail and twisted upright, without a posed figure. |
| Human fail | `buoy-question` — `buoy-question-1-trim.jpg` | A complete hanging red-and-white rescue float appears where the narration says the tied ring was missing. | Empty hook and frayed tie on bare rail; omit the rescue-object noun that induced a complete float. |
| Held | `kitchen-recalled` — `kitchen-recalled-1-trim.jpg` | The selected take shows a steaming pot that implies a recent meal; alternate takes show modern office readers and no cold kitchen evidence. | Cold inverted clean pot beside a closed old report, without food, steam or people. |

No already generated alternate is safe for these nine shots. The other 77 illustrated frames are accepted: harmless extra figures or simplified props are not grounds for a paid retake when they do not assert false evidence. In particular, `overturned-chair-2.jpg` clearly shows the chair on its side and is accepted. The final `exhibit-first-2.jpg` shows the letter and exhibition case and is accepted despite a stylized attendant pose. Replacing a difficult illustration with a source card would alter the approved screenplay and is not part of this repair.

## Scope, cost, and offline checks

- Second pass generated 61 new images and 61 image-judge decisions, costing US$0.8235; local media spend is US$1.9845 across both passes. This receipt makes no paid call or ledger write.
- The third-pass proposal is **nine shots**, at most three new takes per shot. At the observed US$0.0135 per image plus judge decision, a 27-take ceiling is **US$0.3645** before any new reservation. Actual cost must be read back from the media ledger.
- `video.json` SHA-256 before this prompt repair: `55F886845D1A52F55FE5EFC30C4018FF8360EDD94ECB308FB870DDF75D66A2BD`; after: `09FA78E1D58733CBB8ACDAE46812641E80725C0350E0A5206B1F4DC0114F0BB3`.
- Exactly nine existing `data.prompt` strings changed; only `work-date-inference.data.camera` also changed. No narration, scene order, line ID, claim, card or other field was edited. Approved `script.md` SHA-256 remains `408E3C8BAAFC0063B0B53410B579D14BA09D650753DB466A409E59470F9A620B`.
- `node tools/video/cli.mjs lint --slug curio-h12`: exit 0, 0 errors, four pre-existing warnings (repeated lighthouse/island wording, a 10.6-second shot, and textual 8.8-minute estimate). `node tools/video/cli.mjs keyframes --slug curio-h12 --dry-run`: exit 0. `git diff --check`: exit 0.

The revised prompts are candidates. Accept or reject each generated image after visual review; judge PASS alone does not resolve the six human-found contradictions.
