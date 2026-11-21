# S58 R2｜P01 引文定位修正凍結收據

2026-10-20 UTC。R1 收據 `r1-author-freeze.md` 保留原貌；本收據取代 R1 作為**後續獨立覆核的作者候選版本**，不是作者自審 PASS。

## 唯一變更

Reitlinger 固定原文的 1870 年 10 月 28 日出發日期在 **L514**（同書 L408 也預告當天出發）。R1 的 P01 引文 R535–573 涵蓋郵袋與風向，卻不含該日期。R2 將 `research.md` 的 P01 和 `claims.md` 八處 P01 連結統一擴為 [R510–573](https://github.com/GITenberg/A-Diplomat-s-Memoir-of-1870-being-the-account-of-a-balloon-escape-from-the-siege-of-Paris-and__49546/blob/d29b4c2d9670430fcc4b2e5a9e3e39a9e7542f18/49546-0.txt#L510-L573)，並標記 L514。原文位元組 SHA-256 仍是 `ae2c78eb08b76fdac59b91ebdf6b6a187f8ef18649e4d78d461f140467bdb7f7`。故事、分鏡、口播、企劃皆未改。

| R2 凍結檔 | SHA-256 | 相對 R1 |
| --- | --- | --- |
| `research.md` | `8a1db1dc2a9441a7b16683c70067203ddc7be6c0070560f32c02d91b5e32de34` | P01 行號擴大並註明日期行 |
| `brief.md` | `7b44818f6b681a4ee786c00a32359b4181772aeaa1b5cd897bcd13871b1ad016` | 相同 |
| `claims.md` | `73f9ea7122ec728357b7eb3c8487b9657b4bbe0e6d140c4b0514a7deddc2d471` | 八處 P01 引文擴大並註明日期行 |
| `video.json` | `d69ce07f441aeabddc231d4d98fe4437ffea4e7c763198d2a61be1161bebe0cb` | 相同 |
| `script.md` | `9d590c8c3e6f93628d87d4618276ee967364aa36e0b54c7008c9266b6daae0ac` | 相同；narrative `e41d386112b07a74` |

R2 驗證：156 句 `video.json` 與 `claims.md`、`script.md` 逐字逐 ID 對齊；八處 P01 引文皆指 R510–573；原文日期 L514 已對照固定全文。`lint --slug curio-s58`：0 errors、2 個既存不同語義數字詞重複提示。`npm run test:docs-videos`：236/236；`npm run check:tasks`：exit 0，其他既存任務警告；五檔無行尾空白。作者未開始語音、插圖、配樂、合成或付費媒體。

下一關：非作者以此 **R2 五檔 SHA** 獨立覆核史料與書面畫面，再做兩位無前情讀者盲讀與正式核准。若五檔再改，需建立下一版收據和重跑覆核。
