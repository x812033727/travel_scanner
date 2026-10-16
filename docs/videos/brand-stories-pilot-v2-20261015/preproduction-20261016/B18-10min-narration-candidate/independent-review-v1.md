# B18 縮稿候選：獨立事實與敘事審查

- 審查日：2026-10-16；主審：`codex-story-cc-review`。未參與 B18 原稿或候選撰寫。`b18_primary_dates` 另獨立核茶裝置與市場數字，主審亦開啟來源。
- 範圍：#1510 的 `preproduction-20261016/B18-10min-narration-candidate/`；完整讀 frozen 稿、來源包、兩份既有 review，再讀候選全文與實際差異。
- **總結：HOLD，兩處最小修正後可重審文字。** 22 段 PASS、O01 HOLD、T01 FAIL（限排他措辭）。兩個問題均由原稿繼承，並非縮稿新造的史實。沒有理由因此重寫整集。
- 本文的 PASS 只指本次離線編輯審查項目，**不是正式 worker、敘事 panel、腳本收據、製作或發布 PASS**。未操作主機，未呼叫模型／API，未產媒體或改 repository。

## 綁定與實際差異

| 檔案 | SHA-256 |
| --- | --- |
| frozen `scripts/B18.md` | `5326bd6633ad69931fe542badd6cddd2378324ff0bcc4b0f05652941642dc724` |
| candidate.md | `2ee334cf722ee13f113e8ed5c314fa99140438a5bdc3c2da1540090ddefcc35c` |
| paragraphs.json | `28d870c486407ca064f6ee2173d5564cb469e43c076f9e2dfd18a904c860607e` |
| hash-manifest.json | `ee7e93df70bced1262ac4722912e0a799a5333f7a96e5795044e5f46ad9b9c43` |

以 frozen 的 24 段 `>` 旁白逐項比較：只改 O02、O03、I04、E03、E05、T01、T01a、T03；其餘 16 段逐字相同，包含 H01–H03、N03。獨立重算同一計數方式得到 2729→2293 units，減少 436。8 個受讀 source 檔前後 hash 未變；證據與完整 before/after 留於 `B18-10MIN-INDEPENDENT-REVIEW-EVIDENCE.json`。

## 來源與證據界線

- [S0：J-Net21 元祿產業訪談報導，2023-11-13](https://j-net21.smrj.go.jp/special/expo1970/20231113.html)。本次實讀「ビール工場」「町工場」「モノレール」「市場規模」等正文。博志說法是參與者／家屬回憶，其他沿革與市場數字是報導整理，不能把整頁每一項都稱為原始檔案。
- [S1：日本機械學會，第112號機械遺產](https://www.jsme.or.jp/kikaiisan/heritage_112_jp.html)。認定機構的一手記錄。
- [S2：發明協會，迴轉壽司沿革](https://koueki.jiii.or.jp/innovation100/innovation_detail.php?eid=00026&age=high-growth&page=keii)。權威機構的研究沿革，並非本次直接取得的實用新案原卷。
- [S3：石野集團官方沿革](https://www.ishino-group.com/group/)、[S4：石野／北日本カコー年表](https://www.ishino-group.com/history/)。企業一手自述，可補核設備年代；S2 引用了該企業的舊資料，不能冒稱互不相依的雙重證明。

本次沒有取得富士經濟付費原始數據表，N02 仍只能說「2023 年報導引用富士調查」；沒有把 S0 的店數另歸給富士。未使用維基補成唯一事實依據。

## 必要修正（只限兩處）

### O01 — HOLD：相對年份沒有穩定的聽覺錨點

H01 雖是 1948，H02 已依次說到 1958、1970、1978，再隔 H03 與片頭動畫；正文「白石在前一年」容易被接到剛聽過的年份。史實本身有據，只需明示原有年份。

- 將開頭 `白石在前一年，` 換成 **`一九四七年，白石`**，其餘原文不動。
- 依據：[S0「ビール工場」首段](https://j-net21.smrj.go.jp/special/expo1970/20231113.html)。不是新增年代或改掉冷開結構。

### T01 — FAIL：排他措辭與同稿及來源不合

`原本得走進大阪小店才看得到的輸送帶，被更多人看見。` 把「增加曝光」說成「此前只有親自進大阪店才看得到」。同稿 E02 已說店外看得到，S2 在萬博段之前也已記錄東日本加盟擴展。這個限制不是縮稿所需。

- 整句換為 **`這種原先在小店裡運轉的輸送帶，讓更多地方的人看見。`**
- 保留 T01 的表彰、來源歸屬、外國訪客、約240家及茶的引句。
- 依據：[S2 的加盟段→萬博段](https://koueki.jiii.or.jp/innovation100/innovation_detail.php?eid=00026&age=high-growth&page=keii)，以及 [S0 的店外可見敘述](https://j-net21.smrj.go.jp/special/expo1970/20231113.html)。不需要新增「萬博前已到多少店」等未給數字。

## 逐段結論

| ID | 結論 | 本次判讀及來源 |
| --- | --- | --- |
| H01 | PASS | 場景與瓶頸有據；未指定啤酒品牌，問句不是假引語。[S0](https://j-net21.smrj.go.jp/special/expo1970/20231113.html) |
| H02 | PASS | 三個前瞻問題留住答案，年份順序一致；見下方回收表。[S0](https://j-net21.smrj.go.jp/special/expo1970/20231113.html)、[S2](https://koueki.jiii.or.jp/innovation100/innovation_detail.php?eid=00026&age=high-growth&page=keii) |
| H03 | PASS | 是全片設問，沒有新增歷史引語；與後續送盤主線相容。[S0](https://j-net21.smrj.go.jp/special/expo1970/20231113.html) |
| O01 | HOLD | 事實可保留，只修明示年份，理由見上。[S0](https://j-net21.smrj.go.jp/special/expo1970/20231113.html) |
| O02 | PASS | 精簡不改價格／明示機制；「每多一客」屬口語說明，不應製成精確工時計算。[S0](https://j-net21.smrj.go.jp/special/expo1970/20231113.html) |
| O03 | PASS | 製作超量與遞盤瓶頸沒有混成機器會握壽司。注意「年輕師傅離職」根據 S0，S2 只支持訂單超量；製作註保留雙來源。[S0](https://j-net21.smrj.go.jp/special/expo1970/20231113.html)、[S2](https://koueki.jiii.or.jp/innovation100/innovation_detail.php?eid=00026&age=high-growth&page=keii) |
| O04 | PASS | 回呼瓶子並提出轉角問題，新增可理解的吧台限制。[S0](https://j-net21.smrj.go.jp/special/expo1970/20231113.html) |
| I01 | PASS | 接 O04 的實際失效，沒有虛構精確事故。[S0](https://j-net21.smrj.go.jp/special/expo1970/20231113.html) |
| I02 | PASS | 撲克牌／名片兩種說法仍分別歸屬，未合成同一目擊。[S0](https://j-net21.smrj.go.jp/special/expo1970/20231113.html)、[S2](https://koueki.jiii.or.jp/innovation100/innovation_detail.php?eid=00026&age=high-growth&page=keii) |
| I03 | PASS | 說明可確認的板片功能，沒有裁定唯一靈感版本。[S1](https://www.jsme.or.jp/kikaiisan/heritage_112_jp.html)、[S2](https://koueki.jiii.or.jp/innovation100/innovation_detail.php?eid=00026&age=high-growth&page=keii) |
| I04 | PASS | 1957試作與約十年相容；預付費的回憶及動機推測仍有主詞與「或許」。[S0](https://j-net21.smrj.go.jp/special/expo1970/20231113.html) |
| E01 | PASS | 1958年4月首店與場景規模有據，沒有宣稱零人力。[S1](https://www.jsme.or.jp/kikaiisan/heritage_112_jp.html)、[S2](https://koueki.jiii.or.jp/innovation100/innovation_detail.php?eid=00026&age=high-growth&page=keii) |
| E02 | PASS | 50日圓與 O01 的20日圓分期清楚。[S2](https://koueki.jiii.or.jp/innovation100/innovation_detail.php?eid=00026&age=high-growth&page=keii) |
| E03 | PASS | 新明寫1962與原「兩年後」等義；採 S2 的實用新案分類，未沿 S0 的籠統特許稱法。[S2](https://koueki.jiii.or.jp/innovation100/innovation_detail.php?eid=00026&age=high-growth&page=keii) |
| E04 | PASS | 權利保護與社會曝光分開，沒有保證所有店都受禁。[S0](https://j-net21.smrj.go.jp/special/expo1970/20231113.html) |
| E05 | PASS | 300日圓仍明確是萬博套組；博志回憶未被剪成客觀工時數據。[S0](https://j-net21.smrj.go.jp/special/expo1970/20231113.html) |
| T01 | FAIL | 只退回排他性那一句；240為 S2 口徑，不是全部都是加盟店，也未給未證年份。[S2](https://koueki.jiii.or.jp/innovation100/innovation_detail.php?eid=00026&age=high-growth&page=keii) |
| T01a | PASS | 1971提供元祿依 S2；1974整合另有公司沿革支持。沒有泛稱每店安裝。[S2](https://koueki.jiii.or.jp/innovation100/innovation_detail.php?eid=00026&age=high-growth&page=keii)、[S3](https://www.ishino-group.com/group/)、[S4](https://www.ishino-group.com/history/) |
| T02 | PASS | 1978期限與後續進場者相接；未說此前沒有其他壽司店。[S0](https://j-net21.smrj.go.jp/special/expo1970/20231113.html)、[S2](https://koueki.jiii.or.jp/innovation100/innovation_detail.php?eid=00026&age=high-growth&page=keii) |
| T03 | PASS | 「有些店」保住適用範圍，並阻止把期滿當成全國普及唯一原因。[S2](https://koueki.jiii.or.jp/innovation100/innovation_detail.php?eid=00026&age=high-growth&page=keii) |
| T04 | PASS | 是競爭後的不同例子，未合成同一店同一年。略有總結句，列可選節奏建議。[S2](https://koueki.jiii.or.jp/innovation100/innovation_detail.php?eid=00026&age=high-growth&page=keii) |
| N01 | PASS | 保住1985機器／2021認定／早期板片之區別，沒有冒稱1958原機。[S1](https://www.jsme.or.jp/kikaiisan/heritage_112_jp.html) |
| N02 | PASS | 2022實績／2023當時預估界線保留；本次核到的是報導引用，非富士原表。[S0](https://j-net21.smrj.go.jp/special/expo1970/20231113.html) |
| N03 | PASS | 4000多店只歸於2023報導；三句收束不追加單一因果。[S0](https://j-net21.smrj.go.jp/special/expo1970/20231113.html) |

## 三問回收與整體可聽性

| 開場問題 | 實際答案位置 | 判讀 |
| --- | --- | --- |
| H02：轉角怎麼走通，能否開首店 | I01失效→I02–I03板片→I04試作→E01開店 | PASS；解法、試作和營業結果是不同進展。 |
| H02：萬博的人怎麼看 | E05客流與出餐→T01表彰、訪客及知名度 | PASS；沒有虛構訪客對白。T01排他句須先修。 |
| H02：到期後誰進場 | T02新業者與加盟獨立→T03–T04店型及競爭 | PASS；不是只回答「到期了」，也沒有把到期寫成唯一原因。 |

章節線條可讀：缺人→送盤機制→轉角解法→開店及保護→曝光與競爭→留下的記錄。給茶僅88 units，仍是送餐設備延伸，沒有變成另一家公司傳記。I02–I03 的來源分歧會短暫放慢，但正好回收轉角，且有必要避免把傳說演成確定事件；不要求為求快剪掉歸屬。

可選節奏處理（**不是必要 gate**）：T04「從白石一人……這條路已經換了好多種走法」重述剛講過的採購／價格／大店；若實際讀稿嫌長，可只刪該總結句，保留末句接字典的懸念。O04→I01 距離短，不必再加「還記得」，現稿已能承接。不要為每個歷史節點另加回顧句。

字數估時重算與 manifest 相符：正文約550.32–598.17秒；加既有5秒片頭與21秒片尾約576.32–624.17秒。開場約45.12–49.04秒。這些只是在230–250 units/min假設下的估算；沒有可據以承諾最終片長、每鏡≤12秒或TTS語速的實錄。無需加空話湊滿10分鐘。

## 下一步界線

兩處修正可由作者在隔離候選另版完成，重算 hash 後只需核 exact delta 及連續讀法；本報告不自動批准未見的新 bytes。若要轉正式章稿，需重新對齊來源／claims、鏡頭及真正 worker 關卡。Frozen 原稿、既有 review、正式狀態維持原樣；本次沒有改它們。
