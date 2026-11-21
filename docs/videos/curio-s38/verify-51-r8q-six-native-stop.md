# S38 R8q｜PF009–014 六張原生圖逐張驗收

2026-10-22 UTC。依 [獨立書面 PASS](verify-50-r8q-six-prompt-independent.md)對 R8q 六個 ID 各畫**一次**，直接開未裁切 1280×720 原生圖與所選裁邊版。**PF010、PF011、PF012、PF014 直接原圖 KEEP；PF009、PF013 REJECT。**這是四景入選、兩景待修，不是全片分鏡通過。`video.json` 仍為 R8q SHA-256 `087ae9c4cdbb8dea3430cd505d42624e06deca0a94b77e71c49164fbbcc2f4db`；旁白與來源檔未改。

| 景 | 原圖 SHA-256；所選圖 SHA-256 | 機器／原圖判定 |
| --- | --- | --- |
| `pf009` | `e87593dc16e5ff87e91f159fe3b3c6e622fa4cb67a87b205e794bb6c30668ed0`；`a1572c5edfeafc5af49bda188ec1b79731a30e553d921f096641f6de7169f73e` | **REJECT**。成人確實回床，但未裁圖頂底有黑寬帶且呈成熟寫實動畫質感；機器亦以 style／frame 判 9.41/10 FAIL，所選裁圖仍不能修正畫風差。 |
| `pf010` | `b2fd9bdb55b158c6e942ef202dbddcea890ba5a4303670f73568e27ed0da60c0`；`5fc7fd687ced8649ecae9b392df16383047aab399a3525786a498b6efcc65850` | **KEEP**。一名成人在木框窗前再看火，灰天之下火只占窗外局部，對照上一鏡紅光符合「他覺得更小、更遠」的主觀說法；沒有現代街景。機器 10/10 PASS。 |
| `pf011` | `8202ac00ff3e64c1f4b96e9373879a399cf4ba8bf86c97008c99e7c2602a2b8f`；`c1bc71715db707d97170cf07c02ff7d9d83b4902ca3d6b8d388ab44bd3b60466` | **KEEP**。一名戴頭巾、繫圍裙的成人女僕空手在門邊急報，沒有偽造消息紙張；漫畫感嘆記號只是無文字的說話圖像。機器 9.29/10 PASS，只指出景別偏遠。 |
| `pf012` | `704dff2fd866868d391ebb52dca39b5cce66e526507e969aca429ae9da70f3e4`；`9e68b1885804b598622c86568bfe1b03481a57f3535b05a5a7a3902d54172381` | **KEEP**。一名成年人物在木門邊披外衣、準備親自出門；沒有第二名錯置人物或偽造書面消息。眼鏡與衣飾是漫畫概念細節，未用作特定 1666 史實證物。機器 9.29/10 PASS。 |
| `pf013` | `5f81bfa4247ac033f049178cb4daafcc47fc00a1d91e08e45a1d3252d7c212b2`；同原圖 | **REJECT**。雖然畫出塔上人物與遠火，後景卻明顯是 1894 年啟用的雙塔、吊索式 **Tower Bridge**，而非 1666 年的舊 London Bridge。機器 9.29/10 PASS 漏判這個重大時代矛盾；不可因人物年齡改善而收圖。 |
| `pf014` | `b9e847d021298b92143ded0819bc27475a21fe13d4eb4462a53b5ea5948a4bda`；同原圖 | **KEEP**。成年漫畫人物在塔上石欄擔憂、遠處河岸冒煙，畫面沒有具體橋體，也沒先宣布熟人房屋燒毀。機器 10/10 PASS。 |

執行前私有備份於 `review/r8q-six-pre/`；執行後未裁切原圖、裁圖、manifest、帳本與 STOP 備份於 `review/r8q-six-post/`。命令只帶 `--shot pf009,pf010,pf011,pf012,pf013,pf014 --takes 1`，以 EXIT trap 恢復 STOP，未用 force 或 offset；所需 Chromium 私有 shim 可開，但因 PF009 的機器 `needs_review`，CLI 最終以**內容關卡 exit 1** 回報，未產整批可核准聯絡表。帳本由 US$0.4615／29 images／28 judges／1 music 增為 **US$0.5425／35 images／34 judges／1 music**，恰增 US$0.0810；舊 US$0.0035 reservation 未變，遠低於 US$4.58 硬上限。`STOP` 現在存在。後圖單 SHA-256 `ffd0069be9f1b368ffcea76f4b9a94b06eb7d8e1bcbc480c13f70ec90933c8fa`，原先已收 PF001–005／PF008 的 manifest entries 與所選檔案 SHA 均未改。

下一步只處理兩個 HOLD：PF009 可按機器提出的畫風與滿框問題評估同 prompt 第二張，但本輪授權僅一張，需另做有界檢查；PF013 必須先改提示詞，**排除 1894 Tower Bridge 的雙塔吊索輪廓**，再由另一位核對來源與差分。PF015–022 尚未生成，仍不得把本輪四張 KEEP 延伸為全章或全片通過。網站站主音訊／分鏡卡、片頭片尾實際合成及 Studio 可點連結均未完成。
