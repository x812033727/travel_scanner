# 獨立事實查核報告（Round 1）：`sothatswhy-p25-train-tunnel`（為什麼高鐵車頭要做成長鼻子？｜原來如此事務所 Ep 25）

- **查核日期**：2026-11-18
- **查核角色**：獨立唯讀事實查核代理（Independent Fact-Checker `c3d25482e7a9a61b8f907b99d8dbf80d`）
- **查核範圍與初版檔案雜湊（SHA-256）**：
  - `docs/videos/sothatswhy-p25-train-tunnel/video.json`：`c733463fb9c6263f329321742580d5ed91d8c5d86f43cb300a3c9c3c3d2cf134`
  - `docs/videos/sothatswhy-p25-train-tunnel/claims.md`：`8d1244eaca6095997e10806c4db0e81992896cefe194e0e07baf5742e975c4d7`
  - `docs/videos/sothatswhy-p25-train-tunnel/brief.md`：`b9515e01d0894990065ee513a655dd67bbe64bec4f998605f828199da675b08a`

## 一、Round 1 總體判定：FAIL（需修正 3 句台詞措辭歸屬、5 鏡視覺規範違規、9 筆書目資訊及 1 筆發音辭典缺漏）

1. **未公開數據與翠鳥迷思邊界**：PASS（零處捏造 N700／N700A／N700S／N700ST 車鼻公尺數；明確交代「翠鳥只是靈感、曲線由細管射彈與超級電腦硬算出來」）。
2. **台詞歸屬修正項（已排入 Round 2 修正）**：
   - `p011`（F1）：吉川岳（2017）僅提車體側面與車廂間阻力占大半，未提轉向架與集電弓風阻 → 改為外牆摩擦與車廂間亂流累加。
   - `p047`（F2）：原田巌（2003）指圓錐截面積變化率隨距離增大，未寫「暴增越快」 → 改為「截面積增加率越大」。
   - `p060`（F3）：JFS 專訪原文為放棄時速 350 公里以上之「試驗運轉」（test runs），非商業運轉目標 → 改為「試驗運轉」。
   - `p019`、`p095`（F4）：補「約四倍」並區分緩衝罩洩壓窗與隧道上方洩壓孔。
3. **視覺提示詞修正項（已排入 Round 2 修正）**：
   - 第 27 鏡 `above-20hz-audible-boom`（V1）：移除 `a passerby`。
   - 第 58 鏡 `faceless-engineer-400m-houses`（V2）：移除 `nobody: true` 鏡內之人類剪影，改為測音腳架儀器。
   - 第 96–98 鏡（V3）：移除橘色條紋塗裝字樣，統一為無標誌白銀泛稱列車剪影。
   - 第 1 鏡 `kid-platform-noses`（V4）：人物與模型置於下 2/3，上 1/3 留乾淨晴空配合 `layout: "heimao"`。
4. **書目與發音辭典修正項（已排入 Round 2 修正）**：
   - 修正石塚理出版年份為 `2004`（《らん》65 期〈台湾南北高速鉄路用車両の概要〉）、東洋經濟日期為 `2018-03-10` 等 9 筆原題，並補入 JR 東海 `000034313.pdf` 與台灣高鐵 `e1e25e6a-4139-44d4-ac30-3f9724f08310`。
   - `story-lexicon` 補入 `"700T": "七百 T"`；`kid` 語音 `style` 改用試播集定案寫法。
