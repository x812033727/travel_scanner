# X13｜Spotify：買播客、重整播客，接著出現獲利轉折

狀態：**v3 前製稿 HOLD，尚不能進入付費媒體製作或開 PR。** 九件 SEC 原件可取得且雜湊吻合；獨立來源審查在 S9 日期精度、畫面與章名找到五類阻擋，兩名全新隔離讀者也都判單一決策主線不過。這是與 X01–X12 分開的新品牌故事；後續依奇聞檔案局既定的 `cute-mystery` 畫風、濃縮開場後的正式 5 秒片頭、21 秒片尾、繁中可關閉 CC，以及兩支可獨立觀看的 Shorts 製作。正式片頭、片尾和 YouTube 連結只在實際取得／產出後填入，不以概念物冒充。

主問題：一家靠音樂與會員起家的平台，2019 年在兩天內買進播客創作／發行工具和節目公司，為何 2023 年又將部分播客內容資產沖銷並重整，隔年卻迎來第一個全年營業獲利？答案不能寫成「播客讓 Spotify 賺錢」：來源只支持其播客內容組合與成本改變，會員業務與其他因素也在改善。

本階段檔案：

- `source-matrix.md`：SEC 原件網址、取得時檔案 SHA-256、可口播事實與禁止的推論。
- `treatment.md`：六章事件線、開場濃縮、節奏與畫面前提。
- `shorts-hooks.md`：兩支各自有問題、答案與來源的 Shorts 概念。
- `drafts/narration.md`：六章逐句來源標記的繁中旁白工作稿；本版正文紙本約 2,800 個口播字元，實際秒數待 TTS／錄音測量。
- `drafts/shorts.md`：兩支獨立 Shorts 逐句工作稿。
- `visual-plan.md`：匿名播客卡、兩種業務色系、來源口徑明確的後製字卡與正式片頭片尾接點。
- `reviews/`：來源與敘事審查；`review-provenance.md` 說明哪些盲評只作編修意見。

v3 審核收據：[`script-source-audit-v3-independent.md`](reviews/script-source-audit-v3-independent.md) 綁定 source matrix `cb8d31b6…`、Treatment `029f49e1…`、旁白 `44b16a99…`、Shorts `a732bb31…`、畫面 `f2471178…`，判 **HOLD**。S9 的逾十萬影片播客是 2023-07-25 公告時的「now available」，不能斷言為 Q2 末或與該季關閉節目嚴格同時；另須刪掉沒有證據的「舊內容」、2019 卡片的影片觀看路徑、關閉節目的數量／排程細節與章名的季度毛利→全年營業獲利因果。兩名只讀凍結稿的隔離讀者 [`F5`](reviews/blind-fresh-5.md)、[`F6`](reviews/blind-fresh-6.md) 都給 **6／7**，唯一 No 是章三至六主要沿年份和分類推進，尚缺一條能被來源支撐的決策主線。下一版需修正來源措詞並重構敘事，重新做來源審核和兩份隔離盲評；正式 JSON、圖像、語音、音樂與組裝均未開始，整集付費成本上限 US$25。

正式片頭片尾須在合成環境回讀**v4** 全頻道素材並逐檔核 SHA；[`brand-stories-five-20261014/PREFLIGHT.md`](../brand-stories-five-20261014/PREFLIGHT.md) 記錄的 `mokaair-brand-package-v4-endscreen` pin 是 `416c8768d4d29f2e746a0c019d2d598ec367cbb66b0ff996841c523651a63e88`，5 秒片頭 SHA `50a53efa54fe5158a166390c7f46518c052be1af005f99a5f3c57e530b0bb67d`、21 秒片尾 SHA `00eb9ccc8449fa8b47de0aab290b8aa7d55b09962c12a127e0f0c9c5f7834396`。這些是已核准素材在原工作環境的紀錄，**不是雲端已持有或已驗證素材檔**；雲端 `/tmp` 的同長度預覽檔 SHA 不符，不得冒充正式素材。片尾兩支影片卡與訂閱鈕須在 YouTube Studio 從範本影片 `oxEtlA8GWas` 匯入；[`v4 時間修正票`](../../../tasks/open/2026-10-12-correct-v4-youtube-end-screen-timing.md)查到卡位畫面在片尾第 5 秒才清楚，因此可點元素應從**影片最後 16 秒**開始。MP4 本身不能做可點連結。長片、兩支 Shorts 的實際 YouTube URL 與影片 ID 均待真正上傳後寫回，不能先填範本連結。

題材比選（2026-10-20）：100 題清單含 C01–C20、A21 品客與其他品牌，未含 Spotify 或 Airbnb；X01–X12 是 Adobe、Domino's、Netflix、Beats、Meta、WD-40、GoPro、Target、BlackBerry、eBay/PayPal、FedEx、Peloton。Spotify 與前面十二支、既有 C 題均無同主角。Airbnb 的 2020／2022 10-K 可證疫情打擊與復甦，但反轉較常見，2020 淨虧損含上市相關會計因素，難以用一個數字代表旅行需求。Kellogg／Kellanova 2023 年分拆是好故事，但現有 A21 品客已講家樂氏改名與 Mars 收購，角色與事件重疊較多。Spotify 的兩次具日期的買入、2023 播客內容認列、2024 盈利與 2025 成本分類變化，構成較獨特且可逐步揭露的因果問題。

落選選題的實際原件：[Airbnb 2020 10-K](https://www.sec.gov/Archives/edgar/data/1559720/000155972021000010/airbnb-10k.htm) SHA-256 `253c29e43012a62bf28b46ca69538d06994173398a49efa0e8a0b4d5d29f4331`，與 [2022 10-K](https://www.sec.gov/Archives/edgar/data/1559720/000155972023000003/abnb-20221231.htm) SHA-256 `ba6984f9a29367aa4aa7686b40ee8176b346704b626a7c07d01abf4157568277`；後者列 2020 淨虧損 US$4.6bn、2021 虧損 US$352m、2022 淨利 US$1.9bn，但差額不可當作純疫情需求變化。[Kellanova 2023 10-K](https://www.sec.gov/Archives/edgar/data/55067/000162828024005583/k-20231230.htm) SHA-256 `dda2140bab30b5feb2a350081aedc8d498c7eaae7c3c69012364b9bdb129dd73` 記錄 2023-10-02 北美穀片事業分離為 WK Kellogg Co；它與 A21 的同公司段落相撞且原件大於工人讀取上限，故不選。
