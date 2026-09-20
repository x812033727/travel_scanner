# jeju-aewol-cafe-guide — verify-2

日期：2026-09-20

## 獨立第二輪
原作者 Terra，首輪 Astra；本輪 Codex 重新取得4頁原始HTML與可見正文，保存codex-evidence。本輪讀取排除head/script/style/noscript、hidden/aria-hidden/display:none及#__SEARCH_DATA__，不用隱藏SEO payload或遊客評價作事實依據。
- 더선셋：일주서로6111，官方可見正文有室內、戶外露台、涯月海與夕陽；刪掉先前混入的折疊門與整面玻璃窗。保留海景及露台空間網美；餐點僅據可見詳細資訊。
- 봄날：애월로1길25，海景、石牆、한담散步路、巴士站步行約5分鐘與停車擁擠可見。刪掉未逐張確認官方圖片的黃色陽傘說法；沒有公開固定時段。
- 전당포：애월로117，可見手沖選豆、復古空間、底片/拍立得租借、操作與沖印課程。刪掉隱藏資料的品質好豆與五種手沖；不標咖啡品質。
- 노을리：애월해안로654，可見海景、植物園般室內與具名麵包飲品，海景/網美成立。
- 所有店均政府觀光具名分店A1；固定時段與公休不從隱藏利用資訊欄抄出。

## 圖像與授權
hero與photo均已實際看圖：hero為灰雲、海水與黑色岩岸；photo為한담海岸步道、黑色岩岸與行人，不是咖啡店內景。
重新開啟Commons來源頁確認：Aewol in Jeju.jpg原圖4032×3024，Jeong seolah，CC0；Jeju Olle Route 15-B.jpg原圖2237×1600，Jeju Olle Foundation，CC BY-SA4.0。來源與作者已入credit。Hero由CLI適配1600×900。SVG為Mokaair原創。

## 收件命令
已完成本轮修正后的 dry-run → ingest。最终 intake、定向 lint 与图解最终像素检查结果见下方补记；本记录不代表部署或发布。

## 可追溯來源清單
- Visit Jeju：애월더선셋（涯月海、日落、海景與地址）: https://www.visitjeju.net/kr/detail/view?contentsid=CNTS_000000000018299
- Visit Jeju：봄날（海邊景觀、濟州石牆與地址）: https://www.visitjeju.net/kr/detail/view?contentsid=CNTS_000000000018337&menuId=DOM_000001818000000000
- Visit Jeju：애월 전당포（底片相機、手沖、選豆與地址）: https://m.visitjeju.net/kr/detail/view?contentsid=CNTS_300000000013384
- Visit Jeju：노을리（看海、植物園般室內與地址）: https://www.visitjeju.net/kr/detail/view?contentsid=CNTS_300000000015617

圖像授權頁：
- https://commons.wikimedia.org/wiki/File:Aewol_in_Jeju.jpg
- https://commons.wikimedia.org/wiki/File:Jeju_Olle_Route_15-B.jpg

本輪獨立重開上述 Commons 授權頁核對作者、授權及原圖尺寸；CLI 已保留公開信用欄。

## 最終 intake
設定 PYTHONPATH 為隔離repo apps/api後，intake_check.py 通過，正文3845字、無警告。早先未設PYTHONPATH的回退計數不作最終依據。

## 最終圖解像素覆核
已用Chrome render_svg渲染最新版並以view_image實際打開 diagram-round2.png（1600×900）。中韓字形完整、卡片和圖例沒有碰撞或裁切；原白色海岸文字對比不足，已改深色後重新渲染確認。舊左圖中的面水1路與477未標類型已和表格一致。

## 最終 CLI 結果
修正後 dry-run → ingest 成功。以四篇明確 --slug 參數及 --render-dir 執行 pack_cli lint，最終輸出 `4 entries checked`、exit 0（2026-09-20）。所有照片与SVG已實際檢視；收件至隔離repo完成，未提交、推送、部署或發布。
