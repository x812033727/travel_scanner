# S49 R19｜首章限額首輪插圖於來源／年代風險停止

2026-10-22 UTC。[R19 資訊卡獨立書審](r19-moon016-source-card-independent.md)先 PASS；其後依 [六批策略](r17-bulk-art-strategy-independent.md)用 `--takes 1 --shot moon017,...,moon031` 開始首章一批。原訂 12 張，生成 `moon017–025` 的 9 張後碰到策略停止條件，立即恢復 `STOP`；`moon028`、`moon030`、`moon031` **未畫**。沒有啟動下一批，也沒有推分鏡核准。`keyframes` 輸出「stopped by the STOP file after 9 new keyframes」並正常退出。

我以圖像檢視工具逐張打開 **1280×720 原生 JPEG**，同時核對該句旁白、`claims.md` 畫面欄與 judge；評審通過仍可能因來源或時代錯誤而退。完整原圖／選圖 SHA-256、每題分數及原文理由在 [逐張清單](r19-first-chapter-native-inventory.json)；這是獨立直接看圖的編輯判斷，並非站主本人審片或全片人耳核准。

| 景 | 原圖 SHA-256 前 12 碼 | 機器 | 直接原圖結論 |
| --- | --- | --- | --- |
| `moon017` | `6d9acad850fe` | 9.71 FAIL | **HOLD**：沒有連到手臂的手握住大報；裁邊後仍有缺陷。 |
| `moon018` | `119fbb94e8b5` | 9.29 PASS | **KEEP**：灰髮研究者、書架與原增刊缺席的概念安全；手指沒準確指向空隙屬次要細節。 |
| `moon019` | `cab6954b6a1a` | 9.29 PASS | **HOLD**：1859 重印本旁又有一本攤開的書，會把「未得原增刊、可翻的僅重印本」畫成似有第二份來源。 |
| `moon020` | `cc8df9294846` | 7.88 PASS | **HOLD**：現代辦公室、領帶與可讀標籤取代報導內 1835 年觀測站傳信的示意。 |
| `moon021` | `04cce0f9b785` | 9.71 FAIL | **HOLD**：小孩與現代可調電燈取代成年插圖工作者；機器也抓到主體年齡錯。 |
| `moon022` | `6ef0cb929260` | 9.29 PASS | **KEEP**：灰髮研究者拿空白索引卡、抽屜空位；沒有捏造格蘭特原信。 |
| `moon023` | `c10121bc373e` | 9.29 PASS | **KEEP**：成年讀者在想像場景拿無字紙／信封，未呈現已查獲原信。 |
| `moon024` | `35cc6de844e2` | 9.00 FAIL | **HOLD**：可讀字樣及一堆檔案箱／文件，與為表明「皇家學會文件未得」而指定的空托盤相反。 |
| `moon025` | `4432ae0af556` | 9.29 PASS | **HOLD**：人物是穿拉鍊連帽衣與球鞋的小孩，落在這段 1835 年故事的年代之外。 |

`moon019`／`moon024` 有兩張同類「原件／文件似乎在場」的來源層級風險；`moon020`／`moon021`／`moon025` 有三張同類成年或年代錯誤。這兩組都達 [批次策略](r17-bulk-art-strategy-independent.md) 的停止線。我在 `moon024` 原圖檢查後加回 `STOP`，`moon025` 已在執行中的呼叫隨後完成；工具沒有再畫 `moon028`。不要用機器 PASS 當作這六張 HOLD 的放行。

事前已私有備份 manifest、ledger、dry-run 與前十五張選圖 SHA 清單於 `/workspace/.video-work/curio-s49/review/r19-first-chapter-pre/`。`moon001–015` 的清單項目逐一與備份相同，所選檔案 SHA 全合；R18 退件的 `moon016` 在 R19 變成資訊卡，未進新清單。新 manifest SHA-256 `d583679e42d56bcab00eb27e3d4e3df5aadeb4325e0aeac942b042ae8eba0994`。因 `STOP` 早停，這輪沒有重製完整 contact sheet；有圖不等於分鏡核准。

付費前 read-only dry-run 報 MiniMax `image-01` 1K ready，12 張一輪約 US$0.16。實際帳本從 **US$0.6885／51 image／51 judge** 增至 **US$0.8100／60 image／60 judge**，9 圖＋9 judge 正好 US$0.1215，無音樂、無預約；低於整集圖／評審／音樂累計 **US$5.30** 上限，剩 US$4.49。受控命令有 EXIT trap，現在 `STOP` 存在。R19 創作檔 `video.json` `a62df2aa…`、`claims.md` `3ca1287a…`、`script.md` `82369f76…` 未被此畫圖批次修改。

**下一步：**把六張 HOLD 的共同錯誤分組修提示詞／來源示意，對來源敏感的 `moon019`、`moon024` 可比較同章已驗收圖或資訊卡；修改須保留敘事證據層級與插圖比例，且經非作者書面覆核。`moon017` 可在獨立確認後用 judge 的「手臂相連」修正嘗試一張。未畫的三張與其他章可在模式修好後續跑；每張仍須原圖檢查。網站 outline／script／audio 卡目前待站主，技術零旗標旁白不等於人耳審核；片頭、片尾、配樂、成片、Shorts 與真實 Studio 連結仍未完成。
