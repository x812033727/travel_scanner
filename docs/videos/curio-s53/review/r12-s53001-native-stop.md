# S53 R12｜首景第二版原生圖，人工退件並停畫

2026-10-22 UTC。**`s53001` REJECT；`s53003`／`s53010` 與全片其他景未試畫。** 先前的[R12 獨立紙面覆核](r12-s53001-independent.md)只放行這張原生圖重試，不預先核收生成畫面。

付費命令是 `keyframes --slug curio-s53 --shot s53001 --takes 2`，執行時 R12 `video.json` SHA-256 `3b5382c1b06f882936d5e61823efe834f51b1b9c0a858c57f0fc18309be01949`；使用 `EXIT` trap 復原私有 `STOP`。由於提示詞已變，這次產生新版本 take 1 一張與 judge 一次，沒有再買第二張。原生 1280×720 JPEG 私存 `/workspace/.video-work/curio-s53/review/r12-native-first-stop/s53001-1.jpg`，SHA-256 `1b586e6956669a3b6b521a9c7ed38acb43226e6c0eeead197e3f82bc9e483759`；裁邊圖 SHA `87e200daeb72fe6c78576a66c27263fbc8c3007faf253a520390e9bb74445184`，manifest SHA `9d5fc5354d197639f753e8790620a1d83d095913c5ee067e1b11d828e1b35d1e`。R11 原圖及 manifest 仍另存於 `review/r11-native-first-stop/`。

我直接在原尺寸看過 R12 原圖：前景成年人和一排低矮小屋雖更接近旁白，但小屋兩側出現可辨識的**現代汽車、現代樓房、現代硬鋪人行道與街景**；建築背景呈照片／3D 質感，僅人物是卡通。這既違背紙面提示詞「背景只有廣場空地、小屋和天空」，也會把 1907 年救災廣場視覺化成現代住宅街。依系列只退實質年代矛盾與畫風漂移的規則，人工 **REJECT**。機器給 9.29／10、`passed=true`，卻在 `details=7` 明寫「modern urban buildings and vehicles on the sides」；機器通過不能覆蓋直接可見的年代錯置，`needs_review=false` 亦不能代表人工核收。畫面上小屋色彩與構造亦偏現代，故勿拿此圖當分鏡通過。

帳本現為 **US$0.0270**＝2 images＋2 judges、0 music／0 reservations，低於整集圖像＋judge＋音樂上限 **US$4.78**；`STOP` 已存在。下次先由作者在紙面把構圖收緊至單棟小型木造救災屋與局部空地，避免遠景模型自行補現代街道、車輛；由另一人按源文／口播核其差分。未另核准前不再試畫，也不續 `s53003`／`s53010`。
