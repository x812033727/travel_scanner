# Multilingual Editorial Review — `sothatswhy-p12-qr-code`

- **Reviewer**: Independent Multilingual Editorial Reviewer (`1d517f7eda048289a82440e98495ccfb`)
- **Source Baseline**: `docs/videos/sothatswhy-p12-qr-code/video.json` (`p001`–`p159`, 6 chapters, YouTube metadata, thumbnail) & `claims.md` (`C01`–`C11`)
- **Locales Audited**: `en`, `ja`, `ko`, `es`, `pt`, `id`, `vi`, `th`
- **Final Verdict**: **`PASS`** across all 8 locales (all title, TTS, register, and short-cue tightening fixes applied and verified with `lint` 0 errors / 0 title warnings).

## 1. Factual & Technical Audit

All 8 locales accurately preserve every verified technical claim from `video.json` and `claims.md`:

- **Origin & Finder Geometry (`C01`–`C04`)**: 1994 DENSO debut by Masahiro Hara's 2-person team; `Quick Response`; rare `1:1:3:1:1` finder ratio measured across printed flyers, magazines, and boxes; 3 finder corners vs blank 4th corner for 360° orientation; `Model 2` alignment pattern for curved cans and angled shots; unprinted 4-module-wide quiet zone / margin on all 4 sides.
- **Grid Capacity & Reed-Solomon Error Correction (`C05`–`C08`)**: Version 1 (`21×21` modules) growing by `+4` modules per side up to Version 40 (`177×177` modules; up to `7,089` numeric digits or `4,296` alphanumeric characters); 8-bit codeword boxes; Reed-Solomon error correction in satellites/planetary probes and music CDs; `3 + 5 + 2 = 10` framed explicitly as a simplified analogy; 2 error-correction codewords per 1 unknown damaged codeword; DENSO WAVE's `100` data + `100` correction = `200` total codewords (`50 / 200 = 25%`, Level Q).
- **Levels, Burst Damage & Density Trade-Off (`C09`–`C11`)**: Official levels `L` (~7%), `M` (~15%), `Q` (~25%), `H` (~30%) measured against total codewords rather than paper area and never guaranteed against finder/margin damage; center logos spending error-correction quota while avoiding corners and margin; 1 concentrated puddle (2 boxes) surviving while 8 scattered pepper specks across 8 boxes blow the quota under whole-codeword accounting; Version 1 `L=41` vs `H=17` digits and `50` digits forcing Version 2 `H` (max `34`) up to Version 3 (`29×29` modules), shrinking sticker dots and increasing blur risk (`Q/H` for oily factories, `L` for clean high-data uses, `M` ~15% for daily menus).

## 2. Character Voice & Spoken TTS Naturalness

- **Persona Separation**: Chief (`所長`) consistently reads as a calm, warm mentor and Little Q (`小問` / `ハテナ` / `궁금이`) as a lively, curious learner. Rhetorical-question lines (`p082` in `ja`, `ko`, `th`, plus `p158` in `ko`) that had slipped toward Little Q's polite/questioning register (`고쳐요?`, `남겨요!`, `ไงคะ?`, `直せるの？`) were restored to Chief's mentor voice within `max_chars`.
- **Short-Budget Cue Tightening (`p065`, `p075–p076`, `p082`)**: Ultra-short dub budgets on `p075` (`max_chars` 3–8, source `"沒有抄備份，"`) were rebalanced (`p075` standalone natural interjection + `p076` full `"without backup/copy"` clause) across `en`, `ja`, `ko`, `es`, `pt`, `id`, `vi`, `th`, eliminating meaning drift (`es` `"Sin él"`, `pt` `"Único"`), TTS-hostile abbreviations (`en` `"No dup"`, `vi` `"K. chép,"`), spacing errors (`ko` `"안베껴"`, `"한상자"`; `th` `"1กล่อง"`), and mid-word splits (`id` `"Tanpa / salinan"`, `th` `"ไม่จด / ซ้ำ"`).
- **Idiom & TTS Symbol Hygiene**: Restored `"gratis"` in `id` `p132` (`"tak ada yang gratis!"`), `"bagaimana"` in `id` `p052`, `"titik"` in `id` `p063`, and `"receipt"` in `en`/`th` `p154`; expanded written symbols/shorthands (`P&B`, `a B y N`, `4ª`, `/`, `−`, `2x`, `yg`) and Vietnamese ASR homophone traps (`bản` → `phiên bản`, `nối` → `theo`).

## 3. Packaging (YouTube Titles, Chapters & Thumbnails)

- **Series Suffixes**: All 8 locales match the 2026-11-13 canonical series names (`So That's Why`, `なるほど事務所`, `그래서 그랬구나 연구소`, `Así Funciona`, `Agora Entendi`, `Oh Begitu Toh`, `Hóa Ra Là Vậy`, `อ๋ออย่างนี้นี่เอง`).
- **Mobile Title Width (`≤35.5` full-width units)**: Shortened all titles previously over `36` units (`ja` `34.0`, `ko` `33.0`, `id` `33.5`, `vi` `34.0`, `th` `33.5`, plus `en` `31.5` and `es` `32.5`) while preserving the coffee-stain vs clean-QR contrast hook.
- **Thumbnails**: Non-spoiler hooks verified across all 8 locales; tightened `en`, `es`, `id`, and `th` `thumbnail.headline` lines to `≤10` characters per line so all 8 series thumbnails render at the full `150px` display size with zero `thumbnailProblems`.
