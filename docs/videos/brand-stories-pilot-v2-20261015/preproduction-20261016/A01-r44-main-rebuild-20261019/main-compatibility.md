# A01 r44 clean-main rebuild compatibility

> Historical experiment record, before the 2026-10-19 portability correction. The original manifest and builder hashes below describe that experiment. The later correction redacts local paths and rebinds packaging hashes only; current identities and original manifest copies are documented in [the portability receipt](../portability-20261019/README.md). Original validation and content bytes remain unchanged.

This directory is a validation-only sibling rebuilt from the frozen r44 input closure (`build.mjs`, `story-data.mjs`, `brief.md`, `README.md`, `reference/`). It is not an approved replacement candidate. No frozen r44 file was edited.

- Clean main commit: `e42d93979781b250b53f93e36ff1c901679b39ce`.
- Original branch-sync commit: `379b3a80effe7b8a0912324a494832a03d841316`.
- Frozen r44 manifest SHA-256: `62cec617460b882309a48ca76c69615ec20789502538149cc94e47a632144190`.
- This sibling manifest SHA-256: `6657c3e1a14d958728526c81ac4abd7642d6b4e94fcb331bc66a4ac0fb7bccea`.
- Frozen r44 `--check` on clean main: exit 1, `stale output: validation.json` at `build.mjs:408`.
- This sibling `--write` then `--check` on clean main: exit 0; 51 scenes, 52 lines, 55 claims, zero lint errors, zero cute visual errors.

## Exact output comparison

The nine other generated outputs are byte-identical to frozen r44: `candidate/video.json`, `candidate/series.json`, `candidate/lexicon.json`, `candidate/script.md`, `candidate/claims.md`, `research-plan-25-series.json`, `research-year-discrepancy.json`, `source-map.json`, and `source-alignment.json`. `validation.json` is the sole generated output that differs. Its only changed JSON field is `lint_warning_count`, from 40 (frozen) to 43 (clean-main rebuild); all other validation fields are equal. The two manifests differ only at `outputs_sha256["validation.json"]`.

| File | Frozen r44 SHA-256 | Clean-main rebuild SHA-256 |
| --- | --- | --- |
| `candidate/video.json` | `7e1ec10c465dab8f7f774cff8feaad2e7dcfdc8d5aa670856a34f9597a86379d` | same |
| `validation.json` | `73f1791a4593cd0f62c905f8c5dff324f92145a64e15c5ded72c5d5e8899651d` | `c5a95e62d7888e74dba30ecaa1c350d305a3e41462aae34c5048c195af127900` |

## Dependency change and cause

`build.mjs` itself is byte-identical (`9aa6526818517acc3555b0bc4c5112ba69ceb53d918cf68c21ec7c8f8c8ce544`). Its four direct dynamic imports come from the current checkout; the table also includes the changed `duration.mjs` and `narrative.mjs` reached transitively by the lint and story modules. Hashes are SHA-256 of the tracked working-tree file bytes.

| Relevant dependency | Clean main e42d939 SHA-256 | Branch-sync 379b3a8 SHA-256 |
| --- | --- | --- |
| `tools/video/core/screenplay.mjs` | `1a9e75af1d383948ab1861421a337145c7c89ab3cd927daa1d05385aeb55a389` | same |
| `tools/video/core/timeline.mjs` | `0088b369f5ddb962fc5d803bb5dd982f2f8f22b558eca728d0bfca5df1aa39b2` | `369e747e8afc2382fdee8da9ebf9b2f0de14306200bab81ee658057168b3fc3a` |
| `tools/video/core/lint.mjs` | `6f560e91f90126ecbf245ec754a7790ba49362651507d5c01e3ff1a5c939f95a` | `6cc1c1ee9cb425303d7a9f2ffa2d6aa5bddc3fa82c72314ede0060703316a386` |
| `tools/video/core/duration.mjs` | `df4874326d1d098d19a8df5ed4010cc3454537cbc96217a4c4192dc622caea1d` | `12009ae5d12cba73e55ff462e9f9dd107350d53bea1da5a65bf59a1a39e13285` |
| `tools/video/core/narrative.mjs` | `e479a0de6c2b14cd0623769cc226ab7433acb33bbadfde3ed41e927fa89378ae` | `97cdcabb61fcd785821577a403162f0a5cbf57225892467de1bca9baa93b5665` |
| `tools/video/automation/story.mjs` | `db7afddc854f6f106fb7198d8f2634ad15f9e6eb5fe8c295efc604413c8ed179` | `145838ca8c1f707d68925c8dee2bdb0647fe5c4192142040737fabcda1e9e808` |

The causal difference is clean-main `tools/video/core/lint.mjs:474,503`: it runs episode script and narrative checks for `isA01CompactStory(doc)` even when the estimated duration is under `MIN_EPISODE_MINUTES`. The branch-sync version runs those checks only above the length threshold. Linting the exact frozen video under each checkout gives 43 versus 40 warnings, with these three clean-main-only warnings:

1. `scenes[50] (now-outro)`: two outro sentences where the lint rule asks for three.
2. `scenes`: no open loop between 03:02 and 04:41 (99 seconds).
3. `scenes`: no open loop between 04:41 and 06:24 (103 seconds).

These are warning-level findings, not changed video bytes or new source claims. The frozen manifest remains valid as a hash of its own original outputs, but its `--check` is checkout-dependent. For a clean-main-only mechanical check, use this sibling's regenerated validation and manifest as comparison evidence; any promoted candidate should be versioned and reviewed as a separate artifact rather than patching frozen r44 in place.
