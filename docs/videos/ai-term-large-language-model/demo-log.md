# 六筆失物：可重跑離線示範

執行日期：2026-10-04。工具 `Python 3.14.6`。全部資料與人物虛構；沒有真實失主、電話、網路、帳號或模型呼叫。這不是語言模型實測。

在此資料夾執行 `python demo.py data`、`python demo.py evidence`、`python demo.py missing`、`python demo.py count`，或 `python demo.py all` 重跑全部檢查。每種情況都包含資料不變量的斷言；失敗時程式退出，不能把預期輸出當作實際通過。

## 原始資料

| 代號 | item | location | status |
| --- | --- | --- | --- |
| L001 | umbrella 雨傘 | north_counter 北側櫃台 | unclaimed 未領 |
| L002 | bottle 水瓶 | east_shelf 東側層架 | returned 已領 |
| L003 | umbrella 雨傘 | west_basket 西側籃子 | unclaimed 未領 |
| L004 | scarf 圍巾 | south_hook 南側掛鉤 | unclaimed 未領 |
| L005 | cap 帽子 | east_shelf 東側層架 | returned 已領 |
| L006 | glove 手套 | west_basket 西側籃子 | unclaimed 未領 |

資料沒有 owner_name 或 owner_phone。保存「已領」的歷史列，為的是讓觀眾看見只數未領時必須篩選。

## 一、有據的查找：逐字實際輸出

```text
> python demo.py evidence
fictional_data=true; model_called=false
L001 | umbrella | north_counter | unclaimed
```

這支持 L001 雨傘在北側櫃台、狀態未領。它不支持任何訪客是失主，不代表電話或姓名已確認。

## 二、缺資料：逐字實際輸出

```text
> python demo.py missing
record=L001; field=owner_phone
result=UNKNOWN; reason=field_not_in_dataset
```

這支持「本份資料無法回答失主電話」。它不支持世界上沒有電話，也沒有執行外部搜尋。

## 三、工具計數：逐字實際輸出

```text
> python demo.py count
records=6; returned=2; unclaimed=4
unclaimed_ids=L001,L003,L004,L006
unclaimed_umbrellas=2; ids=L001,L003
```

條件一是 `status == 'unclaimed'`，得到四筆；條件二是在這四筆中再選 `item == 'umbrella'`，得到兩筆。回傳參與計數的代號，所以能從清單逐筆核對。

## 實驗邊界

`demo.py` 是確定規則程式，不是語言模型。紀錄與錯誤文字皆由作者撰寫。沒有送任何問題給模型，沒有測過幻覺率、生成效果、提示詞有效率或模型成本。這次成功只證明所附資料和指定程式的三個結果一致。

畫面「王先生已領走北側櫃台的雨傘」是編輯故意製作的錯誤示意，須帶「錯誤示意，非模型輸出」標記。它新增姓名並把未領改已領，兩點都不能從原始清單支持。最後答案可以由模型生成文字；有資料或工具回傳不會讓那段文字變成另一種互斥能力。
