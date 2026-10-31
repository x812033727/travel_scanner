# S49 R28｜`moon032` 虛構構想來源卡（作者候選）

2026-10-22 UTC。**只完成作者窄修，待非作者紙審；不重綁私人圖單、不做付費媒體。**[R27 原圖停批](r27-moon032-native-stop.md)的一張 1280×720 原圖及裁圖，雖機器評 9.29 PASS，卻把應在高處的開口畫成落地門口；史料所說高處物鏡與暗室焦像的關係無法從畫面讀出。保留那張人工退圖為私人證據，不再憑相同圖作 KEEP。R28 只把 `moon032` 從 `shot` 改為 `big` 字卡：

| 位置 | 字樣 |
| --- | --- |
| 上標 | **1835 年報導的虛構構想** |
| 主文 | **物鏡架高處，焦像進暗室** |
| 下標 | **1859 重印本所載，非實作紀錄** |

固定 Locke 名下 **1859 重印本**文字 SHA-256 `3ca0bc9b6fc5c50b090d61bf2049e925d22dd1cdef2b443a282f7fdc5749e654`，[P05 L398–413](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L398-L413)在冒稱 Herschel／Brewster 的對話裡，寫物鏡置於高桿、焦像投向遠處，並假設將焦像送進暗室以反射鏡承接。固定 Jacoby **1902 評論** SHA-256 `f5ab32e64e7ea3735ff90fb000ae8cc82dddea594e0de0c6be30b30f94485029`，[J4083–4125](https://github.com/GITenberg/Practical-Talks-by-an-Astronomer_53396/blob/073dd7dd24b8515dec681441a1cde79477fabf08/53396-0.txt#L4083-L4125)明說這是 *imaginary conversation* 和光學術語拼貼。卡片的上／下標將「1835 虛構報導」「1859 重印本」及「非實作紀錄」同屏，主文只轉述文字構想；它不是實物、可核設計原件、真赫歇爾儀器或 1835 原報影像。`claims.md` 的 `moon032` 畫面欄同樣寫明這些界線，逐句主張和 P05 錨點沒有改動。

[逐字可逆結構差分](r28-moon032-source-card-structured-diff.json)（SHA-256 `d5d4034a75f9c7d51c5841c987f1501989020015b9e79d2e04847ca9398b9bae`）保存 `moon032` 的 `id/template/data` 原文與新文、以及 claims 同列畫面欄原文與新文；倒填可逐位元還原 R27。`video.json` SHA-256 `02fdb0f2ac142634d42ac24f7108bb12424e7a4625756ca559b90d52912552a3` → **`a4d00cdc41078cc016247127c5a3676bb8a8ee98699662395bd2cfdc1f4b62a2`**；`claims.md` `779a8e22e6e7e202249cf7ec645a91a7ade7139c5c0e6ee2bb70c4fa50f2bd2f` → **`b89b557b52bb98dd3e4d654b665e4cd874434784a5850d71044323c7543a44e3`**。其餘 128 個 scene、全部 `lines`／旁白、`moon033–039` 提示詞、章節及來源設定逐項不變；`script.md` SHA **`82369f762cc64f70e300e2104a16af3b8e99f1e3296dd81a34152e967f0ecb0a`** 未變。

正文現在 **119 shot／9 big＝119／128＝92.97% 插圖**，高於 70%；最長連續字卡 **2** 張（`moon031–032`，亦有其他兩連卡），低於 3 張上限。`renderPlan` 對 `moon031/032` 均輸出 `kind=stills`、`moon033` 仍為 `kind=clip`；卡片主文、上標與下標進入實際畫面文字。`lint --slug curio-s49 --json` exit 0、**0 errors／0 warnings**、131 句。以 `spokenUnits` 及 **325 CPM** 只計開場後、片尾前的 120 個正文章節景，2633 units → **486.09 秒＝8:06.09** 最快文字估時；旁白沒改，所以與 R27 相同，實際 TTS 時長不能由此宣稱。`git diff --check` 通過。

私人 manifest 尚綁 **R27** `visual_hash=74c5cc0713c7766d`，而 R28 新 `visual_hash=dfe0bece015e7458`；須待非作者紙審後才能重綁，**現時不可送 storyboard 或續畫 `moon033`**。26 張先前人工 KEEP 的現行圖單與所選檔案未動；R27 退圖不在現行圖單。私人 ledger SHA-256 `076a31adf1dd34d89a11ecc9a18c819bbaa7bec3164b56098fb1d5db4ebb9275`，US$1.0395／77 image／77 judge／0 預約，低於整集 US$5.30；`STOP` 在位、jobs 空。本回無 image、judge、music 或其他付費請求。以目前 119 個正文 `shot` 計，仍有 **93 景未獲人工原圖 KEEP**；完整影片、網站卡、人耳審核、片頭片尾與 Studio 連結均未完成。
