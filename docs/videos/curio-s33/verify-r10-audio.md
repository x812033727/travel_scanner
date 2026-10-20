# S33 R10 配音、全句音檢與停手點

2026-10-20 UTC。R10 固定 `script.md` SHA `f730a8f8834253f648034b86cf590d27233d4f0500c746be6280fd9219549202`、`video.json` SHA `92e6262b08beb8255b5e7b3b4d62b0a76a7f0fb9c7d62839494cb96755751e7a`。獨立來源差分 [PASS](verify-r10-source-independent.md)，兩名全新讀者按系列合併 [PASS](reviews/narrative-r10-merged.md)（A 的 `payoffs` No 留在收據），本版唯一一次 Jev 政策 [PASS](reviews/policy-r10.json)：立場 0.84、建議 0.01、業配 0.02。

R10 `script` 已 `review-push` 到後台，類型 `hand_pushed`、狀態 **pending**；`review-pull` 仍說 R7 站主真實核准綁舊版。依使用者「用推薦的決定就好不用問我，一直做完」的持續授權，本機 `approvals.json` 另外記了明示 **LOCAL DELEGATED** 的 R10 精確劇本核准（13:54:18Z），只是工具繼續配音的本地決定，**不是網站站主新核准**。

| 階段 | 實測與收據 |
| --- | --- |
| 首次 Gemini／Sulafat TTS | `--dry-run` 報 98 句、2,439 字元；實作 98 新句、0 重用。`timeline.json` SHA `dc84b8168f7c61e7e6eea64d403e4497ac19e0b8453a4031094a1f369a30f0e2`、`narration.wav` SHA `4526214ae21b7e11fe994ca0cdbc7056aef54d9123071e55b3f3bcb092f5c2b3`。開場 48.833 秒、正文 580.033 秒（9:40.033）、片尾 20.400 秒、全段 649.267 秒。 |
| 第一次完整音檢 | 98/98 句，33 exact、29 同音／語助、1 Jev 可用、**35 旗標**；98 新轉錄／1 Jev 呼叫。完整 [check](reviews/audio-check-r10a.json) SHA `25b6ccc3c6c9e4f33ce0953d296dd83d59981b2e3f983bb88152a9ec81ef70ad`、[flags](reviews/audio-flags-r10a.json) SHA `87bb0ecf8b21c1aa39261959af816dcdff654c274a9354ea07b4771fecb87391`；35 句的 [風險分級](reviews/audio-triage-r10a.md) 區分語意疑慮與同音／專名 ASR 猜字。 |
| 一次定點補錄與複檢 | 僅 11 句可能改變原意者各補錄一次，268 新字元、87 句重用；全文 `speech_hash` 仍 `694886928090890d`。新 `timeline.json` SHA `0c55400c8b4f6ca78b41aeecfcc1301abe6ec29935535d01222a49ff91148574`、WAV SHA `b61a4a856784a617173aa246bd9a84506504dfdea1fad36122ae506ffe054987`。開場 48.833 秒、正文 **581.533 秒＝9:41.533**、片尾 21.767 秒、總長 652.133 秒＝10:52.133。複檢 98/98：36 exact、29 同音／語助、1 Jev 可用、**32 旗標**；只新轉錄 11 句、1 Jev 呼叫。完整 [check](reviews/audio-check-r10b.json) SHA `7184f0ee0e507bcb37b41db281b73eec259c30592e6841662a675d4fa204e645`、[flags](reviews/audio-flags-r10b.json) SHA `3bcd38ed750540edb3120b24910be955d511166b93972ea2a9d040a619593240`。 |

一次補錄明確清掉 `hj017`（私寫）、`hj045`（命人學）、`hj053`（世宗／薛聰／舊吏讀）三句；其餘 8 句仍標。`hj066` 的新 ASR 已聽對「義禁府」，卻又聽成「著名官員／叫到」，故整句仍標；`hj063` 專書《三綱行實》的新 ASR 猜字反而偏得更遠。剩餘 24 句原樣保留，多屬「新字／薪資」「奏疏／造出」一類近音或罕見人名書名的辨識問題。沒有獨立第二轉錄器或真人聽審，不能從 ASR 及 Jev 分數推出全部 32 句的真實音讀；也不能反過來把它們當作零旗標。

**硬停在音訊關**：`check-audio` 退出碼 1，`check-flags.json` 尚有 32 個 ID；沒有送 `audio` gate、沒有記本機 audio 核准。依本集進入插圖的前置條件，**MiniMax 付費插圖仍 US$0，pilot 未開始**。已備 [原生 1K 三景 pilot 與整集 US$3.65 上限](reviews/art-pilot-r10.md)，只有音質零旗標後才可用。可恢復路徑是獨立第二轉錄／實聽核對剩餘旗標，或只對證實發音不清的原句修讀法；若改稿，必須重新綁定劇本雜湊、來源及敘事關卡。片頭 5 秒動畫、畫面、21 秒左右片尾、配樂、成片及連結包仍未製作。
