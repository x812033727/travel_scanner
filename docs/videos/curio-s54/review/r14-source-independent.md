# S54 R14｜`s54135` 獨立定點史料覆核

2026-10-20 UTC。**史料 PASS；書面畫面 PASS。** R13 唯一來源 HOLD 是 `s54135` 把預先備好的封套歸給希爾本人。本輪核作者 R14 凍結的定點修稿；沒有改口播、主張、畫面或媒體。本結論只放行來源和書面畫面，不替代兩位新稿敘事盲讀、實際出圖或 TTS 品管。

| R14 凍結檔 | 獨立計算 SHA-256 |
| --- | --- |
| `brief.md` | `bedc89ef669f9b64868ff3ccea85adb13ee07d75a1ab2120ab6193079f4623f9` |
| `research.md` | `8bd0b5be9efe77b440b3677ba60b26fa97e9b6de47e8fcfc7b3f6284796eb6ae` |
| `claims.md` | `46d2e01f36e1f79263bcf2be686729a48e4dae3e7e628c492bddef3257b133f3` |
| `video.json` | `ab07d7166dc1141a822747dfd43d46675fa9f5c97ce3cff528875df48764a83b` |
| `script.md` | `483558f1617939d109c453ec35f09840ed3de9bcbf0455aa1598433f9b74448f` |

`s54135` 現為「另一頭的印刷廠也被需求逼緊：**先前備下的大批封套**，居然派不上多少用場。」`claims.md`、`video.json`、`script.md` 三處逐字相同。[固定 Hill H 13390–13399](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13390-L13399) 說實際產量追不上需求、附膠郵票更受歡迎，於是 *the great stock of covers which had been prepared proved of comparatively little value*。新句既保留供需與封套價值的原意，也不再指定未經原文證實的備貨者。`research.md` 的 P11 同樣只說「原先準備的大量封套」。本地 Hill 固定全文 SHA-256 `3bdf96943eea935aec86101874f15aa8f60d518db1437902da52b446f006f939`，與 R13 重新下載的原文及研究檔相同；固定法案、Leavitt 全文 SHA 也分別保持 `f19541ff9faab28b3d61739f09e23b40115fe2220eda870c2d7cd0867758e254`、`cc4b05beb60da3f29bc3565b9bdcefa8a643bf972454c7c0a14690f5bdd49d5e`。

`s54135` 的書面 `data.prompt` 只畫 1840 年五月印刷廠中一位印刷工人堆放無字預付封套，沒有讓希爾扮演備貨者，亦沒有可讀官方庫存紀錄。其餘 R13 受影響畫面的定點史料及書面視覺結論見 [R13 獨立覆核](r13-source-independent.md)；R14 沒有增加新的歷史主張或畫面斷言。這是書面提示詞 PASS，實際生成圖仍須另審。

重新比對全片：145 個唯一敘事 ID，`claims.md` 與 `script.md` 對 `video.json` 口播各 **145／145 逐字一致**；138 個插圖景、7 個工具字卡、24 組 loop。第一章濃縮開場 153 漢字，排除開場八句與片尾的正文 2,643 漢字；按每分鐘 325 字為 **8 分 07.94 秒**，這是書面估計而非 TTS 實測。`node tools/video/cli.mjs lint --slug curio-s54 --json` 回報 **0 errors／0 warnings**、7 章、148 句、工具估 13.9194 分鐘。

R13 的 `s54135` 來源 HOLD 已解除。R14 五檔雜湊須供兩位乾淨讀者重新盲判 13 題；`/workspace/.video-work/curio-s54/STOP` 仍在，舊六句 TTS 草稿不屬於此稿，須待敘事及後續媒體關卡完成。
