# H12 formal script: independent fact verification, round 2

- Checked: 2026-10-16 (Asia/Taipei).
- Bound `video.json` SHA-256: `5E46DDF2C3DE77641A5FF17C9520255D5F3B003429A64EE1C1CB8C9CDE39E859`.
- Verdict: **HOLD for one precise wording change**. All other checked historical anchors are supported; the prior exhibition-tense blocker is resolved. Do not submit this hash for owner script approval.
- Scope: every changed line in `revision-2.json`, its visual data, a reproducible random third of current scene line/data surfaces, plus YouTube metadata and thumbnail. This is a fresh read of the primary sources, not acceptance of `verify-1.md` or the writer's `claims.md` as proof. Actions, expressions, props, and lighting in illustrative prompts are not asserted as photographed historical events.

## Primary source readback

| Key | Source | Live editorial-UA HTTP | Relevant original evidence |
| --- | --- | ---: | --- |
| NLB | [Northern Lighthouse Board: Flannan Isles](https://www.nlb.org.uk/history/flannan-isles/) | 200 | Transcripts of the 1900-12-26 HESPERUS telegram, Moore's 1900-12-28 letter, and Muirhead's 1901-01-08 investigation report; all three were read. |
| GIBSON | [Wilfrid Wilson Gibson, *Fires, Book I*](https://www.gutenberg.org/cache/epub/42677/pg42677-images.html) | 200 | The title page dates the book **1912** and the poem describes an untouched dinner and overturned chair. The book says some tales were reprinted; it does not date this poem's composition. |
| NRS | [National Records of Scotland exhibition notice](https://nrscotland.gov.uk/latest-news/scotland-s-lighthouse-history-in-exhibition/) | 200 | Published 2026-08-03: Moore's original letter was on display for the first time. Ordinary exhibition ran to 2026-09-25 and a special opening occurred 2026-09-26. |

All three HTTP statuses were read on 2026-10-16 using `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`. The source pages were also opened and read. NLB's transcript has one broken sentence around the investigation's inferred date and ARCHTOR report; the script keeps those as separate evidence.

## New or changed lines

| Line ID | Current claim / check | Primary source | Verdict | Required action |
| --- | --- | --- | --- | --- |
| `i73f`, `kxdb` | Opening describes the untouched meal and toppled chair as a later scene **on paper** and asks who wrote it. | GIBSON; NLB | CONFIRMED | None. The opening does not present the meal as Moore's 1900 observation. |
| `448s` | Moore's later letter recounts his initial outside search. | NLB, Moore letter | CONFIRMED | None. Writing posture is illustrative, not documented. |
| `z4u3`, `7tig`, `phjr`, `m6gi`, `8qci`, `3w38` | McArthur's coat remained, Ducat/Marshall's sea boots and protective outerwear were absent, and Moore linked those garments with trips toward the landings; the order and last actions remain unknown. | NLB, Moore letter and Muirhead report | CONFIRMED | None. The rhetorical question is not offered as a witnessed motive. |
| `8hj7`, `dfa9`, `gqqh`, `a83d` | The investigation moved from intact east-side equipment to west-side damage; the missing box left ropes near the crane, still coiled and not unfastened. | NLB, Moore letter and Muirhead report | CONFIRMED | None. |
| `i9ud` | “一九一二年，吉布森寫下一首…” dates the **act of writing** to 1912. | GIBSON, 1912 title page and reprint note | **NOT FOUND / HOLD** | Source proves 1912 publication, not the composition date. Say the 1912 book **published/contained** the poem, keeping the 1912 poem card and the same scene/line ID. Rebind verification to the revised SHA. |
| `wdik`, `dt4e`, `2kc7`, `4ixq`, `kgfx`, `pxtx` | Moore's letter lacks the untouched meal and toppled chair; those are in Gibson's poem, which is not a 1900 eyewitness account. | NLB; GIBSON | CONFIRMED | None. “1912 詩作” means the dated published source, not a proven composition date. |
| `6fu8`, `d4uq` | Visitors **did** see Moore's original letter during that exhibition; the script now speaks in past tense. Distinguishing witness report from inference is editorial reading, not a newly attributed quotation. | NRS; NLB | CONFIRMED | None. No current visitor access is implied. |
| `s4hn` | Muirhead reports the clock had stopped; its face cannot establish **which date** it stopped. | NLB, Muirhead report | CONFIRMED | None. The second clause is a clearly reasoned limit, not an attributed historical measurement. |
| `k8sw` | Muirhead sought Roderick MacKenzie, found and questioned the two sons who actually observed from shore, then read the Return Book. | NLB, Muirhead report | CONFIRMED | None. Keep their testimony distinct from the ARCHTOR ship report. |

## Reproducible random sample

I enumerated the current 98 narration lines plus 96 scene `data.prompt`/card-data surfaces in scene order (194 surfaces). PowerShell `Get-Random -SetSeed 20261016 -Count 65` selected a random third, sorted by the original inventory index. Every sampled historical anchor was checked directly against the original text above; generic acting, props, light, and camera direction are outside historical proof. The changed-line check above is additional to this sample. `youtube.title`, `youtube.description`, tags, and thumbnail were separately inspected; the disappearance, published poem, documented uncertainty, and “1900 年留下的紀錄” all match the cited sources, while the generic series/category tags carry no historical claim.

| Inventory # | Exact surface | Claim ID | Source | Verdict / reason |
| ---: | --- | --- | --- | --- |
| 1 | arrival-date.lines[jjr5]: 一九〇〇年十二月二十六日，弗蘭南群島。 | H12-C02 | NLB | CONFIRMED; historical anchor matches the source |
| 5 | horn-call.lines[a2ec]: 船上的汽笛響了幾次，還是等不到回應。 | H12-C02 | NLB | CONFIRMED; historical anchor matches the source |
| 7 | rocket-call.lines[xng2]: 船長又發了一枚火箭，燈塔依然沒有動靜。 | H12-C02 | NLB | CONFIRMED; historical anchor matches the source |
| 9 | letter-tease.lines[3nwg]: 兩天後，穆爾把這次登島寫進一封信。 | H12-C03 | NLB | CONFIRMED; historical anchor matches the source |
| 12 | west-tease.data.prompt: Close-up at the west landing of a rocky Scottish island under an overcast sky, one inspector stops at a ben… | H12-C09 | NLB | CONFIRMED anchor; generic visual action is illustrative |
| 17 | boat-launched.lines[xf7d]: 小艇靠上東側碼頭，換班的穆爾先跳到了岸上。 | H12-C03 | NLB | CONFIRMED; historical anchor matches the source |
| 18 | boat-launched.data.prompt: Wide shot at a Scottish island lighthouse during a daytime relief visit in 1900, one relief keeper steps fr… | H12-C03 | NLB | CONFIRMED anchor; generic visual action is illustrative |
| 19 | boat-waits.lines[874p]: 同行的人留在艇裡，等他從燈塔回來報訊。 | H12-C03 | NLB | CONFIRMED; historical anchor matches the source |
| 20 | boat-waits.data.prompt: Medium shot at a Scottish island lighthouse during a daytime relief visit in 1900, one sailor waits beside … | H12-C03 | NLB | CONFIRMED anchor; generic visual action is illustrative |
| 22 | letter-recalled.data.prompt: Close-up at a Scottish island lighthouse during a daytime relief visit in 1900, one keeper writes on a blan… | H12-C03 | NLB | CONFIRMED anchor; generic visual action is illustrative |
| 28 | door-boundary.data.prompt: Medium shot in a public archive exhibition room during opening hours, one archivist compares a plain door l… | H12-C04 | NLB | OUT OF SCOPE; no checkable historical claim |
| 29 | cold-fire.lines[5udf]: 穆爾看了火爐，判斷已經好幾天沒生火。 | H12-C04 | NLB | CONFIRMED; historical anchor matches the source |
| 30 | cold-fire.data.prompt: Close-up at a Scottish island lighthouse during a daytime relief visit in 1900, one keeper bends toward a c… | H12-C04 | NLB | CONFIRMED anchor; generic visual action is illustrative |
| 40 | room-question.data.prompt: Medium close-up at a Scottish island lighthouse during a daytime relief visit in 1900, one keeper pauses at… | H12-C05 | NLB | CONFIRMED anchor; generic visual action is illustrative |
| 46 | who-missing.data.prompt: Close-up in a public archive exhibition room during opening hours, one archivist opens three plain personne… | H12-C01 | NLB | CONFIRMED anchor; generic visual action is illustrative |
| 60 | clothing-inference.data.prompt: Close-up inside a Scottish island lighthouse during a daytime relief visit in 1900, one relief keeper looks… | H12-C12 | NLB | CONFIRMED anchor; generic visual action is illustrative |
| 61 | landing-clothes.lines[m6gi]: 他說，那些裝備是他們下到碼頭附近時才會穿的。 | H12-C12 | NLB | CONFIRMED; historical anchor matches the source |
| 65 | sequence-unknown.lines[3w38]: 衣物排不出三人的先後，也沒有人看見他們離開。 | H12-C12 | NLB | CONFIRMED; historical anchor matches the source |
| 66 | sequence-unknown.data.prompt: Medium shot at a reader's desk, one reader leaves three plain figure tokens in an unordered cluster beside … | H12-C12 | NLB | CONFIRMED anchor; generic visual action is illustrative |
| 67 | work-question.lines[h8mk]: 穆爾的信記下做完的工作；調查報告能不能把時間接起來？ | H12-C07 | NLB | CONFIRMED; historical anchor matches the source |
| 68 | work-question.data.prompt: Medium close-up at a Scottish island lighthouse during a daytime relief visit in 1900, one keeper lifts a s… | H12-C07 | NLB | CONFIRMED anchor; generic visual action is illustrative |
| 69 | slate-entry.lines[cuxc]: 調查報告補上信裡沒有寫的石板，上面留著待抄的觀測。 | H12-C07 | NLB | CONFIRMED; historical anchor matches the source |
| 70 | slate-entry.data.prompt: Wide shot in a lighthouse record room during an investigation, one investigator holds an unmarked slate abo… | H12-C07 | NLB | CONFIRMED anchor; generic visual action is illustrative |
| 71 | log-date.lines[s7pw]: 日誌本最後寫到十二月十三日。 | H12-C07 | NLB | CONFIRMED; historical anchor matches the source |
| 78 | morning-reading.data.prompt: Medium close-up in a lighthouse record room during an investigation, one investigator studies a plain barom… | H12-C07 | NLB | CONFIRMED anchor; generic visual action is illustrative |
| 79 | extinguish-time.lines[yt2k]: 石板也留了當天早上熄燈的時間。 | H12-C07 | NLB | CONFIRMED; historical anchor matches the source |
| 80 | extinguish-time.data.prompt: Wide shot in a lighthouse record room during an investigation, one keeper places a small unlit lamp beside … | H12-C07 | NLB | CONFIRMED anchor; generic visual action is illustrative |
| 84 | work-date-inference.data.prompt: Close-up in a lighthouse record room during an investigation, one investigator places the slate beside a cl… | H12-C08 | NLB | CONFIRMED anchor; generic visual action is illustrative |
| 89 | report-delay.lines[ds8v]: 可是這個消息，在失蹤被發現之後才傳到燈塔局。 | H12-C14 | NLB | CONFIRMED; historical anchor matches the source |
| 92 | shore-observers.data.prompt: Close-up in a lighthouse record room during an investigation, one shore observer raises a telescope beside … | H12-C14 | NLB | CONFIRMED anchor; generic visual action is illustrative |
| 93 | visibility-question.lines[nxpd]: 但隔著海看不到光，能直接當成燈已經熄了嗎？ | H12-C14 | NLB | CONFIRMED; historical anchor matches the source |
| 97 | shore-log.lines[szic]: 監督翻查岸上的紀錄，發現看不見並不是新鮮事。 | H12-C14 | NLB | CONFIRMED; historical anchor matches the source |
| 99 | several-nights.lines[s9zp]: 天氣阻擋視線時，連續四五晚看不見燈，也曾發生。 | H12-C14 | NLB | CONFIRMED; historical anchor matches the source |
| 100 | several-nights.data.prompt: Medium shot in a lighthouse record room during an investigation, one observer lowers a telescope in thick c… | H12-C14 | NLB | CONFIRMED anchor; generic visual action is illustrative |
| 101 | two-records.lines[ufsf]: 所以過船的通報和岸上的紀錄，必須分開判讀。 | H12-C14 | NLB | CONFIRMED; historical anchor matches the source |
| 110 | west-recalled.data.prompt: Close-up at the west landing of a rocky Scottish island under an overcast sky, one inspector stops at a ben… | H12-C11 | NLB | CONFIRMED anchor; generic visual action is illustrative |
| 111 | sea-blocks-descent.lines[ijjn]: 海況讓監督下不到碼頭，只能走到起重機平台。 | H12-C10 | NLB | CONFIRMED; historical anchor matches the source |
| 116 | box-location.data.prompt: Medium shot at the west landing of a rocky Scottish island under an overcast sky, one inspector points towa… | H12-C10 | NLB | CONFIRMED anchor; generic visual action is illustrative |
| 119 | height-card.lines[efzu]: 這是設施所在的高度，並不是當時量到的浪高。 | H12-C10 | NLB | CONFIRMED; historical anchor matches the source |
| 121 | box-gone.lines[dfa9]: 放繩具的木箱不見了；繩束卻留在岩縫和起重機旁。 | H12-C11 | NLB | CONFIRMED; historical anchor matches the source |
| 123 | rope-question.lines[gqqh]: 那些繩子，失蹤當天有人用過嗎？ | H12-C11 | NLB | CONFIRMED; historical anchor matches the source |
| 126 | coiled-rope.data.prompt: Close-up at the west landing of a rocky Scottish island under an overcast sky, a gloved hand holds a neatly… | H12-C11 | NLB | CONFIRMED anchor; generic visual action is illustrative |
| 129 | crane-covered.lines[dvmg]: 捲筒的帆布罩還綁著，沒有顯示有人正在動它。 | H12-C11 | NLB | CONFIRMED; historical anchor matches the source |
| 136 | buoy-question.data.prompt: Wide shot at the west landing of a rocky Scottish island under an overcast sky, one inspector studies an em… | H12-C18 | NLB | CONFIRMED anchor; generic visual action is illustrative |
| 139 | buoy-inference.lines[i3cg]: 因此他判斷，救生圈是被海水從固定處撕掉的。 | H12-C18 | NLB | CONFIRMED; historical anchor matches the source |
| 141 | departure-question.lines[7nu6]: 西側的損害能說明三人最後如何失蹤嗎？ | H12-C11 | NLB | CONFIRMED; historical anchor matches the source |
| 143 | evidence-gap.lines[fbx9]: 現場留下受損的設施，卻沒有留下最後一刻的人證；監督會怎麼解釋？ | H12-C13,H12-C17 | NLB | CONFIRMED; historical anchor matches the source |
| 144 | evidence-gap.data.prompt: Close-up in a coastal investigation office in winter, one inspector holds a pen above an unfinished blank r… | H12-C13,H12-C17 | NLB | CONFIRMED anchor; generic visual action is illustrative |
| 145 | investigator-opinion.lines[ecsy]: 一九〇一年一月八日，他寫下自己認為最可能的解釋。 | H12-C09,H12-C13 | NLB | CONFIRMED; historical anchor matches the source |
| 146 | investigator-opinion.data.prompt: Medium close-up in a coastal investigation office in winter, one inspector signs a blank report with a care… | H12-C09,H12-C13 | NLB | CONFIRMED anchor; generic visual action is illustrative |
| 147 | secure-gear.lines[e5pv]: 他的推想是，三人到西側附近，想把繩具箱等器材保住。 | H12-C13 | NLB | CONFIRMED; historical anchor matches the source |
| 150 | wave-hypothesis.data.prompt: Medium shot in a coastal investigation office in winter, one inspector points to an unlabelled water-flow s… | H12-C13 | NLB | CONFIRMED anchor; generic visual action is illustrative |
| 153 | wind-compared.lines[v7k5]: 他也考慮過強風吹走人的可能，還比較了風向。 | H12-C19 | NLB | CONFIRMED; historical anchor matches the source |
| 155 | west-wind.lines[e8ux]: 當時的西風，會把人推向島上較高的地方。 | H12-C19 | NLB | CONFIRMED; historical anchor matches the source |
| 159 | poem-bridge.lines[e2rt]: 又過了十多年，這間空屋在另一張紙上有了新畫面。 | H12-C15,H12-C17 | NLB + GIBSON | CONFIRMED; historical anchor matches the source |
| 161 | poem-recalled.lines[i9ud]: 一九一二年，吉布森寫下一首關於這座燈塔的詩。 | H12-C15 | GIBSON | HOLD; 1912 composition date not established, publication is |
| 165 | overturned-chair.lines[uedh]: 同一段裡，還有一張翻倒在地的椅子。 | H12-C15 | GIBSON | CONFIRMED; historical anchor matches the source |
| 168 | poem-effect.data.prompt: Medium shot at a reading table beside a window, one reader pauses with a startled expression above the poet… | H12-C15 | GIBSON | CONFIRMED anchor; generic visual action is illustrative |
| 170 | memory-recalled.data.prompt: Close-up at a reading table beside a window, one archivist returns a poetry book to one side and lifts a pl… | H12-C03,H12-C15 | NLB + GIBSON | CONFIRMED anchor; generic visual action is illustrative |
| 172 | kitchen-recalled.data.prompt: Medium close-up at a reading table beside a window, one archivist places a clean pot token beside a plain i… | H12-C05,H12-C15 | NLB + GIBSON | CONFIRMED anchor; generic visual action is illustrative |
| 177 | no-fake-diary.lines[kgfx]: 把這幕搬回事發當天，就跨過了文件無法證實的那一步。 | H12-C17 | NLB | CONFIRMED; historical anchor matches the source |
| 182 | letter-fate.data.prompt: Wide shot at a reading table beside a window, one archive attendant opens a shallow document drawer, center… | H12-C16 | NRS | CONFIRMED anchor; generic visual action is illustrative |
| 185 | exhibit-new.lines[6fu8]: 在那場展覽裡，人們曾親眼看見這封信。 | H12-C16 | NRS | CONFIRMED; historical anchor matches the source |
| 186 | exhibit-new.data.prompt: Close-up in a public archive exhibition room during opening hours, one visitor leans toward a glass documen… | H12-C16 | NRS | CONFIRMED anchor; generic visual action is illustrative |
| 193 | ending-outro.lines[wpvq]: 訂閱奇聞檔案局，一起追問故事的來處。 | H12-C16,H12-C17 | NRS + NLB | OUT OF SCOPE; no checkable historical claim |

## Result and limits

- **24 changed line IDs** and their visual data were checked. The only factual HOLD is `i9ud`. Script changes made by this verifier: **0**; unsupported claims: **1**; all other changed historical anchors: **confirmed**. A corrected script requires a new SHA-bound verification receipt; this receipt does not approve a future edit automatically.
- Of the **65 sampled scene surfaces** (36 narration, 29 scene data), `poem-recalled.lines[i9ud]` repeats the same HOLD, two surfaces contain no checkable historical claim (`door-boundary.data.prompt`, the subscription line), and the other 62 have supported historical anchors or clearly illustrative actions. Sampling is not a claim of exhaustive re-verification of all 194 current scene surfaces; the prior 207-item full audit remains bound only to its earlier SHA.
- NLB's period report directly supports `s4hn`'s stopped clock and `k8sw`'s two shore observers. It does not date the clock's stopping, and the script does not use the clock as a loss-time measurement. NRS supports the now-past-tense exhibition sentence `6fu8`; this fixes the first round's factual blocker.
- The 1912 book's date supports a **published poem** and cards labelled “1912 詩作.” It does not support “吉布森在 1912 年寫下” in `i9ud`. The editorially narrow repair is publication/collection wording; do not assert a composition year without a dated original manuscript or publication record.
- The potentially misleading numbers are handled: 70 and 110 feet locate structures, not a measured wave; 15 December afternoon is Muirhead's inference; the midnight ARCHTOR observation is separate from the shore Return Book. The official NLB transcript itself has a broken sentence around the latter two topics, so the script appropriately avoids a more precise event sequence.
- `youtube.title`, description, tags and thumbnail were read. No additional historical mismatch was found; the description correctly distinguishes the 1900 letter/report from the poem, labels the images as AI illustrations, and does not claim a certain death scene.
- There are no narration lines over 40 characters, no Latin/URL/parenthetical pronunciation issue in narration, and no unmarked claim that the narrator personally witnessed the event. Muirhead's wave explanation remains attributed as his opinion. No mismatch with the brief's stated evidentiary boundary was found.
- Independent local lint on this exact SHA: **0 errors**, 3 existing setting-word frequency warnings (`lighthouse`, `island`, `during`); estimated 9.1 minutes is not measured audio. `git diff --check` passed.
- **Fact gate: HOLD.** The independent storytelling gate is separate and also currently HOLD (`payoffs`, `no_recap` in the fresh thirteen-question blind review). The owner must decide whether another narrow script revision is permitted after two revisions. No paid media or backend script submission is authorized by this receipt.
