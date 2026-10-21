# S38 R8i｜`pf006` 第二次試畫前獨立紙上覆核

2026-10-21 00:30 UTC。**PASS：限於 R8i `pf006` 的精確差分、日記來源及提示詞規格；原生新圖、整體分鏡與成片仍 HOLD。**我未撰寫這句提示詞，也未變更創作檔、媒體帳本、停畫標記或網站核准。

## 固定版本與差分

實測 SHA-256：`brief.md` `fa297d70e016d88ba1a59bd92476be22eda3eefc09f36b2d08c0c82ab114643b`、`research.md` `f838518cf2c4ab23de91021ae6024d9431f907866c14301466ca0a06bb3ecdfe`、`claims.md` `f9de8d2771b62cc327f4e599f002af8f3278cfb0f39dbed201e7fdc857201d42`、`script.md` `e59ec137e3de3871e3b0e5063d8f6504d3eb2adb5fe22265eb3faa3d613d5951`、`video.json` **`de27c08f77dd91e66703fcf5c875ee1ea787d34246b93bc6237af8c7fcd03861`**。`visualHash` 從 R8h `1f353c19c4d07f47` 變為 **`79b6a9303fdfaeba`**；lint 實測 0 error／0 warning。

我沒有只採信[作者的結構化差分](verify-21-r8i-structured-diff.json)。從目前 `video.json` 原始位元組把唯一新提示詞換回舊字串，可**逐位元組還原** R8h SHA-256 `7e9eb1a2019bbf55727ac08c1bf273fc2fbf420223c6425083558afbfb9b0631`。解析兩版遞迴比對，唯一差分是 `scenes[5].data.prompt`／`pf006`；前後 `visualHash` 也分別實測相符。`look` 仍恰為 `{"preset":"cute-mystery"}`，`negative` 未新增，沒有改旁白、來源、其他 111 景、品牌或已付圖的請求內容。`pf004／005` 兩張 R8h 原生 KEEP 的實際沿用仍要由工具用逐景 request key／judge stamp 核對，不能憑紙上比對宣稱 manifest 已對應新版。

## 來源與畫面

重新取得固定 GITenberg commit `68fcf49f70ee793b989a6fd0464264d55beb4451` 的 `4200.txt`，原文 SHA-256 **`3cd43a3c39ee72eb9c4a3657f1fcb1723afba291cedac176c65a39289483be5d`**。[D2a](research.md) 引用的 L65784–65831 寫 1666 年 9 月 2 日約凌晨三時 Jane 叫醒佩皮斯，告知城中有火；他走到「她的窗」，覺得火還遠，之後回去睡。`pf006` 旁白仍為「先回到兩天前。九月二日凌晨，女僕珍妮發現城裡有火。」更新後的提示詞用屋外視角、開啟的上層窗、**一位明顯成年的**女僕探出上身並朝遠處小火光看，與這個敘事示意相容；一人及一個連續姿勢，沒有畫第二位目擊者、火源或已確認的燒毀房屋。

日記**沒有**記 Jane 的年齡與相貌、是否親自探出窗、房屋紅磚結構、巷子的外觀，這些是插畫的概念元素，不能在成片或說明欄稱為現場重建。`clearly adult`／`mature facial features` 是避免上次圖像誤畫童貌的製作限制，不是新的歷史主張。提示詞只指定人物、動作、地點與遠火，沒有塞入 `cartoon`、`vector`、色盤等畫風命令，仍由系列 `look` 控制。

## 原生圖 KEEP 界線與停點

[R8h 三景停點](verify-20-r8h-three-shot-native.md)的 `pf006` 原生圖 SHA `a87978e35d8cfb9355ca75969aca21a5082f701da2887dc3503a36471320a78f` 判退：童貌人物坐在室內、火像貼窗，並帶 3D 感和框邊。**下一張必須以 1280×720 原生圖查核**：人物顯然成年，身體確實在開窗處朝外，城火在遠方而非窗邊；房屋沒有明顯不合年代的現代元素，畫風仍是既定平面卡通，無黑邊。機器總分即使高，也不能蓋過上述肉眼衝突。R8i `pf006` **只剩一次** `1 take + 1 judge`；若再退件，整集維持 STOP，不能續買後面一百餘景。

私有 `/workspace/.video-work/curio-s38/STOP` 實測存在。本集 ledger **US$0.2760**（16 張 image、14 次 judge、1 首 music），其中舊 `pf003` **US$0.0035 reserved** 未解；整集硬上限 **US$4.58** 未提高。`pf004／005` 的原生 KEEP、`pf003` 對帳、30–60 秒濃縮開場與網站站主審核均是獨立關卡。此紙上 PASS 不是原生圖片或網站核准。
