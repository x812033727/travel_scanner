# X19 Uber v7｜作者對 v6 雙盲 Q8 的修稿對照

v6 [獨立 SEC 查核](script-source-audit-v6-independent.md)只對舊 SHA 判稿件事實 PASS；兩位全新[讀者 A](blind-a-v6-independent.md)與[讀者 B](blind-b-v6-independent.md)都判正式敘事 Q8 NO。`x190412` 已說明第三季的 Postmates 簽約尚未交割，`x190421` 的「收購仍只是紙上的約定」在同章重講了相同狀態；`x190405` 也已區分簽約與整合。這是作者對照，**不是** v7 的獨立來源查核或敘事票。

| v6 斷點 | v7 修訂 |
| --- | --- |
| `x190421` 把待交割狀態再說一次，雖然後半句帶來另一套 App 尚未接入的新資訊。 | 刪去前半句，整句成為「另一套 App 還沒有接進來。」保留第 4 章到 `x190422` 年底合網問題的銜接。`x190412` 仍是第三季待交割狀態唯一一次明說，`x190405` 保留七月簽約不是完成整合的當時進展。 |

改動只在主片 `x190421` 的旁白與由它生成的 `say`／`say_for`；該鏡的 cue、prompt、shot ID 和 Short 2 最後一拍的取景均不變。六章、110 句、95 張無品牌 still、12 張原生數字卡、24 條有序 loop、187 字開場維持；正文由 2507 字變成 2496 字，按每分鐘 300 字約 **8:19**，仍不是實際 TTS 長度。兩支各 8 拍、163／171 字的 Short 題目和旁白不變，`shorts.json` 重建後仍為原 SHA。

**v7 作者凍結值：** `video.json` SHA-256 `f4e373a53a3424f29f9c3e511f13c2489ac9c7e93c4500413038060d8d08a385`；`shorts.json` `b6b0212372d776c96572450baa8e9c4350499c72923d088ad0bd6833e8681d95`；`drafts/narration.md` `959b8da99002f86239897d52fbc2559b22bf040f179bc8d3e91178fccf965d6f`；`source-matrix.md` `5e949609bf8163b28cfeea3ca3592c52855e6ece34f52f3da37549efe3d31043`；`visual-plan.md` `137cd29316b1ec634d299f23b543974a865d77415916ea2d83ae8afad0c668ee`。來源矩陣只有版本與舊查核界線說明改動，原件日期／bytes／raw SHA 和事實邊界沒有增刪；它仍需新的獨立查核。

作者離線驗證：主片 lint **0 errors／0 warnings**，約 11.3 分鐘的整片粗估；兩支 Short 的個別 schema／主片 shot hash 均 PASS，composer 的 `episodeShortsProblems` 為空；`test:docs-videos` **236／236 PASS**、`check:tasks` exit 0（只輸出倉庫其他任務的既有警告）、`git diff --check` 通過。仍需 v7 **新 SHA** 的獨立 SEC 查核與兩位真正新首讀；正式機還須量 TTS 實質正文 ≥8:00、審核插畫和官方 5 秒／21 秒動畫、守 US$25 實際整片支出、驗 Shorts 25–55 秒及直式觀看，再產 MP4 與真實 YouTube 連結。本作者文件不代替那些驗收。
