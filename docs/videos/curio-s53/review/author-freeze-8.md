# S53 R8｜兩處 `no_recap` 差分修訂，作者凍結

2026-10-20 UTC。[R7 隔離雙盲合併](r7-isolated-merge.md)對同一凍結劇本作官方 OR 判定：**12／13、HOLD**；兩位讀者各自指出 `no_recap` 失敗，A 在開場 `s53001`／`s53003` 看見小屋與期限重述，B 在 `s53105`／`s53110` 看見 680 份完整紀錄重述。R8 只改後一句所在的兩個口播 ID，同步逐句主張表，並用 CLI 重生 `script.md`。R7 盲評與來源覆核檔案均未改動；此為作者修訂，**不是** R8 獨立史料或敘事 PASS。

## 精確五檔 SHA-256

| 檔案 | R8 SHA-256 |
| --- | --- |
| [brief.md](../brief.md) | `8e44f47693dd75ad0a7509ab0f495c06adcc2e614b8c8bc09a51559d7202a27c` |
| [research.md](../research.md) | `2e61530c650852281402476041175154ee69c414daf7431d6aa0db352e7c3d22` |
| [claims.md](../claims.md) | `dcc27889e8302545758345327e86e65f64fb860f2e9fbe35586a3dd7907b847a` |
| [video.json](../video.json) | `7a0b948c52db433c0cda958bb376c56c560b746a4550b07adf174f3493f6f06a` |
| [script.md](../script.md)（CLI 重生） | `209c65b528aed2c36083588ed11c5be2869434571d405367bef2e1f1ef4a0d8d` |

## 改動與來源界線

- `s53003`：「搬離的期限就在那年夏天，一排排救災小屋卻還在廣場上。」→「屋子要搬出去，住戶先得找到能安放它的地。」固定 [1913 年調查 R L4972–4994](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L4972-L4994) 明說搬屋前須證明已買或租地，並記錄 1907 年 6 月清場要求。新句交代下一個具體障礙，不再重述 `s53001` 的廣場小屋或 `s53002` 的夏季期限。原本廣場裡一排小屋的概念插畫仍對應要搬出的房屋；沒有描繪未獲證據支持的搬運機械或某一戶紀實現場。
- `s53110`：「在那六百八十戶裡，只有七十戶買下了地。」→「在這批已訪家庭裡，只有七十戶買下了地。」固定 [1913 年調查 R L10997–11021](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L10997-L11021) 直接寫明 680 家庭中 70 戶買地；`這批` 回指 `s53105` 的較完整訪查紀錄。`s53110` 畫面卡片保留 `70 / 680`，供觀眾辨認比例與分母；口播只說 70，不把受訪樣本外推到 5,343 棟遷屋。

## 作者驗證

重新核對固定 R 與 C 全文 SHA-256，與 [research.md](../research.md) 一致。`video.json` 仍為 **125 景／127 句／16 個 loops**；逐 ID、順序及字串與 `claims.md` 的 127 行全相符，`screenplay(doc)` 與 CLI 重生 `script.md` 位元組一致。除兩個 `line.text` 外，畫面提示詞、卡片、角色、loop、其他口播與 `s53096` 的「一九〇八年六月下旬」均保持 R7。`git diff --check` 通過。

`node tools/video/cli.mjs lint --slug curio-s53 --json`：**0 errors／1 narrative warning**。警告仍是 `s53082`、`s53096`、`s53101` 各說「一九〇八年」，分別指營地關閉、部分小屋搬修結束及訪查開始，是三個不同事件，保留明確年號以免再次誤讀 1907 年。`estimateTimeline` 以 250／325 CPM 預估濃縮開場 **50.40／40.90 秒**、`s53010` 至 `outro` 前正文 **601.30／489.97 秒**（最快約 **8:09.97**）、全旁白 **668.77／544.57 秒**。以上為估算，並非 R8 的實際語音或成片驗收。

**待覆核：**另一位工作者應按以上五檔精確 hash 查兩處來源／書面畫面差分；兩位此前未讀 R8 稿者須用同一 R8 稿隔離完成官方十三題，並按 OR 規則合併。R7 的敘事 HOLD 不會因本作者驗證自動解除。此輪沒有付費旁白、插圖、配樂或發布，也沒有代替站主的劇本或媒體核准。
