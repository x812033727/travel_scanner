# S49 R21｜`moon021` 單景提示詞獨立書審

2026-10-22 UTC。結論：**來源及書面畫面 PASS；僅放行 `moon021` 一張受控首試，不等於原圖或分鏡通過。**

我重新打開 R20 `moon021` 的原生 1280×720 JPEG（SHA-256 `071fcaca2a127b0757086a8a24a8437699905ab3fb7fbe90106f7473e49e29b4`）及裁後選圖（`4fa4068846256c1582fd23591db9326f5ae0f51848a5e0b957225b033eabf8d4`）。原圖頂底黑邊、人物童貌及側鬢缺席均可見；選圖去邊後評審仍 9／10 FAIL，manifest `needs_review=true`。R21 的中近景、灰側鬢與鬍子、成熟臉線及肩型，對準成年辨識；背景填滿寬畫幅四邊，對準黑邊。保留 R20 已安全的窗光、舊式服裝與單張無字月面草圖。

固定 1859 年重印本 SHA `3ca0bc9b…` 的 [P03 L230–250](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L230-L250)只說**報導自稱** Herbert Home 於觀測站繪圖。冒稱的增刊見 [P02 L152–165](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L152-L165)；固定 Jacoby 1902 年評論 SHA `f5ab32e6…` [J4063–4070](https://github.com/GITenberg/Practical-Talks-by-an-Astronomer_53396/blob/073dd7dd24b8515dec681441a1cde79477fabf08/53396-0.txt#L4063-L4070)指正文在美國編造。R21 的灰鬍子畫者是辨識成年人的卡通特徵，未冒充 Home 真肖像、找到的實際草圖或真實觀測室復原。旁白仍先說「文中還把插圖說成」，畫面欄明寫「報導自稱的現場繪圖想像場景」。

我按[可逆差分](r21-moon021-prompt-structured-diff.json)逐字驗證：只換 `scenes[20].data.prompt` 和 claims `moon021` 畫面欄一次，兩檔原始位元組分別還原至 R20 SHA `b557ddb82e51608adf48052b3174ca8f72e309ee4476df630b3993da14afb8d9`／`84e81619c5e57981515a79d4ec3b97c976a9eb72cfb5e8dd2050765d59617`。現行 R21 `video.json` SHA `e01e1d91bff2000cac2ec0e0dcef34b01c431b0259ac81ca914a52f664f11042`、`claims.md` `87447ad856fe06d68ccd02667fad2ab986ad7573d3789ceefa099b04554d1943`；其他 **128／129 景**與 `script.md` SHA `82369f762cc64f70e300e2104a16af3b8e99f1e3296dd81a34152e967f0ecb0a` 未動。`lint --json` 0 errors／0 warnings；單景 `--takes 1 --dry-run` 報 MiniMax `image-01` ready，397／1070 字元、約 US$0.01。帳本 US$0.8910／66 image／66 judge，0 音樂／預約，低於整集 US$5.30 上限；`STOP` 存在。

付費放行範圍只有本景一次，須保存 R20 原圖與前後帳本、EXIT trap 恢復 `STOP`、直接看新原生 JPEG 及 judge。其他首章／章節不在本書審範圍。
