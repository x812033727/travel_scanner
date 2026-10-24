# S53 R14｜首景來源日期卡作者候選

2026-10-22 UTC。**待獨立覆核，沒有新付費呼叫。** `s53001` 的 R11、R12、R13 三張原圖都經直接查看而退件：大型現代街屋、汽車與寫實街景、或不符低矮救災小屋及廣場的多餘人物。兩輪 prompt 修補仍未得到可用圖；依 `curio-episode` 的三次出圖退路，改以來源界線清楚的資訊卡。

R14 只把 `s53001` 由 `shot` 換成 `big`，文字為「1907 年 6 月｜舊金山／廣場裡的小屋／1913 年救濟調查回顧」。1913 年 *San Francisco Relief Survey* 的 [H L4972–4994](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L4972-L4994) 回顧 1907 年 6 月公園委員會清場要求及尚在廣場的救濟小屋；卡片不偽裝成 1907 年現場照片或官方原始通知。旁白「一九〇七年六月，舊金山的廣場裡，木造救災小屋還在。」未變，`claims.md` 與 `script.md` 未變。

[可逆差分](r14-s53001-card-structured-diff.json)只在 `video.json` 改 `s53001` 的模板與資料欄，可逐位元組還原 R13 SHA `8b9c141a39abb6f1d0ef6d815ce80154f5d136168dc90d64659e290f513432d2`。R14 新 SHA `0cbe40d9189710525bf82627bf21e411c2ea600870ceabc1975873e7b0fe1c19`。`lint --json` 0 errors／0 warnings，126 句；正文 115 插圖／8 卡，插圖占 93.5%、最大連續卡片 1。濃縮開場與品牌片頭位置不變。私有 STOP 在位，R13 後帳本 US$0.0405／3 圖／3 judge，低於 US$4.78 上限；無額外媒體。獨立覆核通過後才可進下一景的來源／畫面及付費預檢，不能把卡片決定當作整集分鏡、音訊、網站或成片核准。
