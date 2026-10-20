# R10 fresh blind narrative panel B — curio-s49

**Result:** 12 pass, 1 fail. This is a script-only judgment of the 13 official questions embedded in the narrative command output.

**Evidence basis:** `NODE_USE_ENV_PROXY=1 NODE_NO_WARNINGS=1 VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs narrative --slug curio-s49 --json`. All prose judgments use only its `narration` string. SHA-256 of that string's UTF-8 bytes: `85b3b2473e49caa9cfe8fc8ccfe2525599e9f932208bdb1480dad9860b3695c0`. SHA-256 of `docs/videos/curio-s49/script.md` raw bytes, hashed without reading its prose: `c6389ff27c36856a914442644b71f746c66a89ddb1bd8f0f14a3f086d09fa51c`.

| Official ID | Verdict | Concrete evidence |
| --- | --- | --- |
| `scene_first` | Pass | `moon001`–`moon004`: 1835 年八月，紐約讀者面前出現《太陽報》及其好望角發現。 |
| `no_spoiler` | Pass | `moon004`–`moon008`: 信、光學、第二份觀測及其他編輯反應都停在疑問。 |
| `one_line` | Pass | `moon009`, `moon032`, `moon056`, `moon079`, `moon100`, `moon112`: 從權威包裝走到報導內容與後來的反應。 |
| `no_toc` | Pass | `moon008`, `moon016`, `moon055`, `moon078`, `moon111`: 以故事問題轉場，沒有宣告影片目錄。 |
| `chapters_link` | Pass | `moon008`→`moon009`, `moon031`→`moon032`, `moon055`→`moon056`, `moon078`→`moon079`, `moon099`→`moon100`, `moon111`→`moon112`: 各章首接住上一章的具體物件或問題。 |
| `open_loops` | Pass | `moon004`, `moon015`, `moon028`, `moon038`, `moon050`, `moon061`, `moon073`, `moon083`, `moon094`, `moon104`, `moon111`, `moon121`, `moon128`: 問題間隔均在 90 秒內。 |
| `payoffs` | **Fail** | `moon018` 問增刊從哪裡翻到；`moon019` 只說它是文章自稱的出處。`moon023`、`moon132` 也沒有明確交代該增刊能否查到或查閱位置。 |
| `no_recap` | Pass | `moon003`→`moon009`、`moon024`→`moon093` 是明確回呼；`moon123`–`moon125` 提數字後直接評估證據。 |
| `chapters_are_events` | Pass | `moon001`, `moon009`, `moon032`, `moon056`, `moon079`, `moon100`, `moon112`: 七個章名都是發生的事或揭曉。 |
| `outro_no_next` | Pass | `moon999a`–`moon999c`: 沒有提下一支影片或下一集。 |
| `opening_hooks` | Pass | `moon004`–`moon007`: 場景之後留下信、光學、第二份觀測、其他編輯四個鉤子。 |
| `one_thread` | Pass | `moon008`, `moon016`, `moon041`, `moon070`, `moon091`, `moon118`, `moon132`: 同一條『報紙如何把故事寫得像觀測』的線。 |
| `no_detour` | Pass | `moon096`, `moon103`, `moon108`, `moon123`, `moon125`, `moon130`: 後續奇景、火災與傳播數字都服務於報導可信度及核對問題。 |

**Revision target:** Give `moon018` a direct payoff: say whether the alleged supplement is independently locatable, and what the checked record establishes. Keep the claim bounded by the available evidence.
