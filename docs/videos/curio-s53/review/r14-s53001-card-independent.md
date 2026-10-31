# S53 R14｜首景來源卡獨立覆核

2026-10-22 UTC。**PASS：只放行 R14 資訊卡與本章一次八景首輪試畫；不核准整集分鏡、音訊或網站卡。** 我不是 R14 作者，未改 `video.json`、`claims.md` 或 `script.md`。

我重開固定 1913 年 *San Francisco Relief Survey* 原檔 `/tmp/s53-sf-relief/56217-0.txt`，SHA-256 為 `d627ed287d8a93b9c00225ea47dbdc4f97c36089a890192a602b993c3c185b72`，符合 [research.md](../research.md)。L4972–4994 明述 1907 年六月公園委員會要求救濟機構在八月十七日前把廣場上的小屋清走，並描述清場延誤；因此卡片「1907 年 6 月｜舊金山／廣場裡的小屋／1913 年救濟調查回顧」與現行 s53001 旁白有據。下標清楚標示後出調查，沒有冒稱 1907 年現場照片或原始通知。

我用 [R14 精確差分](r14-s53001-card-structured-diff.json)反向替換，整份 `video.json` 可逐位元組回到 R13 SHA `8b9c141a39abb6f1d0ef6d815ce80154f5d136168dc90d64659e290f513432d2`；現行 R14 SHA `0cbe40d9189710525bf82627bf21e411c2ea600870ceabc1975873e7b0fe1c19`。唯一場次變化是 s53001 的 `shot`→`big` 與該卡資料；同一句口播及餘下場次不變。`script.md` SHA `64ffcd8c0e89c4596a7fd08d41bd74f8a16f55fbc9acc2f41d7f9b914ea300fc`、`claims.md` SHA `b5be9bbbf8c78cc87c32efcc0964afea1cb689a225b1a216184db750623b5f84`，與 R13 相同。

`lint --json` 為 0 error／0 warning、126 句；正文 115 插圖／8 資訊卡，插圖占 93.5%，連續卡片最多 1。第一章其餘插圖是 s53002–s53009 共八景。`keyframes --shot <八 ID> --takes 1 --dry-run` 報 MiniMax `image-01` 就緒，八景首輪約 US$0.11；私有帳本在付費前 US$0.0405／3 images／3 judges、0 reservations，`STOP` 在位，低於整集 US$4.78 上限。R11–R13 的 s53001 三張拒收圖不被重用。只可用 EXIT trap 限額執行這八景一次，逐張檢查原圖和來源；兩張來源層級矛盾或三張同類年代／年齡錯誤則停止擴批。
