# C15 FriXion｜正式專案檔非付費轉換收據

日期：2026-10-24。這份收據記錄已核准原稿到機器專案的轉換；尚無新配音、插圖、配樂、時間軸、成片或後台匯入。站主劇本核准與整支本機試片 US$25 上限分別見 reviews/owner-script-approval.md 和 reviews/owner-paid-pilot-approval.md。

## 原件保全與轉換

| 已核准原件 | Git blob SHA-256，轉換前讀回 |
| --- | --- |
| script.md | C75E85C881F51942C8CAD0BDD0185615F2CBDB6A2CCF2F6EED846724A6ECEBD4 |
| script-source-notes.md | 5429A1B0B04C412A0A50E8F47A4B39123CAE06D9E79771FCBEE9F26F23F2C121 |
| visual-plan.md | 60CD58C0F2BA2874550B34714132CDA8B56712DB81C43C1103F0644B2BB35A45 |
| visual-plan.json | B9E67726FDB99B71B3D6086AC38765EE513171F57E2261213FC843B66BC992A5 |
| treatment.md | D84494C81E2034B116C0322EF416E17C3DDE860B58626D12DE2E73501980D9C0 |
| source-matrix.md | 6E030F4399F6FD2AE99550DE89B5B46658D708CF870910199804069A784C4C09 |

video.json 和 series.json 以 kind story 的「日用品的意外轉身」第 15 集建立；video.json 因現行 core/drama.mjs 的可愛說書 stats 卡相容性用 category explainer，系列身分由 series.json 的 kind story、series slug 和本集 slug 保留。六章依 H01–H08、O01–O13、I01–I18、E01–E15、T01–T13、N01–N20 分組；87 個場景正好承接 87 句原稿，72 張 still 插圖、15 張後製 stats 字卡。每場景唯一原句 ID，原句 text 和候選 prompt／字卡 value 均與核准視覺 JSON 一對一且順序一致，沒有預先拆句、增句或重寫原稿。最長原句紙上 9.36 秒，低於現行單鏡 12 秒硬上限；實際聲音仍待量。

候選插圖維持原稿英文提示詞，不含產品商標或可讀字；video.json 的 look 只有 cute-mystery，所有插圖 visual=still。後製卡的 value 沿用原分鏡 postproduction_text；stats label 和 source 是機器呈現所需的窄說明，正式畫面仍須特別看 1972／1975、微膠囊 μm 與筆尖 mm、E08／E09 研發溫域、N07／N08 兩份文件溫度差異是否分清。claims.md 和 verify-1.md 只把原稿逐句索引及既有獨立來源 PASS 對接 QA；不是新一輪獨立事實審查。兩位 v3 盲讀、最終差異覆核和站主核准仍以其原本雜湊為準。

## 聲音、時間與預算

video.json 暫用既有繁中說書 voice 的 Gemini Sulafat 配置，不代表供應商路由已核可。12 句含拉丁品牌詞的製作列設 say/say_for：PILOT→百樂、Magic Cup→魔法杯、ILLUSION→伊露申、FriXion→魔擦筆；text 完全保留原核准旁白。這些唸法是非付費前製候選，須獨立語音／品牌念法審查與實際聽審後才能當語音驗收，不能從 lint 的詞表消錯推定唸對。T07 沒有改寫。

原分鏡字數代理值：全稿 2,350 字約 564.00 秒；H01–H08 開場 212 字約 50.88 秒；O01–N20 片頭後正文 2,138 字約 513.12 秒；正文 still 約 406.80／513.12 秒，即紙上 79.28%。這些不是 TTS 或真實片格。已核准本機試片上界：72 個基本插圖槽、最多加 12 個、每槽最多 3 次，另 15 張卡、原稿 87 句旁白和 1 首配樂，整片 US$25 硬停線；可見圖片／judge／配樂估額上界約 US$3.482。首筆付費前，仍要讀回單集可歸因預算路由、歷史費用／未結請求、實際供應商與語音／音檢價格、餘額及最壞預留。先實測 O01–N20 正文 TTS 至少 480 秒才可購圖；完成後以片格驗證相關插圖占故事內容至少 70%，並驗收繁中 CC、5 秒片頭、21 秒片尾與結束畫面連結。沒有匯入、上傳或發布。

## 非付費檢查與保留問題

- 87／87 原句 ID、順序及 text 還原；87 景＝72 still＋15 card；六章；12 個 say_for 綁定現行 text；factsChecks：verify-1.md marks no claim NOT FOUND；check:tasks exit 0（其他舊任務警告）。
- node tools/video/cli.mjs lint --slug story-everyday-frixion-c15：狹義 core lint 修正後 **0 errors、6 warnings，exit 0**。核准原句「日本文字」不再誤觸「本文」，同句若另有真正「本文」仍會報錯；詳見獨立認領的 lint 任務。原稿沒有改寫。
- schema.test.mjs、lint.test.mjs、qa/facts.test.mjs 在修正後共 **68／68 PASS**；單獨重跑 lint.test.mjs 為 **50／50 PASS**。drama.test.mjs 在這個 Windows checkout 的 Node test runner 以檔案層級 exit 1 且沒有內層診斷；單獨重跑同樣結果。沒有將此未明測試列為 PASS。
- 六個 warning：adult 出現在 72／72 個核准插圖提示詞、blank 出現在 27／72；紙上鉤子間隔另有 88、72、53、60 秒四處警告。這些是尚待獨立審視的視覺多樣性與敘事節奏問題，未自行改動已核准原稿或候選 prompt。

| 新專案檔 | SHA-256 |
| --- | --- |
| video.json | FB222CAC8FD95FC773F9AEED5F0CAC028C83260C42F604FE9A2568F2FBFCC2F8 |
| series.json | 2CDB882A5037E00B7E2C92BEB8B727EDD3786CC7B14D3F6B2A00D5A619568191 |
| brief.md | 542EA469419527554C2D599FE763157A42C076008FF47829924AC7D2BA7C1C3F |
| claims.md | 49A2559169B2FE55ABF337589DB64E48CEE580BCA1B6D6B21299910927C07EB4 |
| verify-1.md | 6B83984E1C8D1383A0E79A4289BB58B5D4AFEB343DFFB9E74F5AACE8EA3C5F14 |

註：以上 SHA 是撰寫本收據時的工作檔 SHA；後續若改動生成檔，須重算並更新。獨立只讀專案審查見 independent-canonical-conversion-20261024.md，判非付費轉換 PASS、媒體製作 HOLD；本收據不代表付費、匯入或上架。
