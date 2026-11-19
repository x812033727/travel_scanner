# Independent Fact-Check Report — Round 3 Final (`sothatswhy-p25-train-tunnel`)

- **Slug**: `sothatswhy-p25-train-tunnel`（為什麼高鐵車頭要做成長鼻子？｜原來如此事務所 Ep 25）
- **Audit Date**: 2026-11-18
- **Auditor Role**: Independent Read-Only Fact-Checker Subagent (Round 3 Final Verification)
- **Audited File SHA-256 Hashes**:
  - `docs/videos/sothatswhy-p25-train-tunnel/video.json`: `18623ea7ef6385e2f9e0c04b946b966d4b889037e96aacbc51b8bb0df8807779`
  - `docs/videos/sothatswhy-p25-train-tunnel/script.md`: `fe86b114b2afaf72b25d0ac2f2e863f69c56c424f237df214af6b2b8af7426ab` (`narrative 081c62333b99a9b4`, `speech 8aa7b9b763bc411e`)
  - `docs/videos/sothatswhy-p25-train-tunnel/claims.md`: `a00bd71151ca72461265fb183fcbaf8a11497a0129ce7c744630066938798e4a`
  - `docs/videos/sothatswhy-p25-train-tunnel/brief.md`: `b9515e01d0894990065ee513a655dd67bbe64bec4f998605f828199da675b08a`
  - `docs/videos/sothatswhy-p25-train-tunnel/story-lexicon/current.json`: `c043ffcc40f51c1adf8b98a4067981f2fd04361d98a36e17e8d7439c79b80382` (`lexicon_sha256`: `f81576a81ffac051cae8e8e413bace9e414b58b1222effa4ba24eab7a9d76501`)
  - `docs/videos/sothatswhy-p25-train-tunnel/i18n/{en,ja,ko,es,pt,id,vi,th}.json`: `8 / 8` locales (`856 / 856` lines + metadata audited; `0` fabricated N700/N700ST nose-length figures; `8 / 8` canonical series suffixes)
- **Pipeline Lint**: `node tools/video/cli.mjs lint --slug sothatswhy-p25-train-tunnel` → **`0 errors, 15 warnings`** (`106` scenes, `107` lines, `2931` spoken units, `~12.0 min`; Chapter 1 opening hook `00:00`–`00:29`, `0` i18n warnings).

---

## Overall Verdict: **PASS** (`0 NOT FOUND`)

All Round 3 narrative transitions, first-mention scholar/institution introductions, the bridge scene `chief-turn-back-to-nose` (`p038b`), the 6 surgical narrative polishes (`p001`–`p006`, `p056`, `p072`, `p080`–`p081`, `p085`–`p087`, `p100`), and the 3 plain-language technical glosses (`p034`, `p046`, `p080`) are **100% factually supported** by `claims.md` and the 19 verified primary sources in `video.json`:

- **`0 NOT FOUND`** claims across all `107` lines, `youtube.title`, `youtube.description`, `thumbnail.data`, and `sources[]`.
- **Zero fabricated nose-length numbers** for `N700` / `N700A` / `N700S` / `N700ST` (`p082` cites only JR Central's official `27,350 mm` lead-car length; `p099`–`p100` describe `Dual Supreme Wing` wing-shaped cheek ridges + wide Taiwan tunnels without inventing a meter figure).
- **Accurate biomimicry, physics & geometry**: Nonlinear wave steepening (`p034` rear-catching-front mechanism), rotational paraboloid solid-of-revolution geometry (`p046`), kingfisher clean dive inspiration → bullet-in-pipe apparatus → supercomputer rotational-paraboloid calculation (`500` Series `15 m`) vs multi-paraboloidal wide-flat duckbill contour (`700` Series `9.2 m` at `285 km/h`, `p080`–`p081`) vs `Dual Supreme Wing` (`N700S` / `N700ST`) vs `ALFA-X` (`~16 m` & `~22 m` at `360 km/h`) vs RTRI `2019` 3-stage contour (`12 m`-class nose shortened by `1 m`).
- **Visual, policy, loop, and lexicon gates intact**: `64 / 106` (`60.4%`) `nobody: true` shots (`45%–65%` target), `0` speaker/character/prompt mismatches, `0` living or post-1956 real faces, `0` copyrighted liveries or rendered text, `14 / 14` valid `loops[]` IDs, and `700T` bound via `say` / `say_for` + `story-lexicon` (`f81576a81ffa...`).

---

## 1. Verification of Final Round 3 Polishes & Plain-Language Glosses

| Line IDs | Final Text in `video.json` (`d730f97f...`) | Primary Source Support | Status |
|---|---|---|---|
| `p001`–`p006` | Ch. 1 opening hook tightened to `00:29` (< 30s) with explicit subjects (`列車剛進洞`, `洞外四百公尺住戶`, `工程師`) and `700T` bound via `say` / `say_for`. | `Ishizuka 2004`, `Saito 2015`, `JFS 2005`, `Nakatsu 2018`, `Ido 2006`, `Miyachi 2013`. | **FOUND** |
| `p007`–`p009` | Hand-out-window drag intuition (`chief` → `kid`) + first-mention introduction of RTRI (`日本研究鐵路技術的鐵道總研`). | `Ido 2006` (*RRR* 63(9), pp. 30–33). | **FOUND** |
| `p019`, `p024`–`p025` | Compression wave outruns train; first-mention introduction of `美國太空總署 NASA` (`1,225 km/h` sea-level sound speed; `300 km/h` ≈ `1/4` Mach, wave ≈ `4×` faster). | NASA Glenn Research Center; `Saito 2015`; `Miyachi 2013`. | **FOUND** |
| `p027`, `p030`–`p031`, `p035` | Scholar introductions: `研究隧道氣壓的學者齋藤實俊`, `鐵道流體學者小澤智`, `車輛空力專家原田巖` (`v²` vs `v³+` vs `v⁶`). | `Saito 2015` (Osaka Univ. / RTRI), `Ozawa 1995` (*RIMS Kokyuroku* 908), `Harada 2003` (*応用数理* 13(3), p. 199). | **FOUND** |
| `p034` | `壓縮波在長山洞裡後浪追前浪、波面越擠越陡，衝到出口就炸出巨響！` | Plain-language mechanism of nonlinear acoustic wave steepening in slab-track tunnels (`Ozawa 1995`, pp. 30–41; `Saito 2015`, Ch. 1 pp. 1–3). | **FOUND** |
| `p038b`, `p039` | `chief-turn-back-to-nose` bridge scene (`搬不走整座山，工程師就把腦筋動回衝進洞口的那顆車頭上！`) + `kid` sponge guess. | `Miyachi 2013`. | **FOUND** |
| `p046` | `鐵道總研真的拿圓弧蛋頭、尖圓錐，還有拋物線轉出來的旋轉拋物體比過！` | Exact geometric gloss of `回転放物体` (parabola revolved around its axis) + RTRI comparison of ellipsoid, cone, and rotational paraboloid (`Harada 2003`, pp. 200–201). | **FOUND** |
| `p056`, `p059`, `p063`–`p064`, `p070`, `p072`–`p073` | Sanyo `300 km/h` push by `JR 西日本`; `400 m` resident complaints; kingfisher clean dive; `車頂取電的集電弓` owl-feather serrations; Japan's first `300 km/h` commercial Shinkansen (`500` Series, `-15 min`, `>10%` power saved vs `前一代三百系`). | `Nakatsu 2018` (pp. 1–4); `JFS 2005`; JR West `2024-05-24` release. | **FOUND** |
| `p079`–`p082` | `鐵道車輛工程師石塚理` (Kawasaki Heavy Industries Rolling Stock Co.) & `媒體東洋經濟`; `700` Series multi-paraboloidal wide-flat duckbill nose (`把好幾段拋物面組合成寬扁車鼻，跑兩百八十五公里照樣壓住微氣壓波！`); `N700S` `27,350 mm`. | `Ishizuka 2004` (*らん* No. 65, p. 15); *Toyo Keizai Online* (`2024-12-28`, p. 2); JR Central `700` & `N700S` specs. | **FOUND** |
| `p085`–`p087` | Tohoku `320 km/h` `E5` `~15 m` nose callback; `ALFA-X` `360 km/h` `~16 m` & `~22 m` dual noses; RTRI `2019` 3-stage contour shortening `12 m`-class nose by `1 m`. | JR East `E5` spec & `Miyachi 2013`; JR East `2017-07-04` `ALFA-X` release; RTRI `2019-06-24` release. | **FOUND** |
| `p091`, `p094`, `p096`, `p099`–`p103` | Taiwan `700T` wider tunnel cross-section (`Ishizuka 2004`); `日本機械學會期刊` `30–40 m` `45°` slanted vented hood (`Ochiai et al. 2004`); `N700ST` `2027` H2 service, platform wing-ridge check (`p100`), window hood check (`p101`), and final tradeoff synthesis. | `Ishizuka 2004`; `Ochiai et al. 2004` (*JSME* 107(1030), p. 746); THSRC `2026-08-15` `N700ST` release; JR Central `N700S` spec. | **FOUND** |
