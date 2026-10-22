# S53 R22｜地震日來源卡與南公園窄景獨立紙審

2026-10-22 UTC。**紙審 PASS 2／2，限下述定點後續；沒有新原生圖、付費呼叫或分鏡驗收。** 本回直接重開固定 1913 年 *San Francisco Relief Survey* 文字與 R21 原圖，逐項核對作者的 [可逆差分](r22-two-scene-structured-diff.json)，未修改作者稿或私有媒體。

| 景 | 獨立來源及畫面結論 |
| --- | --- |
| `s53010` | 固定來源 [L1438–1465](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L1438-L1465)直記 **1906 年 4 月 18 日 05:12** 舊金山地震及緊隨的大火；1913 年版權頁在原文 L230。`big` 卡的日期／地點、事件標題與「1913 年《舊金山救濟調查》回顧」下標均有依據，沒有假冒當日文件或現場圖。R21 第三／最後一張原圖 SHA `d4becbf39847d5fa962a06a9092374cddd4cc5d08fdf1d24287c56a347528c48` 仍見上下黑邊、人物偏右且比例不合系列；裁圖僅解黑邊，正式 judge 9／10 FAIL。**卡片 PASS；不買第四張 `s53010` 圖，也不把 R21 失敗圖標成 KEEP。** |
| `s53018` | 固定來源 [L4848–4870](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L4848-L4870)明說 South Park 面積不足以容納分開的小屋，沒有給實際帳棚間距。`claims.md` 明標帳棚擁擠畫面為原創概念示意，非現場照片、間距或平面圖。R21 第二張原圖 SHA `03ff3d435f6ed8b1b8e739e9be96470aec9266b65cde964e938e6ce61e8c210f` 的帆布近照片質感，人物正面全身、通道寬；正式 judge 9／10 FAIL。R22 的 432 字元提示詞只留一名灰髮成年工作者側身擠過兩道簡單帳棚牆，胸肩近景、側臉、牆面填框及小塊裸地，直接針對這些失配；`look` 仍僅為 `cute-mystery`。**提示詞 PASS，僅准一張第三／最後原生嘗試。** |

## 精確稿件及停線

固定來源本機原檔 SHA-256 `d627ed287d8a93b9c00225ea47dbdc4f97c36089a890192a602b993c3c185b72`。本回 `video.json` SHA `49bdd04e5ebb88ff98cd207c6da0545faf1d1721834a0dc099d514a2daf9fa99`、`claims.md` SHA `34f765eee27fb0ff083413e3e209b42d5dd09b5a2a7a89f16d14556ce1cac44b`、不變的 `script.md` SHA `64ffcd8c0e89c4596a7fd08d41bd74f8a16f55fbc9acc2f41d7f9b914ea300fc`；作者差分 SHA `0e6f323ca4529c62100729af33206042e77dc64bd124aee63c67d827388607f2`。獨立以四處新字串各唯一反向替換，逐位元組還原 R21 `video.json` SHA `4ac9a518d7387ea66918a89946636ee7dd6412f4926fbe7c5ccbb5a5a249f64a` 與 `claims.md` SHA `02ee7918a362ce130bed4a9e2c1491f0da80880207d7c57d6aa9eae1820a3022`，均與 Git HEAD 原檔相等。差分只改 `s53010` 場景模板／卡資料、`s53018` 提示詞及兩筆 claims 畫面欄；其餘 122 景、126 句口播和章界不變。

獨立 `lint --slug curio-s53 --json` exit 0、**0 errors／0 warnings**；正文 114／123 為 `shot`（92.7%），最長連續卡片 1 張，符合系列 ≥70% 及 ≤3 張上限。`npm run test:docs-videos` **236／236 PASS**，`npm run check:tasks` exit 0（只有既存過期領票警告）。私有 manifest SHA `72399b433a156ee5064f35ee2da318f2495afea8a0eacd9c7ad8b891d7df5164`、ledger SHA `786794fa452fc6049b428726516d86d4e1e7a84aca90fa772658fe26e3081499`、jobs SHA `a9d2c69ab3cb5704417b4f0968a7d8d0dae6eb0e35d37e053463220b30d55ca3` 均與 R21 停線相同；14 張舊 KEEP 的 manifest 條目仍在，實際所選檔 SHA 各與 manifest 相符，`STOP` 在位、jobs 空。帳本 **US$0.4590／35 image／34 judge／0 預約**，整集上限 US$4.78；本輪支出零。

後續只可先在 STOP 保護下處理 R22 與舊 manifest 的畫面雜湊綁定，再對 `s53018` 做 **一張**受控 `image-01` 及 judge；逐張看 1280×720 未裁原圖和所選裁圖。若仍有照片背景、正面全身、寬通道、成年／時代或其他畫風問題，停止試畫並另人評估同章 KEEP 重用或來源卡。機器 PASS 不能覆寫來源矛盾，紙審 PASS 也不是完整第二章、網站卡、人耳、音樂或成片核准。
