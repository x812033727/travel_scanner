# S53 R48｜s53036 原生圖與畫面註記獨立覆核

2026-10-22 UTC。審者 `/root/s63_r7_source_review` 未撰寫此景修訂、未操作付費出圖。**KEEP 原圖及入選裁切；PASS 畫面註記窄修。**此票不代表其他分鏡或整集成片完成。

我直接看未裁 1280×720 `keyframes/s53036-1.jpg`，SHA-256 `053e9369bc5b6d1d68d255532449c18b6dd7933b9efb10006b3e76d8eb448bb0`，及入選 `keyframes/s53036-1-trim.jpg`，SHA-256 `7d63ea5b79edb93b8c7023a77b345c0995a4aa1921d9156ce0443070cbc20a69`。兩者均見銀灰髮、成人面容與身形的人站在低矮木板小屋旁，一隻空手貼近外牆；門關閉，遠處有另一棟完整小屋。沒有火災廢墟、申請單、鑰匙、交屋隊伍或搬屋動作；沒有可讀文字、黑邊或攝影／3D 漂移。裁切保留核心主體，圖仍為二維卡通。機器 judge 9.29 PASS 與這項視覺 KEEP 一致。

重開固定 1913 年 Survey `/tmp/s53-sf-relief/56217-0.txt`，SHA-256 `d627ed287d8a93b9c00225ea47dbdc4f97c36089a890192a602b993c3c185b72`，E L4887–4897 明說 `Some who had not been burned out, but needed to be better housed, received cottages`，其後才說移到自有或租地。旁白「也有沒被燒毀住處、卻需要改善住房的人領到小屋。」保留其中有人、不指認具體個案；本景不先演出下一句的移屋。小屋與人物相對位置是原創概念，不是調查指認的歷史現場，未將服飾或房形細節當史料主張。

成圖沒有原提示要求的床鋪或擁擠室內，但這是非必要的概念細節缺席，不與旁白「原住處未燒毀」矛盾，無須因此重畫。作者只將 claims 的「舊住處牆面與簡單床鋪」改成「完整小舊屋，成圖未呈現床鋪或擁擠內部」，讓文字精確描述入選圖；我直接比較 Git HEAD 與現檔，確認只有 `r48-s53036-selected-annotation-diff.json` 所列字串替換，其餘 claims 內容不動，來源連結與旁白未改。

本票綁 `video.json` SHA-256 `bb1f7bcd556f8c687cc4683eeeb665e0edd762a5e7f39c0ab42e9cfa433bae1c`、`claims.md` SHA-256 `f1200ddef4243b0db7ec0b34394eacabb0656a372b98f670acacafe130af9835`。Episode lint exit 0。KEEP 後仍須由協調者核對入選 manifest 與上述實檔 SHA、ledger、STOP／jobs，才列入整集已收清冊。
