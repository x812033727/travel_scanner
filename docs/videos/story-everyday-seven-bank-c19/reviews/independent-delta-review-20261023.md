# C19 Seven Bank｜五個 HOLD 的獨立差異重核（2026-10-23）

**判定：PASS，五個改動 ID 均解除 HOLD。** 此判定限於作者 PR #1742 的精確 head f45d93dd263a06f582a2ebc06441b3f924bad381。前一輪 [完整獨立審查 PR #1745](https://github.com/x812033727/travel_scanner/pull/1745) 在作者 a33b270152cf67b883a1ab11480fa4eb71234f80 判 74 PASS／5 HOLD；本輪逐項重讀五個 HOLD 的新旁白、來源欄與配鏡。其餘 74 個 ID 的四檔位元組內容沒有改動，因此與前輪判定銜接為 79 PASS／0 HOLD；這不是重新做一次 79 句完整來源審查。

## 固定輸入與改動範圍

- 作者 [PR #1742](https://github.com/x812033727/travel_scanner/pull/1742)：base f388a6cbc58cf2f3d4e1119f03c5908327d42af6，前版 a33b270152cf67b883a1ab11480fa4eb71234f80，新 head f45d93dd263a06f582a2ebc06441b3f924bad381；本分支直接從新 head 建立。
- a33b270..f45d93d 只有五個檔案變動：四份作者稿件與 author-script-receipt-20261023.md。四份稿件的逐 ID 變動只落在 c190313、c190409、c190410、c190501、c190607。已採用的 treatment.md 與 source-matrix.md 相對企劃 base 沒有改動，SHA-256 仍分別為 78EE6CCAAFF13C7D678698773F8B09AF3B7E7A305DE28817D43A4B42BDA56A1D 及 1F4647D2DC177DCF687EB4193B1A1568AAC8D6D5F27DEE8FF504221720F6B509。
- 以下 SHA-256 直接對新 head 的 Git blob 與工作樹檔案重算，兩者位元組相同，且逐項符合作者新版收據：

| 作者檔案（docs/videos/story-everyday-seven-bank-c19/） | Git blob／工作樹 SHA-256 |
| --- | --- |
| script.md | B3DCA5A9CCF80C8FADA51F19DE3F583EE6C061A0980DD8E1FBDD1755B316464E |
| script-source-notes.md | 1259E2A45EBCB2AA97AC3F71B4666AEE0B8D4AAC20382514FBA68CEA72443ABC |
| visual-plan.md | 29951F986497130C4CA1F50B5C59470DC3B216165D7ABECE7F7954280E827E73 |
| visual-plan.json | C2BE4DF77CF58F7501D79386DBA987AF88896573BEA5947469E7C60BC9FC7AC6 |

## 原發行者原件

- [S3，Seven Bank Annual Report 2010](https://www.sevenbank.co.jp/english/ir/library/disclosure/pdf/2010092231.pdf)，PDF 零起算 P14、紙面 p.13，Partner Financial Institutions：公司說合作方使用 Seven Bank ATM，相較自行持有 ATM 可以降低維護及資金成本；未說特定合作方的決策心理、逐家設點原因或實體備鈔量。
- [S4，Seven Bank Integrated Report 2024](https://www.sevenbank.co.jp/english/ir/library/disclosure/pdf/2024073101.pdf)，PDF P17–P18：P17 說配有證件掃描器的新機可用於身分確認；P18 的 Business Overview 說當時已提供使用證件讀取或臉部辨識的部分金融及行政程序。這不能推成每台機器皆提供。
- [S7，IY Bank 2001-11-09 公告](https://www.sevenbank.co.jp/corp/news/2001/1109_1.html)，正文第 2 段：5 月 15 日東京 23 區 59 地點／66 台，7 月 13 日逾千台，11 月公告時已跨至東京以外地區；11 月 11 日的 2,005 台是尚未到的預定值。
- [S6，IY Bank 2002 揭露誌](https://www.sevenbank.co.jp/corp/disclosure/pdf/IYBank.pdf)，PDF P2 的自家金融服務與合作機構 ATM 事業說明，只支持合作網概念，不提供某合作方職員的情緒或選擇現場。

## 五個 ID 的新判定

| ID | 新旁白／來源／配鏡核對 | 判定 |
| --- | --- | --- |
| c190313 | 旁白仍只提出合作機構為何接入的問題。新圖改為素面機器模型、兩張全空白機構卡及兩條連線，已移除虛構銀行職員及「猶豫」表演；不指名合作方或描繪實際會議。 | PASS |
| c190409 | 旁白明指「二〇一〇年報」，用「相比自行持有 ATM，可降低維護與資金成本」表述 S3 P14；來源註記同步刪除設點／備鈔及逐家動機。原有匿名職員比較兩種素面模型仍是概念比較，沒有日期、合約或真實伙伴識別。 | PASS |
| c190410 | 新圖只有兩條素面交易路線與完全空白單據，明寫沒有數字或字；已移除會讓模型畫出幣符／固定金額的擦除動作。旁白仍只否定一律固定收費。 | PASS |
| c190501 | 新圖用泛用較大範圍無字地圖，保留起始小群並新增遠處點位；與 S7 已記錄跨出東京初始區域、旁白「不再只有一角」一致，未描真實分布或預告台數。 | PASS |
| c190607 | 新旁白以「二〇二四年的報告」歸屬證件讀取等辦事功能，且限制不能說每台皆提供；來源註記同步指 S4 P17–P18。新圖拿掉「未啟用」概念機的錯誤前提，只用無字證件圖示與泛用機器模型，其他機器虛化，不畫全網普及或操作介面。 | PASS |

五處更新的插圖提示詞沒有要求品牌、商標、實際報告圖、可讀金額或文字，也沒有虛構合作方心境。模型實際輸出仍須逐圖檢查。

## 跨檔校驗與剩餘關卡

逐行解析 script.md、script-source-notes.md、visual-plan.md 的 ID 表格及 visual-plan.json 的 shots：四檔各 79 行／項、79 個唯一 ID、同順序；script 旁白與 JSON narration 79/79 相同；script 來源欄、notes 與 JSON source_tags 79/79 相同；MD image/card 類型、提示詞／卡片文字與 JSON shot/card、prompt/card_text 79/79 相同。JSON 為 67 shot／12 card，最長連續 card 為 2；按鏡數插圖為 67/79 = 84.81%。image_model 為 MiniMax image-01，look 只有 preset: cute-mystery。鏡數不等於實際顯示時間。

差異白空檢查通過。本次只通過來源與文字配鏡的五 ID 差異重核；兩位只讀旁白盲讀、站主稿件核准、正文實測 TTS 至少 480 秒、成片插圖顯示時間至少 70%、付費上限、生成圖像驗收、匯入、上傳及發布仍各自待辦。此審查 PR 維持 draft、no-auto-merge；沒有更動作者四檔，也沒有付費或製作行為。