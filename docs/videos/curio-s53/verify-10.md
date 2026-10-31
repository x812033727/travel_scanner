# S53 R10｜敘事、政策與語音關卡收據

2026-10-20 UTC。對象是 1906–1908 年舊金山救災小屋的 R10 精確版本。**獨立史料／書面畫面 PASS，官方隔離雙讀者敘事 PASS，R10 政策 PASS；實測語音正文超過八分鐘，126／126 句音檢零旗標。** 網站企劃及劇本卡仍是 `hand_pushed`、站主待審；本機委派劇本選擇有明確附註，不能冒充網站核准。本輪未做付費插圖、配樂、成片或發布。

## 固定稿與敘事

| 檔案 | 本輪末 SHA-256，與 R10 作者凍結及獨立來源審查一致 |
| --- | --- |
| `brief.md` | `8e44f47693dd75ad0a7509ab0f495c06adcc2e614b8c8bc09a51559d7202a27c` |
| `research.md` | `2e61530c650852281402476041175154ee69c414daf7431d6aa0db352e7c3d22` |
| `claims.md` | `b5be9bbbf8c78cc87c32efcc0964afea1cb689a225b1a216184db750623b5f84` |
| `video.json` | `6e271778492bdcd97e1ffb3ee700e99fe848f0fd8d077bb705a6972b3e29a9f5` |
| `script.md` | `64ffcd8c0e89c4596a7fd08d41bd74f8a16f55fbc9acc2f41d7f9b914ea300fc` |

[R10 獨立來源及六景書面畫面審查](review/r10-source-independent.md)為 PASS。兩位未讀本版作者材料的[隔離讀者 A](review/r10-isolated-blind-a.md)、[B](review/r10-isolated-blind-b.md)各有 **13／13** 帶句 ID 的 Yes。[官方合併](review/r10-official-merge.md)使用 `panelVerdict` 與 `mergePanelVerdicts`：十三題全為兩位 Yes、零必答失敗；[CLI 第 9 輪收據](review/r10-official-cli-receipt.json)與現稿的 `narrativeReviewMatches` 為 `true`。CLI 收據 SHA-256 `7d8815cc53d9e2c018eb902844e7e99341e069e8ff62a36f6ddede69664c603d`；[兩讀者合併審計](review/r10-official-merge-audit.json) SHA-256 `76056402de83740e84e9b2fd998ce7387cb7530e7223ed4ddc1d28f258f4cba2`。`lint --slug curio-s53 --json` 仍為 **0 errors／0 warnings**，126 句、124 景。

## 網站及政策

`review-push --report-only` 後讀回網站分類 `category=explainer`、`format=drama`。`review-push --gate outline` 對未改的 `brief.md` 使用原卡；該卡仍 `pending`、`hand_pushed=true`，網站卡 ID `441c79c4-679a-4be5-8de7-e4c0e63b3a23`。本站的 brief parser 看見 **0 個可供 Jev 挑選的選項**，所以沒有宣稱網站挑案。`review-push --gate script` 送出 R10 `script.md` 卡，網站卡 ID `77c7c327-d72a-48e0-8e09-e34067dd2400`，精確內容 SHA 為上表 R10 script SHA，狀態亦是 `pending`、`hand_pushed=true`；原 R5 劇本卡已 `superseded`。這兩張卡仍須站主在網站決定。劇本卡送出時 CLI 重生的 `script.md` 位元組仍等於 R10 凍結。

對完整 R10 的 `policyRequest({doc,brief})` **只送一次** Jev：2,740 個旁白字元、213 個站主觀點字元，請求 SHA-256 `b2b35587b1a9418b0accea2d244a679b382805f253ff2efd447feb58b16a3274`。網站回 `questions=explainer`、`passed=true`；立場 `0.67`、示範不適用、建議 `0.02`、業配 `0.10`。[去憑證政策回條](review/r10-policy.json) SHA-256 `f1a7230f45b136672793e4eaca71fdaf10598b3490eba69164b8f4440518dcd7`。私有請求、預先寫下的防重送紀錄、原始回覆保存在 `/workspace/.video-work/curio-s53/review/policy-pre-tts-r10-{request,attempt}.json` 與 `policy-pre-tts-r10.json`，SHA-256 分別為 `b2b35587…`、`505eb50a…`、`5b81c1bc…`。

此前本機 `approvals.json` 已將站主常設「用推薦的決定」記作 A 案的**委派編輯選擇**。本輪在來源、正式敘事、政策 PASS 後，另把 R10 精確 `script.md` 記作同一常設偏好的**本機委派劇本選擇**，備註明列網站卡待審、只供本輪語音合成／檢查，沒有冒稱站主在網站按過核准；現行本機 `approvals.json` SHA-256 `8f914697c8f4dfbd056b133f5ebf3c04c227b45ddb1029def857e10d83c9a17b`。

## 語音與逐句檢查

`tts --dry-run` 預報 124 個場景語音請求、其中 **16 個需新合成**，其餘可從 R5 精確文字及聲音快取沿用；首輪實際為 **16 次／339 計費字元，108 個沿用**。官方 `check-audio` 每輪均覆核現稿 **126／126 句**。唯一旗標是 `s53110`：「已訪家庭」首輪被轉寫為「移防家庭」，第一輪限縮重錄被轉寫為「移民家庭」；第二輪限縮重錄後轉寫為「已訪家庭」，與原句逐字相符。兩次重錄均只送 `s53110` 一個請求，每次 19 計費字元；**本輪共 18 次新 TTS 請求、377 計費字元**，沒有修改稿件或超過兩輪限縮重錄。

| 輪次 | 新轉寫 | 逐字 | 同音／語助詞 | Jev 接受 | 旗標 | `check` SHA-256 |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| 首次 | 16 | 106 | 15 | 4 | **1**：`s53110` | `ba6dd7716a30cd91467c749594dafda8f50a6fdb2b537a7f9e28b93a2f062fbe` |
| 限縮重錄一 | 1 | 106 | 15 | 4 | **1**：`s53110` | `87f7fcb0d66b58a64d2aa9fc22193efad189423d1722e325da065a7a67988907` |
| 限縮重錄二 | 1 | **107** | 15 | 4 | **0** | `92845bf8c4c4c823d9c38b5d8889a6686b11fc91b2571ba6960e03036b996d05` |

最終 `timeline.json` 有 124 景、126 句、`speech_hash=05c4d9a79a8708b4`；其語音證據完整，`audioEvidenceProblems` 回空陣列。從第一景到正文 `s53010` 起點為 **50.33 秒**濃縮開場；從 `s53010` 至 `outro` 起點的正文為 **588.37 秒（9:48.37）**；片尾旁白 **17.07 秒**；總旁白 **655.77 秒（10:55.77）**，均按每秒 30 frame 的實測時間線計，不含尚未製作的品牌片頭／片尾動畫。最終時間線 SHA-256 `c75c8bde15f7220862ba8083d6590b7b14bb71c456f896f7b58c13352c88a054`；旁白 WAV SHA-256 `08444d50c2f8b70a7079701e157397d9a7c23d08971727164df91a1101e281e1`；零旗標清單 SHA-256 `eb7df37cdd8769f014ddea83fec720e7042900ba9516c892148e0ab32f9b7b1e`。初版、兩輪重錄的 WAV／timeline／check／flags 和受標單句 WAV 均保存在私有 `/workspace/.video-work/curio-s53/review/`；本地試聽頁為該目錄的 `audio.html`。後續已將這份精確時間線[送出網站音訊卡](review/r10-art-preflight.md)，狀態 `hand_pushed`、`pending`，沒有音訊網站核准。

**下關：**站主在網站核企劃／劇本／音訊；插圖[非付費報價與額度快照](review/r10-art-preflight.md)已備妥，付費插圖、配樂與成片仍未開始。`git diff --check HEAD -- docs/videos/curio-s53` 通過；五個凍結輸入在所有 CLI 及網站操作後未變。
