# jeju-gujwa-sehwa-cafe-guide — verify-2

日期：2026-09-20

## 獨立第二輪
原作者 Terra，首輪 Astra；本輪 Codex 重新取得5頁原始HTML與可見正文，保存codex-evidence，排除隱藏SEO payload、script/head/hidden節點。正文僅引用官方詳細資訊與可见頁首，不使用遊客評論。
- 카페공작소：해맞이해안로1446，細花海、店前拍照點、胡蘿蔔蛋糕、영귤/댕유자飲品、寧靜標語可見；海景/網美成立。
- 카페한라산：可見道路地址面水1路48（면수1길48），開闊海景、別館舊電視、路燈、植物與腳踏車；海景/網美成立，圖解道路改為면수1길。
- 미엘드세화：해맞이해안로1464，可見海景、胡蘿蔔蛋糕/汁及蘋果芒果刨冰；維持只有海景，週三公休不引用隱藏欄位。
- 달치즈：해녀박물관길35，可見低矮老屋、傳統住家般外觀、窯烤麵包披薩/咖啡；刪掉仍殘留的祖母、鄉村小物及카이막，菜名表改화덕。老屋支持具體空間，不代表韓屋。
- 477+：질그랭이中心可見正文直接點名二樓咖啡、地址해맞이해안로1392。中心在海邊不證明咖啡座位看海；現代整潔屬一般描述，不足具體網美，表格/正文/圖解改未標類型。保留可見具名飲品/麵包。

## 圖像與授權
已實看兩照片：hero為海女博物館觀景方向的田地、村落與海灣；photo為細花海灘淺水、遊客、防波堤和燈塔，均非店家內景。
重新開啟Commons來源頁核對：Sehwa jeju korea.jpg原圖4032×3024，Sgroey，CC BY-SA4.0；세화해수욕장3.JPG原圖3264×2448，Bohyunlee，CC BY-SA4.0。信用欄完整；hero由CLI適配1600×900。SVG為Mokaair原創。

## 收件命令
已完成本轮修正后的 dry-run → ingest。最终 intake、定向 lint 与图解最终像素检查结果见下方补记；本记录不代表部署或发布。

## 可追溯來源清單
- Visit Jeju：카페공작소（細花海、拍照點與地址）: https://visitjeju.net/kr/detail/view?contentsid=CNTS_000000000018312
- Visit Jeju：카페한라산（細花海水浴場、舊電視、復古空間與地址）: https://www.visitjeju.net/kr/detail/view?contentsid=CNTS_200000000012675
- Visit Jeju：미엘드세화（細花海與地址）: https://www.visitjeju.net/kr/detail/view?contentsid=CNTS_000000000020189
- Visit Jeju：달치즈 구좌세화점（濟州老房子、空間與地址）: https://www.visitjeju.net/kr/detail/view?contentsid=CNTS_300000000015804
- Visit Jeju：질그랭이센터（內文點名카페 477+、二樓現代室內與地址）: https://m.visitjeju.net/kr/detail/view?contentsid=CNTS_200000000010801

圖像授權頁：
- https://commons.wikimedia.org/wiki/File:Sehwa_jeju_korea.jpg
- https://commons.wikimedia.org/wiki/File:%EC%84%B8%ED%99%94%ED%95%B4%EC%88%98%EC%9A%95%EC%9E%A53.JPG

本輪獨立重開上述 Commons 授權頁核對作者、授權及原圖尺寸；CLI 已保留公開信用欄。

## 最終 intake
設定 PYTHONPATH 為隔離repo apps/api後，intake_check.py 通過，正文4178字、無警告。早先未設PYTHONPATH的回退計數不作最終依據。

首次dry-run因photo清單使用URL編碼檔名報Commons notfound，改正為File:세화해수욕장3.JPG後dry-run和ingest成功。Hero220224bytes為CLI品質下限的200KB軟目標例外，低於700KB硬上限。

## 最終圖解像素覆核
已用Chrome render_svg渲染最新版並以view_image實際打開 diagram-round2.png（1600×900）。中韓字形完整、卡片和圖例沒有碰撞或裁切；原白色海岸文字對比不足，已改深色後重新渲染確認。舊左圖中的面水1路與477未標類型已和表格一致。

## 最終 CLI 結果
修正後 dry-run → ingest 成功。以四篇明確 --slug 參數及 --render-dir 執行 pack_cli lint，最終輸出 `4 entries checked`、exit 0（2026-09-20）。所有照片与SVG已實際檢視；收件至隔離repo完成，未提交、推送、部署或發布。

## 最終類型門檻修正覆核（本節取代前述五店版本）
原作者Terra修正後，本輪重新逐段獨立讀稿：477+雖有A1具名來源，卻無任何一種符合本批定義的類型，故已從推薦表、正文、FAQ、aliases、sources及SVG移除。首段殘留「村合作社空間」經本輪指出，作者亦已刪除。最終四家均有官方類型依據，沒有「未標類型」推薦店。

- 카페공작소：CNTS_000000000018312可見正文的細花海與店前拍照點支持海景/網美；新補段落的茶、小物、胡蘿蔔蛋糕沿用同頁已核實資訊。
- 카페한라산：CNTS_200000000012675可見海景與舊電視、路燈、植物、腳踏車支持海景/網美；地址維持면수1길48。
- 미엘드세화：CNTS_000000000020189可見細花海支持海景；新段落的胡蘿蔔蛋糕、汁、蘋果芒果刨冰仍有可見詳細資訊依據。
- 달치즈：CNTS_300000000015804可見濟州老屋、低矮建物外觀支持網美；窯烤麵包與咖啡可見。新段落不把구옥推成한옥，沒有加回隱藏카이막、祖母、鄉村小物。

新增三段是依四家已核實差異做選店和點餐說明，沒有新增營業時段、距離或無來源配方。四來源的最新正規化標題保留。照片與授權沿用前輪，沒有更換影像。

最終四店稿收件：intake_check.py為4店3841字4sources、無警告；dry-run→ingest成功；定向lint --render-dir輸出1 entries checked，exit0。已以view_image實看render-final/jeju-gujwa-sehwa-cafe-guide-diagram-1.png：只有四家，韓文店名/道路與中文標籤完整，無477+殘留、無裁切重疊，海岸文字對比足夠。此最終PNG取代舊五店diagram-round2.png作驗證依據。
