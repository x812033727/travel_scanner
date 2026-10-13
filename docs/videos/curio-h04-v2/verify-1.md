# H04 v2 | Independent fact check, round 1

Checked on 2026-10-14 against the corrected video.json. The checker did not write the H04 script. This is a text and source gate, not media playback or owner acceptance.

## Bound files and coverage

- video.json SHA-256: 10d9e38ea339e2110f3492186f2f7c0119be951106e55be527846eb12971c28b
- script.md SHA-256: 66e463cba367be9e5f2c957a80dbd94ea720c5a81e29aa3e0326603e878ff423
- Narrative hash: 7b9e0ce81bffe363; bound panel 11/11, no failed/advisory checks.
- 101 spoken text lines, all non-shot scene.data, thumbnail, YouTube title/description/tags and 12 source entries inventoried. No say overrides. Every scene has a claim ID. The raw 418-string path inventory is external at C:/Users/x8120/mokaair-work/videos/curio-h04-v2/_tools/claim-inventory.json. Synthetic shot prompts and pure design labels are visual directions, not asserted historic observations.

## Direct source readback

| Source | URL | HTTP / bytes | Evidentiary scope |
|---|---|---|---|
| S01 | https://dyatlovpass.com/case-files-384-387-ru | 200 / 50890 | 1959 closure transcript and scans, sheets 384-387; original p386 viewed |
| S02 | https://dyatlovpass.com/case-files-303-304-ru | 200 / 52273 | 1959 tent examination transcript and original p304 reverse viewed |
| S03 | https://dyatlovpass.com/case-files-309-312-ru | 200 / 48869 | Tempalov testimony transcript and original p312 viewed |
| S04 | https://dyatlovpass.com/case-files-298-300 | 200 / 39309 | Slobtsov testimony translation and scan index; translation is not another witness |
| S05 | https://www.nature.com/articles/s43247-020-00081-8 | 200 / 420415 | 2021 Gaume/Puzrin original Nature article, full HTML |
| S06 | https://www.nature.com/articles/s43247-022-00393-x | 200 / 244900 | 2022 Puzrin/Gaume Nature Comment, full HTML and PDF |
| S07 | https://www.nature.com/articles/s43247-022-00425-6 | 200 / 205767 | 2022 Nature correction of reference DOI only |
| S08 | https://longread.epfl.ch/en/dossier/quand-la-science-permet-dexplorer-un-mystere-russe-vieux-de-60-ans/ | 200 / 141628 | EPFL account of the same 2021 author work |
| S09 | https://ethz.ch/en/news-and-events/eth-news/news/2022/03/the-dyatlov-pass-mystery-and-what-a-research-article-can-trigger.html | 200 / 68906 | ETH account of the same author work |
| S10 | https://actu.epfl.ch/news/intense-press-coverage-prompts-new-expeditions-to-/ | 200 / 36902 | EPFL interview about 2022 expeditions |
| S11 | https://www.interfax.ru/russia/649229 | 200 / 71039 | Interfax first-hand report of 2019 prosecutor statement, not full official report |
| S12 | https://www.interfax.ru/russia/716956 | 200 / 73530 | Interfax first-hand report of 2020 briefing, not full official report |

1959 period documents are preserved by a private site, not direct archival custody. Scan and transcription are one document. S05-S10 concern one research lineage. Interfax reports attributed public statements; the complete prosecutor report was not located, so the narration makes only the narrow public-statement claim.

## Full checkable-claim table

Each c row covers all mapped spoken IDs plus the listed card scene.data paths; M1-M4 cover publication metadata. The raw string-path inventory supports this grouping. HTTP 200 means the body itself was fetched and read on 2026-10-14.

| # | Claim | Where | URL | HTTP | Verdict | Before -> after |
|---|---|---|---|---|---|---|
| c01 | 多數鞋子、外衣與個人物品留在帳內；九人離營的原因是本片問題。 | opening-gear（h4v003）；opening-question（h4v008） | [S1](https://dyatlovpass.com/case-files-384-387-ru) | S01: 200 | CONFIRMED | unchanged |
| c03 | 足跡包含近乎赤腳／薄襪及氈靴等類型，不能概括成九人全赤腳。 | trail-varied（h4v015）；document-footprints-slot（h4v016）；boot-print-evidence（h4v017）；felt-versus-knit（h4v018）; scenes[trail-varied].data, scenes[document-footprints-slot].data, scenes[boot-print-evidence].data | [S1](https://dyatlovpass.com/case-files-384-387-ru)、[S3](https://dyatlovpass.com/case-files-309-312-ru) | S01: 200, S03: 200 | CONFIRMED | unchanged |
| c04 | 可辨足跡指向山下、谷地及森林；不能由方向讀出心情。 | trail-search-start（h4v107）；trail-downhill（h4v022）; scenes[trail-downhill].data | [S1](https://dyatlovpass.com/case-files-384-387-ru)、[S3](https://dyatlovpass.com/case-files-309-312-ru) | S01: 200, S03: 200 | CONFIRMED | unchanged |
| c05 | 十人出發，一人因身體不適折返，九人繼續冬季滑雪旅行。 | journey-numbers（h4v009）; scenes[journey-numbers].data | [S1](https://dyatlovpass.com/case-files-384-387-ru) | S01: 200 | CONFIRMED | unchanged |
| c06 | 死者不全是學生，也包括已工作成員。 | journey-pack（h4v010） | [S1](https://dyatlovpass.com/case-files-384-387-ru) | S01: 200 | CONFIRMED | unchanged |
| c07 | 最後營地在山坡帳篷，留下設備成為事後追查線索。 | camp-platform-context（h4v011） | [S1](https://dyatlovpass.com/case-files-384-387-ru) | S01: 200 | CONFIRMED | unchanged |
| c08 | 1959 年 2 月 26 日白天找到帳篷。 | opening-search（h4v001） | [S1](https://dyatlovpass.com/case-files-384-387-ru)、[S4](https://dyatlovpass.com/case-files-298-300) | S01: 200, S04: 200 | CONFIRMED | unchanged |
| c09 | 搜救者除雪並確認帳內無人。 | opening-inside（h4v002） | [S4](https://dyatlovpass.com/case-files-298-300) | S04: 200 | CONFIRMED | unchanged |
| c10 | 搜救現場是事發一段時間後的現場，不能當離營當時目擊。 | trail-search-start（h4v107）；search-later-weather（h4v012）；search-two-times（h4v030） | [S1](https://dyatlovpass.com/case-files-384-387-ru)、[S4](https://dyatlovpass.com/case-files-298-300) | S01: 200, S04: 200 | CONFIRMED | unchanged |
| c11 | 1959 年 4 月 16 日鑑定依布料／切口／內側細微損傷判斷由內向外刀切。 | tease-fabric（h4v004）；tent-opening-question（h4v105）；tent-examination（h4v031）；fabric-workbench（h4v032）；inside-fabric（h4v033）; scenes[tent-opening-question].data, scenes[tent-examination].data | [S2](https://dyatlovpass.com/case-files-303-304-ru) | S02: 200 | CONFIRMED | unchanged |
| c12 | 內側切口不能獨立證明誰先動刀或每人離帳方式。 | cut-inference（h4v034,h4v035）; scenes[cut-inference].data | [S2](https://dyatlovpass.com/case-files-303-304-ru) | S02: 200 | CONFIRMED | unchanged |
| c13 | 留下用品令調查人員推斷突然離營；急迫是線索引出的判讀。 | remaining-boots（h4v013）；tent-opening-empty（h4v014）；document-shoes-slot（h4v036）; scenes[document-shoes-slot].data | [S1](https://dyatlovpass.com/case-files-384-387-ru) | S01: 200 | CONFIRMED | unchanged |
| c14 | 結案書記八到九組，Tempalov 記八組且未確認第九組。 | footprint-count（h4v019,h4v020）；broken-trail（h4v021）; scenes[footprint-count].data, scenes[broken-trail].data | [S1](https://dyatlovpass.com/case-files-384-387-ru)、[S3](https://dyatlovpass.com/case-files-309-312-ru) | S01: 200, S03: 200 | CONFIRMED | unchanged |
| c15 | 一位勘驗者認為所見足跡顯示普通步行；無法保證全程步態或情緒。 | stride-evidence（h4v023）；stride-inference（h4v024,h4v025）; scenes[stride-evidence].data, scenes[stride-inference].data | [S3](https://dyatlovpass.com/case-files-309-312-ru) | S03: 200 | CHANGED | h4v023/card/SVG: stride length -> tracks; S03 p312 says normal walking but does not state a stride-length measurement |
| c16 | 足跡靠近林緣後被雪覆蓋；火堆附近找到兩人，另三人在火堆朝帳篷的直線上，其中兩人的姿勢被卷宗解讀為可能向帳篷爬；五月最後四人在溪溝附近約四至四點五公尺積雪下被發現，九人無人生還。 | forest-edge-absence（h4v026）；fire-site-two（h4v108）；three-toward-tent（h4v109,h4v110）；discovery-sequence（h4v027,h4v028）；ravine-depth（h4v111）；spring-empty-ravine（h4v029）; scenes[three-toward-tent].data, scenes[discovery-sequence].data, scenes[ravine-depth].data | [S1](https://dyatlovpass.com/case-files-384-387-ru)、[S3](https://dyatlovpass.com/case-files-309-312-ru) | S01: 200, S03: 200 | CHANGED | h4v110: implied all three crawled -> only two postures suggested crawling; Dyatlov lay on his back (S01 p386) |
| c17 | 1959 年 5 月結案決定以無力克服的自然力量概括致因。 | tease-file（h4v005）；archive-closed-folder（h4v037）；natural-force-slot（h4v039）; scenes[natural-force-slot].data | [S1](https://dyatlovpass.com/case-files-384-387-ru) | S01: 200 | CONFIRMED | unchanged |
| c18 | 原文關鍵詞自然力量不等於神祕超自然力量，也沒指定雪板機制。 | natural-not-supernatural（h4v040,h4v041）；archive-ribbon（h4v042）; scenes[natural-not-supernatural].data | [S1](https://dyatlovpass.com/case-files-384-387-ru) | S01: 200 | CONFIRMED | unchanged |
| c19 | 結案書有多頁，整理物品、足跡等；只讀結論會遺漏前文。 | archive-many-pages（h4v038） | [S1](https://dyatlovpass.com/case-files-384-387-ru) | S01: 200 | CONFIRMED | unchanged |
| c20 | 2019 年檢方對外說明複查；2020 年記者會提出雪崩解釋。 | review-timeline（h4v043,h4v044）；empty-speaking-room（h4v045）; scenes[review-timeline].data | [S11](https://www.interfax.ru/russia/649229)、[S12](https://www.interfax.ru/russia/716956) | S11: 200, S12: 200 | CONFIRMED | unchanged |
| c21 | 平均坡緩、可能延遲滑落是模型回應的問題，不是當夜已發生的時間線。 | slope-small-feature（h4v046）；camp-open-question（h4v047） | [S5](https://www.nature.com/articles/s43247-020-00081-8)、[S8](https://longread.epfl.ch/en/dossier/quand-la-science-permet-dexplorer-un-mystere-russe-vieux-de-60-ans/) | S05: 200, S08: 200 | CONFIRMED | unchanged |
| c22 | 2021 年兩名作者研究局部小型雪板的釋放與撞擊機制。 | tease-paper（h4v006）；model-paper-card（h4v048）; scenes[model-paper-card].data | [S5](https://www.nature.com/articles/s43247-020-00081-8)、[S8](https://longread.epfl.ch/en/dossier/quand-la-science-permet-dexplorer-un-mystere-russe-vieux-de-60-ans/) | S05: 200, S08: 200 | CONFIRMED | unchanged |
| c23 | 雪板涉及一層相互連結的雪失去穩定。 | cohesive-snow（h4v049） | [S5](https://www.nature.com/articles/s43247-020-00081-8)、[S8](https://longread.epfl.ch/en/dossier/quand-la-science-permet-dexplorer-un-mystere-russe-vieux-de-60-ans/) | S05: 200, S08: 200 | CONFIRMED | unchanged |
| c24 | 較脆弱雪層可能先破壞，影響上方相連雪板。 | buried-layer-close（h4v050） | [S5](https://www.nature.com/articles/s43247-020-00081-8)、[S8](https://longread.epfl.ch/en/dossier/quand-la-science-permet-dexplorer-un-mystere-russe-vieux-de-60-ans/) | S05: 200, S08: 200 | CONFIRMED | unchanged |
| c25 | 平緩平均坡面不排除局部較陡階梯。 | smooth-surface（h4v051）；surface-and-ground（h4v052,h4v053）；ground-step-context（h4v054）; scenes[surface-and-ground].data | [S5](https://www.nature.com/articles/s43247-020-00081-8)、[S6](https://www.nature.com/articles/s43247-022-00393-x) | S05: 200, S06: 200 | CONFIRMED | unchanged |
| c26 | 模型假設局部地形及埋藏弱層的幾何條件。 | snow-over-step（h4v055）；model-first-two（h4v058）; scenes[snow-over-step].data, scenes[model-first-two].data | [S5](https://www.nature.com/articles/s43247-020-00081-8) | S05: 200 | CONFIRMED | unchanged |
| c27 | 切出搭帳平台會改變雪層支撐和受力，是模型條件之一。 | snow-platform-cut（h4v056）；platform-front-face（h4v057）；model-first-two（h4v058，畫面第二步）; scenes[platform-front-face].data, scenes[model-first-two].data | [S5](https://www.nature.com/articles/s43247-020-00081-8)、[S8](https://longread.epfl.ch/en/dossier/quand-la-science-permet-dexplorer-un-mystere-russe-vieux-de-60-ans/) | S05: 200, S08: 200 | CONFIRMED | unchanged |
| c28 | 切坡後不必立刻滑動；特定模型條件容許延遲釋放。 | quiet-platform（h4v060）；slab-edge-displaced（h4v067）; scenes[slab-edge-displaced].data | [S5](https://www.nature.com/articles/s43247-020-00081-8)、[S8](https://longread.epfl.ch/en/dossier/quand-la-science-permet-dexplorer-un-mystere-russe-vieux-de-60-ans/) | S05: 200, S08: 200 | CONFIRMED | unchanged |
| c29 | 風能搬運既有雪並增加上方載重，不必是新降雪。 | wind-moves-snow（h4v062）；wind-ridge（h4v063）；drift-deposition（h4v064）; scenes[wind-moves-snow].data | [S5](https://www.nature.com/articles/s43247-020-00081-8)、[S8](https://longread.epfl.ch/en/dossier/quand-la-science-permet-dexplorer-un-mystere-russe-vieux-de-60-ans/) | S05: 200, S08: 200 | CONFIRMED | unchanged |
| c31 | 新增載重可使弱層破裂擴展並促成雪板滑動。 | model-later-two（h4v065,h4v066）；slab-edge-displaced（h4v067）; scenes[model-later-two].data, scenes[slab-edge-displaced].data | [S5](https://www.nature.com/articles/s43247-020-00081-8)、[S8](https://longread.epfl.ch/en/dossier/quand-la-science-permet-dexplorer-un-mystere-russe-vieux-de-60-ans/) | S05: 200, S08: 200 | CONFIRMED | unchanged |
| c32 | 數小時是模型情境；研究由推定時距回算積雪通量，並非獨立預測事發時刻。 | model-hours（h4v068）；model-not-timer（h4v069,h4v070）; scenes[model-hours].data, scenes[model-not-timer].data | [S5](https://www.nature.com/articles/s43247-020-00081-8) | S05: 200 | CONFIRMED | unchanged |
| c33 | 模型結果依賴雪厚、強度及載重等參數，當年完整現場參數未知。 | model-snow-sample（h4v061）；measurement-tools（h4v071） | [S5](https://www.nature.com/articles/s43247-020-00081-8)、[S8](https://longread.epfl.ch/en/dossier/quand-la-science-permet-dexplorer-un-mystere-russe-vieux-de-60-ans/) | S05: 200, S08: 200 | CONFIRMED | unchanged |
| c34 | 局部小雪板與大範圍雪崩不同，風吹雪可能改變表面痕跡。 | small-slab-remains（h4v072）；wind-softens-edge（h4v073）；unmeasured-snow（h4v074） | [S5](https://www.nature.com/articles/s43247-020-00081-8)、[S6](https://www.nature.com/articles/s43247-022-00393-x) | S05: 200, S06: 200 | CONFIRMED | unchanged |
| c35 | 後續考察在 2021 年 9 月以無人機測量可能帳篷位置附近地形。 | science-next-evidence（h4v075）；survey-date（h4v076）; scenes[survey-date].data | [S6](https://www.nature.com/articles/s43247-022-00393-x) | S06: 200 | CONFIRMED | unchanged |
| c36 | 後來地形測量發現局部較陡階梯，增加模型地形前提的支持。 | survey-drone（h4v077）；survey-step-close（h4v078） | [S6](https://www.nature.com/articles/s43247-022-00393-x) | S06: 200 | CONFIRMED | unchanged |
| c37 | 地面測量不能直接還原 1959 年雪下弱層的厚度、強度及完整結構。 | survey-two-researchers（h4v079）；snow-return-season（h4v080）；snow-return-question（h4v106）; scenes[snow-return-question].data | [S5](https://www.nature.com/articles/s43247-020-00081-8)、[S6](https://www.nature.com/articles/s43247-022-00393-x) | S05: 200, S06: 200 | CONFIRMED | unchanged |
| c38 | 作者報告 2022 年 1 月 29 日嚮導觀察到兩處近期雪板雪崩痕跡。 | tease-expedition（h4v007）；avalanche-date（h4v081）；nearby-avalanche-context（h4v082）; scenes[avalanche-date].data | [S6](https://www.nature.com/articles/s43247-022-00393-x) | S06: 200 | CONFIRMED | unchanged |
| c39 | 後來痕跡在鄰近山坡，並非事故當晚／原帳篷上方的同一事件紀錄。 | tease-expedition（h4v007）；separate-ridge（h4v083）；field-camera-back（h4v084） | [S6](https://www.nature.com/articles/s43247-022-00393-x) | S06: 200 | CONFIRMED | unchanged |
| c41 | 相較模型假設，後來雪板更軟、坡更陡、下方未被切開，觸發可能不同。 | softer-snow-block（h4v087）；natural-slope-no-cut（h4v088） | [S6](https://www.nature.com/articles/s43247-022-00393-x) | S06: 200 | CONFIRMED | unchanged |
| c42 | 2022 考察原定雪剖面／穩定度試驗受天氣阻礙。 | field-weather（h4v091） | [S6](https://www.nature.com/articles/s43247-022-00393-x)、[S10](https://actu.epfl.ch/news/intense-press-coverage-prompts-new-expeditions-to-/) | S06: 200, S10: 200 | CONFIRMED | unchanged |
| c43 | 作者文章與校方新聞談同一批研究／考察，多個網頁不構成多次獨立驗證。 | same-evidence-folders（h4v092）；shared-source（h4v093,h4v094）; scenes[shared-source].data | [S5](https://www.nature.com/articles/s43247-020-00081-8)、[S6](https://www.nature.com/articles/s43247-022-00393-x)、[S8](https://longread.epfl.ch/en/dossier/quand-la-science-permet-dexplorer-un-mystere-russe-vieux-de-60-ans/)、[S9](https://ethz.ch/en/news-and-events/eth-news/news/2022/03/the-dyatlov-pass-mystery-and-what-a-research-article-can-trigger.html)、[S10](https://actu.epfl.ch/news/intense-press-coverage-prompts-new-expeditions-to-/) | S05: 200, S06: 200, S08: 200, S09: 200, S10: 200 | CONFIRMED | unchanged |
| c44 | 雪板提供可能的離營機制，未證明當夜完整經過、離帳後的行動順序。 | case-status（h4v099）；outro（h4v102,h4v103,h4v104）; scenes[case-status].data, scenes[outro].data | [S5](https://www.nature.com/articles/s43247-020-00081-8)、[S6](https://www.nature.com/articles/s43247-022-00393-x)、[S8](https://longread.epfl.ch/en/dossier/quand-la-science-permet-dexplorer-un-mystere-russe-vieux-de-60-ans/) | S05: 200, S06: 200, S08: 200 | CONFIRMED | unchanged |
| c45 | 保留未知並不使所有傳說獲得相同證據地位。 | closing-folder（h4v100） | [S1](https://dyatlovpass.com/case-files-384-387-ru)、[S5](https://www.nature.com/articles/s43247-020-00081-8)、[S6](https://www.nature.com/articles/s43247-022-00393-x) | S01: 200, S05: 200, S06: 200 | OUT OF SCOPE | editorial inference; matches brief owner viewpoint and evidence hierarchy |
| c46 | 現場足跡以凸起壓實雪形示意，周圍雪面被風吹低，不畫成新踩出的凹洞。 | trail-varied（h4v015）；boot-print-evidence（h4v017）；broken-trail（h4v021）；trail-downhill（h4v022）；stride-evidence（h4v023）; scenes[trail-varied].data, scenes[boot-print-evidence].data, scenes[broken-trail].data, scenes[trail-downhill].data, scenes[stride-evidence].data | [S4](https://dyatlovpass.com/case-files-298-300) | S04: 200 | CONFIRMED | unchanged |
| M1 | 佳特洛夫事件：九個人為何離開山坡上的帳篷？｜奇聞檔案局 | youtube.title | [S01](https://dyatlovpass.com/case-files-384-387-ru), [S05](https://www.nature.com/articles/s43247-020-00081-8) | S01: 200, S05: 200 | CONFIRMED | unchanged; question does not assert a solved cause |
| M2 | Empty tent and shoes in the tent, dated 1959 | thumbnail.data.headline/tag/sub | [S01](https://dyatlovpass.com/case-files-384-387-ru), [S04](https://dyatlovpass.com/case-files-298-300) | S01: 200, S04: 200 | CONFIRMED | unchanged |
| M3 | Description: tent and tracks; cut analysis; closing record; slab model and later survey; source-read date | youtube.description | [S01](https://dyatlovpass.com/case-files-384-387-ru), [S02](https://dyatlovpass.com/case-files-303-304-ru), [S05](https://www.nature.com/articles/s43247-020-00081-8), [S06](https://www.nature.com/articles/s43247-022-00393-x), [S11](https://www.interfax.ru/russia/649229), [S12](https://www.interfax.ru/russia/716956) | S01/S02/S05/S06/S11/S12: 200 | CHANGED | source-read date 2026-10-12 -> 2026-10-14; stale future reread warning removed |
| M4 | 佳特洛夫事件, 戴洛夫山口, 奇聞檔案局, 雪板雪崩, 歷史懸案 | youtube.tags[] | [S01](https://dyatlovpass.com/case-files-384-387-ru), [S05](https://www.nature.com/articles/s43247-020-00081-8) | S01: 200, S05: 200 | OUT OF SCOPE | topic tags; no further factual assertion |

## Verdict and limits

- 47 grouped checkable-claim/metadata rows: 42 CONFIRMED, 3 CHANGED (two historical wording fixes plus one date metadata correction), 0 NOT FOUND, 2 OUT OF SCOPE. Two factual changes in this round; the greater-than-three rule does not require verify-2.
- c15: S03 p312 says tracks suggested normal walking. It does not describe a stride-length measurement. h4v023, card, SVG, claims and notes now say tracks.
- c16: S01 p386 places three bodies on the fire-to-tent line, but only Slobodin and Kolmogorova were described as face down with postures suggesting crawling. Dyatlov lay on his back, head toward the tent. h4v110 and claims now restrict that inference to two.
- The 1959 file says a force of nature, not a named slab mechanism. Later slab work models physical possibility. The 2022 guides saw traces nearby under different slab/slope/cut conditions, not the 1959 event and not a full reproduction.
- Historic dates do not expire soon. URL availability, image licenses and media receipts can change. All 12 source entries now say checked_on 2026-10-14, and the description accurately describes the fresh text readback. Image attribution and license remain for production-stage asset check.
- c45 is an editorial evidence-weight judgment, marked in claims.md and aligned with the brief.md owner viewpoint: remaining uncertainty does not give unsupported legends equal weight.
- Listener pass: zero spoken lines over 40 characters; zero verification formula phrases, Latin words, parentheses or URLs in narration; no source-fact reveal inversion seen. Conceptual SVGs and anonymous searcher imagery must not be presented as incident-time footage or measured 1959 snow profiles.
- No unresolved checkable number, date, identity or model/result claim remains in the final text. Source-custody and prosecutor-report limits are stated above.

## Recheck

- Narrative panel PASS 11/11 at 7b9e0ce81bffe363.
- Lint: 0 errors, 0 warnings; estimated 8.7 min and 101 lines (2026-10-14 final metadata/prompt revision).
- Static renderProblems(doc, root, workdir): [] (separate preflight); no rendered media or audio playback is implied.
