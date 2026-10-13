# H06 聽眾審稿修正與二次查核交接

日期：2026-10-12。依大綱 A，只修改繁中腳本、場景字卡與來源說明；未合成旁白、未生成圖片或媒體。原有 106 場、137 個句 ID 均保留，未重新編號。修改後先跑 `node tools/video/cli.mjs lint --slug curio-h06`；**實際音訊時長仍待 TTS 後檢查**。

| 問題 | 修正位置 | 本輪做法與需要核對的依據 |
| --- | --- | --- |
| 訴請過於抽象 | `court-question-card` `fba5`、`court-read-three-places` `kvx5/7m6v/z5pb`、`court-proof-steps` `8d33/ftkk/qcgw` | 把三項請求分清：給付款項、以公主身分主張德國境內相關遺產繼承權、既有繼承證書有誤；再說為何必須舉證公主身分。依[第三方保存的原判決掃描](https://www.prinz.law/static/urteile/pdf/bgh/III_ZR_139-67.pdf) PDF 第 13 頁（紙本第 12 頁）的訴請；第 3 頁是主文。金額、起訴年份均不口播。 |
| 四輪同義重述 | `court-read-three-places`、`court-proof-steps`、`court-two-years`、`court-two-levels`、`court-judges-bench`、`court-folder-return` | 保留場景與句 ID，但改成不同的閱讀步驟：先找訴請，接著認識民事舉證，再看 1967／1970 兩層結果，最後翻到另一位女工段落。`9vfb` 改講主文與理由的讀法，`sywj` 改作後段轉場，不再各自重複「前審不利、法律審維持」。 |
| 法律審第一次聽不懂 | `court-two-years` `i2rk`、`court-two-levels` `mrsj/qyt5` 與比較卡 | 首次說「法律審」時，直接補「查前審有沒有法律或程序錯誤」；下一張卡分開前審衡量證據和最高法院檢查判法／程序。依原判決 PDF 第 3 頁主文、第 143–144 頁結論及其對 Revision 異議的處理；第二輪獨立查核已確認這個白話化範圍。 |
| 墓地女孩名字講三次 | `grave-sisters-frames` `8e4x`、`grave-no-reference` `vrpx`、`grave-which-sister` `ce8r/zwkk`、`grave-label-vs-proof` `kgvp` | 前兩鏡只示範「先看家族關係、再找討論段落」，唯一具體界線留在 PLOS ONE 比較卡 `zwkk`：「分不出瑪麗亞還是安娜塔西亞」。後面 `kgvp` 只教讀圖與正文對照，不重唸界線。依 [PLOS ONE 原文](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0004838) Discussion。 |
| 五名孩子等於各自姓名確定 | `grave-two-papers`、`grave-five-children` `ufh6` | 卡片先顯示兩篇 2009 年研究都談第二墓，但各答不同問題；結論改說「兩座墓合在一起，五名子女都找到了」，不替第二墓女孩指定名字。依 [PNAS 原文](https://www.pnas.org/doi/10.1073/pnas.0811190106) 與上述 PLOS 限制一併閱讀。 |
| 畫面和旁白不對位 | `hook-hospital-door`、`hospital-two-folders`、`court-judges-bench`、`court-folder-return`、`dna-file-two-paths`、`grave-sisters-frames`、`grave-no-reference`、`grave-label-vs-proof` | 運河獲救配運河岸；兩種說法配兩份**無可讀文字的示意**檔案；主文／理由配判決冊；法院與基因配左右不同物件；家族關係與研究討論配各自的示意畫面。安德森只呈背影，AI 畫面不可冒充原件。 |
| 1995 年論文取得界線 | `dna-book-page` `fmii`、`dna-source-levels` `rap7/k8xz` 及字卡、`youtube.description` | 旁白明說「論文全文要付費，我們沒有讀到」；出版頁只核日期／作者，樣本與結果改引[共同作者 Stoneking 的第一手訪談](https://dnalc.cshl.edu/view/15163-Solving-one-of-history-s-mysteries-Mark-Stoneking.html)。不把訪談稱為 Nature Genetics 正文。 |
| 口語與收尾 | `rbd5/smmb/28mj/2pva/pgcg`、`end-outro` `934q` | 早一章介紹安娜・安德森的名字；改掉抽象書面語；結尾具體問法院是否判她是女工，同時維持三句、單卡不逾時。 |

`video.json` 的判決來源清單優先列可讀的掃描，法院字卡標「判決掃描」；`claims.md` 的 c05/c06 與 `research.md` 的 S1 同步列 PDF 頁碼。原始掃描由第三方保存，並非 BGH 官網。REWIS 全頁本輪仍 403，不把搜尋索引當親讀全文。正文沒有安德森的心理動機、新個人身分鑑定或 1995 年付費原文的未核細節。

交接：請另一代理針對 c05 訴請、c06 法律審白話化及 c14／c15「家族完整 vs 姊妹個別墓位」做 **targeted independent fact recheck**；通過後才進聽音與媒體階段。
