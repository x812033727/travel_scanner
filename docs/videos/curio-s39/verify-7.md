# S39 R3a 提示詞限定修正交接

日期：2026-10-20。這是**作者的生成前提示詞修正收據**，不是獨立畫面覆核通過或圖片成品驗收；沒有生成付費媒體。

## 收到的 R3 獨立稽核

R3 的全新讀者先只讀劇本與官方敘事題，十三題 **13/13 通過**，封存於 `/tmp/curio_s39_r3_fresh_blind_seal.md`（報告 SHA-256 `b5d124c48420e366f01fdc311db39d0ecc3a5fe3a88eee892fe0dd7004037ea1`）。隨後的 `/tmp/curio_s39_r3_source_visual_audit.md` 從五份固定全文重新核字，判定 **89/89 句主張及來源通過**；86 個提示詞中 73 個通過，13 個因紙本表面沒有全幅明示空白而擋下開圖。原 R3 `video.json` SHA-256 `bb5cf9beb9990d430276d95ab1e7a12ae6936c4b1516eee3f5d41e8bf2092ad9`。

## R3a 鎖定與變更範圍

| 檔案 | SHA-256 | 相對 R3 |
| --- | --- | --- |
| `video.json` | `cefceb2ab42451f962bdad8f4910ac12b2aae849b927f6bc363c527e2d214264` | **僅 13 個鏡頭的 `data.prompt` 修改** |
| `script.md` | `f0b16c8dc9b5525fd07097851f1ec0c1e89f0987541c255cc2ef180afc19af28` | 不變 |
| `claims.md` | `52a3a091510c84fff3985fa09e43379ddb15a4ef0f9206a03fdddd84d8935139` | 不變 |
| `brief.md` | `52b2ed80008fc16dfb4570863b13fddc535ca9ff87a6bdadc489245d93c3b635` | 不變 |
| `research.md` | `fe4d68618a07222a1d44b546a575b8f0747d45838002c3dfdf0de095c12b71bc` | 不變 |

被點名的 `cs052`, `cs056`, `cs057`, `cs058`, `cs061`, `cs062`, `cs073`, `cs075`, `cs078`, `cs080`, `cs081`, `cs083`, `cs086` 均已在每個可見紙張、卷軸、書本或紙條上寫明「完全空白」或「無記號」；`cs075`、`cs078` 特別改成**整個可見書頁**空白，並非只要求下方邊緣空白。其他 73 個提示詞及所有 `lines`、`loops`、影片說明、配樂和來源欄位均未改動。這些空白文件供後製有來源的可讀字卡使用，畫面本身不要求生成假古文。

`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs script --slug curio-s39` 重生後劇本雜湊不變；`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s39 --json`：**0 error／0 warning**，89 句、估全片 9:20，開場 00:38 後至片尾章 09:01 為約 **8:23** 故事正文。

## 下一關

獨立查核者只需針對新舊 `video.json` 比較**確實只有上述 13 個提示詞改動**，逐字看這 13 個畫面的每個可見文件表面是否明示空白，再快速掃描其餘 73 個提示詞的單一主體、無偽造可讀字。R3 已通過的劇本與史料關卡以不變雜湊沿用；若審核者找到新增敘事或史料改動，應擋下沿用。提示詞重審通過後，才可進入後續音訊與媒體開工關卡；生成後仍須逐張檢查有無假字或人物混淆。
