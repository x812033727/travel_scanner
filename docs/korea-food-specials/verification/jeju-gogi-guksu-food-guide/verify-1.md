# 濟州肉湯麵：第一輪獨立查核

查核日期：2026-09-20。由不同於撰稿者的模型重新開啟五家 Visit Jeju 官方店家頁，比對每一個逐店段落、圖片與圖解；第二輪獨立查核仍待執行。

## 五店官方頁核對

| 店家 | 官方頁可見證據 | 審稿結果 |
|---|---|---|
| 올래국수 본점 | [Visit Jeju](https://www.visitjeju.net/kr/detail/view?contentsid=CNTS_000000000020099)：本店、귀아랑길 24、單一 고기국수 菜單、豬骨湯／中麵／肉、無專用停車場、櫃檯點餐與結帳。 | 稿件與門牌、菜單、停車描述相符。 |
| 삼대국수회관 본점 | [Visit Jeju](https://www.visitjeju.net/kr/detail/view?contentsid=CNTS_000000000020813)：本店、삼성로 41、三姓穴國수街、肉／粗麵／湯、海苔與調味醬。 | 稿件未自行推定確切營業鐘點。 |
| 국수마당 본점 | [Visit Jeju](https://www.visitjeju.net/kr/detail/view?contentsid=CNTS_000000000019644)：本店、삼성로 65、고기국수、비빔고기국수、멸치국수、몸국、돔베고기、아강발。 | 與삼대國수會館同路不同門牌，稿件已分清。 |
| 골막식당 | [Visit Jeju](https://www.visitjeju.net/kr/detail/view?contentsid=CONT_000000000501163)：천수로 12、豬骨與鯷魚湯底、粗麵及豬肉。 | 魚成分提醒有官方依據；未套用別店湯底。 |
| 국수바다 서귀포본점 | [Visit Jeju](https://www.visitjeju.net/kr/detail/view?contentsid=CNTS_000000000020207)：西歸浦本店、일주서로 580、店內自製生麵、湯頭熬煮超過 12 小時、오겹살。 | 將原稿「自行揉麵」縮為「店內自製生麵」，因官方明寫自製與現場拉麵，未明寫手揉動作；未把오겹살推成黑豬。 |

## 視覺、授權與收件

- 已開啟隔離 repo 實際 `hero.jpg`、`photo-1.webp`，與文字 alt 相符：前者筷子夾肉和麵、下方白色湯碗；後者白碗裡有肉、麵、海苔、蔥圈及紅色調味料。照片只當料理示意，未指認本文五家之一。
- [Commons hero](https://commons.wikimedia.org/wiki/File:%EC%A0%9C%EC%A3%BC%EB%8F%84_%EA%B3%A0%EA%B8%B0%EA%B5%AD%EC%88%98_12.jpg) 註作者 채지형、CC BY 4.0、原圖 5616×3744；[Commons photo-1](https://commons.wikimedia.org/wiki/File:Gogi-guksu.jpg) 註作者 신동혁、CC0、原圖 6000×4000。匯入後檔案分別 192912、60716 bytes。
- 已目視工作目錄渲染的 `diagram-1.png`：三欄「完整菜名／湯底與麵條／城市與門牌」可讀，與正文一致；SVG 也經 ingest 驗證。
- 修正後 `intake_check.py`：5 店、3800 字，無警告；`pack_cli ingest --dry-run` 成功，並已重新 ingest 隔離 repo。

## 留給第二輪

官方頁中某些舊介紹與新「詳細資訊」並存，且有時段、停車資訊會變動；本稿未替出發日保證。第二輪應再看完整文章與引用欄是否仍逐句對應。本輪另跑定向 pack_cli lint --slug jeju-gogi-guksu-food-guide，exit 0：1 entries checked。
