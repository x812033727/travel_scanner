# S53 R39｜`s53029` 縮短來源卡主標獨立書面覆核

2026-10-22 UTC。**PASS，限現行 R39 `s53029` 主標及 `claims.md` 同列所引文字。**我不是 R39 作者；按新 SHA 直接核固定 Survey、[R38 非作者 PASS](r38-s53029-september16-source-card-independent-paper.md)、R39 實檔／差分、1920×1080 截圖和私有停線狀態。沒有改動作者檔、正式圖單、帳本或媒體，沒有付費呼叫、Git 暫存或提交。

## 來源與可讀性

固定 `/tmp/s53-sf-relief/56217-0.txt` SHA-256 `d627ed287d8a93b9c00225ea47dbdc4f97c36089a890192a602b993c3c185b72`。[D L4858–4865](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L4858-L4865) 在 1906 年建屋段落寫 `Building began September 10, and on the sixteenth 20 cottages in Hamilton Square were completed`；下一句分開指出，至少兩三個月後才有相當數量備妥供難民使用。R39 主標「9 月 16 日，20 棟小屋完工」明說日期、數量與完工；上標「1906 年｜舊金山漢密爾頓廣場」完整交代年與地點；下標「1913 年《舊金山救濟調查》｜英語原文意譯」把後出調查與 1906 年事件分開。口播仍明說漢密爾頓廣場。卡面合讀不聲稱當日已入住、全市僅 20 棟或該 20 棟全未使用。R38 PASS 收據 SHA-256 `ddf9749567e8381ac33076d3f066dfdba8a3723d55a408853eae3feac9fbedab` 對既定口播「先」及下句「得再過兩三個月才」的語境判定仍適用；R39 未更動兩句。

我直接看 `/tmp/s53-r39-s53029-card-smoke.png`，SHA-256 `deae60723fd2eda033a508ace6e708e2b949a158edbd78116c262cdefa153994`，並以現行 `slideHtml`、本庫 theme／Noto 字型與本機 Chromium 另行重繪 1920×1080 畫面，得到**逐位元組相同的 PNG SHA**；字型載入完成，內容盒 scroll/client 同為 1728×778。此圖僅是本地版面煙測，非正式影格或史料影像。上標「漢密爾頓廣場」完整同列；主標分成「9 月 16 日，」及「20 棟小屋完工」，R38 的「爾／頓」斷字已消失。日期、數量與完工均清楚，未見裁字、文字碰撞或標籤缺失；此版面改善成立。

## 精確版次與系列檢查

現行 `video.json` SHA-256 `7ebd094e7bd89ba3ebf036440385ffb6f54aa3f8bdf746b30bbcc91c7d72ba10`；`claims.md` SHA-256 `7ea2850176e7e8a27e10fa7807db0007358f52868eb3f8bedd87ca8a711820f4`；[R39 精確差分](r39-s53029-short-main-card-structured-diff.json) SHA-256 `e6c6d950b7ae5faec1b4b8dde8282057266f08384add7fe39704233b929dff24`。實檔的 `scenes[22]`／`s53029` 與差分 `after` 完整相符；其 `id`、`template=big`、`lines`、`kicker`、`sub` 全與 R38 `before` 相同，只有 `data.text` 由「9 月 16 日，漢密爾頓廣場 20 棟完工」縮為「9 月 16 日，20 棟小屋完工」。其他 **123 景**未改。`claims.md` 第 29 行 `s53029` 與差分 `after` 完整相符，僅同列引用的主標替換；其他行未改。將差分 `before` 場景反填並按實檔兩格縮排、非 ASCII 不轉義、尾端換行格式序列化，逐位元組還原 R38 `video.json` SHA `212aa5d440e5c6075af9341ab271e40323d81537cd229acf693f17fc3d2bdc31`；把 claims 舊整行反填，逐位元組還原 R38 `claims.md` SHA `e8892539610547dc8e6242b441b1028f6bb5865b2dd25e9c1fc9f05234285fed`。

`script.md` SHA-256 `64ffcd8c0e89c4596a7fd08d41bd74f8a16f55fbc9acc2f41d7f9b914ea300fc`；126／126 句 ID、文字及語氣均不變。用正式 `loadProject`／`speechHash`／`visualHash` 重算，`speechHash=05c4d9a79a8708b4`、R39 `visualHash=09c82f30136ccbde`。私有 `timeline.json` SHA-256 `c75c8bde15f7220862ba8083d6590b7b14bb71c456f896f7b58c13352c88a054`，仍記相同 speech hash；`narration.wav` SHA-256 `08444d50c2f8b70a7079701e157397d9a7c23d08971727164df91a1101e281e1`。實跑 `VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s53 --json`：exit 0、**0 errors／0 warnings／126 lines**。正文 **111／123 `shot`（90.2%）**，高於 70%；最長連續卡片仍是 `s53028–s53029` **2 張**，低於最多 3 張。

## 18 KEEP 與停線

正式私有 `keyframes/manifest.json` SHA-256 `674e1ca36d3d028ddd120b2c93737b52f55d41ab83d8f644d8835303c5b287d3` 仍綁 R37 `visual_hash=eb73bd967a3b4a7d`，**尚未回綁 R39**。我把 18 筆 ID／所選路徑／SHA／request key 逐筆與 [R37 STOP inventory](r37-s53029-third-native-stop-inventory.json) SHA-256 `dca470c6d626cb8f41e9ab69bfba8f1d62fcef744365ddee96fcc88a414c5c40` 比對，並重算 18 個所選實檔 SHA：全相同；`passed=true`、`needs_review=false`，有效圖單沒有 `s53029`。R37 第三／最後原生圖 HUMAN REJECT 的決定不因字卡改版而變，也不開第四張。

私有 `media/ledger.json` SHA-256 `168c8be9e142222df00780bbee50957126207875d14894aaee0551e1e256e0b5`；逐筆重加 **US$0.6750／51 image／50 judge／0 預約**，低於 US$4.78。`media/jobs.json` SHA-256 `a9d2c69ab3cb5704417b4f0968a7d8d0dae6eb0e35d37e053463220b30d55ca3` 且 `jobs={}`，`STOP` 在位。此 PASS 僅結束 R39 紙審；若採用候選，正式圖單仍需在 STOP 下另行備份、離線回綁 R39 visual hash 並核 18 KEEP。
