# S49 R42｜`moon041` 入選圖 claims 畫面註解非作者覆核

2026-10-22 UTC。**PAPER PASS，僅限本次 claims `moon041` 畫面欄的出版描述修正。**我不是新註解作者；沒有改 `video.json`、`claims.md`、私人媒體檔、任務或 PR，沒有 stage、commit、push，也沒有付費呼叫。此收據不抹去原圖審查分歧，也不核准其餘 storyboard 或成片。

## 入選圖、來源與異議

我自行以完整 **1280×720** 看了第二張 `moon041` 未裁原圖 SHA-256 **`ac27c84942331b8cfa4138273d9d442b01ee16f409ab7f1711155fba787bfd52`** 與目前入選裁圖 SHA-256 **`8762bbf1c1485437dce80cabef48dd6db7c03293c0ad58eeafb58bf05286fd52`**。裁圖去掉原圖上下黑邊；一位灰髮成年讀者指向木桌上**無字紙張的一小塊淡色燭光**，旁邊是短蠟燭與外露火焰，側窗外可見模糊暗月。左側桌邊另有**水平的小型黃銅色鏡筒造型物**，沒有字、光路或可辨認為赫歇爾實際設備的標記；平面描邊卡通畫風合於固定系列。機器 judge **9.29／10 PASS**，`details=7` 正確指出提示排除光學器材卻生成了此道具；紙張也偏離提示的裸木桌面。

我重讀 Locke 名下 1859 重印本 `/tmp/s49-moon-hoax-62779.txt` SHA-256 `3ca0bc9b6fc5c50b090d61bf2049e925d22dd1cdef2b443a282f7fdc5749e654` [P05 L420–443](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L420-L443) 與 Jacoby 1902 `/tmp/s49-jacoby-53396.txt` SHA-256 `f5ab32e64e7ea3735ff90fb000ae8cc82dddea594e0de0c6be30b30f94485029` [J4083–4125](https://github.com/GITenberg/Practical-Talks-by-an-Astronomer_53396/blob/073dd7dd24b8515dec681441a1cde79477fabf08/53396-0.txt#L4083-L4125)。前者的人工光與焦像是**虛構報導**中的光學談話；後者直指它是荒謬的想像對話。兩者都不能證成桌上小鏡筒為真實赫歇爾器材、存世圖像或實驗證據。新註解精確交代紙上光斑與黃銅色道具，並明寫「**概念插畫物件，不是赫歇爾實際器材、存世圖像或實驗證據**」；保留「燭光只示意照亮桌面，不替月球送回新細節」。它沒有把原圖中不存在的無器材裸桌面當成成品，也沒有替這件額外道具編造史料身分。旁白、P05／J 來源欄及 R42 生成提示均未改。

目視結論有**公開保留的分歧**，不作成全員一致：第一位[非作者原尺寸審查](r42-moon041-second-native-independent-visual.md) SHA-256 **`7b3c5ea7e3138651732cd0921c710f5c69c6017f328191e3868a634f11737a52`** 判 HUMAN KEEP、信心 0.75，要求更正 claims；另一位 S53 同行在協作訊息中判 **REJECT**，認為水平黃銅鏡筒十分像有底座的光學器材，違反 R42 提示明寫無器材，紙張也偏離裸木桌面，可能重新暗示器材。此異議**只有訊息，沒有審查檔或 SHA**。第三位先不讀前述兩判的[原尺寸盲審](r42-moon041-second-native-blind-adjudication.md) SHA-256 **`7bf853e5ebda4ac5877bcabd5f0b649ce81b1f390ca0455e95c67611c7ef4440`** 判裁圖 **HUMAN KEEP**、信心 0.91：小道具未接到紙上光斑、未指向月亮，也不是大型或具名赫歇爾裝置；紙張無實驗記號，畫面仍呈現近處照亮而遠月無新細節。我的判斷限於**這段修正後 claims 文字是否忠實描述入選圖並守住來源界線**；依 `curio-episode` 的實質誤導規則，這段文字通過，但上述不同意見與模型 `details=7` 必須留在製作紀錄。入選僅限裁圖，未裁原圖仍有黑邊。

## 精確差異與私人守衛

- 凍結 `video.json` SHA-256 **`07ca48195b04696375564fdde0295ecf35532e75c2b09db09b61a19ba0038f75`**、新 `claims.md` SHA-256 **`b51d288b6a2d33e2a976cf054a2b1cb3fdda5109f2845b18b78d81edffbd48af`**、[單行可逆差分](r42-moon041-selected-visual-claims-structured-diff.json) SHA-256 **`111e09557c61baeaa496c512f14b4a54180c9cf80499576a4b757fbaa0c0d0bd`**。我獨立把該差分 `after→before` 原始位元組替換一次，`claims.md` 逐位元還原 Git `ab0e617d0` SHA `5aa04589f6ad859c9178247003c2c56caeaf40dc03fab003c5e15f73b4020953`；**只有 `moon041` claims 畫面欄**改，其餘列、該列旁白與來源欄不變。`video.json` 對同一 Git 位元不變，全部 **129 景、131 句**不變；`visual_hash=d43f3c8a95c29e22`、`look_hash=98a370ae40badbaf` 不變。CLI lint exit 0：**0 errors／0 warnings／131 lines**。
- 私人 active manifest SHA-256 **`47a517c2b469ca1e48704643a1def318b59aa6f56131d30d1d4d293c56f0aa44`** 綁同一 R42 visualHash，已入選 **33 張**。我逐一核先前 **32／32 KEEP** 的 manifest 記錄與實檔 SHA，並核 `moon041` 新入選裁圖 SHA `8762bbf1c1485437dce80cabef48dd6db7c03293c0ad58eeafb58bf05286fd52`；`keyframeProblems` 只有 **84 景未畫**、其他 0。ledger SHA-256 **`d70880c78ace87406ca881373acfc58c9afd1e736e2decb734d5f86e65f22ae3`**：**US$1.2555／93 image／93 judge／0 預約**，低於整集 US$5.30 上限。`STOP` 在位、jobs 空。此 claims 修訂未觸碰私人入選圖、帳本或費用。

**結論：入選圖 claims 畫面描述 PAPER PASS，須連同 HUMAN KEEP 兩份收據與 S53 同行的訊息異議保存。**這只確認文字如實描述可見物件並明示虛構，不替畫面每一構圖細節作史料背書。後續 `moon042` 若要付費，仍須獨立重核它的既有紙審適用性、33 KEEP 檔案、STOP/jobs、即時媒體額度及整集上限，且一次只畫一張原圖並原尺寸驗收。
