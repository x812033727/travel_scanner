# S04 independent review — 周瑜

Review date: 2026-10-19. **Script snapshot SHA256:** `d08160d898eb254766c0f83c48b6a8a573afd1a0945b5cd190ea7463d6cc2e60` (`script.md`, before any later revision). I read only that script and the `narrative` rendering for the blind pass, fixed the answers in `/tmp/curio_s04_blind_answers.json`, and only then opened `research.md`, `claims.md`, and `video.json`. `VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs narrative --slug curio-s04 --answers /tmp/curio_s04_blind_answers.json` failed five required questions. No media was purchased or generated for this review.

## Blind narrative panel

| Question | Yes? | Exact narration evidence and reason |
| --- | --- | --- |
| `scene_first` | Yes | `[s04001 00:00]` 「建安十五年，周瑜在江陵準備一趟向西的遠行。」 is a specific person acting in a dated place. |
| `no_spoiler` | Yes | `[s04002 00:05]` 「行裝卻沒能帶到終點」 withholds why; `[s04006 00:28]` still asks how the two accounts end. |
| `one_line` | No | `[s04039 03:11]`–`[s04047 03:48]` tell the historical wound and its unknown course; `[s04085 07:06]`–`[s04093 07:50]` return to the wound in the novel. `[s04063 05:04]`–`[s04075 06:07]` and `[s04095 08:02]`–`[s04101 08:35]` likewise revisit the westward journey and death. The comparison is relevant, but it is a second chronological telling. |
| `no_toc` | Yes | `[s04049 03:58]` 「下一項計畫」 refers to Zhou's next proposal, not the video's structure; there is no chapter list. |
| `chapters_link` | No | `[s04021 01:45]` asks who receives command; chapter opening `[s04022 01:50]` restates Cao's advance and does not answer until `[s04025 02:04]`. `[s04049 03:58]` promises a farther plan, but the next opening `[s04050 04:03]` starts the separate Liu Bei containment proposal; the westward plan waits until `[s04055 04:29]`. |
| `open_loops` | Yes | Questions/turns at `[s04003 00:11]`, `[s04016 01:21]`, `[s04030 02:30]`, `[s04042 03:25]`, `[s04054 04:24]`, `[s04064 05:09]`, `[s04089 07:29]`, and `[s04096 08:06]` keep gaps under 90 seconds. This measures frequency; it does not certify each payoff. |
| `payoffs` | No | `[s04042 03:25]` asks what would happen to morale **if he stayed in bed**; `[s04043 03:30]`–`[s04045 03:36]` instead say what actually happened when he rose. `[s04062 04:59]` calls back the opening journey, and `[s04063 05:04]` repeats the halted-plan premise before `[s04065 05:14]` supplies the illness. The `video.json` loop metadata changes the question at s04042 into “can he rise,” which is not the voiced question. |
| `no_recap` | No | `[s04100 08:29]` says both 「沒有」 and 「史書沒有這聲長嘆」 in the same line after `[s04099 08:23]` asks the question. `[s04072 05:51]`–`[s04073 05:58]` establish no illness name, then `[s04083 06:52]` returns to inability to diagnose. |
| `chapters_are_events` | Yes | Scene headings such as 「中了箭，他還巡營」 at `[s04039 03:11]`, 「孫權答應取蜀」 at `[s04050 04:03]`, and 「小說讓諸葛亮來信」 at `[s04085 07:06]` name actions or discoveries. |
| `outro_no_next` | Yes | `[s04103 08:50]` 「下次聽到那聲…」 means the next time the viewer hears the saying; `[s04104 08:57]` is a subscribe request, not a tease for another episode. |
| `opening_hooks` | Yes | `[s04003 00:11]` wound, `[s04004 00:17]` old general and wine, `[s04005 00:23]` letter, and `[s04006 00:28]` Baqiu versions give four future moments. |
| `one_thread` | Yes | `[s04001 00:00]` establishes Zhou's interrupted westward journey; `[s04050 04:03]`–`[s04075 06:07]` reach the illness, and `[s04102 08:42]` answers the title through the novel comparison. |
| `no_detour` | No | `[s04014 01:11]`–`[s04015 01:17]` spend two lines on his music ear without a later tie to the journey or death. `[s04080 06:34]`–`[s04083 06:52]` spend another span on Cheng Pu's wine image and finally say it cannot diagnose the death. The latter repays an opening hook but diverts from the central cause question. |

## Pinned source check

I opened the pinned texts themselves, beyond the production summaries:

| Code | Source read | Decisive passages |
| --- | --- | --- |
| H | [《三國志》卷54, pinned commit](https://github.com/Ancient-China-Books/sanguozhi/blob/10a0b1ab3019d8821262f7402366d14fb4aaa102/OEBPS/Text/054.htm) | 〈周瑜傳〉 `p2` friendship/meeting before crossing; `p4` 208 council; `p5` Huang Gai; `p6` South Commandery arrow; `p7` Liu Bei proposal; `p8` west plan, 「而道於巴丘病卒」, age and mourning; `p9` music. 〈魯肅傳〉 `p15` earlier recommendation; `p21` final petition, Pei's separate 《江表傳》 letter, successor. |
| T | [《資治通鑑》 pinned full text](https://github.com/garychowcmu/daizhigev20/blob/4a6d6f2088825f132521d848c2ea86cf9c9a7620/%E5%8F%B2%E8%97%8F/%E7%BC%96%E5%B9%B4/%E8%B5%84%E6%B2%BB%E9%80%9A%E9%89%B4.txt) | Line 5569 places Zhou's journey from the earlier Baqiu at Sun Ce's 200 death. Lines 5709 and 5715 place the final west plan in 210: 「周瑜还江陵为行装，于道病困……卒于巴丘」. This is a later chronicle, not an independent medical witness. |
| N | [《三國演義》 pinned full text](https://github.com/garychowcmu/daizhigev20/blob/4a6d6f2088825f132521d848c2ea86cf9c9a7620/%E9%9B%86%E8%97%8F/%E6%BC%94%E4%B9%89/%E4%B8%89%E5%9B%BD%E6%BC%94%E4%B9%89.txt) | Ch. 51 starts line 1749, fake death/ambush at 1762–63, first real outburst at 1767; **ch. 54** starts 1817 and contains Zhou's marriage scheme at 1825 and Sun Quan's explanation at 1840; ch. 55 starts 1857 and flight/ambush ends at 1884; ch. 56 starts 1885, renewed burst 1886 and failed western gambit 1914–17; ch. 57 starts 1918, blocked waterway and letter at 1919, cry/death and recommended Lu Su at 1920. This is literary evidence only. |

**Death and source boundary.** H `p8` says 「權許之。瑜還江陵，爲行裝，而道於巴丘病卒……時年三十六」. H `p21` first has Chen Shou's 「周瑜病困，上疏曰……魯肅智略足任，乞以代瑜」 and then Pei's quote from 《江表傳》, 「道遇暴疾，昨自醫療，日加無損」 and 「魯肅忠烈……可以代瑜」; Pei himself says 「意旨雖同，其辭乖異」. Neither gives a disease name or connects the fatal illness to the earlier right-rib arrow. H `p6` explicitly describes that arrow and Zhou's camp inspection. N ch. 57 attributes his death to the invented confrontation with Zhuge Liang; N and H both include a Lu Su recommendation, in different forms. The script's main distinction at s04102 is warranted: **documented illness/death versus novel's anger plot**, without a modern diagnosis or a claim that emotions could never affect him.

**Huang Gai.** H `p5` directly has Huang Gai propose burning Cao's joined ships, prepare ships with brushwood and oil, 「先書報曹公，欺以欲降」, then release and ignite them. Narration s04027–s04028 and their blank-note/burning-boat prompts fit that record; no invented east-wind or personal duel appears. The main text credits allied action, including Liu Bei, Zhou Yu, Cheng Pu, and Huang Gai; s04025–s04029 do not assign the victory to Zhou alone.

## All narration IDs: attribution and accuracy

The following continuous ranges account for **s04001–s04104**. `H` is Chen Shou's main text unless explicitly marked `Pei`; `T` is the later chronicle; `N` is the novel; `I` is a limited inference or framing. The narration switches to an explicitly named novel at s04084–s04085; that boundary must remain audible and visible in the finished video.

| IDs checked | Finding |
| --- | --- |
| s04001–s04006 | H/T date and plan, H wound and Pei's Cheng Pu anecdote, N letter, I opening questions. All defensible as hooks; s04002 says the journey did not finish, which H supports. |
| s04007–s04010 | H `p2` same age, house, mother, shared goods; direct or fair paraphrase. |
| **s04011** | **Fix chronology:** H `p2` says 「會策將東渡，到歷陽，馳書報瑜，瑜將兵迎策」. Zhou met Sun Ce with troops at Liyang **as Sun Ce was about to cross**, before their subsequent operations and crossing. Current 「後來孫策渡江擴張勢力，周瑜帶兵迎他」 reads as though the meeting followed the crossing. |
| s04012–s04016 | H `p2` Sun Ce quote and age/nickname, H `p9` music; s04016 is a forward question. No medicine follows from the music anecdote. |
| s04017–s04021 | H `p3` Sun Ce death, Zhou's return and service; T line 5569 supports the earlier Baqiu to funeral; H `p8` brotherly protocol/ceremony; s04021 a question. Do not confuse this earlier Baqiu with the death site. |
| s04022–s04026 | H `p4` dates Cao's southward advance to Jian'an 13 and records surrender debate, Zhou's naval argument, command with Cheng Pu. H/Pei also credit Lu Su's earlier advice; current script's 「有人」 and shared command avoid claiming sole authorship. |
| s04027–s04030 | H `p5` Huang Gai feigned surrender, fire ships, Cao's retreat and Cao Ren left at Jiangling; s04030 is a supported forward question. |
| s04031–s04038 | H `p6` moves from Red Cliffs to South Commandery, Gan Ning at Yiling, Lü Meng's advice, Ling Tong guarding rear, rescue and scheduled battle; accurate sequence. |
| s04039–s04041 | H `p6` arrow hit **right rib**, severe wound and Cao Ren's move; accurate. |
| **s04042** | **Fix question/cause:** 「若一直留在床上，軍心會怎樣？」 is an unanswerable counterfactual and H says no such outcome. The next lines answer whether Zhou rose, not the question voiced. Use the factual uncertainty, e.g. 「曹仁列陣時，重傷的周瑜還能起身嗎？」. |
| s04043–s04049 | H `p6–p8` Zhou rose and inspected camp, Cao Ren retired, Zhou became Southern Commandery governor, later remained at Jiangling. H has no subsequent wound course, so s04046–s04047's restraint is right. s04049's farther-plan hook is valid but points past the next chapter's first proposal. |
| s04050–s04054 | H `p7` Liu Bei visited Sun Quan, Zhou proposed retaining Liu Bei and dividing Guan/Zhang, Sun Quan declined for strategic reasons. Accurate, without inventing Zhou's anger. |
| s04055–s04062 | H `p8` Liu Zhang/Zhang Lu, Cao's defeat, request with Sun Yu, take Shu then Zhang Lu, hold territory, turn toward Xiangyang, Sun Quan's assent; T line 5715 identifies 奮威 as Sun Yu. These are **proposals**, not executed conquests. |
| **s04063** | **Major factual error:** 「計畫卻停在出發前」 contradicts H `p8` 「而道於巴丘病卒」 and T 5715 「于道病困……卒于巴丘」. He prepared at Jiangling, then became ill/died **on the road**. Do not state the plan stopped before departure. |
| s04064–s04070 | H `p21` illness and successor petition; Pei's separate 《江表傳》 version explicitly has 「道遇暴疾」 and no recovery; labels at s04065/s04069–s04070 correctly distinguish Chen Shou and Pei. s04064's question is answered already at s04065, though metadata incorrectly points only to s04070. |
| s04071–s04074 | H `p21` both wordings recommend Lu Su and Pei says text differs; H `p8` 「巴丘病卒」. Neither text gives disease name; attribution and negative limit are accurate. |
| **s04075** | **Fix:** H `p8` supports age 36 and unfinished conquest but does **not** say the westward force 「沒由他帶出去」. Its explicit 「而道」 argues against an image of never setting out. Say he did not complete the planned conquest. |
| s04076–s04084 | Pei at H `p2/p8` distinguishes same-name Baqiu sites; H `p8` gives Sun Quan mourning; Pei's 《江表傳》 supplies the 「王佐之資」 quote and Cheng Pu/wine details, appropriately labeled s04078/s04081. H `p21` gives Lu Su and Cheng Pu succession. s04083 is a proper limit on the anecdote, not evidence of death cause. s04084 clearly introduces fiction. |
| s04085–s04090 | N ch. 51 title, South Commandery capture and wound burst; N ch. 51 also has Zhou feign a worse illness/death to bait Cao Ren **before** the first outburst. s04088 acknowledges the staged episode, but its narrated order after s04087 is backward within ch. 51; 「同一回」 avoids directly claiming it happened later. N ch. 55 title is correct. |
| **s04091** | N supports the marriage scheme and Liu Bei/Sun Lady escape, but the pinned **51, 55–57** list omits **ch. 54**, where Zhou's scheme is actually established (line 1825 and Sun Quan's explanation at 1840). Add ch. 54 to research/claims citation coverage. |
| s04092–s04097 | N chs. 55–57 support ambush, wound rupture, ch. 56's third-anger heading, renewed westward move, blocked Baqiu waterway, and Zhuge Liang's letter warning of difficult transport and Cao's possible attack. Each section identifies fiction; none can establish the historical cause. |
| **s04098** | **Tighten novel sequence:** N 1920 has Zhou **read the letter, write to Sun Quan, address his commanders, then faint, wake and cry**. Current 「讀後昏厥，醒來喊」 skips the intervening letter and speech and suggests immediate collapse on reading. If compressed, say 「讀信後，他先寫信給孫權、囑咐將士；昏厥醒來才喊……」. |
| s04099–s04104 | N 1920 has the cry then death and a posthumous letter recommending Lu Su; H has illness and a successor petition but **no** cry. s04100's `claims.md` row should include H 〈周瑜傳〉 for the negative history comparison; s04100 also repeats 「沒有」 twice. s04101–s04102 properly separate novel causation from historical illness. s04103's 「沒能帶出去」 metaphor echoes the erroneous before-departure picture; revise with s04063/s04075. s04104 is a CTA, no historical claim. |

## Image prompts and production metadata

- **s04063–s04064 and s04075:** three Jiangling packed-chest images, especially s04075's “empty Jiangling hall” with Zhou himself still at a closed chest *after* s04074 announces his death, create a false before-departure chronology. Show a prepared chest at Jiangling only before the journey; for death/age use an empty travel place, Baqiu road, or abandoned plan without a living Zhou in Jiangling. The s04075 prompt is also internally inconsistent: “empty ... hall, one ... general”.
- **s04047:** a “blank medical scroll” can suggest a historical medical record exists. The sources have no case record or diagnosis. A blank margin in the history book is the accurate image.
- **s04084–s04098:** the novel sequences switch from a reader/book to realistic tents, boats and a distressed commander. The word “novel” in a generation prompt will not be visible to viewers. Keep a persistent on-screen novel label or a visibly distinct book-page frame while these scenes run. The existing historical/novel claim distinction in narration is otherwise sound.
- `video.json` loop `s04005 → s04096` claims to repay who sends the letter, but s04005 already names Zhuge Liang and s04096 asks what the letter says; the new information is s04097. Loop `s04042 → s04043` rewrites a morale counterfactual as whether Zhou can rise. Loop `s04062 → s04063` points to the inaccurate before-departure line. Align metadata with the voiced questions after revision.
- H's Huang Gai wording supports the surrender-note and fire-boat prompts s04027–s04028. No misleading magical wind, named disease, visible original final-letter artifact, or exact modern Baqiu site is asserted by those prompts.

## Verdict

**Hold preproduction pending revision.** Correct the on-road chronology at s04063/s04075 and matching visuals; fix the Sun Ce crossing order at s04011; either include ch. 54 in the novel citations or narrow s04091; and tighten the novel's final letter/fainting sequence at s04098. The history/novel distinction, lack of a diagnosis, Huang Gai fire sequence, and two final-letter attributions are otherwise well supported. Re-run the blind narrative panel on the revised script, particularly its chapter openings, counterfactual hook, repeated answer, and character detours; the current snapshot fails `one_line`, `chapters_link`, `payoffs`, `no_recap`, and `no_detour`.
