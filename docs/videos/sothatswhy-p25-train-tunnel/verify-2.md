# 獨立事實複查報告（Round 2）：`sothatswhy-p25-train-tunnel`（為什麼高鐵車頭要做成長鼻子？｜原來如此事務所 Ep 25）

- **複查日期**：2026-11-18
- **查核角色**：獨立唯讀事實查核代理（Independent Fact-Checker `c3d25482e7a9a61b8f907b99d8dbf80d`, Round 2 Re-Verification）
- **複查範圍與檔案雜湊（SHA-256 實測核對一致）**：
  - `docs/videos/sothatswhy-p25-train-tunnel/video.json`：`b7c90cbb9ec4b820614adc30746104c2ee254a29d9bf76d1d25fa33ece8c2a04`（6 章、105 鏡、106 句台詞 `p001`–`p106`、14 組 `loops`、`youtube`、`thumbnail`、19 筆 `sources[]`）
  - `docs/videos/sothatswhy-p25-train-tunnel/claims.md`：`a00bd71151ca72461265fb183fcbaf8a11497a0129ce7c744630066938798e4a`
  - `docs/videos/sothatswhy-p25-train-tunnel/brief.md`：`b9515e01d0894990065ee513a655dd67bbe64bec4f998605f828199da675b08a`
  - `docs/videos/sothatswhy-p25-train-tunnel/script.md`：`827f82c081c29eaee601ce3b75db4cad286b75792abd072df60c0851510f585f`（`narrative 6979637e37c1ac65` / `speech a1edc4092ffe3ea7`）
  - `docs/videos/sothatswhy-p25-train-tunnel/story-lexicon/current.json`（及快照檔）：`lexicon_sha256 = f81576a81ffac051cae8e8e413bace9e414b58b1222effa4ba24eab7a9d76501`
- **機械檢查結果**：`node tools/video/cli.mjs lint --slug sothatswhy-p25-train-tunnel` → **0 errors, 15 warnings**（預估 11.4 分鐘、106 句、2,761 口播單位；所有 `say_for` 雜湊、14 組 `loops` 前後序、`script.md` 同步性及 `heimao` 縮圖規範均 0 error 通過）。

---

## 一、總體判定（Overall Verdict）：**PASS**

Round 1 查核指出的全部必改與建議項目（`F1`–`F4` 台詞與來源對齊、`V1`–`V4` 畫面規範與 `nobody: true` 純淨度、19 筆書目年份／標題／直接 URL、`700T` 發音綁定 `say`／`say_for`＋`story-lexicon`、`voice.style` 語速提示詞）及 Round 2 收緊之台詞（`p001`、`p040`、`p069`、`p074`、`p086`、`p087`、`p091`、`p097`–`p106`、`youtube.description`）均已逐字、逐欄核對一手文獻與系列規範，確認：

1. **`0 NOT FOUND`**：全片 106 句對白、`youtube.title`、`youtube.description`、`thumbnail` 與 `claims.md` 的每一項事實、年份、數字、人名／機構與物理因果鏈均有對應一手文獻支撐。
2. **零捏造未公開車鼻公尺數**：N700、N700A、N700S、N700ST 均未編造或引用二手矛盾的單獨鼻長公尺數（僅引用 JR 東海公開之先頭車全長 `27,350 mm`、雙重極致翼形 `Dual Supreme Wing` 及台灣高鐵公開之 N700S 基礎架構與營運時程；未公開鼻長附註僅置於 `claims.md` 與 `youtube.description`，對白零防禦性但書朗讀）。
3. **翠鳥仿生順序精準**：嚴守「年輕工程師體感 → 仲津英治聯想翠鳥入水靈感 → 細管射彈測壓與太空研究級超級電腦模擬算出理想截面變化曲線 → 結果與翠鳥喙到頭極為近似」，明確破除拿尺照鳥嘴描圖迷思。
4. **視覺、商標、人物與發音合規 100% 通過**。
