# S49 R19｜`moon016` 來源資訊卡獨立覆核

2026-10-22 UTC。**PASS：可用 R19 資訊卡，並允許按既定 US$5.30 整集上限執行首章未畫插圖的單次首輪批次。** 本回條只核卡片與所述批次前置條件；不核准其他 106 張圖、全片分鏡、站台卡、音訊人耳聽審或發布。我沒有撰寫 R19 的創作修改。

## 精確差分與來源

我讀取 R19 原檔及 [可逆差分](r19-moon016-card-structured-diff.json)，分別把 `video.json` 的 `moon016` 區塊及 `claims.md` 的單列書面畫面文字換回 R18，並核對**整檔原始位元組 SHA-256**：

| 檔案 | R18 還原 SHA-256 | R19 現檔 SHA-256 |
| --- | --- | --- |
| `video.json` | `686c2c7bd35232da0b3483810dfc659e8c01f2bb3dd9a6113fbedafcb2a705c6` | `a62df2aa4003850b38011dcd2877105bf2d98fe4fc36584304655a1d43ef2928` |
| `claims.md` | `42a0ba94dc4677ca8a460f3001d46279f883559784b2d9daa972336316df8839` | `3ca1287ab6b9e579be65c975c3cc7a393beba869c28f29515f1bfe756b5481ec` |

只改 `moon016` 的 `template/data` 和 claims 視覺描述。`script.md` 仍為 `82369f762cc64f70e300e2104a16af3b8e99f1e3296dd81a34152e967f0ecb0a`；旁白句「報導沒有只靠名氣；它又搬來一份學術刊物的增刊。」及前十五張已 KEEP 的提示詞／鏡頭不變。我另把私有 R18 前存 manifest 與目前 `moon001–015` 清單逐項比對，所選圖片檔的 SHA 也與清單相符。

固定 1859 年重印本 `/tmp/curio-moon-source/62779-0.txt` 的題頭 L159–166 明寫「FROM THE SUPPLEMENT TO THE EDINBURGH JOURNAL OF SCIENCE」，正文 L168 起以該刊增刊的口吻說話。這是**報導自己的來源宣稱**；該重印本不提供獨立的 1835 原刊證物。R19 卡片依序寫「報紙自稱／學術刊物增刊／本片未取得原刊」，只表達宣稱與本次查核範圍；沒有說原刊確定不存在，亦不畫會被誤認為存世增刊的實物。這是具體來源名稱卡，符合系列容許的資訊卡用途；R16–R18 三張人工作退的圖片仍不可用。

## 影片與費用邊界

`lint --json` 為 0 errors／0 warnings、131 句。正文 121 張插圖／7 張 `big` 卡，插圖占 121／128＝94.5%；最大連續卡片 2，未達三張上限。R19 `keyframes --takes 1 --dry-run` 報 121 shots、MiniMax `image-01` ready。私有 ledger 此時 US$0.6885／51 images／51 judges／0 music／0 reservations；`STOP` 存在，與 US$5.30 累計上限相差 US$4.6115。

首章未畫的 `shot` IDs 是 `moon017,moon018,moon019,moon020,moon021,moon022,moon023,moon024,moon025,moon028,moon030,moon031`，共 12 張；`moon016` 是卡片，`moon026–027` 和 `moon029` 也不是需畫插圖的景。按 目前單張圖＋評審約 US$0.0135，首輪約 US$0.162；實際呼叫前須重讀模型報價及餘額、備份 manifest 與 ledger，在受控 EXIT trap 下移除並恢復 `STOP`。逐張看原尺寸原圖、對照旁白和 claims；兩張同類來源層級誤導圖或三張同類成年／年代／畫風錯圖即停止下一批，不能以機器 PASS 代替原圖驗收。若某景不過，保留原圖與 ledger，集中修同類提示詞後再由另一人書審。
