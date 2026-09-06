---
id: 2026-09-06-merchant-english-names-unsourced
title: 15 個店家英文名是手寫音譯，查不到出處
status: done
priority: P2
area: api
owner: claude-opus-5
claimed_at: 2026-09-06T21:52:35Z
created_at: 2026-09-06T21:43:25Z
completed_at: 2026-09-06T21:57:58Z
branch: claude/merchant-names-sourced
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

- [x] 15 筆逐家查一個可引用的出處（店家官網、官方觀光頁、Google Places 的 `displayName`），
      把出處記進這張任務。
- [x] 查得到的，把 `name_en` 換成出處上的寫法（多半不用改）。
- [x] 查不到的，把 `name_en` 拿掉，讓那一家退回招牌原文——原票第 3 類的處理方式。
- [x] `test_trend_import.py` 加一條：`name_en` 若不在該列的 `name_zh`／`local_name` 裡，
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

## Result（2026-09-07）

**我開這張票時的判準有一半是錯的。** 我用「這個英文名不在該列自己的資料裡」當成「憑空編的」，
逐家查過之後，15 筆裡有 8 筆其實查得到出處——那個判準只是個代理指標，不是證據。

逐家對它自己引用的來源查證的結果：

| 留下（查得到出處） | 出處 |
| --- | --- |
| Shirogane Sabo | s-sabo.com 頁尾「Copyright © SHIROGANE SABO」 |
| Kawamotoya | kawamotoya.com 站上的羅馬字，也是網域名 |
| Tsuruya Yoshinobu Main Store | tsuruyayoshinobu.jp 頁尾「Tsuruya Yoshinobu CO., LTD.」 |
| Shokudo faidama | faidama.com 寫「faidama」，IG 帳號是 shokudou_faidama |
| HATTIFNATT Koenji ／ manu coffee Daimyo ／ oHacorté Minatogawa ／ Houkiboshi Minatogawa | 品牌本來就在該列裡，只有分店名轉成羅馬字，而那是地名 |

| 移除（來源上一個拉丁字都沒有） | 查了什麼 |
| --- | --- |
| Harajuku Gyozaro | 該列引用的官方頁全篇只有「原宿餃子楼」 |
| Ganso Curry Tantanmen Masatora | curry-tantan.com 只有振假名 まさとら，沒有羅馬字店名 |
| Dongqu Fenyuan | efy.com.tw 全站沒有任何拉丁字店名 |
| Jin De Spring Rolls | 台南觀光官方頁只有「金得春捲」 |
| Xiu An Do Hua | 同上，只有「修安扁擔豆花」 |
| Tai Cheng Fruit Shop | 同上，只有「泰成水果冰店」 |
| Hao Shuang Huangpu | 高雄眷村官方頁只有「蠔爽 黃埔總店」 |

**分界線很乾淨**：日本店家的自家網站幾乎都在頁尾或網域寫了自己的羅馬字；台灣的官方觀光頁
一個都沒有。那七筆退回招牌原文，也就是原票第 3 類的處理方式——英文讀者拿到 `東區粉圓` 貼進
地圖找得到那家店，拿到 `Dongqu Fenyuan` 多半找不到。

新的守門測試 `test_an_english_name_not_in_its_row_has_a_recorded_source`：`name_en` 若不在
該列的資料裡，就必須列在 `SOURCED_ENGLISH_NAMES`，而清單每一筆旁邊都有出處註解。
另一條測試防清單放到爛掉（列了資料檔已經沒有的 slug）。破壞測試驗過會失敗。

沒有用 Google Places：資料庫裡沒有快取的官方名稱（`restaurant_places` 只存 ID），
要拿就得花配額，而店家自己的網站是更直接也免費的出處。
