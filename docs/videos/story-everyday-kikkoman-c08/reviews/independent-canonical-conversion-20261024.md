# C08 龜甲萬｜正式專案檔獨立轉換覆核

日期：2026-10-24。結論：**非付費 canonical 轉換 PASS；lint、媒體與上架 HOLD**。覆核只讀 Git HEAD 的核准原件與 index 的新專案檔，沒有改稿、付費生成、匯入或上傳。

## 精確輸入

| 核准原件 | Git blob SHA-256 |
| --- | --- |
| script.md | B9E4C547FFA190609B433D48FF7E27A94B9C9DF4322AEB48104A3163694B3376 |
| visual-plan.md | 776F26F2E15477D443C6D8CFAC0EF32440DCBE5EFA85CA022FEDE7F883A84785 |
| script-source-addendum.md | 82D1147FE720B4ECB3A9222C8A19E76717BC40B4E70B56EA9A3256F5D22DEDE5 |
| treatment.md | 22BCC1A47CDAB1A4A251B4B27F37C75BB98A8BB819DCCF15D4CD6CD64E98E506 |
| source-matrix.md | 0F755DFF2B4F58D9401D1649BE6C7535721C99AFA4D6C88CEDA310F691C57B32 |

原件在 HEAD、index 與工作檔一致；前兩份與 owner-script-approval.md、企劃與 owner-treatment-approval.md 的 SHA 綁定一致。新 video.json 的 index SHA-256 為 `57371891A62B0B8F4E6DDBD9E5FFEA196DADE2EF3D92B5F4BC17C319DD0805B2`；visual-plan.json 為 `B505F4E7464B539FF0833E5B3851F445BD262B156969FD605739A03D02199CB2`。

## 逐項判定

- 核准 script／visual 與新檔逐列 84／84 ID、順序和旁白 text 完全一致。73／73 個 shot prompt 與運鏡逐字保留；11／11 張後製卡的**完整**原方向保存在 visual-plan.json，六章句數 8／18／13／11／25／9，最多一張連續字卡，九個 loop 保留。
- claims.md 和 verify-1.md 各 84／84 ID 與既有來源限制對應；verify 是先前查核鏈的 QA 對接，並非本次重做的史料研究。video.sources 包含採用的 12 個網址；source addendum 第 13 個未採用網址有清楚標示。候選圖片提示詞沒有被禁用的品牌／人名。
- 五處 GK 候選 say_for 均等於對應**原 text** SHA-256 前 12 位；這只驗證綁定，不能當作真人發音驗收。
- 按 text 計算正文 1,927 units／462.48 秒；套入 GK 候選說法後按 core spokenText 計算 1,937 units／464.88 秒。兩者都是紙上代理值且低於 480 秒，沒有實際 TTS。73／84 是鏡數占比，並非實際插圖片格時間。

## 不可越過的問題

- lint 實跑為 **1 error／13 warnings，exit 1**。c080611 核准原句的「下一集」確實違反現行片尾規則，不能改 lint、用 say 隱藏或私改受核准雜湊保護的原稿。作者收據列的 A／B 是尚未採用的最小改句；需先做新版逐句來源／畫面差異查核、旁白盲讀及站主核准，再同步更新 script、visual 和衍生檔。
- c080407 核准的是泛用瓶嘴側面輪廓；目前 stats 模板只排文字（tools/video/templates/templates.mjs:548–554），video.json 的 label 不是那張示意圖。c080506 的兩開口大小對照也須在後製畫面製出並驗收。
- C08 沒有自己的整支報價、付費上限核准或可歸因預算路由。首次付費、實測正文 ≥480 秒、正式插圖畫面占比 ≥70%、音訊／字幕／成片／後台／上傳驗收都未完成。

本收據支持保存**非付費轉換成果**與待審差異，不能作為「lint PASS」、「製作完成」或「可上架」的證據。
