# C20 Zippo｜Treatment 獨立一手來源審查

審查日期：2026-10-23（台北時間）。本收據只審作者草稿的企劃事實，不是逐字稿核准、站主採用、保固法律意見或製作許可。審查者在獨立工作樹讀取原件；沒有編輯作者的 Treatment 或 source matrix。

## 固定受審版本

| 對象 | 固定值 |
| --- | --- |
| 作者 PR | [#1708](https://github.com/x812033727/travel_scanner/pull/1708)，草稿；head `b83a45fac8a97752aa3f96be46e64a4ba4968728` |
| `treatment.md` | Git blob `1032cfa8b7d7aeb8f857306ead277fa371de943a`；**Git blob 內容 SHA-256 `DDB768024F4560C00CEEF298C1D2EE48145683544DF0BECE4E88331885D2A2B6`** |
| `source-matrix.md` | Git blob `36ac6492a033531ea30e3c463894b2b0829227d1`；**Git blob 內容 SHA-256 `741689FC4BF7D2705546567DEE067AAA884C58CFF61E1ABC9D13C1BC8B3A78CB`** |

SHA-256 由 `git cat-file blob HEAD:<path>` 的原始位元組獨立重算，另以 `Get-FileHash -Algorithm SHA256` 核對檢出檔案，兩種讀法一致。以下判定只適用於上述位元組；作者改動後須重審受影響項目。

## 逐項裁決

| ID | 判定 | 直接來源與核對結果／可說界線 |
| --- | --- | --- |
| **M01** | **PASS，限公司回顧** | [Zippo 歷史〈1930s〉](https://kb.zippo.com/the-history-of-zippo)說第一款於 **1933** 年製成；[Zippo 第六億支時間軸〈1932〉](https://zippo.com/pages/600-millionth-zippo-lighter)說公司 **1932** 年創立。不能把成立年當成第一支製成年。 |
| **M02** | **PASS，限公司回顧** | [Zippo 歷史〈1930s〉](https://kb.zippo.com/the-history-of-zippo)敘述 Bradford 友人、奧地利款須雙手操作、保留擋風煙囪、改金屬盒與鉸鏈蓋。這是日後公司版本，不是同日目擊證詞；Treatment 明示歸屬且不編對話。 |
| **M03** | **PASS，限公司回顧** | [Zippo 歷史〈1930s〉](https://kb.zippo.com/the-history-of-zippo)把 US$1.95、最初產品與終身功能承諾連寫；[Smithsonian 館藏目錄〈Biographical / Historical〉](https://sova.si.edu/record/nmah.ac.0094)可作後來背景，但該館藏年代標為 **1937–1998**，此處未展示 1933 年保證卡。因此「從第一批起」和售價必須歸給公司回顧；創辦人靠燃料或耗材回本的動機、損益均無原件證明。 |
| **M04** | **PASS，原始專利** | [US 2,032,695 原件掃描，第 1 頁頁首](https://patentimages.storage.googleapis.com/c6/09/ea/1d1b14be9be79c/US2032695.pdf)列申請 **1934-05-17**、核准 **1936-03-03**、兩位發明人 **George Gimera 與 George G. Blaisdell**，受讓人 Zippo Manufacturing Company。後接的五人是合夥人，不能算五名發明人。矩陣所列 [USPTO 同件 PDF](https://ptacts.uspto.gov/ptacts/public-informations/petitions/1507161/download-documents?artifactId=wVFWR82SmfXBO2f_lYEl6UFtZ5DdhPwVoBFixGiFaCQ8Am7M1WH5qrE)本輪無可抽取文字；可讀的美國專利原件掃描足以獨立核證。 |
| **M05** | **PASS，限當年申請內容** | [同一原始專利，第 1–2 頁說明與唯一 claim](https://patentimages.storage.googleapis.com/c6/09/ea/1d1b14be9be79c/US2032695.pdf)有套合的內外部件、翻蓋鉸鏈、燃料空間、擋風屏、火石齒輪；說明書把少外露突起、簡化機構列作設計目標。這不能驗證每代量產品完全相同、每件零件可修、實際故障率或保修獲利。 |
| **M06** | **PASS，限公司回顧** | [Zippo 歷史〈1940s〉](https://kb.zippo.com/the-history-of-zippo)說 **1941** 年美國參戰後停止民用市場生產、轉供美軍、鋼殼黑色裂紋塗裝，**1945** 年回歸民市。沒有同期軍需合約或保修條款；Treatment 沒把戰爭與保修建立已測因果。 |
| **M07** | **PASS，限公司後述** | [Zippo 底部日期碼頁〈Dating／Date Codes〉](https://kb.zippo.com/zippo-lighter/date-codes)稱從 **1950 年代中期** 使用，初始品質管制目的包含辨認送修批次問題。不能倒寫 1930–40 年代已有當代年月碼，也不是保固到期日。 |
| **M08** | **PASS，限傳統商品與現行美國說明** | [美國知識庫〈Warranty & Repair〉](https://kb.zippo.com/warranty-repair)將終身承諾明指 **Zippo windproof pocket lighters**；[Zippo 美國官方商品指南〈Lifetime Guarantee〉](https://zippo.com/pages/product-guide-western-lighters)明說免費恢復機械狀況，塗裝不保證；[不點火排查頁](https://kb.zippo.com/zippo-lighter/not-lighting)列燃料、火石、燈芯的日常保養。矩陣所列美國說明書 PDF 本輪超時，已用可讀的官方原始網頁補足，不能推到其他產品或免費供應消耗品。 |
| **M09** | **PASS，僅英國現行流程** | [Zippo UK〈Zippo Repairs: Windproof Lighter〉，`Prepare Zippo Lighter To Ship` 的 `IMPORTANT`](https://www.zippo.co.uk/pages/zippo-repairs-windproof-lighter)說內膽通常**換新而非維修原件**，要求取回原內膽者須在表單註明。僅在送修內膽且需要處理時適用；不能說整支一律換新，也不能推成全球流程。 |
| **M10** | **PASS，限美國現行終身保證** | [美國知識庫〈Decoration Wearing Off〉](https://kb.zippo.com/zippo-lighter/worn-deco)明排除外部 finish／decoration；未滿一年者可聯繫客服討論選項。[〈Broken Hinge〉](https://kb.zippo.com/zippo-lighter/hinge-broke)則承諾免費修鉸鏈。不能把「外觀不保證」講成所有外觀問題無處理途徑，也不能說每種外殼損傷會修復原貌。 |
| **M11** | **HOLD：矩陣用字須更正，費用條款待直接讀件** | [Zippo UK 同一送修頁，`Sending Zippo Lighter`](https://www.zippo.co.uk/pages/zippo-repairs-windproof-lighter)對英國居民要求 **insured and via a trackable method**；矩陣寫「可追蹤**或**保價」把 *and* 寫成 *or*，應改「保價／投保**且**可追蹤」或忠實意譯。該頁只列寄送方式，**未直接寫明誰負擔郵資**。矩陣所引[英語國際版說明書 PDF](https://productinstructions.zippo.com/Documents/English%20outside%20of%20USA%20and%20UK/01_Windproof_Lighters/01_Windproof_Instructions-English_en.pdf)本輪網頁開啟回 `400 Timeout fetching`、`curl` 回連線逾時，故搜尋索引片段不作已直接讀件的費用分配證據。Treatment 中「送修寄件流程也不是『所有成本都零』」若意指**實付費用**，亦應改窄為已證的英國寄送要求，或補可直接讀的一手地區費用條款；逐字稿不得擴成全球統一郵資。 |
| **M12** | **PASS，僅美國 FAQ 所示 Arc 產品** | [美國知識庫〈Double Arc Rechargeable Lighter Insert〉，`If my insert needs repair`](https://kb.zippo.com/arc-repair-faqs-and-guidance)明示 **two-year warranty window**，[總保修頁](https://kb.zippo.com/warranty-repair)將其他產品分開。Arc 內膽不自動承襲傳統防風口袋打火機的終身保證；兩年後是否另有服務或各地權利，此來源不能決定。 |
| **M13** | **PASS，限公司生產紀錄** | [Zippo〈600 Million Zippo Lighters〉頁首及時間軸](https://zippo.com/pages/600-millionth-zippo-lighter)稱 **2020-06-03** 製作第六億支。這是公司報告的**累計生產**節點，不是 2020 年單年銷量；不能倒推保修造成銷量、盈利或環境效果。 |

## 初版 Treatment 裁決與作者待辦（`b83a45fac8a97752aa3f96be46e64a4ba4968728`）

**整體：HOLD 採用，僅因 M11 尚有精確用字錯誤與費用原件缺口。** 六章主線、歷史歸屬、兩位專利發明人、傳統防風款與 Arc 的商品範圍、美國外觀排除、英國內膽更換及第六億支的限定說法，均與本輪可讀一手來源相符。這只通過企劃層的來源審查；不是劇本、時長、影片或站主採用的 PASS。

1. 在作者分支的 M11 把英國寄送方式的「或」改成「且」；維持英國地域標籤。
2. Treatment 的第 5 章若以「不是所有成本都零」暗示顧客必有實付寄件費，也須改窄成英國寄送方法，或補一份可直接讀取的現行官方費用條款。英語國際版 PDF 的搜尋索引文句不足以代替直接讀件。
3. 若作者改 Treatment 或矩陣，對新 Git blob 內容重新計算 SHA-256，受改動的 M 項重新覆核；本收據的固定雜湊不能沿用。

未進行逐字稿、影像或聲音生成、付費請求、匯入、上傳、發布或合併。

## 作者修訂的精確差分覆核（`936873bbb21808546f2dfdbdb17a5e363f263198`）

作者在獨立審查後推送新 head。審查者從遠端重新 `git fetch`，以 `git cat-file blob origin/codex/brand-story-zippo-c20:<path>` 重算位元組 SHA-256，並對前述 `b83a45f` 逐檔比對；沒有取作者口頭摘要作判據。

| 對象 | 修訂後固定值 |
| --- | --- |
| `treatment.md` | Git blob `93b25d03ccb89240c718beef6d8207e505813d8b`；內容 SHA-256 **`3DF65F2FA5EC7B7FAF0F4C3A576C27E66C89EF3368DAAB9AC060E87EB52156E7`** |
| `source-matrix.md` | Git blob `34add6adc97dede409004d537651f94e306c7db4`；內容 SHA-256 **`6687CD9072DFCAFA533DB90F93565CEC802AC225DA147E0D7EFE8BABAD0FB08E`** |

**M11 差分：PASS，僅英國頁面所述寄送方式。** 矩陣改成英國居民「保價**且**可追蹤」，與 [Zippo UK 原頁 `Sending Zippo Lighter`](https://www.zippo.co.uk/pages/zippo-repairs-windproof-lighter)的 *insured and via a trackable method* 一致；不再主張國際版 PDF 的申請人付費句，明註該 PDF 目前不可直接讀回。Treatment 第 5 章移除「所有成本都零」與寄件費推論，只說英國站另列寄件方式，並保留不套用全球的限制。

**此 head 的 Treatment 來源裁決：PASS。** 本次差分未更動 M01–M10、M12–M13 的事實主張，故沿用上表在各自公司回顧、專利、現行美國／英國頁面的限定 PASS。矩陣中的 `RECHECK` 是作者等待獨立覆核的狀態；本節即該覆核結果。若作者再改任一受審檔案，本 PASS 不自動移轉到新雜湊。這仍只通過 Treatment 來源關，不代替站主採用、劇本逐句查核、時長、成本或影片關卡。
