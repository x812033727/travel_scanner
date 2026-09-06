---
id: 2026-09-06-merchant-english-names-unsourced
title: 15 個店家英文名是手寫音譯，查不到出處
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-09-06T21:43:25Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/foods/data/trend_merchants.json
  - apps/api/tests/test_trend_import.py
---

# 15 個店家英文名是手寫音譯，查不到出處

## Why

`2026-09-06-merchant-names-chinese-in-other-locales` 的 Steps 明文寫著：

> 第 1 類用店家官網或官方觀光頁上的羅馬字招牌（`local_name` 通常已經有），**不要自己音譯**。

而且它把 `白金茶房`、`食堂faidama` 列為第 3 類「這些不該動」。

PR #285 補的 28 個 `name_en` 裡，有 **15 個在該列自己的 `name_zh` 與 `local_name` 裡完全找不到**，
也就是憑空寫出來的羅馬字：

| slug | name_en | 該列有的資料 |
| --- | --- | --- |
| taipei-dong-qu-fen-yuan | Dongqu Fenyuan | 東區粉圓 |
| tainan-xiu-an-bian-dan-dou-hua | Xiu An Do Hua | 修安扁擔豆花 |
| tainan-jin-de-chun-juan | Jin De Spring Rolls | 金得春捲 |
| tainan-tai-cheng-shui-guo-bing-dian | Tai Cheng Fruit Shop | 泰成水果冰店 |
| kaohsiung-hao-shuang-huang-bu-zong-dian | Hao Shuang Huangpu | 蠔爽 黃埔總店 |
| fukuoka-bai-jin-cha-fang | Shirogane Sabo | 白金茶房 |
| okinawa-faidama | Shokudo faidama | 食堂faidama |
| yokohama-chuan-ben-wu-cha-pu | Kawamotoya | 川本屋茶舖 |
| osaka-kyoto-he-wu-ji-xin-ben-dian | Tsuruya Yoshinobu Main Store | 鶴屋吉信 本店 |
| tokyo-yuan-su-jiao-zi-lou | Harajuku Gyozaro | 原宿餃子樓 |
| yokohama-yuan-zu-...-zong-ben-dian | Ganso Curry Tantanmen Masatora | 元祖カレータンタン麺 征虎総本店 |
| okinawa-houkiboshi | Houkiboshi Minatogawa | Houkiboshi ／ 港川本店 |
| okinawa-ohacort | oHacorté Minatogawa | oHacorté 港川本店 |
| fukuoka-manu-coffee | manu coffee Daimyo | manu coffee 大名店 |
| tokyo-hattifnatt | HATTIFNATT Koenji | HATTIFNATT 高円寺のおうち |

**不是每一筆都一樣嚴重。** 最後四筆只是把分店名從漢字換成羅馬字（`大名店`→`Daimyo`、
`港川本店`→`Minatogawa`），品牌名本來就在資料裡，風險低。前面那些是整個店名的音譯，
而那正是原票要擋的事：一個英文讀者把 `Dongqu Fenyuan` 貼進 Google 地圖，多半找不到那家店；
`東區粉圓` 至少找得到。

這不是主張那些音譯是錯的——`Tai Cheng Fruit Shop` 有可能就是店家官網用的寫法。
問題是**從資料裡看不出來有沒有出處**，所以沒有人能複查。

## Definition of done

- [ ] 15 筆逐家查一個可引用的出處（店家官網、官方觀光頁、Google Places 的 `displayName`），
      把出處記進這張任務。
- [ ] 查得到的，把 `name_en` 換成出處上的寫法（多半不用改）。
- [ ] 查不到的，把 `name_en` 拿掉，讓那一家退回招牌原文——原票第 3 類的處理方式。
- [ ] `test_trend_import.py` 加一條：`name_en` 若不在該列的 `name_zh`／`local_name` 裡，
      就必須列在一份「已查證」的允許清單，且清單每一筆都要有出處註解。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_trend_import.py -q
```

## Notes

- 這 121 家裡有 74 家已經有 `google_place_id`，Google Places 的 `displayName` 就是官方英文名，
  不用自己音譯也不用一家一家開網站。這是最省事的出處。
- 部署與資料都已經上線了（正式站已發布的店家 `name` 含漢字的是 0 筆），所以這張票是回頭補查證，
  不是修壞掉的東西。
- 發現方式：跑 `backfill-merchant-english-names` 的 dry-run 時看到清單裡出現資料檔沒有的字串。
