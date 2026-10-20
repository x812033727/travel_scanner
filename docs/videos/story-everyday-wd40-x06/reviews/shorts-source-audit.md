# X06 兩支精華 Shorts｜獨立來源複核

2026-10-20；`shorts.json` SHA-256：`d4c0795abdcd1bea197bee729eba0fb70c80703b1fb2f4fb9956731677bd6773`。**離線腳本 PASS**；此結論不代替日後配音、關鍵影格、成片及 Shorts 品管。撰稿者完成初稿後，由另一代理逐句對照 `source-notes.md` 與下列 SEC 原件；長片 `video.json` 仍綁定 `4c9215b06364b3fb96cd9249054c6e7c15de381b4e8717a39a11fb9ad62bf1ba`。

| 腳本 | 原件與可說範圍 | 結果 |
| --- | --- | --- |
| `short-1` | [FY1995 10-K](https://www.sec.gov/Archives/edgar/data/105132/000089843095002264/0000898430-95-002264.txt) 證明收購前已有海外子公司銷售與出口；[FY1997 10-K](https://www.sec.gov/Archives/edgar/data/105132/000101706297002143/0001017062-97-002143.txt) 明說 1995-12-08 收購 3-IN-ONE 相關資產，取得 17 國既有網絡，並有選擇地將 3-IN-ONE 導入公司原有通路；[FY2008 10-K](https://www.sec.gov/Archives/edgar/data/105132/000119312508214535/d10k.htm) 明說網絡後來確實把 WD-40 引入原未販售的市場。腳本將原有海外銷售與新取得入口分開，沒有把全部海外業績歸因於收購。 | PASS，11 句口播及標題／說明一致。 |
| `short-2` | [FY2025 10-K](https://www.sec.gov/Archives/edgar/data/105132/000010513225000067/wdfc-20250831.htm) 寫 EIMEA 家清已完成出售，美洲家清當時正積極求售、目標 FY2026；[2026 Q3 10-Q Note 3](https://www.sec.gov/Archives/edgar/data/105132/000010513226000061/wdfc-20260531.htm) 寫 2026 年 4 月美洲品牌不再主動求售，改保留營運並由 `held for sale` 改列 `held for use`。腳本的「改決定只談美洲」限定正確，沒有把 EIMEA 已售業務說成一起留下。 | PASS，11 句口播及標題／說明一致。 |

兩支各有六個順序正確的 beat，所有 `shot` ID 都指向當前 X06 長片的一張 `shot`；Shorts 只重用計畫中的長片鏡頭，還沒有真實關鍵影格。逐支抽出為單一 JSON 後使用原生 `tools/video/shorts/cli.mjs validate --file`，兩支均通過。正式製作須以實際長片關鍵影格 hash 重新驗證，量測 25–55 秒，且不得把本收據視為發布核准。
