# seoul-yeonnam-hongdae-cafe-guide — verify-1

日期：2026-09-20

## 獨立來源與事實覆核
原撰稿與本輪查核為不同模型；本輪 Codex 逐頁重抓官方可見正文、地址、菜單、時段與標籤。快照在 codex-evidence。
- Coffee Libre：KTO 舊頁為 성미산로198；品牌現址為 성미산로32길20-5。兩頁不可拼接成新分店 A1，已從推薦、來源、表格、圖解與 aliases 全部移除。
- 替補 Polv Yeonnam：Visit Seoul 官方分店頁 PolvYeonnam/KOPoym5k2，2026-05-15 發布、05-21 更新，可見 동교로41길32一樓、10:00–21:30、派與法式吐司。咖啡師經歷不足以支持自烘或賽事標籤，未標類型。
- Overdeep：성미산로149-8，2、3樓及屋頂；三位設計師、深海主題、媒體藝術及珊瑚貝殼布置支持網美；週一休、週二至日11–21。
- Layered：성미산로161-4；歐洲住家、古董物件、窗邊及露台支持網美；每日10–22。
- Parole & Langue：성미산로29안길8；住宅改建、方形派；13–21、週一休。未將 cozy 翻成安靜。
- Antique Coffee 延南：연희로25-1一樓；花藝與古典空間支持網美；每日10–22。
- 題目、描述移除店數。刪重複入選段；沒有咖啡品質或韓屋標籤。交通不自行估距離，圖解改地址分組。

## 實際影像與授權
已以 view_image 實看 hero、photo-1 與 Chrome 渲染的 diagram-1.png。Hero 是弘大夜間霓虹步行商街，photo 是夜間路口、車輛與行人；均作區域照片，非推薦咖啡店內景。SVG 四張道路卡片清晰，中韓文字完整，無碰撞或裁切；已修復 & 字元 XML。
Hero Hongdae 1.jpg 原圖3024×4032，CLI重抓並適配1600×900，226856 bytes：工具品質下限後的200KB軟目標例外，低於700KB硬上限，不再手動縮到675px。兩張 Commons Sgroey照片的來源及 CC BY-SA 4.0 credit 由 ingest 寫入。

## 收件命令
已完成本轮修正后的 dry-run → ingest。最终 intake、定向 lint 与图解最终像素检查结果见下方补记；本记录不代表部署或发布。

## 可追溯來源清單
- 오버딥 연남: https://korean.visitseoul.net/area/x/ENP8jtxt1
- 카페 레이어드 연남점: https://korean.visitseoul.net/area/x/ENP74gju2
- 파롤앤랑그: https://korean.visitseoul.net/area/x/51091
- 앤티크커피 연남점: https://korean.visitseoul.net/area/x/ENPfru4mc
- 폴브연남 | Visit Seoul: https://korean.visitseoul.net/restaurants/PolvYeonnam/KOPoym5k2

圖像授權頁：
- https://commons.wikimedia.org/wiki/File:Hongdae_1.jpg
- https://commons.wikimedia.org/wiki/File:Hongdae_2.jpg

本輪獨立重開上述 Commons 授權頁核對作者、授權及原圖尺寸；CLI 已保留公開信用欄。

## 最終 intake
設定 PYTHONPATH 為隔離repo apps/api後，intake_check.py 通過，正文3889字、無警告。早先未設PYTHONPATH的回退計數不作最終依據。

## 最終 CLI 結果
修正後 dry-run → ingest 成功。以四篇明確 --slug 參數及 --render-dir 執行 pack_cli lint，最終輸出 `4 entries checked`、exit 0（2026-09-20）。所有照片与SVG已實際檢視；收件至隔離repo完成，未提交、推送、部署或發布。

## 類型門檻更正（最終版本優先）
前輪替補Polv雖有Visit Seoul當前分店A1頁，卻沒有足以支持網美、咖啡品質、韓屋或海景的可見文字；本批每店須有至少一個官方支持類型。因此已從正文、推薦表、來源、FAQ及SVG全部移除，不再用未標類型作推薦。最終四店為Overdeep、Layered、Parole & Langue、Antique Coffee，皆網美且有具體空間依據。新補段落為按已核實時段、空間及預約語言作實用建議，未追加店家事實；來源標題保留主協調者最新正規化值。

最終類型門檻修正後：intake 4店4077字4來源無警告；dry-run→ingest成功，定向lint輸出1 entries checked、exit0。已實看render-final/seoul-yeonnam-hongdae-cafe-guide-diagram-1.png，移除Polv後改為現場確認提示卡，中韓字可讀無裁切重疊。
