# S38 four-prompt R8b3 static audit — PASS

Current `docs/videos/curio-s38/video.json` SHA-256: `bdceef9ad332e0ce85dd629eea2bf5e944399ee2113586c0eebc4b4265c2963a`.

The authenticated R8b2 baseline `/tmp/curio_s38_r8b2_snapshot.json` hashes `ca2bb866b0fb452607f20764f652c715f1447bc226f9df0a28bfc3b1d73cb1fc`. A recursive parsed-JSON comparison found **exactly four changed leaves**, all `data.prompt`: `pf001`, `pf002`, `pf071`, `pf072`. Every other JSON value is equal. `script.md` remains `e59ec137e3de3871e3b0e5063d8f6504d3eb2adb5fe22265eb3faa3d613d5951`; `claims.md` remains `f9de8d2771b62cc327f4e599f002af8f3278cfb0f39dbed201e7fdc857201d42`.

Pepys's 4 September diary passage, pinned in `research.md` as D4a (GITenberg text lines 65997–66002), says Batten first dug a garden pit for his wine; in the evening Pepys and Sir W. Pen dug *another* for their own wine, and Pepys added his `Parmazan` cheese. `pf001`/`pf071` show two adult men digging the second pit, and `pf002`/`pf072` show adult hands placing a hard-rind cheese with wine in that pit. The 1660s clothes, spades, wine vessels and garden soil are plausible visualizations. Faces cropped out and the continuous closed rind target the two rejected pilot failures (childlike adults and hole-riddled modern cheese). No writing, cheese recovery, price, weight or invented outcome appears.

Fresh `node tools/video/cli.mjs lint --slug curio-s38 --json`: exit 0, **0 errors, 0 warnings**. The two warnings on the intermediate `d7bc2027…` version were removed before this audit; that version is not approved. Image generation still needs a **small human-inspected pilot**: inspect apparent adult scale and period clothing, a compact intact cheese without Swiss holes, the correct second pit, and no invented text before longer production.

Read-only audit; no repo edit or media spend.
