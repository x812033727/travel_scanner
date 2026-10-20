# S43 R5 — independent source and written visual audit

**Verdict: HOLD pending precise wording/citation fixes.** Frozen candidate: `video.json` SHA-256 `2b15522f7d48afba6eae5f6487136d0ed85debd8b419cff22f4d209f87eede8b`; `script.md` `1bf9783c75ca9c93db3f1302b89b2e1bfaa3248321745beca6812039e76f5dac`; `claims.md` `ef4c28e9e11f16170fff83792a1c1894b611d87be71d750618d8469647458655`; `research.md` `d3a6b472d29e4266e1c44b51b0aba9965f3e6ecea31f52a00ae314ef2d906f9e`.

Pinned local witness SHA-256s match `research.md`: L `/tmp/s43-life-letters.txt` `c795bf75dde25565205b8d3ec696e92cebc9019da7dd28d01936fa15bc334dec`; A `/tmp/s43-darwin-auto.txt` `eb2c4e03f7eff1ac5c6fdaa865099e8238df712d04e820c24d7768f6961cde96`; V `/tmp/s43-beagle.txt` `24b8d915eb5f61c091ee66403096bb3a950e3c0cb310caf086b6be0cc86781f1`. The 92 shot IDs/order/narration strings match exactly across `video.json`, `script.md`, and `claims.md`; all 105 claim citations resolve to the expected fixed commits and valid source lines (88 L, 14 A, 3 V). The three outro lines match video/script and are bounded in `claims.md`.

## Fixes

1. **`dn015` — Henslow did not say “同住”.** L5639–43 says Fitz-Roy sought a companion who was also a gentleman, not a person to share his cabin. Darwin later reports Fitz-Roy's cabin offer at L5951–53 (`dn065`). `dn015` says `亨斯洛說，菲茨羅伊也希望找到能與自己同住的紳士同伴`; change to `能在船上作伴的紳士` or equivalent. Its `claims.md` boundary already says the initial request did not arrange shared quarters.

2. **`dn077c`, plus `claims.md` and `research.md` 6b — “attached compass” is too specific.** L6231–35 reads `a good telescope, with compass, 5 pounds`. It records a telescope with compass in a purchase list but does not establish that the compass was physically attached/integrated. `附羅盤的望遠鏡` risks that reading. Say `望遠鏡和羅盤` or `望遠鏡，連同羅盤` throughout. `dn077c` visual only shows a plain telescope, which is safe. L6115–17 supports the earlier “buy nothing until settled” contrast.

3. **`dn032` — wording of the Peacock letter is not preserved here.** L5712–24 directly shows Darwin declining in his Henslow letter. L5738–40 says only that he *wrote* to Peacock and asked Henslow to tell Fitz-Roy; it does not show what Darwin said to Peacock. `把拒絕寫進給亨斯洛與皮科克的信` overstates this witness. Say he declined in the Henslow letter and also said he wrote to Peacock.

4. **`dn014` — cite the small-vessel detail.** Its only range, L5620–57, has the companion requirement and ship but not the vessel's size. L5965–68 says `small vessel`; add that range or remove `小` from this scene.

## Supported chain and source limits

L5620–57 supports Henslow's August 24 recommendation and his *two-year forecast*, while L5661–5706 supports Peacock's proposed route and no-salary position; neither is final Admiralty routing. L5708–42 and L5746–65 support the first refusal and Darwin's own list of his father's objections. L5786–5810 identifies the editorially presented list and labels Wedgwood's reply `In C. Darwin's writing`. L5868–73 confirms Darwin said his father had changed his mind; the father's “common sense” line and uncle persuasion narrative are from the much later A871–89.

L5884–5928 supports Jenyns, Henslow's caution, and Wood. L5932–6006 supports the renewed abandonment after Wood received Fitz-Roy's letter, the unavailable friend, cabin offer, and cramped conditions; L6009–30 names Chester. The Fitz-Roy-to-Wood letter itself is absent, so `dn007/057–076` are rightly framed through Darwin's contemporary account. L6089–95 lists requested items, L6115–19 says he planned to buy nothing yet, L6121–25 records Fitz-Roy's *advice* to get a written freedom-to-leave assurance, and L6137–53 records an unitemized parcel, Beaufort's *reported* victuals-list remark, and Darwin's still unresolved South Sea condition.

**September 9 turn:** in the same letter L6220–27 says Darwin visited Fitz-Roy again and they drove about shopping; L6227–31 says `You may consider it settled that I go`, with an untoward-accident caveat. This is Darwin's own decision, not proof of the Admiralty's final South Sea instructions. A891–99 is Darwin's *1876 recollection* of later hearing the nose story, not a 1831 rejection record. V63–78 is later published thanks; V147–53 gives the ten-gun brig, two gale-driven returns and December 27, 1831 departure. A938–45 is Darwin's own retrospective career judgment. The outro correctly limits absence of a nose rejection to the cited contemporary letters.

## Written visual pass

All 92 shot prompts contain one adult actor or no human. The 22-year-old Darwin, other adults, and elderly memoir Darwin are appropriately separated. `dn006/010/018/038/077a` avoid unsupported two-person scenes; `dn007/057/058/076` do not show a readable missing captain letter; `dn074e` does not present a real surviving victuals ledger; `dn078–083` avoid a formal nose examination; the charts do not display an approved final route. Wooden sailing-ship interiors provide a period cue.

**Advisory:** V148 explicitly calls Beagle a ten-gun brig. Exterior prompts `dn027/086/087` use generic “small sailing vessel” / “small masted sailing ship”; add `1831 British naval brig` to reduce modern-yacht or wrong-rig generations. Current written prompts do not themselves depict a wrong vessel. Actual image fidelity awaits generation and inspection.

This was an independent local-source/text-prompt audit only. No site or media tools were called and no repository files were edited.
