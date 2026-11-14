# S38 R8ae PF021 最後一次提示詞獨立紙審

2026-10-22 UTC。審者 `/root/s38_pf021_last_paper`，未撰寫本輪提示詞。結論：**PAPER PASS**，僅限新提示詞與固定史料、旁白的相容性；成圖仍須依系列規則驗收。不得把本票當作第三張原圖已通過，也不得因此購買第四張。

鎖定 `video.json` SHA-256 **`a150042d8a53b5d63a86821759a81aef934240008ad4dd82c55bb83b99060844`**。作者初稿審閱中刪去冗餘地名 London，以免地點多樣性 lint 警告；最終仍明記 Thames landing、1666，時地沒有改義。`script.md` SHA `e59ec137e3de3871e3b0e5063d8f6504d3eb2adb5fe22265eb3faa3d613d5951`、`claims.md` SHA `f9de8d2771b62cc327f4e599f002af8f3278cfb0f39dbed201e7fdc857201d42` 不變。獨立解析前後 JSON 確認只改 `scenes[20].data.prompt`；以 verify-107 的舊值反填最終新值，逐位元組復原 Git 前版 SHA `c531301285fd9cbc3730f40c9c4a1d37936f00f2c7a0bfb98bf0c1ba97a7e121`。正式 lint exit 0，0 errors／0 warnings，112 句。

重開固定 Pepys 日記 `/tmp/s38-r8j-pepys-4200.txt`，全文 SHA `3cd43a3c39ee72eb9c4a3657f1fcb1723afba291cedac176c65a39289483be5d`。1666-09-02 L65821–65823 原文寫住戶一直等到火觸及房屋，然後 `running into boats`。旁白「佩皮斯見有些住戶等火貼近門口，才往船上跑。」與 claims D2a 相符。成人攀入靠岸低木船、一腳已在船內、雙手抓近側船舷，清楚表示朝船移動；冒煙磚牆在身後只提供火災脈絡，不新增抵達安全地點的結果。灰髮、衣物、船型與構圖是年代相容的插畫選擇，不聲稱日記辨認了某位居民或精確登船姿態。

新稿把左右岸屋之間的奔跑縮成單一成人登船動作，正對 verify-106 記錄的方向錯誤。仍由既有 cute-mystery preset 管畫風，未新增 style／negative 或要求可讀文字。實際生成可能仍畫錯手腳、方向或畫風；依 curio-episode 收圖規則，只因材料性旁白／來源矛盾、judge 不過或畫風漂移退件，不因未記載的非關鍵插畫細節重畫。

只讀核對時 active manifest SHA `843b8c4f060a59abdd390c814d8a9328c9c1e210212c9a4554dcc6a6669bc955` 仍綁前版 visual hash `03d5ee8d1b78b924`，13 張 KEEP 所選實檔 SHA 全符；沒有 PF021 入選。Ledger SHA `c321c103af687f456f8d34d0301d180380fdbcc4b28ed815a196395b25513df3`；STOP 在位、jobs 空。本票沒有重綁或媒體呼叫。付費前須在 STOP 下安全重綁最終 visual hash，再查 live 模型／餘額／單景 dry-run 與整集 US$4.58 上限；僅餘 PF021 第三／最後一次原生試畫，PF022 不由本票放行。
