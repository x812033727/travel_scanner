# S38 R8w｜PF015 舊圖回收的服務端停線

2026-10-22 UTC。接 [R8w 獨立紙審 PASS](verify-72-r8w-pf015-reuse-independent-paper.md)，在**不允許第四張圖**的邊界內嘗試一次正式 PF015-context judge。結果是 **服務不可達，圖單 HOLD**；沒有生成、沒有評審、沒有花費。

批前精確 `video.json` SHA-256 `af739ca32d19df378b942f04118377f8357b6b16d03f07a1e3203b53182c3bc9`；現行 `pf015.data` 與同章已收的 `pf010.data` 完全相同。用正式 `Stage.imageKey` 算 MiniMax `image-01`、1K、seed 1、無參照、image selection version 0、743 字 composed prompt，兩景均得 **`417bcf79c5715425`**，與 PF010 manifest 選圖 request key 相同。`cached()` 對該 key 命中 `keyframes/pf010-1.jpg`，SHA-256 `b2fd9bdb55b158c6e942ef202dbddcea890ba5a4303670f73568e27ed0da60c0`；沒有待續 job。已直接查看 1280×720 原圖和選圖 `pf010-1-trim.jpg`：無現代車、可讀字、額外肢體或黑邊；然而 PF015 自己的 scene ID 仍需獨立 judge stamp，不能挪用 PF010 的 10／10。

安全包裝 `/tmp/s38-r8w-block-image-submit.mjs` 拒絕任何 `POST /api/video/media/images`，允許只讀 status 與正式 judge；後續重跑用版本會回本地合成 HTTP 422，讓工具釋放任何因模型變動而預約的圖額度。Shell `EXIT` trap 恢復私人 `STOP`。執行 `keyframes --slug curio-s38 --shot pf015 --takes 1` 前重算上述 key、快取位元雜湊與待續 job，均通過；接著工具在取得 media-status 時退出 **4**：`cannot reach https://mokaair.com: fetch failed`。沒有進到 `Stage.image` 或 `Stage.judge`，也沒有生成新 PF015 裁圖。日誌為 `/tmp/s38-r8w-cache-judge.stdout`、`.stderr`。

批前／批後私人 manifest SHA-256 同為 `2517afd911a9a49a01a555718b09ca776cd95015c6f1a32b2090900754fded0a`，ledger SHA-256 同為 `a40873757bb51cbba4fc0240b76c6e2641b7c626e5328f18215c0b5fc73db86b`；仍 US$0.7045／47 images／46 judges／1 music，另有先前 US$0.0035 reservation。`STOP` 已復位。PF015 manifest 仍選到第三張**退件圖**，所以不准送 storyboard；待網站恢復後，以相同 cache-only image guard 重跑一次、付費僅一個新 judge（約 US$0.0035，整集 US$4.58 上限內），查看新原圖／裁圖及 judge stamp，再接受或退回。PF019 也仍未畫。
