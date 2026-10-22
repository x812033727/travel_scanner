# S49 R35｜`moon036` 折射／入射角來源卡非作者紙審

2026-10-22 UTC。**PASS，僅限 R35 精確來源卡書面候選。**我不是 R35 作者；沒有修改 `video.json`、`claims.md`、任務、私有 manifest，也沒有出圖或付款。本紙審確認卡文字、來源界線、版面及 29 張既收圖；仍須安全離線回綁新 `visualHash`，後續圖片各自按原尺寸驗收，並不等於 storyboard 或成片通過。

## 來源與 R34 圖像退件

獨立重開固定 Locke 1859 年《The Moon Hoax》重印本 `/tmp/s49-moon-hoax-62779.txt`，SHA-256 `3ca0bc9b6fc5c50b090d61bf2049e925d22dd1cdef2b443a282f7fdc5749e654`。扉頁 L75 載 1859 年出版，L164–165 自述 1835 年 8–9 月先見於 *New York Sun*；P05 L417–422 的**虛構**對話，確寫 Brewster *hesitatingly referred to the refrangibility of rays, and the angle of incidence*。固定 Jacoby《Practical Talks by an Astronomer》`/tmp/s49-jacoby-53396.txt` SHA-256 `f5ab32e64e7ea3735ff90fb000ae8cc82dddea594e0de0c6be30b30f94485029`，J L4083–4108 引述同一段並明說是沒有可理解科學意義的想像光學對話。因此 `moon036` 不可畫成 Brewster 真實實驗、真器材或存世角度圖。

R35 保留口播「布魯斯特在文中遲疑，先提折射和入射角該怎麼辦。」；卡上標「1835 年報導的虛構對話」、主文「折射與入射角」、下標「1859 重印本所載，非實作紀錄」。三句是對上述史料的意譯及出處界定，沒有假裝逐字引句，也沒有把虛構討論說成真實光學結論。`claims.md` 同列亦明說不冒充實驗、存世圖紙或 1835 原報影像，與卡面相符。

獨立原尺寸查看 R34 第二張退件 `keyframes/moon036-1.jpg`（1280×720，SHA-256 `356fb638cbef0197a2b2ad58643f7971af80b71c63187589716d1ba8d66508f8`）：灰髮成年讀者與羽毛筆已有改善，但紙面兩條長線跨越大半紙、交成 X，筆尖未完成要求的小 V 第二短畫。與 [R34 停線回條](r34-moon036-native-stop.md)及[庫存](r34-moon036-native-stop-inventory.json)所記一致。來源卡直接撤掉易被誤認為歷史圖紙的角度畫，沒有花錢試第三張。

## 精確差分及卡片版面

獨立按 [R35 結構差分](r35-moon036-source-card-structured-diff.json) SHA-256 `b67a7ce2ec6546a52b300cce50dc8a29aac9f35ff4f9779ea3667556ec09f673` 核對兩個舊／新值。從 R34 Git `a9be49f74` 取原始位元組，把現稿 `scenes[32]` 反填舊 scene，再把 `claims.md` 的 `moon036` 新行反填舊行，兩檔都**逐位元組重現** Git 版。解析比較 129 景，僅 `moon036` 由 `shot` 改為 `big` 並換 `data`，其 `lines` 及其他 128 景、全域設定完全不變；131／131 口播 ID 與文字相同，speechHash 同為 `96f0b30e8cb408c7`。

| 檔案／繫結 | R34 → R35，或未變 SHA-256 |
| --- | --- |
| `video.json` | `c3c87e4a4a29627f596bb4108320c1f33b3694b6699cc9acd62dfd07b2c7fba4` → `fe4e3c2b3fd6691fa467d253965b4efa8c44c870582159fe110160dd16b029c3` |
| `claims.md` | `2718f55cdf7501a847a1cab51c88a07dfef0b1ed34209206a87a97442ad90313` → `824d15a121e9ca7ae147acfe60e1fa92e4e6aa871e70c788f9606c0750b0da79` |
| `script.md` | 未變 `82369f762cc64f70e300e2104a16af3b8e99f1e3296dd81a34152e967f0ecb0a` |
| `research.md` | 未變 `f5da15ac571478389b9b9920832f79434f83af0d312cb84747dcdb680a667750` |
| visualHash | `1c3c268eca8111e4` → `87f0c570cd6211b0` |

實跑 `VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s49 --json` exit 0：**0 errors、0 warnings、131 lines**。正文 128 景中 118 `shot`、10 卡，插圖比例 **92.1875%**，最長 **2** 張連卡，符合 `curio-episode` 的至少 70% 插圖／最多 3 連卡。獨立 `renderPlan` 核 `moon036` 是 `big` 的一個 `stills` state，實際可見文字含上述三句。再用本機 Chromium 於 **1920×1080** 載入同一 HTML、原主題 CSS 和字型：三行分別在畫面內，字型載入、外部資源無拒絕，內容區 `scrollWidth=clientWidth=1728`、`scrollHeight=clientHeight=778`，整頁無水平或垂直溢出。這是卡面版面檢查，沒有生成影片或付費圖片。

私有有效 `keyframes/manifest.json` SHA-256 `d1937dac303f4d5dd82ddcb1a4f5b6c5e797bcfba47ea25ad25d89697df2bd36` 仍綁 R34 `visual_hash=1c3c268eca8111e4`，有 **29** 筆 KEEP、沒有兩次退件的 `moon036`；依 R34 清單逐張核所選實檔 SHA，29／29 相符。`media/ledger.json` SHA-256 `91c21846627fffc589d57187fb7a39fb3e07bccd1ee1acc1e2a1a8c6e1c8913a`，逐筆合計 **US$1.1340／84 image／84 judge／0 預約**，低於整集 US$5.30；`media/jobs.json` SHA-256 `a9d2c69ab3cb5704417b4f0968a7d8d0dae6eb0e35d37e053463220b30d55ca3` 且空，`STOP` 在位。新卡讓已收圖單的 visualHash 失配，**須先在 STOP 下備份並安全離線回綁**，重核 29 KEEP 條目及所選實檔；本紙審沒有做該步，也沒有放行 `moon037–039` 批次付費、網站關卡或成片。
