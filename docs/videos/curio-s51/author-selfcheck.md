# S51 作者凍結檢查｜2026-10-20 UTC

**狀態：**作者前製已完成並固定；這份自檢**不等於**獨立史料審核、兩位不同盲讀者的敘事審查、網站大綱／劇本核准或成片驗收。原 Amber Room 題因來源網域目前代理 CONNECT 403 而延期，詳見[原題票](../../../tasks/open/2026-10-20-curio-s51-amber-room-source.md)。S51 改為加州人號求救火箭題。

| 內容檔 | SHA-256 |
| --- | --- |
| `brief.md` | `82a2e4a3d7a240dd0f249eeeec3b3dffdf1446d9eb049432320e72fe6b6a1023` |
| `research.md` | `039ca3ecc3f5099537e51e48d0f1788faf0bdf9c5d254f2ae64dd5ff89b56459` |
| `claims.md` | `21dd50280e0d89ca998a9cf5a0820589b6ae5ffbf233e49ba988aa6dd477dad1` |
| `script.md` | `5b6c6d0924670033b379c40a00f4ae3991d920661a5479631e5ba2e3143de42b` |
| `video.json` | `1639fd758d59f44b7dbae66603f1148c3abf7dd6229f16b32b3c5b34bdcf20df` |

## 來源與論點

- 作者直接重開三份固定文字：[1912 年英國正式調查](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt) 原始 SHA `5ac8c66266f84fb1fd01f50aab93044526c369df0d876c7e24dd20451f0053bd`；[Beesley 1912 年自述](https://github.com/GITenberg/The-Loss-of-the-S.-S.-Titanic--Its-Story-and-Its-Lessons_6675/blob/98d777343615ef35522ca8e04e451ec5d7f37eb3/6675.txt) `58062b750f1737ac908af48f3ec81016353404631978dc419138a5a2ef7a5ce9`；[Gracie 1913 年自述](https://github.com/GITenberg/The-Truth-about-the-Titanic_67584/blob/a2cbb33f09c5ce0ff00a78581a56cb6756967c42/67584-0.txt) `d9ab71205530a5df41dddf74090e598fcc4de06efba9eb234bffa07f20a61a1f`。原始文字臨時檔在 `/tmp/curio-s51-sources/`，不是倉庫交接的唯一依據；固定 GitHub URL 和 SHA 已寫入 `research.md`。
- 主張邊界：火箭約八枚；加州人號船橋有人看見白色火箭；Stone／Gibson 與 Lord 對通報數和時刻有矛盾；英國調查**認定**他們看見的是鐵達尼號，且當夜未出航。船長當夜是否辨出船名、精確距離、若出航能救多少人，皆不寫成已證事實。電子轉錄的一處經度疑似誤植，腳本不用坐標。
- 倖存者 Beesley 只直接證實自己從鐵達尼號看見火箭；他對鄰船的判斷與 Gracie 的指控都屬事後論辯。獨立來源審核仍須逐行覆核這些邊界。頻道 URL 依既有 Curio package，未把它當歷史證據；來源及頻道 URL 均已放進說明欄。

## 稿件、時長與畫面

- `node tools/video/cli.mjs lint --slug curio-s51 --json`：**0 errors，0 warnings**；工具估全段 11.59 分鐘、140 句、10 章。自寫對齊檢查：`video.json`、`script.md`、`claims.md` **140/140 逐句同文**；12 組 `loops` 回收均在埋設之後。
- 正文 137 景全部為 `shot`（**100%**）；最後另有一景 `outro`。日間文件覆核鏡頭穿插在夜間事件插畫之間，避免把事後調查畫成當夜目擊；畫面不是照片或人物肖像。付費 MiniMax 圖**尚未生成**。
- 專案 `estimateTimeline` 依 250／300／325 CPM 加場景停頓，首 8 景開場為 **44.6／38.4／36.2 秒**；之後 129 景故事正文為 **635.1／549.2／519.1 秒**，三種估速均超過八分鐘。最後三句普通片尾口播估 **15.9／13.6／12.8 秒**；實際頻道 TTS 正文時長仍需單獨測量，估時不是音訊驗收。
- 原創 5 秒片頭應在首章後，以 branding pin `intro_at: "after_first_chapter"` 指定。共用 21 秒 `v4-endscreen` 應接在正片口播後，最後 16 秒預留 Studio 的兩個可點影片元素和訂閱元素，私人上傳後才匯入既有範本、設時間並逐一點測。這些素材未加入此 JSON，無成片、音訊、插畫、配樂、上傳或發布。

## 下一關

獨立來源審核和兩位不同盲讀者在**同一套 hash**上讀稿，必要修正後重新固定版本；再走網站大綱／劇本審查。獲得整集媒體預算授權後才跑 TTS、圖像與配樂；實測正文至少八分鐘，完成音檢、畫面、成片及 Studio 結束畫面。
