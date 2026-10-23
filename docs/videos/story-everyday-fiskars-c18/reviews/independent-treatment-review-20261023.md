# C18 Fiskars｜獨立 Treatment 來源覆核

覆核日：2026-10-23（台北）。審查者：`codex-c18-independent-review`，未撰寫 C18 Treatment 或來源矩陣，也未修改作者兩檔。

## 站主採用後狀態差異覆核：PASS

作者 [PR #1702](https://github.com/x812033727/travel_scanner/pull/1702) 最新 head `c82b348110728e25e3bd2adea8c22136a22fb538`。由該 head 的**實際 Git blob bytes** 重算：`treatment.md` SHA-256 `74E6239C274C73C243962253425A2438E73677072EF35FF60F53AE1EA6ED6FF8`；`source-matrix.md` SHA-256 `88F6C22CF1361B871E02DCD5DA896618B2F2EC9361B346E7B79D1F7536EB7623`。與前次已核 head `95285e787b65729292232572970340953ffce3ac` 比較，兩份作者檔的差異只有 Treatment 開頭／結尾的關卡狀態與審查連結、矩陣前言的審查連結，以及 M02 評級 `RECHECK`→`PASS`。M01–M12 的事實陳述、引據、年代、權屬、畫面邊界和 Treatment 六章正文均**未改**；作者另更新自己的任務狀態，未納入本收據的來源判定。

**本次 metadata delta PASS；前次 M02 修訂後的 M01–M12／六章內容 PASS 可沿用到上述新 head。** 這只確認最新作者檔反映站主已採用企劃，未把企劃通過推成逐字稿、逐鏡、付費、匯入或發布核准。以下兩節分別保留前次事實修訂 PASS 與最初 HOLD 的精確版本歷史。

## 前次 M02 事實差異覆核：PASS

作者已在 [PR #1702](https://github.com/x812033727/travel_scanner/pull/1702) 新 head `95285e787b65729292232572970340953ffce3ac` 窄修本收據唯一 HOLD。從該 head 的**實際 Git blob bytes** 重算：`treatment.md` SHA-256 `A18B0A0FAE68F8689CA365F498325860FB0C657E59E2AEFA932FE1371AE743D9`；`source-matrix.md` SHA-256 `506268EF53EF65B77D8836480614EED9FA55B58BE7FDAADE11C6650552AC75F3`。PR 的兩檔 diff 僅改矩陣 M02 與 Treatment 第 2 章對應格，其他 M01、M03–M12 說法未變。

| 差異 | 重新核對與結論 |
| --- | --- |
| 矩陣 M02 | 改成「二戰後公司管理層推動公司結構改革，以適應大量生產」，並明示不能推剪刀產量或大量生產起始日。與 [2024 公司上市說明書 PDF 頁 44](https://fiskarsgroup.com/wp-content/uploads/2024/01/Fiskars-Oyj-Abp-Listing-Prospectus-for-Fiskars-Corporations-EUR-200-million-sustainability-linked-notes.pdf) 及 [公司歷史頁 1940s 段](https://fiskarsgroup.com/about-us/our-story/) 相符。**PASS**。 |
| Treatment 第 2 章 | 改成「戰後為適應大量生產而推動的公司結構改革」，畫面／口播邊界又補不得報戰後剪刀產量或量產起始年。1649、1832、1960 年代的相鄰節點沒有新因果，六章仍維持原順序。**PASS**。 |

**本版企劃來源結論：M01–M12 PASS，六章方向 PASS，均須保留原表限定語。** 在此版覆核時，PASS 只解除舊版 M02 HOLD，當時尚不代表站主採用；後續採用狀態已由首節重核。這也不是逐字稿、逐鏡、配音或付費授權。以下舊版 HOLD 表與逐項核對保留作差異追溯，不可誤讀為新 head 仍 HOLD。

本機 `npm run check:tasks` 此時因審查者工作樹的同一任務同時留在 `tasks/open` 與 `tasks/done` 而退出 1：任務板 `done` 曾寫出完成副本，移除 open 副本則遭 `blocked by policy`。這兩個結案殘留**未納入本次 PR 提交**，審查者不再嘗試刪除或繞過。收據內容以已推 PR 檔案讀回為準；此環境限制不改變上面的來源差異判定。

## 舊版判定（已由上述差異覆核解除）

**HOLD（M02 一處需修）**。M01、M03–M12 依下表所列來源與限定語可用；M02 的「戰後大量生產」比原始來源多一步。這是對下列**精確版本**的判定，作者修字後須重算 SHA-256，並由獨立審查者只重核改動及相鄰主張；本收據不能沿用為新版 PASS。

| 受檢物 | GitHub PR #1702 的 Git blob SHA-256 |
| --- | --- |
| head | `513d0d3049058e51308d0e2b269b4b44f84ad312` |
| `treatment.md` | `67193B4605575D30AF08257E41DB242A9894A994AF4A5F040F85FAABC3552460` |
| `source-matrix.md` | `0CC179EF98F6ACAD351116B8B816FD706D4C6F4DA9E5BBEE37D859C36C7EBDA2` |

兩檔以 `git show <head>:<path>` 取得原始 blob bytes，重算 SHA-256；工作樹檔案雜湊亦一致。PR 仍是 draft，本審查不代表站主採用企劃、逐字稿審核、付費或發布。

## M01–M12 逐項覆核

| ID | 判定 | 直接讀到的依據與 Treatment 界線 |
| --- | --- | --- |
| M01 | PASS | [公司歷史頁](https://fiskarsgroup.com/about-us/our-story/) 1649 段與 [2024 上市說明書](https://fiskarsgroup.com/wp-content/uploads/2024/01/Fiskars-Oyj-Abp-Listing-Prospectus-for-Fiskars-Corporations-EUR-200-million-sustainability-linked-notes.pdf) PDF 頁 44 均述 1649 鐵工坊；說明書又記 1883 年有限責任公司成立。Treatment 已避免把 1649 年說成現代剪刀上市或同一法人持續不變。 |
| M02 | **HOLD** | 同一份 [2024 上市說明書](https://fiskarsgroup.com/wp-content/uploads/2024/01/Fiskars-Oyj-Abp-Listing-Prospectus-for-Fiskars-Corporations-EUR-200-million-sustainability-linked-notes.pdf) PDF 頁 44 明確支持 1832 年餐具廠使產品範圍包含剪刀；戰後句說的是管理層實現**調整公司結構以容納大量生產的計畫**。[公司歷史頁](https://fiskarsgroup.com/about-us/our-story/) 相同。矩陣 M02「公司轉向大量生產」和 Treatment 第 2 章「戰後大量生產」省掉了結構改革，容易被理解為已核得實際生產量或剪刀量產起始。改為「二戰後才推動適應大量生產的公司結構改革」；不得推出具體產量或剪刀全線量產年份。 |
| M03 | PASS，限歸屬 | [2006 年報](https://fiskarsgroup.com/wp-content/uploads/2021/08/fiskars_en_2006.pdf) PDF 頁 6 將橘柄剪刀故事起點放在 1967 年並具名 Olof Bäckström；[公司歷史頁](https://fiskarsgroup.com/about-us/our-story/) 說 1967 年基本款準備製造；[MoMA 館藏](https://www.moma.org/collection/works/3250) 另列設計跨度 1960–1967 與這件實物 1976。Treatment 寫 1967 年設計節點可用；逐字稿不要指定未獲原件支持的精確開賣日。 |
| M04 | PASS，限公司說法 | [2017 合作展新聞稿](https://fiskarsgroup.com/news/press-release/innovation-and-creativity-fiskars-corporation-participating-in-the-new-land-of-technology-exhibition-as-corporate-partner/) 引述公司主管，將新研磨方式連於刀片、塑膠連於握持；[2006 年報](https://fiskarsgroup.com/wp-content/uploads/2021/08/fiskars_en_2006.pdf) PDF 頁 6 稱塑膠成型讓一般用剪刀更便宜，並述製程改良。Treatment 沒有給無來源的效率或成本數字，也沒有把性能歸因於橘色。 |
| M05 | PASS，限事後回顧 | [公司歷史頁](https://fiskarsgroup.com/about-us/our-story/) 1967 段與 [2006 年報](https://fiskarsgroup.com/wp-content/uploads/2021/08/fiskars_en_2006.pdf) PDF 頁 6 敘述機器剩橘色材料而多做樣品；[Fiskamin 展覽稿](https://fiskarsgroup.com/news/press-release/orange-and-more-exhibition-celebrates-fiskamin/) 說該塑膠器皿系列間接促成橘柄剪刀。Treatment 將其歸給公司回顧，未推定 Fiskamin 器皿與剪刀是同一天、同一批機器。網頁配圖像一張手寫紙與剪刀，但未提供可辨識的原始票冊或工單，仍不能把回顧拍成現場紀錄。 |
| M06 | PASS，限事後回顧 | [公司歷史頁](https://fiskarsgroup.com/about-us/our-story/) 列黑、紅、綠、橘四款樣品與內部投票；[2017 新聞稿](https://fiskarsgroup.com/news/press-release/innovation-and-creativity-fiskars-corporation-participating-in-the-new-land-of-technology-exhibition-as-corporate-partner/) 的公司主管將決定日說為 1967-10-05。Treatment 沒有寫票數、具體對話或把日期當現存會議紀錄。 |
| M07 | PASS | [2006 年報](https://fiskarsgroup.com/wp-content/uploads/2021/08/fiskars_en_2006.pdf) PDF 頁 6 明列左手用款 1972 年引入，並說後續人體工學與製程改善。Treatment 沒有宣稱發明全球第一把左手剪刀。 |
| M08 | PASS | [公司歷史頁](https://fiskarsgroup.com/about-us/our-story/) 1977 段與 [2024 上市說明書](https://fiskarsgroup.com/wp-content/uploads/2024/01/Fiskars-Oyj-Abp-Listing-Prospectus-for-Fiskars-Corporations-EUR-200-million-sustainability-linked-notes.pdf) PDF 頁 45 都記美國剪刀工廠創設。Treatment 只說設廠，未推成全部產品在美製或顏色造成海外擴張。 |
| M09 | PASS，限公司年報 | [2003 年報](https://fiskarsgroup.com/wp-content/uploads/2021/08/Fiskars_2003_en_v1.pdf) PDF 頁 3、12 記 2003 年在芬蘭註冊剪刀橘色商標；[2006 年報](https://fiskarsgroup.com/wp-content/uploads/2021/08/fiskars_en_2006.pdf) PDF 頁 6 重述。未讀芬蘭登記簿原頁，Treatment 已用「公司年報記載」而非宣稱獨立核實案號／法律範圍。 |
| M10 | PASS，限公司文件 | [2006 年報](https://fiskarsgroup.com/wp-content/uploads/2021/08/fiskars_en_2006.pdf) PDF 頁 6 明列美國 2007 年 1 月註冊；[2014 年公司加拿大新聞稿 PDF](https://mb.cision.com/Public/10696/CM_109706/94b40ab74060676f.pdf) 只佐證美國 2007 年。未讀 USPTO 原件，不補案號。2014 稿封面及內文日期口徑不同，**不用它證明加拿大精確註冊日**。 |
| M11 | PASS，按登記範圍 | [加拿大 CIPO 原始登記](https://ised-isde.canada.ca/cipo/trademark-search/pdf/1602003?lang=eng) PDF 頁 0 記 TMA877999、2014-05-15 註冊、手動剪刀商品，標示限定為**圖示特定把手整個可見表面**的橘色。Treatment 只述特定把手與商品，未外推全世界所有橘色。登記頁當前權利人是 Fiskars Finland Oy Ab，與原始登記人欄不同；後續稿件若具名權利人須按時點分開。 |
| M12 | PASS | [MoMA 藏品 306.1977](https://www.moma.org/collection/works/3250) 以標題直接區分 1960–1967 設計跨度與 1976 年這件實物，材質欄是塑膠、不鏽鋼；當次頁面標「Not on view」。Treatment 只把它作館藏、沒有說現在展出或把 1976 實物說成 1967 原型。 |

## 六章與畫面覆核

- 六章沿 1649 → 1832／戰後 → 1967 → 1972 → 1977 → 2003／2007／2014 推進。末章回看 MoMA 的 1976 館藏實物，是結論的實物回扣，不是宣稱 2014 後才製造。
- 「橘色剩料、員工投票」只按公司的後來敘述；沒有獨立的當年投票票數或配色工單。本集亦沒有從商標登記年或設美國工廠推出銷量、跨國因果。
- 畫面限制足夠明確：無品牌或可讀字的通用剪刀、抽象塑膠流程、匿名工廠；不複製 MoMA 實物照片、公司歷史照片或 CIPO 圖示。註冊圖的**特定形狀**不能用泛用剪刀直接替代為「登記原件」。
- 9:34 旁白、每 30–45 秒鉤子與正文插圖至少七成仍是企劃預排；沒有逐字稿、真實 TTS 或逐鏡時間軸，不據此核准付費製作。

## 修訂與下一關

作者已將 `source-matrix.md` M02 與 `treatment.md` 第 2 章戰後量產句收窄，並通過前次差異重核；站主其後採用此企劃方向，最新狀態與標籤已在本收據首節核實。下一關是逐字稿與逐句來源審查。兩位只讀旁白盲讀、整支報價、付費、匯入及發布都不在本收據範圍。
