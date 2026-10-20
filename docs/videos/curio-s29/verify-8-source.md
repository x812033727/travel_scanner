# Curio S29 R5 independent source and still-prompt audit

Scope: 94 `claims.md` narration rows and 92 `video.json` still prompts; no generated media inspected or changed. This follows the [blind narrative seal](verify-8-blind.md).

## Fixed artifacts

- `video.json` SHA-256 `483ebde58834462f74b8e63a8cfe51a85a69178b35af4ccdb89f49ab66c2be44` — match.
- `claims.md` SHA-256 `473d3010c09a8a4c0babc087c0414a308e596abc00a686de538dddf0d46aa893` — match.
- Freshly fetched Sanguozhi `020.htm` at commit `10a0b1ab3019d8821262f7402366d14fb4aaa102`, SHA-256 `dec2ae1713a56e2a33d367d691904004db60740f9490023b52695bfd3740bbc8` — match.
- Freshly fetched CBETA `T04n0203.xml` at commit `dbdea41071e1e260ad84b72faefd4587333cf76d`, SHA-256 `0b0d59c2c02da42fae95e3ed48f64e20813602b6f48032770a0ce557a6ff90b1` — match.

## Primary-source conclusions

- Sanguozhi p6: 孫權曾致巨象; 太祖 asked courtiers; 沖曰「置象大船之上，而刻其水痕所至，稱物以載之，則校可知矣」; 太祖大恱，即施行焉. The text supplies neither a stone specification nor an elephant weight, a weighing ledger, operator identities, or date of the weighing.
- Sanguozhi p6: 少聦察岐嶷、生五六歲... is a general youth description. 年十三、建安十三年疾病...及亡 dates death to Jian’an 13 (208 CE), not the boat scene.
- CBETA lines 657–681: Buddha addresses monks about respecting elders, describes the expulsion law, the minister hiding his father underground, and earlier riddles.
- CBETA lines 682–686: deity asks the white elephant’s weight; father answers「置象船上，著大池中，畫水齊船深淺幾許；即以此船，量石著中，水沒齊畫，則知斤兩」; minister「即以此智以答」. It specifies stone, pool, same boat, and `畫`, but reports an answer rather than a poolside execution or final weight.
- CBETA lines 686–742: more questions, promised protection and treasure, father’s disclosure after a no-punishment promise, law changed, elder respected; Buddha identifies himself as the former father. Header line 12 says「元魏 吉迦夜共曇曜譯」; it does not date the prior story or establish any path to Cao Chong.

## Individual claim rows

| Narration ID | Direct-source scope checked | Result |
|---|---|---|
| `boat001` | S1 | Pass |
| `boat002` | S1 | Pass |
| `boat003` | S1 | Pass |
| `boat004` | S1 | Pass |
| `boat005` | B2,B4 | Pass |
| `boat006` | B1 | Pass |
| `boat007` | S1,B2 | Pass |
| `boat008` | S1,B2,B4 | Pass |
| `boat009` | S1 | Pass |
| `boat010` | S1 | Pass |
| `boat011` | S1 | Pass |
| `boat012` | S2 | Pass |
| `boat013` | S1 | Pass |
| `boat014` | S1 | Pass |
| `boat015` | S1 | Pass |
| `boat016` | S1 | Pass |
| `boat017` | S1 | Pass |
| `boat018` | S1,B2 | Pass |
| `boat019` | S1 | Pass |
| `boat020` | S1 | Pass |
| `boat021` | S1 | Pass |
| `boat022` | S1 | Pass |
| `boat023` | S1 | Pass |
| `boat024` | S1 | Pass |
| `boat025` | S1 | Pass |
| `boat026` | S1 | Pass |
| `boat027` | S1 | Pass |
| `boat028` | S1 | Pass |
| `boat029` | S1 | Pass |
| `boat030` | S1 | Pass |
| `boat031` | S1 | Pass |
| `boat032` | S1 | Pass |
| `boat034` | S1 | Pass |
| `boat036` | S1 | Pass |
| `boat037` | S1 | Pass |
| `boat039` | S1 | Pass |
| `boat041` | S1 | Pass |
| `boat043` | S1 | Pass |
| `boat044` | S1 | Pass |
| `boat045` | S1 | Pass |
| `boat046` | S1 | Pass |
| `boat048` | S1,B1,B2 | Pass |
| `boat049` | B1 | Pass |
| `boat050` | B1 | Pass |
| `boat051` | B1 | Pass |
| `boat052` | S1,B1 | Pass |
| `boat053` | B1 | Pass |
| `boat054` | B1 | Pass |
| `boat055` | B1 | Pass |
| `boat061` | B2 | Pass |
| `boat062` | B2 | Pass |
| `boat063` | B2 | Pass |
| `boat064` | B1,B2 | Pass |
| `boat065` | B2 | Pass |
| `boat066` | B2 | Pass |
| `boat067` | B2 | Pass |
| `boat068` | B2 | Pass |
| `boat069` | B2 | Pass |
| `boat070` | B2 | Pass |
| `boat072` | B2 | Pass |
| `boat073` | S1,B2 | Pass |
| `boat075` | S1,B2 | Pass |
| `boat076` | S1,B2 | Pass |
| `boat077` | S1,B2 | Pass |
| `boat078` | S1 | Pass |
| `boat079` | B2 | Pass |
| `boat080` | B2,B3 | Pass |
| `boat081` | B3 | Pass |
| `boat084` | B1,B3 | Pass |
| `boat085` | B1,B3 | Pass |
| `boat086` | B3 | Pass |
| `boat086a` | B3 | Pass |
| `boat086b` | B3 | Pass |
| `boat086c` | B3 | Pass |
| `boat087` | B3 | Pass |
| `boat088` | B3 | Pass |
| `boat090` | B3 | Pass |
| `boat091` | B1,B3 | Pass |
| `boat092` | S2,B1 | Pass |
| `boat094` | S1,B2,B4 | Pass |
| `boat095` | S3 | Pass |
| `boat096` | S3 | Pass |
| `boat097` | B4 | Pass |
| `boat098` | S3,B4 | Pass |
| `boat099` | B4 | Pass |
| `boat100` | S1,B2,B4 | Pass |
| `boat101` | S1,B4 | Pass |
| `boat102` | S1 | Pass |
| `boat103` | B1,B2 | Pass |
| `boat104` | S1,B2,B4 | Pass |
| `boat105` | S1,B2,B4 | Pass |
| `boat106` | S1,B2,B4 | Pass |
| `boatout1` | outro/no factual assertion | N/A: audience invitation |
| `boatout2` | outro/no factual assertion | N/A: audience invitation |

Claim assessment: 92 content lines, including their questions and explanatory inferences, stay within the two excerpts and their explicit limits; the two outro lines make no historical assertion. The claim text in every row matches its `video.json` narration text exactly. I found no unsupported borrowing direction, stone retrofitted into Sanguozhi, invented recorded weight, or claim that the sutra method was physically carried out.

## Individual still prompts

| Scene ID | Result | Source-bound note |
|---|---|
| `boat-001` | Pass | Schematic or document-reading image; no contradiction with the line or either excerpt. |
| `boat-002` | Pass | Schematic or document-reading image; no contradiction with the line or either excerpt. |
| `boat-003` | Pass | Schematic or document-reading image; no contradiction with the line or either excerpt. |
| `boat-004` | Pass | Schematic or document-reading image; no contradiction with the line or either excerpt. |
| `boat-005` | Pass | Legendary elephant is a schematic cue; text records a question and proposed method, not a witnessed pond scene. |
| `boat-006` | Pass | Schematic or document-reading image; no contradiction with the line or either excerpt. |
| `boat-007` | Pass | Schematic or document-reading image; no contradiction with the line or either excerpt. |
| `boat-008` | Pass | Schematic or document-reading image; no contradiction with the line or either excerpt. |
| `boat-009` | Pass | Schematic or document-reading image; no contradiction with the line or either excerpt. |
| `boat-010` | Pass | Schematic or document-reading image; no contradiction with the line or either excerpt. |
| `boat-011` | Pass | Schematic or document-reading image; no contradiction with the line or either excerpt. |
| `boat-012` | Pass | Schematic or document-reading image; no contradiction with the line or either excerpt. |
| `boat-013` | Pass | Schematic or document-reading image; no contradiction with the line or either excerpt. |
| `boat-014` | Pass | Schematic or document-reading image; no contradiction with the line or either excerpt. |
| `boat-015` | Pass | Schematic or document-reading image; no contradiction with the line or either excerpt. |
| `boat-016` | Pass | Boy touches an existing mark; the source does not name who carved it. |
| `boat-017` | Pass | Schematic or document-reading image; no contradiction with the line or either excerpt. |
| `boat-018` | Pass | Schematic or document-reading image; no contradiction with the line or either excerpt. |
| `boat-019` | Pass | Boy compares water and notch as an illustration of the method, not a documented personal action. |
| `boat-020` | Pass | Schematic or document-reading image; no contradiction with the line or either excerpt. |
| `boat-021` | Pass | Schematic or document-reading image; no contradiction with the line or either excerpt. |
| `boat-022` | Pass | Schematic or document-reading image; no contradiction with the line or either excerpt. |
| `boat-023` | Pass | Schematic or document-reading image; no contradiction with the line or either excerpt. |
| `boat-024` | Pass | Bundle is deliberately unspecified; S says 物 and does not name stone. |
| `boat-025` | Pass | Schematic or document-reading image; no contradiction with the line or either excerpt. |
| `boat-026` | Pass | Schematic or document-reading image; no contradiction with the line or either excerpt. |
| `boat-027` | Pass | Schematic or document-reading image; no contradiction with the line or either excerpt. |
| `boat-028` | Pass | Schematic or document-reading image; no contradiction with the line or either excerpt. |
| `boat-029` | Pass | Schematic or document-reading image; no contradiction with the line or either excerpt. |
| `boat-030` | Pass | Schematic or document-reading image; no contradiction with the line or either excerpt. |
| `boat-031` | Pass | Schematic or document-reading image; no contradiction with the line or either excerpt. |
| `boat-032` | Pass | Schematic or document-reading image; no contradiction with the line or either excerpt. |
| `boat-034` | Pass | Schematic or document-reading image; no contradiction with the line or either excerpt. |
| `boat-036` | Pass | Schematic or document-reading image; no contradiction with the line or either excerpt. |
| `boat-037` | Pass | Two boats depict the narrated counterfactual, not a recorded second boat. |
| `boat-039` | Pass | Schematic or document-reading image; no contradiction with the line or either excerpt. |
| `boat-041` | Pass | Schematic or document-reading image; no contradiction with the line or either excerpt. |
| `boat-043` | Pass | Schematic or document-reading image; no contradiction with the line or either excerpt. |
| `boat-044` | Pass | Schematic or document-reading image; no contradiction with the line or either excerpt. |
| `boat-045` | Pass | Schematic or document-reading image; no contradiction with the line or either excerpt. |
| `boat-046` | Pass | Schematic or document-reading image; no contradiction with the line or either excerpt. |
| `boat-048` | Pass | Cellar and boat share a frame schematically; the sutra gives no physical map. |
| `boat-049` | Pass | Schematic or document-reading image; no contradiction with the line or either excerpt. |
| `boat-050` | Pass | Schematic or document-reading image; no contradiction with the line or either excerpt. |
| `boat-051` | Pass | Schematic or document-reading image; no contradiction with the line or either excerpt. |
| `boat-052` | Pass | Schematic or document-reading image; no contradiction with the line or either excerpt. |
| `boat-053` | Pass | One listener is visible in a framed shot; the sutra addresses plural monks. |
| `boat-054` | Pass | Schematic or document-reading image; no contradiction with the line or either excerpt. |
| `boat-055` | Pass | Schematic or document-reading image; no contradiction with the line or either excerpt. |
| `boat-061` | Pass | Elephant near pond is an allegorical cue; the sutra does not narrate moving a live elephant there. |
| `boat-062` | Pass | Schematic or document-reading image; no contradiction with the line or either excerpt. |
| `boat-063` | Pass | Schematic or document-reading image; no contradiction with the line or either excerpt. |
| `boat-064` | Pass | Schematic or document-reading image; no contradiction with the line or either excerpt. |
| `boat-065` | Pass | Modern miniature makes the proposed sutra method visibly schematic. |
| `boat-066` | Pass | Modern miniature makes the proposed sutra method visibly schematic. |
| `boat-067` | Pass | Modern miniature makes the proposed sutra method visibly schematic. |
| `boat-068` | Pass | Modern miniature uses stone only for the sutra version. |
| `boat-069` | Pass | Modern miniature isolates the same boat required by 即以此船. |
| `boat-070` | Pass | Modern miniature illustrates a method; the sutra records an answer, not poolside execution. |
| `boat-072` | Pass | Schematic or document-reading image; no contradiction with the line or either excerpt. |
| `boat-073` | Pass | Schematic or document-reading image; no contradiction with the line or either excerpt. |
| `boat-075` | Pass | Schematic or document-reading image; no contradiction with the line or either excerpt. |
| `boat-076` | Pass | Schematic or document-reading image; no contradiction with the line or either excerpt. |
| `boat-077` | Pass | Schematic or document-reading image; no contradiction with the line or either excerpt. |
| `boat-078` | Pass | Schematic or document-reading image; no contradiction with the line or either excerpt. |
| `boat-079` | Pass | Schematic or document-reading image; no contradiction with the line or either excerpt. |
| `boat-080` | Pass | Schematic or document-reading image; no contradiction with the line or either excerpt. |
| `boat-081` | Pass | Schematic or document-reading image; no contradiction with the line or either excerpt. |
| `boat-084` | Pass | Schematic or document-reading image; no contradiction with the line or either excerpt. |
| `boat-085` | Pass | Schematic or document-reading image; no contradiction with the line or either excerpt. |
| `boat-086` | Pass | Schematic or document-reading image; no contradiction with the line or either excerpt. |
| `boat-086a` | Pass | Schematic or document-reading image; no contradiction with the line or either excerpt. |
| `boat-086b` | Pass | Schematic or document-reading image; no contradiction with the line or either excerpt. |
| `boat-086c` | Pass | Schematic or document-reading image; no contradiction with the line or either excerpt. |
| `boat-087` | Pass | Schematic or document-reading image; no contradiction with the line or either excerpt. |
| `boat-088` | Pass | Elder is shown after the disclosure and king’s change of law. |
| `boat-090` | Pass | One listener is visible in a framed shot; the sutra addresses plural monks. |
| `boat-091` | Pass | Schematic or document-reading image; no contradiction with the line or either excerpt. |
| `boat-092` | Pass | Schematic or document-reading image; no contradiction with the line or either excerpt. |
| `boat-094` | Pass | Schematic or document-reading image; no contradiction with the line or either excerpt. |
| `boat-095` | Pass | Schematic or document-reading image; no contradiction with the line or either excerpt. |
| `boat-096` | Pass | Schematic or document-reading image; no contradiction with the line or either excerpt. |
| `boat-097` | Pass | Schematic or document-reading image; no contradiction with the line or either excerpt. |
| `boat-098` | Pass | Schematic or document-reading image; no contradiction with the line or either excerpt. |
| `boat-099` | Pass | Schematic or document-reading image; no contradiction with the line or either excerpt. |
| `boat-100` | Pass | Schematic or document-reading image; no contradiction with the line or either excerpt. |
| `boat-101` | Pass | Schematic or document-reading image; no contradiction with the line or either excerpt. |
| `boat-102` | Pass | Schematic or document-reading image; no contradiction with the line or either excerpt. |
| `boat-103` | Pass | Schematic or document-reading image; no contradiction with the line or either excerpt. |
| `boat-104` | Pass | Schematic or document-reading image; no contradiction with the line or either excerpt. |
| `boat-105` | Pass | Schematic or document-reading image; no contradiction with the line or either excerpt. |
| `boat-106` | Pass | Schematic or document-reading image; no contradiction with the line or either excerpt. |

Prompt assessment: all 92 are `shot` scenes with `visual: still`, distinct Han-era / legendary-kingdom / modern-study framing, and no explicit claim that the two story worlds meet. Ambiguous props and location details are cartoon illustration, as the Curio episode rule permits; the prompts do not contradict a source fact. This assessment does not certify the unseen generated images.

## Gate

`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s29`: **0 errors, 0 warnings**; estimates 9.4 minutes and 94 lines.

**Overall: PASS. No source-factual or still-prompt blocker found.**
