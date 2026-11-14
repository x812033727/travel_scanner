# Curio S38 R5 post-seal Pepys, claims, and prompt audit

The fresh narrative seal is `/tmp/curio_s38_r5_fresh_blind_seal.md`, written before this audit. I did not open prior S38 reviews or edit author files or media.

## Integrity and coverage

- Script SHA-256: `e7eca53fdb4d6fbae4c4454fc652bb33bd00ca1156f5e30e9fada26413a63cd5`.
- Claims SHA-256: `2c0041720122040c94782054024e82f6dcf6da352e10986d1cdc71c93c594bb1`.
- Video JSON SHA-256: `cafb69b501d7f0d41d09d90c8650a2f7198ffb5388c57beacf15a5a88f2994ec`.
- The fixed full `4200.txt` source at `/tmp/curio-s38-pepys-4200.txt` matches the research SHA-256 `3cd43a3c39ee72eb9c4a3657f1fcb1723afba291cedac176c65a39289483be5d`. I reopened and read its continuous 2–6 September 1666 entries, lines 65795–66175, keeping the editor's bracketed notes distinct from the diary proper.
- Complete exact-text coverage: 112 sequential script IDs; 112 sequential claims rows; 112 sequential video scenes; 111 `shot` scenes with nonempty prompts and `visual: still`; one outro. All claim and video line texts match script line texts. No missing/duplicate ID or multi-line scene.

## Source verdict

**Pass for historical claims and their assigned diary ranges.** The narration preserves Pepys's key witness boundaries: Jane *heard* of 300 houses [pf011–pf012; source lines 65804–65806]; the Tower lieutenant *told* him the baker-house origin [pf016–pf017; 65813–65815]; he saw Michell's house burned only from the boat [pf019; 65816–65819]; and he says `nothing missed I could see, or hurt`, which the narration renders as a limited visual check [pf108; 66166–66167]. The cheese size, price, and later retrieval are not invented [pf073, pf110; 66000–66002].

Four requested revision points pass precisely:

| Narration | Fixed diary evidence | Finding |
|---|---|---|
| [pf040] Bridge upstream and downstream | Lines 65897–65907 say the fire had spread `both below and above` the bridge; the river context makes these downstream/upstream. | Pass. |
| [pf069] Office papers in first pit | Lines 65997–66002: Batten digs a pit for his wine; Pepys then places office papers in that pit; he and Pen dig `another` in the evening. | Pass. |
| [pf077] Letter seeking permission, no reply | Lines 66004–66012: Pepys writes to Coventry about permission to pull down houses and `received no answer`. | Pass. |
| [pf085] Boat downstream | Lines 66072–66083 say Pepys takes wife and gold `down by ... boat to Woolwich`; Woolwich lies downstream of central London. | Pass. |

The two-pit sequence, Pen's workers and local firebreak, 5 September return past watched goods, and 6 September unloading all agree with diary lines 65997–66012, 66020–66026, 66083–66093, and 66166–66170 respectively.

## Visual prompt verdict

I reviewed all 111 still prompts against their lines and the diary. **No clear historical contradiction blocks the prompt set.** The important revised scenes are sound: [pf069] places blank office papers by Batten's wine in the first garden pit; [pf077] shows a writer waiting by an outgoing letter without fabricating a reply; [pf089] shows the watched goods still on a boat; and [pf107] shows unloading later.

Two prompts are weaker than their narration but do not assert a false event:

- [pf040] says only `flames farther along a city waterfront`, so the image request does not explicitly ask for flames on *both* sides of London Bridge. A bridge-centered wide view would make the corrected fact visible.
- [pf085] requests one writer boarding a Thames boat with a closed chest; it does not include his wife or a downstream orientation. A downstream departure with wife and secured money would better represent the spoken line. The source says he took gold, without specifying a chest at this departure, so a neutral secured bundle would be more exact.

These are visual specificity notes. The frozen R5's remaining blockers are the two **blind narrative** failures documented in the separate seal: the same-day backward jump [pf075] and repeated house-survival fact [pf094]. No source or still-prompt blocker was found beyond them. Only prompts, not generated image files or a finished MP4, were audited.
