# S49 R44｜`moon044` 首張原圖與入選裁圖獨立原尺寸驗收

2026-10-22 UTC。**原圖 HUMAN REJECT；入選裁圖的畫面內容 HUMAN KEEP；整景仍 TECHNICAL HOLD。**我不是 `moon044` 提示詞作者，分別以原生 **1280×720** 查看兩張實檔。此判斷只處理這一景的可見畫面，不是機器 judge 通過、圖單放行、整集 storyboard 或成片驗收；本審沒有生成、評審或購買媒體，也沒有更改私人圖單。

## 凍結文字與來源界線

- 現行 `video.json` SHA-256 **`dd2dae850cdf455a01b9c99a01af2d9ef3370d81d11c7349f661d6a6220f8d9c`**，`claims.md` SHA-256 **`70f0d9255397880586c96a49cbda77cf3ca722b68815455f29b6ac9f841c2ebb`**。`look.preset` 是 `cute-mystery`；`moon044` 旁白是「連費用都有了；紙上的鏡片究竟鑄出來了嗎？」；提示詞及 claims 同列畫面欄都是「Close shot of one imagined 1830s glassworker, a visibly middle-aged adult with grey temples, lined face, broad adult shoulders and plain period work clothes, checking an empty circular mould, soft furnace light」。claims 明示這是虛構報導的想像畫面，非真實月面或器材。
- [R40 非作者紙審](r40-moon044-045-mature-glassworker-independent-paper.md) SHA-256 **`ca7696ff6f43632a98e215714fe0d18fd2d913d9a382f034328c51bec48e9d07`** 判上述文字 PAPER PASS；[R44 適用性收據](r44-moon044-r40-paper-applicability.md) SHA-256 **`6ddaf058241042f3eb0d2e82edf537e06e0415f3666b38427314936e464361cd`** 核明現行 `moon044` 與 R40 凍結 scene 和 claims 整列相同。兩份紙審均不代替本次看圖。
- 固定 Locke 名下 1859 重印本 `/tmp/s49-moon-hoax-62779.txt` SHA-256 **`3ca0bc9b6fc5c50b090d61bf2049e925d22dd1cdef2b443a282f7fdc5749e654`**，[P05 L435–489](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L435-L489) 在虛構故事中敘述估價、鑄模、首鑄失敗與再鑄成功。Jacoby 1902 評論 `/tmp/s49-jacoby-53396.txt` SHA-256 **`f5ab32e64e7ea3735ff90fb000ae8cc82dddea594e0de0c6be30b30f94485029`**，[J4083–4125](https://github.com/GITenberg/Practical-Talks-by-an-Astronomer_53396/blob/073dd7dd24b8515dec681441a1cde79477fabf08/53396-0.txt#L4083-L4125) 稱該儀器為想像中的器材，沒有獨立核證真實鑄鏡。圖中鑄模因此只能當作故事概念示意。

## 兩張 1280×720 畫面

| 實檔 | SHA-256 | 獨立目視判斷 |
| --- | --- | --- |
| `/workspace/.video-work/curio-s49/keyframes/moon044-1.jpg` | `953ee0d75c8f0c033dd80460dd3a01a1122a64ee8710ada39b3ad375d08db223` | **HUMAN REJECT**。畫面頂部 y=0–56、底部 y=666–719 有全寬黑色 letterbox；即使主體內容適合，黑邊違反系列畫框驗收。 |
| `/workspace/.video-work/curio-s49/keyframes/moon044-1-trim.jpg` | `a86d16982330409a164f6e7d8112626be67c8589bdc80161889730ff8913174f` | **HUMAN KEEP，僅指畫面內容**。裁圖仍是 1280×720，頂部與底部已由場景像素填滿；逐行按每 16 像素抽樣，720 行都沒有全寬近黑邊。人、雙手與空圓形鑄模都留在畫內。 |

裁圖是一位灰鬢／灰髮、眉額與臉頰有成人面紋、肩寬明顯的成熟工匠；高領長袖工作衣與深色圍裙可作 1830 年代樸素工裝的卡通示意，沒有可見年代錯置。他把雙手放在**空**圓形鑄模邊緣並往內查看；模內沒有完成鏡片、可供觀測的鏡面或可辨識的赫歇爾真實器材。左側柔和暖光提供爐火／工場氣氛，沒有要求觀眾把光源認作史料中的特定熔爐。畫面保持 `cute-mystery` 的平面可愛卡通、低飽和暖暗色調；沒有可讀文字、數字、現代工具或現代服飾。人物和鑄模有一般卡通簡化，但未形成與旁白或固定來源相矛盾的物質主張。依 `curio-episode` 的「只退會誤導的圖」界線，**這張無黑邊裁圖的內容可用**；原圖的黑邊仍須退件。

## 機器狀態與後續守衛

查看時私人 `keyframes/manifest.json` SHA-256 **`8798fc406f8f737536a327c2a3ffa61d9d8bac8d5c2949962a5f37a0559b8533`**：`shots.moon044.file` 指向上述裁圖，`judge.overall=9.71`，但 `judge.passed=false`、`scores.frame=0`、`needs_review=true`，問題明寫上下黑邊。這是原始取樣的機器判斷；人工看到裁圖已去黑邊，不會把該失敗紀錄改寫成通過。

S49 是 `drama` 格式；`tools/video/media/keyframes.mjs` 的 `acceptBest()` 明確只准 `illustrated` 格式，對 drama 的 `--accept-best` 拋出 UsageError。故本次 **HUMAN KEEP 不能解除 TECHNICAL HOLD**，也不能手動改 manifest 的 `passed`／`needs_review`、把此裁圖升格為正式 KEEP 或繞過 storyboard 關卡。維持 STOP；任何後續圖單選取或新媒體嘗試都要走此格式允許的流程與既有預算／原尺寸守衛。本審沒有執行這些後續步驟。
