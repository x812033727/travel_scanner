# S53 R33｜`s53028` 第二張原生圖非作者原尺寸驗收

2026-10-22 UTC。**HUMAN REJECT。**我不是 R33 提示詞或第二張出圖作者；獨立查看第二張實際 1280×720 未裁原圖及所選裁圖，並對照現行稿件、固定 1913 年 *San Francisco Relief Survey* D 原文、相鄰已入選景的 `cute-mystery` 畫風及 Curio 驗收規則。本收據只判斷此張實際圖，沒有修改稿件、圖單、帳本、任務或購買媒體。

| 核對對象 | SHA-256／狀態 |
| --- | --- |
| 第二張未裁 `keyframes/s53028-1.jpg`，1280×720；私人退件備份同位元組 | `433affe85ed0e5c9db5b61fadaeb9cf228a06a6c2ea8e8574c264eccfdee1f2e` |
| 第二張所選 `keyframes/s53028-1-trim.jpg`，1280×720；私人退件備份同位元組 | `87e41ddf06d462214a39e8cddb5073482745827d37f4a13f6ec127d2b4d36789` |
| R33 `docs/videos/curio-s53/video.json` | `b41e032ca0006897cf12328d43a0f1f13383d5645892eb34c89d7ba917ca8cfd` |
| R33 `docs/videos/curio-s53/claims.md` | `f0e4d90b916e6676b9b70dc0637412bc29e00e6335abfa298f5f10edb68edbba` |
| 固定 `56217-0.txt` | `d627ed287d8a93b9c00225ea47dbdc4f97c36089a890192a602b993c3c185b72` |
| 私人退件時 19 筆 `manifest.json` 備份 | `0e724be5182a570ae88c0ca94de2226b2970fa175d23388d406fa63ab700f631` |
| 恢復後有效 18 KEEP `keyframes/manifest.json` | `1c97c4ab17ffcae0624c0f312d731c9b7c91919c167d0c7f41aee1e6cbdc12bf` |
| 恢復後有效 `keyframes/contact-sheet.png` | `0c1694a9150059b8656f778562ecaf925b3a4827d88b919d40464912abb0f930` |
| 有效 `media/ledger.json` | `51419ed2bc7373282deb3af23f3cdb1ae12c7243d1e5b3eb996b43f4d65c1c5c` |

`s53028` 口播「九月十日，小屋工程開始。」；現行 prompt 要求在裸地帳棚前，一位灰髮、未戴帽的成年木匠以**短木摺尺**沿低鋸架上的**單片散置粗木板**量長度，且不出現完成的小屋或屋架；`claims.md` 明列畫面是非史實物件的概念示意。[Survey D L4858–4864](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L4858-L4864) 說小屋為取代帳棚而建，**1906 年 9 月 10 日開工**，**9 月 16 日 Hamilton Square 有 20 間完工**。新圖有成年、灰髮、未戴硬帽的人，裸地及帆布帳棚，沒有已完工房屋；就這些來源與年代事項而言，R32 首張的童貌近代硬帽及過早建成小屋問題沒有重現。

但原圖與裁圖都把人物畫成接近自然身形比例、面部寫實線紋與沉重表情的成年男子，與同集相鄰已入選 `s53027` 的大頭、簡化五官及小身體可愛卡通畫風顯著脫節。它仍是平面插畫，並非照片；具體問題是固定 `look.preset=cute-mystery` 所需的可愛解說插畫風格在這一景漂走。畫面橫向只有**一條帶刻度的長木條**，被人物雙手扶在鋸架上緣；下方可見的是鋸架橫梁，沒有可辨的另一片散置粗木板，因此看不出「用尺量板」。裁圖只是收緊畫框，沒有補出第二件物件或改變人物畫風。

退件時圖單的 judge 給 **9.0／10、`passed=false`、`style=0`、`details=7`**；它所記「非 chibi 畫風」及「尺與木板合成一根有刻度木條」和原尺寸人眼所見一致。依 Curio skill 的驗收規則，**畫風漂移本身就是退件理由**；本張的具體量板動作又與現行 prompt／claims 不符。故判 **HUMAN REJECT**，不可因總分 9.0 或年代場景已改善就選入。此判斷沒有聲稱 Survey D 記載某位木匠或這支尺，也沒有把畫面判為另一項歷史日期錯誤。

第二張 image-01 圖像與一次 Gemini judge 的私人退件檔案已封存：拒收原圖、裁圖的備份 SHA 與上列實檔相同；19 筆退件圖單內 `s53028` request key 為 `4592b1134f5d8aad`，`needs_review` 在位，judge 為上述 FAIL。有效 18 KEEP manifest 與第二張前備份**逐位元組相同**，`visual_hash=33aeb288b6ac5808`，沒有 `s53028`；其原有 18 筆 ID、request key、所選 SHA 與 R32 後圖單一致，所選實檔 SHA 全數核對無誤。有效 contact sheet 亦與第二張前備份逐位元組相同。ledger 逐筆加總 **US$0.6210／47 image／46 judge／0 預約**，包含 R32 巢狀目錄首張的兩筆費用及這次第二張兩筆，沒有重置付費次數。有效 `media/jobs.json` SHA `a9d2c69ab3cb5704417b4f0968a7d8d0dae6eb0e35d37e053463220b30d55ca3` 且 `jobs={}`，`STOP` 在位。依本景既定停線，本收據不放行下一景或再付款。
