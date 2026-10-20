# S54 R14 narrative merge and pre-audio policy

Status: **PASS** for the two-reader narrative panel and the exact R14 Jev policy request. This is a pre-audio gate; it does not certify audio or final video quality.

## Frozen inputs

| File | SHA-256 |
| --- | --- |
| `script.md` | `483558f1617939d109c453ec35f09840ed3de9bcbf0455aa1598433f9b74448f` |
| `video.json` | `ab07d7166dc1141a822747dfd43d46675fa9f5c97ce3cff528875df48764a83b` |
| `brief.md` | `bedc89ef669f9b64868ff3ccea85adb13ee07d75a1ab2120ab6193079f4623f9` |
| A ballot JSON | `dd7595468f4fc189a4d5f0eda42093fac031077d775bed7524d605c68fad66c8` |
| B ballot JSON | `5d8aea685ecbb0780cd42b5e2333e56713cc07740c933f9715c9f52b9909d29e` |

Both independent readers voted yes on all 13 fixed questions, with the same `panel_rules_sha256` (`5d71fef2cf3831dc33c0c32b2b297f633c47bfe41fbad18865ae08ed0c91cb75`) and `panel_narration_sha256` (`b908a3f32e597ebf8c7cc477e462777d7ed3583ca243d91b3f628b1f507116e9`). The official `mergePanelVerdicts` OR rule yielded 13 yes, no required failures and no advisory failures. [The merge audit](merge-audit.json) retains each reader's answers and has SHA-256 `3c9fe0dbe422b491a1249e894df33d4cc2cb3d3f87c8a28374c4c015a4002679`. [Merged answers](merged-answers.json) have SHA-256 `dee2e3337ecd061d2cdfea5ed112d804749343792ddd0689d54c103bc86cd3c9`.

The official `narrative --slug curio-s54 --answers .../merged-answers.json --json` exited **0** with `passed:true`, `failed:[]`, `advisory:[]`. It wrote `/workspace/.video-work/curio-s54/review/narrative.json`; the [archived CLI receipt](merged-narrative-cli-receipt.json) is byte-identical, SHA-256 `eae6116bcfec5babeb787304ea13e5f7aa4ef0e1e37baa4ded00bbf59d9a2f59`.

## Jev policy

The request used `policyRequest({doc, brief})` from `tools/video/qa/policy.mjs`, with the exact R14 `video.json` and `brief.md`: 3,483 narration characters and 72 viewpoint characters. [The exact request body](policy-request-body.json) has SHA-256 `4c6552953e8f9e14b448993f60bca2b774ccb8cd9e3f30b33121344532e491aa`. One POST went to `/api/video/automation/judge/policy`; no retry was made. HTTP 200 returned `passed:true`, `questions:"explainer"`, stance `0.69`, demo not applicable, advice `0.01`, sponsored `0.26`. [The raw response](policy-response.raw.json) has SHA-256 `4e450e08aea72d4db9fcfa6919809f91fe9f7b1e006e69a21b3d37561a19531e`; [the parsed receipt](policy-receipt.json) has SHA-256 `5ae05e7733ad38d6749fdb015511a7f01879dfce872efe06ac2ff5fbf6734c9a`.

The `/workspace/.video-work/curio-s54/STOP` file remained present throughout this work. No script, claims, brief, visual, or audio content was edited, and no TTS was run.
