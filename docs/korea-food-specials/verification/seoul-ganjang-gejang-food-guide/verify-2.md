# seoul-ganjang-gejang-food-guide — verify-2

日期：2026-09-20

## 獨立來源與事實覆核
本輪為不同於原撰稿者的 Codex 獨立第二輪，6個官方來源重抓HTTP200，原HTML、可見正文及manifest均在codex-evidence。
- KTO韓英料理頁支持生蟹以醬油調味液醃製、與辣味版本區別，以及蟹殼拌少量飯的吃法；沒有添加保健或安全療效。
- 양반댁：인사동길19-18，醬蟹定食為主菜；鍋飯及配菜、其他굴비/보쌈不混作醬蟹套餐保證。平日11:30–21、15–17休息，週末11–21。
- 함초간장게장：명동8가길27地下一樓，醬蟹及醬油蝦等官方菜單；11:30–22。
- 진미식당：마포대로186-6，gejang定食、每日限量及尖峰預約；12–20，15:30–17休息，週日休，無停車。刪除無獨立來源的外地同名店敘述。
- 게방식당：선릉로131길17，醬油/辣味蟹、蟹湯、蟹拌飯；11:30–21，15–17:30休息，週日休。沒有沿用米其林作入選根據。
- source title 對齊頁面，SVG description補上並與desc一致。菜名對照不把蟹殼拌飯當成每店都有게장비빔밥菜單。

## 實際影像與授權
已以view_image實看hero、photo與Chrome渲染PNG。Hero為白盤醬汁醃蟹、辣椒及芝麻；photo為蟹肉蟹黃近拍，兩者為料理示例而非指定店菜照。SVG兩欄菜名對照1600×900，韓文與中文字可讀、無裁切重疊。
Commons Gejang.jpg：kimsco，CC0；Ganjang-gejang 1.jpg：lazy fri13th，CC BY 2.0；credit/source_url由ingest保留，非觀光網站圖像挪用。

## 收件命令
已完成本轮修正后的 dry-run → ingest。最终 intake、定向 lint 与图解最终像素检查结果见下方补记；本记录不代表部署或发布。

## 可追溯來源清單
- [K-로컬 미식여행 33선] 01. 한국의 독보적인 밥도둑, 간장게장> 여행기사 :대한민국 구석구석: https://korean.visitkorea.or.kr/detail/rem_detail.do?cotid=3dd61995-fae7-4e70-8d6c-e2e4197ebb7b
- Ganjanggejang: Korea’s Ultimate “Rice Thief”-  VISITKOREA: https://english.visitkorea.or.kr/svc/contents/contentsView.do?menuSn=904&vcontsId=221242
- Yangbandeck (양반댁)-  VISITKOREA: https://english.visitkorea.or.kr/svc/contents/contentsView.do?vcontsId=99515
- Hamcho Ganjanggejang (함초간장게장)-  VISITKOREA: https://english.visitkorea.or.kr/svc/contents/contentsView.do?vcontsId=59525
- Jinmi Sikdang (진미식당)-  VISITKOREA: https://english.visitkorea.or.kr/svc/contents/contentsView.do?vcontsId=192629
- Gebang Sikdang (게방식당)-  VISITKOREA: https://english.visitkorea.or.kr/svc/contents/contentsView.do?vcontsId=59972

圖像授權頁：
- https://commons.wikimedia.org/wiki/File:Gejang.jpg
- https://commons.wikimedia.org/wiki/File:Ganjang-gejang_1.jpg

本輪獨立重開上述 Commons 授權頁核對作者、授權及原圖尺寸；CLI 已保留公開信用欄。

## 最終 intake
設定 PYTHONPATH 為隔離repo apps/api後，intake_check.py 通過，正文3839字、無警告。早先未設PYTHONPATH的回退計數不作最終依據。

## 最終 CLI 結果
修正後 dry-run → ingest 成功。以四篇明確 --slug 參數及 --render-dir 執行 pack_cli lint，最終輸出 `4 entries checked`、exit 0（2026-09-20）。所有照片与SVG已實際檢視；收件至隔離repo完成，未提交、推送、部署或發布。
