# seoul-jokbal-food-guide：第二輪獨立查核

查核日期：2026-09-20。撰稿 Sol，第一輪 Terra，本輪 Astra。從 pack 來源重新核對料理、門牌、五香分店及素材。

- [KTO 성수족발](https://english.visitkorea.or.kr/svc/contents/contentsView.do?vcontsId=51924) 明寫 `성동구 아차산로7길 7`、braised pigs' feet 與 blood sausage soup；原稿未把英文店頁沒有的韓文菜名補造出來。
- [KTO 滿足五香豬腳弘大](https://big5chinese.visitkorea.or.kr/svc/contents/contentsView.do?vcontsId=52515) 正式頁面可見 `서울특별시 마포구 동교로 191`、五香豬腳、勁辣豬腳、菜包肉、大盤麵；第一輪待核的地址已確認。原 pack 用舊路由，本輪改為可開啟的官方 canonical URL，並同步生成腳本。
- 第一輪已直接重新取得 Visit Seoul 的 `평안도 족발집`、`뚱뚱이할머니집`、`영동족발` 三個店頁，核過其店名、區域、道路及相關料理。這三頁本輪的網頁工具被 Visit Seoul 防火牆攔下，故沒有把本輪重開宣稱成功；保留第一輪可重現紀錄為資料依據。

實際檢視三張料理圖：hero 是金屬盤的切片豬腳、photo-1 是白盤切片豬腳與雙格醬料碟、photo-2 是菜包肉與豬腳併盤。修正 photo-1 的 alt，由「一碟醬料」改為可見的雙格醬料碟；圖說沒有冒稱拍攝於文中店家。把 `diagram-1.svg` 以 Chrome 渲染為 1600×900 PNG，韓文／中文和兩欄內容清晰、未截斷；菜名與一起上桌的搭配品有區分。圖片來源、作者、授權已由第一輪記在 manifest。

結論：KTO 官方來源支持受檢兩店的門牌和菜色；三個 Visit Seoul 店頁在第一輪可查，本輪因網站防火牆限制無法獨立再查。整批 lint 另記於總驗收紀錄。
