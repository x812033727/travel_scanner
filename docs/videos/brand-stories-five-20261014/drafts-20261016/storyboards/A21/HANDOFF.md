# A21 Pringles 免費分鏡交接

狀態：待 root 獨立分鏡審查；不是正式 worker 章節或媒體核准。

- 原全文 SHA：`c250fb1f03f1b4868519a7d902af08247a214b2a228dc372efde8474b94cdc82`。原稿 47 段、2,281 字；active 候選 47 段、2,283 字。只改 T06 主詞；其餘 46 段、所有 ID／順序不變。active 原段與 UTF-16 偏移完整重建。
- 89 鏡：78 插畫（87.64%）、11 卡，最多 2 連卡；3 組共用後規劃 75 張獨立圖片，沒有已產圖片。
- 開場共用圖：S004→S035（H03→E01）、S005→S055（H04→T01）、S006→S067（H04→N01），各組 prompt／camera／asset key 相同，收圖後仍須同 file/hash。
- H04 依原分號拆開 2008 與 2009 預告。S005 估 2.40–2.61 秒，保留原句快速預告，不補停頓。其餘 21 鏡的 5–8 秒邊界估值例外完整列於 metrics。
- 六章正文含 hook：估 547.92–595.57 秒（9:08–9:56）；hook 39.36–42.78 秒。另加 5＋21 秒 branding，總估 573.92–621.57 秒（9:34–10:22）。不是 TTS 實測。
- 片尾最後 16 秒（片尾第 5–21 秒）保留連結區；實際既有影片／訂閱目標與 branding file/hash 尚待上架包。
- 33 個 CID 映射至 6 個 active source index；各句沿原段 CID 範圍繼承，不冒充已做字句級 worker claim 查核。所有 source pins 為 repository_root 相對路徑。
- 數字卡限案件配方、裁判層級、當事人估額／說法；42% 不當門檻，估額不當欠稅，2025 不當品客再審。沒有內部 fetch 失敗狀態進觀眾卡。
- 官方 shot_reading CLI 實跑 exit 0：78 張插畫，0 traps；無三連同運鏡。沒有模型、網路、付費、TTS 或媒體生成。

## 檔案雜湊

- storyboard.json：`a5fab1e0e5932c34ed64e2731e2f40aafbea608dd57856758963ba4f117ccba3`
- storyboard.md：`eb730a3f75a35b30e8d0d908e854daa1b860da8712c892dbf9bd78a585e37218`
- source-map.json：`4d449e1638d2ea1e75a4b843830f70da14747fd2eec45f19a0dd83c9821cc5d8`
- paragraph-table.md：`9c01718b39e26776c83c9c0c8dec73d38bf1c0073c252d6e126ed30485f053f9`
- offline-verification.json：`7c1544e2150dae3a558f12cf9556728486b7d0f6e60b5bad025d95eb4c614ab7`

## 唯一原文改動

T06：

> 這回，稅務機關要說服上訴法院，高等法院把這句話讀得太窄，而最初稅務法庭的判斷應該恢復。

C22 仍綁原 2009 判決（active source index 3）；此改寫由作者澄清主詞，獨立覆核待 root。完整前後字串／hash、v1 保全及分鏡 delta 見 revision-manifest.json 和 adaptation-manifest.json。S064 的示意律師改為中性法律讀者比較卷宗；同鏡不把兩方論點歸給一人。原稿、v1 分鏡與既有獨立 review 均未改。

## 重跑

在 repo 根目錄以穩定 Node 執行本目錄 build-prep.mjs，再執行 run-offline-checks.mjs。或以 PREP_REPO_ROOT 指定 repo 根目錄；來源 pin 不依賴本機絕對路徑。complete-prep-template.mjs 是一次性的 A16 模板差異記錄，不要重複執行。

正式章節轉換、真查核／聽稿／敘事關卡、實錄時長、完整報價授權、圖片評審、成片播放與站主審查仍待做。
