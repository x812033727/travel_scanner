# B18 法院 PDF 分源候選：獨立審查紀錄

- 審查人：Codex /root/b18_pdf_fact_reviewer；日期：2026-10-17。
- 審查對象：隔離候選 B18.json，row SHA-256 9a8ceabd48c6970cd654c077ab33499d070fbbcf5eca4e078e5777a12f99dc9b；canonical story SHA-256 7a598d16c9efcd9014f3554531dfe5569408cb1542cbeb1f90fdfbff4b0975e5。
- 作者的 15 檔 manifest sha256.json SHA-256：87d9ee2fafe2b579dad9dd496391e31d5db585054abf89da380edfd345b959f4。本審查新增的收據與報告不在該作者 manifest 的 15 檔清單內，須各自核對。
- 結論：此企劃資料列與精確改動可簽 pass；僅法院 PDF 專屬的 must_verify[4] 列 reviewer_only:[4]。沒有發現仍需修正的 P1／P2。這不是六章場景、影片成片或匯入核准。

## 獨立讀源

1. [日本法院官方判決 PDF](https://www.courts.go.jp/assets/hanrei/hanrei-pdf-13913.pdf) 的**判決理由**第 8 頁第 466–469 行認定「コンベヤ附調理食台」實用新案第 579776 號於昭和 37 年 12 月 6 日（1962 年）登錄。第 10 頁第 574–578 行認定**該項**權利於昭和 47 年（1972 年）因存續期間屆滿而消滅，之後有許多企業「原告とは無関係に」經營使用輸送帶餐台的壽司店。這段沒有認定每家店的開幕日、所有權利同時到期，或期滿是開店的唯一原因。
2. 同一 PDF 第 5 頁第 306–315 行屬於**被告答辯**，其中提到另一第 851953 號權利，沒有給出該權利的期滿年；不可把它改寫成法院的獨立認定。
3. [J-Net21 訪談](https://j-net21.smrj.go.jp/special/expo1970/20231113.html) 第 1232–1234 行報導律師／專利代理人警告相似店、部分加盟店後來獨立，也把一項被稱為「特許」的權利失效寫成 1978 年。[發明協會沿革](https://koueki.jiii.or.jp/innovation100/innovation_detail.php?eid=00026&age=high-growth&page=keii) 第 34、43 行分別寫 1962 年實用新案登錄及 1978 年後新業者進入。這些 1978 年版本不能取代法院對第 579776 號的 1972 年認定；完整權利鏈尚未證實，本片不口播 1978 年。
4. 其餘來源也開啟核對：[日本機械學會機械遺產第 112 號](https://www.jsme.or.jp/kikaiisan/heritage_112_jp.html) 第 14–20 行區分 1985 年的堺東店輸送機與另存的早期板片；[石野集團年表](https://www.ishino-group.com/history/) 第 71–77、107–113、146–153 行支持 1971 年給茶設備、1980 年旁通裝置與 1986 年 ㄇ 字型店；[石野集團介紹](https://www.ishino-group.com/group/) 第 37–40、352–360 行另有 1974 年整合／販售說法。1971／1974 差異維持 caveat，不進旁白。

## 與父候選的精確差異

- must_verify[4] 從混合來源 [0,2,3] 拆成法院 [3]，只述第 579776 號的登錄、期滿及其後與原告無關企業經營；must_verify[5] 從 [0,3] 拆成 J-Net21 [0]、保留 attributed:true，只述警告與部分加盟店獨立。其餘八筆事實未改。
- turn.point、turn-s079 的唯一改動口播及主張 t8 都由「元祿之外」收窄為「與本案原告／提告的元祿壽司公司無關」，符合判決原文；t8 的 fact 指標從 5 改為 4，直接 source 仍為法院 [3]。e8 和 t9 保留 J-Net21 [0] 及 fact 5。
- 法院來源 supports 現在只說第 5 頁答辯**提及**第 851953 號，沒有為它填入期滿年。企劃 caveat 明寫 1978 年僅作分歧註記、本片不口播；標題、主旨、章摘要、十筆必查事實及 88 句既有旁白沒有 1978 年口播主張。
- turn-s077 畫面改為 1962 年的登錄情境；turn-s079 改為 1972 年後未指定時點的街景，無開幕日或日曆線索。沒有把 1972 年視覺化成新店開幕日。
- 六章仍為 85 景、88 句。除上述一行口播、一筆主張、兩個提示外，其餘 87 句、64 筆主張、直接來源與故事順序未改。claim-coverage.json 的 **65／65 筆場景主張仍是 UNCHECKED**，沒有任何一筆因本 row 審查而變成 PASS。

## 使用界限與待驗

正式來源讀取器的既有讀回對法院 PDF 只取得 application/pdf 而非可供工人引用的正文；候選 build.mjs 的 fetchProblems 檢查使用模擬結果，並非新的正式工人查核收據。因此，reviewer_only:[4] 只代表本審查人獨立讀取法院原文且確認 PDF 專屬事實，不代表 worker 已讀判決。新收據只綁定上列 canonical story SHA；舊收據對新 row 已失效。正式六章來源查核、聽眾及敘事關卡、配音、圖像、CC、成片與站主觀看均須另走原流程；此候選未改 active episodes/B18.json、episodes/reviews/B18.json、stories.json 或正式主機。
換行機械修正：審稿收據及本報告正規化為 LF；收據 JSON 欄位與文字未變，故事 canonical SHA 及作者 15 檔 manifest 未變。
