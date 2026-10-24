# S50 R5｜片尾政策窄修、企劃來源界線與連結：作者凍結

2026-10-20 UTC。R4 完整 `explainer` [Jev 政策回覆](r4-policy.md)的業配分數為 **0.33／上限 0.30，FAIL**；回覆沒有指出單一句子。R5 是作者提出的**候選修訂**，不能由 R4 分數推定片尾就是原因，也不能沿用 R4 的來源、敘事或政策 PASS。尚未對 R5 送出 Jev、網站卡、TTS 或付費媒體。

R5 只改三類文字：

1. `fire999c` 口播從「想從當年的記錄分清傳說與證據，訂閱奇聞檔案局。」改成「**當年的日記和證詞刊本固定版連結，都放在說明欄供你核對。**」；`claims.md` 同步為連結承諾，不作歷史新主張。`video.json.youtube.description` 原已列 Pepys 日記和 1667 年證詞刊本的固定版 URL，因此所說的連結真實存在。這個中性片尾只是政策改稿假設，需以完整新稿重新取得政策回覆。
2. 讀稿時發現 `brief.md` A 方案與濃縮開場段仍留有 R3 已被獨立來源審核退回的「測量員面對的城區／走入火後街區」。兩處窄改為「**刊本留下的城區受損數字／測量員後來留下受損數字**」，不再暗示 A 1667 刊本記有測量員進街的動作；R4 `fire008` 口播本已改為數字層級。這會改企劃雜湊，須另一人重核差分，並使網站舊大綱卡不能充作 R5 核准。
3. 說明欄新增與 S45/S46/S48/S49/S51 相同的奇聞檔案局[頻道 URL](https://www.youtube.com/channel/UCR0rRWT4blMDUwEMx-TZ57Q)。既有五條來源 URL 與對 Gazette／Museum 因代理 CONNECT 403 而未直接重驗的註記均保留。畫面 `outro.data.cta` 仍是「訂閱奇聞檔案局」；企劃的原創 5 秒片頭、共用 21 秒 `v4-endscreen` 與最後 16 秒 Studio 兩推薦框及訂閱圈計畫沒有改。畫面 CTA 與影片說明欄尚非已上傳、可點擊元素。

| R5 內容檔 | SHA-256 |
| --- | --- |
| `brief.md` | `bac9d05082626689833057f30718c0f9d6d798562460335c8bcb834216ed1a3b` |
| `research.md`（R4 不變） | `27f9df563ab8376d2f6ee10837772821534515fd29b86b7e83e259eb56023a95` |
| `claims.md` | `5e4ee9c6aacd0aab79d0f5ca5847229150dacfa451b32df0a25c55ef2eaedf64` |
| `script.md`（CLI 重生） | `009d4ed8204dcd541fc7cfb05cad73d3081ae75fb96a2f9faa71d4361b0a7ad8` |
| `video.json` | `f994e4fee7268364caf049d3fd4a69e00011b06991c77acff03919b5e21ecc67` |

`video.json` 反轉**只有** `fire999c` 文字與說明欄頻道 URL 即重得 R4 SHA `0fa7b40caee68e8d475827ca551d14b15eac14d7f85fec68c0497cd4f80d7a1f`；`claims.md` 反轉該列即重得 R4 SHA `41ebfffe54f72c0fda9f1fd563d90613efb2dbb6757e2d49a8f2e832558b4805`；`brief.md` 反轉上述兩短語即重得 R4 SHA `60040a61dcf7b2b4b62bba30773537d4c559104724a7f6d83926082211d983e1`。`research.md`、其他 118 句、所有視覺提示詞、章節、`loops`、縮圖和來源錨點未變。`script --slug curio-s50` 重生後敘事短碼 `f8ed89791e73d12b`、語音短碼 `7982e6c12b4daf11`；119／119 ID 唯一，`video.json`、`claims.md`、`script.md` 同 ID 同文同序。開場與正文台詞未變，R4 估開場 39–48 秒、正文最快約 8:40，仍須 TTS 實測。

`lint --slug curio-s50 --json` 為 **0 errors／1 warning**，只警告片尾沒有口頭訂閱提醒；畫面訂閱 CTA 仍在，不為消這項警告再加入可疑口播。`git diff --check` 通過。下一位工作者須對 R5 精確 `brief.md` 的測量員界線、`fire999c` 與書面畫面差分獨立覆核；兩名只讀 R5 劇本的全新讀者須重新評 13 題，然後才可用完整 R5 `{ doc, brief }` 做一次新 Jev 政策檢查。網站 outline/script 若再送亦只能稱 `hand_pushed pending`，不冒稱站主網站已核准。政策 PASS 與音訊零旗標前不做圖、配樂或成片。
