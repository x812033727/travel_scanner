# S46 R14｜三景試畫提示詞定點修正

2026-10-20 UTC。[首輪原生圖驗收](r14-art-pilot-native.md)的 `bkw002,bkw006,bkw007` 為 **0/3 KEEP**；首輪圖及機器評審已花 **US$0.0405**。依[預先訂定的試畫門檻](r14-art-pilot-plan.md)，這次僅修三個 `video.json` 的 `data.prompt`；沒有再呼叫付費圖片、配樂、語音或成片服務。第二輪原生圖、獨立裁決與其餘 107 景均尚未開始。

| 景 | 原提示詞 | 修正後提示詞與針對的原生錯誤 |
| --- | --- | --- |
| `bkw002` | `Close shot at a wooden writing table, one lady in a plain 1840s dress turns the sealed envelope in her hand, mild overcast light` | `Close shot at an 1840s American wooden writing table, one adult woman in her late twenties wearing a high-necked long-sleeved Victorian dress turns a small sealed blank envelope to see its triangular flap, mild overcast light`。明寫成年與維多利亞時代洋裝，並以可見封口和三角封舌限定信封，針對首輪東亞式衣裝與未封平紙。 |
| `bkw006` | `Wide shot in a 1840s college lecture room, one female reader in an 1840s coat waits beside a lecture room door, soft window light` | `Wide establishing shot from inside an 1840s medical college lecture hall, curved empty wooden benches leading toward an open doorway, one adult woman in her late twenties wearing a full-length high-necked Victorian dress waits just beyond it, soft window light`。把鏡頭位置與講堂長椅列為主體空間，明寫成年與長裙，針對首輪學生感近景、講堂不可辨。 |
| `bkw007` | `Medium shot in a plain 1840s hospital, one adult woman pauses beside a blank bedside card, mild overcast light` | `Medium shot in a simple 1840s infirmary ward with unadorned plaster walls and a plain wooden cot, one adult woman in her late twenties wearing a floor-length long-sleeved Victorian dress pauses beside a blank bedside card clipped to the wooden headboard, muted daylight`。以簡單灰泥牆、木床、長裙和空白床頭卡具體指向 1840 年代病房，針對首輪現代裝置、病床與年幼護士形象。 |

三景仍是單一成年人物、單一主動作、無可讀文書的卡通示意；服裝、長椅、木床是提示詞層級的時代視覺線索，不作史料原物重建宣稱。沒有加入冗長否定詞，`look` 的 `cute-mystery` 預設未改。**新提示詞尚須另一人獨立核對史料與書面畫面**；先前 [R14 來源／畫面 PASS](r14-source-independent.md) 綁舊版 `video.json`，不能直接算作新版的裁決。

## 精確版本與工具檢查

| 檔案 | SHA-256 | 本次狀態 |
| --- | --- | --- |
| `video.json` 修前 | `e6db00932cd190a614de70e56abb577d1c7fe3fd7b3ffc2df0a0f123d0335577` | 首輪三張原生圖所綁版本 |
| `video.json` 修後 | `790f04b477f0ad4c91f41e3e089e3c5c486addda36822140b0e2d85167f9f0a4` | 僅三個上述 `data.prompt` 與修前不同 |
| `script.md` | `d5d01d3c96327060df9e7531aba796af45bedeaa25b8124c5993de528f7a8e40` | 原樣 |
| `claims.md` | `3bb23f35174a424e1f6981cd70926491edb521c758b562bb9a499d19298cfbe8` | 原樣 |
| 私有 `narration.wav` | `f705fd6052dca8bdd00e441d4a9cf1730e7efc9a90b5f7609b10a7685e027c5a` | 原樣 |
| 私有 `timeline.json` | `60331fbdcd8f30b37facafe65c9ded9b619eaf43ada9e576f01653d2adf7f67c` | 原樣 |

`lint --slug curio-s46 --json`：**0 errors、1 個既有片尾未口播訂閱 warning**，沒有本次提示詞的新警告。`keyframes --slug curio-s46 --shot bkw002,bkw006,bkw007 --takes 1 --dry-run` 通過：三景提示詞預算分別 **225/1071、260/1072、269/1072** 字元，皆在供應商限制內；下一次三張單張試畫報價約 **US$0.04**，計入已核准的整集 **US$4.54** 上限。`git diff --check -- docs/videos/curio-s46/video.json` 通過。

下一關由**另一人**對上述精確 `video.json` SHA 重新作史料與書面畫面差分審核；PASS 後才可依原方案對同三景各付費重畫一次。須逐張直接驗收未裁切原生圖並記 KEEP／REJECT。第二輪若少於 **2/3 KEEP**，停止這個付費插圖方案；不能以機器高分取代原生裁決。
