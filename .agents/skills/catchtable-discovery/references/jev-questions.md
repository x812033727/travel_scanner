# Jev 在這條管線的四題（第二階段）

Jev（`apps/api/app/ai/jev.py`）只做判斷：`choice` 選一個、`score` 放在量表上、`noul` 回一個陳述為真的
機率；每個答案帶校準過的信心。`route_answer` 依全站設定把答案分成 act／confirm／hold
（`jev_act_confidence` 0.9、`jev_flag_confidence` 0.5）。`JEV_CJK_AUTOPILOT_ENABLED` 關著時，非英文
state 的 act 一律降成 confirm——所以現階段 Jev 只排序與標旗，人做最後一下。

程式落點是票 `2026-09-22-catchtable-import-and-jev`。在它落地前不要寫一次性腳本去改判定。

## 不問的

名次、價格、營業時間、日期先後、數量（TypeSafe 公布的弱點：日期當文字讀、不是計算機、分數校準弱），
以及「這家店紅不紅」——我們不做排名。

## 四題

| 題 | 型別 | 何時問 | state 放什麼 | 答案怎麼用 |
| --- | --- | --- | --- | --- |
| 同店 | `noul` | 去重時，名稱正規化後相似或地址同路的配對 | 兩邊的韓文名、道路名地址、區域、CatchTable 的 alias | ≥ act 才當 `duplicate`；confirm 進人工清單；hold 視為不同店但記下 |
| 分類 | `choice`（18 個 slug，criteria 用英文說明） | 每筆 `import` | 韓文店名、CatchTable 料理類型、官方頁一句描述 | 建議主分類；人確認後才寫 `category_slugs[0]` |
| 商圈 | `choice`（該城市的 area key，criteria 帶韓文與英文） | 地址對不到 `area_catalog` 的 `terms` 時 | 道路名地址 | 建議 `district_key`；人確認 |
| 本店 | `noul` | 找到官方頁之後 | 官方頁標題與前幾百字、店名、地址 | 低於 flag 直接退回重找來源；其餘人看 |

### 問法（照 `app.ai.jev` 的模型）

```python
from app.ai.jev import ChoiceQuestion, NoulQuestion

state = {
    "candidates": [
        {
            "id": "daelimchanggobar",
            "local_name": "대림창고 다이닝 & 바",
            "listed_cuisine": "餐酒館",
            "listed_address": "서울 성동구 성수이로 78",
            "official_excerpt": "…官方頁前幾百字…",
        }
    ],
    "catalog_match": {"slug": "seoul-daerimcanggo", "local_name": "대림창고", "address": "서울 성동구 성수이로 78"},
}
questions = {
    "daelimchanggobar:same": NoulQuestion(
        instructions="Candidate daelimchanggobar and catalog_match are the same restaurant branch, not two venues at one address."
    ),
    "daelimchanggobar:category": ChoiceQuestion(
        instructions="Which category best describes candidate daelimchanggobar?",
        criteria={"izakaya-bar": "bars, wine bars, pubs", "fine-dining": "tasting-menu restaurants", "home-style": "everyday Korean set meals", "bbq-grill": "grilled meat", "hotpot-soup": "soups and stews"},
    ),
    "daelimchanggobar:official": NoulQuestion(
        instructions="official_excerpt of candidate daelimchanggobar describes this specific branch (same name and address), not the brand or another branch."
    ),
}
```

- 問題名以 alias 為前綴，一批候選放同一個 state；`JevRequestTooLarge` 就對半切，照
  `app/hotspots/ai_search.py` 的 `_jev_shadow_assessment` 做。
- 每次呼叫先過 `consume_jev_call`（每日 `jev_daily_call_budget`，預設 200）；一批 30 家是個位數呼叫。
- state 只放店名、地址、料理、官方頁摘錄；不放任何人的身分、不放整頁 HTML。
- 分類的 criteria 用英文寫（TypeSafe 說英文最準），選項就是 `category_catalog.py` 的 slug。

## 影子量測，再放手

1. 第一批全部由人判，候選檔就是基準。
2. 落地後跑報告指令：讀候選檔，問四題，印每筆「Jev 答案／tier／人的判定／是否一致」，什麼都不寫。
3. 每題分開算 agreement（整體與分語言，照 `app/hotspots/guide_shadow_cli.py` 的算法），不一致的逐筆看：
   一個方向錯得特別多，比整體百分比重要。
4. 分類與商圈是低風險欄位（分類只增、商圈是瀏覽提示），agreement 夠才值得為它們開
   `JEV_CJK_AUTOPILOT_ENABLED`；同店與本店這兩題關係到「寫錯一家店」，維持 confirm。
5. 門檻用全站設定，不另開一套；要改就改設定並把數字寫進票。

TypeSafe 只計輸入 token（`guide_shadow_cli.py` 記的是每百萬 0.042 美元），一批的成本可以忽略；
真正的成本是人看 confirm 清單的時間，所以報告要把 confirm 的筆數印出來。
