# S38 R8l｜`pf007` 蠟燭與窗邊近景窄修

2026-10-21 00:46 UTC。**作者候選，未自判來源、畫面或原生圖片 PASS。**承接 [R8k 原生停點](verify-29-r8k-pf007-native-stop.md)，只改 `pf007.data.prompt`：從易產生 3D 與現代電燈的整間臥室，改為一位成年男子穿素面睡袍走向木窗，單支蠟燭照亮臉與灰泥牆，窗外是拂曉。新蠟燭、橡木桌和灰泥牆只作概念場景，不宣稱是佩皮斯住屋的精確復原；日記 D2a 的 Jane 叫醒、佩皮斯穿睡袍走向窗邊及認為火遠的先後不變。系列 `look` 未改，提示詞不寫畫風字。

[結構化單葉差分](verify-30-r8l-structured-diff.json) SHA-256 **`964f8e8987b05973d93af7495bb3c3c5a9205af67e939884eeced05f4012420f`**。將目前 `pf007` 唯一新提示詞原始位元組換回 R8k，整檔 SHA 精確回到 **`d98065c80a7153ce252bcb77d06cf6fb72d7bb51c0d1931ed70c25493e79a6f3`**；解析 JSON 僅 `scenes[6].data.prompt` 一個葉節點不同。R8l `video.json` SHA **`2e9ec8c6f2962b420719ef62185d38def7f915bac3fac2e55fb0f16b231c6778`**、`visualHash` **`859769ddb7cef27f`**；`research.md`、`brief.md`、`claims.md`、`script.md` 沿用 R8j 的四個 SHA，未修改旁白與音訊。

`lint --slug curio-s38 --json`：**0 errors／0 warnings**。`STOP` 在，ledger 仍 **US$0.3165**（含 `pf003` US$0.0035 reserved），整集上限 US$4.58。請未撰寫者先核日記 D2a、原生退件、快取、唯一差分及提示詞；若紙上 PASS，最多一次 `pf007` **1 take＋1 judge**（約 US$0.0135），原生判退立即恢復停畫。第一章 28.90 秒、其餘未畫景及網站音訊／分鏡核准都仍 HOLD。
