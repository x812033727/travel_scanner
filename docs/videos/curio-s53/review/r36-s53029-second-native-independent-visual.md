# S53 R36｜`s53029` 第二張原生圖獨立原尺寸視覺判定

2026-10-22 UTC。**我的視覺判定為 HUMAN KEEP（有條件，信心約 0.75）；這不是機器 PASS 或正式選入。**我在閱讀其他 R36 視覺判定之前，直接看了 1280×720 未裁原圖及 1280×720 所選裁圖，依固定來源、口播與 Curio 的「只退實質誤導或畫風漂移」界線判斷。另一位獨立讀者對成年辨識及閒置姿勢判 HUMAN REJECT，意見仍分歧；作者已封存本張並把有效圖單恢復為 18 KEEP。本收據只記我的人眼判斷，沒有改稿、私有媒體、圖單或 Git，也沒有付費呼叫。

| 固定核對對象 | SHA-256／狀態 |
| --- | --- |
| 第二張未裁原圖 `keyframes/s53029-1.jpg`，私人 held 備份同位元組 | `e1d4dd5aec3b4a563252b9c458aa1f9e42e9992138f0e67423e1534e9829837b` |
| 第二張所選裁圖 `keyframes/s53029-1-trim.jpg`，私人 held 備份同位元組 | `731330acda8649dcc99aedc8e0e1c4e724ca8f5f81674c3ea1089afc7fd06a45` |
| R36 `docs/videos/curio-s53/video.json` | `601b54f492cb38ddf046f200f6bb02097868e25b9217605d2661abc33c1aa49e` |
| R36 `docs/videos/curio-s53/claims.md` | `0795312a9584486511f8695faeee7dda73863fd5ca64f705da99da5ccba6a745` |
| 未改 `docs/videos/curio-s53/script.md` | `64ffcd8c0e89c4596a7fd08d41bd74f8a16f55fbc9acc2f41d7f9b914ea300fc` |
| 固定 Survey 原文 `/tmp/s53-sf-relief/56217-0.txt` | `d627ed287d8a93b9c00225ea47dbdc4f97c36089a890192a602b993c3c185b72` |

## 原尺寸所見與來源界線

未裁圖及裁圖均顯示一間外牆、木門和門框已完成的小屋，門內黑暗，無家具、燈、住戶或第二個人物；圖為 2D 平塗、清楚描邊，未漂成照片或 3D。門邊人物全身入鏡，頭大身短、臉頰平滑，乍看有童貌風險；但短灰白髮、下垂眼神、深色工作上衣和腰間可見的工具帶／紅色工具，合起來在本系列 Q 版人物比例下**較像年長工人**。我對年齡的把握只是中等，沒有把灰髮一項當成決定性證據。相比 R35 首張原圖 `6652f9899e861d54fdba6407f658e019280faaadeed7dc2690b993e8dc82e112` 的黑髮童貌、暖光室內及無工具人物，第二張的角色和空屋訊號已有實質變化。

固定 [Survey D L4858–4865](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L4858-L4865)記 1906 年 9 月 10 日開工、9 月 16 日漢密爾頓廣場完成 20 棟，之後仍隔至少兩三個月才有相當數量可供難民使用。口播是「六天後，漢密爾頓廣場先完成二十棟。」這張圖用**一間完成的小屋**概念化首批完工，工具帶人物在門邊，黑暗未布置的可見室內沒有家庭使用線索；我不認為它實質宣稱 9 月 16 日已有住戶入住。Survey 也未說當日二十棟絕無任何人進入，故人物位於門檻本身不能推出與史料相反的入住主張。這是概念插圖，不是當日照片或對 20 棟房型的逐棟重建。

## 真實缺口、機器判定及使用限制

R36 prompt 要成年建造者**站在屋外**，一手「試」門框、另一手扶門邊，且只取上半身與門柱的近景；現有原圖人物站在／略位於**門檻內**，一手碰近門柱，另一手靠在胸前，動作讀成停在門口，**看不出明確的兩手驗框**。門與整個人都入鏡，也不是上半身近景。這些字面失配是真實的，不應把我的視覺 KEEP 改寫成「prompt 完全達成」。私人封存的 19 景 `rebind-backups/r36-s53029-second-native-held-manifest.json` SHA-256 `a7259016c40ff87a24f55f693710f4ed005706a6e4c1f6329fe07880b674ddf4`，其中本景 `needs_review=true`、機器 **9.0／10，`passed=false`、`subject=0`、`details=7`、`style=10`**；它指出閒置姿勢及全身取景，我同意這兩項觀察。我的 KEEP 僅表示在「是否實質誤導完工與入住」的人眼界線下，該姿勢仍可作與來源相容的完成小屋插圖。

若未來重新考慮此圖，現行 `claims.md` 的「站在小屋外、以手檢查木門框」須先改為實際可見的「灰髮、佩工具帶的人物立在完成小屋門檻，手碰門柱；室內暗且未見住戶」之類描述；不能把缺少的驗框動作當成圖像證據。人物年齡仍有合理異議，應把本 HUMAN KEEP 視為**有條件且非一致的人眼意見**，不是替另一位 REJECT 裁決，更不是跳過機器 gate 的依據。

只讀覆核後，有效 `keyframes/manifest.json` SHA-256 `deae00309dd2e438ad4f20252f6a8e3178432f15a6fb967350aeba0db27142a7`，`visual_hash=7a88c3a7a90cc951`，仍只有 **18 筆 KEEP**，其所選實檔 SHA 全對、無 `s53029`；與第二張前備份逐位元組相同。原圖、裁圖及機器 FAIL 的 19 景圖單均有私人 held 備份，未列入有效 manifest。`media/ledger.json` SHA-256 `acbe13e67db05424cbad7e252578fc8a5dd7bac5f04b38a2783ef1d3f6bc235b`，逐筆合計 **US$0.6615／50 image／49 judge／0 預約**；`media/jobs.json` SHA-256 `a9d2c69ab3cb5704417b4f0968a7d8d0dae6eb0e35d37e053463220b30d55ca3` 且 jobs 空，`STOP` 在位。現行 `format=drama` 的 `tools/video/media/keyframes.mjs` 限 `--accept-best` 於 illustrated 路線，無法藉此把本機器 FAIL 圖選入。**因此有效選圖仍是 HOLD；我的 HUMAN KEEP 只在視覺審查層成立。**
