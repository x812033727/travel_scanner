# S44 A 案劇本前製查核（2026-10-20）

## 精確版本與來源

網站於 10:36:26 UTC 對 `brief.md` SHA-256 `44f332d8c1a4d50550c4ba17927964523ed0a7a2fc0a2ebf5227fba898ff63de` 選定 A 案；站台回條詳見 [verify-site-gates.md](verify-site-gates.md)。本稿另由未驗證的暫稿改寫，未把那份暫稿當核准劇本。

| 對象 | SHA-256／結果 |
| --- | --- |
| [video.json](video.json) | `6572e05b1deb0ba86bbb7b3aea507e04ca8bc51af9af41e7432d9defd866c16c` |
| [script.md](script.md) | `0b5053192d0ca3747811bb789dbde224bc83ba8307708b61f89843d075a37651` |
| [claims.md](claims.md) | `6bdfeec7c41424bfa9a2029d7f211b49afe471bc5f61956abd56f6549f46ad72` |
| [research.md](research.md) | `19501e94ad524c39eb5bc7c2597f41477fcb3259afaddf1f5eb46a65839745bc` |
| [shorts.json](shorts.json) | `5b19e2a349ed55db7695fe0011977b29ca4caf271a5551a33eb7e1cf2c01ec99` |
| 故事盲讀固定題本（本地收據） | `/tmp/s44-frozen-panel-v5.txt` SHA `d0bc20bf47eb8600a996a0bd86503b4f3462647e23740554cbe47906f3c35bda` |
| John Snow 1855 固定版原文 | GITenberg commit `6a27453cc0bb85c3fc125c5e13900c8f3a8b48db`；477,330 bytes；SHA-256 `3f3e71972f603e5fa50a0e71045afffa994ae38a86a8912dda3e90c8babb37af` |

## 已驗證的劇本與分鏡文字

- 93 句正文、3 句片尾；正文 83 景插圖、10 景資料卡，插圖占比 **89.2%**，連續資料卡最多 1 景。七章，18 組具體伏筆與回收；估算全稿 9.5 分鐘、濃縮開場約 39 秒、其後故事正文約 8 分 34 秒。這是文字估算，實際時長須在語音合成後量測。
- `lint` **0 error、1 warning**。唯一警告是片尾口播沒有說「訂閱」；為避開前集政策評審把頻道訂閱口播誤認成業配，口播採中性導引；動畫片尾的訂閱圓框仍在規劃。`script --slug` 已從同一 `video.json` 產生劇本。劇本現已送網站人工 script gate，仍 pending；詳見 [verify-site-gates.md](verify-site-gates.md)。
- 獨立史料／視覺查核者重新核對固定 Snow 原文、93/93 句正文、3/3 句片尾、83/83 張插圖提示詞、10/10 張資料卡及 13 組來源錨。最初唯一具體問題是 `snow032` 卡片把 61 例的消息來源全寫成「家屬」；原文僅說 *I was informed*，卡片已改為「獲飲水證詞」。查核者對修正後**前一版** `video.json` SHA `59a25347e2993198031354522fb000c4c42a6bfb24ef23e2ab47725049271945` 確認史料與分鏡文字 PASS。唯讀收據在本次工作環境 `/tmp/s44-source-visual-audit-v2.md`，SHA-256 `5752c73851ab4ed96d94439f8ff5192bc67962fde12e0ea1ef2fdd836765eb26`；查核者曾見舊版敘事稿，**不計入故事盲讀**。
- 第一位真正盲讀者對舊版 13 題給 **12/13**，指出 `snow060` 問到能否證明每名工人喝哪種水，後文卻未回答。舊版讀稿 `/tmp/s44-blind-reader-a.json` SHA-256 `67f129140a46c8ffdde307e0e5827aec9fb94e92ddc53e414c2708570d1a8514`，**不是通過憑證**。後改 `snow060`，使 `snow061–062` 的馬歇爾逐人訪查直接回應。這一行對舊版的獨立史料／畫面差分已通過：`/tmp/s44-v3-root-independent-source-delta.md` SHA `23cb51a6d172c964a99892bb3ef5fe88fa6a4dba64d9bfb8abe92f3f43bcfcb4`。
- 第二位全新盲讀者對中間版劇本 SHA `50f89447bd643e2fd61b7b5e55804b5962285c1252e25326b2986ca5987cab31` 回報 **12/13**，指出 `snow033–037` 的否認喝水、`snow056–057` 的酒廠取水與 `snow090` 證據總結重複，收據 `/tmp/s44-blind-v3-b.json` SHA `cd9df0063136c6e46b92522e48ef68c4e88cb1dd9ce627ef3af4c0b4f185a66f`，**不是通過憑證**。後改 `snow033` 的「家人」為原文支持的「據報」；`snow034–037` 轉向食店、咖啡館九名已亡顧客與未知供水方式；`snow056–057` 分清酒廠兩種供水和廠主的猜測／確定；`snow090` 加入 9 月 2 日另位居民遇到**透明而有臭味**的水。這些變更對上一版的獨立史料／視覺差分已通過：`/tmp/s44-v4-root-independent-source-visual-delta.md` SHA `33cb9f7693d9fa35569a8f6bacb677f42a134de3eeb9cf6dbc35c750c248ed5b`。
- 再兩位全新讀者對上一版劇本 SHA `d44b1e0321b9e88a42a4e28343786994bc6e5435c3d03a1195d63dee75651aca` 分別報 **12/13**（`no_recap`）和 **11/13**（`no_recap`、`payoffs`）：`/tmp/s44-fresh-blind-v4-a-receipt.md`、`/tmp/s44-v4-b-receipt.json`，**都不是通過憑證**。現版移除 `snow048` 重述把手的半句，`snow087` 改為拆除後 9/9 與 9/10 的新發病數，`snow089` 改問透明水有無其他異樣讓 `snow090` 的氣味直接回答，`snow091` 改為其他受訪者未察覺變化，`snow092` 單獨收束把手效果無法由數字判定。獨立查核者已按 Snow 原文核對以上精確差分及新提示詞，PASS：`/tmp/s44-v5-root-independent-source-visual-delta.md` SHA `327cc5ee52320a310bc917fdbb747802e309f2529f3050f9c1d5feb4be447db2`。
- 兩位**全新、彼此獨立**讀者只拿本版固定口播與官方 13 題，對現行劇本 SHA `0b5053192d0ca3747811bb789dbde224bc83ba8307708b61f89843d075a37651` 各交 **13/13 yes**、各自官方本地 verdict PASS。A 原始答案 `/tmp/s44-fresh-blind-v5-a-answers.json` SHA `d105c9b063fe4c6aa5a8f310e9f1941b2f1f38dd12cbb420f7334f79c8a07fb8`，B 官方格式答案 `/tmp/s44-fresh-blind-v5-b-answers.json` SHA `4fd7a9ae9183eef50978df092826cc4e8dee7286ea85809b575707618d64c3f2`；合併收據 `/tmp/s44-v5-blind-merge-receipt.json` SHA `a97d11807acaf861ed1f595263618f69e2565d75b73eac85bd1b2934f06112f2`。本機 `review/narrative.json` SHA `e76849d1b0da85cc0f1a8cb100cfa629185ace2828d62354bd1844c4acb02988` 記錄 `readers:2` 與 `passed:true`。同版已提交網站 script gate，網站仍待站主處置。
- 原文只支持 9 月 7 日史諾向堂區理事會說明、8 日把手拆除；1855 年出版地圖涵蓋到 9 月 30 日，不得進 1854 年會議畫面。資料表是**最終病亡者的發病日估算**，部分倒推、45 例未知；拆把手前已下降，不能把行動說成當夜使疫情結束，也不能說完全沒有保護效果。未畫出可見病菌或來源不明的地下污染路徑。這些是後續原尺寸插圖驗收的重點。

## 片頭、片尾、連結與 Short

此集的 39 秒濃縮開場計畫接共用 5 秒品牌動畫片頭；正片口播後接 21 秒品牌片尾，末 16 秒為兩支影片和訂閱的 Studio 元素區。這些尚是**組片計畫，沒有成片或可點連結**。`video.json` 說明欄已列固定版 Snow 原文、1855 年地圖和頻道網址。`shorts.json` 是一支 8 景、六拍的 25–55 秒 `from-episode` 草案；episode schema 與取鏡檢查通過、8/8 句口播與長片逐字相同；沒有關鍵影格與長片語音，因此尚不能組直式成片。

媒體報價為本地 dry-run：Gemini 96 句／約 2,200 計費字元；MiniMax 83 張靜圖、0 張 end frame，一次通過約 US$1.12，最多三次約 US$3.36，另有配樂約 US$0.08。**目前媒體費用 US$0，尚未要求產生。**

## 未完成關卡

網站 script gate 已收到這一版劇本，回覆 **pending／waiting for the owner**；在網站核准前，語音、插圖、配樂、成片、Short 及 YouTube 私人上傳均未完成。文件測試 `npm run test:docs-videos` **236/236** 通過，`npm run check:tasks` 驗證 **2113** 張任務票通過（既有跨票警告）。
