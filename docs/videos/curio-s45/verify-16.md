# S45 R8｜同版政策、站台卡與語音交接

2026-10-20 UTC。精確 R8 `brief.md` SHA-256 `965d4f46b1b90cad9d52882ca5187003c42ca9a897debc874fbc0937d5a40909`、`script.md` `6210aa1a85ca1e69ee01a3cfe9ce5a970336b262cdc3beb8cd1e944f1da1603e`、`video.json` `c3fa833ef6f60de7e3ef90e1fc7436d72add3c6a30d3756b6a97bfbaaa28d4ce`。已通過[獨立來源／書面畫面](review/r8-source-independent.md)及[兩名真正新讀者的合併敘事](verify-15.md)，保留 B 的 `no_recap` No 與片尾口播訂閱警告。

本站已存在 `category=explainer` 的 S45 row；在確定三檔雜湊無漂移後，只對 R8 做一次類別正確的 `policyRequest`。請求 SHA-256 `518ad0f1fde0c6528c2c555714411739e7e42ec9daa83555d9461362908482c4`，匿名[回條](review/r8-policy.json) SHA-256 `26a8db10b5edbba4d8b98ce056b52719d3b8b70c37d5e160c704bf17e2a86f76`：Jev `explainer` **PASS**，立場 .78、示範不適用、建議 .02、業配 .02。R6 舊兩次政策 FAIL 仍是歷史記錄，不挪作 R8 的成績；R8 呼叫紀錄在本地工作目錄 `review/policy-pre-tts-r8.*`，不重送同一 paid request。

`review-push` 已把精確 R8 A 企劃與劇本送網站；兩者 `hand_pushed`。`review-pull` 說舊核准綁已變更版本，而**目前兩張卡 waiting for the owner**，不能叫網站或站主已核准 R8。依使用者「用推薦的決定、不用問、持續製作」的持續授權，本地 `approvals.json` 於 14:50:31Z 對精確 R8 brief、14:50:35Z 對精確 R8 script 記 **LOCAL delegated editorial decision**，每條明註網站仍 pending、不是站主網站核准；這讓工具在本地繼續語音，不改寫網站審核事實。

`tts --dry-run`：Gemini `Sulafat` ready，102/102 新句、約 **2,558** 可計字元，站台顯示當月剩 8,620,990 字元，約免費層 0.5%。此時**尚未實際合成**，更沒有零旗標音檢、插圖、品牌片頭片尾、配樂、成片或可點連結。下一步只做精確 R8 TTS、實測開場／正文，再跑每句完整音檢；任何旗標先分級處理，零旗標且獨立音質證據足夠前不啟動 MiniMax 付費製圖。R8 `lint` 的 1 項片尾口播訂閱警告已公開保留；視覺 21 秒動畫片尾仍規劃訂閱與推薦卡位。
