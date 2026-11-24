# S38 independent script, source and visual review — round 1

Date: 2026-10-19 UTC. Reviewer did not author this script. The review is bound to `script.md` SHA-256 `461c0d454b94e370c4071c6a7f8c75326976fd7d796d347a44a030f7323efeea` and `video.json` SHA-256 `25ff99955050295aba473bef78137d08ea1da2725ea9a9587e0af2298cbce314`. Narrative tool hash: `58f61b4344022d74`; canonical script binding: `e3cede97ec67cca83f2bbfec1de90ded2c3da48fd849540b25a50272c27d120d`.

## Blind panel and checks

I read only the narration in `script.md` and the 13-question output of `VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs narrative --slug curio-s38` before opening research, claims, visual prompts or prior review. I sealed the raw answers at `/tmp/curio-s38-blind-answers.json` before source review (SHA-256 `f39cd90e6af2a6201b50737194b48fa454694d50a062b550168d1c1b5063093f`); an identical copy is [blind-1.json](blind-1.json). For the canonical CLI, I added bracketed line citations to those same answers, with no yes/no changes, in [narrative-answers-1.json](narrative-answers-1.json) (SHA-256 `aa90981f17e2b7911734ea520912db9d3ba6d0daf85f329eac741617cdd9f16e`). `narrative --answers` exited 1 and wrote [narrative-1.json](narrative-1.json): **10 yes / 13, failed `chapters_link`, `payoffs`, `no_detour`**. `lint --slug curio-s38` exited 0 with **0 errors, 0 warnings**.

| Blind failure | Evidence and repair target |
| --- | --- |
| `chapters_link` | `pf087` asks whether the shipped boxes are safe. The next chapter's first line, `pf093`, opens on a different fire; the boxes return only at `pf097`. Either connect the chapter opener to the unresolved question, or change the prior question to one that the new fire actually answers. |
| `payoffs` | `pf033` asks about **Pepys's own wine**, but `pf064–pf068` say only “wine”; the diary explicitly distinguishes Batten's wine in pit one from “our wine” and “my wine” in pit two. `pf054` asks how much the lighter can carry, but the later lines offer cargo examples without a capacity or limit. State the ownership payoff and frame the boat question around an answer the source can provide. |
| `no_detour` | `pf093–pf096` spend four beats on another fire, gutter water and the river ruins before returning to the pending boxes question. Link this sequence to the prior unresolved danger, or shorten and refocus it on Pepys's remaining concern. |

## Primary source check

Independently fetched the pinned [GITenberg Pepys diary text](https://github.com/GITenberg/The-Diary-of-Samuel-Pepys---Complete_4200/blob/68fcf49f70ee793b989a6fd0464264d55beb4451/4200.txt#L65795-L66174) at commit `68fcf49f70ee793b989a6fd0464264d55beb4451` and read the continuous 2–6 September 1666 entries, lines 65795–66174. Downloaded text SHA-256 is `3cd43a3c39ee72eb9c4a3657f1fcb1723afba291cedac176c65a39289483be5d`, matching `research.md`. This is the edited Wheatley text, with later annotations in square brackets. The diary's first-person observations, reported speech and later editorial notes have different evidential weight. All 102 `video.json` lines match the 102 `claims.md` rows and 102 `script.md` lines byte for byte; the claims map covers every narrated line. The 2 September `D2a` span in `research.md` stops at line 65820, although `claims.md` uses `D2a` through line 65831 for `pf018–pf021`; the latter range is the correct one for those lines.

| ID | Source boundary and needed wording |
| --- | --- |
| `pf095` | The diary says women worked “in the cannells, sweeping of water” at lines 66147–48. It does **not** say they swept gutter water **toward the fire**. Remove the destination from narration and image prompt. |
| `pf087`, `pf097` | On 5 September, while returning from Woolwich, Pepys already saw his goods “well in the lighters at Deptford, and watched well by people” (lines 66083–85). On 6 September he **landed** all the goods safely at Sir G. Carteret's and saw nothing missing or hurt (lines 66165–67). `pf097` “found” can imply a first discovery; describe the landing/check instead. A question at `pf087` may still ask whether unloading will go well, but should not conceal that he already saw the goods guarded. |
| `pf071` | At lines 66004–12 Pepys proposed summoning workers, Sir W. Pen went to arrange it, and Pepys wrote Coventry about permission to pull down houses. “He was contacting workers” blurs those separate actions; specify his proposal and Pen's mission. |
| `pf036` | Lines 65884–87 say Mrs Batelier came during dinner to inquire about two relations whose houses were burned. The diary does not explicitly record her learning that news **at the table**. Keep this as a diarist report, without making an invented exchange sound witnessed. |

Other sampled risk boundaries are handled well: `pf011` marks Jane's 300-house report as hearsay (lines 65804–06); `pf016–pf017` attribute the Pudding Lane origin to a Tower officer (65812–15); `pf065–pf068` keep Batten's first wine pit separate from Pepys and Pen's second pit (65997–66002); `pf075` limits demolition's effect to where it was done (66023–26); `pf083–pf086` limit survival to Pepys's house and office (66085–93); and `pf100` leaves the cheese's later fate unknown within these five entries. The title's “why” is supported only as an inference from urgent evacuation and the approaching fire, not by Pepys stating a motive or a special value for the cheese.

## Visual prompt check

Reviewed all **101 image prompts** against their paired spoken lines and the primary source; `pf102` is the outro card. The project uses `format: drama`, `look: {"preset":"cute-mystery"}` and the required continuous music settings. Images are illustrative. The following prompts materially risk saying something different from the narration or diary:

| Scene | Prompt mismatch and repair |
| --- | --- |
| `pf025` | A ruler **hands an unlettered message** to Pepys. The diary records the king verbally commanding him to tell the mayor (lines 65839–44). Show the king speaking or gesturing, without a physical royal note. |
| `pf045` | The prompt stacks **account books beside a locked chest in the cellar**. Pepys put money and iron chests in the cellar, while gold bags, chief account papers and tallies went to the office or a separate box (lines 65944–50). Show the cellar chest only, or clearly separate the office papers. |
| `pf056` | The prompt has a person **pressing a box through** the postern. Pepys says there was “no passing with any thing through the postern” because of the crowd (lines 65970–74). Show the box blocked at the narrow gate. |
| `pf087–pf088` | `pf087` visually places Pepys **on the church tower** one line before `pf088` narrates him climbing it. Move the tower view to `pf088`; make `pf087` match the revised spoken question. |
| `pf095` | “Sweeping water ... **toward a small fire**” repeats the unsupported destination in the narration (lines 66147–48). Show women working in street gutters without specifying where the water goes. |

Lower priority: `pf014` says a familiar **riverside** house, while the spoken line and diary locate the acquaintance's house **on London Bridge** (lines 65809–18); naming the bridge in the prompt will keep the geography clear. `pf101` shows a present-day reader indoors while the spoken invitation places the viewer in the historical yard; consider a yard image for a closer match. Other prompts omit people or objects to keep one clear subject, without contradicting spoken facts.

## Length and production boundary

The authored timeline uses 250 spoken units per minute plus pauses: first chapter **31.0 s**, narration body through `pf101` **525.9 s (8:45.9)**, and the full file **532.8 s (8:52.8)**. The first chapter has three explicit questions (`pf003–pf005`) and is under a 45-second opening. There is little margin on the eight-minute body floor: at 275 units/minute the same body is **487.5 s (8:07.5)**; at 300 it is **453.8 s (7:33.8)**. Add enough source-backed speech to keep the measured TTS body over 8:00; about 132 additional spoken units would cover the 300-unit/minute estimate if other lines stay unchanged. Do not treat the lint estimate as measured speech duration.

**Gate:** Script/source/visual review is not yet passed. Revise the cited lines and prompts, regenerate `script.md`, then obtain a fresh blind narrative review bound to the new hash and repeat source/visual checks for changed scenes before paid narration or artwork.
