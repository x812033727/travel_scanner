# X19 Uber v6｜作者對 v5 雙盲 HOLD 的修稿對照

v5 [獨立 SEC 查核](script-source-audit-v5-independent.md)只對舊 SHA 判稿件事實 PASS；兩位全新[讀者 A](blind-a-v5-independent.md)與[讀者 B](blind-b-v5-independent.md)共同否決正式敘事 Q7 回收和 Q8 重複。A 另否決 Q5 章首銜接、Q13 旁支。這是作者對照，**不是** v6 的獨立查核或敘事票。

| v5 讀者提出的斷點 | v6 可核對的修訂 |
| --- | --- |
| A／B Q7：`x190505` 問 Postmates 整合能否改變虧損，後面只有部門數字，無法證明收購造成了什麼。 | `x190505` 只留下有 S5／S6 順序支持的使用者遷移動作；`x190506–509` 接上隔年實際轉入人數。`x190516` 明說整個 Delivery 部門合計帳**拆不出 Postmates 單獨盈虧**。`x190515` 新增可核算的同季部門虧損差額 US$71m（S2 −US$232m、S6 −US$161m），不把它歸因於收購。 |
| A／B Q8：`x190218` 距 `x190215` 三句又念一次「退出八個市場」。 | `x190215` 保留唯一八市場數字；`x190218` 改說餐廳進站後還須顧客下單，司機手機才有取件地址，推進供給到成交的機制。 |
| A Q5：第五章末 `x190522` 問年底外送是否轉正；第六章首 `x190601` 重問而不回答。 | `x190601` 第一個句子直接揭示 2021 Q4 Delivery 部門調整後 EBITDA 轉正，`x190602` 才給 +US$25m 與上年對照；`x190603` 另限定部門單季口徑，不冒稱公司 GAAP 淨利。 |
| A Q13：第五章虧損之後的 `x190515–516` 跳去美國雜貨／便利品與示意取件，沒有推進兩條路的帳。 | 同兩個槽改為 2020 Q2 至 2021 Q2 Delivery 部門虧損縮小 US$71m，並限定這是部門合計結果。畫面改為前後部門帳與未拆分的收購資料夾；第六章自然接「年底會轉正嗎」。 |

主片仍六章、110 句、95 張無品牌 still、12 張原生數字卡、24 條有序 loop；濃縮開場 187 字，正文紙面 2507 字，按每分鐘 300 字約 **8:21**，不冒稱成音。頻道既有 5 秒片頭仍在濃縮開場之後、21 秒片尾仍在最後三句之後。兩支各 8 拍、163／171 字的 Short 題目及旁白未改；相同 `shorts.json` SHA 仍由重建器核對 16 個主片 shot 引用。

**v6 作者凍結值：** `video.json` SHA-256 `a3149c4904182bf473a7d452c3e5a80de790402c4b240e10da4b2610e1dfbaf8`；`shorts.json` `b6b0212372d776c96572450baa8e9c4350499c72923d088ad0bd6833e8681d95`；`drafts/narration.md` `57d29905fafd83eab2352a351d671680b48ea362540777166cfb90851af898f1`；`source-matrix.md` `b8fdd00b82d6bae3a4979583f9aad5ec5f8cdd39519b5a7ec41e1e47f0ea1cd6`；`visual-plan.md` `f60cdcadb58c5f4ed75e1357aee6a176fdd52c8cc00815f187a45e1cf80b9a14`。S1–S8、S3a、S5a 的矩陣 bytes／raw SHA 是 2026-10-20 快照；v5 查核已發現 10/21 回應的唯一 SEC script tag 輪換而非正文改動。v6 新來源查核若重抓，必須分開記新 raw hash 與明示的固定-tag 比對，不能宣稱原 raw hash 未變。

作者離線驗證：主片 lint **0 errors／0 warnings**、`episodeShortsProblems=[]`、兩支 Short 各自 schema／shot hash PASS、`test:docs-videos` **236／236 PASS**、`check:tasks` exit 0（倉庫其他既有任務警告）及 `git diff --check` 通過。仍需 v6 **新 SHA** 的獨立 SEC 查核與兩位真正新首讀；正式機還須量 TTS 實質正文 ≥8:00、審核插畫和官方 5 秒／21 秒動畫、守 US$25 實際整片支出、驗 Shorts 25–55 秒及直式觀看，再產 MP4 與真實 YouTube 連結。此作者文件不代替那些驗收。
