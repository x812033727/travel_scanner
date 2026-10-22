# S53 R19｜第二章八景獨立史料與提示詞紙審

2026-10-22 UTC。**PASS：只准這八景各一次原生 MiniMax 試畫與原圖逐張驗收；尚無原生 KEEP 或整章畫面 PASS。**我未參與 R19 作者七景修稿，也未改任何 `video.json`、`claims.md`、`script.md` 或既有媒體。核對的輸入為 `video.json` SHA-256 `62254351988dae8424e0d94bb136a6b7171e5d991f2c9962508af03fc7248c3a`、`claims.md` `b5be9bbbf8c78cc87c32efcc0964afea1cb689a225b1a216184db750623b5f84`、`script.md` `64ffcd8c0e89c4596a7fd08d41bd74f8a16f55fbc9acc2f41d7f9b914ea300fc`、`brief.md` `8e44f47693dd75ad0a7509ab0f495c06adcc2e614b8c8bc09a51559d7202a27c`、`research.md` `2e61530c650852281402476041175154ee69c414daf7431d6aa0db352e7c3d22`。

## 固定來源及八景判定

我直接重讀 1913 年 [*San Francisco Relief Survey* 固定全文](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt)，本機 SHA-256 `d627ed287d8a93b9c00225ea47dbdc4f97c36089a890192a602b993c3c185b72`。八句旁白在 `video.json`、`claims.md`、`script.md` 的 ID 和文字 **8／8 逐字一致**；R19 只換七個提示詞，未動旁白。這些人物均為匿名原創示意，沒有把對話、公告、地契或建築圖當成可查原件。

| 景 | 固定史料與 R19 紙審 | 原圖仍須檢查 |
| --- | --- | --- |
| `s53010` | **PASS，R18 原提示詞未動。**[L1438–1465](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L1438-L1465)記 1906-04-18 清晨地震與後續大火；成年住戶望向遠方煙柱是有來源的概念畫。 | 1906 衣著、成人面容、遠煙而非現代城市或已重建街道。 |
| `s53011` | **PASS。**[L4250–4264](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L4250-L4264)明載第一晚在公園／廣場休息、攜寢具、毛毯搭在木杆上作簡易遮蔽，帳棚後來才漸增。新版有皺紋成人帶寢具走向毛毯棚，沒有把後期成排帳棚放進第一晚。 | 第一晚只有臨時遮蔽與裸地；不能生出整齊小屋、現代露營區、兒童主角或把後期營地前移。 |
| `s53014` | **PASS。**同 [L4848–4870](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L4848-L4870)支持帳棚作過渡居所；新版是戶外成人整理帆布門襟，已移除戶外場景的 `window light` 自相矛盾。 | 帳棚與陰天自然光；無屋內窗戶、完工小屋或童貌。 |
| `s53015` | **PASS。**同一段說雨季將至，先問帳棚能否長住；新版成人在簡單帳棚口望聚雲，不把尚未到的暴雨說成已發生。 | 1906 夏末簡陋營地，成人主角；沒有強暴雨、現代營帳或已建小屋。 |
| `s53017` | **PASS。**同一段說救濟機構先**決定**分開小屋，9 月 10 日才開工；兩名成年工作者在未建地面比劃間距是概念示意，已去掉施工木板與假計畫紙。 | 僅帳棚與空地；若出現施工中或完工小屋、可讀假圖面即退。多人互動可能畫錯，須看原圖。 |
| `s53018` | **PASS。**同一段明指 South Park 面積不足容納分開小屋；一名成年工作者用手勢量狹小帳棚間空地，直接對上限制，沒有假地圖或產權線。 | 狹窄裸地與帳棚需同時可辨，不能畫寬廣空公園或已完工小屋。 |
| `s53020` | **PASS。**同一段記 1906-08-01 對外**公開計畫**、9 月 10 日才開工；成人職員對一群成人住戶說明是匿名概念示意，不宣稱能查到該次公開方式。 | 必須是成年人物、尚在帳棚時期；不得變成有文字的假公告、正式可識別會議或已施工場景。 |
| `s53021` | **PASS。**[L4934–4941](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L4934-L4941)記營地多在公地，救濟機構須向公園委員會詢問用地；成人沿公共廣場的帳棚望向公地是相關示意，產權差異仍靠旁白說明。 | 不得出現可讀地契、假界線、救濟機構自有土地標牌或現代街景。 |

## 可逆性、快取與下一步

我逐欄核對[作者七景差分](r19-next-chapter-seven-prompt-structured-diff.json)：`scenes[10–16].data.prompt` 恰為 `s53011/14/15/17/18/20/21` 的七處變更；`s53010` 和另外 117 景的其他欄位不變。把七個 `new` 逐一回填 `old` 後重新序列化，SHA-256 **精確還原 R18** `81c8a7ef0efda1d86c02ab6ebc20199f6b9d70149c2a8cfaab731594e7d06519`；現行 R19 重新算為 `62254351988dae8424e0d94bb136a6b7171e5d991f2c9962508af03fc7248c3a`。`lint` 仍 0 error／0 warning。

私有首章 `s53002–09` 的八個 manifest 選圖條目仍在，所指八份圖檔的 SHA 均與 manifest 相符；`s53007` 沿用 `s53003` 的已接納圖。Manifest SHA-256 `2aa4d25a3950d5c076c2565702aff9e8431eed6e7c0ca62a4454a937558fd1f5`，帳本 SHA-256 `442d21b4ff1258f7819c7540a462b5ddd296f18e84faaa16e9436ed43eac36ed`，**US$0.3105／23 images／23 judges／0 reservations**，`STOP` 在位。媒體工具在 `visual_hash` 更新時會保留自身 request key 與 judge 問題未變的舊景；原圖前後仍須核對這八個 key 與選圖 SHA，不能只信 manifest 總張數。

對這八景實跑 `keyframes --slug curio-s53 --shot s53010,s53011,s53014,s53015,s53017,s53018,s53020,s53021 --takes 1 --dry-run`：MiniMax `image-01` 1K ready，**最多八次生成加八次 judge，約 US$0.108**，加到目前約 US$0.4185，低於既定整集 **US$4.78** 上限。正式試畫必須在現有 `STOP` 的 EXIT trap、單一付費端點和逐景原生圖檢查下進行；**出現三個相關原圖缺陷就停止**。這份紙審不預判機器 judge PASS 的 JPEG 必然可用。
