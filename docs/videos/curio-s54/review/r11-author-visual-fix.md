# S54 R11｜作者單景畫面修正凍結

2026-10-20 UTC。[R10 雙盲正式合併](r10-isolated-merge.md) 對劇本判 **13/13 PASS**；[R10 獨立來源與書面畫面](r10-source-independent.md) 判旁白史料及主張對齊 PASS、畫面 **HOLD 僅 `s54109`**。作者只修該景提示詞；本紀錄不宣告 R11 獨立畫面、實際生成圖、政策或媒體 PASS。

| 凍結輸入 | SHA-256 |
| --- | --- |
| `research.md` | `412eef60918feb5c989d0e1675e8a6f7373ba9f720428cb9221d797d1975b60f` |
| `brief.md` | `5e234769e00988f427151afc953407ff52711df6c12c74043e64b67567509942` |
| `claims.md` | `6c1848776533319a8c2119c98d5c3320ca3574fb787ae220da4a6ad8ffb9d151` |
| `video.json` | `180f30aaf651eb2031271a8f934894facd85096abc034c20de74ba22e1a2d445` |
| `script.md` | `d48b818f3eefecf633f75f9a206bb10d22a212831b7855e902739da2e3b30938` |

`s54109` 旁白仍是「希爾回憶，四月二十二日財政部定下新時點。」畫面由 `Close shot inside a London receiving house in May 1840, a postal worker opens a blank April calendar, gentle window light` 改為 `Close shot inside an April 1840 government planning office, an office assistant opens a blank calendar, gentle window light`。這是 4 月決策的概念示意，不假裝重建決策原件或可讀公文。R10 的其他場景、旁白、主張、日期、來源與片尾均未改。

位元組檢查：把 R11 `video.json` 中唯一一處新提示詞替換回上述舊提示詞，所得 SHA-256 精確等於 R10 的 `67aec9cf177fe7a0639573dcf59249893f641cf51f70da152cd3ba0207fa59d6`；其餘四個作者輸入的 SHA-256 亦與 R10 相同。重跑 `VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs script --slug curio-s54` 後，`script.md` 位元組雜湊仍是 R10 原值。`lint --slug curio-s54 --json` 為 **0 errors、0 warnings**，7 章、147 敘事場、工具書面估計 13.896 分鐘；開場 151 漢字，後續正文 2,631 漢字，325 字／分估 8.10 分鐘。

下一位工作者只須獨立重查本景書面畫面與新 `video.json` 雜湊的綁定，再處理後續關卡。沒有合成語音、繪製付費插圖或送出影片。
