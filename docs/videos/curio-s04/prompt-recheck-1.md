# S04 prompt-only restart QA

**PASS for the frozen prompt file at SHA-256 `ce08b26f6b9d8529245b9c2aa633335c083247410cb299bb0063d6c457db4e64`.** This approves the prompt revision for image generation, subject to inspecting the newly generated stills; it does not approve any of the 20 blocked initial JPEGs listed in `/tmp/curio_s04_initial_image_qa.md`.

## Reproducible checks

| Item | Result |
| --- | --- |
| `docs/videos/curio-s04/video.json` SHA-256 | `ce08b26f6b9d8529245b9c2aa633335c083247410cb299bb0063d6c457db4e64` |
| `docs/videos/curio-s04/script.md` SHA-256 | `2201aaa948660f2375d60d5fe598a87c4a61e10d22cf32c137c2702d1ba494ac` |
| `docs/videos/curio-s04/claims.md` SHA-256 | `67862926e1e395fc27d9e1a319d46239e6820c33814d337f92fa292fe91ae928` |
| Parsed JSON against `HEAD:docs/videos/curio-s04/video.json` | Exactly **67 leaf changes**, all `scenes[*].data.prompt`; 92 scenes, 91 shots. No narration lines, scene IDs, chapter, camera, look, voice, music, source, claims, or other top-level/scene data changed. `script.md` and `claims.md` are unmodified in `git status`. |
| `node tools/video/cli.mjs lint --slug curio-s04` | Exit 0; **0 errors, 0 warnings**; estimated 8.1 minutes, 92 lines. |
| Series look and names | `look` remains exactly `{ "preset": "cute-mystery" }`; all 91 image prompts have **zero direct historical personal names** matching Zhou Yu, Sun Quan, Cao Ren, Lu Su, Sun Ce, Zhuge Liang, Liu Bei, Cheng Pu, Gan Ning, Ling Tong, Sun Yu, Liu Zhang, or Zhang Lu. The earlier 17 name-bearing leaves were replaced by role and appearance descriptions. |

## Prompt IDs checked

The 21 changed prompts within the first 33 shot records are: `pack-for-west`, `approval`, `succession-hook`, `same-age`, `sunce-dies`, `serve-sunquan`, `debate`, `why-surrender`, `zhou-argues`, `water-sickness`, `request-thirty`, `city-grain`, `jiangling-not-over`, `ning-ahead`, `rescue-request`, `leave-ling`, `ning-freed`, `right-rib`, `severe-wound`, `cao-ren-hears`, `walks-camp`. This covers **all 20 blocked selected frames** and the unselected `pack-for-west` shot from the initial image QA.

The 46 changed later prompts are: `enemy-recedes`, `still-governing`, `future-hook`, `liu-takes-jingzhou`, `liu-arrives`, `liu-visits`, `quan-declines`, `not-anger`, `zhou-audience`, `west-opening`, `cao-busy`, `ask-sunyu`, `take-shu`, `hold-west`, `turn-north`, `yes-to-plan`, `return-jiangling`, `what-stopped`, `letter-first`, `prepare-future`, `unfinished-frontier`, `liubei-nearby`, `people-unsettled`, `replacement`, `lusu-history`, `lusu-merit`, `last-words`, `sudden-illness`, `life-length`, `regret-plan`, `sunquan-mourns`, `meet-at-wuhu`, `pay-funeral`, `kingmaker`, `succeed`, `chengpu-takes`, `four-thousand`, `move-lukou`, `novel-obstacles`, `letter-warns`, `novel-liuzhang`, `letter-difficult`, `novel-sigh`, `after-letter`, `novel-last-order`, `famous-cry`.

The 12 acceptable cached selected-shot prompts are byte-for-byte unchanged versus HEAD: `old-wound-question`, `novel-letter-question`, `last-line-question`, `cao-south`, `jingzhou-navy`, `cao-threat-question`, `given-command`, `cao-withdraws`, `beside-jiangling`, `ride-to-ning`, `arrow-awaits`, `zhou-rises`.

## Historical and visual sense check

- The blocked cap/office/classroom/roller-shutter cases now call for late-Han-style wrapped hair, simple robes or lamellar vest, timber/woven-mat halls, low wooden tables, an **earthen** Baqiu road, a timber mourning hall, wooden granary doors, timber Yiling gates, and plain unlettered maps. These are illustrative setting cues, not claims of a precise reconstruction.
- `serve-sunquan` now has **one** foreground young ruler listening to counsel; `debate` has an uncrowned young ruler rather than the initial 208 imperial crown. `leave-ling` puts a counter behind the river line to symbolize keeping Ling Tong in the rear. `cao-ren-hears` now has the garrison chief listening to an off-frame report with a small background line of soldiers.
- `right-rib` places a short arrow at the **right ribs** without blood; `severe-wound` shows subdued rest in a war tent. These match the sourced arrow wound and heavy injury while adding no link between that old injury and the later fatal illness. `sunquan-mourns` explicitly uses an **undyed plain mourning gown**, matching `素服舉哀`.
- The westward and northward maps remain a **proposal** in council or travel preparation; they do not depict Shu conquered. Travel illness, recommendation of Lu Su, Sun Quan's mourning, and Lu Su/Cheng Pu succession remain in their narrated sequence. The eight changed novel shots preserve the visible blank illustrated-storybook page border, distinguishing the later fictional letter and famous cry from the chronicle account.
- The final 17 descriptor substitutions preserve each prior action, period anchor, and single foreground subject: `pack-for-west`, `same-age`, `serve-sunquan`, `debate`, `zhou-argues`, `request-thirty`, `severe-wound`, `future-hook`, `liu-visits`, `ask-sunyu`, `turn-north`, `prepare-future`, `people-unsettled`, `lusu-history`, `sudden-illness`, `sunquan-mourns`, `kingmaker`. No changed prompt asserts a new historical event or medical diagnosis.

## Audit trail and acceptance boundary

The intermediate SHA `55b9d0df712bcadfd659dd0f40fafa50867a5b724a78a4c3dc4daab895143854` was **BLOCKED** for 17 direct historical names contrary to the curio series rule to describe deceased figures visually rather than naming them in image prompts. The six earlier content/composition issues (`serve-sunquan`, `sunquan-mourns`, `cao-ren-hears`, `leave-ling`, `succession-hook`, `sunce-dies`) were already repaired in that version and remain repaired in the final file. The final SHA above passes the prompt-only audit.

Image acceptance still needs a human review of the resulting manifest and contact sheets. The first auto-judge passed several clearly modern or contradictory frames, so its green flag alone is insufficient evidence for those 20 shot IDs.
