# H06 v2｜來源重開與查核筆記

**2026-10-14 圖卡更新：**下段的「現行」敘事 hash、影片 SHA 與 51 鏡描述是原生圖卡修訂前的歷史快照。c02 來源界線與 104 句口播未變；開場兩鏡已改 `diagram`，新的 `narrative_hash=a8b72a5524beace9` 已獨立盲評 11/11 通過，正式時間軸重建為 `829335243ac71490e3ba552ea18a2c1f949c47a06362aee3979cbf6005d170d2`，後台音訊審核待站主核准。精確收據見 [運河圖卡交接](native-canal-cards-20261014.md)。

狀態：2026-10-14 離線重製稿的來源查核筆記。這份筆記記錄實際重開的材料、可支持的敘述與無法直接檢視的部分；BGH 原判決掃描、PLOS ONE 原文及 Stoneking 第一手訪談另作增量來源抽查。**現行**敘事 hash `02a39e4e1fb460a7` 已獨立盲評 **11/11 PASS**；104 句配音的新版時間軸 SHA-256 `a885d5871108adaeacf346ccefa8d30a15556dda9623b5fa9fc5d9cf792f8e84` 已由站主在 `/admin/videos` 核准，`review-pull` 與 `status` 讀回 `[x] narration approved`。音訊檢查保留 8 句轉錄旗標，由站主聽審接受；這不是全部畫面欄位的逐項雙人查核、站主審片或成片核准。下文保留先前 hash 與舊版待審紀錄作歷史快照。三鏡付費小樣有兩張運河鏡頭退回、一張病院插畫通過，尚無全片分鏡或成片。圖像收據見 [visual-pilot-01.md](visual-pilot-01.md)；`video.json` 的 `claims` 代號對照 [claims.md](claims.md)。

## 本次直接重開的原件

| 來源 | 直接可見的部分 | 用途與限制 |
| --- | --- | --- |
| [Coble 等，PLOS ONE 2009 原論文](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0004838) | 摘要、導論、方法與討論。導論記載地質學家 Avdonin 於七〇年代末找到第一墓，與少數友人保密至 1991 年；第一墓含夫婦、三女兒及四名隨行人員。2007 年第二墓距第一墓約 70 公尺，官方整理出 44 件骨與牙碎片。 | 支持 c01、c11–c14、c18；發現、官方發掘與發表年份必須分開。該篇 DNA 不能單獨替第二墓的女兒指定瑪麗亞或安娜塔西亞。 |
| [Stoneking 第一手訪談，Cold Spring Harbor DNA Learning Center](https://dnalc.cshl.edu/view/15163-Solving-one-of-history-s-mysteries-Mark-Stoneking.html) | 研究者說明頭髮與醫院保存組織由獨立團隊分析，兩份安德森檢體相符，但不符安娜塔西亞的已知母系參照。 | 支持 c09 的樣本鏈與排除結論；訪談不是 1995 年論文全文。 |
| [DNA Learning Center 教師指南原件](https://www.dnai.org/romanovs/romanov_guide.pdf)與[同機構工作簿](https://dnalc.cshl.edu/assets/files/dnalc-live/17207.the_mystery_of_anastsia_workbook.pdf) | 教師指南 PDF 第 25 頁的答案記載安德森與 Carl Maucher 有母系關係；工作簿 PDF 第 11 頁標示 Maucher 是 Franziska Schanzkowska 的母系姪孫。 | 支持 c19 的陽性母系線索及親屬關係；這是研究機構的教學材料，不冒充 Nature Genetics 原論文。 |
| [美國 NIJ 法醫 DNA 教材](https://nij.ojp.gov/nij-hosted-online-training-courses/principles-forensic-dna-officers-court/08-mitochondrial-dna-y-str-analysis/introduction-mtdna/maternal-inheritance-0) | 明確說明母系親屬可有相同 mtDNA，不能用 mtDNA 唯一識別個體。 | 支持 c20；片中因此說「支持她可能是失蹤女工」，不說「這項比對獨自證明本名」。 |

## 直接存取受限的原件

- [Stoneking 等，Nature Genetics 1995](https://www.nature.com/articles/ng0195-9)與[PubMed 書目](https://pubmed.ncbi.nlm.nih.gov/7704032/)可核作者、1995 年 1 月刊期及 DOI；出版社正文需要訂閱。本稿沒有把從機構教學原件及研究者訪談取得的結論偽稱為已逐字讀過該論文。
- [Rogaev 等，PNAS 2009](https://www.pnas.org/doi/10.1073/pnas.0811190106)及[PubMed 摘要](https://pubmed.ncbi.nlm.nih.gov/19251637/)支持兩墓找齊五名子女的結論；本次網頁直接取用時，PMC 鏡像顯示機器人驗證。舊版第二輪曾讀 PNAS 原文，本版仍需另人複核敘述。PLOS ONE 2009 原文的討論也明說羅曼諾夫家族無一人從 1918 年處決中生還。
- [德國聯邦最高法院 III ZR 139/67 判決的第三方掃描](https://www.prinz.law/static/urteile/pdf/bgh/III_ZR_139-67.pdf)由舊版 `verify-2.md` 逐頁目視檢查；本版亦重開掃描並目視核對 PDF 第 3、5–8、13–15、138–139、143–144 頁，詳見 [verify-1.md](verify-1.md)。這是第三方保存的原判決掃描，未將 OCR 視為官方逐字稿。民事法律審的裁定界線與 1995 年科學結論分開說。

## 本版改稿所需的界線

- `[v205]` 與 `[v206]` 的 1921 年報紙段已刪除；現在由 1920 年運河、1922 年病院訪客順序敘述，不再讓時間倒退。
- `[sywj]` 說出被告提出的失蹤女工姓名；`[v223]` 才給毛赫爾母系相符的結果。`[v225]`–`[v226]` 立刻解釋此比對不能唯一指名。
- `[v228]`–`[zwkk]` 先交代俄、美人類學者對缺哪名女兒的分歧，再用 PLOS ONE 的基因結果說明它不能單獨替第二墓女兒指定姓名。
- `[dszz]` 只說一九二二年病院裡有人把她和安娜塔西亞連在一起，不指稱訪客是第一位提出者；法院掃描保留兩種說法。正文法院段依一九六七年前審、一九七〇年法律審推進，`[mrsj]` 的抽象報題句已刪。
- `[v203]` 在開場只問兩份檢體能否說出身分，`[bp4e]` 先交代母系序列比較方法，`[4yw7]` 才揭兩份檢體彼此相符；`[pxbi]` 只讓人發現林地碎片，`[v2jq]` 才點名第二墓。`[73wj]` 指出第一墓缺口不能定安德森身分，接上其後檢體研究。
- `[d7um]` 才第一次直說開場 `[cr5q]` 的身分答案：運河邊女子不是安娜塔西亞。舊 `[xdsv]` 的提前明示與 `[56m3]` 的純預告已刪；法院未裁定女工身分，母系證據提供了支持女工說法的陽性線索；她的主觀想法沒有從這些材料得到答案。
- 片中插圖屬情境示意；資料卡上的法律、DNA 與墓地結論則以所引來源為準。現行入片三張史料照；另外兩張是尚未入片的候選素材。五檔均在外部 v2 工作目錄的 `stock/<sha256>.jpg`，來源、授權與校驗見 [assets-provenance.md](assets-provenance.md)。沒有使用或生成可冒充真實法庭、檢體或遺骸的照片。

## 尚待關卡

旁白盲評曾於舊敘事雜湊 `3dfdec113ca9958c` 達 11/11。三句片尾縮短的中間稿 `d41e2ee344214192` 有 11 題非盲增量自檢；刪兩景後的 `58fa44c88676a90a` 獨立盲評只通過 6/11，指出病院說法過早定因、法院年份倒序、報題句、墓地與檢體斷線、開場預告在正文重講。`4357e2c8b1c822eb` 的第三輪獨立盲評為 8/11，`5b07ddebadb37624` 的下一輪仍因章節跳接與人名回呼未過。視覺修改前的敘事雜湊 `cd0c02e7514e16e0` 曾由新盲評者通過 11/11；音訊修訂前的畫面版 `5616d43e89294144` 亦獲獨立 11/11，外部舊 `review/narrative.json` 當時只綁該 hash。其後兩份獨立盲評各得 10/11：`0073b9aa00f1c79a` 指出片尾提出新問題卻未回答；`df71f4756cfa1883` 指出病院「還能靠什麼辨認她」未在親友章明確回收。後續盲評又指出 03:35 章首重述證詞衡量、05:19 重述保存切片、07:24 問出無法確認的女兒個別姓名，以及 00:55 章首未接前一問；編稿增量修正後，**節奏修訂前 `349cf912c147f530` 獨立 11/11 PASS** 並已綁定外部 `review/narrative.json`。原版已有獨立逐句事實覆核 `verify-1.md`；BGH、PLOS ONE、Stoneking 增量來源抽查不冒稱全部主張與畫面重新逐欄核准。站主已選 A，大綱核准綁 `brief.md`。初次 TTS 與 16 句旗標、重錄 8 句、曾有 H06 專屬 `STOP`，皆為歷史狀態；現行配音與核准有效性見文末。首輪三鏡小樣兩張退回、一張病院候選保留；第二輪運河全景雖獲 judge PASS，人工仍因來源界線退回。現行兩鏡新提示只通過 dry-run，尚無成片檢查及站主驗收。

現行三張入片歷史照片的字幕標示可確認年代與館藏；安娜塔西亞照片只有「1918 年前」的來源界線，不虛填單一年份。另兩張候選照保留外部原圖與來源簿記錄，未列入現稿 `assets[]`。法院資料卡以「繼承權官司」稱呼民事請求，公主身分是請求成立的前提。第二墓距離卡讓 70 公尺與 44 件各在對應口播時出現；兩篇論文對照卡先顯示「是否齊全」的問題，五名子女找齊的答案到下一張卡才出現。圖像小樣第二輪和實際音訊時間軸的節奏檢查另見文末及 [visual-pilot-01.md](visual-pilot-01.md)。

## 視覺小樣前的來源與畫面修訂（2026-10-14，當輪預檢快照）

- 開場前三個 MiniMax 鏡頭連續呈現運河邊匿名女子、同一衣袖與扶欄動作、兩年後病院內的匿名女子。提示詞只指定當時可接受的普通環境與背影，不重建安德森臉部、具體救援者或誰先說出公主姓名。第一張原生字卡 `berlin-name-blank` 明標「開場插圖為 AI 情境示意，非現場照片」；這是畫面揭露，不代表已生成或已審看片段。當輪 `look.preset` 為 `cute-mystery`，`look.style` 曾指定人物為 Q 版；後來的成人比例修訂見文末。
- `court-question-card` 只列安德森的給付及繼承身分請求；「舊證書有誤」延至下一張 `court-question-certificate`，並以「她主張」歸屬當事人。`court-hamburg-corridor-beat-2` 只畫匿名文書整理的普通動作，不畫法官手中的虛構證人信。`dna-two-results` 由插圖改成原生字卡，直接顯示頭髮與保存組織的母系序列相符，避免讓虛構點陣看似原始基因資料；皇后與毛赫爾的比對結果仍各由後續原生字卡呈現。`dna-maucher-support` 的支系隱喻保留多名母系親屬，不暗示單一身分識別。
- 二〇〇七年開場及正文尋找鏡頭只顯示匿名搜尋與後續量測，不畫遺骸、骨牙碎片特寫或可冒充真實墓地的「發現照」。五張已核照片的外部原圖與來源簿保留；只有三張實際使用者列入 `assets[]`，上架來源不會誤列另兩張候選。
- 只更動鏡頭提示詞、原生字卡文案、一景 `shot`→`big` 的版型與 `assets[]`。場景與旁白 ID、順序、口播文字、章節未更動。更新的稿子敘事 hash `5616d43e89294144` 已通過獨立 11/11，靜態估 **502.533 秒**、**85 景、104 句、51 張插圖**。`lint` 0 errors／0 warnings、`cadenceProblems=[]`、最長畫面 **7.8 秒**、插圖覆蓋約 **52.83%**、`renderProblems=[]`；`keyframes --dry-run` 確認 MiniMax `image-01` 1K、51 個鏡頭、一輪約 US$0.69、三輪上限約 US$2.07、目前 US$0.00。所有時間與畫面占比是合成前預估，正式 TTS 與實圖審查後需再量；大綱選項核准前不進付費製作。

`renderProblems` 使用本版外部 `stock/` 工作目錄預檢為空。縮短三句片尾前，`lint` 曾估 9.02 分、片尾單張卡約 13.2 秒，造成節奏警告；`target_minutes` 因本批八分鐘以上規格改為 `[8,11]`。視覺修訂前的 `cd0c02e7514e16e0` 稿保留三句、原 line ID、預設停頓與同一張收束卡；又刪除空泛過場、重排法院審理、把兩張未用照片撤出場景，並修好卷宗姓名與第一墓的章節接續。當輪 `lint` 為 0 errors、0 warnings，估 **8.376 分、85 景、104 句**，片尾單張卡估 **7.5 秒**；`cadenceProblems=[]`、最長畫面 **7.8 秒**、插圖覆蓋約 **53.75%**。此估時只高於八分鐘約 22.5 秒，正式合成音檔須實測正文至少 8:00 及片尾實際畫面停留。格式預檢不代表史實、成片或站主核准。

**2026-10-14 大綱快照補註（當時狀態）：** [brief.md](brief.md) 第 62 行把五張候選照的來源簿與 `assets[]` 並列，現行 `video.json.assets[]` 實際僅有三張入片照；另外兩張只保留在 [assets-provenance.md](assets-provenance.md) 與 v2 外部 `stock/`。brief 第 68 行仍以未來式安排獨立盲評；當時敘事 hash `5616d43e89294144` 已獨立通過 11/11，BGH、PLOS ONE 與 Stoneking 有增量來源抽查，但沒有宣稱現行全部欄位逐項重審。其後站主已選 A、合成初輪 TTS；大綱核准仍綁未改動的 brief，敘事盲審與音訊核准的最新有效性以文末更新為準。

## 音訊旗標後的法律審口播修訂（2026-10-14）

`[qyt5]` 舊句「最高法院檢查前審判法有無違法」唸讀不順，轉錄也聽成「前審判決有無違法」；現改為「安德森提起法律審；最高法院檢查前審判決有沒有法律或程序上的錯。」此句由 [BGH 原判決掃描](https://www.prinz.law/static/urteile/pdf/bgh/III_ZR_139-67.pdf)與 [claims.md](claims.md) c06 承接：法律審檢查法律與程序上的瑕疵，不重新逐一評證。`[934q]` 改為觀眾留言選項，避免舊版片尾提出「哪份證據最有力」卻未回答，也不替證據作虛假的效力排名。`[28mj]` 現直接回呼「怎麼辨認她」，明說親友可以作證但接待不能證明身分，對應 c04；`[sexv]` 明說前審作出判決，不重述前章證詞衡量；`[v217]` 只補信封頭髮是第二份檢體，不重複醫院保存切片。`[rbd5]` 把病院本名難核對接到開場公主疑問，`[v227]` 指向女工線索日後的檢體證據，`[cfvr]` 只問能辨認的男孩；林地 loop 改 `v204 → ufh6`，不謊稱基因分清第二墓女兒個別姓名。這些是編稿者依 c02–c04、c06、c09–c10、c14–c15 做的增量來源核對，不冒稱原獨立事實覆核者重新簽核。

節奏修訂前稿 `script.md` 已重生，85 景、104 句、七章，`lint` 0 errors／0 warnings，靜態估約 8.4 分。獨立盲審 11/11 PASS 綁 `narrative_hash=349cf912c147f530`；外部 `review/narrative.json` 記錄 round 10、`passed=true` 及 `script_hash=d5ca610b92e9c97286ff61153f5f7559dfc86d5375fefe039cf1f9b1f257afec`。盲審引用原句時寫 `[line_id mm:ss]`，協調者只刪括號內時間以符合 CLI `[line_id]` 語法，沒有改判斷或引文；原答、轉換及註記均保留在外部 `review/`。先前無 ID 的格式失敗收據已由現行有效收據覆蓋。初輪 `timeline.json`、首輪 `review/check.json` 與初輪 8:19 是歷史狀態；站主解除 H06 `STOP` 後，現行配音已重建，詳見下節。

本地、唯讀的 Whisper medium 曾完成初輪 16／16 個音訊旗標的第二意見，原逐句輸出與分類留在外部 `review/whisper-medium-flags-20261014.*`。`sexv`、`qyt5` 因稿面改動已依新稿重合成；`sywj`、`pgcg` 的「尚茨科夫斯卡」結尾在兩個轉錄器皆呈「斯基」，`2pva`、`xx8w` 仍有辨音疑點。其餘句的第二意見支持原音或顯示近音轉字差異，保留快取 take，不作無差別重錄。這些轉錄差異與人耳核准分開記錄。

## 配音、旗標與節奏修訂前站主核准（2026-10-14）

H06 專屬 `STOP` 由站主手動解除後，現行 104 句 TTS 重用 90 句快取、合成 9 句，新增 177 billable chars。`timeline.json` 為 15,028 幀／30 fps，即 **500.933 秒（8:20.93）**；`narration.wav` SHA-256 `528671067cbc165ca7d0ac32b487311dc147dc89a98eafe62515072cad57db0a`。正式 `check-audio` 覆蓋 104/104 句；13 句初始旗標用逐檔 WAV SHA 對上原始 Whisper medium 轉錄後，清除 5 句，餘 8 句記於 `review/check-flags.json`（`speech_hash=9ae95e3507d3809f`；`review/check.json` SHA-256 `21e676ca2624dc6ad553b6b6bacb2b1e096ec0e8e79b62884ac450031a7fed7d`）。原始轉錄、SHA 映射與差異收據保留在外部 `review/whisper-medium-*-20261014.*`。時間碼按 `timeline.json` 的起始幀計算。

| 起始 | 句 ID | 原稿 | 轉錄旗標原因 |
| --- | --- | --- | --- |
| 00:38.73 | `pxbi` | 二〇〇七年，俄國林地有人注意到地上的碎片。 | Gemini 聽成「俄國領地」；Whisper 聽成「惡果林地」，需確認近音。 |
| 03:18.03 | `sywj` | 還記得卷宗裡的名字嗎？失蹤女工法蘭齊絲卡・尚茨科夫斯卡。 | 兩轉錄器把「失蹤女工」記成近音錯字，姓氏尾音「斯卡」記成「斯基」，需聽稱謂與人名。 |
| 03:35.17 | `sexv` | 一九六七年，前審法官終於作出判決。 | 兩轉錄器把「前審」記成「前身」，近音待辨。 |
| 04:01.63 | `i2rk` | 一九七〇年，最高法院駁回她的法律審。 | 兩轉錄器把「她」記成「他」；Gemini 另多「了」。 |
| 04:49.00 | `2pva` | 研究辨出尼古拉二世夫婦和三名女兒。 | Whisper 把「尼古拉」記成「尼古勞」，需聽人名；Gemini 開頭誤記。 |
| 05:31.90 | `xx8w` | 這種遺傳特徵，會沿母親那一邊傳下去。 | 兩轉錄器都略去「一」，需確認是否漏唸。 |
| 06:04.27 | `pgcg` | 提供者卡爾・毛赫爾，是尚茨科夫斯卡的母系親屬。 | 兩轉錄器把姓氏尾音「斯卡」記成「斯基」，需聽人名。 |
| 07:11.90 | `h9hy` | 男孩的父系資料，補上第三道比對。 | 兩轉錄器把「父系」記成「複習」；Gemini 另錯記「第三個筆袋」，Whisper 保留「第三道比對」。 |

站主曾於 `/admin/videos` 審聽並核准節奏修訂前的音訊時間軸；`review-pull --gate audio` 讀回 `approved_at=2026-10-14T00:27:28.634Z`，綁 `timeline.json` SHA-256 `500df86851e4891f6707882dc28a16bf43900179abe6924c6a06a566a5948747`。審核預覽位於外部工作目錄 `review/narration-528671067cbc165c.m4a`，並提交至後台 [影片審核頁](https://mokaair.com/zh-TW/admin/videos)。八句旗標作為轉錄追溯記錄保留；音訊核准不表示轉錄器逐字一致。後續圖像、成片及上架各有獨立關卡。

## H06 開場圖像小樣提示修訂（2026-10-14）

為避免成人被畫成兒童，首輪付費小樣的 `video.json` 保留 `cute-mystery` 色盤、紙張、深色描線與平面賽璐璐陰影，將 `look.style` 的 Q 版頭身及大眼改為明確成人自然比例；全域 `look.negative` 排除成人兒童比例、照片或 3D 質感、浮水印與上下黑邊。開場三鏡分別指定完整成人背影、單隻裁到前臂的成人手、病院門內無可辨臉的成人背影，沒有加入可冒充來源事實的救援者或說出名字的訪客。旁白 ID、文字、順序與 `timeline.json` 均未更動。首輪結果、原圖 SHA 和後續兩鏡提示修訂見 [visual-pilot-01.md](visual-pilot-01.md)。

第二輪只重試第一張運河全景，裁切圖 SHA-256 `f7ca62fa0e45afefd19fcbd355e5a573a83b9ef9f820610595717b4bca26cf11`、judge 9.29 PASS；人工仍因可見女子側臉及未獲 c02 支持的救援前站立姿態退回。外部逐檔核對收據在 `review/visual-pilot-20261014-canal-retry/`，累計圖像與 judge 花費 US$0.0540。當輪開場提示來源 `video.json` SHA-256 `9a0c81de5dda856974db9779832b12f9e8b6a393a1140ea935bed8b445cec315` 改為第一鏡無人運河空景、第二鏡無人欄杆與明示為圖像疊層的留白卡；病院候選 SHA-256 `17e388e0807ee107220a11ad1a1e70e4a7a9ec496aba60ef94dfa9d69d6c33f9` 保留。兩鏡 dry-run 及 lint 0/0 通過，**尚未按開場新提示買圖**；當輪敘事 hash `349cf912c147f530` 與當時已核准的音訊時間軸均未改。後續只調畫面卡節奏，見下節。

節奏修訂前，按正式 `timeline.json` 的 15,028 幀／30 fps 重量，`shot` 畫面 7,853 幀，占 **52.256%**。但 `cadenceProblems` 報 `grave-first-count` 第一狀態 8.2 秒及 `end-outro` 單一狀態 9.0 秒，超過插圖說書每個畫面狀態最多 8 秒的規格。早先的 7.8 秒是 TTS 前靜態估時，不能代替本次結果；成片前須修好、重檢。片尾若改分景或版型會使敘事 hash 變動，必須新一輪獨立敘事盲評。當時只檢查而未改原時間軸，故原音訊核准仍在；下節實際修訂後，以新核准狀態為準。

## 真實時間軸畫面節奏修訂（2026-10-14，當輪快照）

保持原 **85 景、104 句**的場景 ID、句 ID、口播文字、句序及音訊分組。`grave-first-count` 在 `[v215]`「九具遺骸／四名隨行人員」時揭露第四張數字卡；其餘三張依 `[yqep]` 1991 年正式發掘、`[2pva]` 三名女兒、`[s4mq]` 尚缺兩名孩子逐張顯示。[PLOS ONE 原論文](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0004838)摘要與導論明列第一墓九具、四名隨行人員及父母與三名女兒。`end-outro` 保留原場景 ID 和三句口播，從無法揭露的 `outro` 版型改成雙欄 `compare`：第一句先顯示「檢體：她不是安娜塔西亞；母系線索不能唯一確認本名」，第二句 `[934q]` 才揭露「判決：公主身分未獲證明」，底部保留「訂閱奇聞檔案局，一起查證」。兩欄分別對應 c09／c20 與 c06，沒有把法律審說成 DNA 鑑定。

當輪 `video.json` SHA-256 `47ee9a64126003aa2076bbb12d12434f4bbaa71bc3f1ca53781245bd069c2f69`，`visual_hash=ceb1cb5bcb84aad2`，`pictures_hash=046720f1333f63b4`；`script.md` SHA-256 `87b6a30a01801a233bdbd7619af081fb523c60e8d7e86cb52eec653c14d33b54`、`narrative_hash=02a39e4e1fb460a7`。先前 `349cf912c147f530` 的獨立 11/11 **不能移作新稿核准**；本 hash 後續已重新獨立盲評通過，收據見本頁最後一節。開場兩鏡提示與病院候選未因本節修訂而改動；當輪兩鏡新提示只通過 dry-run，無新付費圖像。

TTS 先 dry-run 確認 99 個請求全命中快取、0 字需合成，再正式重建時間軸：**0 新請求／0 billable characters**。新 `timeline.json` SHA-256 `a885d5871108adaeacf346ccefa8d30a15556dda9623b5fa9fc5d9cf792f8e84`，舊檔 SHA-256 `500df86851e4891f6707882dc28a16bf43900179abe6924c6a06a566a5948747` 已連同原 `approvals.json` 逐檔保存於外部 `review/cadence-before-20261014/`。新舊 `timeline.lines[]` **104/104 筆 JSON 等值**，含每句起訖幀、`audio_samples`、`audio_sha256`；逐句 `line ID audio_sha256` 清單另存 `review/cadence-line-audio-sha-20261014.txt`，該檔 SHA-256 `6d061861f0700c5342ab5d1c1bc3039bda53ae9be1483f4ff9e626ce2abcb6ff`。`audio_evidence`、總長 15,028 幀及 `speech_hash=9ae95e3507d3809f` 亦完全相同。`narration.wav` SHA-256 仍為 `528671067cbc165ca7d0ac32b487311dc147dc89a98eafe62515072cad57db0a`。變動的是畫面版型與 reveal 狀態，故檔案層級的 `timeline.json` SHA 改變。

依**新正式時間軸**重測，`cadenceProblems=[]`：101 個畫面狀態、平均 5.0 秒、最長 **8.0 秒**；第一墓四段為 3.9／4.3／5.2／4.3 秒，結尾兩段為 3.0／6.0 秒。`shot` 仍占 7,853／15,028 幀，即 **52.256%**；`lint` 0 errors／0 warnings。用本機 Chromium 只渲染兩景的五個代表狀態到外部 `review/cadence-card-preview-20261014/`，版面檢查 0 問題、人工看過完整四卡及結尾前後狀態，逐項出現且文字未溢出。這是局部靜圖預檢，尚非成片播放與 QA。

**當輪核准狀態：**站主原音訊聽審綁舊 `timeline.json` SHA；即使 104 句原 WAV 和 `narration.wav` 均未變，`approvalState(audio)` 對新檔當時回報 **stale**。新敘事 hash 當時也須獨立盲評；兩項後續結果見下節。此處不把舊核准或原 11/11 冒稱有效；後續圖像批量、渲染、成片與上架仍各有關卡。

## 新時間軸關卡讀回（2026-10-14）

站主在後台核准 H05、H06 的新版旁白時間軸後，對 `curio-h06-v2` 重新執行 `review-pull --gate audio`，回報 `audio: approval recorded`；緊接的 `status` 顯示 `[x] narration approved`。後台影片清單亦顯示 H06-v2「沒有待決定」。這筆核准只適用本節上方 `a885d587...` 的時間軸，並不代表關鍵影格或成片已核准。

未讀先前判詞的獨立審稿者對 `narrative_hash=02a39e4e1fb460a7` 重新答十一題，10 項必答及 1 項參考題均為 `yes`，`script_hash=548038290136685be6dd21ee4a74ad0fd6ea464f66623ac912ea0add1e9571ca`。首輪答案因引文缺句 ID 而被格式檢查拒收；補上句 ID 的第二輪通過。原答及隔離收據保留在工作目錄外，通過版再用 `node tools/video/cli.mjs narrative --slug curio-h06-v2 --answers <file>` 記入本片工作目錄；`status` 已讀回 `storytelling panel: passed`。審稿者另提醒法院、實驗室與墓地鏡頭須明顯呈現為示意重建，歷史照片的實際檔案及權利仍待成片前核對。

## MiniMax 提示詞離線修訂（2026-10-14，現行）

站主選擇維持 MiniMax、暫只做離線規劃。51 個 `shot` 的 ID、類型、時窗與全部 104 句旁白未動；`look.negative` 清空，部分鏡頭改用可見的 2D 色塊、墨線、概念圖和匿名場景描述，避免重複前幾輪照片質感、虛構人物與假文字。現行 `video.json` SHA-256 `52e29bceaa443ce740ba0db5ff9eb64cca27613340828f813c56dcee00d2607a`、`look_hash=d57461da98a0ba9b`、`pictures_hash=09fd4baed7f1480e`；敘事 hash `02a39e4e1fb460a7`、speech hash `9ae95e3507d3809f`、正式時間軸 SHA-256 `a885d5871108adaeacf346ccefa8d30a15556dda9623b5fa9fc5d9cf792f8e84` 均未變。`lint` 0 errors／0 warnings，51 鏡 `keyframes --dry-run` 全過；沒有新生圖、判圖或費用。舊運河圖和現有縮圖來源仍為退件，舊 look 的病院圖只能作歷史候選。逐鏡風險與後續小樣條件見 [離線視覺規劃](offline-visual-route-20261014.md)；這不是已核准全片分鏡或成片。

## 後續一張 MiniMax 小樣（同日增補）

上述「沒有新生圖」只描述離線修訂當輪。站主之後另准一張 `hook-canal-rail` 小樣；現行 look/pictures hash 下，MiniMax 生成圖像卻把運河概念畫成山灣，底部有虛構小字。judge `subject=0`、`passed=false`，人工亦退件；裁切圖 SHA-256 `3b50bc6fbcec7253873d02e44c774d96a3ad71814fa6493f6c42d2a5390e4188`，manifest SHA-256 `a9b9a08abb9153b0487c3db1f67a8131cc08f957f94fe78f8195459060c614c0`。不得進片或作縮圖，不再就同提示付費重試。完整收據與 50% 插圖占比下的替代方案分別見 [visual-pilot-01.md](visual-pilot-01.md) 第四輪、[offline-visual-route-20261014.md](offline-visual-route-20261014.md)〈退件後的離線替代方案〉。旁白與敘事核准綁定仍是上段 hash；分鏡與成片未完成。
