# S53 R36｜`s53029` 成年建造者屋外驗門框獨立書面覆核

2026-10-22 UTC。**PASS，僅限本版 `s53029` 的固定來源、既定口播與書面畫面概念。**我不是 R36 提示詞作者；這不是第二張原生圖的 KEEP，也不核准其他景、圖單回綁、全片或發布。本次只讀，沒有購圖、judge、私有媒體修改或 Git 暫存。

## 來源及第一張原生圖

固定 1913 年 *San Francisco Relief Survey* `/tmp/s53-sf-relief/56217-0.txt` SHA-256 `d627ed287d8a93b9c00225ea47dbdc4f97c36089a890192a602b993c3c185b72`。[D L4858–4865](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L4858-L4865)記 1906 年 9 月 10 日動工，**9 月 16 日漢密爾頓廣場完成 20 棟小屋**；緊接著說仍需至少兩三個月，才有相當數量房屋備妥供難民使用。`s53028` 來源卡講開工，`s53029` 口播「六天後，漢密爾頓廣場先完成二十棟。」對得上這段先後。原文沒有指認某位建造者、門框檢查或 9 月 16 日的住戶；「相當數量尚待備妥」亦不等於斷言當日所有小屋都無人使用。

我直接看了 R35 第一張未裁 1280×720 原圖的私人備份 `rebind-backups/r35-s53029-first-native-rejected-original.jpg`，SHA-256 `6652f9899e861d54fdba6407f658e019280faaadeed7dc2690b993e8dc82e112`。畫面是一名童貌人物從有暖光的完成小屋門內探出，沒有成年建造者在屋外檢查門框，且屋立面而非門框近景佔畫面。此圖容易把「首批小屋完工」讀成來源未證實的當日孩童入住，故先前 HUMAN REJECT 的主體和時序疑慮成立。

R36 正向指定一位灰髮、有面紋、未戴帽的明顯中年以上成年建造者，站在一間**已完成的小型木救濟屋外**，一手試門框、一手扶門邊；上半身與門柱構成近景中心，室內為暗且無人的背景、光線改為陰天日光。這直接對準首張童貌、屋內視角、燈光和沒有驗框動作的失配。`claims.md` 明定為匿名**原創概念示意**，不把該人物、屋型、工序或入住情況說成史料記載；只畫一處門框並不冒稱逐棟呈現 20 棟。畫面選擇空室內不構成「20 棟皆空置」的歷史斷言。現稿仍用 `look.preset=cute-mystery`，未加 `look.style` 或 `look.negative`；景別、時地、一名成人的一項驗框動作及柔和自然光符合系列插圖寫法。文字限制無法保證模型成圖，第二張仍須直接看未裁原尺寸。

## 獨立 R35 → R36 版次核對

我直接讀 R35 Git commit `88b83988964fa235ef97d52915df32ba8dd4b586` 的三份舊檔，重新計算 SHA-256：

| 檔案 | R35 Git | R36 現行 |
| --- | --- | --- |
| `video.json` | `dc3bfba35e527d0206a56e78c5784fd8eab7d5fe38c97c59d233280e7861df79` | `601b54f492cb38ddf046f200f6bb02097868e25b9217605d2661abc33c1aa49e` |
| `claims.md` | `85eb3ce65fbef3746cd30a311d9af067968b32e5f5152a9c8c24e53d0a1200f9` | `0795312a9584486511f8695faeee7dda73863fd5ca64f705da99da5ccba6a745` |
| `script.md` | `64ffcd8c0e89c4596a7fd08d41bd74f8a16f55fbc9acc2f41d7f9b914ea300fc` | `64ffcd8c0e89c4596a7fd08d41bd74f8a16f55fbc9acc2f41d7f9b914ea300fc` |

`review/r36-s53029-adult-exterior-doorway-structured-diff.json` SHA-256 `0659203b3466efb8a0fec54eb8c1291a24030c215e60d7c48a08a09027e9f02d`。124 景中只有 `scenes[22].data.prompt` 的值不同，其他 123 景完整相同；`claims.md` 132 行只第 29 行 `s53029` 改動。差分的舊／新完整景物件與 claims 整行逐值吻合；在現稿將新景換回差分舊景，按現有 canonical JSON 格式序列化，逐位元組重現 R35 `video.json`；把 claims 新行反填舊行，同樣逐位元組重現 R35 `claims.md`。**126／126** 句 ID 與口播文字完全相同，`script.md` 同 SHA；現稿 `speechHash=05c4d9a79a8708b4`，私人 `timeline.json` SHA-256 `c75c8bde15f7220862ba8083d6590b7b14bb71c456f896f7b58c13352c88a054`、`narration.wav` SHA-256 `08444d50c2f8b70a7079701e157397d9a7c23d08971727164df91a1101e281e1`。

現稿 `visualHash=7a88c3a7a90cc951`。正文 123 景有 112 個 `shot`（91.1%），卡片最長連續 1 張；實跑 `VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s53 --json`：exit 0，**0 errors／0 warnings／126 lines**。

## 私有停線

只讀重算有效 `keyframes/manifest.json` SHA-256 `051f6055af0209948d665b095b1201ef37967c5c34c74cb2c3213292909dec59`，仍綁 R35 `visual_hash=76b75a45d888af0b`；**18 張 KEEP** 的所選實檔 SHA 全對，無 `s53029` 退件條目，尚未綁 R36。`media/ledger.json` SHA-256 `fb92ccb3157efcb91b384f86a3f03d0d184a0e6b8a6b956cbbaced369b694878`，逐筆合計 **US$0.6480／49 image／48 judge／0 預約**，其中 `s53029` 一次 image、一次 judge。`media/jobs.json` SHA-256 `a9d2c69ab3cb5704417b4f0968a7d8d0dae6eb0e35d37e053463220b30d55ca3` 且 jobs 空，`STOP` 在位。

**本書面 PASS 不等於第二張圖可用。**後續若進入受控第二次原生圖，須先安全離線回綁及額度預檢，然後看未裁原圖與 judge 是否真的呈現成年屋外驗框、完成但不暗示入住的小屋及一致的 2D 畫風；退件即停下窄修，不把本紙審當成選圖核准。
