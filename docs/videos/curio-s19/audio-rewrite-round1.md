# S19 audio rewrite round 1 — 2026-10-20

The previously reviewed R5 `script.md` was SHA-256 `a68cc615c3d79ad7b1cac7002d5a20179b2f6cc09b1e739071e4f479e0d7eb5a`. Its 110-line recording had twelve flags after two permitted retake rounds; [the frozen final flag receipt](audio-flags-final.json) records them. The first two retake rounds cost 520 and 257 billable characters, as [R5 verification](verify-5.md) records. The local Whisper second opinion could not download its model because the proxy returned HTTP 403; it supplied no transcript.

This is the **first wording rewrite round**, with only the twelve flagged narration IDs changed. No image generation or new TTS call occurred during this handoff. The new, generated [script.md](script.md) has SHA-256 `0ba634669a95b549f32e2d3fbc9250a68454ed69099e6940c1e819269836ea75`; its narrative hash is `8b2e8d7a0233ae93`. The first chapter label now uses 「刊出」 to match the narration. The previous R5 local script approval is stale for this version. It was delegated production authorization, not an owner-personal reading.

| ID | R5 script | Last Gemini transcript | R6 wording |
| --- | --- | --- | --- |
| `et001` | 一八八七年二月，巴黎一份報紙排出一封抗議鐵塔的信。 | 一八八七年二月，巴黎一份報紙刊出一封抗議鐵塔的信 | 一八八七年二月，巴黎一份報紙刊出一封抗議鐵塔的信。 |
| `et014` | 在他們眼中，鐵製高塔一進城，這幅畫就會走樣。 | 在他們眼中，鐵製高塔一建成，這幅畫就會走樣。 | 在他們眼中，鐵製高塔一建成，這幅畫就會走樣。 |
| `et015` | 信說，人們早把它叫作「巴別塔」。 | 據說，人們早把它叫做巴別塔。 | 抗議信寫道，人們早把它叫作「巴別塔」。 |
| `et020` | 外國遊客還沒來，信已想像他們嘲笑法國品味。 | 外國遊客還沒來，心已想像他們嘲笑法國品味 | 外國遊客還沒來，抗議者就想像他們嘲笑法國品味。 |
| `et022` | 這是請願書描出的未來景象，不是實測的塔影。 | 這是請願書描繪出的未來景象，不是實測的塔影。 | 這是請願書描繪出的未來景象，不是實測的塔影。 |
| `et027` | 信已登報；被抗議的艾菲爾，會先答哪一點？ | 星儀燈號， 被抗議的艾菲爾會先打哪一點？ | 這封抗議信刊出後，艾菲爾先回應了什麼？ |
| `et030` | 他說加尼耶也在塔的委員會，會裡做過的事都曾得到他的同意。 | 他說賈尼耶也在塔的委員會，會裡做過的事都曾得到他的同意。 | 他說，建築師加尼耶也在塔的委員會，會裡做過的事都曾得到他的同意。 |
| `et076` | 二十多年後，費里耶的一份報告被呈交科學院。 | 二十多年後，費立葉的一份報告被呈交科學院 | 二十多年後，軍官費里耶的一份報告被呈交科學院。 |
| `et089` | 有了這條跨海聯絡，報導還想拿它做什麼？ | 有了這條跨海聯絡，寶島還想拿它做什麼？ | 有了這條跨海聯絡，報紙還想拿它做什麼？ |
| `et096` | 沒有；這則短訊完全沒有寫市府的決議。 | 沒有，這則簡訊完全沒有寫市府的決議。 | 沒有；這篇報導沒有記載市府的決議。 |
| `et098` | 但要說無線電因此讓塔免拆，還缺契約和市府紀錄。 | 但要說，無線電因此讓它免拆，還缺契約和市府紀錄。 | 但要說無線電因此讓鐵塔免於拆除，還缺契約和市府紀錄。 |
| `et101` | 還記得那二十年嗎？已讀報紙裡，沒有到期拆塔令。 | 還記得那二十年嗎？一度報紙裡，沒有到期拆塔令。 | 還記得那二十年嗎？我們讀過的報紙裡，找不到到期拆塔令。 |

The edits retain the same source boundary: the 1887 *Le Rappel* petition and Eiffel interview, and the 1913 *L’Illustration* wireless note. In particular, 「建築師加尼耶」 repeats the role already stated at `et025`; 「軍官費里耶」 follows the 1913 source's *commandant Ferrié*. The ending still says the read newspapers lack a demolition order and does not claim wireless alone saved the tower. [claims.md](claims.md) has the same twelve exact new sentences with their pinned source links.

**Checks completed:** `rewriteProblems` accepted all twelve lines with no changed numeric, Latin, or dictionary tokens; `lint --slug curio-s19 --json` returned zero errors and zero warnings. `tts --dry-run` shows exactly twelve requests pending and about 274 billable characters, with Gemini Sulafat available. The revised script's **estimated** body from the second chapter to the outro is 501.8 seconds (8:21.8); R5's **measured** body was 510.2 seconds (8:30.2). The R6 duration remains unmeasured until TTS.

**Next gate:** give a fresh source-isolated reader this exact R6 script hash and the generic thirteen narrative questions, then have an independent reviewer check its source claims against the pinned newspapers. Preserve the raw answers and exact-hash receipts. After those pass, record only the delegated script gate actually granted, run one R6 TTS pass, and repeat `check-audio`. If any names or homophones remain flagged, use at most one further wording round and new exact-hash reviews; otherwise leave the audio gate for the owner. Do not start images before zero audio flags and the whole-episode image cap are confirmed.
