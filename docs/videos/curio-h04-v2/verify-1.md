# H04 v2 | Independent fact check, round 1 + incremental recheck

**Current status (2026-10-14):** `script.md` SHA-256 `3bfdfb11bccfb8e1f017cdd6edcfdc9c4b1b5bee491e049f8e081dfd56ad8fae` and `video.json` SHA-256 `77d4bff38b04972bd51c206a517691061faddcd28332cf4d98b037284b81f615`. The independent round-17 blind read passed all 11 questions at narrative hash `e9062e4ca246f5d0`. Current narration is 8:40 for 100 lines; `check-audio` has zero flags and the audio review was approved and pulled back. The visual gate is unfinished: the monthly judge quota is 10,000/10,000, old keyframes do not match current look/picture hashes, and storyboard, rendered frames, MP4, captions, upload package, owner playback and upload are absent. Earlier hashes and passes below are historical snapshots.

Round 1 was checked on 2026-10-14 against its then-corrected video.json, then incrementally rechecked after narration clarity edits. The checker did not write the H04 script. The round-1 hash binding below is historical; the final current-file binding and media status are at the end of this record. This is a text and source gate, not media playback or owner acceptance.

## Round-1 bound files and coverage (historical)

- video.json SHA-256: 3c2d69d7ac4b8648de3b82d3d2219211b543bfeca5c41d71a2fd6e54ab3e8e6a
- script.md SHA-256: c301f67c3bab8cd2f80ca51b29c710df897786ef69f8129f458c7c3cb8b7a15b
- Earlier narrative hash: 08d742bb00e24507; its round 8 panel passed 11/11. A later independent blind read found new narrative failures, so this verdict does not apply to the current file.
- At round 1: 101 spoken text lines, all non-shot scene.data, thumbnail, YouTube title/description/tags and 12 source entries inventoried. No say overrides. Every scene had a claim ID. The raw 418-string path inventory is external at `<home>/mokaair-work/videos/curio-h04-v2/_tools/claim-inventory.json`. Synthetic shot prompts and pure design labels are visual directions, not asserted historic observations.

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
| c15 | 一位勘驗者認為所見足跡顯示普通步行；無法保證全程步態或情緒。 | stride-evidence（h4v023）；stride-inference（h4v024,h4v025）; scenes[stride-evidence].data, scenes[stride-inference].data | [S3](https://dyatlovpass.com/case-files-309-312-ru) | S03: 200 | CHANGED | h4v023/card: stride length -> tracks; S03 p312 says normal walking but does not state a stride-length measurement |
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
| c32 | 數小時是模型情境；研究由推定時距回算積雪通量，並非獨立預測事發時刻。 | model-hours（h4v068）；model-not-timer（h4v069）; scenes[model-hours].data, scenes[model-not-timer].data | [S5](https://www.nature.com/articles/s43247-020-00081-8) | S05: 200 | CONFIRMED | current script removes repeated h4v070 |
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
- c15: S03 p312 says tracks suggested normal walking. It does not describe a stride-length measurement. h4v023, card, claims and notes now say tracks.
- c16: S01 p386 places three bodies on the fire-to-tent line, but only Slobodin and Kolmogorova were described as face down with postures suggesting crawling. Dyatlov lay on his back, head toward the tent. h4v110 and claims now restrict that inference to two.
- The 1959 file says a force of nature, not a named slab mechanism. Later slab work models physical possibility. The 2022 guides saw traces nearby under different slab/slope/cut conditions, not the 1959 event and not a full reproduction.
- Historic dates do not expire soon. URL availability, image licenses and media receipts can change. All 12 source entries now say checked_on 2026-10-14, and the description accurately describes the fresh text readback. Image attribution and license remain for production-stage asset check.
- c45 is an editorial evidence-weight judgment, marked in claims.md and aligned with the brief.md owner viewpoint: remaining uncertainty does not give unsupported legends equal weight.
- Earlier listener pass: zero spoken lines over 40 characters; zero verification formula phrases, Latin words, parentheses or URLs in narration. Card reveal order still requires inspection in a rendered cut. MiniMax concept illustrations and anonymous searcher imagery must not be presented as incident-time footage or measured 1959 snow profiles.
- At this source-check round, no unresolved checkable number, date, identity or model/result claim remained. Later narration edits and their current-file check are recorded below. Source-custody and prosecutor-report limits are stated above.

## Incremental source check: narration clarity edits

Eight spoken lines changed after round 1; the source register, visual claims, title and description did not. The original claim table above records round-1 findings; these rows checked wording at that incremental stage. On 2026-10-14, the 1959 closure transcript was reopened, the authors' 2021 and 2022 articles were read back from the publisher's full HTML, and the ETH/EPFL accounts were reopened. The 2022 field observations support conditions and local avalanche occurrence, not a reconstruction of the 1959 event.

| Line | Wording at that round / factual boundary | Source | Incremental verdict |
|---|---|---|---|
| h4v028 | 「還沒找到的四人」在五月於溪溝附近發現；沒有宣稱四人那時才失蹤。 | [S01](https://dyatlovpass.com/case-files-384-387-ru), sheet 386 (4 May, four named bodies) | CONFIRMED; c16 unchanged |
| h4v068 | 模型產生可行情境，但不能求得事故發生的實際時刻。論文的延遲範圍依賴假設的風搬雪量，且以法醫推定時距回算條件。 | [S05](https://www.nature.com/articles/s43247-020-00081-8), Results / Discussion | CONFIRMED; c32 limitation clearer |
| h4v070 (removed after this round) | Earlier line repeated h4v068's model-time limit. Its removal does not weaken the retained h4v068 boundary. | [S05](https://www.nature.com/articles/s43247-020-00081-8), wind deposition flux / forensic-delay discussion | historical only; c32 retained |
| h4v072 | 「小規模雪板滑動」準確傳達模型的 relatively small slab，且沒有稱整座山崩落。 | [S05](https://www.nature.com/articles/s43247-020-00081-8), Abstract / Results | CONFIRMED; c34 unchanged |
| h4v078 | 無人機地形測量讓局部陡坡這項模型前提有更多依據；未說事故雪板已獲證實。 | [S06](https://www.nature.com/articles/s43247-022-00393-x), summer 2021 drone survey / Fig. 2 | CONFIRMED; c36 unchanged |
| h4v080 | 現行「山坡的形狀」只是前版「坡面形狀」的同義改寫；坡形不能單獨推算 1959 年埋藏弱層厚度或強度，仍是測量範圍與模型參數的界線。 | [S05](https://www.nature.com/articles/s43247-020-00081-8), assumed snow properties; [S06](https://www.nature.com/articles/s43247-022-00393-x), terrain survey | CONFIRMED as a limited inference; c37 unchanged |
| h4v092 | 作者發表後續研究文章，ETH、EPFL 校方也發表介紹考察的文章；沒有把校方報導算成獨立科學重演。 | [S06](https://www.nature.com/articles/s43247-022-00393-x), [S09](https://ethz.ch/en/news-and-events/eth-news/news/2022/03/the-dyatlov-pass-mystery-and-what-a-research-article-can-trigger.html), [S10](https://actu.epfl.ch/news/intense-press-coverage-prompts-new-expeditions-to-/) | CONFIRMED; c43 unchanged |
| h4v102 | 當輪的「雪板滑動可行，仍未證實」保留作者提出 plausible explanation 與無法重建當夜完整事件的界線；現行台詞另在下節核對。 | [S05](https://www.nature.com/articles/s43247-020-00081-8), [S06](https://www.nature.com/articles/s43247-022-00393-x), [S10](https://actu.epfl.ch/news/intense-press-coverage-prompts-new-expeditions-to-/) | CONFIRMED for earlier wording only |

No new checkable claim or new unsupported certainty was introduced by those eight edits. This was an incremental source check, not a second exhaustive 418-string inventory.

## Recheck

- The earlier narrative panel passed 11/11 at 08d742bb00e24507. Later wording and scene-order revisions invalidated that panel; the current-hash result is below.
- Earlier lint and duration are historical; see current-hash result below.
- Static renderProblems(doc, root, workdir): [] (separate preflight); no rendered media or audio playback is implied.

## Earlier narrative and source-bound incremental recheck (historical)

2026-10-14 earlier independent blind read: `script.md` SHA-256 `bfc8957d9f8d9b813e365995ff801a7f3f981c6cb38cf6e8deeb9810eb87e661`, narrative hash `45fbdc690376028d`; all 11 questions passed, including the nine mandatory questions. Its exact yes/no evidence was recorded at that stage; `review/narrative.json` now holds the later round-17 result. The corresponding `video.json` at that earlier review was `621b0f4fef51ce0d151e143eb6852898fa34e003098cef02239ee90ad2f6558b`. This earlier pass is not the current narration or visual gate.

| Line or card | Claim and limit at that round | Direct source | Verdict |
|---|---|---|---|
| h4v027–029 | The last four were still missing when the April tent finding was released; they were found near the ravine in May, and their discovery appears in the May closure. This tells the investigation sequence, not each person's movements. | [S01](https://dyatlovpass.com/case-files-384-387-ru), pp. 385–387; [S02](https://dyatlovpass.com/case-files-303-304-ru), pp. 303–304 | CONFIRMED; c16, scene order changed |
| h4v034–035 | The cloth examination concluded inside-out cuts, but did not identify who cut or each person's exit. | [S02](https://dyatlovpass.com/case-files-303-304-ru), p. 304 | CONFIRMED; c11/c12, clearer question/limit |
| h4v036–038 (earlier wording) | The May 28 closure records belongings and inside cuts; Ivanov signed it. The question about the cause he wrote is paid off at h4v039. A later edit replaced h4v036's repeated inventory with the document's four-page structure. | [S01](https://dyatlovpass.com/case-files-384-387-ru), pp. 384–387 | CONFIRMED for earlier wording; c13/c17/c19 |
| h4v066–067 | The paper models failure of a weak layer and a possible delayed slab release under its assumed conditions. The time range is fitted against forensic estimates, not a clock independently measuring the 1959 event. | [S05](https://www.nature.com/articles/s43247-020-00081-8), model/results | CONFIRMED; c28/c31 |
| h4v099, h4v102 and ending cards | The model does not explain the group after leaving the tent or body locations. A small slab is a possible reason for leaving, not proof of the full night. The answer card keeps the missing contemporary evidence visible. | [S05](https://www.nature.com/articles/s43247-020-00081-8), conclusion; [S06](https://www.nature.com/articles/s43247-022-00393-x), later-field limits | CONFIRMED; c44, narrowed ending |

That round's lint had zero errors and three topic-frequency warnings; its body estimate was about 8.70 minutes for 101 spoken lines. The final 100-line script and measured narration are recorded below; card timing and source labeling still need inspection in a rendered cut.

## Intervening narrative repair (historical, 2026-10-14)

An independent recheck of the intervening `b02402c546239d71` script found two repeats: h4v036 repeated the inside-cut and gear evidence, while h4v070 repeated h4v068's model-time limitation. The repair changed h4v036 to the closure's four-page structure and removed h4v070. That intermediate 100-line TTS measured 8:41; its one-line redo, hashes and pending-review status are historical. The final text and media evidence follow.

## Current-file recheck and remaining media gates (2026-10-14)

- `script.md` SHA-256 `3bfdfb11bccfb8e1f017cdd6edcfdc9c4b1b5bee491e049f8e081dfd56ad8fae`; `video.json` SHA-256 `77d4bff38b04972bd51c206a517691061faddcd28332cf4d98b037284b81f615`. The independent round-17 blind read bound to narrative hash `e9062e4ca246f5d0` passed 11/11. Its yes/no evidence is in the v2 work directory's `review/narrative.json`. The line changes at h4v013, h4v036, h4v067 and h4v102 preserve the checked boundaries: the shoes prompt is an explicit callback to the opening; four pages and the last-page cause are supported by [S01](https://dyatlovpass.com/case-files-384-387-ru); delayed release remains conditional under [S05](https://www.nature.com/articles/s43247-020-00081-8); and a slab remains only a possible reason to leave the tent. h4v070 stays removed.
- Current 100-line narration measures 8:40 (15,604 frames at 30 fps). `timeline.json` binds speech hash `ed9b3d4509f1a7b9`; `review/check-flags.json` lists zero flags. The audio review was pushed, autoapproved and pulled back; `node tools/video/cli.mjs status --slug curio-h04-v2` reports `narration approved`. This is a machine audio gate, not a record of owner listening.
- The current picture plan has 52 MiniMax image-01 shots. Estimated illustration share is 54.07%; its boots shot is 5.9 seconds and outro shot is 7.3 seconds. Static cadence/render preflight reported no problems. These are plan measurements, not proof of rendered duration or visual correctness.
- The judge monthly allowance is 10,000/10,000. The old keyframe manifest was drawn under earlier look/picture hashes and includes missing frames and human-identified false scenes; it is audit history, not approved current visual material. New paid keyframes and human image inspection remain before storyboard, render, assemble, captions, MP4, package, owner playback or YouTube upload. No v2 upload has occurred.
