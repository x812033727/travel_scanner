# A01 r47 independent narrative reader A

- Reviewer: `a01_r46_reader_a`, returning as independent reader A; no manuscript authorship. This is a successor reread by the same reader, not a claim of a fresh blind session.
- Reviewed package: `docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/A01-editorial-candidate-20261019-r47`.
- Reviewed manifest SHA256: `323dc77c5ec678ef38c35204eb7865d46c8ca612b5e82f0a6083ddf70c59a24e`; read back from the local file and matched the assigned digest.
- Scope: **offline narrative only**. Read the complete frozen `candidate/script.md` and `candidate/video.json` before examining validation metadata. No authored revision notes, delta, or other reader's report were used to decide the result.
- Rules: current repository `AGENTS.md`, `brand-story` and `youtube-video` skills, `references/story.md`, and relevant `references/script-writing.md` sections already read for this assignment; the actual `NARRATIVE_PANEL` contract and `TIGHT_CADENCE` were loaded again from `tools/video/core/narrative.mjs`.
- Owner direction: a single factual Rollaboard story. The explicit A01 actual narration-body target remains **420–480 seconds**. This review does not grant duration approval or substitute estimates for TTS measurement.
- Verified candidate structure: 50 scenes, 52 narration lines, 54 referenced claim IDs, and 8 loop rows.

## Result

**Narrative PASS: 13/13 true, including all 12/12 required true.** The advisory `chapters_are_events` is true. The three P2 issues from reader A's r46 review are resolved. **No remaining or newly established P1/P2 narrative issue** was found in this reread.

This result covers the narration's structure and clarity. It is not historical source verification, audio QA, visual QA, a host-worker review receipt, final-video acceptance, or authorization for paid production. The package's `duration_gate_passed: false` remains valid and unchanged.

## All 13 panel answers

The IDs and boolean semantics follow the current `NARRATIVE_PANEL`; `chapters_are_events` is the only non-required question. Each quotation is an actual narration line from this r47 `candidate/video.json`.

```json
{
  "answers": [
    {
      "id": "scene_first",
      "yes": true,
      "evidence": "[r44l001] 一九九三年，記者的 Travelpro Rollaboard 放不進座位下，也塞不進頭頂櫃。這只會滾的登機箱，為什麼到了機艙就卡住？"
    },
    {
      "id": "no_spoiler",
      "yes": true,
      "evidence": "[r44l001] 一九九三年，記者的 Travelpro Rollaboard 放不進座位下，也塞不進頭頂櫃。這只會滾的登機箱，為什麼到了機艙就卡住？"
    },
    {
      "id": "one_line",
      "yes": true,
      "evidence": "[r44l029] 到九三年，記者回看早期市場：這類輪子登機箱原本只有 Travelpro 製造，而且靠郵購販售。"
    },
    {
      "id": "no_toc",
      "yes": true,
      "evidence": "[r44l036] 這次 Dash 試了四家主要品牌的輪子登機箱，Travelpro Rollaboard 也在其中。她不只在地面拉，還把箱子帶上飛機試。"
    },
    {
      "id": "chapters_link",
      "yes": true,
      "evidence": "[r44l043] Dash 在報導裡說，當時這一類內建輪箱通常過得了多數窄走道；舊輪具拆開、摺起的動作，可以省下。"
    },
    {
      "id": "open_loops",
      "yes": true,
      "evidence": "[r44l035] 她也記得，等前面的旅客收好外套時，仍得扛著行李。到了這次測試，輪箱遇到路緣和樓梯，又會怎樣？"
    },
    {
      "id": "payoffs",
      "yes": true,
      "evidence": "[r44l048] 她只好把外袋多放的東西拿出來。這回，箱子才終於能收好。"
    },
    {
      "id": "no_recap",
      "yes": true,
      "evidence": "[r44l044] 回到開頭那次收納失敗：Dash 的 Travelpro，座位下和頭頂櫃都放不進去。"
    },
    {
      "id": "chapters_are_events",
      "yes": true,
      "evidence": "[r44l021] 先注意到成品的，是 Plath 身邊的其他機師。有人看他拉著箱子走，直接請他也做一只。（章名：機組員把它拉出車庫）"
    },
    {
      "id": "outro_no_next",
      "yes": true,
      "evidence": "[r44out2] 喜歡這種有來源的日用品故事，歡迎訂閱。"
    },
    {
      "id": "opening_hooks",
      "yes": true,
      "evidence": "[r44l005] 到了一九九三年，一位記者把 Travelpro Rollaboard 拉向陡路緣；樓梯也是要過的一關。"
    },
    {
      "id": "one_thread",
      "yes": true,
      "evidence": "[r44l018] 這次不用另外拖一台推車。輪子、拉桿和放衣物的箱身，在同一件行李上。"
    },
    {
      "id": "no_detour",
      "yes": true,
      "evidence": "[r44l045] 走道寬度和收納空間，考驗的是不同的尺寸。她的箱子，究竟在哪裡多出了體積？"
    }
  ]
}
```

The positive `no_recap` answer does not mean every object is named only once. The screw-fastened assembly is identified again as its physical state becomes the obstacle in the security exchange, while the integrated product is kept distinct. Those references advance the action or prevent object confusion. The long-delayed return to the opening fit incident is now an explicit callback and immediately advances to a new cause. There is no second closing summary.

The callback “回到開頭那次收納失敗” at `r44l044` is not a table of contents: it identifies a concrete unresolved event, then `r44l045`–`r44l048` supply its explanation and resolution. It is also not the chapter's first line; the new chapter starts with the cabin-aisle consequence at `r44l043`.

## Recheck of reader A's three r46 P2 findings

| r46 finding | r47 evidence | Decision |
| --- | --- | --- |
| Opening reveals the successful removal remedy; later fit question pretends its outcome is unknown | `r44l001` now asks why the case gets stuck without mentioning removal or successful stowage. `r44l044` recalls the known failure; `r44l045` asks where the extra volume came from. `r44l046`–`r44l048` give the outside-pocket cause and remedy for the first time. | Resolved. The mystery is its cause, not whether the already-described failure occurred. |
| Last chapter opens with a zipper diversion after a size cliffhanger | `r44l041` now raises the zipper question during packing; `r44l042` answers it in the same chapter and ends with cabin space. The new final chapter begins at `r44l043`, addressing narrow aisles, then reaches storage. | Resolved. The chapter boundary now advances the obstacle just raised. |
| Zipper fact and ground-versus-storage conclusion repeat | `r44l047` contains the new outward bulge and final-opinion question, without repeating the zipper verdict. The former `r44l050` summary is absent. `r44l048` resolves the fit failure; `r44l049` adds Dash's preference, followed by the viewer question and CTA. | Resolved. The close retains new information and stops. |

## Cadence, hooks, and payoff quality

Read-only recomputation with `estimateTimeline()` and `narrativeProblems(..., {cadence: TIGHT_CADENCE})` gives **0 errors and 0 warnings**. The standard estimated timeline totals 466.0 seconds before final branding; the estimated opening is 50.9 seconds. These figures are used only to locate the written beats. They do not prove actual spoken timing.

I find no meaningful-hook gap exceeding 45 seconds on that paper timeline. The sequence includes actual changes in obstacle or information: the screw-fixed case confronts the guard; the later integrated product removes the separate trolley; crew interest becomes orders and greater production; mail order explains traveler access; Dash tests the ground, packing, and cabin constraints. Questions are tied to those changes rather than added as empty punctuation.

| Setup | Payoff in this script | New information supplied |
| --- | --- | --- |
| `r44l003` / `r44l011`: screw-fastened case at security | `r44l012`–`r44l013` | Demand to detach, inability to detach, and the guard's brief reply; the actual passage method remains unreported. |
| `r44l004`: colleagues notice the later case | `r44l021` | They ask Plath to make one, beyond merely looking at it. |
| `r44l005` / `r44l035`: curb and stairs | `r44l037` | The reported ground-test outcome. |
| `r44l020`: first everyday users | `r44l021`–`r44l023` | Other pilots and flight crew adopt the product. |
| `r44l023`: garage capacity | `r44l024` | Production moves to a warehouse. |
| `r44l028`: route to travelers | `r44l029` | Early mail-order sales. |
| `r44l001`, recalled at `r44l044`–`r44l045`: unexplained cabin fit failure | `r44l046`–`r44l048` | Extra clothes and books in expandable outside storage increase its volume; removing them enables stowage. |
| `r44l047`: final opinion despite that failure | `r44l049` | Travelpro remains among Dash's preferred cases. |

The opening has three later moments after its first incident (`r44l003`, `r44l004`, `r44l005`), with the relevant outcomes withheld. The main opening problem also has its own delayed cause and remedy.

The new zipper question is modest, but it now follows a fully packed case and receives the recorded answer immediately. I do not count it as an unsupported major reversal or a filler problem. Chapter endings are not all the same rhetorical question, and the script does not repeatedly say “還記得”. The ending's final preference adds a consequence after the physical solution, rather than replaying the journey.

## One line across three distinct cases and periods

The central line is the handling problem: how to carry a case through an airport without a separate trolley, and what still prevents the integrated commercial case from fitting onboard. It remains the same problem when the narration moves from Plath to Dash.

- `r44l002`, `r44l003`, and `r44l008` retain the **undated** checkpoint anecdote and identify the hard case plus screw-fastened external trolley. The guard's “好” is not presented as a known clearance procedure (`r44l013`).
- `r44l004` identifies a **different later integrated case**. `r44l015` preserves the missing modification history, and `r44l016` shifts explicitly to the separate product record. The narration does not invent a continuous transformation of the screw-on cart sample.
- `r44l025` identifies **1989 as the patent filing point**; it does not date the original anecdote. The record's design concerns at `r44l026` continue the storage question rather than introduce another product story.
- `r44l001`–`r44l002`, `r44l029`, and `r44l031` distinguish the **1993 reporter and commercial product**. `r44l043` remains a category-level aisle statement; `r44l044`–`r44l049` describe Dash's particular Travelpro failure, remedy, and preference.

These are observations about the narration's attribution and distinctions. No new historical-source verification was performed, and the admitted gaps should not be converted into dates, causal links, or invented physical sequences.

## Duration remains a separate open gate

`validation.json` records actual narration-body target `[420, 480]`, `actual_tts_duration_not_measured: true`, and `duration_gate_passed: false`; `manifest.json` also retains `duration_gate_passed: false`.

The recorded body estimates are 450.4 seconds at 250 CPM, 414.1 at 275 CPM, and 383.0 at 300 CPM. The latter two fall below the actual target's lower bound, and none is a TTS measurement. **This narrative pass does not clear that hold.** It also does not recommend slower delivery, longer pauses, or recap material to fill time. Actual timing and the eventual spoken hook intervals still require their designated production checks.

Only this independent report was authored. No older r46 file, frozen r47 candidate output, manifest, task record, runtime state, PR, or production approval was changed.
