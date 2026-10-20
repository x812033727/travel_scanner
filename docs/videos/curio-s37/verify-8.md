# S37 R7 audio wording repair and review handoff

2026-10-20. The exact R6 narration passed the independent written gate but its Gemini Sulafat audio failed three full `check-audio` passes despite two targeted retakes. Results were 31, then 12, then **11 flagged lines**, each pass checking all 91 spoken lines. The final R6 flag IDs were `pl008, pl009, pl020, pl017, pl051, pl052, pl055, pl026, pl059, pl085, pl099`. Recurring name transcriptions included 小普林尼, 叔父 and 米塞努姆; some changed meaning, such as 李維 heard as 李敖 and 信裡 heard as 心裡. No R6 audio approval was given, and no MiniMax image or music generation began. Details of the first two passes and the whole episode US$3.64 image/music cap are in [verify-7.md](verify-7.md).

R7 changes only the **spoken text of those 11 lines**, in `video.json`, the matching 11 `claims.md` rows and regenerated `script.md`. Shot prompts, order, `look`, loops, image count and sources are unchanged. Each replacement is narrower or equivalent to the same pinned Pliny passage:

| ID | R7 wording and reason |
| --- | --- |
| `pl008` | 「少年的母親請艦隊司令抬頭，看遠處那團不尋常的雲。」 keeps the mother's call to the previously identified fleet commander without reintroducing two repeatedly misheard names. |
| `pl009` | 「他剛吃過一點東西，本來又回去看書。」 uses the established subject rather than repeating 叔父. |
| `pl020` | 「雲一會兒亮，一會兒暗；寫信時，他猜是泥土和灰混進了雲裡。」 retains the letter writer's inference and avoids 信裡/心裡 confusion. |
| `pl017` | 「那張字條來自山腳下的瑞克蒂娜；她只能從海上逃。」 preserves the note, sender and only escape route. |
| `pl051` | 「他說那時自己十八歲，居然還在讀羅馬史書，一面做摘錄。」 describes the source's Livy extracts without a name the checker twice heard as 李敖. |
| `pl052` | 「一位從西班牙來的朋友，看見少年還拿著書，停住腳步。」 omits the friend's already established relation to the elder Pliny, which the checker twice heard as 神父. |
| `pl055` | 「母子起身離開小院，朝城外走去。」 uses the already established town rather than repeating a place name the checker repeatedly misheard. |
| `pl026` | 「身後的人群一路推擠，母子也被迫往前走。離開房屋後，就能站穩嗎？」 preserves the crowd's pressure and the next danger without 逃/嚎 or 像/想 confusion. |
| `pl059` | 「少年抬頭看向海灣另一邊；雲又變成什麼樣子？」 keeps the same viewpoint and question, using the established young Pliny as subject. |
| `pl085` | 「母子回到原來的城鎮；這一夜還能好好休息嗎？」 keeps their return to Misenum and the following night's question. |
| `pl099` | 「兩封信把地點說清楚了：這位少年當時在海灣對岸的軍港，不在龐貝。」 answers the Pompeii question by pointing back to Misenum, identified by name and fleet command earlier in `pl007`, without another unstable pronunciation. |

R7 SHA-256: `script.md` `b8c6cca751dc9801d09f8f4cb17b632e73cd7cf5b9ece13094c7550511490359`; `video.json` `31eb25bf7130bbcbd1e1a6f9f0bfbe78154dcf13d527e27738ea5dd4a05c7de2`; `claims.md` `2beae04c177796443055a56e0c6ef10e1a40b5163e4b812cdfe0b3a5b9d6730a`. The 91 spoken IDs/texts match the 91 claim rows in order, with zero mismatches. `lint --json` reports **0 errors, 0 warnings**, 91 lines and 9.31 estimated minutes. This is an estimated length only; R7 body length must be remeasured after TTS.

The R6 blind review, source audit, narrative record, exact-script approval, timeline and audio receipts are **not transferable** to this wording change. The fresh context-isolated reader sealed [13/13 Yes](verify-8-r7-blind.md), and the line-cited [formal R7 answers](narrative-answers-r7.json) passed the official importer. The subsequent [full R7 source/prompt audit](verify-8-r7-source.md) found a **material blocker**: `pl020` sounds as though the uncle wrote the letter and inferred the cloud's cause. It also identified the opening's one-letter implication and smaller source/prompt precision points. R7 was **not** approved or synthesized. [R8](verify-9.md) corrects the findings and requires a new independent exact-hash gate. The US$3.64 pre-art whole episode image/music cap must be checked again against the eventual final timeline; S04/S23 shared MiniMax quota and branded intro/outro gates remain in force.
