# Locked reference pictures (season one)

Chosen by the owner on 2026-11-10 ("照內建的": the default picks from the screen test). JPEG copies (quality 2) of the Colab
outputs; the original PNG hashes, seeds and prompts are in `../../screen-test/runs/` (r1/r2 manifests and progress files).
Use these as `<Picture N>` references for Ref2VA clips and as image 1 for any new costume look (`latent: image1`, change only the costume).

| File | Source take | Seed | Original PNG sha256 |
| --- | --- | --- | --- |
| nora-portrait.jpg | r3 nora-portrait-fix-b (exactly one change on the 2026-11-10 pick; see the screen-test README 〈定妝照修圖 r3〉) | 713001 | be2e49a63ee5fd178da42dbd05a23429a3c5288e99083a77ca69fe662660e62c |
| elias-portrait.jpg | r1 elias-a | 711002 | 88706d26c0136dc81ce2eb6c31248534ba7e460d5aa9e2a7ee3b1e4fdf2078c8 |
| grant-portrait.jpg | r3 grant-portrait-fix-b (exactly one change on the 2026-11-10 pick; see the screen-test README 〈定妝照修圖 r3〉) | 713005 | dde046a36af4438f155cd1532e82e9bf67c6eedcc37445ab163223da8aa4fc58 |
| peg-portrait.jpg | r1 peg-a | 711006 | 13787db056b7f5d22459d385d1bb582ad3309440e3b3035a3e96b4f281403b17 |
| nora-work.jpg | r3 nora-work-fix-a (exactly one change on the 2026-11-10 pick; see the screen-test README 〈定妝照修圖 r3〉) | 713002 | c31ef29a130671deceb8bbd4d90d4ce3b37d99d7c0b40ac1fd73775a12d565bb |
| elias-furnace.jpg | r2 elias-furnace-a (on elias-a) | 712001 | 427925000c7cda634d77b7dfe8609567461201c78f636c31fed6f7f300f0469a |
| peg-coat.jpg | r2 peg-coat-a (on peg-a) | 712002 | 6800ce245a8afc90f464a9750c65d8ce12aab14f0414bd54eb329e184aa8c3ff |
| set-glass-house-living.jpg | r1 set-glass-house-living-a | 711008 | 382f5b1778d47c6fd4eb20950701ca835a1b958898548bf7886c4f8d8b6aeb70 |
| set-glass-house-ext.jpg | r1 set-glass-house-ext-a | 711009 | 07b03bdc70bf049adb056c1b757ac0e69c931ee735ee6933db20d41476957e1d |
| set-remelt.jpg | r1 set-remelt-a | 711010 | 28680f0625c6ea4cfae23530e24aaeaacd990d8cdd4823f6d0f6f127d6750471 |
| set-glass-house-bedroom-am.jpg | vpilot set-bedroom-v-a (vertical 1088×1920, the 2026-11-10 vertical pilot) | 721000 | 0f1db9515fb2567361cd50855e5be93f83b1c1f7a8444888ec6fa7b90fc5e122 |

2026-11-12: `nora-portrait`, `nora-work` (small red marks removed) and `grant-portrait` (closed-mouth smile removed) replaced by the owner's picks from round r3; the r3 manifest is built by `../../screen-test/build.py r3`.

`SHA256SUMS` covers the JPEGs in this folder.

## First batch (episodes 1–10, 2026-11-12)

Picked by Claude on the owner's 2026-11-12 instruction (「參考圖 你建議決定」); the manifests are built by `../../screen-test/art.py`.

| File | Source take | Seed | Original PNG sha256 |
| --- | --- | --- | --- |
| cole-portrait.jpg | a12 cole-a — Cole | 714000 | 6993dfcb1245f737090cc0edc645da5b5a93a62dc8111aeaacd7a1f5c0e37b91 |
| nora-night-coat.jpg | a12 nora-night-coat-b — Nora night-coat full body (ep. 2); hair dry in the picture, the clips add the rain | 714003 | d07a3fe7071e4826455a3c252d55347cb92d27eeb78f2e30d75bf4c452526ed7 |
| nurse-kim-portrait.jpg | a12 nurse-kim-a — Nurse Kim (take b looked 45) | 714008 | bb1dd1dc8f2cb229be8bd355a70c405ad5120b248c886b66f7062f07a4e07706 |
| grant-rain.jpg | a12 grant-rain-a — Grant rain look; the picture barely differs from the portrait, the clips add the rain | 714010 | 10eb07f55d59244638dc5afaf1b72d1ad1b3c07f0b4beaf6388fd049fc0d27d0 |
| on-call-doctor-portrait.jpg | a12 on-call-doctor-a — on-call doctor (take b has lettering) | 714012 | 41be05ea2198343bb5cdca2d438d27ec7597e19487f8b21c5d7e5f190d803c56 |
| nora-discharge.jpg | a12 nora-discharge-b — Nora discharge full body (eps. 6–10) | 714015 | 3c0a404763875145ff3bbc1a47b7237ab6d19fd8e2ce9deba5e3ffe7ef09eed4 |
| fisk-portrait.jpg | a12 fisk-b — Fisk (take a too tight, a T-shirt under the suit) | 714017 | 3c3f3368828981caa48d9713817dc9ff8033f6bb5de9764578555a553fe7cfa8 |
| set-glass-house-bedroom-bed-sconce.jpg | s1 set-glass-house-bedroom-bed-sconce-v-a — #2 bedroom at night, wall lamp on (edit of the morning bedroom; one seed) | 740020 | 63ecb3f283ab9f1a6156457cf75beb68bceed2f9d77efae4f96a575d6a50f515 |
| set-glass-house-living-liv-day.jpg | s1 set-glass-house-living-liv-day-v-a — #5 living room, overcast morning, sofa left and table right (take b has grey borders) | 740050 | 0b590d2b6fb553b12c8079b057b93b50c4f89af12150639cf5285020186fa714 |
| set-glass-house-nursery-nur-day.jpg | s1 set-glass-house-nursery-nur-day-v-b — #9 nursery by day, crib left, rocker with the basket right | 740091 | a5c29e0841b56cd3d8fe78c0a5794b245dc009c28717aacb5ecb881d5b822fb0 |
| set-glass-house-door-in-day.jpg | s1 set-glass-house-door-door-in-day-v-a — #7 front door from the entry, afternoon drizzle; flaw: the steps and mat read as on the camera side, so frame it tighter than the steps (take b opens outward) | 740070 | a70087aab7912dd83c681ac60acea5c810abf0c3775cbef7d885b27f9c941e33 |
| set-glass-house-door-out-rain.jpg | s1 set-glass-house-door-door-out-rain-v-a — #12 front of the house, night rain, lamppost right, drive curving lower left; flaw: the interior is lit (written dark), the clip prompt keeps it dark | 740120 | 82c9dd261fd268ce3107fb43132c7b9bd030c2cba49b87fe88198b26f01f7e62 |
| set-ambulance.jpg | s1 set-ambulance-amb-v-a — #14 ambulance from the stretcher's head end (take b side-on with marks) | 740140 | b29a97a96f4fc068887f3b7fdbbb8adfd51b8a3ebadbdb8d3de20ca7e552b9fe |
| set-hospital-room-night.jpg | s2 set-hospital-room-room-night-v-a — #16 hospital room at night: bed head on the left wall, open door on the right (take b has no door) | 740160 | d2e738fbc99da4eb18ea67c8dc21e3a6e849c197e9bc479a0448fb2c213b14da |
| set-glass-house-living-liv-gold-a.jpg | s2 set-glass-house-living-liv-gold-a-v-a — #21 living room at sunset with the two ladders (take b has none) | 740210 | e4efc2d1faaee2a0270f8a6cb8e50927054282cd9def4c3c9a84e4a96202df18 |
| set-hallway.jpg | s2 set-hallway-hall-v-b — #15 hospital corridor, bench at the far end on the left; a small wall sign on the right stays out of frame (take a: a red digit display) | 740151 | a71504f4c667355a2dcdbd677fc5b320b462b4bb5b79572679b80478b0889fd0 |
| set-grant-car-interior-day.jpg | s2 set-grant-car-interior-gcar-day-v-b — #19 Grant's back seat with the centre console, firs left and sea right | 740191 | 70385a364d42e147cd296db0cb1b3e9ec4b9f80358c6050b5b3fbddbeac337b9 |
| set-glass-house-door-out-gold.jpg | s2 set-glass-house-door-door-out-gold-v-a — #20 front of the house at sunset, lamppost on the right (take b opens outward) | 740200 | e28dfe586636e2e9165ca4f6d41aa2a9955b1352f2582279e3e271612d594bfb |
| set-glass-house-door-in-gold.jpg | s2 set-glass-house-door-door-in-gold-v-a — #24 front door from inside at sunset, standing open inward (take b from outside) | 740240 | 3680a365cc77d5d504ef314d96241af185ea3df2f9da6b77eb0e87fc4d6524e3 |
| set-motel-room-night.jpg | s3 set-motel-room-mroom-night-v-a — #32 motel room at night: headboards on the right wall, red neon in the curtain gap, bathroom door half open | 740320 | 0f4e58cf6b5ef2913b26ee0afe384a4fe2fdacf118d2b74eadb01c2a0ccea8c0 |
| set-glass-house-study.jpg | s3 set-glass-house-study-study-v-a — #27 study at sunset, shelves on the left wall with grey folders on the bottom shelf | 740270 | b8c60740a261fa5a9905b3698fa5f15334a01b0e69a0d59cd94b3619ecd84468 |
| set-coastal-drive.jpg | s3 set-coastal-drive-drive-v-a — #28 the drive down the bluff at sunset, guardrail on the sea side, the house small at the top | 740280 | 1c46d6f93101b6318071fd7ae6822eaa287a5d0ca6b6479d6d8342d517177307 |
| set-grant-car-interior-gold.jpg | s3 set-grant-car-interior-gcar-gold-v-b — #29 Grant's car forward through the windshield toward the house (take a looks back at a second row); the sunroof also shows the house | 740291 | 7c7547b138a83a29b733117194433e1dfade6e8c05bee3bb598d3793325d1eb4 |
| set-bus-stop.jpg | s3 set-bus-stop-bus-v-a — #30 harbor bus shelter at dusk, blank route panel, cranes with red lights | 740300 | 78f8e3d36ed6698d2036b049b5d2d46b41d57d90f9ea088dd24b1baa6059e29f |
| prop-forever-no1.jpg | p1 prop-forever-no1-a — No. 1 vase with a forearm for scale (take b a wavy sculpture) | 760110 | 873b468958000d14bc0d40622112b5ae44f825e078286f7a1a61aa6201bca832 |
| prop-keepsake.jpg | p1 prop-keepsake-a — glass block, faint green, hand for scale; a hand-shaped shadow inside the glass, watch for it | 760030 | 822eb7bce701a9483d12882f38dae1eaa3f67ccc081fee393ce48c5fb4b0d9c2 |
| prop-knit-hat.jpg | p1 prop-knit-hat-a — half-knitted cream baby hat on two needles in Peg's hands (take b drew a sweater) | 760020 | e05b3ca9aa645313398d7a5c1d6f47c615c67f297742db5a9b42fe3ddc264736 |
| prop-nora-suitcase.jpg | p1 prop-nora-suitcase-b — navy soft-sided suitcase by her knee (take a hard-shell) | 760041 | f26ee9e2fa91fc2a18f49b4b4d0c0ae5cace83dd65dbf3a0c61a554a54ee303f |
| prop-peg-suitcase.jpg | p1 prop-peg-suitcase-a — old tan hard-shell suitcase (take b empty frame) | 760050 | a6121da9e3f41bac63a5cd05973f663f568c717b2be30fcf7522a00979df3da7 |
| prop-peg-ring.jpg | p2 prop-peg-ring-b — Peg's wedding ring on an older hand (both takes close) | 760261 | 8fec9fc0e0ee73c906bf99930aed48b4404d2486f781e98d46fbfbeeb255a18e |
| prop-ledger.jpg | p2 prop-ledger-b — small brown ledger with a pencil, in a hand for scale | 760081 | f49e9c1c57523b10c0d1e076b1ec7cbc236ba9e1e17d5d295caa0350e859782e |
| prop-camel-coat.jpg | p2 prop-camel-coat-b — camel coat with deep patch pockets over the sweater dress (eps 1-10); the model's face is not Nora: never pass it with a face in the shot, prefer the a5 nora-discharge-coat full body | 760251 | 12f7a43eb539ac0583bd835493df136c301203abd51d8d9446a62677be68f8bc |
