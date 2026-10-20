# R14 isolated narrative merge

## Frozen input

The two readers judged only `docs/videos/curio-s52/script.md` and the 13 official `narrative` questions before comparing answers. The script SHA-256 was and remains `e1d04c2bd2e126baf5f777f8237cc1e4c075fdfc465ef6a183ec861fd212ae9c`.

| Reader | Frozen answers | Frozen JSON SHA-256 | Yes / no |
| --- | --- | --- | --- |
| A | `r14-isolated-blind-a.json` | `fce1e11a7594816ea0a77c4f71cfd76dc456eadc4c800cb5ee8338f292c24e1a` | 11 / 2 |
| B | `r14-isolated-blind-b.json` | `9893ebc9fbb25055ff19a0359abd09a30b5efba0cd9f9f1e63f3d3c3bb7bfdc5` | 12 / 1 |

Both original JSON files are unchanged. Their evidence named exact line IDs without square brackets. The CLI requires `[s52001]` form even when the bare ID and exact quote are present. The format-only copies `r14-isolated-blind-a-normalized.json` (`50b0a3cadcaa0265ea2cb35c4dd3cef6022c80ae6dab64b29631f73eaf550651`) and `r14-isolated-blind-b-normalized.json` (`82c11b16282768d5754b79292503e0342d1e91c585ca4fe34428183270e381af`) add one exact script line with a bracketed ID to each piece of evidence. All 26 yes/no decisions remain unchanged.

## Official merge

`mergePanelVerdicts` in `tools/video/core/narrative.mjs` uses **any-reader-yes OR**. The merged answer is yes when either reader gives a cited yes. `r14-isolated-merged-answers.json` was generated from `panelVerdict` on the normalized copies, then `mergePanelVerdicts`; SHA-256: `12c132505e9af625a6e171c71238d48f1d273759b4fff500e89863bfbdfa611d`.

| Question | A | B | Official OR |
| --- | --- | --- | --- |
| `payoffs` | No | Yes | Yes |
| `no_recap` | No | No | **No** |
| Other 11 | Yes | Yes | Yes |

The shared failure is specific. [s52122]「會。皇家學會的刊物把格林、庫克與索蘭德的觀測分別列出。」 is immediately restated as [s52315]「原報把格林與庫克的讀時各自排開，索蘭德也有自己的欄位。」 The latter adds no new contact time or observation. Reader A also flagged the unanswered clock comparison at [s52313]–[s52314] for `payoffs`; reader B accepted the calibration table as the answer, so official OR passes that question.

## CLI receipt and disposition

Command: `node tools/video/cli.mjs narrative --slug curio-s52 --answers docs/videos/curio-s52/review/r14-isolated-merged-answers.json --workdir /workspace/.video-work`

**HOLD.** CLI exit code **1**; 12 of 13 merged answers are yes; `failed` contains only `no_recap`. The valid canonical receipt is `/workspace/.video-work/curio-s52/review/narrative.json`, round **13**. Its checked-in snapshot is `r14-canonical-cli-receipt.json`, SHA-256 `b8a6c399985e92045632fb9ea29ae0d83e0bdf7f05c1e154fc4b4a1b60a4bf0e`. An isolated CLI run yielded the same answers and `failed` list in `r14-isolated-cli-receipt.json`, round **1**, SHA-256 `212f0da82a1aa6b25cd1ceea9c2c7fab4e6607dacfa403d2a16983d358700cec`.

An earlier CLI attempt used the frozen files' unbracketed evidence and was **format invalid**, marking all 13 answers no; this was not a substantive review verdict. It produced canonical round **12** before the format rule was found. That receipt is preserved as `r14-invalid-first-run-receipt.json`, SHA-256 `bf3c9a77354399051c4998c08aba7f43beaf5a984cc143bab8e4107afe8835b1`. The later official CLI run created round **13** and superseded the bad result without hand-editing the canonical record.

No script or paid media was changed. The author can remove or replace the repeated point at s52315, then obtain a new script hash and fresh blind reviews.
