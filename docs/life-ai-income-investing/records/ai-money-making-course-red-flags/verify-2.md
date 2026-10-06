# verify-2 — ai-money-making-course-red-flags（第二輪：重查、法遵、讀者優先，2026-10-05）

讀法：全部在 2026-10-05 以 curl -sSL（UA 為 Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)）重抓，確認 HTTP 200，去掉 `<!-- -->` 註解與 script／style 後讀本文。腳本與抓下的純文字在 /home/user/batch-ai-income/_tools/ai-money-making-course-red-flags/v2/。law.moj.gov.tw 的單條頁第 2 條第一次回 HTTP 200 但內容是「Unreachable Server」錯誤頁，不算來源；改讀 LawAll（pcode=J0170001）全文，第 2 條第 10、11 款可讀。

格式：主張｜判定｜來源。

## A1. 第一輪改過的事實（逐條重查）

- 第一次申訴可直接向業者，或用消保會「線上申訴與調解」系統；上班時間（不含午休）撥 1950 向縣市消費者服務中心諮詢；業者應自申訴之日起十五日內妥適處理；未妥適處理向縣市消保官第二次申訴；仍未妥適處理向縣市消費爭議調解委員會申請調解；消費訴訟不以申訴、調解為必要｜ok｜https://cpc.ey.gov.tw/Page/71E988F034956960
- 線上申訴系統「將自動通報相關直轄市、縣（市）政府的消費者服務中心受理」｜**改字**：正文原寫「所在縣市」，FAQ 寫的是「相關」縣市，改為「系統會通報相關縣市的消費者服務中心受理」｜https://cpc.ey.gov.tw/Page/1DCF8AA4D223F601/37082320-17f6-43d9-b3f5-1d9adb61211a
- 1950：上班時間（不含午休）撥打，直接轉接至所在地縣市政府消費者服務中心；是諮詢服務｜ok｜https://cpc.ey.gov.tw/Page/A1D31DAB12817E9
- 消保法第 43 條（向業者、消保團體或消費者服務中心申訴；十五日內妥適處理；未獲妥適處理向消保官申訴）｜ok｜https://law.moj.gov.tw/LawClass/LawSingle.aspx?pcode=J0170001&flno=43
- 消保法第 44 條（申訴未獲妥適處理得向直轄市或縣（市）消費爭議調解委員會申請調解）｜ok；正文補「縣市的」與條文一致｜https://law.moj.gov.tw/LawClass/LawSingle.aspx?pcode=J0170001&flno=44
- 摘要 4、表格第 2、4 列、diagram-1 第一列與 desc、圖片 alt、description 的新流程｜ok（與上列三頁一致；摘要 4 刪去 1950 一句以縮短，1950 仍在正文、表格、圖與 description）｜同上
- 165：可諮詢、檢舉或報案；市話免付費；行動電話除中華電信門號免付費外，其他電信每分鐘新臺幣 1 元；165 官方網站可網路報案｜ok｜https://www.npa.gov.tw/ch/app/faq/view?module=faq&id=2144&serno=A1078837
- 摘要 3「依原主管機關的函釋」：經濟部工業局 110.5.31 函，業者利用其他現成之影音或通訊軟體系統教學，與網路教學應記載事項的定義不符；行政院 112-02-17 刊登，資料來源消費者保護處｜ok｜https://www.ey.gov.tw/Page/8F51FEE53AB45EA9/00ff0685-60a0-4aef-ae23-0b9b19f0fc5c

## A2. 第一輪未能確認的項目

- 網際網路教學服務應記載事項的現行條文：law.moda.gov.tw/LawContent.aspx?id=GL000019 今天 curl 與 WebFetch 仍回 403，Wayback CDX 連線被重設。數位產業署法規命令列表（https://moda.gov.tw/ADI/services/laws-regulations/related-law-and-regulation-of-adi/886，HTTP 200）仍列此事項；WebSearch 限定 moda.gov.tw、gazette.nat.gov.tw、ey.gov.tw 只找到 2023-12-04 的修正「預告」（預告期至 2024-02-02），沒找到正式發布修正的公告。重抓行政院附檔 PDF（https://www.ey.gov.tw/File/3089198AE3736626?A=C，HTTP 200，pdftotext）：前言適用範圍、應記載事項一（審閱期至少三日）、八（現金與分期總價、加價購買課程總價）、十八（期滿或用完即終止；此外得隨時通知終止，業者不得拒絕，依雙方擇定方式結算）、二十（廣告為契約一部分）、不得記載事項一、五、六、十二，與正文一致。行政院頁註明 109-05-15 生效、111-08-27 業務移撥數位發展部｜**仍未能直接讀到現行版**；正文用到的各點在公告版與 2023 草案都相同，維持第一輪的處理，不改｜https://www.ey.gov.tw/Page/DFB720D019CCCB0A/397a2ff8-748a-4df1-a52e-860278d0c275
- LINE 群組／現成視訊軟體不在契約規範內：正文已寫明是原主管機關（經濟部工業局）的函釋；數位發展部是否沿用無公開資料可查，維持｜unresolved（已在正文標明出處層級）
- 線上申訴系統 FAQ 原本只在 notes.md：第二輪把 sources 裡的「通訊交易7日解除權例外規定自105年1月1日起施行」新聞稿（cpc.ey.gov.tw/Page/53D79214534B3D4C）換成這頁 FAQ。理由：被換掉的新聞稿只支持「少了告知，就不能用這個例外拒退」，而準則第 2 條本文（「並經企業經營者告知消費者，將排除……解除權之適用」）已在 sources，條文本身就支持這句；FAQ 則是「系統通報縣市消費者服務中心受理」唯一的來源。sources 維持 20 筆。
- 正文長度：改後 2,739 字（工具計），在 1,800–3,000 內、高於 2,200–2,600 目標。沒有可刪而不損資訊的段落，未刪。
- 第一輪用 shell heredoc 寫中文：本輪所有修改都用寫成檔案的腳本（v2/fix2.py）或編輯工具，沒有用 heredoc。

## A3. 抽查（verify-1.md 的條列，從第 2 條起每隔三條）

- 摘要 2：數位內容例外須事先同意並經告知排除（準則第 2 條本文與第 5 款）｜ok｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=J0170012
- 把工具能力說得比實際多，可能構成引人錯誤之表示（公平法第 21 條第 1、2、4 項：價格、品質、內容、用途及其他具招徠效果事項；服務準用）｜ok｜https://law.moj.gov.tw/LawClass/LawSingle.aspx?pcode=J0150002&flno=21
- 違反多層次傳銷管理法第 18 條處七年以下有期徒刑（第 29 條，另得併科一億元以下罰金，正文未寫）｜ok｜https://law.moj.gov.tw/LawClass/LawSingle.aspx?pcode=J0150017&flno=29；第 18 條同日重抓 ok
- 線上課程契約應寫明現金／分期總價及加價購買課程總價（應記載事項八）｜ok｜https://www.ey.gov.tw/File/3089198AE3736626?A=C
- 7 日從隔天起算；期限內發出書面即算數（Q&A 056；第 19 條第 4 項）｜ok｜https://cpc.ey.gov.tw/Page/4432D6D5FA6677B9/c25817a4-de69-4835-a81a-ebd05a19669b；https://law.moj.gov.tw/LawClass/LawSingle.aspx?pcode=J0170001&flno=19
- 例外準則依消保法第 19 條第 2 項訂定，105-01-01 施行；第 2 條第 5 款｜ok｜https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=J0170012
- 名稱與主管：行政院頁「自111年8月27日業務移撥數位發展部」｜ok｜https://www.ey.gov.tw/Page/DFB720D019CCCB0A/397a2ff8-748a-4df1-a52e-860278d0c275
- 廣告為契約一部分；不得記載「廣告僅供參考」（應記載事項二十、不得記載事項六）｜ok｜https://www.ey.gov.tw/File/3089198AE3736626?A=C
- 公平法第 21 條各項｜ok；另見下方「改」：第 5 項但書（非知名公眾人物、專業人士或機構的薦證者，以報酬十倍為限）原本略去，正文補上｜https://law.moj.gov.tw/LawClass/LawSingle.aspx?pcode=J0150002&flno=21
- 公平法第 42 條：「得限期令停止、改正……並得處新臺幣五萬元以上二千五百萬元以下罰鍰」｜ok；正文「並處」改為「並可處」，與條文的「得」一致｜https://law.moj.gov.tw/LawClass/LawSingle.aspx?pcode=J0150002&flno=42
- 165 可諮詢、檢舉或報案；市話免付費｜ok｜https://www.npa.gov.tw/ch/app/faq/view?module=faq&id=2144&serno=A1078837
- 表格第 1 列（消保法第 19 條）｜ok｜https://law.moj.gov.tw/LawClass/LawSingle.aspx?pcode=J0170001&flno=19
- 表格 caption「查證於 2026 年 10 月」：2026 也是 diagram-1 頁尾數字的對應｜ok｜—
- diagram-1 廣告與詐騙兩列：處理原則第 3 點（社群／通訊軟體群組、說明會、銷售現場口頭推銷）、第 8 點（書面或電子文件、真實姓名及地址、廣告等事證）；刑事警察局假求職（訂金、保證金、訓練費；以設定薪資轉帳騙取帳戶及密碼）、假投資（LINE 投資群組、小額獲利、拒絕出金、「保證獲利」「穩賺不賠」必定是詐騙）｜ok｜https://www.ftc.gov.tw/internet/main/doc/docDetail.aspx?uid=165&docid=13937（114.7.1 發布最新修正）；https://www.cib.npa.gov.tw/ch/app/data/view?module=wg116&id=1909&serno=87a85079-c42f-48cb-9506-14e08c912a39；https://www.cib.npa.gov.tw/ch/app/data/view?module=wg116&id=1909&serno=a4f8d5ab-3d53-4d22-9411-031fddde7a4e
- 站內連結三筆：repo 內容包的 zh-TW 標題分別為「警示帳戶是怎麼來的：避免帳戶被凍結的實際做法」「網銀與帳戶安全：裝置綁定、OTP 與常見詐騙手法」「AI 詐騙與 Deepfake：台灣案例與防範」，kind 皆為 life｜ok｜apps/api/app/guides/content/*.json
- 額外重查：薦證規範說明三（四）（五）、消保法第 2 條第 10、11 款（LawAll）｜ok｜https://www.ftc.gov.tw/internet/main/doc/docDetail.aspx?uid=165&docid=13021；https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=J0170001

## B. 法遵

- **改**：批次 README 規則 4 禁寫「月入」「被動收入」「躺著賺」。原稿在摘要 1 與話術清單第 1 項把這些字當警訊引用。雖然是當反例引用、工具的 FINANCE_CLAIM_WORDS 也不適用（無 finance topic），但這三個字串本身被規格點名，改成同義的警訊說法：「保證每月進帳」「保證每月進帳多少」「什麼都不用做也有收入」。警訊的意思不變。全文已無「月入」「被動收入」「躺著賺」「輕鬆賺」。
- 無收入承諾、無收入截圖或見證；全文沒有金額舉例，所以不需要「假設」標示。
- 沒有平台費率或抽成。LINE 只作為詐騙與上課管道的描述出現，沒有推薦或貶低任何平台。
- 法律陳述都對到法條或主管機關頁：消保法第 2、19、43、44 條、合理例外準則、網路教學應記載事項、公平法第 21、42 條、薦證規範說明、處理原則、多層次傳銷管理法第 18、29 條、刑事警察局手法說明、警政署 165 FAQ。
- **改**：公平法第 21 條第 5 項的十倍上限原本略去，會讓一般學員見證人誤以為要負全額連帶責任，補一句。
- **改**：第 42 條的罰鍰是「得處」，正文改為「並可處」。
- 「保證獲利」「穩賺不賠」仍在話術清單第 6 項，這是刑事警察局頁的原話、以詐騙特徵引用，保留。

## C. 讀者優先與文字

- 「本文」「這篇」0 次；正文沒有查證過程的敘述；來源只在 sources 與表格依據欄。
- 導言第一段第一句就回答問題（判斷重點是賣方怎麼承諾、怎麼收錢）。
- **改**：站內連結文字裡的「Deepfake」第一次出現沒有中文，補成「Deepfake（深度偽造）」。其餘外文只有 AI、LINE（品牌名）。
- 台灣用語、無驚嘆號、無贅語。
- 正文 2,739 字（工具計），在 1,800–3,000 內，高於 2,200–2,600 的目標；摘要 4 已縮短，其餘段落各有法規資訊，沒有再刪。

## 圖

- 重看 diagram-1.png 與 hero.png（第一輪渲染，SVG 本輪未改）：無壓線、無溢出、無互疊；diagram-1 第一列順序與 desc、alt 一致；hero 無 logo、無人臉、一行 56px 字，無上升長條或金幣。

## 機械檢查

- pack_cli ingest --dry-run：通過（dry run: nothing written）。
- intake_check.py：RESULT PASS（0 failures）；body_length=2739；sources=20。
