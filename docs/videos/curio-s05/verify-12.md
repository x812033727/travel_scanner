# Curio S05 independent audit and delegated script gate

- `docs/videos/curio-s05/script.md` SHA-256 `ceef439e4a2e5eba7f60c0ad7f177bdecfa05c11c723665283a1210b615e2d54`; `video.json` SHA-256 `6a199dd829c8134ad39bd3d3f0283b41e98328f387d3ee18a9044a0d1dfdbcd3`.
- Before reading S05 claims, research, reviews or tasks, the independent reader sealed all 13 blind answers as yes in [`blind-18.json`](blind-18.json) (SHA-256 `7f38253490856a4930945a069bc93b0a407a91665c59309585f03017c30dfee6`). `VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs narrative --slug curio-s05 --answers docs/videos/curio-s05/blind-18.json` wrote canonical `/workspace/.video-work/curio-s05/review/narrative.json`, round 22, passed, no failed or advisory question.
- Prior exposure before sealing: only the assignment title/hash, S05 filename in a prior git-status listing, generic curio skill and narrative procedure, then S05 script and video narration. No S05 claims, research, previous verdict or task content was read before sealing.

## Source and claim check

Pinned SG35 is `Ancient-China-Books/sanguozhi` commit `10a0b1ab3019d8821262f7402366d14fb4aaa102`, `OEBPS/Text/035.htm`. Independently downloaded `/tmp/curio-s05-SG35.htm` SHA-256 `bd76ca6444c3b7b7bd6bebd21f8586af707637ce8d5b559f2aaf7e15ff0acc6f`; this is byte-identical to the local pinned checkout. These are digital transcriptions, not manuscript facsimiles.

- SG35 p0, source line 13: Zhuge's Jingzhou farming, Guan Zhong/Yue Yi comparison, and Xu Shu among friends recognizing ability.
- SG35 p1, source line 14: Chen Shou's main text says Xu Shu recommended Zhuge at Xinye, Liu initially requested he be brought, Xu urged a personal visit, and Liu `凡三往，乃見`; later closeness and the Guan/Zhang fish-water remark. Within the annotation span, the cited *Wei Lüe* says Zhuge went north to Liu at Fancheng, the two were `非舊`, the yak-tail exchange occurred, Liu adopted the household-registration suggestion, and treated him as `上客`. The annotation then says `九州春秋所言亦如之`, followed by Pei's distinct `臣松之以爲` judgment rejecting Zhuge as the first visitor. The script consistently attributes these layers and does not present Pei's quoted alternative as his conclusion.
- SG35 p8, source line 21: the memorial has the complete `三顧臣於草廬之中` phrase, `諮臣以當世之事`, `遂許先帝以驅馳`, and `二十有一年矣`. SG35 p21, source line 47: Chen Shou's collection preface also says Liu visited Zhuge three times; the script correctly treats it as the same author, not another independent witness.
- All 98 video narration IDs are covered exactly once in `claims.md`; none are missing or orphaned. Manual comparison of the mapped source passages found no material contradiction. The source's absence of dates for each visit, a full *Jiuzhou Chunqiu* passage, or independent origin chains is correctly framed as an evidence limit.
- `node tools/video/cli.mjs lint --slug curio-s05 --json`: 0 errors and 0 warnings.

## Body length and visual pairings

`estimateTimeline` places the opening at 47.067 s, the story body from `visit-008` to `outro` at 502.867 s = 8:22.867 across 87 lines, and the outro at 9.8 s; total 559.733 s. The current workdir `status` says narration `timeline.json` belongs to an older script. Thus the eight-minute result is an estimate with 22.867 s margin; current-script TTS must be measured before claiming an audio pass.

Current storyboard: 87 `shot` prompts, two `big` text cards (`visit-061`, `visit-069`), and one outro. No blocking visual contradiction was found by checking prompts against each adjacent line and SG35. `visit-069` displays the exact `三顧臣於草廬之中` quote with attribution to Zhuge's memorial and Pei's use of it. `visit-061` lists *Wei Lüe*, *Jiuzhou Chunqiu*, and the memorial while narration explains their roles; visually the flat list does not itself distinguish two alternative-claim titles from the text Pei used to rebut them. This is a clarity risk if viewers read the card without following narration.

Nonblocking generated-image watchpoints:

- `visit-016` shows a closed cottage gate for the three visits. SG35 does not supply the exact appearance or events of each trip; retain the cartoon as illustrative, and reject an output that makes unsupported novel-specific events look documented.
- `visit-031a` and `visit-031c` show one retainer when narration names both Guan Yu and Zhang Fei. The one-person image can illustrate one reaction, but review whether a generated frame misleadingly suggests only one person objected.
- `visit-081` and `visit-082` say `golden afternoon/window light`, a color-bearing prompt that may drift from the fixed `cute-mystery` palette. No generated images for the new storyboard are available to inspect.

`status` says current-script narration is stale and keyframes are missing. No media was generated or episode source edited during this audit; git index was untouched.

## Delegated gate

The user authorized the recommended A outline and continued production without asking at each gate. At 2026-10-19T22:43:53.847Z, the local `approve --gate outline` recorded the current `brief.md` SHA-256 `ba3e7f5e7577…`. At 2026-10-19T22:43:56.375Z, `approve --gate script` recorded this exact script SHA-256 `ceef439e4a2e…` after the independent 13/13 blind and source audit. Both approval notes identify these as delegated editorial actions; the owner has **not** personally read this revision. The script and narration remain frozen while audio is synthesized and checked.

## Current-script narration measurement

After approval, `tts --dry-run` quoted 94 requests, 67 new syntheses and 1,709 billable characters (2,352 characters for the entire narration). The initial current-script `tts` completed 67 new requests and reused 27 cached takes. Two later same-text retake batches synthesized 16 clips / 406 characters and 11 clips / 293 characters. The latest `timeline.json` contains 98 lines over 90 scenes, with `speech_hash` `a239b301641b640e` and narration SHA-256 `4f7e35a9c6cad835c86bba49d80fdb14cb8a6449ff0b4921f41fc362204b64f4`. At 30 fps, story body `visit-008` begins at frame 1388 (46.267 s) and `outro` begins at 588.400 s: **542.133 seconds = 9:02.133**, above the eight-minute floor by 62.133 seconds. Full audio is 597.767 s. This is measured current-script audio, not the earlier estimate.

`music --dry-run` quotes one 600-second Gemini Lyria 3.5 track at approximately US$0.08. The existing S05 media ledger before music shows US$0.017 from the old accepted image, its judge, and one reservation; speech usage is reported in characters and is not listed as a USD ledger entry. No new image generation has been started while the shared MiniMax slot is held. The audio gate remains pending the unresolved flags described in `audio-qa.md`; no owner listening is claimed.
