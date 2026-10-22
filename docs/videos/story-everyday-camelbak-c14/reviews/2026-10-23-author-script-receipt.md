# C14 CamelBak｜作者 v4 稿件收據（待獨立審查）

- 日期：2026-10-23（台北時間）；作者：`codex-c14-script`；去向：[draft PR #1695](https://github.com/x812033727/travel_scanner/pull/1695)。
- 站主採用的 [Treatment](../treatment.md) SHA-256 `078DC1D77C46EB49BB6F27F60535F22775781E5963783BDA7C1F7625B1A8700E` 與 [來源矩陣](../source-matrix.md) SHA-256 `F8CF68AA36264DF18CDBE6ECD698D4AF1F22E405DEAADA8ED275B7685050587E` 已重驗，作者未改其位元組。
- 這是作者稿，**不代表獨立來源／逐鏡、雙盲敘事、站主稿與分鏡、TTS 長度或付費核准**。

## v4 交付 SHA-256

| 作者檔案 | SHA-256 |
| --- | --- |
| [`script.md`](../script.md) | `24F35BFE6B2E65D1498580D61E22F6D852C4506159561A24E2014176E20089D4` |
| [`script-source-notes.md`](../script-source-notes.md) | `491E0A240C6A728008F221E1957A248BB84373A6D4C8D6B4D59BA8ABADE3CBC2` |
| [`visual-plan.md`](../visual-plan.md) | `0388A2DCED4DDBA08775CA49A446EA426369F0AA3DA8DF0DADCFCB4DF5795C41` |
| [`visual-plan.json`](../visual-plan.json) | `49B658C19D4FE9C944B014EF8369AF079A2479B9553C2FB9CB2DB5E665270FF9` |

## 為何重寫

v1 與 v2 的純旁白各有兩位獨立讀者 HOLD，見 [v1 協調收據](blind-narration-v1-coordinator.md) 與 [v2 協調收據](blind-narration-v2-coordinator.md)。v2 的 61 句逐句來源 PASS 綁舊版；v3 I01 字卡 [獨立 PASS](independent-v3-i01-visual-recheck.md) 也只綁舊視覺檔。這些判讀不轉簽 v4。

v4 把 Fawcett 平行專利的長旁支移出口播，改用可直接核對的連結：1998 送件、2000 公開的 CamelBak 名下口器 [US6070767A](https://patents.google.com/patent/US6070767A/en)；2005 送件、2006 十月公開且**在文件中**援引前件的水瓶 [US20060226110A1](https://patents.google.com/patent/US20060226110A1/en)；2006 二月 [GearJunkie 到場報導](https://gearjunkie.com/uncategorized/outdoor-retailer-trade-show-winter-market-2006-gear-highlights) 的 CamelBak 水瓶。專利提案不當成精確量產零件表，五月開賣只當當時預告。2003 [Stars and Stripes 寄送報導](https://www.stripes.com/news/2003-12-21/donor-manufacturer-team-up-to-send-personal-hydration-systems-to-troops-1909877.html1) 只說另一使用場合，不當首次軍用或後來水瓶的動機。2007 設計題目明示為[公司新聞稿](https://www.snewsnet.com/press-release/camelbak-better-bottle-wins-design-award)自述；2014 產品與通路以及 2012／2014 毛銷售占比均明示 [SEC 年報](https://www.sec.gov/Archives/edgar/data/1345122/000134512615000005/codi-12312014x10k.htm) 的年度、分母與歸屬。新 D01–D07 只列在來源註解，不修改站主已採用矩陣。

主線按襪中點滴袋與衣夾 → ThermoBak／山地車群體 → 1993 賽場到店面 → 1998 口器文件 → 2003 額外使用場合 → 2005／2006 瓶專利及較早展會實物 → 2006 瓶類與公司策略 → 2014 通路、商品占比往前。1988 專利背景及商標 first-use 不替品牌回憶的同一場騎乘定年；口播不猜原型比賽年份。2014 的 50%／37% 是 CamelBak **毛銷售額商品占比**，不是現況、市占或 1993 巡店的因果。六章以騎車背水、日常拿瓶的使用動作回答開場，不把公司動機寫成作者猜測。

## 本機機械檢查與停線

- 74 個唯一行 ID，行末有 S 原件標籤；JSON 74 鏡按同序對應，`look.preset` 精確為 `cute-mystery`；濃縮開場後 5 秒片頭，21 秒 v4 片尾與 Studio 連結位。
- 逐句按每分鐘 250 個口播字元估算，正文 2,459 字元／約 2,027 漢字，鏡頭時間共 **590.7 秒**，加片頭片尾 **616.7 秒**。最長單鏡 11.0 秒；標記鉤子最大估計空檔 36.0 秒。**未做 TTS，正文實際 ≥480 秒仍待實測。**
- 58 幅概念插圖／16 張後製字卡；規劃插圖 **452.8／590.7 秒＝76.7%**，最長連卡 2。圖中無商標、專利附圖、具名真人或真實軍方／賽事重建；圖片尚未生成，成片占比未驗。
- 本輪解析結構自檢 PASS；`git diff --check` exit 0；`npm run check:tasks` exit 0，驗證 2,084 張任務票，輸出其他既存長期認領／重疊範圍警告。提交前還需對暫存檔跑 `git diff --cached --check`。
- 既有 `npm run test:docs-videos` 在 v1 工作樹因缺 `pinyin-pro` 退出 1；`npm ci --no-audit --no-fund` 超過八分鐘後已停止，本輪沒有重試全量測試，不把它記為通過。

請另一代理以以上**四個 v4 SHA**重開原件逐句與逐鏡審查，另派兩位未讀本稿的純旁白讀者。若任何人 HOLD，須修訂並重綁 SHA；作者不代簽。後續仍需 TTS 實測、圖片逐張驗收、站主稿／分鏡採用與付費前報價。本輪沒有付費、匯入、上傳、合併、發布或部署。
