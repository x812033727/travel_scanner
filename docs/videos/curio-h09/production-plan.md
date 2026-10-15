# 奇聞檔案局 H09｜製作與關卡

狀態：更新版大綱 A 已核准。Colorado（BB-45）的艦種已由「巡洋艦」更正為「戰艦」；正式 `script.md` SHA-256 `E9404ADD9954E66AA6C26FC3725D7C0ABD09D91B9E571ED2631C152E4579633C` 經獨立史料與十三題敘事收據通過，後台已讀回站主核准。B06 單句重錄後的時間軸 SHA-256 `69E3FF3DC95E6EF3811044DC765EEEEEE79D02E28F2F829C68B95171A2691BC2` 也已讀回站主核准。插畫 92／92 鏡有 selected image，0 鏡 `needs_review`；四頁分鏡聯絡表已由站主在 `/admin/videos` 核准，`review-pull` 綁定 manifest SHA-256 `4E8D778DEDB8A67816E37E11304A9028A5C021C7F8513AB2153B9F47C0654FFA`。字卡與縮圖已渲染，92 鏡皆是零購買片段的靜圖慢運鏡。繁中成片與 111 條字幕已完成，獨立抽看通過；站主已在後台核准 `final.mp4` SHA-256 `BE7FC71416AFBBF84BD228470FAAE4CBA9AD47D803FD2CEE3C00A7AD04E5F956`。英、日、韓標題說明、字幕及配音均已由站主勾選；三語翻譯與獨立審稿已完成，站主已另授權多語配音與音訊 QA，新增 US$2.00 估算停手上限；日語新版已合成、完成增量 QA 並由站主試聽接受；韓語五句定向重錄與增量 QA 已完成，九句殘餘旗標待站主試聽；英語音軌已合成，完整音訊 QA 尚在執行。H09 專屬 `STOP` 已恢復；圖片帳本 US$2.403、零預留。站主授權繁中旁白、音訊 QA、插畫合計 US$4.50 估算停手上限，不含多語或上傳；圖片與評審的本集執行上限為 US$3.80。

## 作品規格

- 單一問題：1937 年艾蜜莉亞・艾爾哈特與佛瑞德・努南失聯後，已知證據能把飛機定位到豪蘭島附近海域，還是尼庫馬羅羅島？結尾是「未結」，不把任一假說說成定論。
- 繁中先行；正文至少 8 分鐘，目標約 10 分鐘；先用一個具體的 8:43 電台場景作 30–60 秒開場，頻道片頭接在其後。片尾用 v4 結束畫面，不在旁白點名下一集。
- `format: "drama"` 的無角色可愛解說；`look: { "preset": "cute-mystery" }`；插畫使用 MiniMax `image-01`。歷史人物只畫逝世超過 70 年者的卡通化形象，現代研究者不畫本人。
- 插畫呈現故事，不假扮成照片、考古證據或飛機殘骸的重建。日期、數字、機構立場與來源用少量卡片；正文至少 70% 是插畫，連續卡片最多三張。
- 公有領域檔案照片和文件的授權要逐件核對，若使用則當貼圖式來源卡。2026 年探勘現場影像未取得授權前不放進成片。

## 畫面預算與停手上限

下表依 2026-10-15 的 `video.json` 逐景計數；92 張插畫已生成、逐圖驗收，四頁分鏡聯絡表也已獲站主核准。劇本修改或 TTS 時間軸若要求重新切景，須重新計數與報價。

| 段落 | 插畫景 | 來源／數字卡 | 鏡頭任務 |
| --- | ---: | ---: | --- |
| 8:43 開場濃縮 | 9 | 0 | 耳機、電台、海面；三個未揭曉的未來時刻 |
| 最後電訊與位置線 | 10 | 1 | 人、飛機、海圖；卡片只放 157／337 |
| 1937 年搜索 | 17 | 2 | 艦艇、搜索、豪蘭島；海軍判斷與島上假說分開標 |
| 1940 年島上電報 | 12 | 1 | 島上調查與文件，絕不畫遺骨成真品 |
| 1941／2018 年骨骸判讀 | 12 | 1 | 研究者只畫手／資料；把兩次判讀分清 |
| 2020／2024 年兩處異常 | 12 | 1 | 深海岩石與 Taraia 是兩個目標 |
| 2026 年 Taraia 現場調查 | 18 | 1 | 10／13 沙洲踏查、10／14 無人機與磁力／側掃聲納已開始；探針／清淤仍待做，沒有 Electra 鑑定結果 |
| 未結與結束畫面 | 2 | 1 | 最後一個插畫回呼和片尾 |
| **已核准分鏡** | **92** | **8** | **正文插畫占 92／99（outro 不計），約 93%** |

開畫前 `keyframes --dry-run --takes 3` 對 92 張、MiniMax `image-01`、1K 的報價為首輪約 US$1.242、每張最多三輪的圖片與評審總額約 US$3.726；這是開畫前估價，新增有據重畫後不能當作目前預算。現行 manifest 為 92／92 鏡，媒體帳本有 178 次圖片與 178 次評審，US$2.403、零預留；已付費音訊不在這份媒體帳本。站主已授權 Gemini Sulafat 旁白、Gemini 轉寫／TypeSafe Jev QA 與整集 MiniMax 插畫，三項合計 US$4.50 為估算停手上限，未含多語或上傳。為原始旁白、F03／Z01／B06 重錄及反覆音訊 QA 留額度，本集圖片與評審的執行上限收緊至 US$3.80，`series.json` 的 `media_cap_usd` 執行這個上限；圖片帳本目前距此上限尚有 US$1.397，總上限另留 US$0.70 給音訊與 QA 的歷次估計成本。92 鏡已畫完，不因剩餘額度增加無證據的重畫。共用的 US$200 後台設定不能代表 H09 上限；供應商帳單與音訊 QA 的實際 token 費用尚未取得，所有數字只是模型價目與本機帳本估算，不能說成發票級保證。任何新增付費工作前都應重核總估算，不足就停。Google 價目：https://ai.google.dev/gemini-api/docs/pricing 。

## 多語製作授權與停手

站主於 2026-10-15 另行授權將 H09 的英、日、韓文稿送 Gemini 配音與轉寫，並用 TypeSafe Jev 判讀音訊差異；多語新增 US$2.00 為**估算停手上限**，與原繁中旁白／QA／插畫 US$4.50 合計規劃上限 US$6.50，不含上傳。三語文稿已獨立審稿、來源雜湊有效；合併 main 後的乾跑分別為 7,146、3,236、3,244 計費字元，合計 13,626，18／300 句估需不超過 1.15 倍加速，0 句無法塞入時槽。這些不是實際供應商發票或最高計費量。

多語 `dub` 與 `check-audio` 沒有 H09 專屬美元硬上限。每次只執行一個語言，先確認本集 `STOP` 與配音服務狀態，再暫時移開 `STOP`；每語完成後恢復 `STOP`，核對快取、時槽、轉寫旗標與累計費用估算。若估計會超過新增 US$2.00、帳單／回應不明、或出現不確定的付費工作，立即停手並留下原有快取與 hold。舊的繁中成片核准不代替外語音軌試聽及後台語言關卡。

2026-10-15 多語執行中收據：日語首輪 100 句／3,236 計費字元，第一次定向重錄 14 句／466 字元，再修正 ALI 正式名稱 1 句／42 字元；新版實測 4／100 時槽需加速，最高 1.12 倍，零超時。新版 check-audio 為 63 句逐字、19 句 Jev 接受、9 句由第二轉寫清除、9 句殘餘旗標。站主已在本對話回覆「日語旁白可以」，本機 review/dub-ja-owner-acceptance.json 綁定音軌 SHA-256 4f091b943757ba5005d3814a893a3ea25bce08074352272dc16aafdcddc9b695 與九句逐句錄音；原 QA flags 保留，人工接受不冒記為 Jev 全過、主旁白關卡或 Studio 已上傳。韓語首輪 100 句／3,244 字元，QA 為 68 句逐字、9 句 Jev 接受、9 句由第二轉寫清除、14 句旗標；取得站主韓語檔案移交授權後，只修有據的五句，乾跑 5 次／175 字元、零超時，定向合成已完成且 100／100 時槽無加速、無超時。新版韓語 QA 為 72 句逐字、10 句 Jev 接受、9 句由第二轉寫清除、9 句殘餘旗標；五句新錄音全部獲自動接受。review/dub-ko.html 已交站主試聽，綁定音軌 SHA-256 5b0f7422a759a820c10acfcf06893fbfe2a32e656d6d3a66a21fa9137f7748f3。英語 100 次／7,146 字元已合成，100 時槽無加速、無超時；第一套轉寫 73 句逐字、27 句經 Jev 判讀，其中 20 句正做離線第二轉寫。每一付費階段結束都恢復 H09 STOP，本機候選交付包已建立；英語音訊 QA 與韓語站主試聽完成前，仍不視為全部音訊已驗收。

## 路線與安全邊界

本集選用本機 `format: "drama"` 的單集可愛解說，風格 `cute-mystery`，目標約 10 分鐘，圖片 `image-01`。後台另有單集自動路線：建立請求後會安排企劃模型寫故事聖經，站主核准文件後再寫劇本；企劃與撰稿的模型呼叫可能立即產生費用。本集未走該路線。

2026-10-15 已在後台唯讀讀回 `series_script_gate=ON`、`auto_pick_look=ON`、`auto_approve_storyboard=ON`、`max_usd_per_video=US$200`；未建立 H09 請求。`max_usd_per_video` 是**共用設定**，不是 H09 的專屬圖片上限；`0` 會關閉上限。單集沒有可靠的「提交後立刻暫停」操作。站主核准劇本後，圖片流程可能自動展開，所以送出或放行相關階段前要有可執行的單集費用控制。共用 US$200 不能約束 H09，調低又可能影響 H07 或其他片；本集先在本機 `format: "drama"` 的受控產線預製作，不把全站上限視為單集授權。後台企劃與劇本 AI 呼叫也可能產生費用，尚未啟動。

## 驗收與交付

1. 大綱與劇本：來源逐項核對、盲評現行十三題、`lint` 零錯誤、站主在後台核准相應文件；`loops` 每個懸念有回收。
2. 付費前：依定稿景數與媒體狀態乾跑報價，取得 H09 整集一次授權；每個重畫只以違反九題圖像評審、與旁白矛盾或畫風漂移為由。
3. 音訊與視覺：TTS 時間軸及試聽、插畫聯絡表逐張驗收、分鏡關卡、實際片頭片尾、字幕同步、成片自動 QA。
4. 時效性：成片前與上架包送出前重查 Purdue／ALI 的現場結果；若新證據改變結論，重新查核、改稿並使相關核准重走。`資料截至` 寫實際查核日。
5. 上架包：繁中先完成，其它語言依 H09 自己的後台勾選；私人上傳、發布與播放驗證分開留證，發布由站主執行。

## 2026-10-15 本機預檢收據

- 獨立史料覆核與十一題敘事盲評重新 PASS，均綁定 `script-draft.md` SHA-256 `361ECEA6E3FFDF8283F7B3C1C325E1C9B83FA122E67AACB3C637A41BDCA11F83`；`verify-1.md`、`narrative-blind.md` 記錄 10／13→10／14 的事實及敘事修訂。獨立 `visual-qa.md` 分鏡文字 QA 綁定 `video.json` SHA-256 `F3159462A1B030FE197E2B35D552D6AE74B3EF40587B6C4ACDAE2842AE2766D2`，確認 95 句拆成 100 個配音段仍逐字一致、92 張待生成插畫、7 張字卡及 1 張片尾。這不等於實際插畫驗收。
- `node tools/video/cli.mjs lint --slug curio-h09`：0 錯誤、3 項敘事啟發式警告、估時 11.2 分鐘。兩段超過 90 秒的提醒須以實際配音時間軸重新核對；片尾「回到最初那條線」是回收主題的回答，仍須聽稿確認是否自然。`script --slug` 已重產正式送審用 `script.md`，SHA-256 `3B1ECF0743F7BD83333ED68E697219333E81BBDCF7392C92D976F62BA6627D4C`。
- `tts --dry-run`：100 次請求、約 2,654 個計費字元，沒有合成。`keyframes --dry-run --takes 3`：92 景，首輪約 US$1.24、每景最多三輪約 US$3.73，當前媒體帳本 US$0.00；沒有產圖。主機目前共用的每片上限仍是 US$200，**不是**本集授權或本集硬上限。開畫前須就 H09 取得整批美元上限；以本機人工檢查帳本與停止執行來約束，不得把 US$200 當成可花額度。
- `npm run check:tasks` 通過。`npm run test:docs-videos` 為 214／215 通過；唯一失敗是未修改的 `imported-long-languages/runner.test.mjs` 在 Windows 子行程 `package-runtime.mjs` 以 `3221226505` 崩潰，單獨重跑相同。這項失敗不在 H09 檔案範圍內，沒有被誤報成全綠。
- 2026-10-15 `review-pull --gate outline` 將含 Purdue 10／14 進度的 `brief.md`（SHA-256 `D93595C10AB24AD8AE55F5C7BD9A246FA7B4EFA6DE4D8626A318AB1FD511A83A`）讀回為站主核准大綱 A；本機 `approvals.json` 記錄 approved_at=`2026-10-14T23:48:50.461Z`。正式 `script.md`（SHA-256 `3B1ECF0743F7BD83333ED68E697219333E81BBDCF7392C92D976F62BA6627D4C`）已 `review-push --gate script`，隨後 `review-pull --gate script` 讀回站主核准；本機 `approvals.json` 記錄 approved_at=`2026-10-14T23:51:59.021Z`，對應的 `script.md` 雜湊與工作目錄一致。劇本核准尚未涵蓋音訊或圖片費用。
- 2026-10-15 再查 Purdue／PRF 官方最新仍為 10／14 的 Taraia 水下測勘開始公告，資料尚待分析，未確認機體；目前核准稿不用修訂，成片前仍須再查。旁白合成命令曾提出執行，但自動審核拒絕把完整稿件送到 Gemini，理由是劇本核准並非外部合成的明確授權；命令未執行，沒有產生音檔或費用。
- 2026-10-15 站主明確授權把 H09 的 100 句稿件送 Gemini Sulafat 製作繁中旁白，並以 MiniMax image-01 產整集 92 張插畫；另同意 Gemini 轉寫／TypeSafe Jev 音訊 QA，三項合計 US$4.50 為停手上限。首輪 TTS exit 0：100 句、2,654 計費字元、0 句重用，實際 narration.wav 657.933 秒（10:57），ffmpeg 完整解碼；依 Google 2026 Standard 音訊輸出率估約 US$0.1480，文字輸入及最終帳單未量得。圖片 ledger 仍 US$0.00。逐句檢查發現 h1j3jy6q.say 重複「研究團體」，只修該覆寫；正文與 narrative hash 不變，script.md 新 SHA-256 7294FD9410349DCBA89347631DF46A551C8A6C570A58983BE11E58A073FA41D5，已重新 review-push 並從後台讀回新版 script.md 核准，approvals.json 記錄 approved_at=`2026-10-15T00:10:29.529Z`。第二次 TTS exit 0：只重錄 1 句（28 字元），99 句快取重用，新 narration.wav 657.233 秒（10:57），完整解碼；乾跑 0 句待合成。Gemini 轉寫與 Jev 音訊 QA 已完成：100 句均已轉寫，20 句為自動差異旗標，不等同證實念錯。站主已逐句試聽並回覆「旁白可以」；音訊卡在 `/admin/videos` 核准，`review-pull --gate audio` 讀回 `timeline.json` SHA-256 `DD46E9CC89C4BBC03C0500BA98AEB973B1D6328C6C3792CB0C56349D21BD8CF7`，approved_at=`2026-10-15T00:46:46.700Z`。插畫未啟動。

- 2026-10-15 付費產圖前，自動審核拒絕 `keyframes --takes 3`：離線 `drama_preflight.mjs` 固定用 Gemini 圖價誤報三輪約 US$39.74，而真實 `image-01` 乾跑報約 US$3.73；當時 CLI 只有共用 US$200 上限，評審失聯也可能少記帳。該命令未執行，H09 圖片帳本 US$0.00。已另認領窄票修正預檢與單集媒體上限；修好、測試及重新送審前不呼叫付費圖片 API。
- 2026-10-15 再預檢：本機目錄與正式站均選 `image-01` 1K；92 張首輪 US$1.242，最多三輪圖片加評審 US$3.726，本集圖片／評審估算上限 US$3.84，正式站 H09 帳本仍 US$0.00。`Stage.generate` 與 `Stage.judge` 都在付費 POST 前預留並查本集上限；圖片失聯／5xx 不自動重送，已計費的失敗工作按回報正價記錄。`stages.test.mjs` 聚焦測試 30／30 通過；`npm run check:tasks` 通過。全套 `test:tools` 在 Windows 出現多個無診斷的子程序失敗，未宣稱通過。舊旁白與 QA 的供應商實際帳單不可得，US$4.50 是依價目估算的停手控制，不是發票級保證。
- 2026-10-15 臺灣時間 09:20 再看 PRF／ALI 官網與普渡 10／14 正式公告，未發現更新的機體鑑定；磁力儀與側掃聲納資料仍待分析，核准稿維持「未結」。來源：https://amelia.prf.org/ 、https://www.purdue.edu/newsroom/2026/Q4/earhart-expedition-update-underwater-survey-of-taraia-object-begins/ 。發布前仍須再查一次。
- 2026-10-15 原本的整批 `keyframes --slug curio-h09 --takes 3` 通過執行審核後開始；第 7 鏡後用本集 `STOP` 暫停。首版 7／92 鏡、11 次圖片與 11 次評審入帳 US$0.1485，無未結預留；`low-fuel-warning` 與 `uncertain-broadcasts` 各三輪仍為 `needs_review`。人工冷看發現另四鏡的船上人物、手勢或飛機擬人問題，即使評審 pass 亦未人工通過；細節見 `visual-qa.md`。只修改六鏡畫面提示詞，`video.json` SHA-256 `C8EA0BB8352FFEE86A2B7D113D1256C86321045EE39C18A8D8E94381A70B5075`；已核准 `script.md` SHA-256 仍是 `7294FD9410349DCBA89347631DF46A551C8A6C570A58983BE11E58A073FA41D5`。修訂後 lint 為 0 錯誤、原有 3 項敘事警告；新版尚未重新生圖。首版圖片與收據保留以便比較；下一步是新 SHA 的七鏡小樣、逐張驗收、再決定整批 92 鏡。

- 2026-10-15 現行十三題規則及提示詞全片覆核後，`video.json` SHA-256 為 `4BA994EE7838E8E324B40DC9364E48E62212D7E9FB83FEE8B3E49C19C8F2A8C9`。四張已付費合格圖的 image key 逐一與 manifest 相符，可用快取；Itasca 地貌錯誤、另兩鏡評審未過，須有據重畫。`review-push --gate script` 重產正式稿為 SHA-256 `D63D46A3E93F7469B9A610CDBD83FB599A1A313D9AAA0A0233EF02C1951C9F82`，後台 `review-pull` 已讀回此版核准；獨立史料及十三題敘事收據已重新綁定此檔。舊 F2890AA3… 是送審前檔案雜湊，不能當現行核准證據。
- 2026-10-15 核准後 TTS 乾跑為 2 句／74 計費字元；實跑僅合成 F03、Z01，98 句快取重用，新 `narration.wav` 657.333 秒（10:57）、ffmpeg 完整解碼；再乾跑 0 句待合成。新 `timeline.json` SHA-256 `4D9E93A62523ECD1579DDCB854F175FE0538748133641BDBC092019119F96538`。`check-audio` 只新轉寫 2 句、呼叫 Jev 1 次；F03 逐字吻合，Z01 轉寫字面差異獲 Jev 0.51（閾值 0.5），其餘 19 個旗標均不在這兩句，且為先前站主已試聽的舊句。`review-push --gate audio` 已送新版時間軸，`review-pull` 仍顯示等待站主。`STOP` 曾在核對無 H09 背景程序、媒體帳本無預留及現行劇本核准後暫時移除以重錄；音訊送審後已重新建立 H09 專屬 `STOP`，等待站主核准才繼續產圖。媒體帳本仍是 US$0.1485，未執行新插畫呼叫。供應商音訊與 QA 發票未取得，總額控制仍是價目估算。
- PR #1503 的首個成本控制提交 `5800dd6c2` 在 Linux CI 的 `video-tests` 等檢查出現六個媒體整合測試回歸；已修正重判預留／入帳邏輯和兩項舊的帳本斷言，`stages.test.mjs` 聚焦 32／32 通過。本機 Windows 整合測試子程序仍無診斷地崩潰，須待後續提交的 Linux CI 確認；CI 未轉綠前不再付費產圖。
- 2026-10-15 站主已於後台核准新版音訊；`review-pull --gate audio` 把現行 `timeline.json` SHA-256 `4D9E93A62523ECD1579DDCB854F175FE0538748133641BDBC092019119F96538` 記入 `approvals.json`，approved_at=`2026-10-15T03:18:04.384Z`。確認現行檔案雜湊一致、無 H09 node／ffmpeg 背景程序、圖片帳本 US$0.1485 且零預留後，僅移除 H09 專屬 `STOP`。定向重畫 `itasca-waits`、`low-fuel-warning`、`uncertain-broadcasts` 各一輪，評審皆通過且人工看圖沒有舊版史實／構圖問題；其餘四張合格付費圖保留快取。定向重畫後圖片帳本約 US$0.19；整批 92 鏡已按 `--takes 3` 和本集 US$3.80 圖片上限啟動，結果仍待完成與逐張驗收。普渡／PRF 於 10／15 再查仍以 10／14 探測進度為最新公告，尚無 Electra 鑑定結果。
- 2026-10-15 首次整批在 28 鏡、US$0.648、零預留時受 H09 `STOP` 暫停：獨立看圖指出 `search-from-howland`、`colorado-over-gardner` 把低平環礁畫成高山，`pilot-sees-empty` 尚未完成且首張也畫成山崖；`colorado-seaplane` 雖得 7.18 分通過，人物與飛機融合、輪式飛機無浮筒，無法表達旁白的「水上飛機」。`video.json` 只改這些有證據的鏡頭及未產出的高風險環礁畫面提示詞，已通過的其他圖依 key 保留。修水上飛機提示詞時以[美國海軍搜尋史](https://www.history.navy.mil/content/history/museums/nnam/education/articles/from-the-cockpit--stories-of-naval-aviation/naval-aviation-and-the-search-for-amelia-earhart.html)確認 Colorado 為 battleship BB-45 且派 O3U Corsair 水上飛機；因此 `claims.md`、草稿 B06、`video.json` 一句及朗讀覆寫由「巡洋艦」改「戰艦」，正式 `script.md` 重產為 SHA-256 `E9404ADD9954E66AA6C26FC3725D7C0ABD09D91B9E571ED2631C152E4579633C`。lint 0 錯誤、原有 3 項警告；此稿與後續音訊須重新走核准，完成前不再付費產圖。
- 2026-10-15 獨立史料收據與十三題敘事收據均重新綁定 `E9404ADD…`，100 句逐句核對；敘事 13 題皆通過，沒有失敗或提醒。站主於 `/admin/videos` 核准，`review-pull --gate script` 於 `2026-10-15T03:51:16.998Z` 讀回與本機 `script.md` 完全相同的 SHA-256。`tts --dry-run` 僅有 B06 `h0z9kbbf` 一句／23 字元待合成；在確認無 H09 媒體程序、圖片帳本 US$0.648 且零預留後，暫時移開 H09 專屬 `STOP`，一般 `tts` 僅合成這一句，重用其餘 99 句，音訊 10:57 且 ffmpeg 完整解碼，乾跑歸零。新 `timeline.json` SHA-256 `69E3FF3DC95E6EF3811044DC765EEEEEE79D02E28F2F829C68B95171A2691BC2`；`check-audio` 僅新轉寫該句，逐字吻合、零新 Jev 呼叫，餘 19 旗標皆為先前站主已試聽的舊音。新版試聽頁已更新，音訊已 `review-push` 到後台、目前等待站主；`STOP` 已恢復，在音訊核准前不繼續付費插畫。
- 2026-10-15 站主核准新版音訊，`review-pull --gate audio` 於 `2026-10-15T04:00:39.431Z` 記錄 `timeline.json` SHA-256 `69E3FF3DC95E6EF3811044DC765EEEEEE79D02E28F2F829C68B95171A2691BC2`，與本機檔案一致。定向重畫兩處山地、第一張未完成的搜索機鏡頭及水上飛機鏡頭，再把兩張因圖中字樣未過自動評審的鏡頭改成無帽無線電員與簡化位置線，現行 `video.json` SHA-256 `2B84A62E17B47FA7B5BC8905CD9E01D148A619FF348610318E15E2AD87F39389`；28 鏡均有 selected image、0 鏡 `needs_review`。已選水上飛機圖仍是概念性示意，浮筒及一個極小輪點不完全符合 O3U 史照，待完整分鏡一併讓站主檢視；未宣稱它是精確機型復原。媒體帳本 59 張圖與 59 次評審 US$0.7965、零預留；剩餘 64 鏡未製作，分鏡與成片未送審。
- 2026-10-15 全片插畫、分鏡與本機剪輯起點：`video.json` 最終畫面提示詞 SHA-256 `72E29DCF4C62A2C58B7F1AE6B701FBD7DDD7FBD2467687A370A3C436B822C1A7`，正式劇本 E940 與音訊時間軸 69E3 均未改。全 92 鏡 selected image、0 `needs_review`，四頁聯絡表經獨立逐頁檢查及站主檢視，後台 `review-pull --gate storyboard` 在 `2026-10-15T05:43:44.681Z` 讀回 manifest SHA-256 `4E8D778DEDB8A67816E37E11304A9028A5C021C7F8513AB2153B9F47C0654FFA` 的核准。帳本 178 圖／178 評審、US$2.403、零預留；一次逾時請求經兩次正式站唯讀查無工作後才釋放單筆預留並定向重送，詳見 `visual-qa.md`。Purdue／PRF 於 05:15 UTC 再查，最新可見仍是 10／14 調查開始公告，尚無確證殘骸，劇本「截至十月十四日」不需變動。`render` 已產 8 張字卡／縮圖狀態；`clips --dry-run` 確認 92 張皆為 still、0 段需買，實跑產生 92 筆靜圖 clip manifest、0 付費片段。`music --dry-run` 顯示此集沒有設定音樂，未啟動配樂服務。此檢查點本機 `assemble` 尚在進行；完成結果另記於下一條。
- 2026-10-15 繁中成片與字幕：`assemble` exit 0，100／100 片段、20,493 影格、`checks.json` 的 `ok=true` 且 `problems=[]`；1920×1080、30 fps H.264 與 48 kHz 雙聲道 AAC，片長 683.100 秒（11:23.1），音量 −14 LUFS、true peak −0.9 dBFS，片頭在 58.80 秒。`final.mp4` SHA-256 `BE7FC71416AFBBF84BD228470FAAE4CBA9AD47D803FD2CEE3C00A7AD04E5F956`；`STOP` 已恢復。`captions` 本機產出繁中 111 條 SRT，開頭 00:00、最後一條結束於 11:00.687，核准的 `timeline.json` SHA-256 仍為 `69E3FF3DC95E6EF3811044DC765EEEEEE79D02E28F2F829C68B95171A2691BC2`。本機 lint 0 錯誤、原有 3 項啟發式提醒；`npm run check:tasks` 通過；`npm run test:docs-videos` 214／215 通過，唯一失敗是先前已見的 Windows `imported-long-languages` 子程序 exit `3221226505`、沒有診斷輸出。獨立抽看對整部聲畫完整解碼，核對片頭／旁白對齊、2024 深海聲納與 2026 Taraia、未來探測的條件語氣及片尾，未見空白、裁切或錯誤發現宣稱；最終 QA／站主成片核准尚未完成。

## 多語交付前再查與檢查（2026-10-15）

- 再查 Purdue 官方 Earhart 專題最新仍為 2026-10-14 的水下測勘開始公告，未查到已確認 Electra 殘骸的官方結果；現行稿保留「截至十月十四日」及尚未定案的結尾。來源：https://www.purdue.edu/newsroom/2026/Q4/earhart-expedition-update-underwater-survey-of-taraia-object-begins/ 。
- 本輪 lint：0 errors、3 個未改繁中鏡頭／敘事啟發式 warnings；long-form check：473 plans PASS。check:tasks：1911 files PASS，只有既有其他票的認領／範圍警告。
- 本輪 test:docs-videos：214／215 PASS；唯一失敗仍是 imported-long-languages/runner.test.mjs 的 package-runtime.mjs Windows 子行程以 3221226505 結束，無 stdout/stderr。沒有將此環境問題記為全綠，也沒有為本次文案變更修改共用工具。完整紀錄留於本機 review/docs-videos-multilingual-20261015.log。

### 本機多語候選交付包

- 已產生繁中 111、英文 130、日文 148、韓文 140 條字幕；三個外語均使用各自 dub 時間軸。英語原有三條每秒 20.4–22.1 字的閱讀速度問題，獨立覆核後僅延長末尾至同鏡現有停頓：cue30 +243ms、cue71 +100ms、cue127 +110ms。文字與開始時間未改；四語實際 SRT 重新 parse/checkCues 均零問題。原始 manifest/SRT/VTT 保存在 review/captions-before-en-timing-20261015，調整收據在 review/captions-en-timing-20261015.json；不得把原產生器結果描述成原本通過。再跑 captions 會覆蓋此調時，須重新驗收。
- package 4／4 PASS：四語字幕及標題說明、三條 current 配音，每條 683.100 秒、AAC 48kHz 雙聲道；metadata.json SHA-256 132a7512ea926c2075f686648caf39625e87777df1a1f0e6e2558782086f8904。獨立核對成片、預設縮圖、四份 SRT 與三條配音的來源及 upload 雜湊全部吻合。此為本機結構驗收；韓語試聽及英語完整 QA 仍待完成，尚未送 publish/languages 審核、尚未上傳 YouTube。
- 使用已核准的共用縮圖。三語縮圖文字其實完整；frames manifest 早於翻譯，語系縮圖未渲染，故 package 顯示的「沒有縮圖文字」為舊診斷。選定的 metadata/captions/dub 交付範圍允許沿用預設縮圖。字幕 freshness 與縮圖舊診斷分別已開未認領追蹤票，未在本集製作中改共用工具。
