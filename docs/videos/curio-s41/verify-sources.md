# S41 independent primary-source audit — 2026-10-20

## Verdict

**Final verdict: PASS for source feasibility and revised Q01–Q15.** Q06 now attributes penalties to Li Si’s proposal and accurately says `官吏知情不舉`; Q10 cites the J6 L8980 year label; Q15 separates 《易》 word variants from 《書》 lost chapters. `brief.md` now says `史官所藏的非秦記錄`, and `research.md` separately anchors 侯生、盧生. No factual or broken-anchor blocker remains in these three documents. The central answer is textually defensible: the *Shiji* passage does not order every book burned; it names non-Qin records under the historians, book possession outside the 博士官 clause, and three explicit practical-book exceptions. It also specifies harsh penalties. The four witnesses here are transmitted, later historiography, **not an extant Qin order, Qin-law manuscript, execution tally, or archaeological proof of the fate of each title**.

I independently downloaded the four **commit-pinned raw** Kanripo files by HTTPS into new `/tmp/s41-independent-*.txt` paths and read the cited lines with one-based physical line numbers (`nl -ba`). I did not use earlier `/tmp/s41-*.txt` copies. All four hashes match `research.md`:

| Code | Fixed raw file (new copy) | SHA-256 verified | Lines |
| --- | --- | --- | ---: |
| J6 | [KR2a0001_100.txt](https://raw.githubusercontent.com/kanripo/KR2a0001/1c19dc6fa970b1c530fced9e8e3697d19163c26c/KR2a0001_100.txt) (`/tmp/s41-independent-J6.txt`) | `b2c951b0613186eca4026c0f91d1dc913046313e778a2af368fd32fd63545991` | 20,557 |
| J87/J121 | [KR2a0001_500.txt](https://raw.githubusercontent.com/kanripo/KR2a0001/1c19dc6fa970b1c530fced9e8e3697d19163c26c/KR2a0001_500.txt) (`/tmp/s41-independent-J87J121.txt`) | `02ebd6e50938cf3ab8c4df6bfa8d880a6c434f51518d38eba2183829dcebb07e` | 59,225 |
| H2 | [KR2a0007_002.txt](https://raw.githubusercontent.com/kanripo/KR2a0007/683113d4baf6febecaf2ccb7913df87c4d68d454/KR2a0007_002.txt) (`/tmp/s41-independent-H2.txt`) | `26e42470c1a7351fcceca967ea35514ca9567a9fe3de47e5697c63ff4bb4af20` | 169 |
| H30 | [KR2a0007_030.txt](https://raw.githubusercontent.com/kanripo/KR2a0007/683113d4baf6febecaf2ccb7913df87c4d68d454/KR2a0007_030.txt) (`/tmp/s41-independent-H30.txt`) | `58fd3be80541ddd20bf86f2523aae54e3d9256f96320a698d93e210404d06f8e` | 1,285 |

## Q01–Q15 against the exact text

This table documents the independent textual checks, including issues found in the initial draft and resolved in the revised documents.

| ID | Result | Evidence and limits |
| --- | --- | --- |
| Q01 | PASS | J6 L8835 says `三十四年`; L8843 says `始皇置酒咸陽宮`. Its present anchor L8827–8848 contains both. This is *Shiji* chronology, not a Qin court transcript. |
| Q02 | PASS | J6 L8863–8885 has 淳于越, 殷周, `封子弟功臣`, and `何以相救哉`; he disputes political arrangements, not a proposed book policy. |
| Q03 | PASS | J6 L8913–8947 has `學古`/`以非當世`, `私學`/`非法教`, and `主勢降乎上`; the row accurately attributes this reasoning to Li Si. |
| Q04 | PASS, clarify shorthand | J6 L8951–8952 reads `臣請史官 / 非秦記皆燒之`. The object is the **non-Qin records of/under the historians**. Do not attach `非秦` to `史官` (“non-Qin historians”) or infer that all official archives were exempt. The same text states a proposed rule, not a count of books lost. |
| Q05 | PASS, clarify scope | J6 L8953–8957 reads `非博士官所職，天下敢有藏《詩》、《書》、百家語者，悉詣守、尉雜燒之`. The 博士官 qualification belongs to this possession clause. `天下敢有藏` supports a summary about non-exempt private possession, but the text does not itself say every book in 博士官 custody survived or define the state of every other office's holdings. |
| Q06 | **PASS after wording and citation revisions** | The original anchor J6 L8962–8975 started **after** `有敢偶語《詩書》者` at L8961; the revised anchor now starts at L8961. J6 L8965–8966 says `吏見知不舉者與同罪`, meaning officials who knew and failed to report. The revised row uses `官吏知情不舉` and explicitly calls this Li Si’s proposal as narrated by *Shiji*; both issues are resolved. |
| Q07 | PASS | J6 L8972–8973 explicitly says `所不去者，醫藥卜筮種樹之書`. Name only these three classes, not all agriculture, science, or religious literature. |
| Q08 | PASS | J6 L8974–8976 has `若欲有學法令，以吏為師。制曰：「可。」` The emperor's assent is narrated in *Shiji*, and does not prove universal execution. |
| Q09 | PASS | J87 L19445–19456 repeats removal, thirty days, the three exceptions and official teaching; L19460–19463 narrates assent and collection, but supplies no local execution total. J87 is a second *Shiji* location, not an independent Qin witness. |
| Q10 | **PASS after citation revision** | J6 L9180–9184 says 御史 examined `諸生`, `四百六十餘人`, `皆阬之咸陽`; L9191–9194 has 扶蘇. The earlier L9138–9195 span did not contain `三十五年`, which is J6 L8980; the revised Q10 now adds J6 L8979–8983. The revised research row separately anchors 侯生/盧生 at J6 L9109–9115 and their departure at L9155 within the case span. Do not use 460 as book-ban punishment statistics. This is a later-year episode in the annal, not the text of the previous year's proposal. |
| Q11 | PASS | J6 L9173–9184 calls those examined `諸生`; L9194 has 扶蘇's `諸生皆誦法孔子`; J121 L48287–48290 retrospectively says `焚《詩書》，阬術士`. These are differing terms within one *Shiji*, and neither proves that all 460 were exclusively 儒生 or exclusively 方士. |
| Q12 | PASS, avoid causation jump | J121 L48656–48675 says 伏生 had been a Qin 博士, `秦時焚書，伏生壁藏之`, then `其後兵大起，流亡，漢定，伏生求其書，亡數十篇，獨得二十九篇`. “After war and displacement he found only 29” is accurate. The passage does not allocate the missing chapters between the decree, concealment, war, and later loss. Present wall concealment as *Shiji*'s retrospective story, not a photographed/recovered wall cache. |
| Q13 | PASS | H2 L89 and L92–L94 say `四年` and `三月 ... 除挾書律`. The main annal establishes repeal of a law by that name; the parenthetical `應劭曰`/`張晏曰` glosses are later commentary, **not surviving text of a Qin statute**. Do not claim the exact original provisions, uninterrupted enforcement until Hui Di, or immediate recovery of books. |
| Q14 | PASS | H30 L19–L30 says Han opened routes for donated books; books were still incomplete by Wu Di's time; by Cheng Di, 陳農 sought lost books and 劉向 was assigned collation. This is retrospective catalogue preface, not evidence that everything was restored. |
| Q15 | **PASS after wording revision** | H30 L63–L67 says 《易》 continued through divination and records wording omissions (`或脱去無咎悔亡`), **not missing chapters**. H30 L85–L101 recounts 《書》's lost chapters, 伏生's 29 chapters, a claimed 孔壁 version, and missing slips/characters. The revised Q15 says 《易》傳本文字有異 and reserves `缺篇` for 《書》; this is supported. The 孔壁 account is later retrospective tradition; L91–L92 even preserves divergent identifications in a commentator's note. |

## Cross-document review and scene boundaries

1. The revised `brief.md` now says `史官所藏的非秦記錄`, resolving the initial ambiguity in `非秦史官記錄`. In any card, quote the fixed original `史官非秦記` with a source, then explain the syntax. Keep the historian clause distinct from the 博士官/possession clause.
2. The revised `research.md` row 13 now distinguishes 《易》字句差異 from 《書》缺篇; this resolves the initial imprecise `缺頁` wording.
3. The revised `research.md` now cites both the `三十五年` year label (J6 L8980) and the named 侯生、盧生 at J6 L9109–9115. Let visuals show the investigation through a sourced record/blank documents and 扶蘇's remonstrance, not a reconstructed execution. No scene should turn the 460 into people punished for possessing the books named in the prior-year proposal.
4. H2's `除挾書律` may appear as a sourced short quotation. Do not place it on a purported Qin decree: the evidence is the later *Han shu* annal. J6 and J87/J121 are one Han-era historiographic work; H2/H30 are a later compilation with inline notes. These layers do not independently authenticate an extant Qin-law original.
5. The brief's closing `對傳承留下可見的缺口` works as cautious synthesis if the script attributes loss and recovery to the later histories. Avoid drawing a precise causal line from the 30-day order to every missing 《書》 chapter or to a measured book-loss rate.

All 48 GitHub blob links in the three revised documents were checked against the pinned filenames, commits, and fresh raw line counts: 0 malformed, wrong-commit, or out-of-range anchors. This validates link structure and anchor range; it does not claim a browser page render was tested. No repository files, site gates, or paid media were changed by this independent audit. This receipt is the audit deliverable.
