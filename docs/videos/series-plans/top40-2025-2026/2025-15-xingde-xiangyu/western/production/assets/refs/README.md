# Locked reference pictures (season one)

Chosen by the owner on 2026-11-10 ("照內建的": the default picks from the screen test). JPEG copies (quality 2) of the Colab
outputs; the original PNG hashes, seeds and prompts are in `../../screen-test/runs/` (r1/r2 manifests and progress files).
Use these as `<Picture N>` references for Ref2VA clips and as image 1 for any new costume look (`latent: image1`, change only the costume).

| File | Source take | Seed | Original PNG sha256 |
| --- | --- | --- | --- |
| elias-portrait.jpg | r1 elias-a | 711002 | 88706d26c0136dc81ce2eb6c31248534ba7e460d5aa9e2a7ee3b1e4fdf2078c8 |
| peg-portrait.jpg | r1 peg-a | 711006 | 13787db056b7f5d22459d385d1bb582ad3309440e3b3035a3e96b4f281403b17 |
| nora-work.jpg | r3 nora-work-fix-a (exactly one change on the 2026-11-10 pick; see the screen-test README 〈定妝照修圖 r3〉) | 713002 | c31ef29a130671deceb8bbd4d90d4ce3b37d99d7c0b40ac1fd73775a12d565bb |
| elias-furnace.jpg | r2 elias-furnace-a (on elias-a) | 712001 | 427925000c7cda634d77b7dfe8609567461201c78f636c31fed6f7f300f0469a |
| set-glass-house-living.jpg | r1 set-glass-house-living-a | 711008 | 382f5b1778d47c6fd4eb20950701ca835a1b958898548bf7886c4f8d8b6aeb70 |
| set-glass-house-ext.jpg | r1 set-glass-house-ext-a | 711009 | 07b03bdc70bf049adb056c1b757ac0e69c931ee735ee6933db20d41476957e1d |
| set-remelt.jpg | r1 set-remelt-a | 711010 | 28680f0625c6ea4cfae23530e24aaeaacd990d8cdd4823f6d0f6f127d6750471 |

2026-11-12: `nora-portrait`, `nora-work` (small red marks removed) and `grant-portrait` (closed-mouth smile removed) replaced by the owner's picks from round r3; the r3 manifest is built by `../../screen-test/build.py r3`.

`SHA256SUMS` covers the JPEGs in this folder.

## First batch (episodes 1–10, 2026-11-12)

Picked by Claude on the owner's 2026-11-12 instruction (「參考圖 你建議決定」); the manifests are built by `../../screen-test/art.py`.

| File | Source take | Seed | Original PNG sha256 |
| --- | --- | --- | --- |
| cole-portrait.jpg | a12 cole-a — Cole | 714000 | 6993dfcb1245f737090cc0edc645da5b5a93a62dc8111aeaacd7a1f5c0e37b91 |
| nora-night-coat.jpg | a12 nora-night-coat-b — Nora night-coat full body (ep. 2); hair dry in the picture, the clips add the rain | 714003 | d07a3fe7071e4826455a3c252d55347cb92d27eeb78f2e30d75bf4c452526ed7 |
| on-call-doctor-portrait.jpg | a12 on-call-doctor-a — on-call doctor (take b has lettering) | 714012 | 41be05ea2198343bb5cdca2d438d27ec7597e19487f8b21c5d7e5f190d803c56 |
| nora-discharge.jpg | a12 nora-discharge-b — Nora discharge full body (eps. 6–10) | 714015 | 3c0a404763875145ff3bbc1a47b7237ab6d19fd8e2ce9deba5e3ffe7ef09eed4 |
| fisk-portrait.jpg | a12 fisk-b — Fisk (take a too tight, a T-shirt under the suit) | 714017 | 3c3f3368828981caa48d9713817dc9ff8033f6bb5de9764578555a553fe7cfa8 |
| set-glass-house-bedroom-bed-sconce.jpg | s1 set-glass-house-bedroom-bed-sconce-v-a — #2 bedroom at night, wall lamp on (edit of the morning bedroom; one seed) | 740020 | 63ecb3f283ab9f1a6156457cf75beb68bceed2f9d77efae4f96a575d6a50f515 |
| set-glass-house-living-liv-day.jpg | s1 set-glass-house-living-liv-day-v-a — #5 living room, overcast morning, sofa left and table right (take b has grey borders) | 740050 | 0b590d2b6fb553b12c8079b057b93b50c4f89af12150639cf5285020186fa714 |
| set-glass-house-door-out-rain.jpg | s1 set-glass-house-door-door-out-rain-v-a — #12 front of the house, night rain, lamppost right, drive curving lower left; flaw: the interior is lit (written dark), the clip prompt keeps it dark | 740120 | 82c9dd261fd268ce3107fb43132c7b9bd030c2cba49b87fe88198b26f01f7e62 |
| set-hospital-room-night.jpg | s2 set-hospital-room-room-night-v-a — #16 hospital room at night: bed head on the left wall, open door on the right (take b has no door) | 740160 | d2e738fbc99da4eb18ea67c8dc21e3a6e849c197e9bc479a0448fb2c213b14da |
| set-hallway.jpg | s2 set-hallway-hall-v-b — #15 hospital corridor, bench at the far end on the left; a small wall sign on the right stays out of frame (take a: a red digit display) | 740151 | a71504f4c667355a2dcdbd677fc5b320b462b4bb5b79572679b80478b0889fd0 |
| set-glass-house-study.jpg | s3 set-glass-house-study-study-v-a — #27 study at sunset, shelves on the left wall with grey folders on the bottom shelf | 740270 | b8c60740a261fa5a9905b3698fa5f15334a01b0e69a0d59cd94b3619ecd84468 |
| set-coastal-drive.jpg | s3 set-coastal-drive-drive-v-a — #28 the drive down the bluff at sunset, guardrail on the sea side, the house small at the top | 740280 | 1c46d6f93101b6318071fd7ae6822eaa287a5d0ca6b6479d6d8342d517177307 |
| set-grant-car-interior-gold.jpg | s3 set-grant-car-interior-gcar-gold-v-b — #29 Grant's car forward through the windshield toward the house (take a looks back at a second row); the sunroof also shows the house | 740291 | 7c7547b138a83a29b733117194433e1dfade6e8c05bee3bb598d3793325d1eb4 |
| prop-forever-no1.jpg | p1 prop-forever-no1-a — No. 1 vase with a forearm for scale (take b a wavy sculpture) | 760110 | 873b468958000d14bc0d40622112b5ae44f825e078286f7a1a61aa6201bca832 |
| prop-keepsake.jpg | p1 prop-keepsake-a — glass block, faint green, hand for scale; a hand-shaped shadow inside the glass, watch for it | 760030 | 822eb7bce701a9483d12882f38dae1eaa3f67ccc081fee393ce48c5fb4b0d9c2 |
| prop-knit-hat.jpg | p1 prop-knit-hat-a — half-knitted cream baby hat on two needles in Peg's hands (take b drew a sweater) | 760020 | e05b3ca9aa645313398d7a5c1d6f47c615c67f297742db5a9b42fe3ddc264736 |
| prop-nora-suitcase.jpg | p1 prop-nora-suitcase-b — navy soft-sided suitcase by her knee (take a hard-shell) | 760041 | f26ee9e2fa91fc2a18f49b4b4d0c0ae5cace83dd65dbf3a0c61a554a54ee303f |
| prop-peg-suitcase.jpg | p1 prop-peg-suitcase-a — old tan hard-shell suitcase (take b empty frame) | 760050 | a6121da9e3f41bac63a5cd05973f663f568c717b2be30fcf7522a00979df3da7 |
| prop-peg-ring.jpg | p2 prop-peg-ring-b — Peg's wedding ring on an older hand (both takes close) | 760261 | 8fec9fc0e0ee73c906bf99930aed48b4404d2486f781e98d46fbfbeeb255a18e |
| prop-ledger.jpg | p2 prop-ledger-b — small brown ledger with a pencil, in a hand for scale | 760081 | f49e9c1c57523b10c0d1e076b1ec7cbc236ba9e1e17d5d295caa0350e859782e |
| prop-camel-coat.jpg | p2 prop-camel-coat-b — camel coat with deep patch pockets over the sweater dress (eps 1-10); the model's face is not Nora: never pass it with a face in the shot, prefer the a5 nora-discharge-coat full body | 760251 | 12f7a43eb539ac0583bd835493df136c301203abd51d8d9446a62677be68f8bc |
| sienna-portrait.jpg | a4 sienna-b — Sienna (a4 redraw; the a12 run had drawn her full-length with no face; take a framed to the waist) | 714029 | 98f27623e5a445648f18f8eaf901f46d84f7ac0b051be5f13321c5de601df1a4 |
| deputy-portrait.jpg | a4 deputy-fix-b — deputy, lettering edited off (take a added glasses, a different face); watch the badge in drafts | 715003 | 3a06f8562edfbe2295238e66ec1c4ece6454e4a7c616bef52f7350f621128830 |
| set-motel-front-night.jpg | a4 mfront-night-fix-a — #31 motel office at night, the MOTEL neon sign edited off; the window shows the parking lot | 715100 | 7653738b9c56f64127c1d6d5228b7586bf943d3b3e150582a3e56947c1f55f4d |
| set-glass-house-bedroom-north-sconce.jpg | s7 bed-north-sconce-b — bedroom reverse (redraw.py s7): glass on the left, half-open door at the back right with the camel coat on its hook, wall lamp on; the glass reflects the bed, keep it out of close shots | 750001 | 3eacb6eb89584a4d8ef998ca37fec1a98a1de486c302ec240fcbe0fe2b266d6f |
| set-glass-house-living-liv-gold-a.jpg | s7 liv-gold-a-a — #21 redrawn: single storey, heavy curtains at the table end, two short ladders behind the sofa (take b has no ladders) | 750010 | 73e4549c9df1e5d8c9391be67702bcbe877e997f317a333f0dfe4661a06e3559 |
| set-glass-house-nursery-nur-day.jpg | s7 nur-day-b — #9 redrawn: flat ceiling, black steel floor-to-ceiling window, crib left, rocker right (take a has a frame inside the frame) | 750051 | dc52df0296e66937fe62f00028858a6b51f571c3f1c82a4524c0f21026c18902 |
| set-motel-room-night.jpg | s8 mroom-night-a — #32 redrawn to decision 1: aisle view, headboards on the far wall, window and curtains on the left, Nora's quilts left, Peg's thin blanket right | 750130 | d5d5aaa481f6660bc7d5ce10dd174ff8dbdd51887cb0cdd8df39a2d8f3ad181b |
| nurse-kim-portrait.jpg | a5 nurse-kim-fix-a — Kim, mouth corners level (a5 one-change edit of the a12 pick) | 716000 | 689b820d046048e8fa188919eb8ef1cd51c160b347eb6fa664212250b6fb454e |
| grant-rain.jpg | a5 grant-rain-fix-a — Grant rain look, wet hair and collar (a5 edit of grant-portrait); the lenses are not fogged, the clips write it | 716010 | 026f0ad75db109c82e82d9c1dce8bdd1111046d047d9c2d50de2c5f3269962b1 |
| nora-discharge-coat.jpg | a5 nora-discharge-coat-a — Nora discharge + camel coat worn open, full body (a5 edit of nora-discharge); eps 6-9 | 716020 | 160572e7fcae443d2686b50cec5940608889e9fb6a781ba8613aa5aa6deb8db3 |
| prop-canvas-tote.jpg | p4 prop-canvas-tote-b, cropped to y 512–1664 (1248x1152) so her face is out of the frame — tote on the left shoulder over the oatmeal cardigan (both p2 and p4 takes drew a face; never pass the uncropped PNG) | 761021 | a99e38ad9a249b4df0a0322fd55bdcb3e3665279f4d7923d176693f8702340f0 |
| dr-brandt-portrait.jpg | f1 dr-brandt-b — Dr. Brandt drawn new (redraw.py f1; the a12 pick kept an embroidered name through two edit tries): plain white coat over navy scrubs | 717501 | 14137fe180d1424a29099471fba293fd71c15508a2c4e54fa5838e264248953c |
| prop-forever-vase.jpg | p3 prop-forever-vase-a — factory Forever vase for the ep. 1 TV ad: exactly one change on the picked No. 1 (lip level); the two read alike at a glance, the difference is in the lip | 760120 | a88558b267c5ed843e833d7548d4c901730c75ceab1008bce2cd46e4178f1c80 |
| set-glass-house-living-east-gold.jpg | s9 liv-east-gold-b — living room toward the entry (s9 retry): table left, sofa right back to camera, curtains at the table end, firs through the entry glass; the light reads grey, the shots write the sunset beam | 750501 | 67d0b7ce26ec74d0ee93152d9e6228e8b4bcb17a7aa9fc9e8109e83732c5bfc8 |
| set-glass-house-door-in-day.jpg | s9 door-in-day-a — #7 retried (s9): from inside, door closed, lamppost on the grass left of the steps, gravel forecourt and firs outside, no sea | 750510 | bb8554ac9d6b1583538a560b32f963c918480317672daf5a5f0a7ec05665464a |
| set-glass-house-door-in-gold.jpg | s9 door-in-gold-a — #24 retried (s9): door open inward against the left wall, gold forecourt and firs outside, no sea, no sun | 750520 | b5f68e8f2c3daf98ca6092ac946be5456a218b2062973e7771e88de484bcb50a |
| set-grant-car-interior-day.jpg | s9 gcar-day-a — #19 retried (s9): from the dashboard looking back at one rear bench, front seat tops at the bottom edges, no sunroof | 750530 | 9d0235f7ebea8737d28f78a05c27c2b4983144c7c7b76ccff9387bece6a5d97a |
| set-glass-house-door-out-gold.jpg | f1 door-out-gold-lock-b — #20 with the 3-like mark edited off the lock plate (f1); the oval left on it reads as a thumb-turn | 717041 | 99ee51093b17322f1847a1cca6b10b409b874b5a62f98e332695a685edf0f58b |
| set-bus-stop.jpg | f1 bus-stop-notice-a — #30 with the paper notice edited off the glass (f1) | 717050 | fee95de3a7d0421750ea26b0c848fd0df84e7464905a22932868323b69c0b363 |
| set-glass-house-bedroom-am.jpg | f1 bedroom-am-nightstand-a — #1 morning bedroom with a pale oak nightstand (f1 edit of the vertical pilot take), matching the night pictures | 717060 | 9137b46abfe2d23c00772bb9c205e6866625a2754f8da14b93b1636fd98bd1a2 |
| set-ambulance.jpg | f1 ambulance-end-wall-a — #14 cropped to the cabin (816x1440) and the far window edited into a plain padded wall (f1) | 717080 | 252ca237ad1a8ccd31cdb35da406414ae8a415b8542e1e7e66e04cfcfc672bd7 |
| grant-portrait.jpg | f1 grant-portrait-lapel-b — Grant, the dark mark on the left lapel edited off (f1 on the r3 pick; take a added a pocket square) | 717011 | d731f69eaeb70cbb4acc18415390ccf00bd14868dfa15314aed47968c57b6d98 |
| peg-coat.jpg | f1 peg-coat-pendant-a — Peg coat, necklace without the ring-like pendant (f1 on the r2 pick) | 717030 | da720a1c631011d519b275bc896e1875e4977f4660935c91f8771a3933a5b43b |
| nora-hospital.jpg | f1 nora-hospital-freckles-a — Nora hospital look, forehead spots off, freckles across the nose (f1 on the a4 pick) | 717070 | 5f9b3a8526c56915fa55831abbfaa2d4321151393bcdd607a1a3209123dffcf5 |
| nora-portrait.jpg | f1 nora-portrait-freckles-b — Nora, forehead spots off, freckles across the nose and cheeks as cast.json says (f1 b on the r3 pick; same framing). The r3 picture it replaces: sha256 be2e49a6… seed 713001 | 717001 | 9ae9f58faf1c8a645341b728db905f06a339df28c24835169fe46226f3a03baf |
| sienna-full.jpg | a3 sienna-full-a — Sienna full body from the picked portrait, gold watch on the left wrist (a3) | 714022 | 55f2ed472eede0cf1c7ddac311a56d65b866ddacbbc6394faccd2a8b2772b944 |
| installer-lead-portrait.jpg | a3 installer-lead-a — installer lead: red beard, grey knit cap, grey work clothes (a3) | 714024 | 30d55d1a8dd7f33ca20e9510cc9cf1a22174b1ea9a151afe839b8874d868a715 |
| bev-portrait.jpg | a3 bev-a — Bev, motel night clerk (a3); her glasses chain is beaded, keep it apart from Peg's necklace in shots with both | 714026 | 0a2b073dc63213c4cd118d20609459ae64af3c211f30aa177d5816c8369553d8 |
