# A37 worker 來源存取補充：row v2 候選

2026-10-16，編輯 `/root/a01_repair_editor`。僅本機 Temp。這是來源存取修正提案，不是獨立內容審查或 worker／媒體 PASS；未更動原 row、v4 全文、既有審查或 timeout 證據。

## 候選與結論

- 新檔：`A37-row-v2.json`，SHA-256 `df32efa32d3b4bc0b629901255cb009d48a57629cac610a5eb163178712a7dad`。
- STORY_KEYS 投影的 storyHash：`07eb8e786b9d6d0ac1c6ccb25991a5ba5b5da89ac30c330d8009d1b902b966c1`。
- 原 row `A37.json` 保留，SHA-256 `42c232614376c1dfac93606d8758bb8a637bcc598312c3687b61ae307b295421`。
- v4 全文保留，SHA-256 `63e6277c85cc573556651f686cbf7722d602c620265e7730a9f3f32b7d016d09`。
- `storyProblems=[]`；6 章、10 組 must_verify、10 個來源；point 最長 244 字、claim 最長 123 字、supports 最長 139 字。
- 最終新 row 實跑 repository `fetchSources`：10 個來源 HTTP 200，其中 9 個 reader 可讀；只有官方 PDF 的 `readable=false`。在**沒有獨立 review**時，`fetchProblems` 仍明確列出 `must_verify[0]` 缺少 worker 可讀文字。未消除此訊息或自行加 `reviewer_only`。

## 官方 PDF 的身分、全文與覆蓋範圍

原 [75 週年新聞稿頁](https://www.adidas-group.com/en/media/press-releases/adidas-celebrates-75-years-of-innovation-and-sports-history) 的 Resources → Press Release Download 直接連到：

[同一份 2024-08-13 官方新聞稿 PDF](https://res.cloudinary.com/confirmed-web/image/upload/v1723530968/adidas-group/media/press_releases/2024/20240813_Press_Release_adidas_75_Anniversary_EN_qvrqgp.pdf)。Cloudinary 是官網明示的文件 CDN；未使用轉載站或代理。

- 本機：`../A37-reader-alternatives/adidas-75th-20240813.pdf`
- HTTP 200、`application/pdf`、67,724 bytes、2 頁。
- SHA-256：`70007cfe29d79f348fec65d6bb6de2279d4353fb1a246e367f2a463368328c3c`。
- 已全文抽文並逐頁實看 `adidas-75th-page-1.png`、`adidas-75th-page-2.png`。內容、日期、題名與原 HTML 的新聞稿一致；不是只有搜尋摘要。
- 第 1 頁正文第 2 段：洗衣間主詞是阿迪；1924 與哥哥共同設廠；1928 Lina Radke 穿兄弟供應的鞋，獲阿姆斯特丹 800 公尺金牌。
- 第 1 頁正文第 3 段：二戰後分開；1949-08-18 登記完整公司名；1954 德國國家隊穿旋入式鞋釘球鞋。
- 這些段落**沒有**交代阿迪與隊伍「密切／持續合作」的程度，也沒有明說 1954 那批鞋「按天候換釘」。新 row 不由這份 PDF 推導這兩個修飾。PUMA 2006 回顧內的選釘動作仍保留其原有歸屬。
- 相同 worker `pageReader({whole:true})` 對 PDF 回傳 `status:200, ok:false, error:"not a text page (application/pdf)"`；不稱它是 reader 已讀來源。

## reader 嘗試與未採入口

證據位於 `../A37-reader-alternatives/`，每個 `<id>.json` 保留真正回傳、時間、elapsed 及正文（成功時）。沿用 repository 的 editorial User-Agent、20 秒上限、HTTPS／redirect／字數規則，沒有改 reader、偽造成功、代理、IP 強制指定或登入繞路。

| 檔案 ID | 正規入口 | 實際結果 | 處理 |
| --- | --- | --- | --- |
| history | Adidas Group `/en/about/history` | status 0，timeout | 保留失敗 |
| factsheet-de | 官方德文 75 週年 factsheet | status 0，timeout | 保留失敗 |
| gameplan-original | 2021 原 GamePlan A URL | status 0，fetch failed | 保留失敗 |
| press-de | 同篇官方德文新聞稿 | status 0，timeout | 保留失敗 |
| original-nonwww | 原新聞稿正常 non-www 入口 | status 0，fetch failed | 保留失敗 |
| report2024 | 官方 2024 年報 Product and Marketing HTML | 200，可讀 35,783 字元 | 只有 1949 公司名／1954 鞋釘，並非完整替代，未加進 row |
| press-official-pdf | 官網直接連出的同篇 PDF | 200，不是 reader 支援的文字格式 | 人工實讀來源候選 |
| factsheet-en | 官方英文 75 週年 factsheet | status 0，timeout | 保留失敗 |
| report2019 | 官方 2019 年報 70 Years of adidas HTML | 200，可讀 5,617 字元 | 加入 row 新 index 9，支援精確登記日／公司名 |
| adidas-uk-football-history | HISTORY 正文連出的 Adidas UK 官方足球鞋史 | status 0，timeout | web 可實讀但 worker 仍不可讀，未加入 row |

`fetch-A37-B14-A21.json` 與 `fetch-A37-host.json` 原始失敗紀錄完全保留。上述新增實測是本機結果；沒有主機操作，也不把本機新入口結果說成主機已實測。

## source index 映射

| 舊 index | 新 index | 變更 |
| --- | --- | --- |
| 0 | 0 | 市立博物館，逐值保留 |
| 1 | 1 | 同一 75 週年新聞稿 HTML → 官網直接連出的 PDF；publisher／supports 清楚標 PDF 與能力邊界 |
| 2 | 2 | PUMA 年表，逐值保留 |
| 3 | — | 2021 Adidas 歷史文退出本候選 active sources；原 row、原全文 S4 與人工實讀紀錄保留 |
| 4 | 3 | HISTORY，逐值保留 |
| 5 | 4 | PUMA 2009 活動稿，逐值保留 |
| 6 | 5 | 市政府經濟史，逐值保留 |
| 7 | 6 | PUMA 2006 研發回顧，逐值保留 |
| 8 | 7 | DFB 回顧，逐值保留 |
| 9 | 8 | DFB 比分資料，逐值保留 |
| 新增 | 9 | [2019 官方年報登記段](https://report.adidas-group.com/2019/en/at-a-glance/2019-stories/70-years-of-adidas-new-work-spaces.html) |

## must_verify 與人工覆核邊界

- 新 0：只列同一 PDF 的洗衣間、Lina、1954 鞋釘三項，僅引用 `[1]`。**建議獨立審者實看 PDF 後決定 `reviewer_only=[0]`**；編輯沒有把此欄寫入候選。
- 舊 0 的共同登記、博物館專鞋移到新 2，保留可讀博物館／PUMA 來源；新 2 的原有 RUDA 四個日期、15 名員工、另一建築完全保留。
- 新 1 仍引用 HISTORY 的分工、同屋、私人原因未定；刪原 Adidas 歷史文的「戰時壓力」修飾。1948 分開仍在新 2。
- 新 3 文字不變；登記日期／完整公司名由新 9 的官方年報直接支援，仍保留 PUMA／市政府對同鎮的支援。
- 舊 6 的 1954 鞋資訊移至新 0；新 6 專列 DFB 比賽日期、雨場及比分，不留未由替代來源證明的合作程度或按天候換釘。
- 4、5、7、8、9 的 claim 文字完全不變，只做來源 index 映射。
- 這不是擴大例外：只需 PDF 那一列交另一位人工核對；其他九列仍可由 worker 讀其來源。機械預檢保留這項未完成審查。

## row 相對 v4 全文的精確差異

全文未覆寫，48 段原文及其既有 review 都仍是歷史基準。下表是採用 row v2 時必須遵守的縮限，不能假稱原 v4 已照此逐字修訂。

| 全文段／claim | v4 原句或範圍 | row v2 的允許範圍／差異 |
| --- | --- | --- |
| H01、O01／C01、C06 | 1924-07-01 共同登記與各運動專鞋 | 內容不變；改由新 must_verify 2 管理 |
| H02、O03、O04／C02、C07 | 阿迪洗衣間、1928 Lina 的 800m 金牌，金牌屬選手 | 內容不變；新 must_verify 0 用官方 PDF 人工核對 |
| O08／C09 | 「走過第二次世界大戰」後問還要一起做嗎 | 僅保留時間先後；PDF／HISTORY 都交代二戰後分開，不以戰爭造成分裂作定論 |
| I03／C09、C12 | 「後來的故事裡，有家庭生活的摩擦，也有戰爭帶來的壓力。」 | row 不再授權「也有戰爭帶來的壓力」；保留 HISTORY 的家庭摩擦與私人原因未定。全文原句保留但不能由新 row 再生成這個已退役修飾 |
| E06／C04 | 同年 8/18 登記，名字包括 Adolf Dassler／Adidas | 內容不變；新 2019 官方年報 HTML 直接支援 |
| E10／C17、C31 | 「阿迪和西德國家隊密切合作。」 | 新 engine.point 僅說「西德隊穿著Adidas球鞋進入1954決賽」；不敘述合作的程度、持續期間、未記錄的接觸 |
| T01a／C17、C30 | Adidas 鞋釘「按天候換上適合的版本」，再對照兄弟的調整需求 | 新 turn.point 只依 PDF 說「國家隊穿旋入式鞋釘球鞋」，與哥哥回顧作鞋釘結構對照；不保留 Adidas 的天候調整修飾。PUMA 球員按天候選長中短釘仍在原 E08d／新 must_verify 5 |
| 其餘段落 | 兩公司成立、產品研發、決賽、鎮民社交傾向、死亡與2009混隊比分 | 內容不變；source index 對齊上表。未新增人物行動、原因或傳承關係 |

原全文的 2021 Adidas 歷史文（全文 **S4**，舊 worker source index **3**）仍可供人工讀原版與比對，不被抹除。新 row 的源引採此補充限定；若要求原全文每個修飾都進入新成片，須另解決 S4 的正式取證，不能把本候選當完全逐字等價。

## 交獨立審者

1. 核對新 row 與 `A37-row-v2-manifest.json` 的完整 exact_delta／來源映射；確認退役修飾沒有殘留在 active point、claim、caveat。
2. 實讀 PDF 兩頁及 2019 官方年報首段，核對 PDF 雜湊與來源鏈。
3. 查 `A37-row-v2-fetch.json`：全部來源 HTTP 200、PDF 明確不可讀，剩下的唯一未完成機械門檻為 must_verify 0。只有另一位審者可決定例外與收據。
4. 新稿後續仍要走真實 writer／checker／listener／敘事 panel 與媒體試作；本步沒有取代任何關卡。
