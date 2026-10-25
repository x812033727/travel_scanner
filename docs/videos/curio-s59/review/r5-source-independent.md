# S59 R5｜單景差分獨立史料與書面畫面覆核

2026-10-21 UTC。**史料與 110 句逐字對照 PASS；書面畫面仍 HOLD，僅 `s59027` 的「紙盤自身有淺螺旋槽」暗示未釐清。**我沒有寫 R5 提示詞、修改五份創作檔、呼叫付費媒體或核准網站卡片。這個判定只對下列精確版本有效。

| 創作檔 | 實測 SHA-256 |
| --- | --- |
| `research.md` | `d0077504f3dbe828363158a25c7e7dade955089f49dbb03a734893739e12467e` |
| `brief.md` | `9d68d7b4dad27f56b6dbc53f7890bc0db84590de3e445302f8f4836c286ac1e3` |
| `claims.md` | `e19a8aa75c7d61bbba54b4d747db3b7025ac34599964ac0c4c115fbacd8d8c0b` |
| `video.json` | **`77a9ab9de42dd36f9af3b94a6c28312e18e6f846418e38ee2fe0d9ace30b06f7`** |
| `script.md` | `5b18eb40b5c3434599abbd939d3231fc30837e360bfaff0ea00d23cdca89cf48` |

## 差分與來源重驗

我直接讀 R5 `video.json` 原始位元組，把 [作者差分](r5-author-structured-diff.json)所列新提示詞唯一出現處換回 R4 舊字串，重得完整 R4 SHA-256 `108db5d8ae5b540e396b1e9add3490c7ac8761e1aaa7dfd76b172edbadaba226`。解析 JSON 遞迴比對**恰只** `scenes[26].data.prompt` 一個葉節點不同；R5 `visualHash` `7417dce22257dbfe`、R4 `6c891383737963b9` 均自行重算相符。其餘場景、110 句台詞、來源、畫風、章節及片頭片尾完全相同。`lint --slug curio-s59 --json` 實測 0 error／0 warning。

我重新下載固定 GITenberg 原文 E（1910 愛迪生授權傳記）及 D（1878 杜蒙塞爾），原始位元組 SHA-256 分別為 **`9818547c6dd15e488c1923bad5cc09cb4fa3f447641daaaf77b2f539b4d49d34`**、**`c48361e94523ebacc000172ebab34895bb20c0b7e458ac3e122f90a3cc9e717c`**，與 `research.md` 的固定值吻合。R4 [獨立覆核](r4-source-independent.md)已在同一四份未改文件和原 R4 `video.json` 上核對 110／110 句、122 個固定引用及其他 99 張插圖／10 張卡片；上述**精確單葉差分**表示那些文字與畫面不受 R5 改動，史料／逐句 PASS 可沿用，惟新提示詞必須另判。

## `s59027` 尚有一處介質錯置風險

[E5195–5206](https://github.com/GITenberg/Edison--His-Life-and-Inventions_820/blob/b100fab326616897d87d7e296672f5f916624d32/820.txt#L5195-L5206) 明說：**螺旋槽在承托的 platen 上**，上面另放一片**紙盤**；訊號的凹凸壓在紙盤上，重播機使用 contact point 讀取壓痕。[D6935–6953](https://github.com/GITenberg/Le-T-l-phone-le-Microphone-et-le-Phonographe_27574/blob/825f6fa891c8a23d957829a717c37a6af1dea2ae/27574-8.txt#L6935-L6953)則描述後來的**圓筒錫箔**：針走過壓痕使薄片再振動。兩層來源與稿中條件式問題可相接，但不能把紙盤畫成後世有刻槽的唱片。

R5 已把 R4 錯誤的**手指讀槽**換成「成人發明者觀看、播放針在上方」，這一點和「能不能重播」的未解問題相容；一人一動作且沒有風格口令，也沒有提早畫成播出成功。然而完整新提示詞說 `a stationary paper disc with a playback needle poised above **its shallow spiral groove**`。`its` 的自然指涉是紙盤，會要求模型在紙盤**本身**畫一條淺槽；固定 E 的槽是在紙盤下方的承盤，紙盤上應是**壓出的訊號痕**。這個差異會把紙盤電報的概念畫成唱片式槽，不宜靠後續機器評分猜模型如何理解。因此本版書面畫面 **HOLD**。

建議只把該景改成「一名成人觀看紙盤上**沿螺旋路徑的凸起壓痕**，播放接點停在壓痕上方、雙手離開紙盤」的靜止概念景；也可明說下方承盤的螺旋槽，但不要再稱它為紙盤的槽。仍不畫可讀字、成功播放或未經來源證實的巴黎現場動作。修正後要凍結新五檔 SHA，讓未撰詞者重核確切葉節點；R5 敘事盲讀或政策判定也必須綁到新版本。**本 HOLD 阻擋付費語音與插圖；不替網站站主做核准。**
