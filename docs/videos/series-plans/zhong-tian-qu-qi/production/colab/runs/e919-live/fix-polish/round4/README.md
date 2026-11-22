# 第 19 集（e919）第二波重拍（round4）：s16、s32

2026-11-22，照 `review-zt/WAVE2-BRIEF.md` 與 `WAVE2-CANDIDATES.md`。種子 9199401／9199402，每鏡兩支 960×544 Ref2VA。
`python3 -I ../../../_scripts/polish-build.py 19 4` 寫出 `runpod/live/fixp4/`（4 支、28 秒）。只寫提示詞，沒送出任何工作。

| 鏡 | 錯在哪 | 改了什麼設計 | 圖 | 拿不準的 |
| --- | --- | --- | --- | --- |
| s16（C） | 燈籠骨架是乾淨竹圈掛巴掌大銅牌，不像燒過的證物；第 17 集已把這個道具重拍成直骨圓球籠、圓木底座、正面拇指甲大方孔銅片 | base `fix1/.../ref-s16-9191201`。照第 17 集 s39 第二輪（現行）的設計：送同一張 `prop-denglong-gu-l1`、道具句照抄（加「方孔」），腰上中近景、低機位，燈籠第一格就托在右掌胸高、跟頭一樣大，藍布攤在下緣；拿掉解布包、從包裡拿出（fix1 拿出來的就是竹圈）；一個動作：最後幾字把燈籠往畫右抬一掌停住；臉朝畫右的錢員外，逐部位寫到最後一格不笑；拿掉胸前鼓包句 | `xuyan-portrait-l1`、`xuyan-angle-a-l1`、**`prop-denglong-gu-l1`**、`set-xianya-gongtang-floor-l1`；拿掉帶斜嘴笑的 `xuyan-angle-b-l1` | 候選清單寫「插入特寫」；這句是許硯的模型原聲（`voice_off` 只有 s09、s34），拍成沒有嘴的插鏡就得改用錄音、跟他前後鏡的聲音不同，所以保留他的臉、把燈籠放大到跟頭一樣。沒有另裁 w2 圖：`prop-denglong-gu-l1` 就是第 17 集現行 s39、s40 用的那個樣子 |
| s32（B，取代 s31） | 前景阿令背影是整頭盤髻、露後頸，跟定妝照（半披髮加木簪）與相鄰 s31、s08 不同 | 協調者 2026-11-22 定：守定妝規則，s31 不拍（現行是半披髮，對）、改 s32。base `d1/.../ref-s32-9191102`，原機位、台詞（許硯原聲）、動作不變，只改阿令的髮型句：頭頂一個小髻、一支木簪、其餘長髮直直垂到背後 | 加 `aling-portrait-l1`、`aling-angle-b-l1`（側面看得到垂背長髮），許硯三張與 `set-xianya-steps-l2` 照舊，共 6 張 | 背影裡垂髮可能被畫成全盤；現行片段裡沒有阿令半披髮的背影可裁，所以用定妝照與側面圖。原本為 s31 裁的 `aling-panji-*-w2` 兩張已刪 |

## 檢查（2026-11-22）

- `polish-build.py 19 4`：2 鏡（s16、s32）、4 支、28 秒
- `preflight-prompts.py …/fixp4/colab-jobs.json`：0 error(s)、0 warning(s)
- `h3r.sh check --manifest …/fixp4/colab-jobs.json`：0 error(s)、0 warning(s)
