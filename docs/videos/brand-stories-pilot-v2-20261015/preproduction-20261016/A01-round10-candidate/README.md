# A01 round 10 offline candidate — UNREVIEWED

**Status: UNREVIEWED. The actual round 9 narrative panel FAILED** `chapters_link`, `payoffs`, and `one_thread`. This directory is a source-bound editing candidate for `story-rolling-suitcase-v2`, **not an import payload, review receipt, approval, or media instruction**. Do not install it on the host, import it, retry a model, or start paid picture/audio work from this folder. A fresh independent fact and narrative review of the exact candidate would be required first.

The frozen round 9 files are in `source/chapters/`; `candidate/chapters/` changes only the `origin-01` line `zc7k`, `now-01` line `7asx`, and the corresponding `now.claims[0]` (`n1`) wording from 「推出了」 to 「發表了」. IDs, all other lines, source/fact references, verdicts, notes, loops, image prompts, and flags are preserved. `inverse-diff.json` records the exact three byte substitutions and reversal order. The independently preserved two-line intermediate `now.json`, manifest, inverse diff, and validation are in `prior-two-line/`.

## File map and fixed evidence

| File | Purpose |
| --- | --- |
| `manifest.json` | SHA-256s for the round 9 source, the prior two-line candidate, final chapter files, inverse diff, and validation; explicit `UNREVIEWED_OFFLINE_CANDIDATE`. Original Temp manifest SHA-256: `839ea9093b259450c7fd3469d78eb404206e77a524d16bd8323e21227c427ee1`. |
| `files.sha256.json` | Complete relative file inventory with byte counts and SHA-256 for every other file in this directory. The inventory excludes itself to avoid a circular hash. |
| `source/chapters/*.json` | Exact six round 9 chapter bytes; composite source SHA-256 in the manifest: `cf39296d597d36db3cafedc1c2ca5ae730dd104a34b1d1868fb5b83fc089c56b`. |
| `candidate/chapters/*.json` | The three narrowly edited fields in six complete chapters; no live chapter was overwritten. |
| `inverse-diff.json`, `prior-two-line/` | Full reversible sequence and the earlier two-line package's hashes. `prior-two-line/now.json` preserves the intermediate before claim sync. |
| `validation.json` | Local compose/lint/timeline output only: 0 mechanical errors, 37 warnings, 63 scenes/92 lines, ~520.33 estimated seconds. It does **not** contain a new independent narrative judge result or measured TTS. |
| `evidence/round9-narrative.json` | Actual historic panel, `round=9`, `passed=false`; SHA-256 `dd458ee2b6eee90a3b358408c605620c108ca4387afb94249fd555abc01babab`. Other `evidence/` files are exact series, script preview, brief, and lexicon inputs used for local compose/lint. |
| `composed-preview/story-preview.json` | Offline rendered *JSON preview only*, byte-identical to the prior two-line preview; deliberately not named `video.json` so no video workflow mistakes it for an active episode. No generated images/audio/media exist in this package. |
| `visual-warning-audit.md` | Read-only MiniMax/cute-mystery and pacing review; original SHA-256 `b6e678d3f910e53136dcf54909b0d8937bc4b01421ccd9822defb722038da97c`. Its opening names the Temp source bundle; the byte-identical bundle is preserved here. |

`node verify.mjs` rechecks all JSON, source and candidate hashes, exact forward/inverse edits, source/fact/claim fields, historic FAIL, preview compose, and mechanical lint using the repository's current renderer. It does not call a model, host, or provider and writes nothing.

## Editorial and image boundaries

The 1997 wording uses the [Samsonite 2011 prospectus](https://corporate.samsonite.com/on/demandware.static/-/Sites-InvestorRelations-Library/default/dwa68533ea/PDF/announcements/2011/20110602100852_Samsonite_Final_Prospectus_en.pdf), printed p.72/PDF P80, lines 3057–3058: Samsonite **presented** a balanced four-wheel upright case that could be pushed or pulled. It does not establish 1997 retail availability, and 2000 Spinners are a later separate entry. [Travelpro's company history](https://travelpro.com/pages/our-history) supports the earlier two-wheel upright pull use; it does not establish Plath-to-Samsonite technical inheritance. The [Winnetka Historical Society article](https://www.winnetkahistory.org/gazette/before-her-time-anita-willets-burnhams-rolling-suitcase/) was independently located in the official site's search index, but a direct page open timed out; this limits what can be claimed as directly reread in this preparation.

Before any bulk MiniMax images, the visual audit identifies four source/voice alignment fixes: `origin-01` (mother pulls the case; current picture shows son about to carry it), `idea-01` (the buyer refuses; current picture shows the salesman sending someone out), `idea-05` (the picture prematurely shows another refusal), and `now-01` (1997 presentation is shown in a retail shop). It also identifies 14 still-image holds over 10 seconds. The smallest **proposed**, unrun three-shot pilot is `turn-15` → `now-01` → `now-02b`, testing two-wheel upright, 1997 push/pull four-wheel, and 2000 multidirectional side movement in one continuous segment. Those prompt/shot changes are recommendations only; this folder intentionally preserves the frozen candidate bytes.

The historic round 9 FAIL remains valid as a historic outcome. Neither the rule clarification in a separate PR nor the wording in this folder converts it into PASS. No new host readback, paid generation, TTS measurement, final cut, upload, or owner playback is represented here.
