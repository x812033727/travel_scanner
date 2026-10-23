# C15 FriXion｜作者稿與分鏡收據

日期：2026-10-23（Asia/Taipei）。**狀態：作者自查完成，待獨立查核、兩位只讀旁白盲讀及站主劇本／逐鏡核准。** 此文件不是獨立來源查核 PASS，也不是付費製作批准。

## 承接的核准範圍

- 站主已採用修訂六章企劃，依 `owner-treatment-adoption.md`；Treatment SHA-256 `D84494C81E2034B116C0322EF416E17C3DDE860B58626D12DE2E73501980D9C0`；來源矩陣 SHA-256 `6E030F4399F6FD2AE99550DE89B5B46658D708CF870910199804069A784C4C09`。兩份原件在此分支未修改。
- 原 Treatment 草稿 PR #1696 的最新任務移轉提交：`7031cd928ba5f43856bf96af58732004d3a627bd`。本稿由它另開 `codex/brand-story-frixion-c15-script` 分支，草稿 PR 應以該分支為 base。
- 舊 `tasks/open/2026-10-22-c15-frixion-treatment.md` 經使用者手動移除後，作者在原 Treatment 工作樹核對：舊檔不存在、`tasks/done` 完成版存在；只提交該已完成的任務移轉。沒有繞過先前的自動核准封鎖。

## 作者稿凍結內容

| 路徑 | SHA-256 |
| --- | --- |
| `script.md` | `FAB7571AD64F338FD44C19AD2B60CB04FB70BC62A3D4BD8E70FF5E998B8AAF8E` |
| `script-source-notes.md` | `6102BBE94D970F2F2D344D4ADCECBC592C32A40C4805F1D26C319468C78F8B8E` |
| `visual-plan.md` | `AB6EF77756ED8E6904AE22B7ACE8DB2D733338B7C4647658E319A2D19272F512` |
| `visual-plan.json` | `6B33E813D57BAC2C1DAF0C29BBC2E6CAE9C784D80D23520D048C479271EB72DE` |

上表綁定 PR 的 Git blob 位元組（`git show HEAD:<path>`）而非 Windows 工作檔換行。`visual-plan.json` 在本機工作檔為 CRLF，當時量到的 SHA-256 `6D11E8F1B682DC390541DE795F53FE548E81F0FC73193FFB2DE07FB77C2E8AF1`；Git 收進的是 LF，因此 PR 與 fresh checkout 的 SHA-256 為上表 `6B33E813…`。兩者只有換行差異，逐鏡內容未改；獨立審查請以 PR blob 雜湊綁定。

87 句旁白和 87 鏡 ID 一對一。71 鏡插圖，16 張後製字卡；最長連續字卡 2 張；71 個圖片提示詞各不相同。旁白欄合計 2,414 字符，**250 字符／分的紙上代理值約 579.4 秒**；按旁白字符加權的紙上插圖占比約 80.3%。這些都是規劃數，不是 TTS、圖片時間或剪片實測，不能拿來通過正文 480 秒及插圖畫面 ≥70% 關卡。片頭 5 秒與片尾 21 秒不計入正文。

作者機械檢查：`script.md`、`visual-plan.md`、`visual-plan.json` ID 集合相同且無缺漏；提示詞不含 FriXion／PILOT／ILLUSION／Magic Cup 等品牌或產品字、logo、字體及畫風替代詞；`look.preset` 全為 `cute-mystery`，模型為 `MiniMax image-01`。畫面是內容相關的概念插畫，非歷史照片或精確化學示意。`npm run check:tasks` 於本工作樹退出碼 0，驗證 2076 張任務檔；其他既有任務的過期持有及範圍重疊只列 warning。最後提交前再記錄 `git diff --check`。

任務板小插曲：`npm run tasks -- done 2026-10-23-write-c15-frixion-source-bound-script` 初次寫出 `tasks/done` 後，回報 `tasks/open` 舊本仍存在並退出碼 1。作者核對完成版存在後，依 CLI 的「delete that open copy by hand」提示，以 PowerShell `Remove-Item -LiteralPath` 僅移除**本支新建**的 open 副本一次；讀回 `open=False / done=True`，再跑 `check:tasks` 已通過。這不是 Treatment 既有任務檔；不因 CLI 首次失敗宣稱已自動乾淨移轉。

## 另一位審查者要做的事

1. 重開 S1–S6，一句一句核對來源矩陣的窄說法，尤其 1972 專利只見公司回顧、2002 ILLUSION 仍有色、2006 才有 FriXion、2004 只是商品化決策、試賣數字的分母、現行 60°C 與 2017／2024 約 65°C 各有文件歸屬，以及低溫回色沒有保證。
2. 逐句和配對圖一起看，有無用概念插畫偷渡額外史實；特別檢查 H03、I16、E08–E10、T06–T07、N07–N12。審查者另留獨立收據，不能把本作者收據改寫成 PASS。
3. 兩位只讀旁白的盲讀者不看來源說明，分別檢查單線敘事、口語、45 秒鉤子、伏筆回收及重複句；作者檔若實質改動，重算雜湊並重核變動範圍。

## 後續停線

尚無任何本集付費 TTS、圖片、配樂、成片、上傳、發布或站主劇本核准。獨立稿件關卡後需向站主送審目前劇本與逐鏡方向；整支圖片張數、每張嘗試數與總費用另需一次報價、另獲核准。即使獲准，先實測正文旁白 ≥480 秒與預算路由，才可買圖；實際時間軸仍須確認插圖占比 ≥70%。
