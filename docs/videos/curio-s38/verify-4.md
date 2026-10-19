# S38 R4 independent blind and source review

2026-10-19. This review is bound to [`script.md`](script.md) SHA-256 `62af2f7d762b082a1e6910df28a721fac6c14cb4d081f06516f48b5511cd1411`. I read that script alone and sealed the 13 yes/no answers and 13 independent comprehension answers in a message to the coordinating agent before opening any other S38 file. I had not read an earlier S38 iteration. Source, claims, prompts and the review rules were inspected only after the blind verdict was sealed.

## Blind narrative verdict

**13/13 yes**: all 12 required checks and the optional chapter-title check pass. This is the independent reader's verdict for this exact script, not a claim that a canonical `narrative --answers` receipt has been run. No narrative blocker was found.

| Check | Verdict | Script evidence |
| --- | --- | --- |
| `scene_first` | Yes | `pf001` starts in Pepys's London garden on September 4, with him and Sir William Pen digging the second pit. |
| `no_spoiler` | Yes | `pf003`–`pf005` ask how close the fire came, whether the house survived, and what became of the cheese without giving the results. |
| `one_line` | Yes | `pf006` explicitly returns two days to the fire's start; the later days move forward to the second pit and the fate of Pepys's home and goods. |
| `no_toc` | Yes | `pf023` has Pepys hurry to Whitehall as the next action; chapter changes do not announce a list or a plan for the video. |
| `chapters_link` | Yes | `pf064` asks what still cannot be moved, and the next chapter opens at `pf065` with the wine left in the yard. The other joins likewise follow a question or action: `pf022→pf023`, `pf039→pf040`, `pf051→pf052`, `pf082→pf083`, `pf102→pf103`. The `pf005→pf006` return is clearly dated as two days earlier. |
| `open_loops` | Yes | `pf022` asks who can stop the wind driven fire; later questions at `pf039`, `pf051`, `pf064`, `pf074`, `pf082` and `pf102` continue the cadence. |
| `payoffs` | Yes | `pf090` reveals that the house Pepys feared losing still stands; `pf110` answers the remaining cheese question with the diary's silence. |
| `no_recap` | Yes | `pf072` names “開場那塊起司” when the second pit is reached in sequence, adding the two pit context rather than replaying the opening. |
| `chapters_are_events` | Yes | Titles name actions or discoveries, including “九月四日，兩個土坑先後挖開” and “九月六日，佩皮斯帶人救火並卸下貨物”. |
| `outro_no_next` | Yes | `pf112` invites subscription without promising a next episode. |
| `opening_hooks` | Yes | `pf003`, `pf004` and `pf005` plant three distinct later answers after the garden scene. |
| `one_thread` | Yes | Pepys's attempts to protect his home and possessions carry the account from `pf001` through the September 6 unloading and `pf110`'s cheese boundary. |
| `no_detour` | Yes | The crowded receiving house at `pf055` and the workmen discussed at `pf075` directly affect the evacuation and whether his office survives. |

## Primary source and attribution

I downloaded the [pinned Pepys diary text](https://github.com/GITenberg/The-Diary-of-Samuel-Pepys---Complete_4200/blob/68fcf49f70ee793b989a6fd0464264d55beb4451/4200.txt#L65784-L66175) directly from GITenberg commit `68fcf49f70ee793b989a6fd0464264d55beb4451`. The full `4200.txt` SHA-256 is `3cd43a3c39ee72eb9c4a3657f1fcb1723afba291cedac176c65a39289483be5d`, matching [`research.md`](research.md). I checked the September 2–6 diary passages against the narration and [`claims.md`](claims.md), preserving Pepys's direct sight, secondhand reports and later editor insertions as separate kinds of evidence.

- **`pf014`, `pf017`, `pf022`:** At lines 65807–65818 Pepys sees the bridge end burning and worries about Michell and Sarah while atop the Tower; he sees Michell's house burned only after he takes a boat. At lines 65812–65815 the Tower lieutenant *tells him* the King's baker's house in Pudding Lane was the origin. Lines 65827–65835 say the high wind drove the fire into the City. The three lines and their prompts preserve those distinctions; no prompt shows Pepys witnessing ignition or confirming the familiar house from the Tower.
- **`pf055`:** Lines 65956–65964 put Pepys in Sir William Rider's crowded Bednall Green house among goods from several friends. The narration and receiving room prompt fit.
- **`pf075`:** Lines 66000–66011 put the second pit in the evening and then use “This afternoon” to look back to Pepys and Pen discussing the threatened office in the garden. `pf075` explicitly says “稍早那天下午”, so the narrated return does not turn that afternoon discussion into an event after the evening pit.
- **`pf107`–`pf108`:** Lines 66083–66085 say Pepys *saw his goods watched in lighters at Deptford* on September 5; lines 66165–66170 say he *landed* the goods at Sir George Carteret's on September 6 and could see none missing or hurt. `pf107`–`pf108` and their prompts put unloading and visual inspection on the latter day; they do not assert a full inventory.
- **Cheese and fire boundary:** Lines 65997–66002 distinguish Batten's first wine pit with Pepys's office papers from Pepys and Pen's second wine pit with Pepys's `Parmazan` cheese. Lines 66023–66026 and 66089–66093 support only local fire stops near Tower Street and Pepys's lane. The September 2–6 entries do not give the cheese's size, price or later retrieval, and the script makes no such claim.

## Manifest and visual gate

The script has **112 sequential, unique line IDs**. All **112** claim rows and **112** `video.json` scene lines match the script exactly in ID, order and narration text; every scene has one line. The manifest has **111 `shot` scenes with prompts** and **one `outro`**; its eight chapter starts and all loop setup/payoff IDs are in order. I read all 111 prompts against their paired narration and the diary boundary. The flagged source points above have suitable scenes: `pf014` shows worry from the Tower, `pf017` no ignition scene, `pf022` wind driven smoke, `pf055` a crowded receiving room, `pf075` an afternoon garden discussion, and `pf107`–`pf108` unloading and inspection at Deptford. No blocking source, line pairing or prompt contradiction found.

This review covers the frozen script, claims, primary text and static prompts. It makes no claim about recorded speech, rendered pictures or measured duration. No script or media was changed.
