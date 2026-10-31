# S49 R21｜`moon021` 原圖黑邊與成年辨識定點修復

2026-10-22 UTC。R20 [六景原生圖驗收](r20-six-hold-native-stop.md)中的 `moon017/019/020/024/025` 已 KEEP，只有 `moon021` HOLD。這是**作者書面修訂，尚待另一人獨立來源／畫面覆核**；本輪沒有新付費呼叫，也沒有放行該圖、首章或全片分鏡。

我直接看了 R20 `moon021` 的 1280×720 [原生圖清單](r20-six-hold-native-inventory.json)所列 JPEG（SHA-256 `071fcaca2a127b0757086a8a24a8437699905ab3fb7fbe90106f7473e49e29b4`）和裁後選圖（`4fa4068846256c1582fd23591db9326f5ae0f51848a5e0b957225b033eabf8d4`）。原圖上下有明顯黑邊，評審 9／10 **FAIL**，`frame` 指出黑邊，`details` 指定的側鬢不見；灰髮角色身形與臉頰仍容易看成孩童。裁圖雖去邊，沒有重新得到評審通過，manifest 仍 `needs_review=true`。R19 的現代電燈已消失、月面草圖與窗光已有，故不再改動那部分概念。

R21 只將 `moon021` 改成**中近景、灰側鬢加灰色小鬍子、成熟臉部線條與成人肩型**的 1830 年代插圖工作者；仍是一個人在想像中的南方觀測室畫一張無字月面草圖。提示詞要求室內背景延伸到寬畫幅四邊，以對準原圖黑邊。這些是避免模型把人物與構圖畫錯的卡通特徵，並非史料證實的 Herbert Home 容貌。固定 1859 年重印本 P03 L230–250 只顯示報導**自稱**現場插圖由另一人畫成；P02 的增刊來源也是文章自稱，1902 Jacoby 的後出評論 J4063–4070 說文章在美國編造。因此不能把本景當作真實 1835 觀測圖或人物肖像。`claims.md` 同列畫面欄同步改寫；旁白與來源連結未動。

[逐字可逆差分](r21-moon021-prompt-structured-diff.json)只記 `video.json` 的 `scenes[20].data.prompt` 與 claims 的 `moon021` 畫面欄。R20→R21 整檔 SHA-256：`video.json` `b557ddb8…` → **`e01e1d91bff2000cac2ec0e0dcef34b01c431b0259ac81ca914a52f664f11042`**；`claims.md` `84e81619…` → **`87447ad856fe06d68ccd02667fad2ab986ad7573d3789ceefa099b04554d1943`**。逐字還原此單一變更可還原兩檔原始位元組 R20 雜湊。其他 **128／129** 景，包括此前十五張及 R19/R20 的八張首章 KEEP，均未改。`script.md` 仍為 `82369f762cc64f70e300e2104a16af3b8e99f1e3296dd81a34152e967f0ecb0a`；既有語音的文字綁定不變。

`lint --json` **0 errors／0 warnings**、131 句；只讀 `keyframes --shot moon021 --takes 1 --dry-run` 報 MiniMax `image-01` ready，提示詞 397／1070 字符預算內，單次約 US$0.01。私有帳本維持 **US$0.8910／66 圖／66 judge／0 音樂／0 預約**，整集圖、評審、音樂累計上限 US$5.30；`/workspace/.video-work/curio-s49/STOP` 在位。下一位應依 R21 精確檔獨立查核來源與差分，之後只在受控呼叫中試 `moon021` 一張、直接看原圖；原 R20 FAIL 圖不可沿用。網站 outline／script／audio 卡仍待站主，並未得到人耳核准。
