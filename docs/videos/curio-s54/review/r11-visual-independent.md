# S54 R11｜單景修正獨立覆核

2026-10-20 UTC。**書面畫面 PASS**，只對下列五檔有效。此輪僅檢查 R10 的 `s54109` 畫面 HOLD 是否由單一提示詞修好；R10 的史料／主張 PASS 與劇本文字盲讀已有各自紀錄。實際生成圖、政策、旁白與站台審核仍是後續關卡。

| 凍結檔 | 獨立重算 SHA-256 |
| --- | --- |
| `research.md` | `412eef60918feb5c989d0e1675e8a6f7373ba9f720428cb9221d797d1975b60f` |
| `brief.md` | `5e234769e00988f427151afc953407ff52711df6c12c74043e64b67567509942` |
| `claims.md` | `6c1848776533319a8c2119c98d5c3320ca3574fb787ae220da4a6ad8ffb9d151` |
| `video.json` | `180f30aaf651eb2031271a8f934894facd85096abc034c20de74ba22e1a2d445` |
| `script.md` | `d48b818f3eefecf633f75f9a206bb10d22a212831b7855e902739da2e3b30938` |

把 R11 `video.json` 內唯一一次新提示詞

> `Close shot inside an April 1840 government planning office, an office assistant opens a blank calendar, gentle window light`

以 R10 舊提示詞 `Close shot inside a London receiving house in May 1840, a postal worker opens a blank April calendar, gentle window light` 逆向替換，所得 SHA-256 **精確為 R10 `video.json` 的 `67aec9cf177fe7a0639573dcf59249893f641cf51f70da152cd3ba0207fa59d6`**。另外四個凍結檔與 R10 位元組雜湊完全相同；旁白、主張、分鏡數目、其他畫面均未變。

`s54109` 仍唸「希爾回憶，四月二十二日財政部定下新時點。」[希爾原文 H 13328–13329](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13328-L13329)正是 4 月 22 日 Treasury Minute。新提示詞改為 **1840 年四月的政府規劃辦公室**，只畫匿名職員翻無字日曆；不再把決定畫到五月倫敦收件所，也不假裝重建可讀原件。R10 此景的書面畫面 HOLD 已解除。這仍只是生成前提示詞審查，不能代表未來圖像合格。

[R10 兩位隔離盲讀正式合併](r10-isolated-merge.md)的 **13/13 PASS** 綁定劇本文字 SHA `d48b818f...`；R11 `script.md` 與該 SHA 完全相同，因此**原讀者對文字的答卷仍適用**。若 `narrative` 命令另把整份 `video.json` 雜湊視為關卡依據，應在 R11 新分鏡檔上用原合併答卷重跑官方命令，不能冒稱已重跑。

`VIDEO_WORKDIR=/workspace/.video-work NODE_USE_ENV_PROXY=1 NODE_NO_WARNINGS=1 node tools/video/cli.mjs lint --slug curio-s54 --json` 回傳 **0 errors、0 warnings**；147 個敘事場，工具書面估計 13.896 分鐘。未做 TTS、插圖或媒體處理。
