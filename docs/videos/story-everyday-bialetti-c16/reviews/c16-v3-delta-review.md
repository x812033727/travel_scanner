# C16 Bialetti｜09e24dc 作者修訂的獨立差異覆核

日期：2026-10-23。審查者 `codex-c16-v3-delta-review`；只讀作者工作樹，沒有改動作者稿。對象是草稿 [PR #1704](https://github.com/x812033727/travel_scanner/pull/1704) 的精確 head `09e24dc11b9d0e3549a7c31f80d33db79d56ec82`。先前 [PR #1720](https://github.com/x812033727/travel_scanner/pull/1720) 的 81/81 來源與配鏡 PASS 只適用於舊 head `b98f47e3d391b1e5b8d8b44f593c96ab9c57fdc5`，不能轉移到以下新 bytes。

## 精確輸入與改動範圍

從 `git show 09e24dc:<path>` 的原始 Git blob bytes 以 Python `hashlib.sha256` 重算：

| 作者檔案（同在 `docs/videos/story-everyday-bialetti-c16/`） | bytes | SHA-256 |
| --- | ---: | --- |
| `script.md` | 13,896 | `91E711AEA2DB75D7C01D05B608C4D936FD99BFCED3ADDF6CD38D20FE60FEA068` |
| `script-source-notes.md` | 8,515 | `AA29858F39F2B639E97A0D10D51005FB9FA156FB30AD74AE730069F726D6500A` |
| `visual-plan.md` | 15,043 | `8C49EB8099583C261CDC30290F00AC61FD1DBFF219CA2F8175944760F5B41299` |
| `visual-plan.json` | 21,290 | `8BEAD3AD93C03B3A481D3B7D1CD2A091E0D763200206EC992A7274B58C1260AE` |

`git diff b98f47e 09e24dc` 顯示稿件四檔、作者收據和作者任務註記共六個檔案變動。逐 ID 比對：`script.md`、視覺 Markdown 與 JSON **都只改 `c160212`、`c160417`、`c160601`**；沒有增減 ID，也沒有改其他 78 句／78 鏡。來源註記同步調整這三段的解說、M11 使用位置、鉤子回收表及紙上字數；另兩檔只更新作者收據和任務進度。

從新 head 原始 blob 解析結果：81 個唯一旁白 ID、81 個 Markdown 鏡頭 ID、81 個 JSON 鏡頭 ID 同序；Markdown 與 JSON 的 ID／kind／鏡頭或字卡文案逐欄 **81/81 相同**。視覺組成仍是 72 `shot`、9 `stats`，最長連續字卡 2 張，`look` 是 `cute-mystery`。這是文字方案校驗，不是生成影像或實測時長。

## 三處獨立判定

| ID 與跨章承接 | 來源、旁白、畫面判定 |
| --- | --- |
| `c160212 → c160301` | **PASS。** 改問「後來被記成哪一年的設計」，下一章立即用「公司與博物館後來…標在一九三三年」回答。公司 [2007 公開說明書印刷頁 68](https://www.borsaitaliana.it/prospetti-informativi/926pros_1_it.pdf)及 [Museo Omero 物件頁](https://museoomero.it/en/opere/moka/)都提供回顧式 1933 標示。問答不再追問未有來源的「八角輪廓怎麼留下」，也不把 1933 畫成當年原始專利。`c160212` 的空白設計卡接 `c160301` 的有歸屬後製年份卡，畫面與語音相符。 |
| `c160417 → c160501` | **PASS。** 前句只從「可煮」轉向「帶到使用者面前」，`c160418` 再問誰承接；`c160501` 回答雷納托，`c160502` 才首次說早期產量少，沒有重複前一章的產量說法。[Museo Omero 的 Alfonso Bialetti 人物頁](https://museoomero.it/opere/autori/alfonso-bialetti/)記載早期量少、雷納托戰後擴產與宣傳；[Bialetti 公司年表](https://bialettiafrica.com/pages/our-history)及[公開說明書印刷頁 68](https://www.borsaitaliana.it/prospetti-informativi/926pros_1_it.pdf)支持戰後宣傳方向。`c160417` 的匿名概念人物搬壺去無字展示桌是敘事轉場，沒有畫具名交付、確切銷量或已知買家。 |
| `c160519 → c160601` | **HOLD：承接成立，來源界線仍含混。** `c160519` 問壺為何留在爐邊；新 `c160601` 用旋開、重新裝水放粉與可重複使用直接作答，[Museo Omero 物件頁](https://museoomero.it/en/opere/moka/)也支持可分合構造。然而旁白直述「隔天早晨，爐邊的人**又把同一只壺旋開**…」，在歷史敘事中容易聽成某戶被記錄的隔日行為；來源只描述壺的構造和使用方式，沒有這戶、這一天或連續兩次使用的原始記錄。來源註記及圖像 prompt 雖標「概念清晨」，觀眾只聽旁白仍無此界線。`c160601` 圖像本身標成「第二個概念清晨」、匿名人物與原創壺，未冒充檔案影像，可保留；但它和直述旁白組成的對鏡仍須待旁白修正。 |

可窄修 `c160601` 為條件式或明示想像，例如「隔天早晨若想再煮一杯，同一只壺仍能旋開，重新裝水、放粉」；保留爐邊的故事回收，也不宣稱某戶確曾如此操作。修後須以新四份 Git blob 雜湊重核同 ID 旁白、來源註記和配鏡，不能沿用本收據。

## 裁決與限制

本輪三處差異為 **2 PASS、1 HOLD**；承接與機械配對通過，但新 head 的逐句來源／配鏡整套仍是 **HOLD**。按舊版 PR #1720 對完全未變的 78 句／鏡之 PASS 加本輪差異裁決，現有 **80/81 旁白來源 PASS、81/81 視覺文案自身 PASS，`c160601` 對鏡整體 HOLD**。這不是兩位全新旁白盲讀，也不是站主稿件、真實 TTS 時長、插圖時間占比或付費製作核准。

本輪直接重開了公司公開說明書、Museo Omero〈Moka〉、公司歷史年表及 Fondazione Fiera Milano 在 [Google Arts & Culture 發布的 1957 雜誌廣告館藏記錄](https://artsandculture.google.com/asset/pubblicit%C3%A0-moka-express-bialetti/MgG9-eGz81X0-Q?hl=en)。Museo Omero 人物頁、義大利文化部人物頁的直接載入逾時，但官方頁搜尋索引有相關段落；本輪沒有把搜尋索引當成特定家庭行為的證據。M16 角色身分及 M17 發明／權屬／訴訟仍維持原 HOLD 界線。沒有修改作者檔案、產生付費媒體、合併、匯入、上傳或發布。

審查任務 `done` 前的 `npm run check:tasks` exit 0（2,082 個任務檔，既有警告）；81/81 配對 Python 斷言通過。`npm run tasks -- done` 寫成 `tasks/done` 後未能移除本工作樹新建的 `tasks/open` 原檔；一次針對該**精確路徑**的 `Remove-Item` 被執行政策以 `blocked by policy` 拒絕，因此不再用其他方式刪除。提交只納入 `tasks/done` 版本及本收據；本機未追蹤的 open 副本使 done 後的本地任務檢查不可代表提交樹。
