# H09《艾爾哈特最後飛向哪裡？》十三題敘事獨立審讀｜2026-10-15

受審正式稿：script.md SHA-256 F2890AA3BE81026F846B9F76F9BA59A1C8B69FEBF7D3D7A7BFB8C0EF6DECC0A1；本機 narrative 判定綁定 narrative_hash 1617913c723b78bd、script_hash a29a9e618b6485c254ab2e2a6446e69b30bcfc8955bb0450e7d542accd83858e；編輯底稿 script-draft.md SHA-256 CF579A778769BCE9905B2C5C477C075FF3D140D9EE7433F48373732644D4D881。下表用底稿 O01–Z03 及正式稿的場景／句 ID 定位。舊版十一題收據綁定底稿 SHA 361ECEA6E3FFDF8283F7B3C1C325E1C9B83FA122E67AACB3C637A41BDCA11F83，不能代替本次十三題判定。

方法：未參與 H09 撰稿的審讀員重新讀完整正式旁白，依 tools/video/core/narrative.mjs 現行 NARRATIVE_PANEL 的十三題逐題判斷。這只審敘事，不代替史料查核、站主劇本核准、旁白試聽、插畫或成片 QA。

**判定：十三題皆為「是」；十二題必答全過，第九題參考題亦過。** 本機 `narrative --answers` 已以 exit 0 記錄於媒體工作目錄 `review/narrative.json`（round 1，13 answers，0 failed，0 advisory）。 第六題是文字節奏判讀；新 F03、Z01 尚未重錄，舊音訊秒數不能當作新版旁白實測。

| 題／ID | 判定 | 句子證據與理由 |
| --- | --- | --- |
| 1 scene_first | **是** | O01–O04（itasca-waits／h035intd 起）把 1937-07-02 的 Itasca、7:42 燃油警訊與 8:43 電訊放在同一現場。 |
| 2 no_spoiler | **是** | O06–O08（uncertain-broadcasts／h0ac4220、search-plane-island／h07qifh3、island-telegram-tease／h1xsq9te）只問訊號、搜索機及醫師判讀；結果到 B05、B10–B14、D03 才交付。 |
| 3 one_line | **是** | O04 最後電訊→A10 艇長決策→B 段搜救→C／D 段島上骨骸→E／F 段機件候選與現場檢驗，按發生與再檢驗次序前進。E09–E12 是同一失蹤機另一候選落空，E11 明說與 Taraia 不同。 |
| 4 no_toc | **是** | O06–O08 是未揭曉事件而非章節導覽。B03「接下來十六天」指歷史時間。C03 的鞋、瓶、六分儀盒是電報內容，C07–C08 隨後檢查其辨認力，並非排後文目錄。 |
| 5 chapters_link | **是** | A01 承 O09 位置線、B01 接 A11 派人、C01 接 B 段飛越島後的發現、D01 接送驗骨頭、E01 接 D13 尋找機件、F01 接 E13 出航。Z01（unresolved-verdict／h0ctdw9q）直接給截至 10/14 仍無可確認機件的結果，承 F15 對兩處說法均不能定案的界線，已無「回到」標籤。 |
| 6 open_loops | **是，限文字判讀** | A10 把往哪端找留給 B 段；B11–B14 的正式報告與飛行員信形成反轉，B15 搜救收隊仍找不到飛機，C01 接島上骨頭；C13→D03 掛住鑑定，D11–D13→E01 轉向機件；E05（how-to-test／h00s999r）問如何由影像得到實物，E13→F01 抵達；F03（purdue-historical-link／h0op7m6k）問是否有 Electra 可辨部件，F07 資料待分析、F12–F13 仍是待驗條件。秒數界線見下。 |
| 7 payoffs | **是** | O06→B04–B05 具名回收疑似訊號，O07→B08–B14 回收飛島搜索機，O08→D01–D05 點名電報並給醫師判定；C13→D01–D03 回答檢驗。E05 的方法由 F08–F11 的探針、比對與清淤計畫回答；F03 的 Electra 部件問題在 Z01 以截至 10/14 無確認結果回答，沒有冒稱已找到或已排除。O09 去向問題也在 Z01 以未定案收束。 |
| 8 no_recap | **是** | O04 只報位置線，A06–A09 首次解釋它無法定位；B15 只說 1937 年搜救未找到，F07 只說 2026 年儀器資料待分析。Z01 首次給截至 10/14「仍沒有能確認屬於那架 Electra 的殘骸」的全案現況及未定案結論，未重播電訊或潟湖細節。F03 問是否有部件，與 E05 問取得實物的方法、F08–F11 的具體檢查不同。 |
| 9 chapters_are_events（參考） | **是** | 艇長攤線、十六天搜救、島上電報、醫師男性判定、潟湖影像與考察團抵達都是事件；最後一章〈未結〉為規則允許的現況收束。 |
| 10 outro_no_next | **是** | Z01–Z03 只有現況結論、觀眾可答的追查選擇及訂閱邀請，未提下一支影片。 |
| 11 opening_hooks | **是** | O06 疑似訊號、O07 搜索機飛島、O08 骨骸電報依正文順序留下三個具體未揭曉時刻。 |
| 12 one_thread | **是** | 主角是「追查同一架失蹤 Electra 的去向」：O01 一架飛機、A03 點名 Electra、B02 搜尋、C01／C10 驗島上可能性、D13 回到機件、E02／E13 測潟湖候選、F03／F11／F13 問並檢驗是否為該機、Z01 點名仍無確認機件。更換調查者未更換追查對象。 |
| 13 no_detour | **是** | F03 已把原普渡資助飛機的歷史巧合改成辨認機件的未答問題，F04–F13 推進現場檢驗。E09–E12 的 2024 岩石是同一架失蹤機的競爭候選及影像誤判教訓，E11 防止把其結論套給 Taraia。C03 的電報物件和 F11 的檢驗準則都服務去向問題，沒有另開題目。 |

## 時間與時效界線

現行 lint：0 錯誤、3 警告，分別是兩段估算開環空檔與 Z01 約 10.6 秒畫面停留。第六題按事件和問題人工判讀，不以啟發式警告冒充實際空窗。已核准**舊版** timeline.json SHA-256 DD46E9CC89C4BBC03C0500BA98AEB973B1D6328C6C3792CB0C56349D21BD8CF7，舊 speech_hash 31ed2734d0317ba9，音訊實長 657.233 秒。未改段落的舊時間：A10 captain-choice 124.5 秒→B12 pilot-letter 200.8 秒為 76.3 秒；B12→C01 island-work-party 250.7 秒為 49.9 秒；E13 voyage-to-lagoon 515.6 秒→F07 instruments-survey-b 571.8 秒為 56.2 秒；F07→F12 wood-would-exclude 607.5 秒為 35.7 秒。新版 F03、Z01 改變 speech_hash，**尚無新版 TTS／時間軸**；這些舊秒數只供定位，重錄後須重新量第六題。

本次讀到的[普渡大學 2026-10-14 公告](https://www.purdue.edu/newsroom/2026/Q4/earhart-expedition-update-underwater-survey-of-taraia-object-begins/)仍稱水下磁力儀與側掃聲納調查剛開始、資料待分析，負責人說尚早下結論；Z01 的截至日期另依 claims.md H09-C05／C14／C16。成片與上架前要再查官方進度；若有新鑑定，稿件與本收據都須重審。
