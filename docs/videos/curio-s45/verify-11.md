# S45｜R7 片尾政策窄修與站台狀態：作者凍結送審

2026-10-20 UTC。**此為撰稿者自查，不是 R7 的獨立來源／書面畫面覆核、兩位全新敘事盲讀或政策 PASS。**R6 精確來源／書面畫面已在 [verify-9.md](verify-9.md) 判 PASS；兩位全新讀者對 R6 在 [verify-10.md](verify-10.md) 為 12/13 與 13/13，沒有共同必答 No，敘事 PASS。R6 任何口播修訂都需另凍結、重審。

| R7 凍結輸入 | SHA-256 |
| --- | --- |
| `research.md`（未改） | `97b91f2344190fbc424fd29eca17da2bee372673bdc7fd36e7161e13ef31ab65` |
| `brief.md`（未改） | `e4a75c2afb0ad4a5070fb3d49fec186b95946fc31e9d3ed2a2bf72fe916c6437` |
| `video.json` | `0d66e204647c4d80e1a1f72a5797308152640650c5a4cd1c576c36d42f99bb21` |
| `script.md` | `410e003181e831f21f68815446a70df6265a591f56d13e59cae51eae38a8534f` |
| `claims.md` | `979c8275f480433565dcd69affde37916eeed72f120fd78d4c9cf8c515bccfcb` |

## 政策收據與原因界線

首次用上述 **R6** 精確企劃／劇本形成 `policyRequest({doc, brief})`，正文 2,715 字元，`request_sha256` `0d55a53d3059ba18c1bafc2f51dbd2cae9fa5a4a2794cafef17adab534378fe9`，一次向站台 Jev 詢問。因 S45 當時**尚未登記為站台影片**，後端 `apps/api/app/video_automation/judge.py` 的 `policy_questions_for` 按不存在／未分類的 `VideoProject` 預設為 `tutorial`，回覆 `stance .76 / demo .12 / advice .02 / sponsored .29 / passed false`；[完整匿名回條](review/r6-policy-before-site.json) SHA `7026aecb81c796f125e812383d7095f67e051235467088da10737914bcff6264`。`video.json` 當時及現在均有 `category: explainer`；`policyRequest` 本身只送 `{slug, script, viewpoint}`，站台以**資料庫類別**選題組，不是稿件分類文字。第一次失敗是先後順序造成的提問錯類，不可當成內容政策 PASS。

後送站台大綱時，站台才產生 `category: explainer, format: drama` 的 S45 row。確認此 row 以後，對**同一 R6 request hash** 再做一次不同題組的有效檢查；回覆 `questions: explainer / stance .75 / demo null / advice .02 / sponsored .35 / passed false`，業配分數高於 .30 門檻。[完整匿名回條](review/r6-policy-categorized.json) SHA `edc243b106736b38a48151dfa6321374937c651f455fb4a0abd877ad717738b7`。Jev 沒指出是哪一句引發分數，不可斷言原因。**R6 政策 FAIL，不啟動付費 TTS。**

R7 只將片尾 `bly999c` 的口播「想繼續沿原文看歷史故事，訂閱奇聞檔案局。」改成「原著固定版連結在說明欄，方便對照她自己的敘述。」；連結實際已列於 `video.json.youtube.description`。`outro.data.cta` 仍是畫面的「訂閱奇聞檔案局」，既有 21 秒 `v4-endscreen` 和最後約 16 秒的可點位置規劃未改。這是**降低可疑推銷語氣的一個可測窄修**，未聲稱已知 Jev 的因果理由。99 景正文、日期、史料引文、查核界線、音色、來源及 A/B 大綱均未動；`claims.md` 僅同步更正片尾說明。

`node tools/video/cli.mjs script --slug curio-s45` 已重新生成同版 `script.md`。`lint` 是 **0 errors、1 warning**：片尾口播不說「訂閱」；本輪保留畫面 CTA，因此明示此 warning，沒有為消警告重新加入被政策懷疑的口播。99/99 正文旁白在 `script.md` 和 `claims.md` 同 ID 列逐字一致、99/99 列有固定 1887 年原文 commit 行號；96/99 正文景是插圖，17 條 `loops` 順序合法。估時計算在 300 spoken units/minute 開場 40.40 秒、正文 **492.00 秒（8:12）**、純劇本 548.80 秒（9:09）；250 為開場 46.97 秒、正文 573.47 秒（9:33）、純劇本 639.67 秒（10:40）。均未經實際語音量測。

## 站台及媒體狀態

`review-push --gate outline` 把**未改的** `brief.md` SHA `e4a75c2a…` 送站台，Jev 推薦 A（1.00，stance .89、demo 不適用、advice .02）。站台回覆本片沒有 `auto.json`，所以 review `hand_pushed: true`；`review-pull --gate outline` 為 **pending / waiting for the owner**。`review-push --gate script` 亦將 **R6** `script.md` SHA `a30602d0…` 送上，回覆 `hand_pushed` 與 **pending**；這不是 R7 劇本卡，也不是任何站台核准。站主的既有「用推薦的決定就好不用問我」授權，只在本地 `approvals.json` 留下**代理選 A** 的 `outline` 雜湊核准註記，明說站台仍 pending；R7 的 script 本地核准尚未記錄。待 R7 所需獨立覆核後，應送新版站台劇本卡並如實拉回狀態，再記本地代理核准。

R6 `tts --dry-run` 唯一媒體預檢：Gemini `Sulafat` ready，102 requests／102 待合成，約 2,515 可計字元（0.5% 免費層），站台當時顯示當月尚餘 8,624,038 字元。**dry-run 未合成、無支出**；R7 尚未下付費 TTS、插圖、配樂、站台最終審核、組片或發布。

R7 接下來需要**另一位工作者**對片尾文字與描述連結做獨立來源／書面畫面差分覆核，另請**兩位從未讀此稿或其審核的讀者**對 R7 精確 `script.md`／`video.json` 做官方十三題盲讀。通過後才對 R7 的**新**精確政策 request 作一次 Jev 檢查，再決定旁白付費階段；R6 舊分數與舊讀者裁決不得挪用。
