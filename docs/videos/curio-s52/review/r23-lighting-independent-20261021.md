# S52 R23 independent visual/light audit — HOLD

2026-10-21 UTC. **HOLD remaining paid art.** The eight R23 light edits are sound and byte-exact, but the full prompt scan found one other material location contradiction in an unchanged shot. This receipt does not withdraw the R22 native KEEP decisions for `s52001` and `s52002`.

## R23 change verification

- Current `video.json` SHA-256 is `86f9b98339a6e29b73446709ebb923f323e77277076a698c718952df725acd81`, matching the structured diff. Each of its eight new prompt strings occurs exactly once at the stated scene ID. Replacing those eight strings with their recorded old values restores R22 SHA-256 `3e380aa29543a868dd643f588834e188d48c481da4c36e0a738a17968af9ad41` byte for byte. Recursive comparison of parsed files finds exactly eight changed leaves: `scenes[5,20,21,26,40,51,60,81].data.prompt` (`s52006`, `s52020`, `s52021`, `s52026`, `s52056`, `s52071`, `s52081`, `s52100`). All other JSON, including `s52001` and `s52002` prompts and cameras, is unchanged across the exact R22 reverse.
- Cook's June 3 entry at local source lines 5963–5975 says there was **not a cloud the whole day**. The two transit-day replacements (`s52020`, `s52100`) correctly move from overcast light to shade/reflected light under a clear sky. `s52021` and `s52081` remove impossible window light at open canvas; `s52006`, `s52026`, and `s52071` use coastal light outdoors; `s52056` uses ambient light beneath the shore canopy. Each keeps the scene's main subject and action.

## Full prompt spot check

I scanned all **113 scenes** (110 nonempty shot prompts, two `big` cards, and one outro). No remaining prompt explicitly puts overcast weather on June 3. The remaining shore `overcast` prompts are dated April, before June 3, or belong to the returning-boat account on June 4; archive/reading-table weather is not a claim about the transit sky. Remaining `window light` prompts are in archive/reading settings or a generic research table, without a specified outdoor location. Three prompts (`s52055`, `s52057`, `s52070`) show a two-person teaching or handoff action, but name one primary actor and one recipient; they do not set two competing protagonists. Check these frames directly when generated.

**Blocking unchanged prompt — `s52014`:** “Wide shot **in an eighteenth-century archive room** by day, one anonymous dock worker carries a plain crate **beside a ship**, late afternoon light.” Its spoken line says the Society learned on April 3 that the ship had been found. A full ship beside a dock worker inside an archive room is an incoherent place for that event and risks paying for a misleading historical frame. Clarify whether the scene is indoors with a small model or outdoors beside the vessel before batch art. This is separate from the eight correct R23 light changes; I made no prompt edit.

At review time `/workspace/.video-work/curio-s52/STOP` still existed as an empty regular file. The ledger remained **US$0.0675**, 5 images, 5 judge calls, zero reservations, SHA-256 `f5df12777013c85e0e40f079f42864b3b5c66a8754453ed68c447bb63737a301`; the stated episode ceiling remains **US$4.46**. I did not remove STOP or call a paid API.
