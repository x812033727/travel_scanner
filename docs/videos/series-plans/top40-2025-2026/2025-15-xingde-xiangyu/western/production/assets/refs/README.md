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
