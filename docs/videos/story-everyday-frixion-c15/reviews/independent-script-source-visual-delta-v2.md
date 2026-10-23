# C15 FriXion｜盲讀後作者修訂的獨立來源與配鏡差異覆核

**判定：PASS（來源主張與預製作逐鏡文字）；無本輪 HOLD。** 審查者 `codex-c15-independent-delta`，日期 2026-10-23。此收據對應[作者草稿 PR #1701](https://github.com/x812033727/travel_scanner/pull/1701) head `31e43913902cc397a4bd3e6924a01b692f63f83f`，從前一輪來源／配鏡 PASS 所綁的 `665738706d90f7bddae20d1874cfb24dd878fe1d` 做差異覆核。兩個 head 的五檔 diff 是 `script.md`、`script-source-notes.md`、`visual-plan.md`、`visual-plan.json`、`reviews/author-script-receipt.md`；除此五檔外沒有其他差異。本審查在新獨立工作樹 `codex/brand-story-frixion-c15-delta-review-v2` 讀取，未改作者內容。

| PR #1701 新 head 的實際 checkout 檔案 | SHA-256 |
| --- | --- |
| [`script.md`](../script.md) | `7B048F142FE360999CEE86B99FA80ACFD4F8703AC0582E1F4B27E8A514E67126` |
| [`script-source-notes.md`](../script-source-notes.md) | `262C40FEF9909C0684242DBEB005A1CB9B627ED14C0F1D66EF80ABDE19CF76D6` |
| [`visual-plan.md`](../visual-plan.md) | `8547133B168FD34B327882CD199E20AF27C410B21CC4742C182213AF99A23D7D` |
| [`visual-plan.json`](../visual-plan.json) | `F9B5FB39A70E9FD0BAEE74717F18327E01C9E704087896D83A800EFEC8AF0440` |

四檔 `git ls-files --eol` 均為 `i/lf w/lf`；`Get-FileHash -Algorithm SHA256` 與作者收據所記 Git 內容雜湊一致。前輪 [PR #1705](https://github.com/x812033727/travel_scanner/pull/1705) 的 v2 PASS 只綁舊 head 四個 SHA，不沿用作為新稿審查結果。PR #1701 在本次讀回時仍為 OPEN、draft，head 為上表指定提交，帶 `no-auto-merge`。

## 來源差異判定

重開 PILOT 的 [2024 開發故事 Part 1](https://www.pilot.co.jp/media_english/005/)、[Part 2](https://www.pilot.co.jp/media_english/006/index.html)、[現行商品 FAQ](https://www.pilot.co.jp/support/frixion/frixion_1.html)、[高溫消色與低溫回色 FAQ](https://www.pilot.co.jp/support/frixion/1334578774507.html) 及 [2017 十週年新聞稿](https://www.pilot.co.jp/press_release/2017/01/18/1010.html)，逐一核對以下 **34 個改過的旁白 ID**，並以先前已核的未改 53 句為基線。2024 故事是 PILOT 事後回顧；稿件有歸屬，不能當作獨立現場紀錄。

| 改動 ID | 原件定位與結論 |
| --- | --- |
| H01、H04–H08；O01–O04、O10 | Part 1 的 `1970–1974`、`1975–1985`、`2001–2002` 段支持秋葉靈感、1976 變色**紙杯**、2001 微膠囊 2–3 μm、2002 ILLUSION。Part 2 的 `2002–2006` 段支持歐洲行銷提問及 2004 商品化決定。新版開場四個時刻只提出後續問題，未說當年杯與可擦筆同配方，也未把 ILLUSION 說成已能消字。O03 的「當時沒想到書寫工具」亦見 Part 1 的 `1975–1985` 段。**PASS**。 |
| I10；E05 | Part 1 的 `1993–2000` 段明說膠囊變小使膜變薄、易破及耐用膜的挑戰；Part 2 的 `2002–2006` 段明說改錯後另需特殊筆重寫。新版轉成問句與障礙，未擴大到全歐同一書寫法規。**PASS**。 |
| E13–E15；T01–T03 | Part 2 的 `2002–2006` 段明說 2004 年實驗室小量可做，但產線大量同品質極難，研究者反覆往返實驗室與工廠；其後 2006 歐洲上市，同一支筆能寫、消、再寫。E15 只承諾「何年買得到」，T01 以 2006 上市回收，沒有聲稱知道未記錄的具體量產解法。T02–T03 說使用結果，未先解釋微膠囊消色機制。**PASS**。 |
| T05–T09；N01–N05 | Part 2 的 `2006–2024` 段支持日本朝商務使用者推廣、2007 年 3 月上市、初期 0.7 mm、約半年後 0.5 mm、日文密集筆畫與較大墨水粒子通過細筆尖的難題。三日試賣 3,000 支及「約計畫三倍」已退出旁白及字卡。該段並明說按壓式暴露筆尖易乾、較大粒子與筆珠間隙、反覆實驗精修**筆尖內部結構**、2010 推出；N03 的新增細節因此有直接依據，未杜撰密封件或工法。N05 的微膠囊摩擦轉無色由現行 FAQ 支持。**PASS**。 |
| N07–N08、N10、N13、N20 | 現行 FAQ 將消色設定寫作 60°C、約 -10°C 起可能回色；另一 FAQ 解釋約 -20°C 可較完整但不保證，摩擦過的痕跡不保證完整恢復。2017 新聞稿把摩擦消色寫作約 65°C。新版明確把 60 與 65 歸屬不同文件，沒有混成一個跨年代精確規格；冷熱使用提醒與訂閱收尾沒有新增不可核史實。**PASS**。 |

## 逐句配鏡與結構

`script.md`、`visual-plan.md`、`visual-plan.json` 各有 **87 個唯一 ID、同序**；JSON 的 87 段 `narration`／`source_tags` 與劇本逐字相同，每列的 `kind`、提示詞或後製字卡、`visual_guardrail` 亦與分鏡 Markdown 逐字相同。新版是 **72 個 `shot`、15 個 `card`**，72 條 shot 提示詞均不重複；最長連續字卡 2。全部 shot 的 `model` 為 `MiniMax image-01`、`look` 只有 `{"preset":"cute-mystery"}`，沒有 `style`／`negative`。圖片提示詞未含 PILOT、FriXion、ILLUSION、Magic Cup、商標、logo 或要求可讀文字；卡片只在 `postproduction_text` 承載文字，沒有圖片模型提示詞。

本輪 **23 個改過的逐鏡文字 ID**：H01、H04–H06、H08、O01、O04、O06、O11–O12、I02、I13、E15、T03、T05–T08、N01、N16–N18、N20。H04 是無字紙杯與水壺，尚未畫出變色結果；H05 未畫微膠囊已穿過筆尖；H06 未畫透明結果；H08 及後段所有杯子回呼均明寫紙杯，與 Part 1 一致。E15 的空貨架只是上市時間疑問，未把 2004 畫成已備貨；T03 的修正工具被放下，配合單筆完成修正；T07–T08 的筆畫與膠囊是無字、無精確比例的概念畫；N01 不假造工程測試。15 張字卡再核一次年份、溫域及 0.5 mm 的文字，舊 T07「3,000 支／三倍」卡已消失。上述畫面未對旁白新增相矛盾的具體史實。**配鏡 PASS**；實際生成圖仍須另行驗收。非阻斷文字差異：`visual-plan.md` 頁首寫「連續字卡最多一張」，但 E08–E09、N07–N08 各為兩連卡；作者收據及 JSON 的兩連卡記法正確，仍低於 Curio 規則的三連卡上限，後續可把頁首改成「最多兩張」以免誤導。

JSON 的紙上 `paper_seconds_at_250_cjk_per_minute` 合計 **564.96 秒**，其中 shot 句占 **81.18%**；這只是文字代理值，不能當成實際 TTS 正文 ≥480 秒、實際每 45 秒鉤子或剪後插圖 ≥70% 的驗收結果。本收據不是兩位只讀旁白的敘事盲評，也不是站主劇本核准、付費圖片／聲音預算核准、成片、上傳或發布。舊 [PR #1707](https://github.com/x812033727/travel_scanner/pull/1707)／[#1709](https://github.com/x812033727/travel_scanner/pull/1709) 的 HOLD 固定舊劇本 SHA-256 `81CB336C…631672A4`；兩位讀者須在本輪劇本 SHA-256 `7B048F14…4E67126` 各自重讀。若作者再改任何內容檔，依新雜湊重新覆核變動。
