# 延南／弘大咖啡：第二輪獨立查核

查核日期：2026-09-20。Sol 模型獨立於 Terra 撰稿及 Astra 首輪查核，重新開啟 Visit Seoul 官方頁、兩個 Commons 授權頁，目視隔離 repo 圖片；最終 SVG 渲染及 CLI 結果記在下方。

## 類型門檻與四店

初稿替補的 [폴브연남](https://korean.visitseoul.net/restaurants/PolvYeonnam/KOPoym5k2) 確有 2026-05-15 製作、05-21 更新的具名官方頁，`동교로 41길 32 1층`、10:00–21:30、派與法式吐司均可見。可是頁面沒有能支持本批「網美／咖啡品質／韓屋／海景」任一類型的具體證據：咖啡師有歐洲經歷不等於自家烘焙或賽事資歷，櫻花路位置也不等於店內空間特色。按照 README 每家咖啡店須有官方支持類型的門檻，Astra 已將 Polv 從最終 pack 的表格、逐店段落、來源、圖解與 aliases 移除；也沒有恢復舊地址衝突的 Coffee Libre。

最終四個官方店家頁另行直接重新抓取，皆 HTTP 200。`verify2_fetch.py` 留有抓取腳本與當時五頁的輸出方式；其 Polv 請求僅作排除判斷，非最終入選店。四個逐店段各自有官方頁及 Naver 連結。

| 店家 | 官方可見文字 | 本輪判斷 |
|---|---|---|
| [오버딥 연남](https://korean.visitseoul.net/area/x/ENP8jtxt1) | `성미산로 149-8`、2/3 樓與屋頂，週二至日 11:00–21:00、週一休，深海主題與拍照空間。 | 網美標籤有具體空間文字；不是海景。 |
| [카페 레이어드 연남](https://korean.visitseoul.net/area/x/ENP74gju2) | `성미산로 161-4`、每日 10:00–22:00，歐式家屋風格、古董及甜點。 | 網美標籤有來源，沒有誤作韓屋。 |
| [파롤앤랑그](https://korean.visitseoul.net/area/x/51091) | `성미산로29안길 8`、13:00–21:00、週一休，住宅改建及方形派。 | 網美僅依住宅改建；未推成安靜或品質認證。 |
| [앤티크커피 연남점](https://korean.visitseoul.net/area/x/ENPfru4mc) | `연희로 25-1 1층`、每日 10:00–22:00，花藝／古典室內與甜點。 | 網美標籤有空間依據，專業 barista 不被當成自烘證據。 |

最終總表四列、逐店四段與 SVG 的道路門牌一致，四家均標有「網美」且各有官方具體空間文字。沒有咖啡品質、韓屋或海景標籤。

## 圖片、圖解與授權

- 隔離 repo hero 已目視：弘大夜間步行商圈霓虹招牌與行人；photo-1 是夜間道路、路口與車輛。兩者均是區域示意，沒有冒充五家店內景；alt 與畫面相符。
- [Commons Hongdae 1](https://commons.wikimedia.org/wiki/File:Hongdae_1.jpg) 與 [Commons Hongdae 2](https://commons.wikimedia.org/wiki/File:Hongdae_2.jpg) 均記載作者 Sgroey、CC BY-SA 4.0，原圖分別 3024×4032、4032×3024；隔離 repo pack 由 ingest 保留 credit。
- 已目視最終 `render-final/seoul-yeonnam-hongdae-cafe-guide-diagram-1.png`：四張卡片中三張列四家門牌，左下卡片是「現場確認」提示，Polv 及其道路已移除；中韓文字均可讀，未見裁切或重疊。圖明說地址分組不代表方向、距離或步行先後，與正文一致。

## 收件結果及限制

- 初版五店時 `intake_check.py` 為 3889 字、dry-run 與定向 lint 通過，但 Polv 類型門檻未過；這些舊結果不作為最終包的完成證據。修正後我獨立重跑 `intake_check.py`，**4 店、4077 字**、exit 0、無警告；Astra 對最終包重跑 dry-run→ingest 與定向 `pack_cli lint`，exit 0：`1 entries checked`。hero 226856 bytes 略高於 200000 bytes 指引，低於硬上限，匯入器已在品質下限。
- 官方營業時間僅反映 2026 年 9 月可見頁；出發日仍須查商家公告。本輪不聲稱部署或發布。
