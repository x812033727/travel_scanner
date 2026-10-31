# S55 R12｜十月見證歸屬的一句來源修訂

2026-10-20 UTC。這是針對 [R11 獨立史料覆核](r11-source-independent.md) 唯一 HOLD 句 `s55065` 的**作者候選稿**。該覆核指出，後出的十月繫留記載不能證明富蘭克林本人是否在場。R12 只敘述細節的文獻來源，不推斷他的行蹤。

## 五檔凍結 SHA-256

| 檔案 | R12 SHA-256 |
| --- | --- |
| `brief.md` | `c1f45453a7b13de1857a192b4c64571bbf1fce7cf12943a48a2369c829e04070` |
| `research.md` | `299b4ace9f8c5ea9d784b2d0296bdbf16c851108ae3b070264107f773cf9deeb` |
| `claims.md` | `317c50ab5142b13cf097cbc09a45a128068a6b27dd478f8a130f54a25c64409f` |
| `video.json` | `5aac04b0f097c9c5611874a946dc73d963a00109489a3ed361e5fb20953c119a` |
| `script.md` | `4a36cef7c4ba278089cb8fc49398a4470bb288822d6a59ab73794e8323b5b38a` |

## R11→R12 差異與史料界線

| ID | R11 旁白 | R12 旁白 |
| --- | --- | --- |
| `s55065` | 富蘭克林沒有親眼見到這回；後來的書說，氣球在空中停了多久？ | 十月這回的細節，要看後來的書：氣球在空中停了多久？ |

`claims.md` 的同一列逐字更新，來源仍是固定提交的 [P05／M 1293–1390](https://github.com/GITenberg/Wonderful-Balloon-Ascents--Or-The-Conquest-of-the-Skies--13-A-History-of-Balloons-and-Balloon-V__899/blob/c3f6d020de7d9a0ad864aabcf89138476680574e/899-0.txt#L1293-L1390)。該列畫面界線從「不作富蘭克林目擊」明確寫為「不推斷富蘭克林是否在場」，避免把當時信件未記下十月一事讀成他不在場。1870 年書房的書面提示詞仍以後出文獻呈現這段細節，未改動。

從 R12 `video.json` 只反向替換上述一句，SHA-256 精確回到 R11 `6cd095d19e64edc535fe64eedf871c7d552a3ad18bb585d1dbc030a535760803`；從 R12 `claims.md` 反向替換同句及界線短語，SHA-256 精確回到 R11 `3880224df0a16b826e2ecc8ba0d8842a0e7c814f13cfa1863ad90c2dbcc8f4a3`。所以其他旁白、來源連結、書面畫面、畫風和配樂設定都與 R11 相同。R11 的其他 13 句及書面畫面已由前述獨立覆核判 PASS；本頁不代替 R12 獨立判定。

## 作者機械檢查與交接

- `node tools/video/cli.mjs script --slug curio-s55` 已從 R12 `video.json` 重產 `script.md`。
- 140 個唯一旁白 ID；正文 138 句與 `claims.md` 的 138 列逐 ID、逐字相同，另兩句為既有 CTA。
- `node tools/video/cli.mjs lint --slug curio-s55 --json`：**0 errors／0 warnings**；工具估全片 13.63 分鐘。138 句正文合計 2,808 個漢字，扣除未改的 175 字開頭後為 2,633 字，按每分鐘 325 字約 8.10 分鐘。
- `npm run tasks -- check`：通過，只有既有任務持有時長及跨任務範圍警告。

**下一關：**由未參與作者修訂者對 R12 五檔 SHA 核 `s55065` 來源與書面畫面，再由兩位無前情讀者獨立盲評，正式合併敘事判定後跑本版政策與 TTS／全句音檢。R10 音訊仍 HOLD；R11 的來源 HOLD 不因本頁自行轉為 PASS。本輪沒有呼叫付費媒體，也沒有聲稱人耳聽檢。
