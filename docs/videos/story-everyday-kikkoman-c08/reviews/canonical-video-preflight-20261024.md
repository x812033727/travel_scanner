# C08 龜甲萬｜正式專案檔非付費轉換收據

日期：2026-10-24。本次只把站主核准的文字稿與逐鏡方向轉成機器可讀專案，沒有新配音、圖片、配樂、時間軸或成片，也未匯入、上傳或發布。另一位代理的只讀轉換覆核見 independent-canonical-conversion-20261024.md：非付費轉換 PASS、媒體 HOLD。

## 原件保全與核准範圍

| 已核准原件 | SHA-256，轉換前後相同 |
| --- | --- |
| script.md | B9E4C547FFA190609B433D48FF7E27A94B9C9DF4322AEB48104A3163694B3376 |
| visual-plan.md | 776F26F2E15477D443C6D8CFAC0EF32440DCBE5EFA85CA022FEDE7F883A84785 |
| script-source-addendum.md | 82D1147FE720B4ECB3A9222C8A19E76717BC40B4E70B56EA9A3256F5D22DEDE5 |
| treatment.md | 22BCC1A47CDAB1A4A251B4B27F37C75BB98A8BB819DCCF15D4CD6CD64E98E506 |
| source-matrix.md | 0F755DFF2B4F58D9401D1649BE6C7535721C99AFA4D6C88CEDA310F691C57B32 |

站主對前兩個檔案的決定在 owner-script-approval.md；企劃採用在 owner-treatment-approval.md。script.md 和 visual-plan.md 頁首仍稱「初稿／待審」，那是早於核准的原文，不能修改以免解除雜湊綁定。來源判定沿 v3 全量表到 v5.3 差異鏈及兩位新版旁白盲讀；claims.md 和 verify-1.md 僅是既有判定的 QA 對接，不是新一輪來源查核。

## 可還原性及畫面限制

- 六章 84 句原稿，84 個同 ID 場景，順序與 text 完全相同；沒有預先拆句、增句或重寫。73 個 shot 的英文 prompt 與運鏡文字逐列原樣投影，11 張後製卡的完整方向文字保存在 visual-plan.json。卡片最長連續一張，73／84 即 86.9% 是鏡數，不是畫面秒數。
- video.json 的 11 個 stats 場景是機器預覽，只用原分鏡卡片所述的數字或短句及來源。c080407 原核准方向另有「泛用瓶嘴側面輪廓」；現行 stats 樣板只能排文字，正式後製須按 visual-plan.json 加示意並獨立驗收，不能把純文字預覽視為該鏡完成。c080506 的兩開口大小比較也須驗收真正後製畫面，不能畫成精確實物比例。
- 原稿五句 GK 只在候選語音的 say 欄分隔為 G K、由 say_for 綁定原 text；字幕與核准逐字稿完全不改。這是朗讀候選，尚未經獨立念法審查或真人聽審，不能因 lexicon lint 不報錯就宣布唸法通過。
- video.json 因目前 core/drama.mjs 的 cute-mystery stats 卡相容性採 category explainer；series.json 的 kind story、系列 slug 與第 8 集保留品牌故事身分。正式後台匯入時須讀回分類與系列歸屬。

## 時長、預算與片尾 HOLD

核准原稿第 2–6 章有 76 句，直接按 text 計算為 1,927 units／462.48 秒；採機器專案五處 GK 候選 say 與 core spokenText 重算則為 1,937 units／464.88 秒。兩者都只是按 250 units/min 換算的紙上代理量，並非 TTS 實長，也不達成正文至少 480 秒的證明。lint 顯示約 9.9 分鐘是連同開場、場景停頓與畫面間隔的整體紙上時間，不能取代正文純語音量測。正式畫面時間亦須證明插圖占正文至少 70%。

C08 沒有 production-quote.md 或站主專屬的付費試片上限核准。其他集的 US$25 決定不移轉到本集；在可歸因預算路由、歷史費用與供應商讀回、整支數量／嘗試次數／總額報價及站主核准前，不呼叫付費 TTS、MiniMax、Jev 或配樂。

本次 lint 的唯一 error 是已核准的 c080611 片尾原句：「想接著看其他日用品怎麼意外轉身，訂閱頻道，下一集繼續拆開來看。」現行奇聞檔案局規則禁止片尾預告確定的「下一集」。這是原稿與現行規則的真實衝突，不能改 lint、靠 say 遮住，或私自改寫機器稿。下列僅是待審的最小候選，**沒有寫進 script.md 或 video.json**：

| 候選 | 完整替換句 | 相對原句 |
| --- | --- | --- |
| A | 想接著看其他日用品怎麼意外轉身，訂閱頻道，繼續一起拆開來看。 | 只把「下一集繼續」改成「繼續一起」，不承諾下一集題目或時程。 |
| B | 想看更多日用品怎麼意外轉身，歡迎訂閱頻道，和我一起拆開來看。 | 保留訂閱理由，改為不指定下一集的系列邀請。 |

若採候選，須先對 c080611 與相鄰結尾做新差異來源／畫面查核和只讀旁白盲讀，再取得站主對新版確切雜湊的稿件核准。修改正文以補足 480 秒也同樣需要來源、敘事與站主重核。未核准前，C08 不可當作 lint 綠燈或可付費、可上架成片。

## 非付費預檢

- 作者逐列比對：84／84 旁白 ID、text、逐鏡 ID、shot prompt、運鏡與卡片原方向相符；73 still、11 card、六章、五個 say_for 與五份核准原件 SHA 均通過。
- node tools/video/cli.mjs lint --slug story-everyday-kikkoman-c08：1 error、13 warnings，exit 1。唯一 error 如上；警告含四個無明示景別的原 prompt、瓶子／generic 提示詞重複、三鏡紙上逾 10 秒、五段鉤子間隔逾 45 秒、開場只種兩個 loop 與「一九六一年」重述。警告保持可見，未為消警告改動已核准旁白或逐鏡。
- factsChecks：verify-1.md marks no claim NOT FOUND，PASS；schema/lint/facts 針對性單元測試 67／67 PASS；npm run check:tasks exit 0，只有其他舊票的警告。

| 新專案檔 | SHA-256 |
| --- | --- |
| video.json | 57371891A62B0B8F4E6DDBD9E5FFEA196DADE2EF3D92B5F4BC17C319DD0805B2 |
| visual-plan.json | B505F4E7464B539FF0833E5B3851F445BD262B156969FD605739A03D02199CB2 |
| series.json | 45595A5ED0D415FC9269E04C617A65B0287CCAA885935D86B5BD6DBB85535E20 |
| brief.md | B66B69CC4F9617E946B00B821CBBA819B356CE6A734C3C34DF5845EB04A983DF |
| claims.md | E70EE7655C0BA5A05885752C894300BE1C2676540F89528493E1AFC9D8E26F1B |
| verify-1.md | D8232211492E279E58BC23F45C276D41FF49B74B74215DF86408B53554282FCC |

上述新檔雜湊在本收據撰寫時讀回；若後續修改生成檔，須重算並更新。本收據不表示 lint 通過、付費製作或上架完成。
