# S53 R35｜`s53029` 首張原生圖非作者原尺寸驗收

2026-10-22 UTC。**HUMAN REJECT。**我不是本景提示詞或首張出圖作者；獨立打開 1280×720 未裁原圖與所選裁圖，核對現行 `video.json`、`claims.md`、固定 1913 年 *San Francisco Relief Survey* D 原文和本集畫風。本回只寫此收據，沒有更動稿件、私有圖單／帳本、任務或購買媒體。

| 核對對象 | SHA-256／狀態 |
| --- | --- |
| 首張未裁 `keyframes/s53029-1.jpg`，1280×720；退件備份同位元組 | `6652f9899e861d54fdba6407f658e019280faaadeed7dc2690b993e8dc82e112` |
| 首張所選 `keyframes/s53029-1-trim.jpg`，1280×720；退件備份同位元組 | `29baab08c56f34e112f04ac3470fe7d968fc2efc6b78b6a5beb2797371101886` |
| 當前 `docs/videos/curio-s53/video.json` | `dc3bfba35e527d0206a56e78c5784fd8eab7d5fe38c97c59d233280e7861df79` |
| 當前 `docs/videos/curio-s53/claims.md` | `85eb3ce65fbef3746cd30a311d9af067968b32e5f5152a9c8c24e53d0a1200f9` |
| 固定 `56217-0.txt` | `d627ed287d8a93b9c00225ea47dbdc4f97c36089a890192a602b993c3c185b72` |
| 退件時 19 筆 `manifest.json` 私人備份 | `056f04081de9228931bbbdd42ae4bed236f7ac053951e297a405e888714f5437` |
| 恢復後有效 18 KEEP `keyframes/manifest.json` | `051f6055af0209948d665b095b1201ef37967c5c34c74cb2c3213292909dec59` |
| 恢復後有效 `keyframes/contact-sheet.png` | `0c1694a9150059b8656f778562ecaf925b3a4827d88b919d40464912abb0f930` |
| 有效 `media/ledger.json` | `fb92ccb3157efcb91b384f86a3f03d0d184a0e6b8a6b956cbbaced369b694878` |

`s53029` 口播「六天後，漢密爾頓廣場先完成二十棟。」；現行 prompt 指定一名匿名建屋工人在完成的小屋**門口檢查門框**，近景、昏暗燈光。固定 [Survey D L4858–4864](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L4858-L4864) 記 **1906 年 9 月 10 日開工**、**9 月 16 日 Hamilton Square 完成 20 間**，並緊接說仍過了至少兩、三個月，才有相當數量的房屋可供難民使用。原文沒有指認此日某位建屋工人、門框檢查或任何一名兒童入住。

原圖和裁圖都顯示一間已有門窗的完成小屋；門內暖光照著**一名童貌人物**，孩子由室內探頭、扶著打開的門向外看。畫面沒有成年建屋工人，沒有檢查門框的動作。屋立面及大片院子佔據畫框，門口人物很小；比要求的門框近景明顯更遠。入選裁圖略收邊，沒有改變主體或動作。完成的小屋、夜間燈光與平面可愛 2D 畫風本身沒有違反來源或本集風格；一屋代指二十屋也只是畫面取樣，不是此回退件原因。

退件時 judge 給 **9.0／10、`passed=false`、`subject=0`、`details=7`、`style=10`**，指出孩子由屋內張望，並非工人檢查門口，畫框也不是 close shot。這兩項與原尺寸所見一致；把取景稱作 wide 或 medium 有主觀餘地，但「不是近景」沒有實質爭議。圖像把「首批小屋完工」的事件改成近似孩子已在屋內使用，觀眾可能讀成此日已有住戶；Survey D **沒有確立**該孩子或當日入住，且明說相當數量房屋可供居住仍需兩、三個月。這不是斷言 9 月 16 日絕無一人入屋，而是指出這張圖使未經來源支持的使用情景蓋過建屋完成的主題。依 Curio 的來源／旁白與主體驗收界線，我判 **HUMAN REJECT**，不能以總分 9.0 選入。

首張 image-01 圖像與一次 Gemini judge 的退件原圖、裁圖、19 筆圖單及 contact sheet 已封存於私人備份；退件圖單 `s53029` request key `d67d4da448448547`、`needs_review=true`，與上述 FAIL 一致。有效 18 KEEP manifest 及 contact sheet 與首張前備份**逐位元組相同**，`visual_hash=76b75a45d888af0b`，沒有 `s53029`；原有 18 筆 ID、request key、所選 SHA 仍與前回 KEEP 一致，所選檔 SHA 全數核對無誤。有效 ledger 逐項合計 **US$0.6480／49 image／48 judge／0 預約**，已包含本張及其 judge；有效 `media/jobs.json` SHA `a9d2c69ab3cb5704417b4f0968a7d8d0dae6eb0e35d37e053463220b30d55ca3` 且 `jobs={}`，`STOP` 在位。本收據不放行其他景或批次付費。
