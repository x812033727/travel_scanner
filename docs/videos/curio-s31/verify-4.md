# S31 R3｜敘事去重修稿交接（四）

2026-10-20。R2 的全新盲讀在 13 項官方敘事問題中得到 12 項 YES；唯一未過的 `no_recap` 指出 ly063／ly066、ly054–ly057／ly090、ly083／ly091 重述相同資訊。這份 R3 交接記錄針對該盲讀修稿，**新文稿仍待另一場全新盲讀及獨立來源／分鏡核查**。前一次來源問題與 R2 修法見 [verify-2.md](verify-2.md)、[verify-3.md](verify-3.md)。

## 凍結文稿

| 產物 | SHA-256 |
| --- | --- |
| script.md | `cfc5a32d15d7e5cca20f972aca6dfdb2810a96fe8791d23c70da2188d20dfb5a` |
| video.json | `9847d87ff094cd3b84c399c997f8de2c437264a4f78d54aed5c38c4eb75bc8b5` |
| claims.md | `addcf78f2ded2e3a8778b7c59b176151a15742c09de52ea9803534c53a03f72f` |

固定古籍版本、全文 SHA-256 與每種文本的證據上限沿用 [research.md](research.md)。R3 沒有另添史料或改變核心結論。`script.md`、`video.json`、`claims.md` 的 97 個旁白 ID 與字串一一對齊；正文 96 景均為 still shot，另有片尾一景。18 條問題與回收仍在；系列 lint 為 0 errors、0 warnings，估全片 9.3 分鐘，片頭約 45 秒，正文約 8 分 30 秒。

## R2 盲讀指出的重複與 R3 修法

| 位置 | R3 實際改動 |
| --- | --- |
| ly063 → ly066 | 保留 ly063 的圖序受眾，ly066 改成作者描完果肉汁液後把筆轉向「離本枝」的文字次序，不再重說沒趕上鮮果頭幾日的人。畫面改為學者翻向無字新頁。 |
| ly054–ly057 → ly090 | 地理志段已說廣州貢品不能定位貴妃那一籃；ly090 改成「我試著添一條虛線，才發現它也替那籃果子指定了方向」，讓結尾發生一次具體但撤回的落筆動作，不再重念地名和來源上限。提示詞只讓筆停在無標記地圖上。 |
| ly083 → ly091、ly092 | ly083 仍回答巴峽能否作送果起點；ly091 擦掉地圖邊緣的短筆痕，ly092 問擦後還能留下哪一筆，不再重說巴峽文本的界限。 |

R2 敘事盲讀的獨立封存回執位於 `/tmp/curio_s31_r2_narrative_blind.md`，只供追溯舊稿失敗原因；它不能當成 R3 的通過證明。R3 需以本頁 exact script SHA 重做官方 13 題，另一位讀者需以本頁 exact script/video/claims SHA 核查全部逐句來源及 96 個提示詞。兩關都完成前不開始音訊、生圖、配樂、合成或其他付費媒體。

## 本輪本地核對

- `VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s31`：0 errors、0 warnings；章節從 00:45 至 08:02 接續，估全片 9.3 分鐘。
- 逐項比較 `script.md`、`claims.md`、`video.json`：97/97 ID 順序與旁白字串相同；96/96 正文 still shot、18 條 loops。
- `npm run test:docs-videos`：236 pass、0 fail。`npm run check:tasks`：exit 0；其他工作票有既存的持有時間／範圍警告。`git diff --check`：無空白錯誤。
