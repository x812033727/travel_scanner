# C18 Fiskars｜獨立逐句來源與配鏡查核

審核日期：2026-10-23。審稿者：`codex-c18-independent-audit`。初審綁作者 PR #1711 的 `ea46ff32b07a234e20e8e462ba8986e5150d3693`；第一輪複核綁 `50f17c46609148311c57adead19b806c51eefe62`；**本次終檢**綁同 PR 的 `2e212b27d68bb408c0ca64bc2d6be05bf255fe64`。目前**來源與同 ID 配鏡：PASS**。原 H01–H04 與後補 `c180312`／`c180404` 均已修妥；兩位純旁白盲讀、站主劇本核准及付費生產仍是獨立關卡。本 PR 只改獨立收據與本票，未改作者四個輸入檔。

## 本次四個輸入檔 SHA-256

| 檔案 | SHA-256 |
| --- | --- |
| `script.md` | `596FD0658B0165E88CF2F816A8E64BB9BA2768C5B2F686CD093148CCA54D1C7C` |
| `source-notes.md` | `0E8591F7FB8A0DED5706E57B6BB631E98F86F17EF57CEE417136E638BFEDBEFA` |
| `visual-plan.md` | `87BF9FF384DD51956152F5531310C388230EF6E315F6E20511ACC2AA07E75ACE` |
| `visual-plan.json` | `6301E905E5C019CC04EC6F82B3874E8CC1FAD48335B7B6A1AAAC19B664FB1F99` |

四值由新作者工作樹檔案 bytes 獨立計算，與交接預期一致。任何輸入改字，本次判定都不自動適用。

## 直接開啟的 M01–M12 原件

Fiskars 官網在網頁擷取器逾時；改以專案要求的 `Mokaair-editorial/1.0` User-Agent 直接抓原網址，以下 Fiskars HTML/PDF、Cision PDF、CIPO PDF 均回 HTTP 200，PDF 直接抽取相應頁文字。MoMA 館藏頁直接讀取。這些是公司／官方原件，不把較早的企劃 PASS 當作本次逐句查核。

| 矩陣 | 原件與本次核到的界線 |
| --- | --- |
| M01–M02 | [Fiskars 沿革](https://fiskarsgroup.com/about-us/our-story/)及[2024 年公司債券說明書](https://fiskarsgroup.com/wp-content/uploads/2024/01/Fiskars-Oyj-Abp-Listing-Prospectus-for-Fiskars-Corporations-EUR-200-million-sustainability-linked-notes.pdf) PDF 0-based p44：1649 鐵工坊；1832 餐具廠產品含剪刀；二戰後的結構改革是為適應大量生產，沒有戰後剪刀產量。 |
| M03–M04 | [2006 年公司年報](https://fiskarsgroup.com/wp-content/uploads/2021/08/fiskars_en_2006.pdf) PDF p6 與 [2017 年公司新聞稿](https://fiskarsgroup.com/news/press-release/innovation-and-creativity-fiskars-corporation-participating-in-the-new-land-of-technology-exhibition-as-corporate-partner/)：年報將 Bäckström 的橘柄剪刀起點放在 1967，說塑膠握柄使一般用剪刀「更便宜」；新聞稿說新研磨法與塑膠帶來新的人體工學。兩者都沒有剪切效率或**製作成本**測量。 |
| M05–M06 | [公司沿革](https://fiskarsgroup.com/about-us/our-story/)、[2006 年報](https://fiskarsgroup.com/wp-content/uploads/2021/08/fiskars_en_2006.pdf) p6、[2024 年說明書](https://fiskarsgroup.com/wp-content/uploads/2024/01/Fiskars-Oyj-Abp-Listing-Prospectus-for-Fiskars-Corporations-EUR-200-million-sustainability-linked-notes.pdf) p45，以及 [2017 年公司新聞稿](https://fiskarsgroup.com/news/press-release/innovation-and-creativity-fiskars-corporation-participating-in-the-new-land-of-technology-exhibition-as-corporate-partner/)：機器剩橘料、黑／紅／綠／橘試色及內部投票都是多年後的公司敘述；精確投票日期也只見後來新聞稿。另讀[公司 Fiskamin 展覽新聞稿](https://fiskarsgroup.com/news/press-release/orange-and-more-exhibition-celebrates-fiskamin/)：只說 Fiskamin 意外促成橘柄剪刀，不能據此斷言兩者同日或同一機器。本稿沒有這項額外推斷。 |
| M07–M08 | [2006 年報](https://fiskarsgroup.com/wp-content/uploads/2021/08/fiskars_en_2006.pdf) p6 清楚記產品線左手用款於 1972 推出，並談後續人體工學及製程改良；[公司沿革](https://fiskarsgroup.com/about-us/our-story/)和[2024 年說明書](https://fiskarsgroup.com/wp-content/uploads/2024/01/Fiskars-Oyj-Abp-Listing-Prospectus-for-Fiskars-Corporations-EUR-200-million-sustainability-linked-notes.pdf) p45 記 1977 美國剪刀廠。這不能推出全球第一把左手剪刀或此後全在美國製造。 |
| M09–M10 | [2003 年報](https://fiskarsgroup.com/wp-content/uploads/2021/08/Fiskars_2003_en_v1.pdf) p3／p12 說芬蘭 2003 年註冊；[2006 年報](https://fiskarsgroup.com/wp-content/uploads/2021/08/fiskars_en_2006.pdf) p6 說美國 2007 年 1 月註冊。[2014 公司加拿大新聞稿 PDF](https://mb.cision.com/Public/10696/CM_109706/94b40ab74060676f.pdf)也列芬蘭／美國年份。芬蘭、美國的登記簿與確切商品／標示範圍並未在本次原件組內；保留「公司年報記載」，不可借用加拿大範圍替兩地作證。該新聞稿的「上週」時間敘述與 CIPO 官方登記日不合，本稿採 CIPO 日期是對的。 |
| M11 | [加拿大 CIPO TMA877999 原始紀錄](https://ised-isde.canada.ca/cipo/trademark-search/pdf/1602003?lang=eng) p0：2014-05-15 註冊；商品是手動剪刀；標示是**登記圖中那把剪刀的特定握柄整個可見表面**所施用的橘色。不是橘色本身在所有商品、所有剪刀或所有國家的壟斷。 |
| M12 | [MoMA 藏品 306.1977](https://www.moma.org/collection/works/3250)：設計年段 1960–1967、這件實物 1976、材質塑膠與不鏽鋼，頁面目前標示未展出。它不是可指認的 1967 首件。 |

## 變更複核：原 HOLD H01–H04

第一輪複核於 2026-10-23 重新以專案 User-Agent 取回 [Fiskars 公司沿革](https://fiskarsgroup.com/about-us/our-story/)、[2006 年報](https://fiskarsgroup.com/wp-content/uploads/2021/08/fiskars_en_2006.pdf)、[2003 年報](https://fiskarsgroup.com/wp-content/uploads/2021/08/Fiskars_2003_en_v1.pdf)與[加拿大 CIPO TMA877999](https://ised-isde.canada.ca/cipo/trademark-search/pdf/1602003?lang=eng)，四個原網址均回 HTTP 200；直接重讀機器剩料／四色投票、`cheaper`、芬蘭及美國年份、加拿大標示與商品欄。其餘 M01–M12 的先前直接查核界線仍列在上表。第一輪作者只動 7 個旁白 ID、4 個 JSON 鏡頭，以及來源註記／MD 摘要；沒有改其餘 78 句事實。

| 原 HOLD | 這版句／同 ID 畫面 | 複核 |
| --- | --- | --- |
| H01 | `c180103`／`c180104` | **PASS（指定兩句）**。開場先說「按 Fiskars 多年後的說法」，再說不同色樣品等著被選；不再把樣品說成真的排在桌上。`c180104` 改成手中比較純色通用握柄樣片，MD 明示概念工坊，未增加可驗的 1967 現場事實。前版仍殘留的 `c180312`／`c180404` 已於下節終檢通過。 |
| H02 | `c180307`／`c180308` | **PASS**。[2006 年報](https://fiskarsgroup.com/wp-content/uploads/2021/08/fiskars_en_2006.pdf)只說塑膠柄讓一般用剪刀變得更便宜，沒有成本測值；旁白現照此說且不報數字。`c180308` 換兩把通用剪刀的概念對照，不再畫成本帳。 |
| H03 | `c180511` | **PASS**。[CIPO 原件](https://ised-isde.canada.ca/cipo/trademark-search/pdf/1602003?lang=eng)的 `particular handles` 與 `whole visible surface` 兩層限定進入旁白。JSON 畫兩個橘柄整個可見面，但要求外形原創、通用；MD 明說不是登記圖複製。沒有把示意圖當法律原件。 |
| H04 | `c180608` | **PASS**。旁白先說各地要分開看，再只述讀到的加拿大原件所列手動剪刀及圖中特定握柄；沒有借加拿大範圍替芬蘭／美國登記簿作證。三份空白概念文件與旁白相合。 |
| 原輕微建議 | `c180609`／`c180214` | **已清理**：「一桶」改成「一點」剩料；圖片 prompt 把否定式「沒有文字」換成正面「素面桌上的握柄」，不要求可讀字。 |

## 終檢：前版殘留兩句

作者從 `50f17c46609148311c57adead19b806c51eefe62` 到 `2e212b27d68bb408c0ca64bc2d6be05bf255fe64`，四個輸入檔中僅 `script.md` 的下列兩行有改動；`source-notes.md`、配鏡 MD 和 JSON 位元組皆未變。獨立重讀[公司沿革](https://fiskarsgroup.com/about-us/our-story/)與[2006 年報](https://fiskarsgroup.com/wp-content/uploads/2021/08/fiskars_en_2006.pdf)的相關段落：前者記黑、紅、綠、橘四色原型和內部投票，後者記各色樣品及投票；兩者均未記實際桌面擺放。`source-notes.md` 也明說缺少此證據。

| ID | 新旁白與同 ID 畫面 | 判定 |
| --- | --- | --- |
| `c180312` | 「那些不同顏色的樣品還沒有答案」已刪先前的「桌上」；JSON 仍畫匿名設計者在素面桌上排四色通用握柄樣品。整體 MD 將 74 鏡定為原創概念插圖，旁白不稱實際現場。 | **PASS**；畫面只作概念轉場，沒有新歷史位置斷言。 |
| `c180404` | 「公司說，樣品還有黑色、紅色和綠色，合起來四種試色」已刪先前歸給公司的「桌上」；JSON 仍畫匿名人物於素面桌排列四色通用握柄。MD 第四章明說這是按公司後來回憶畫的概念，不演真實投票。 | **PASS**；四色與公司原件一致，桌面僅為構圖。 |

這兩句是前次漏列的原 H01 來源邊界問題，並非新增事實。本輪 diff 沒有其他旁白、來源註記或配鏡改動，故沒有新的事實或視覺主張。

## 85 句與配鏡結構核對

初審已逐句讀過 85 個「旁白／依據」與同 ID JSON prompt／後製卡、逐章對 MD；第一輪重讀 7 個變動旁白 ID 和 4 個變動 prompt，終檢再讀 `c180312`／`c180404` 與同 ID 畫面。本輪重跑全 85 個 ID 的結構和禁詞核對。沒有新的來源、地點、人物或法律斷言被加進圖片 prompt；第一輪改過的 prompt 是 `c180104`、`c180214`、`c180308`、`c180511`，終檢未改 prompt。

| 章 | ID | 句／JSON 景 | `shot`／`stats` | 目前判定 |
| --- | --- | ---: | ---: | --- |
| 1 | c180101–c180108 | 8／8 | 8／0 | 原 H01 指定兩句已修，其他原件／概念配對相合。 |
| 2 | c180201–c180215 | 15／15 | 12／3 | 未變；來源與概念配對相合。 |
| 3 | c180301–c180316 | 16／16 | 15／1 | 原 H02 已修，`c180312` 桌面措辭已修，配鏡為概念畫面。 |
| 4 | c180401–c180416 | 16／16 | 15／1 | `c180404` 桌面歸屬已修；1972 左手用款仍正確。 |
| 5 | c180501–c180519 | 19／19 | 15／4 | 加拿大標示已準確限定；芬蘭／美國年份仍明說出自公司年報。 |
| 6 | c180601–c180611 | 11／11 | 9／2 | 加拿大法域範圍與 MoMA 年代、材質的區分相合。 |

85 個旁白 ID 與 85 個 JSON ID 順序完全相同，雙方重複 0，總計 **74 插圖／11 後製卡**，最多連續 2 張卡。74／85 僅是張數，仍不證明插圖畫面時間 ≥70%。74 個圖片 prompt 沒有品牌／設計師姓名、logo、商標圖、MoMA、歷史年份數字或要求可讀字；模型 `MiniMax image-01`、`look: {"preset":"cute-mystery"}` 未加 style／negative。片頭仍在 `c180108` 後 5 秒，v4 片尾仍在 `c180611` 後 21 秒與連結位置。沒有將橘色寫成已證銷量原因。

正文 TTS ≥480 秒、插圖畫面時間 ≥70%、兩位新的純旁白盲讀、站主劇本核准、報價及付費批准均未完成。來源／配鏡可交下一個純旁白盲讀關卡；本收據不跨越其餘關卡。
