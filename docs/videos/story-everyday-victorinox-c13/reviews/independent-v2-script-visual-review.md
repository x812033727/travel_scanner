# C13 Victorinox v2｜獨立逐句／逐鏡差異覆核

2026-10-23（Asia/Taipei）｜審查者 `codex-c13-independent-v2`｜草稿 [PR #1693](https://github.com/x812033727/travel_scanner/pull/1693)｜**整份稿件交站主前 HOLD**。這是對舊版 [獨立 HOLD](independent-script-visual-review.md) 後的作者修訂作差異覆核，並重看全稿的敘事接力；不是只讀旁白的盲評、成圖驗收或製作核准。

| 審查輸入 | SHA-256 |
| --- | --- |
| PR 作者輸入 head | `f38c5b3655b8c313fb523cde340e796473af2033` |
| `treatment.md` | `A4A47F06F52490B4044267405445F31AC31EF7FB2C19575D59511D5BE0C57F20` |
| `source-matrix.md` | `295A7793DE618FEF714FA530F78592527EF77E82BAA38EE5594745B8386641D1` |
| `script.md` | `FC538ED72ED024CF3F832D9CD1232C674C9C26F31039E06A3C762EADDEB25E10` |
| `script-source-notes.md` | `DE87D4F65F50B608C977A1B25A3321FA7D2C9CE8861CC78AD8987492DB5CF043` |
| `visual-plan.md` | `E6AEEDE4D4CC5573E9C6C6C74684378BC10E84FAD7F387960C3AFB0D6112A303` |
| `visual-plan.json` | `9BFE558EFCCFD7C37357A00973EE9D42007897990E861CEE65C510F73D84DA86` |

## 舊版 HOLD 的差異結果

- **T02–T03 來源 PASS。** 新稿不再聲稱兩次訪談的人數差異，而是把部分員工借調、約四至八個月、避免裁員明確歸屬於 Elsener 多年後的本人回憶。[S6 訪談](https://www.swissmadebusiness.com/brands/victorinox)確有這些內容。這不能當成同期員工名冊或獲利額的證明。
- **E03／T03 字卡內部標記已移除，但 E03 另有來源越界。** [S5 2002-01-29 報導](https://www.swissinfo.ch/eng/archive-banking-fintech/sales-blunted-at-victorinox/2511740)只說瑞士軍刀 *sales* 在 2001 年第四季跌近三分之一，沒有交代是件數還是金額；E03 卡寫「刀具**銷量**近減三分之一」把口徑限定為件數，應改為「瑞士刀**銷售**近降三分之一」等不限定單位的說法。T03 卡「CEO 多年後回憶｜曾短期借調員工」與修稿相符。
- **61 個插圖 prompt 的畫風字串修正 PASS。** 每一個 prompt 已拿掉 `cute-mystery`；`visual-plan.json` 的 `look` 仍只有 `{"preset":"cute-mystery"}`。逐鏡文字保留概念示意、不畫商標及可讀字的界線；生成後仍要逐張驗收。

## 本輪新 HOLD

- **N11 字卡時間不準。** 卡寫「限制發生於 **2001 後**」，一般讀法是 2001 年之後，但 [S5 當期報導](https://www.swissinfo.ch/eng/archive-banking-fintech/sales-blunted-at-victorinox/2511740)把機場禁售、手提攜刀限制和 2001 年最後三個月的下滑放在一起；旁白 H02 也說「二〇〇一年九月後」。改為「**2001 年九月後**」等清楚年份，不能把事件推到 2002 年。
- **故事仍像在口播查核工作。** `H06` 宣告要分三本帳；`O05–O06` 講哪個紀錄不能證明什麼；`T04` 說「因此我們只說」而畫面讓編輯抹掉人數；`N02`／`N06` 再講來源沒有因果。這些界線應留在編輯筆記、用發生的事或有歸屬的當事人說法接力。尤其 `T04` 直接把編輯取捨說給觀眾，與 `brand-story` 的「查核過程不進旁白」相牴觸。`E04–E11` 分來源期間有必要，但連續多句帳本解說後，應由真正的公司應對行動接手，不要再增加查核口吻。
- **主要反轉重播。** `H03` 已說 1989 年北美有手錶，`O11` 再完整報一次，`N11` 又把同一日期當片尾「最意外」答案；`H04`、`O12`、`N04` 也反覆報 1999 年授權旅行用品。對照 `script-writing.md` 的「一個事實只講一次」與開場先掛問題、後面才揭曉的要求，這版至少要決定哪一處第一次給年份，再讓後文用真正的新行動推進。此為文字編輯覆核，不冒充兩位只讀旁白的盲讀判定。

## 支持的邊界與機械結果

我重開了 [Victorinox 年表](https://www.victorinox.com/en-CA/All-about-Victorinox/History/cms/history/)的 1989／1999／2005／2014／2017 節點、[SABI 2001-07-30 8-K](https://www.sec.gov/Archives/edgar/data/731947/000073194701500009/sabeightk.htm)、[SABI 2001 10-K](https://www.sec.gov/Archives/edgar/data/731947/000073194702000003/tenq.htm)的 11 月營運節點、[SABI 2002 Q2 10-Q](https://www.sec.gov/Archives/edgar/data/731947/000073194702000016/tenq2.htm)的 −34%／+7%／+16% 產品銷售比較，以及 [S10 2002-01-25 經理訪談](https://www.swissinfo.ch/spa/archivo-finanzas/caen-ventas-de-navajas-suizas/2505136)的十月口徑。作者修訂的其他 73 句與舊審輸入相比未改；其來源界線沿用舊版逐句審查，**沒有把舊 HOLD 直接升格成現版 PASS**。十月、第四季、美國 SABI 全年與瑞士公司不可混成同一分母；CEO 事後解釋也不可當量化救援證明。

獨立解析本版 JSON：**75 句／75 鏡**，ID 同序；61 張插圖／14 張卡，預排正文 **599 秒**、插圖 **490 秒（81.8%）**、最長連卡 **2**、最長單鏡 **12 秒**。這些全是**稿面編排**，並未實測 TTS 正文至少 480 秒、實際鉤子間隔或成片插圖畫面占比。冷開場後 5 秒片頭、正文後 21 秒 v4 片尾與連結位均有註明。

**下一步**：作者只修 E03／N11 卡與上述旁白敘事問題，保持所有時間窗、公司、商品狀態及回憶歸屬；再由獨立者按新 SHA 重核，交兩位只讀新版旁白的讀者盲評。站主只採用企劃，尚未核准本劇本／分鏡或整支費用。沒有 TTS、圖片、配樂等付費生成，沒有匯入、上傳、合併或發布。
