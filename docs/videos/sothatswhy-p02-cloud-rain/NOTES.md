# sothatswhy-p02-cloud-rain 製作紀錄

企劃：[`../so-thats-why/dialogue-pilot-20261103/README.md`](../so-thats-why/dialogue-pilot-20261103/README.md)。任務：`tasks/open/2026-11-03-sothatswhy-dialogue-pilot-p02.md`。

## 稿子怎麼產生

`video.json` 的 `scenes` 與 `loops` 由 [`build_scenes.py`](build_scenes.py) 產生（`python3 build_scenes.py body.json` 再併回 `video.json`），改台詞改這支檔再重產，
不要只改 `video.json`，不然下次重產會被蓋掉。其他欄位（角色、聲音、youtube、sources）直接寫在 `video.json`。

## 2026-11-03

- **撰稿**：7 章、131 句、104 張插圖、13 張卡片，小問約 24% 字數，lint 估 11.9 分鐘、0 錯誤。
- **查核**（另一個代理，[`verify-1.md`](verify-1.md)）：31 條主張 27 OK、4 FIX、0 CUT，另 9 處標題、縮圖、卡片修改；全部已照改。
  打不開的來源（AMS 詞彙 403、UCAR cloud weight 404、NASA GPM FAQ 503）沒有引用。夏威夷大學教科書的 `pressbooks-dev` 網址從 `sources` 拿掉，同書以 LibreTexts 版本列。
- **盲評**（兩位互不相干的新讀者，只讀 `narrative` 的文字稿）：
  - 第 1 輪 7/13（[`review/narrative-round1.json`](review/narrative-round1.json)）：片尾重述、「第一件／第二件」「三件事」清單、重複數字、章名是功能、一小時的回收沒點名、雨滴形狀是岔題。全改：拿掉重述與編號、第五章改成小問在陽台實況看到花椰菜頂→砧狀頂→涼風、章名改成事件。
  - 第 2 輪 9/13（[`review/narrative-round2.json`](review/narrative-round2.json)）：開場問句先講了「一小時內大雨」、片尾兩句重述、開場只有兩個鉤子、雨滴形狀仍像岔題。已照改（開場改成「幾頭大象重」「會不會下、要多久」兩個預告；片尾改成點名回呼；雨滴形狀接回「空氣擋住往下掉的東西」與「雨滴不會一直長下去」）。
  - 規則是最多兩輪，**第三輪交站主判**：改後的稿還沒有新讀者讀過。
- **已知不改的警告**：有角色的影片會套漫劇的 `craft` 節奏警告（鏡頭中位數 2.5–3.5 秒、一句 12 字內），那是戲劇的目標；解說的所長長句照奇聞旁白的節奏，不為了消警告切碎。「girl」出現在一半的插圖，是因為小問兼任內容插圖裡的那「一個人」（企劃 §3）。
