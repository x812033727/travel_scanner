# 大邱烤腸：第二輪獨立查核

查核日期：2026-09-20。此輪由 Sol 模型獨立於 Astra 撰稿及 Terra 首輪查核執行；以 pack 四個店家 URL 直接重新取得大邱市官方 HTML、另開 Commons 授權頁，並實際目視隔離 repo 的圖片與工作目錄 SVG 渲染圖。

## 分店、門牌與豬牛

官方頁透過 Python `urllib.request` 直接請求四頁，各回 HTTP 200、UTF-8；web 擷取器無法開啟此站，故以直接請求為本輪可重現證據。查核腳本與關鍵字節錄在同資料夾 `check_official.py`。

| 官方分店頁 | 可見店名、門牌及菜單 | 稿件結果 |
|---|---|---|
| [팔공막창 idx 1603](https://www.daegufood.go.kr/kor/food/food.asp?idx=1603&gotoPage=1&snm=9&ta=5) | `팔공막창`，中區 `동성로6길 46 (공평동)`；菜單有 `팔공막창`、`생막창`，未逐一標豬牛。 | 保留「先問原料」，未以店名、照片猜豬牛。 |
| [딱조아막창 idx 758](https://www.daegufood.go.kr/kor/food/food.asp?idx=758&gotoPage=1&snm=9&ta=5) | `딱조아막창`，北區 `대불서길 58-1 (산격동)`；明列 `돼지막창` 與 `불양념돼지막창`。 | 豬類標示與分店地址相符。 |
| [동봉(범어점) idx 743](https://www.daegufood.go.kr/kor/food/food.asp?idx=743&gotoPage=1&snm=9&ta=5) | 標題點名 `동봉(범어점)`，壽城區 `범어천로 128 (범어1동)`；明列 `소막창구이`。 | 牛類標示與範魚分店相符，未把午餐定食等同烤腸全天供應。 |
| [성주막창 idx 856](https://www.daegufood.go.kr/kor/food/food.asp?idx=856&gotoPage=1&snm=9&ta=5) | `성주막창`，達西區 `상화로 73 (진천동)`；正文說真泉為第二店。 | 未借用大明洞本店地址；`생막창`／`양념막창`未推定豬牛。 |

KTO 繁中料理頁只作通用豬大腸頭介紹；文章沒有將其套到牛막창或未標原料的店。四家店的品牌、門牌、豬牛用語未見混用。

## 視覺與授權

- 已目視隔離 repo `hero.jpg`：金屬烤網上的切塊烤腸、網下火光，alt 相符。[Commons 原檔](https://commons.wikimedia.org/wiki/File:Makchang.jpg) 註作者 채지형、CC0、原圖 5069×3379。
- 已目視 `photo-1.webp`：抽風管下的烤網、橘褐色烤腸、周圍碗盤，alt 相符。[Commons 原檔](https://commons.wikimedia.org/wiki/File:Makchang-gui.jpg) 註作者 Michael Sean Gallagher、CC BY-SA 2.0、原圖 2592×1936。Commons 稱該照片為牛烤腸，但本文只用作烤腸示意，也明說照片不能推定四店原料，沒有圖片與商家錯誤連結。
- 已目視 `diagram-1.png`：三欄「原料／調味／上桌後烤法」均可讀、無裁切或重疊；`돼지막창→豬`、`소막창→牛`、單寫 `막창` 先詢問，以及 `양념막창` 為調味版的文字與本文一致。

## 結果與限制

第一輪紀錄稱未執行 dry-run/ingest/lint；作者後續筆記有收件與定向 lint 記錄，且隔離 repo 內容與資產實際存在。本輪不把兩者混成第一輪驗證。定向 pack_cli lint --slug daegu-makchang-food-guide 本輪 exit 0：1 entries checked。營業時間、價格和供應仍需出發日重查；本輪不對商家營業現況作保證。
