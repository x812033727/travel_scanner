# A01 六章敘事離線候選（2026-10-18）— HOLD

這是 `story-rolling-suitcase-v2` 的本地敘事候選，從正式機唯讀 `snapshot-104` 推出。舊版 manifest `A391F721CBA58896E8E9C9ED2F20C2794C587AE61C8E07C379DBD85518585F42` 與兩份獨立 **HOLD** 意見留在 [`review-baseline-A391F721/`](review-baseline-A391F721/)；新版沒有沿用舊審稿結論作 PASS。沒有改正式章稿、收據、媒體、付費項目或凍結的 round12／R9。

## 故事順序與觀眾鉤子

| 章 | 人物的阻力、動作、結果與下一步 |
| --- | --- |
| 開場 | 第一句就有 Sadow 雙手提沉箱、重機器從旁滑過的反差；鏡頭到第三句才揭示輪板。另留下百貨採購與機師車庫兩件未解的事，畫面不先露拒絕、訂單或成品。 |
| Anita | 館方記述她出發前不想再提重箱、家計緊；兒子**先**用舊嬰兒車輪改箱，一家六口**後**出發。丈夫取笑後，她仍帶輪子箱巡講；館藏留下其中一只。沒有她影響 Sadow 的證據。 |
| Sadow | 多年後他仍在機場提兩只塞滿的箱子；回工廠給舊箱裝四腳輪與拖繩。專利提出可拖也可提的設計，隨後他帶樣品找買家。 |
| 百貨 | 採購先拒絕；Macy 副總裁親自拉樣品、叫回採購並決定進貨。Sadow 回憶顧客看懂後接受。章尾轉到**另一種**外置推車在安檢卡住的獨立問題。 |
| Plath | 他看到旅客拆卸金屬推車，把箱子鎖上推車再試，安檢員的「好」只按他本人回憶敘述。機師 Bill Emmer 另有**未標年份**的舊輪子袋與改良草圖回憶，不能剪成安檢事件的確定前因後果。Travelpro 回顧 1987 年車庫 Rollaboard；之後的專利不倒寫成該原型逐件規格。 |
| 車庫之外 | 其他機師看 Plath 使用後請他製作，後有機組使用與旅客在航站看見。Samsonite 研究主管的 **Piggyback 是另一產品線**：1987 年障礙試拉，既有大箱不適合客艙，1988 年訪空服員，1990 年手提款進店。這段短支線放在 Plath 的 1989 搬倉與 1991 全職經營結局**之前**。最後才提後來四輪款、裝太滿與樓梯前仍要提箱的限制。 |

章名只在首鏡出現，均不寫答案。`video.loops` 申報 **14 組**來源有據的障礙／動作／結果，其中開場三組是 `3rdw→idiy`、`b6mn→j9sw`、`jtmg→3zwf`。這是供審稿者核對的**提案**，不是已驗收的留存率。`source-map.json` 逐組列真正的結果與待查畫面，`validation.json` 列章接點和每段估時計算。五個章接點只有 `idea→engine` 直接在下一章首句回答；其餘是人物或阻力的延續，沒有冒稱已收束。審稿若認為某個結果被前句或畫面劇透，應將該回路剔除。

## 來源與未證邊界

- [Winnetka Historical Society](https://www.winnetkahistory.org/gazette/before-her-time-anita-willets-burnhams-rolling-suitcase/)支持 Anita 家庭改箱、丈夫反應、後續巡講與館藏；[家族簡史](https://www.winnetkahistory.org/who-were-the-burnhams/)補沿路畫畫換餐宿。1933 遊記原頁未直接查閱，口播保留館方歸屬。
- [ABC 2010 年 Sadow 訪談](https://abcnews.com/Travel/suitcase-wheels-turns-40-radical-idea-now-travel/story?id=11779469)支持兩只箱、輪板、工廠樣品、百貨拒絕及副總裁試拉。[US3653474A](https://patents.google.com/patent/US3653474A/en)只支持申請書的問題與設計主張，不等於每只售出商品的實際構造。
- [ABC／USA TODAY 2012 年 Plath 訪談](https://abcnews.com/Travel/rollaboard-luggage-celebrates-wheelie-big-birthday/story?id=17024603)提供安檢回憶；安檢員回應不是獨立的正式放行紀錄。[US4995487A](https://patents.google.com/patent/US4995487A/en)較晚描述外置推車反覆拆綁；[Travelpro 沿革](https://travelpro.com/blogs/the-travelpro-blog/the-history-of-rolling-luggage)提供公司所述 1987、1989、1991 年事件。
- [Bill Emmer 第一人稱回憶，印刷頁 46–47](https://rnpa.org/images/old-contrails/Contrails-199-Aug2016.pdf)記舊機組袋、草圖遭婉拒及第二件袋子的平衡問題，**沒有事件年份或與安檢經歷的先後**。同刊頁 48 重印另一作者 Joe Sharkey 的旅客見空服員拉箱回顧，沒有乘客詢問售點的對話。[Travelpro 當時執行長訪談](https://www.globaltravelerusa.com/reinventing-the-wheel/)供同機師請他製作的具體動作，不能拿訪談的相對年份定年。
- [Samsonite 研究主管 1992 年個案](https://www.quirks.com/articles/research-with-travelers-helps-samsonite-develop-a-convenient-new-line-of-luggage/)是公司第一人稱回顧，不是獨立銷售數據；沒有證據顯示 Piggyback、Rollaboard 與 1997 四輪款之間的技術傳承。

[`candidate/claims.md`](candidate/claims.md)只列播出的主張，均為 `PENDING`。[`source-map.json`](source-map.json)記逐句來源、舊→新 scene／claim ID、刪除理由和視覺防劇透待審點；舊 `base/verify-1.md` 的歷史確認不能搬成新版收據。

## 建置與長度缺口

在儲存庫根目錄跑 `node docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/A01-hook-cadence-candidate-20261018/build.mjs --check`。`--write` 只重建本資料夾。程式驗 `base/` 快照 SHA、原句與原 prompt；[`manifest.json`](manifest.json)綁 build、README 與輸出 SHA-256。

目前 **67 鏡／77 句／1,845 口語單位**，`lintVideo` **0 error、34 warning**，cute 視覺檢查 **0 error**。66 鏡仍指定 still；在 300 CPM 有 13 鏡靜態估時超過 8 秒。第一句的反差從 0 秒開始、前 30 秒共六鏡，開場估 35.6 秒。這些都是腳本與分鏡估計，未經真實配音、圖片與剪輯驗證。

| 靜態語速 | 六章總旁白估時 | 低於 540 秒 | 待審事件節奏最長空檔 |
| --- | ---: | ---: | ---: |
| 250 單位／分鐘 | 513.5 秒 | 26.5 秒 | 68.9 秒 |
| 275 單位／分鐘 | 473.5 秒 | 66.5 秒 | 63.4 秒 |
| 300 單位／分鐘 | 438.8 秒 | 101.2 秒 | 58.7 秒 |

正式 `story.mjs checkLength()` 對 10 分鐘 cute 規格查的是**六章 timeline 總長**（包含 hook 與 outro 旁白，不含外加片頭片尾動畫），範圍 **540–660 秒**。先前台灣華語 TTS 接近 300 CPM；此版不能宣稱符合片長。300 CPM 的事件代理另有 `r14i02→j9sw` 52.5 秒及 `r16n06→body:end` 58.7 秒的空檔；代理不會判斷真人是否仍想看，亦不把隨手加問號當作解法。沒有用慢播、空鏡、冷知識或未證史實補長。

本地 [`candidate/series.json`](candidate/series.json)同步六章新版大綱與溫暖、好奇、自然停頓的台灣華語說故事配音指示；[`candidate/lexicon.json`](candidate/lexicon.json)只提供 Bill／Emmer 的**未試聽**發音候選。`base/series.json` 保持原封不動。正式機使用六個 `story/chapters/*.json` 按 `hook→origin→idea→engine→turn→now` 組合，跨章移動須另審 scene／claim ID、章名、縮圖與 loop；`source-map.json` 的遷移表和新版 series plan 都是 **SPEC_ONLY**，合併 `video.json` 不能直接安裝。

下一關是獨立逐句事實與盲聽敘事審查，再考慮是否有足夠一手人物事件做不拖戲的延長版；之後才測實際 TTS、低成本分鏡／裁切節奏、MiniMax 插畫與可關閉繁中 CC。**沒有正式審稿收據、成片或付費製作授權；狀態維持 HOLD。**
