# W30 `curio-w30-monde-selection` Production Notes (N9070)

## Topic & Score
- **Pool ID**: `N9070` (`#9` pool core — Monde Selection 比利時世界品質評鑑大賞金獎貼紙).
- **Title (`zh-TW`)**: `比利時金獎憑什麼滿街貼？Monde Selection 過80分就發｜奇聞檔案局`
- **Duration & Structure**: 56 scenes (`36/56 = 64.3%` `nobody: true`), 111 lines, 2,063 spoken units (~8.4 min), 7 chapters, 8 verified official/academic/media primary URLs.
- **1956 Real-Person Redline**: Zero living or post-1956 deceased individuals named or depicted; only institutional actors, anonymous shoppers/judges/brewmasters/planners, and recurring researcher `Ada` (4 scenes, locked to `ada-canon-v2.png`).

## Pre-TTS Quality Gates Passed
1. **Fact-Check (`verify-2.md`)**: **VERDICT: PASS** across all 8 primary URLs (Monde Selection FAQ/Evaluation, Foods R&D official EUR fee schedule & 2018 global/Japan statistics, Oct 2024 press release announcing 2025 abolition of Silver/Bronze awards, Monde Selection 2026 Nominee Label 416-product directory, Meijo University *Meijo Ronso* 2005 premium beer paper, *Diamond Online* listed e-commerce operator column).
2. **Lexicon (`docs/videos/lexicon.json`)**: Appended 7 terms (`Monde`, `Selection`, `Nominee`, `Label`, `Diamond`, `Online`, `Prime`) for clean pronunciation and `0 errors, 0 warnings` lint.
3. **Opening Review (`opening-review.json`)**: **PASSED** on v20 (`newcomer 9.1 / scroller 9.0 / stickler 9.1`, all `would_stay_300: true`, `swipe_at: null`, `problems: []`). Key breakthrough: unified the opening into the single 2018 global cohort (`2,800` entries, `>91%`, Europe cold vs Japan `>1,300` over half) and reserved the 2026 Nominee Label (Taiwan 126 #1 vs Belgium 0) for Chapter 6 climax.
4. **Narrative Panel (`narrative.json`)**: **PASSED** on v20 — 2 independent blind readers `14/14` + `14/14` = **`28/28 ALL YES`**.
5. **Keyframes (56/56)**:
   - Theatrical-light rich-gouache style (`4` Ada shots locked to `ada-canon-v2.png` + `52` object/scene/anonymous-character shots, all via built-in `generate_image` `$0`; zero MiniMax image generation).
   - Programmatic 4-edge border check: `0 border flags`.
   - Independent 2x-zoom 4-quadrant visual audit across 3 rounds (`43/56` R1 -> `13` redrawn -> `9/13` R2 -> `4` redrawn -> `2/4` R3 -> final `2` (`s02`, `s07`) redrawn & verified PASS): **`56/56 100% PASS`**, all imported via `keyframes import --provider external --usd 0`.
6. **8-Locale Translations & 9 Rendered Thumbnails**:
   - Translations for `en, ja, ko, es, pt, id, vi, th` merged, independently audited, and 9 thumbnails (`heimao-left` over `stock/c9468e2c1edab47a80154e016ee4daa58c60ae6b658613295af98551b4624a71.jpg`) rendered & visually inspected.
7. **Lint**: `curio-w30-monde-selection: 0 errors, 0 warnings`.

## Post-TTS Queue
- **Pre-TTS locked**: Waiting for upstream Gemini TTS daily RPD quota reset (or upgraded API key in `/admin/settings`) after W25 (12 redo lines) -> W26 (25 remaining lines) -> W27 -> W28 -> W29 -> W30.
