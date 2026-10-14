# H06 v2｜獨立事實覆核（第 1 輪）

日期：2026-10-14。原覆核者未撰寫 H06 v2 旁白；先只讀 CLI 旁白及 11 題，對舊敘事 hash `3dfdec113ca9958c` 得到 **11/11 PASS**（答案與 gate 存外部工作目錄 `review/narrative-answers-round3.json`、`review/narrative.json`），再閱讀 `video.json`、寫手資料與原始來源。其後的片尾縮短、刪景、章節順序與回呼及去重、法院重排修訂由改句者作增量來源自查；視覺修改前 `cd0c02e7514e16e0` 再獲獨立盲評 **11/11 PASS**。**音訊修訂前的畫面版 `5616d43e89294144` 也曾由獨立盲評通過 11/11**，並對 BGH 原判決掃描、PLOS ONE 原文與 Stoneking 第一手訪談作增量來源抽查；這不冒稱全部畫面欄位重新逐項簽核。站主已選大綱 A；現行音訊修訂後敘事 hash `349cf912c147f530` 另獲獨立盲評 **11/11 PASS** 並綁定外部 `review/narrative.json`。本文不代替現行音訊、圖像、渲染、成片播放或發布核准。

## 範圍、版本與來源

- 音訊修訂前讀回的 `video.json` SHA-256：`19f0fa0534933043307815c9bb18145a8ed0ac6891742f4206a50eba78384e74`；`script.md`：`fd2189d186df57c01ba261817aad4fb6873ac1d53ab1b36c1d4438330662b328`；`claims.md`：`fb56896a8f7ccfadd6a11ebbf53b395f8031e3864fb3ea956c2997e03a7f8cd4`；`brief.md`：`df25a00988d06e30f2e6a08e84df0eaecacb12ba4c929bb1e4670acea6756b1d`。上述為當輪檔案 SHA，當輪敘事 hash 為 `5616d43e89294144`，85 景、104 句、七章；外部舊 `review/narrative.json` 綁此 hash 並記錄 11/11 PASS。
- 原獨立覆核從 91 景抽出 112 句旁白，連同每張資料卡的 `data`、縮圖、YouTube 標題／說明／標籤，共 **470 個原始字串／數值欄位**，逐項清單在外部 v2 工作目錄 `_tools/claim-inventory.md`。現行 85 景、104 句、七章；舊清單不冒稱為新稿逐欄重抽。下表將重複的可查事實整併為 26 組；原核對清單的其他未改項保持歷史紀錄，新改句和畫面另在文末逐項增量核對。`say` 欄位原逐句抽取，本稿沒有覆寫。
- 2026-10-14 取得 [1970 年德國聯邦最高法院判決掃描](https://www.prinz.law/static/urteile/pdf/bgh/III_ZR_139-67.pdf)全 144 頁，逐項親讀與本稿有關的 PDF 第 3、5–8、13–15、138–139、143–144 頁。此為第三方保存的原判決掃描，**非官方法院網站逐字稿**；掃描中的部分人名及日子遮蔽。另重開 [PLOS ONE 2009 原文](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0004838)、[研究者 Stoneking 第一手訪談](https://dnalc.cshl.edu/view/15163-Solving-one-of-history-s-mysteries-Mark-Stoneking.html)、[冷泉港教師指南](https://www.dnai.org/romanovs/romanov_guide.pdf)與[工作簿](https://dnalc.cshl.edu/assets/files/dnalc-live/17207.the_mystery_of_anastsia_workbook.pdf)、[NIJ 母系 DNA 教材](https://nij.ojp.gov/nij-hosted-online-training-courses/principles-forensic-dna-officers-court/08-mitochondrial-dna-y-str-analysis/introduction-mtdna/maternal-inheritance-0)，均 HTTP 200。
- [Nature Genetics 1995 書目頁](https://www.nature.com/articles/ng0195-9)為 HTTP 200，但論文正文需訂閱；本文的樣本結論據研究者第一手訪談及教學原件，不冒稱逐字讀過論文。[PNAS 2009 出版頁](https://www.pnas.org/doi/10.1073/pnas.0811190106)直接讀取為 HTTP 403；[NIH E-utilities 所載原作者摘要](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=19251637&retmode=xml)為 HTTP 200，明載兩墓研究辨認全家包括五名子女。影片不以它替 PLOS ONE 的第二墓姊妹指定個別姓名。
- 五張候選史料照的 Commons 原件頁均 HTTP 200；v2 外部 `stock/` 五檔重新算 SHA-256，全部與檔名及 [assets-provenance.md](assets-provenance.md)相符。現行僅三張排入圖片卡並列入 `video.json.assets[]`，年份／年代、館藏與「不是現場／證物」限制逐張檢查；其餘兩張只留候選素材記錄，沒有把示意插圖當原件。

## 逐項主張

`CONFIRMED`／`CHANGED` 記錄原獨立覆核的來源判斷；本輪動到的主張列另標「編稿增量相符；待獨立重綁」。下表與文末增量段合看，才能對照現行 SHA；它不宣稱原覆核者已重新逐欄核准新稿。

| # | 主張 | where（句 ID／scene.data） | URL | HTTP | 判定 | 修改前 → 修改後 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 / c01 | 1918 年尼古拉二世夫婦及五名子女遇害；倖存說曾流傳。 | qwh4、4jhc、berlin-timeline.data、n3d8、berlin-family-places.data | [plos](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0004838) | 200 | CONFIRMED | — |
| 2 / c02 | 1920 年 2 月柏林運河救起女子；不報姓名，警方未查出身分。 | j6u5、v201、cr5q、rbd5、berlin-name-blank.data、c63r、berlin-hospital-window.data、uq5m、berlin-staff-corridor.data、qwh4、4jhc、berlin-timeline.data | [court](https://www.prinz.law/static/urteile/pdf/bgh/III_ZR_139-67.pdf)、[csueb](https://www.csueastbay.edu/museum/pre-exhibit/dna/history-fraulein.html) | 200／200 | CONFIRMED | — |
| 3 / c03 | 1922 年病院裡有人把女子與公主連上；判決保留姓名先由誰提出的兩種說法。 | dszz、v202、rbd5、berlin-name-blank.data、uq5m、berlin-staff-corridor.data、cap5、n3d8、berlin-family-places.data、e773、9tfu、uqyb、u6iw、hospital-album-hands.data、hcra、kvce、jnga、hospital-two-starts.data、smmb、x2py、8nrj | [court](https://www.prinz.law/static/urteile/pdf/bgh/III_ZR_139-67.pdf) | 200（原獨立來源讀回） | 編稿增量相符；待獨立重綁 | dszz 不再指訪客先帶進名字。 |
| 4 / c04 | 1928 年遠親 Xenia Leeds 邀她赴美；接待與其他皇室親友的否認均非確定身分證明。 | egvx、v208、relatives-day-room.data、28mj、2scy、xhf4、euyy | [court](https://www.prinz.law/static/urteile/pdf/bgh/III_ZR_139-67.pdf)、[time](https://time.com/archive/6662258/russia-whose-body/) | 200／200 | CONFIRMED | — |
| 5 / c05 | 民事請求是給付、繼承權確認及安德森主張舊繼承證書有誤；公主身分為訴請前提，證書有誤並非法院已認定的事實。 | ykiq、pfpa、8nrj、kv2b、kyrc、2ap4、fba5、court-question-card.data、v209、court-question-certificate.data、v210、court-question-premise.data、xhf4、ftkk、court-proof-steps.data | [court](https://www.prinz.law/static/urteile/pdf/bgh/III_ZR_139-67.pdf) | 200 | CHANGED | 三張 court-question 字卡 kicker「身分訴訟」→「繼承權官司」，對齊判決的財產／繼承訴請；現行 v209 又明說「她還主張」，避免把訴求寫成既判事實。 |
| 6 / c06 | 1967 前審證據判斷不利；安德森提起法律審後，1970 德國聯邦最高法院駁回，維持公主身分未獲證明。 | ykiq、pfpa、kyrc、26m8、fba5、court-question-card.data、v209、court-question-certificate.data、v210、court-question-premise.data、euyy、ftkk、court-proof-steps.data、sexv、v212、95fq、wmiq、court-two-years.data、qyt5、court-two-levels.data、i2rk、court-high-result.data、y57g、8erd、court-ruling-scope.data | [court](https://www.prinz.law/static/urteile/pdf/bgh/III_ZR_139-67.pdf) | 200（原獨立來源讀回） | 編稿增量相符；待獨立重綁 | 26m8 不再先說 1970；先由 sexv／wmiq 報 1967 前審，i2rk 才報三年後的法律審；刪去 mrsj 報題句。 |
| 7 / c07 | 被告提出 Franziska Schanzkowska 說法；法院不以該身分或主觀冒認動機作裁定。 | ykiq、pfpa、sywj、y57g、8erd、court-ruling-scope.data、bnbr | [court](https://www.prinz.law/static/urteile/pdf/bgh/III_ZR_139-67.pdf)、[workbook](https://dnalc.cshl.edu/assets/files/dnalc-live/17207.the_mystery_of_anastsia_workbook.pdf) | 200／200 | CONFIRMED | — |
| 8 / c08 | 安德森 1984 年過世；身分研究發表於 1995 年 1 月。 | dw29、v203、tgm6、dna-publication.data | [csueb](https://www.csueastbay.edu/museum/pre-exhibit/dna/history-fraulein.html)、[nature](https://www.nature.com/articles/ng0195-9) | 200／200（訂閱摘要／書目） | CONFIRMED | — |
| 9 / c09 | 頭髮與醫院保存的組織由獨立團隊分析並互相符合，均不符皇后已知母系參照；片尾首次直說公主身分的否定答案。 | dw29、v203、cr5q、bxmt、v216、tgm6、dna-publication.data、kckw、v217、dna-hair-and-box.data、bp4e、xx8w、4yw7、v218、8hyx、ix4m、fa8j、dna-mismatch.data、xz9y、d7um、end-outro.data | [stoneking](https://dnalc.cshl.edu/view/15163-Solving-one-of-history-s-mysteries-Mark-Stoneking.html)、[csueb](https://www.csueastbay.edu/museum/pre-exhibit/dna/history-fraulein.html) | 200／200 | CONFIRMED（片尾增量） | 刪去 xdsv／56m3；d7um「她不是安娜塔西亞」才直接回答開場，不指名另一個本名。 |
| 10 / c10 | 排除公主身分與支持女工身分，是不同層級的證據結論。 | v227 | [court](https://www.prinz.law/static/urteile/pdf/bgh/III_ZR_139-67.pdf)、[stoneking](https://dnalc.cshl.edu/view/15163-Solving-one-of-history-s-mysteries-Mark-Stoneking.html)、[guide](https://www.dnai.org/romanovs/romanov_guide.pdf)、[nij](https://nij.ojp.gov/nij-hosted-online-training-courses/principles-forensic-dna-officers-court/08-mitochondrial-dna-y-str-analysis/introduction-mtdna/maternal-inheritance-0) | 200／200／200／200 | CONFIRMED | — |
| 11 / c11 | 第一墓於 1970 年代末被找到、1991 年正式發掘，九人中有父母及三名女兒，少一男一女。 | yqep、v215、2pva、s4mq、grave-first-count.data、73wj、xz9y | [plos](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0004838) | 200 | CONFIRMED | — |
| 12 / c12 | 2007 年第二墓距第一墓約 70 公尺，官方整理出 44 件骨與牙碎片。 | pxbi、v204、v2jq、v219、j43h、v220、grave-distance.data、yv8b、grave-fragments-limit.data | [plos](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0004838) | 200 | CONFIRMED | — |
| 13 / c13 | 研究以母系、常染色體及 Y-STR 三種系統辨認第二墓的阿列克謝與一名姊妹。 | pxbi、v204、yv8b、grave-fragments-limit.data、znfv、grave-lab-sealed-tray.data、g6ne、7sxb、9jd8、h9hy、grave-three-tests.data、b5hx、grave-data-overlap.data、cfvr、jptu、92k7、grave-two-children.data、dkkf、jqxi、grave-two-papers.data | [plos](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0004838) | 200 | CONFIRMED | — |
| 14 / c14 | 俄美人類學者對缺哪位姊妹意見不同；PLOS 所報 DNA 無法單獨辨出瑪麗亞或安娜塔西亞。 | jptu、92k7、grave-two-children.data、v228、v229、grave-anthropologists-disagree.data、ce8r、zwkk、grave-which-sister.data、dkkf、jqxi、grave-two-papers.data | [plos](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0004838) | 200 | CONFIRMED | — |
| 15 / c15 | PNAS 2009 研究辨認兩墓合計含尼古拉二世夫婦全部五名子女。 | cr5q、cfvr、dkkf、jqxi、grave-two-papers.data、ufh6、grave-five-children.data | [pnas](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=19251637&retmode=xml)、[plos](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0004838) | 200（NIH E-utilities 原作者摘要；PNAS 站 403）／200 | CONFIRMED | 刪除純預告 56m3，研究結論仍在 ufh6。 |
| 16 / c16 | 法院、安德森檢體與兩墓研究回答不同問題，為編輯整理的證據分層。 | 73wj | [court](https://www.prinz.law/static/urteile/pdf/bgh/III_ZR_139-67.pdf)、[stoneking](https://dnalc.cshl.edu/view/15163-Solving-one-of-history-s-mysteries-Mark-Stoneking.html)、[plos](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0004838)、[pnas](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=19251637&retmode=xml) | 200／200／200／200（NIH E-utilities 原作者摘要；PNAS 站 403） | CONFIRMED | — |
| 17 / c17 | 本集材料無法判定安德森主觀上如何理解或接受公主名字。 | x2py、y57g、8erd、court-ruling-scope.data、bnbr、4s6y | [court](https://www.prinz.law/static/urteile/pdf/bgh/III_ZR_139-67.pdf)、[stoneking](https://dnalc.cshl.edu/view/15163-Solving-one-of-history-s-mysteries-Mark-Stoneking.html) | 200／200 | CONFIRMED | — |
| 18 / c18 | 地質學家 Alexander Avdonin 於 1970 年代末找到第一墓，與友人保密至 1991 年。 | 4uuj、et4h | [plos](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0004838) | 200 | CONFIRMED | — |
| 19 / c19 | 安德森母系 DNA 與 Carl Maucher 相符；Maucher 是 Franziska 的母系姪孫，支持女工說法。 | jmhr、pgcg、v223、dna-maucher-match.data、v224、v225、v226、dna-maucher-limit.data、end-outro.data | [guide](https://www.dnai.org/romanovs/romanov_guide.pdf)、[workbook](https://dnalc.cshl.edu/assets/files/dnalc-live/17207.the_mystery_of_anastsia_workbook.pdf) | 200／200 | CONFIRMED | — |
| 20 / c20 | 母系 DNA 可由親屬共享，相符不能單憑此唯一指名某人。 | v225、v226、dna-maucher-limit.data、end-outro.data | [nij](https://nij.ojp.gov/nij-hosted-online-training-courses/principles-forensic-dna-officers-court/08-mitochondrial-dna-y-str-analysis/introduction-mtdna/maternal-inheritance-0) | 200 | CONFIRMED | — |
| 21 | 1885 年 Dalldorf 病院外觀；F. A. Schwartz／Heimatmuseum Reinickendorf；非 1920 現場。 | berlin-hospital-window.data.caption／credit／image；assets[] | [原件頁](https://commons.wikimedia.org/wiki/File:Blick_auf_Irrenanstalt_Dalldorf_1885.jpg) | 200 | CONFIRMED | — |
| 22 | 約 1917 年 Nicholas II 與 Alexei；Bain／美國國會圖書館。 | berlin-family-places.data.caption／credit／image；assets[] | [原件頁](https://commons.wikimedia.org/wiki/File:Czar_%26_Czarewitch,_3-16-17_LCCN2014700375.jpg) | 200 | CONFIRMED | — |
| 23 | 安娜塔西亞真實肖像，拍攝於 1918 年前；Bain／美國國會圖書館；非訪客手上原件。 | hospital-album-hands.data.caption／credit／image；assets[] | [原件頁](https://commons.wikimedia.org/wiki/File:Grand_Duchess_Anastasia_Nikolaevna_Crisco_edit_letters_removed.jpg) | 200 | CHANGED | 肖像 caption 補「1918 年前」；YouTube 說明收窄為「可確認的年代及館藏」，不杜撰拍攝日。 |
| 24 | 1914 年羅曼諾夫全家照；Bain／美國國會圖書館；非訴訟證物。 | 候選素材記錄；現行未入片或 `assets[]` | [原件頁](https://commons.wikimedia.org/wiki/File:Russian_Royal_Family_LCCN2014694658.jpg) | 200 | CONFIRMED | — |
| 25 | 1917–18 年 Nicholas II 與三名女兒，Maria 為攝影者；耶魯 Beinecke；非墓地影像。 | 候選素材記錄；現行未入片或 `assets[]` | [原件頁](https://commons.wikimedia.org/wiki/File:RomanovsatTobolsk.jpg) | 200 | CONFIRMED | — |
| 26 | 片名、縮圖與說明重提公主身分問題、1920 救起、1970 判決、1995 檢體、2009 五名子女；未把母系匹配說成唯一指名。 | youtube.title／description／tags[]；thumbnail.data | [court](https://www.prinz.law/static/urteile/pdf/bgh/III_ZR_139-67.pdf)、[csueb](https://www.csueastbay.edu/museum/pre-exhibit/dna/history-fraulein.html)、[nature](https://www.nature.com/articles/ng0195-9)、[stoneking](https://dnalc.cshl.edu/view/15163-Solving-one-of-history-s-mysteries-Mark-Stoneking.html)、[plos](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0004838)、[pnas](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=19251637&retmode=xml)、[guide](https://www.dnai.org/romanovs/romanov_guide.pdf)、[nij](https://nij.ojp.gov/nij-hosted-online-training-courses/principles-forensic-dna-officers-court/08-mitochondrial-dna-y-str-analysis/introduction-mtdna/maternal-inheritance-0) | 200；PNAS 站 403，NIH 原作者摘要 200 | CONFIRMED | — |
| 27 | 所有 shot 的匿名人物、桌面、光線、無字道具、鏡頭運動屬情境示意；章名、CTA 與製作設定不是歷史事實。 | scenes[].data.prompt／camera／visual；scenes[].chapter；end-outro.data；thumbnail.data.tag | video.json 的 youtube.description | 本地 | OUT OF SCOPE | — |

## 結論與交接

- **事實組 26：24 `CONFIRMED`、2 `CHANGED`、0 `NOT FOUND`；另 1 組示意視覺 `OUT OF SCOPE`。** 第 5 組把三張法院卡的「身分訴訟」收窄為「繼承權官司」；第 23 組在安娜塔西亞肖像卡補上可確認的「1918 年前」，YouTube 說明同時收窄為「可確認的年代及館藏」。兩項事實措辭修正未超過三項，**不需第二輪事實覆核**。另把 `v211`／`v218` 的 claim ID 對齊 c05／c07／c09，為查核索引修正，旁白事實不變。
- **時間與權限：** 片中的 1920、1922、1928、1967、1970、1984、1995、2007、2009 年都指歷史事件或出版日期，沒有宣稱現行法律或存活者。來源在 2026-10-14 重開的讀取狀態如上；第三方掃描、訂閱限制與 PNAS 出版頁 403 應隨製作包保留說明。`sources[].checked_on` 的 2026-10-12 是寫手先前讀取日，本報另記本輪讀回，不冒充各筆都在今日更新欄位。
- **觀點：** `brief.md` 的站主觀點要求法院、安德森檢體及墓地研究各守證據邊界。旁白把「法院未證明她是公主」「安德森兩份檢體不符皇后母系、與毛赫爾母系相符」「兩墓找齊五名子女」分開；未把母系相符寫成唯一姓名識別，也未推測其主觀動機。無觀點衝突。
- **聽稿與揭露：** 現行 104 句沒有超過 40 字、未列入發音表的 Latin 字、括號、URL、`say`，也沒有「經查證／本影片」等查核口吻。`grave-distance` 的 70 公尺與 44 件現依 `j43h`／`v220` 分句揭露；`grave-two-papers` 的 PNAS 字卡先問是否齊全，`ufh6` 下一卡才回答五名子女均找到。公主身分的否定句如今第一次在片尾 `d7um` 說出。
- **音訊修訂前的機械檢查：** `node tools/video/cli.mjs lint --slug curio-h06-v2 --json` 為 0 errors、0 warnings，正文靜態估 502.533 秒（8.376 分）、104 句、1,687 spoken units、七章；同張 `end-outro` 靜態估 7.5 秒。`renderProblems(video.json, root, {workdir})` 與 `cadenceProblems` 為 `[]`；最長畫面 7.8 秒、51 張插圖覆蓋約 52.83%。估時不是合成音檔長度，現行口播與正式語音仍須驗正文至少 8 分鐘及片尾實際畫面停留。
- **曾懷疑而未改：** 判決掃描遮蔽 1920 年救起的確切日子，影片只說月份；[CSUEB 博物館解說](https://www.csueastbay.edu/museum/pre-exhibit/dna/history-fraulein.html)雖記 2 月 17 日，本稿未用日數。PLOS ONE 表格的女兒暫定姓名與俄美形態學意見不同，正文已明說基因結果無法單獨指定第二墓女孩；沒有擅取表格標籤。1995 論文全文及 PNAS 出版頁直接存取受限，已以上述可讀的第一手研究者敘述及原作者摘要作有限查核，不添加未核機率。

## 上一輪三句片尾縮短的增量核對（2026-10-14，歷史紀錄）

原 `d7um`、`934q`、`tstk` 依序縮為「她不是安娜塔西亞。」「證據能證明到哪步？」「訂閱，一起查證。」；line ID、場景、字卡、`claims[]` 和三句預設停頓均未變。第一句仍只排除公主身分：[Stoneking 共同研究者第一手訪談](https://dnalc.cshl.edu/view/15163-Solving-one-of-history-s-mysteries-Mark-Stoneking.html)說兩份互相相符的安德森檢體不符安娜塔西亞已知母系參照；它不宣稱單憑母系序列確證另一個本名。第二句重問證據界線，第三句是訂閱邀請，均不添加可查歷史事實。

縮句前靜態估時約 **9.02 分**，但三句同張片尾卡約 **13.2 秒**，超過 8 秒節奏準則；當輪縮句後同卡估 **7.7 秒**，全片估 **8.93 分**，低於原設定 9 分下限但高於本批 8 分鐘要求，故把 `target_minutes` 從 `[9,11]` 調為 `[8,11]`。當輪 `narrative --slug curio-h06-v2` 讀到舊雜湊 `d41e2ee344214192`；改句者做的 11 題**非盲增量自檢**均答是，答案在外部 `review/narrative-outro-selfcheck.json`，verdict 在外部 `_tools/outro-selfcheck/curio-h06-v2/review/narrative.json`，並未覆蓋舊版獨立盲評。

## 身分揭曉延至片尾的增量核對（2026-10-14，歷史稿）

刪去 `dna-closed-album` 的 `[xdsv]` 與 `end-canal-return` 的 `[56m3]`；前者在實驗室段落先說破公主身分，後者只預告片尾會回答。現行 `[fa8j]` 僅說兩份檢體沒有對上皇后母系，直到 `[d7um]` 才第一次明說「她不是安娜塔西亞」，並回收開場 `[cr5q]`；[Stoneking 第一手訪談](https://dnalc.cshl.edu/view/15163-Solving-one-of-history-s-mysteries-Mark-Stoneking.html)直接支持排除判斷，沒有據此唯一指認另一個本名。`[934q]` 改為「哪份證據最有力？」屬觀眾提問，不增添歷史事實；`[tstk]` 仍是訂閱邀請。

`script --slug curio-h06-v2` 在該輪重生為 89 景、110 句、八章、敘事 hash `58fa44c88676a90a`。當輪靜態估時 **526.133 秒**，片尾 **7.500 秒**；`lint` 0/0、`cadenceProblems=[]`、`renderProblems=[]`，插圖占比 **53.8%**。後來獨立盲評對此 hash 為 6/11，指出開場說法、法院順序、過場及回呼問題；本節數值不是現行稿的關卡結論。

## 七章順序與預告回收的增量核對（2026-10-14，歷史稿）

改稿者依原獨立覆核記錄的[德國法院判決掃描](https://www.prinz.law/static/urteile/pdf/bgh/III_ZR_139-67.pdf)，把 `[dszz]` 改為病院裡「有人」把女子與安娜塔西亞連上，不替兩種姓名起點選邊；`[26m8]` 只交代身分舉證，`[sexv]`／`[wmiq]` 先報一九六七年前審，`[i2rk]` 再報三年後的法律審結果。抽象的 `[mrsj]` 報題句刪去；當輪 `court-two-levels` 的 `[qyt5]` 說最高法院檢查判法有沒有違法，後續因唸讀不順改寫，見下節。法院掃描是第三方保存的原判決，這一輪未冒充另一次獨立逐頁讀回。

按 [Stoneking 第一手訪談](https://dnalc.cshl.edu/view/15163-Solving-one-of-history-s-mysteries-Mark-Stoneking.html)，`[v203]` 只問檢體能否回答身分，正文 `[bp4e]` 點名開頭兩份檢體並新增母系序列相互核對的方法，`[4yw7]` 才報結果。按 [PLOS ONE 2009 原文](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0004838)，`[pxbi]` 僅讓人注意林地碎片，正文 `[v2jq]` 點名開場碎片來自第二墓，`[v219]` 才分清業餘發現與正式進場。`[73wj]` 把第一墓缺口界定為不能替安德森身分下定論，接上 `[bxmt]` 的檢體研究，未聲稱墓地發現必然促成該研究。

`hook-canal-rail` 以匿名、無可辨臉的救援動作對齊「救起」；`dna-two-results` 以頭髮信封、醫院玻片與相同的示意圖案對齊兩檢體相符，圖案不是實際基因數據；林地開場只示意未辨碎片，正文才見第二調查區。短章邊界從八章調為七章，約 55／84／83／60／65／59／117 秒，章名只寫事件或揭曉。

當輪旁白 hash `4357e2c8b1c822eb`，靜態估 **523.4 秒**、89 景、109 句、七章；片尾 **7.5 秒**、最長畫面 **7.6 秒**、插圖占比約 **54.0%**。`lint` 0 errors／0 warnings、`cadenceProblems=[]`、`renderProblems=[]`。本節只是該輪修稿者的來源增量自查，**不是現行稿的獨立事實簽核或敘事盲評**。

## 第三輪盲評後的法院順序與刪景（2026-10-14，歷史稿）

第三輪獨立盲評對舊 `4357e2c8b1c822eb` 為 8/11。本輪用原獨立覆核讀回的[法院判決掃描](https://www.prinz.law/static/urteile/pdf/bgh/III_ZR_139-67.pdf)第 3、7、138–139、143–144 頁與 [PLOS ONE 2009 原文](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0004838) 的既有來源界線作**寫手增量核對**：

| 位置 | 現行改動 | 來源界線 |
| --- | --- | --- |
| `[ykiq]`、`[sexv]`–`[i2rk]` | 開場只說 1970 年最高法院審查前審；正文依 1967 前審未證明、法律審範圍、1970 駁回、裁定界線的順序。 | 不把法律審說成重新辨認全部證人，也不把未證明說成刑事裁罪。 |
| `[3y3m]`、`[5htn]`、`[v211]`、`[sywj]` | 刪三句重述／預告；`[egvx]` 直接給 1928 邀訪，女工全名接在被告提出另一說法 `[xhf4]` 後。 | Xenia Leeds 邀訪、被告提出 Schanzkowska 線索均在原法院與同期資料；法院未裁定女工身分。 |
| `[as2s]`、`[yuvi]`、`[4s6y]` | 刪森林預告和五名子女結果的重述；保留五名子女找齊的首次揭示，接上 DNA 不能判讀安德森主觀相信什麼。 | 母系比對能處理親緣，不能重建其心念；不從未判動機推測詐欺。 |
| `grave-2007-path`、`grave-2007-path-beat-2` | 前景只示意業餘發現者最初注意碎片，後景才畫正式調查的測繪動作。 | PLOS ONE 分述初見與調查；畫面不是實地照片，也不重現可辨遺骸。 |
| 史料照與 `youtube.description` | 現行三張 `photo` 卡；另外兩張候選照的來源／SHA 保留但不說已入片，說明欄同步改三張。 | 五檔候選素材的原件授權判斷保留，影片中的使用數量以 `video.json.scenes` 為準。 |

該輪敘事 hash **`5b07ddebadb37624`**，**85 景、104 句、七章**；靜態 **497.7 秒（8.295 分）**，片尾 **7.5 秒**、最長畫面 **7.8 秒**、插圖占比 **53.3%**。`lint` **0 errors／0 warnings**；`cadenceProblems=[]`、`renderProblems=[]`。這是歷史修稿的增量來源核對，不是後續稿的獨立盲評或原覆核者重簽。

## 卷宗姓名與第一墓的接續修訂（2026-10-14，現行編稿增量）

前一輪 `5b07ddebadb37624` 的獨立盲評指出開場 `[pfpa]` 的「另一個女人」沒有足夠明確地回呼，也指出 `[bnbr]` 到第一墓 `[4uuj]` 像無緣由跳章。現行 `[sywj]` 先問「還記得卷宗裡的名字嗎」，再揭示被告提出的失蹤女工法蘭齊絲卡・尚茨科夫斯卡；女工身分仍不是法院裁定。`[bnbr]` 留下皇室墓地未找到的缺口，`[4uuj]` 接「這個缺口」與七〇年代末第一墓的發現。這只建立觀看順序，沒有聲稱法院訴訟促成尋墓；史實邊界仍分別見[法院判決掃描](https://www.prinz.law/static/urteile/pdf/bgh/III_ZR_139-67.pdf)及 [PLOS ONE 2009 原文](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0004838)。

`[v209]` 現明說舊繼承證書有誤是安德森「主張」，`court-question-certificate` 字卡也寫「她主張舊證書有誤」，沒有把訴求說成法院認定。照片來源簿把五張已核候選與三張現行入片照片分開；兩張未入片的照片不充作成片中的畫面。這些均是修稿者的增量查核，不冒稱原覆核者重新簽核。

視覺修訂前的旁白 hash **`cd0c02e7514e16e0`**，**85 景、104 句、七章**；靜態 **502.533 秒（8.376 分）**，片尾 **7.5 秒**、最長畫面 **7.8 秒**、插圖占比 **53.75%**。`lint` **0 errors／0 warnings**，`cadenceProblems=[]`、`renderProblems=[]`。距 8:00 僅約 **22.5 秒**估時裕度，須以正式音檔時間軸確認正文達標；該輪後來取得獨立盲評 11/11，但目前畫面版的 hash 已改。

## 畫面預檢增量核對（2026-10-14）

本輪未改任何旁白句子、ID、場景順序或章節。`hook-canal-rail`、`hook-canal-rail-beat-2`、`hook-hospital-door` 是同一匿名女子的運河邊與病院情境示意，主體以背面、手部或遠景呈現；沒有資料可以還原實際衣著、救援姿勢或病院內誰先開口，故畫面不作原始照片或檔案影像使用。片頭後 `berlin-name-blank` 原生字卡標明「AI 情境示意，非現場照片」，說明欄也有揭露。`hook-hospital-door-beat-2` 只用兩個影子示意不同的後來說法，不虛構證詞文字。`look.preset` 仍為 `cute-mystery`，明示 `look.style` 只在有人的鏡頭畫 Q 版人物，純物件與地形維持無人的構圖；不改既定色盤。

`court-question-card` 不提前暗示舊證書已有錯誤；下一張 `court-question-certificate` 明確歸為安德森主張。`court-hamburg-corridor-beat-2` 改畫匿名書記整理普通資料，不再呈現法官手中虛構的證人原信。`dna-two-results` 改用原生 `big` 字卡直寫兩份安德森檢體母系序列相符，依 [Stoneking 第一手訪談](https://dnalc.cshl.edu/view/15163-Solving-one-of-history-s-mysteries-Mark-Stoneking.html) 的可見敘述，避免虛構實際基因圖；`dna-maucher-support` 的支系隱喻保留其他母系親屬，界線由鄰近原生 `compare` 字卡說明。`hook-forest-path` 與 `grave-2007-path` 只畫業餘尋找者觀察地面，`grave-2007-path-beat-2` 才畫後續量測；不重現或生成可辨遺骸。三張入片照片仍有 `assets[]` 與原件信用資料，兩張未用候選只留在 [assets-provenance.md](assets-provenance.md) 和外部工作目錄，不進上架圖片來源清單。

當輪 `node tools/video/cli.mjs script --slug curio-h06-v2` 產生敘事 hash `5616d43e89294144`；外部舊 `review/narrative.json` 曾綁定並通過獨立 11/11。當輪格式預檢為 85 景、104 句、51 個 MiniMax `image-01` 鏡頭，估 **502.533 秒**、插圖占比 **52.83%**，`lint` 0 errors／0 warnings，`cadenceProblems=[]`，最長畫面 **7.8 秒**，`renderProblems=[]`；`keyframes --dry-run` 顯示 1K、每鏡最多三輪，當時付費生成 **US$0.00**。這是當時成圖前檢查，不是畫面審片；後續核准與音訊修訂狀態見下節。

## H06 音訊旗標後的編稿增量（2026-10-14）

站主已在後台選大綱 A，`review-pull` 讀回綁 `brief.md` SHA-256 `df25a00988d06e30f2e6a08e84df0eaecacb12ba4c929bb1e4670acea6756b1d` 的核准。初輪 TTS 合成 104 句，舊時間軸量到 8:19；`check-audio` 標記 16 句。重錄其中 8 句後由 H06 專屬 `STOP` 停下，新音檔與舊 `timeline.json` 不符，**現行旁白不算合成完成或核准**。這些外部工作目錄的收據與舊音檔檢查仍保留。

最初修 `[qyt5]`，把不易唸讀的「最高法院檢查前審判法有無違法」改為「安德森提起法律審；最高法院檢查前審判決有沒有法律或程序上的錯。」此句對應 c06 與同場原生比較卡的法律／程序範圍；依[德國法院判決掃描](https://www.prinz.law/static/urteile/pdf/bgh/III_ZR_139-67.pdf)作編稿者的來源增量核對，不將法律審說成重新逐一衡量證人，也不冒稱原獨立覆核者已重新簽核。其後 `[934q]` 把未回答的「哪份證據最有力」改為觀眾留言選項；`[28mj]` 明確回收辨認問題，對應 c04 的接待與身分證明界線；`[sexv]` 換成 1967 年作出判決，避免和前章重複衡量證詞；`[v217]` 只說信封頭髮是第二份檢體，不重述醫院保存切片。後一輪再把 `[rbd5]` 的病院身分難題接上開場、`[v227]` 指向女工線索日後的檢體證據、`[cfvr]` 收窄為已能辨認的男孩，林地碎片的 loop 改為 `v204 → ufh6`；這些增量用 c02–c04、c06、c09–c10、c14–c15 的來源界線檢查，不把女兒的個別姓名說成 DNA 已能分清。

新稿經數輪獨立盲評指出並修正片尾新問句、親友辨認未回收、法院章重述、檢體保存重述與墓中女兒未定名等敘事問題。現行 `349cf912c147f530` 的另一位獨立盲評者只讀 CLI 旁白與 11 題，回覆 11/11 yes；其證據原格式為 `[line_id mm:ss]`，協調者只刪括號內時間以符合 CLI 的 `[line_id]` 驗證語法，未改 yes/no、行 ID 或引文。轉換註記及答案在外部 `review/narrative-answers-20261014-h06-lineids.*`；`review/narrative.json` 記錄 round 10、`passed=true`、`narrative_hash=349cf912c147f530`、`script_hash=d5ca610b92e9c97286ff61153f5f7559dfc86d5375fefe039cf1f9b1f257afec`。前一次沒有行 ID 的答案被 CLI 判為格式失敗，並非當輪內容盲審判否；後續有效收據已覆蓋。

現行 `video.json` SHA-256：`a6a8c3be0cccaf7856c0c1640a2dd8fed8191254166dfe4684c7a20c1c9d98df`；`script.md` SHA-256：`87f3d96bd0022b57f98ba53f8a8b546c5a63ea1a794a3809e910308a193014b6`；`claims.md` SHA-256：`23ae37ee83b57c21b85ced05fe964b12ea7a3d2f150ea8fd83500dc04d57d4a0`；核准大綱 `brief.md` SHA-256 仍為 `df25a00988d06e30f2e6a08e84df0eaecacb12ba4c929bb1e4670acea6756b1d`。現行 85 景、104 句、七章，`lint` 0 errors／0 warnings，靜態估約 8.4 分；實際旁白時間軸尚未重建，8 分鐘門檻須再依正式音檔核對。首輪 TTS 104 句合成後有 16 個檢查旗標，重錄前 8 句後 H06 專屬 `STOP` 生效；`timeline.json` 與現行稿及部分 take 不符，無旁白核准，亦無 H06 付費圖片或成片。
