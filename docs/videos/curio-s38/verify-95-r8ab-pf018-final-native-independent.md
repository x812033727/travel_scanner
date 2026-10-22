# S38 R8ab｜PF018 第三張暨最後一張原生圖獨立人工驗收

2026-10-22 UTC。**PF018 HUMAN REJECT。**我直接查看未裁切的 1280×720 原圖與目前 manifest 所選檔；兩者是同一個 JPEG。正式九題 judge 為 9.29／10、`passed=true`、`detached=10`，但機器評分不能替代這一景的動作驗收。這是 PF018 **第三張且最後一張實際原圖**；首兩張已分別在 [verify-87](verify-87-r8z-pf018-seed1-human-reject.md) 與 [verify-91](verify-91-r8aa-pf018-seed1-fail-stop.md) 退件，不能因換提示詞或重用 seed 1 再購第四張。本審只讀私人圖像、manifest、ledger、STOP、jobs 與固定史料；沒有付費呼叫、重綁、改動創意檔或私人媒體狀態。

## 圖像與敘事判斷

- 固定 Pepys 轉錄 `/tmp/curio-s38-pepys-4200.txt` SHA-256 `3cd43a3c39ee72eb9c4a3657f1fcb1723afba291cedac176c65a39289483be5d`，1666-09-02 L65816–65822 先記他坐船穿過橋，接著記眾人把財物投入河中，或 `bringing them into lighters that layoff`。現行 PF018 旁白是「他搭船沿河看，人們正把家當搬上平底貨船。」；它與 [R8ab 書面獨立紙審](verify-93-r8ab-pf018-final-independent-paper.md)核對的來源一致。`video.json` SHA-256 `b955dae2c2620b7477fcdef24606d9c1696f390c927f9fc7be10aa058d0b2ae9` 的 `scenes[17]` 要一名成年居民把木箱**越過低船舷向甲板內放下**。
- 原圖實見**兩名成年人**：左邊灰髮、面有皺紋，右邊亦有成年臉型與身形。兩人都抓著一只木箱的側把，蹲在寬而平的木船甲板上。木箱的底邊已落在兩人腳間的甲板，船舷橫在兩人及箱子後方；沒有岸邊交接、箱子跨舷、或從船外進到船內的可辨方向。因此畫面讀作兩人在**船內扶持或安置已上船的箱子**，未呈現旁白和日記的核心「把家當搬上／into lighters」動作。與第二張相同的核心缺口仍在，不能僅憑船上有箱子判作正在裝船。
- 額外一位成人偏離提示詞的「one resident」，但日記本來寫 `Everybody`，此處**不是**史料矛盾或獨立退件理由。箱子的木材、居民相貌與衣著也是示意，不要求日記逐項證實；沒有可辨為佩皮斯本人或聲稱他上了貨船。畫中低矮船舷、木甲板和河水可讀作平底貨船；未見明顯近代器物。畫面是系列的平塗可愛卡通，無照片、油畫、3D 質感或游離線段；原圖上下均有繪畫內容，**無黑寬帶**。退件只落在這一景必須讓觀眾看見的裝船動作，而非這些可接受的插畫細節。

## 位元證據與只讀停點

| 項目 | SHA-256／狀態 |
| --- | --- |
| 未裁切原圖 `/workspace/.video-work/curio-s38/keyframes/pf018-1.jpg` | `837607f332ad31e267e308135daa7b7d1799d9dbc6ecc6f26c6959eeddf86aa0`；1280×720 |
| Active manifest 入選 `keyframes/pf018-1.jpg` | 同一檔、同一 SHA `837607f332ad31e267e308135daa7b7d1799d9dbc6ecc6f26c6959eeddf86aa0`；無裁邊版可代替；manifest `sha256` 與實檔相符 |
| Active `keyframes/manifest.json` | `a1378645da92bc99af515237d315d9314fe294d5071e44e5621954d885012811`；`visual_hash=7f7b8b8dda0faefa`，目前含 11 個原 KEEP 加 PF018；manifest 收錄不等於人工 KEEP |
| 原 11 個 KEEP 完整條目 | UTF-8、Unicode 不跳脫、鍵排序 compact JSON 的 SHA `59cb354fcf4a4d38d746e4fc49e7dd39742d248ce1094d7de4d80a95f8a6e301`，與 [離線重綁清冊](verify-94-r8ab-pf018-final-rebind-inventory.json)一致；逐一讀取 11 個入選 JPEG，實際 SHA 均與 manifest 相符 |
| `media/ledger.json` | `aeabef894ef973efdfda24cc94a390586d422f1669cc8b4432e60e4f7f95a28f`；累計 US$0.8090、54 image、54 judge、1 music，另有 US$0.0035 舊 reservation |
| 停點 | `/workspace/.video-work/curio-s38/STOP` 在位；`media/jobs.json` 為 `{"jobs":{}}`，SHA `a9d2c69ab3cb5704417b4f0968a7d8d0dae6eb0e35d37e053463220b30d55ca3` |

正式 judge 在 `details=7` 指出兩人共搬敞口箱，其他項目均為 10。上述人體、船、畫風和無黑帶觀察支持其多數評分；人工退件理由是它沒有把箱子**搬入**船中的動作畫清楚。後續只可按已定停線保留證據並從 active manifest 隔離 PF018，再選同章已合格圖或日記來源卡，受正文插圖比例與連卡上限約束；本審不執行那些變更。
