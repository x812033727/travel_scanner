# S61 R9｜推薦 A 案、媒體報價與政策誤判停點

2026-10-22 UTC。R9 [獨立固定史料與書面畫面](r9-independent-source-visual.md) PASS（103／103 史實旁白、96／96 插圖提示、7／7 資訊卡）；[兩位正式隔離盲讀合併](r9-formal-merge-audit.md) 13／13 PASS。R9 `video.json` SHA-256 `005cc35734535c8a01ee46f7ee5dc1a3555d3b543d0fc3b42c0beda2812d97ce`、`script.md` `e3f27c9da2b951fd744e9de48b2c64d665ef4f76cd6abaa4e323b43c5ebb9eb9`、`claims.md` `37eb7bf2a039692d583e15b1e2e2aab477096ba47ee526fe8876a26e995df11c` 未動。本輪只把 `brief.md` 的過期 R8 HOLD／R9 待審狀態與暫時性媒體文字改成正確 R9 PASS／後續收據索引，A／B 大綱與六章企劃內容不變；新大綱 SHA-256 `564fc9466b0de3473198bfd7fbf590468b3a708c81579249466a8121620137a0`。另新增 [正式品管可見的史實查核入口](../verify-1.md)，指向既有獨立 R9 收據，不冒稱新做一輪獨立查核。

## 大綱與劇本的精確核准

站主於本對話已授權「用推薦的決定就好不用問我」。A 案「已經炸過一次的城市，又收到警報」為作者推薦，網站 `review-push --gate outline` 的 Jev 也選 **A（1.00）**，網站回覆符合立場 0.89、建議 0.01。網站因本機稿沒有工人的 `auto.json`，把 outline 與 script 各送一張 `hand_pushed` 審核卡、仍顯示 pending；**沒有聲稱站主親自閱讀劇本、點選後台或聆聽語音**。依上述站主對推薦決策的授權，本機 `approve --gate outline` 與 `approve --gate script` 記錄代行決定及 exact hashes：`brief.md` `564fc9466b0d…`、`script.md` `e3f27c9da2b9…`。私人 `approvals.json` SHA-256 `3341ba97b394ab02477b3dc3190102236be0afe4f625cc0ff2bb089a080a9da5`。後台待辦與本機雜湊核准的來源不同，兩者不得混稱。

## 政策預檢：站台 Jev 判業配 0.31

對 exact R9 旁白與 `brief.md` 站主觀點只送**一次**網站 `automation/judge/policy`；私有原始答覆保存在 `/workspace/.video-work/curio-s61/policy-preflight.json` SHA-256 `0602e5b14d07a0795f0208a9342259938ac37ff611bc297844d1f61842ccc64f`。Jev 回 `stance=0.70`、`demo=null`（解說不適用）、`advice=0.01`、`sponsored=0.31`，因站台 0.30 門檻而 `passed=false`。全稿搜尋只見片尾「想聽有出處、不把警報說成結果的歷史故事，**訂閱奇聞檔案局**」及品牌片尾的訂閱文案，沒有贊助商、商品、價目或業配口播。這與另案 [自家訂閱 CTA 政策誤判修正 PR #1664](https://github.com/x812033727/travel_scanner/pull/1664)的問題相符；修正尚未部署，不把這張 FAIL 說成 PASS。已保留政策結果，**不重問 Jev，也不為降低分數改寫已過史料與雙盲的稿件**。完片時須在站台修正生效後以正式 QA 重新判，或交站主對政策項作明確裁決。

## 語音及整集媒體價格

正式 `lint --json` exit 0，0 errors／0 warnings，106 句（103 句正文與 3 句品牌片尾）、六章；開場按 325 字／分鐘估 **48.23 秒**，正文 **487.13 秒（8:07.13）**，是合成前估時。`tts --dry-run` 為 **106 句／2,668 計費字元**，頻道聲線 `gemini:Sulafat` ready、當月餘 7,887,491 字；本輪沒有合成音檔、timeline、check-audio 或人耳審聽。S60、S62 同一網站語音近日均先回 429 忙碌／額度，故本輪不再送可預期失敗的第三次實際語音請求；下一次不早於 **2026-10-22 07:05 UTC** 太平洋午夜重置後，先重查狀態、再單次嘗試，若仍 busy 就停止。

`media-status` 顯示 MiniMax `image-01`、當月餘 10,056 image／8,506 judge／28 music，S61 本集 US$0。`keyframes --dry-run --takes 3` 對 **96 個插圖景**報單輪約 **US$1.30**、最多三輪約 **US$3.89**；`music --dry-run` 因沒有目前劇本的 TTS timeline 而拒絕報價。整集插圖＋評審＋配樂的硬上限須在同版語音完成、正式音樂 dry-run 後一次固定；這裡的 US$3.89 僅是插圖報價，**不是已開畫授權或已花費**。所有原生插圖、音樂、品牌動畫、正片、Short、字幕、QA、上架包和真實 YouTube Studio 可點連結均未製作／驗收。
