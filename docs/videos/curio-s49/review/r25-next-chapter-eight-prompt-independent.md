# S49 R25｜下一章八景獨立書面圖審

2026-10-22 UTC。只審 R24 分鏡的第二章首八個尚未製圖的 `shot`：`moon032–moon039`；八景都屬「不存在的巨鏡被寫得像工程記錄」，在 R24 來源卡 `moon031` 之後，沒有跨章挑圖。**逐句史料／claims 8／8 PASS，現行圖像提示詞 2／8 PASS、6／8 HOLD；整批不可直接開畫。** 這不是原生圖片或整集 storyboard 驗收。

## 綁定與來源

- R24 `video.json` SHA-256 `98e00e94079f0725068ecdc44be124934fc69540c0d9be62a0c8340d2222d13c`；`claims.md` `e6a8115bc1b9c14078e99059b836cb6d15027f67fe073671de1daa45d9d54190`；`script.md` `82369f762cc64f70e300e2104a16af3b8e99f1e3296dd81a34152e967f0ecb0a`；`research.md` `f5da15ac571478389b9b9920832f79434f83af0d312cb84747dcdb680a667750`。只讀 `lint --slug curio-s49 --json` exit 0，0 errors／0 warnings，131 句。
- 固定 L：Locke 名下 1859 重印本，GITenberg commit `ce684a827afd854e0843679fe4568fcaeeb12ae7`，本地原文 SHA-256 `3ca0bc9b6fc5c50b090d61bf2049e925d22dd1cdef2b443a282f7fdc5749e654`，[L390–520](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L390-L520)逐段寫虛構 Brewster 對話、無鏡筒高物鏡／暗室反射鏡、倍率增高而光少、人工光與顯微鏡、蚊幼蟲比喻。固定 J：Jacoby 1902，commit `073dd7dd24b8515dec681441a1cde79477fabf08`，原文 SHA-256 `f5ab32e64e7ea3735ff90fb000ae8cc82dddea594e0de0c6be30b30f94485029`，[J4083–4125](https://github.com/GITenberg/Practical-Talks-by-an-Astronomer_53396/blob/073dd7dd24b8515dec681441a1cde79477fabf08/53396-0.txt#L4083-L4125)明稱此段是虛構、光學詞彙拼貼。L 是後印文本，J 是後出分析；畫面不得冒充 1835 原報、真赫歇爾器材或已核實實驗。

## 逐景判斷

| 景 | 書面結論 | 依據與下一步 |
| --- | --- | --- |
| `moon032` | **HOLD** | 旁白「兩人想讓」只是虛構討論；現稿 `technician adjusting a high lens above a dark observing room` 把想像中的方案畫成已建造／操作的器材。改成 1830 年代成年讀者觀看一張無字扁平物鏡／暗室概念圖，明確無實體高架或真天文台。 |
| `moon033` | **PASS，原圖仍須驗收** | L 直接說暗室用反射鏡接影像；現稿明寫 `imagined 1830s`、單一成年人、無字素面反射鏡，沒有假裝原件。原圖須拒絕現代工坊／實驗衣、童貌、可讀字、實體已建成巨鏡或黑邊。 |
| `moon034` | **HOLD** | 旁白是對倍率與光量的討論，現稿讓未定年代的學者湊近實體望遠鏡目鏡，容易像真 Herschel 已用該器材實測。改成 1830 年代成年人對著無字概念紙與逐暗的光圈示意；勿用可辨真望遠鏡或量測紀錄。 |
| `moon035` | **HOLD** | 「紙上的赫歇爾」提出人工光問題；`telescope focus diagram` 容易生出後世工程圖或有字原件。改成 1830 年代成年讀者指向一張單頁、無字、非原件的簡筆焦點概念圖，避免現代控制器及真正設計圖的外觀。 |
| `moon036` | **HOLD** | L 支持折射與入射角話題；`at an imagined lab` 未定年代，常導向現代實驗室／白袍，而紙上的兩人只是對話。改 1830 年代高領衣成年人在木桌上畫無字光線角度，明確是原創討論示意、非實驗照片。 |
| `moon037` | **HOLD** | L 的動作是虛構 Brewster 聽後從椅上跳起；現稿只讓一位不明年齡學者在鏡片圖旁舉手，缺少關鍵反應且圖像可能像真光學成果。改為 1830 年代成年人物從木椅起身、面向另一人，無光學原件／現代服飾。 |
| `moon038` | **HOLD** | 旁白問這場對話是否真解決光不足；`one student smiling at an unmarked dialogue block on paper` 生出無來源的學生／可能童貌與近代漫畫對話框，沒有承載懷疑。改成成年 1835 年讀者對無字報紙略帶疑問的近景，不畫對話框或原報複製。 |
| `moon039` | **PASS，原圖仍須驗收** | L 確實以水滴中的蚊幼蟲、顯微鏡放大作虛構文章的類比；`imagined 1830s reader`、簡單顯微鏡與水滴是概念示意，旁白明說「作者拿…打比方」。原圖須拒絕童貌、現代電子顯微鏡／白袍、幼蟲變成已拍攝的真實月球證據或可讀文字。 |

六個 HOLD 只需窄修各景 `data.prompt` 及 claims 同列畫面欄，保留 `moon033/039`、旁白、來源錨點、章節、運鏡、先前 26 張 KEEP 圖的請求鍵與選圖 SHA。作者應留可逆前後差分、新 `video.json`／`claims.md` SHA、lint 0／0，再交非作者覆核全部八景的新凍結版；只有紙審通過才按停止標記和整集上限逐景試圖。機器 PASS 仍須看 1280×720 原生圖與裁圖。

## 私人媒體狀態

R24 `keyframes/manifest.json` SHA-256 `4f40a7ad117ed6393b4fea39e4cfbd206ee0312b1c6c9b25ba8e3bc48e72c611`，保留 26 個已驗收條目且對應選圖檔 SHA 全部相符；`moon031` 退件圖不在現行圖單。120 個 `shot` 中其餘 **94** 個未畫，包含本批八景。私有 ledger SHA-256 `ec7da38adbceaf55dfec5683982791f0cf3084d12d22d23e428d976f8a10c893`，US$0.9990／74 image／74 judge／0 reservations，低於 US$5.30；`STOP` 在位。本輪沒有媒體呼叫、帳本／圖單修改或付費。
