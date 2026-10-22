# S53 R29｜`s53025` 成年職員與一年期限概念圖獨立紙審

2026-10-22 UTC。**PASS，限史料與書面畫面；未審第二張實圖。**本審查不是 R29 作者。固定對象為 commit `2c15fd2340558707b348b432439be55061351518` 的 `video.json` SHA-256 `2d2191c6a66ae253f4ce9d167babb364729134c4e56244b68723cce1b091a59a`、`claims.md` SHA `98726486a0dc99c3920f9f5a2cfb39fd021d6407a73041b2a2e3beb0779aba7a`、未改 `script.md` SHA `64ffcd8c0e89c4596a7fd08d41bd74f8a16f55fbc9acc2f41d7f9b914ea300fc`。未修改任務、Git、私人圖單或媒體，沒有付費呼叫。

## 史料及書面畫面

重新打開固定 `/tmp/s53-sf-relief/56217-0.txt`，SHA-256 `d627ed287d8a93b9c00225ea47dbdc4f97c36089a890192a602b993c3c185b72`，與 [`research.md`](../research.md) 一致。[1913 年 *San Francisco Relief Survey* G L4934–4941](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L4934-L4941)說救濟機構就公園、廣場詢問公園委員會；委員會無權正式授權，於 **1906 年 8 月 17 日**同意最多一年不干預使用，之後小屋應盡快移走。`s53025` 原旁白「委員會無權正式准許，只同意從那年八月起一年內不干預」在此界線內，並未聲稱取得正式許可。

[R28 首張原圖](r28-s53025-native-independent-visual.md) SHA `a83746167bb2c899f7643c7e66344297ed26e22b3568d168540469aab8840448` 已由作者及非作者 HUMAN REJECT。我再次看 1280×720 原圖：左下是清楚的現代平面螢幕，右側職員童貌，巨大牆曆只有亂筆，沒有可辨公園草圖；機器雖 9.29／10 PASS，其 `details=7` 也指出現代螢幕。R29 改為桌面近景、灰髮有面紋且未戴帽的成年職員、桌上小張**無字十二格一年期限紙條**及旁邊**無字公園／廣場地塊草圖**，背景限素牆、單一窗與灰色日光。這些是針對 R28 時代、年齡、景別、牆曆和缺圖問題的具體改寫；`look` 仍只有 `cute-mystery` preset。

十二格只能當「最多一年」的**原創視覺比喻**，不是一月到十二月的實際公告，也不是現存日曆、會議紀錄、地圖或正式許可證。R29 的 `claims.md` 已明示紙條、草圖是概念示意；提示詞不要求簽字、官印或可讀文字。桌面、匿名人物及其動作也不是來源證實的歷史現場。下一張若畫成現代螢幕、童貌、具月份的曆本、正式批准文件或缺少公園地塊草圖，仍須依原尺寸實圖退件；書面 PASS 不預判模型會遵守。

## 精確差分及安全狀態

獨立核對 [R29 可逆差分](r29-s53025-adult-calendar-structured-diff.json) SHA **`fea84a2a9b88a36815b6b909aef46006aeb3e8dc344ee751319a0454e8b235f1`**：新 prompt 與 `claims.md` 同列各精確反填一次，即逐位元組等於 R28 commit `92d60cf5b`，分別重得 `video.json` SHA `458d3391180cff7b57abe2081eba956b711d9572a18f7acbf59c1a185c6a9b1c`、`claims.md` SHA `87a5b5d15e0e2e73bc14b1160b66017f6617f746fdbf76401eae4fc5dc5900c7`。124 景僅 `scenes[19]` 的 `s53025.data.prompt` 不同；其他 123 景與 **126／126 句口播 ID／文字**不變，該景 `camera=pan right`、`visual=still` 不變。`node tools/video/cli.mjs lint --slug curio-s53 --json` exit 0，**0 errors、0 warnings、126 lines**。現稿 `visualHash=7374825e2bdc1744`。

只讀檢查有效私人 `keyframes/manifest.json` SHA `14cf3ce74ed6d6bbd075e77b4d78af48523bcb65f1d2a3517dbbd2a28a5e9726`：16 張 KEEP 的實檔 SHA 逐一符合所選條目，對這 16 景的 `keyframeProblems` 為空；沒有 `s53025` 退件條目。manifest 仍綁 R27 `visual_hash=018662cfba7a270f`，**尚未綁 R29 現稿**。`media/ledger.json` SHA `a5ba3579536d2d683a36422d1440edf8a16845d45d990e036389099cc1f42727`，合計 US$0.5535／42 image／41 judge／0 預約，低於整集 US$4.78；`media/jobs.json` SHA `a9d2c69ab3cb5704417b4f0968a7d8d0dae6eb0e35d37e053463220b30d55ca3`，jobs 空，`STOP` 在位。語音 `timeline.json` SHA `c75c8bde15f7220862ba8083d6590b7b14bb71c456f896f7b58c13352c88a054`、`narration.wav` SHA `08444d50c2f8b70a7079701e157397d9a7c23d08971727164df91a1101e281e1` 未變。本紙審不構成實圖 KEEP、完整分鏡、網站關卡或成片核准。
