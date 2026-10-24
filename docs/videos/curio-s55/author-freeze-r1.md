# S55 逐句稿 R1：作者交接

2026-10-20 UTC。推薦 A「從樹枝到脫繩」已依獨立題材 [PASS](source-feasibility-1.md) 寫成完整候審稿。**本記錄是作者交接，不是獨立逐句來源覆核、盲評、站主劇本核准或媒體驗收。**

## 精確版本

| 檔案 | SHA-256 |
| --- | --- |
| `research.md` | `429ba95ec515b09a91f831baa436348ece8d8983d090f8bebe64a0ca640bdd3d` |
| `brief.md` | `e603fdcccf91d884b71cf073005299bcf97dfa8b8cd4a35a44a9b8ea46a28f77` |
| `source-feasibility-1.md` | `070c33f7b6b7c4ecc4692742a574cf454759c174f7d777c71d5d6a555af2141d` |
| `video.json` | `ece1d62b6b0a2a34cf442b67f7b04190c934c47d54141d957c358d6c7487e1e2` |
| `script.md` | `e9c2ab9462948301006739b815afbe70ccaf0515e2453f4bf6c0024ceaecbe76` |
| `claims.md` | `9af49bc43f6a41359eb0bec4ea70db17cee3ac7c6f278260244d8048fc8f081e` |

原獨立題材 PASS 所指的 `brief.md` 是 `2d5fcbf012be3d1b3614e8f38d96511a8d42ad2ee3a5807abdb0edbf542c55f6`。之後僅新增 lint 要求的三個 H2 標題，三段文字及史料選擇不變；差異已在 PASS 檔末段記錄。

## 作者量測與交付

- `video.json` 共 7 章、149 個含濃縮開場的旁白句、3 個片尾卡句、127 個 `shot` 插圖分鏡、12 個指到精確句 ID 的懸念回收。逐句 `claims.md` 的 149 列與旁白 ID／原文完全相等，全部有固定提交行號連結。
- 開場濃縮的旁白有 167 個中文字，按每分鐘 325 字上限估 30.8 秒。之後第二章開始前依 [頻道規格](../BRANDING.md) 插 5 秒片頭（`after_first_chapter`）。**尚未合成音檔，沒有實測秒數。**
- 正文不算開場與片尾，有 2,667 個中文字；按每分鐘 325 字上限估 **8.21 分鐘**。影片工具以 250 spoken units／分鐘連停頓估整段腳本 **13.88 分鐘**；實際 TTS 和成片仍須分別量時長，未把估時當成通過。
- `look.preset` 為 `cute-mystery`，127 個正文場景全為原創插圖提示詞，強制分清密封氫氣球與底部開口熱氣球、繫留與脫繩。籐台掛樹只畫在有繩的試升。原件字樣、航線、人物逐字對話與照片均不重建。
- `music` 沿系列無人聲輕快懸疑配樂。`outro` 的三句只做本集收束、留言問題與訂閱邀請；正式片尾採頻道 21 秒 v4 endscreen，最後 16 秒應在 Studio 匯入兩個推薦元素與訂閱元素。YouTube 說明欄有 F／M／E 三個固定全文連結與真實頻道連結；`video_id` 留空，等真實上傳後才可填。

## 自動檢查

- `node tools/video/cli.mjs script --slug curio-s55` 已從精確 `video.json` 產生 `script.md`。
- `node tools/video/cli.mjs lint --slug curio-s55 --json`：**0 errors、0 warnings**，估時 13.88 分鐘、152 句含片尾。
- `npm run test:docs-videos`：236/236 通過；`npm run check:tasks`：格式檢查通過，另有既存任務過期與重疊警告。
- 本稿尚待另一位工作者逐句對 F／M／E 審核，再交兩位新讀者各自盲讀。**沒有呼叫付費配音或插圖，也沒有成片、Short 或可點的 YouTube 片尾連結。**

## 下一關

獨立查核者須重開固定版全文，以本表精確 `video.json`、`script.md`、`claims.md` 判逐句來源、證據層級、視覺界線和日期處理。特別注意 F 的「據說」戈內斯攻擊、未親見凡爾賽動物實驗、M 的十月繫留與錯寫十月二十一日、11 月有繩的樹梢試升、乘員轉告的地標／著地，以及 12 月當晚未收到安全消息。實際媒體階段應以核准後的精確稿件和當次報價、時長、聽審及畫面查驗為準。
