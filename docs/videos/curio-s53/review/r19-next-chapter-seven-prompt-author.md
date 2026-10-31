# S53 R19｜第二章七景提示詞窄修

2026-10-22 UTC。依 [R18 第二章八景獨立紙審](r18-next-chapter-eight-prompt-independent-hold.md)的精確 HOLD 回條（SHA-256 `cb1c95b0526cd02ec65155e6a59c72fcc876f9cf6659138c1cc40bba571a32b0`），本輪**只改** `s53011/14/15/17/18/20/21` 七個 `data.prompt`。`s53010` 紙面 PASS，提示詞逐字不動；八句旁白均保持原字，`claims.md` 史實列、`script.md`、章界、運鏡、其他 117 景也不動。這是作者書面修稿，尚待非作者按新檔獨立覆核；沒有付費試畫。

| 景 | R18 可預見錯置 → R19 圖像動作 |
| --- | --- |
| `s53011` | 抽象成人與首夜整齊帳棚 → 1906 年震後首夜，皺紋清楚的成年住戶帶寢具走向**毛毯搭在杆上的簡易遮蔽**；少數成年人在廣場裸地休息，不把後期營地倒放到首夜。 |
| `s53014` | 戶外帳棚卻有窗光、未明成人 → 明寫 1906 年夏季戶外廣場、灰鬢有面紋的住戶整理帆布門襟、陰天自然光。 |
| `s53015` | 抽象 `refuge` 易變現代露營 → 1906 年晚夏，成年住戶立於簡易帳棚口看聚起的雲；畫的是雨季將近的疑問，沒有已發生的暴雨。 |
| `s53017` | 木板／圖紙／builder 會把**決策**誤作開工或原始圖面 → 兩位成年救濟工作者在尚為帳棚的營地指向**分開的空地**並思量間距；只見帳棚和未建地面。 |
| `s53018` | 空白地塊圖沒有顯出南公園限制 → 成年工作者站在 South Park 帳棚間，以手勢比對狹窄裸地；畫面不擺分開小屋或假地圖。 |
| `s53020` | 拿文件走向桌子看不出「公開」 → 八月一日成年職員**對一小群成年住戶說話**並向營地伸手；沒有可讀公告、假原始計畫或已施工小屋。 |
| `s53021` | 空白土地圖易冒充產權材料 → 成年工作者沿公共廣場的帳棚步行，望向開闊公地與街道；公有而非救濟機構自有的法律差異由原旁白說明，畫面不假造地契或權限移轉。 |

來源為固定 1913 年 *San Francisco Relief Survey* 文字檔，SHA-256 `d627ed287d8a93b9c00225ea47dbdc4f97c36089a890192a602b993c3c185b72`。[L4250–4264](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L4250-L4264)記首夜在公園／廣場暫住、帶寢具、以毛毯搭簡易遮蔽，帳棚後來漸增；[L4848–4870](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L4848-L4870)區分雨季前**決定**分開小屋、South Park 面積不足、**8 月 1 日公開計畫**與 **9 月 10 日才開工**；[L4934–4941](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L4934-L4941)說用地多為公地、救濟機構需問公園委員會。人物與動作是匿名概念示意，沒有聲稱找到某個人、公告、建築圖或產權原件。

[七景逐字可逆差分](r19-next-chapter-seven-prompt-structured-diff.json)保存每個舊／新提示詞和精確 `scenes[index].data.prompt` 路徑；逐項 `new→old` 回填可位元組還原 R18。`video.json` SHA-256：R18 `81c8a7ef0efda1d86c02ab6ebc20199f6b9d70149c2a8cfaab731594e7d06519` → R19 **`62254351988dae8424e0d94bb136a6b7171e5d991f2c9962508af03fc7248c3a`**。`claims.md` 保持 `b5be9bbbf8c78cc87c32efcc0964afea1cb689a225b1a216184db750623b5f84`；`script.md` 保持 `64ffcd8c0e89c4596a7fd08d41bd74f8a16f55fbc9acc2f41d7f9b914ea300fc`；`brief.md`、`research.md` 也與 R18 凍結雜湊相同。CLI `lint --slug curio-s53 --json` exit **0**，**0 errors／0 warnings**、126 句；stdout、stderr、exit 均存同目錄。

私有 `keyframes/manifest.json` SHA-256 仍為 `2aa4d25a3950d5c076c2565702aff9e8431eed6e7c0ca62a4454a937558fd1f5`，故首章 `s53002–09` 八張 KEEP 候選的 request key／選圖 SHA 逐一保留；`s53001` 來源卡未動。帳本 SHA-256 仍為 `442d21b4ff1258f7819c7540a462b5ddd296f18e84faaa16e9436ed43eac36ed`：**US$0.3105／23 images／23 judges／0 reservations**，低於整集 **US$4.78** 上限；`STOP` 在位。本輪沒有圖、音樂、付費呼叫、commit 或 push。整批要先等獨立紙審 PASS，才能在受控 STOP 流程下一景一次試畫，再直接檢查原生 JPEG；網站卡與人耳音審仍待完成。
