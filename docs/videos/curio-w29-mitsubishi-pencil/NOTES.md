# W29 `curio-w29-mitsubishi-pencil` Production Notes (N9050)

## Topic & Score
- **Pool ID**: `N9050` (score **9.27** — #8 highest-scoring unproduced `curio` topic in `apps/api/app/video_pools/data/pools.json`).
- **Title (`zh-TW`)**: `三菱鉛筆不算三菱？早財閥11年註冊還買下LAMY`
- **Duration & Structure**: 55 scenes, 110 lines, 2,060 spoken units (~8.4 min), 8 chapters, 12 verified official primary URLs (all HTTP 200).
- **1956 Real-Person Redline**: Only pre-1956 deceased historical figures named (`岩崎彌太郎` d.1885, `眞崎仁六` d.1932); zero living or post-1956 deceased individuals named or depicted.

## Pre-TTS Quality Gates Passed
1. **Fact-Check (`verify-2.md`)**: **VERDICT: PASS** (`12/12` primary URLs verified, `0 DISCREPANCY`, `0 NOT FOUND`; fixed Round-1 catches including `LAMY` 1930 founding phrasing, `非財閥體系`, `德國有形固定資產`, `本業賺五百九十萬`, `歐洲去庫存與成本影響`, and Mitsubishi official history URLs).
2. **Lexicon (`docs/videos/lexicon.json`)**: Appended 10 W29 brand terms (`uni`, `Hi-uni`, `JETSTREAM`, `KURUTOGA`, `LAMY`, `safari`, `inside`, `M17`, `uniball`, `ZENTO`) for clean pronunciation and `0 errors, 0 warnings` lint.
3. **Opening Review (`opening-review.json`)**: **PASSED** on v14 (`newcomer 9.0 / scroller 9.0 / stickler 9.0`, all `would_stay_300: true`, `swipe_at: null`, `problems: []`).
4. **Narrative Panel (`narrative.json`)**: **PASSED** on v14 — 2 independent blind readers `14/14` + `14/14` = **`28/28 ALL YES`**.
5. **Keyframes (55/55)**:
   - Theatrical-light rich-gouache style (`5` Ada shots locked to `ada-canon-v2.png` via built-in `generate_image` \$0 + `50` non-Ada shots via `gemini-3.1-flash-image` / built-in `generate_image` \$0; zero MiniMax image generation).
   - Programmatic 4-edge border check: `0 border flags`.
   - Independent 2x-zoom 4-quadrant visual audit across Rounds 1–4: **`55/55 100% PASS`** (all imported via `keyframes import --provider external --usd 0`).
6. **8-Locale Translations & 9 Rendered Thumbnails**:
   - All 8 locales (`en`, `ja`, `ko`, `es`, `pt`, `id`, `vi`, `th`) independently audited -> **`8/8 PASS`** (fixed `en m055`, `es m014/m076/m082`, `pt m014/m029/m076/m098`, polished `ko`/`id`/`vi`/`th`; Thai description 1,844 UTF-8 bytes <= 2,200, female polite tone `ค่ะ`/`นะคะ`, exact `บริษัทแม่`).
   - Hero thumbnail (`v7`, `stock/c0a5fb24c95a010e319ede2b77b55a3bea05dffcf1c15ef236de341fa19217ef.jpg`): `heimao-left`, seamless sky gradient with diagonal sunbeams, Ada lower-left, burgundy-gold-black uni pencil + canary-yellow LAMY safari + exact 3 ruby diamond crystals lower-right -> independent visual audit **`9/9 PASS`** across `zh-TW` + all 8 locales with zero text collisions.
7. **Lint**: `curio-w29-mitsubishi-pencil: 0 errors, 0 warnings`.

## Budget Hold / Post-TTS Queue
- **Pre-TTS locked & backed up** (Google Drive `W29/` `1MR-xLg-e1WyGVAKPpeXx_8wT4eHo9mGr`, `W29/製作檔/` `1Dy7BYrYxiW9N7XmnMNECkpoPm5xfo92p`, zero-diff verified; `/admin/videos` `script` + `storyboard` gates pushed).
- **Pending Owner Confirmation**: Do NOT run Gemini `tts` until owner confirms Ultra slot budgets are restored in `/admin/settings` (or explicitly authorizes `SITE` TTS). Post-TTS order once confirmed: `W25 -> W26 -> W27 -> W28 -> W29`.
