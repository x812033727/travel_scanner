# S62 R15｜夜景修復後剩餘原圖覆核與 STOP

2026-10-22 UTC。**`s62028` 機器 PASS 但原圖把木星旁靜止細點畫成帶拖尾的飛過光體，已立即設 STOP。**R14 的 `s62023` 白晝圖先前人工 REJECT；R15 最後一次實際重畫已由製作方另記[夜景 KEEP](r15-s62023-final-native-keep.md)，共 3／3 actual，不在本票重判。`s62024` 原問題快取經 judge PASS，製作方已按一般夜空／觀測者示意接受，並不把背景普通星點當精確原始目鏡圖。本票只覆核 R15 新付費出圖 `s62025` 起；普通匿名 chibi、ruff 與道具簡化不另退。

| 景 | actual | 原圖 SHA-256 | selected SHA-256 | 獨立判定與依據 |
| --- | ---: | --- | --- | --- |
| `s62025` | 1/3 | `5d247ec4eb2a7511da886be8a4e9d218c56a062b5c9267cd395aa16eba160149` (`s62025-1.jpg`) | 同原圖 | **KEEP。** 1610 服飾的匿名學者在素紙前持筆／指示，可作方位敘述的過渡示意；下一景來源卡才具體標示東二西一，這張素紙不冒稱精確原始星圖。明亮庭院在此讀作整理圖解，無即時夜間觀測動作。 |
| `s62027` | 1/3 | `a63300d21d27304d6841e4d5ba8b8284ecba3247e02ee4ab75d09d65cbdc7d07` (`s62027-1.jpg`) | `d139c35deff3622b261506ad86ebe6c6fd1ca1f4a5629c3be651ee25873b3735` (`s62027-1-trim.jpg`) | **KEEP。** 暮色天窗、數個普通淡點和疑惑的學者，能示意他當時仍把細點當背景恆星；未畫成帶標號的原始觀測圖。選裁保留人物與天窗。 |
| `s62028` | 1/3 | `823a1d703360238dd9e08de5f0e2e3deed35a65a09cdb1b2f632b3b4e9c20ab1` (`s62028-1.jpg`) | `567c21f164337957ea1cad7efee95263d436744af5f68aadabf884beb84565c2` (`s62028-1-trim.jpg`) | **REJECT／STOP。** 旁白是「三點排得整齊、又比旁邊細星亮，才讓他多看了一會」，承接木星旁近乎固定的三個小光點；圖中卻只有一個極亮光體帶長尾橫劃夜空，明確讀成流星／彗星式掠過，而不是一排細點。原圖與選裁都保留長尾，這是核心天象錯誤，不能因機器 9.29 PASS 接受。已用 1／3，剩 2。 |
| `s62029` | 1/3 | `3ee503c105a1e63937e45833320a661ec8d97ce57aa670dfdaf40ddb9af370e4` (`s62029-1.jpg`) | `f026bf668c8ac53b65cff81cf6df022f83a7f7b8dce18f66fab3a334f6841f92` (`s62029-1-trim.jpg`) | **KEEP。** 早期服飾人物面對空白紙頁，與「第一晚沒有細量距離」相容；分規省略只是普通道具簡化。選裁未引入任何數字或假星圖。 |
| `s62030` | 1/3 | `ec78b10ff395ce3f424d5e8a18699c8c6c56439af2d9cd11adcfedf2c0f46d3d` (`s62030-1.jpg`) | **無 selected**：STOP 前 image ready，未 judge／未寫入 manifest | **HOLD，非 KEEP。** 原圖有空白簿頁和 1610 式領口，對「缺舊位置」的語義未見立即重大錯誤，但皮膚／背景偏立體柔光；須由正式 judge 後再核原圖與選用狀態，本票不先接受。 |

R15 log 寫 `stopped by the STOP file after 5 new keyframes`：`s62025`、`s62027`、`s62028`、`s62029` 各 1 次 image／judge，`s62030` 1 次 image ready 未 judge。停止時 `STOP` 在位、`media/jobs.json` 為 `{"jobs":{}}`；總帳 **45 image／44 judge／US$0.5975、零預留**。本輪 3 KEEP、1 REJECT、1 HOLD；`s62028` 修圖前不可直接擴批。manifest SHA-256 `fed66bbb5805a62a120e2369488408c72ee756ea7945e51efb5e86ee2d6cea76`；`video.json` SHA-256 `9fa0b2fc205310c5389b4611043be82c2590b773a3d6df7f58e2acf3c6a5a257`，`claims.md` `1565041acc73dedfbe70c3bec542ba49d621ff4e437dc804b5332e2bcf561354`。未改 creative、manifest、媒體帳本或已選圖，也未呼叫付費工具。
