# S56 R4 author fix and independent-review handoff

2026-10-20 UTC. This is an **author repair**, not an independent PASS. It addresses the written-visual and claim-sheet findings in [R3 independent HOLD](r3-source-independent.md) without changing any spoken line, chapter, loop, source URL, thumbnail, description, or research boundary.

| File | R4 SHA-256 |
| --- | --- |
| `script.md` | `b76995caa74f0a1f65b068d9e115659d7c48678600b80e9ff502e641a6505152` |
| `video.json` | `9516fc7c0d76c011d39e00be5262e6011a2b2a8597636074334c88ba901447ff` |
| `claims.md` | `1d267cb9365eab571b3b94f13de5ebc136e323bc0d80869db0abac3874ccc1d3` |
| `brief.md` | `a17b3ac122723c1229bdb1bcf1af2c546b7665407bad5677a24658ad50583dfd` |
| `research.md` | `59549e98e6ae258cedfc5b43e6684ecaa1102284d0dee13b0beef6443e4a6fb7` |

## Narrow R3 → R4 delta

- `video.json` `s56117` now directs the lodgers and their luggage **toward the outside door**, matching Loesch's boarders leaving with what they could carry [L322–327](https://github.com/GITenberg/Personal-Experiences-During-the-Chicago-Fire-1871_66433/blob/08931a6f2629fd4b8be37b1ec548857d48d17eb9/66433-0.txt#L322-L327).
- The five-frame refuge run `s56161–s56165` now uses night or distant fire light for fence removal, post pulling, well water, overnight watching, and the final roofs before rain. Loesch says the fence work began **long after dark** [L595–600](https://github.com/GITenberg/Personal-Experiences-During-the-Chicago-Fire-1871_66433/blob/08931a6f2629fd4b8be37b1ec548857d48d17eb9/66433-0.txt#L595-L600); his watch and last row of houses lead to about 1:30 a.m. Tuesday [L601–609](https://github.com/GITenberg/Personal-Experiences-During-the-Chicago-Fire-1871_66433/blob/08931a6f2629fd4b8be37b1ec548857d48d17eb9/66433-0.txt#L601-L609). `s56160` remains the earlier furrow view, while `s56166–s56167` already show rainy night.
- `claims.md` `s56146` now names **Loesch's 1925 station recollection** and its 1925 desk image; `s56149–s56151` now describe the current Monday walk, furniture burial, and burning street/fence images. The engine counterfactual remains confined to `s56148` [L537–557](https://github.com/GITenberg/Personal-Experiences-During-the-Chicago-Fire-1871_66433/blob/08931a6f2629fd4b8be37b1ec548857d48d17eb9/66433-0.txt#L537-L557).
- Claim citations now directly cover the dated letter at `s56015` [F204–208](https://github.com/GITenberg/A-Letter-from-the-Fire-Being-an-account-of-the-Great-Chicago-Fire_66472/blob/60c777551301c30942acf749d4bb37ca32752353/66472-0.txt#L204-L208), Foster's northward crossing at `s56112` [F447–459](https://github.com/GITenberg/A-Letter-from-the-Fire-Being-an-account-of-the-Great-Chicago-Fire_66472/blob/60c777551301c30942acf749d4bb37ca32752353/66472-0.txt#L447-L459), the Foster bridge contrast at `s56118` [F447–459](https://github.com/GITenberg/A-Letter-from-the-Fire-Being-an-account-of-the-Great-Chicago-Fire_66472/blob/60c777551301c30942acf749d4bb37ca32752353/66472-0.txt#L447-L459), and refugees carrying possessions at `s56152` [L560–575](https://github.com/GITenberg/Personal-Experiences-During-the-Chicago-Fire-1871_66433/blob/08931a6f2629fd4b8be37b1ec548857d48d17eb9/66433-0.txt#L560-L575). The older relevant ranges remain in those rows.

## Checks and next gate

The `script.md` byte hash is identical to R3 because narration and scene grouping were untouched. Parsed `video.json` still has **176** unique ordered `s56001–s56176` spoken-line IDs, **141** scenes (**137** written `shot` prompts and four `big` cards), seven chapters, and **17** ordered setup/payoff loops. All 176 line texts exactly match `script.md` and their one row each in `claims.md`; every row has a pinned-source link. `node tools/video/cli.mjs lint --slug curio-s56` returned **0 errors, 0 warnings** (00:59 estimated opener, 14.4-minute estimated total). `git diff --check HEAD -- docs/videos/curio-s56` passed.

The five hashes above are frozen for a **fresh independent R4 source and written-visual check**. These checks do not establish narrative blind-review results, measured TTS duration, generated-image quality, or permission to generate paid media.
