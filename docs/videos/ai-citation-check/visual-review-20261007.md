# AI 引用查核：實際渲染畫面覆核（2026-10-07）

本次已完成 36 景、67 個原生靜態狀態 PNG、整張 contact sheet，以及主縮圖原尺寸和 320×180 縮小預覽的實際目視檢查。首版發現兩張比較卡有 13 個像素列进入下緣字幕保留區；root 以保留原有字句的版面修改修正後，已實際重畫並逐張覆核這兩個狀態。其餘 65 張 still、縮圖和原生時間軸的 SHA-256 完全未變。最終圖片未見文字裁切、重疊、缺字、對照錯置，或把教學示意誤標為真實模型輸出的問題。

結論為「最終靜態畫面覆核完成，可供草稿審閱」。本記錄沒有核准音訊、完整影片、上傳或發布，亦不代表站主驗收。實際播放器字幕重疊、轉場與聲畫同步仍須另行驗證。

- 檢查者：Codex `/root/preflight_consumer`。
- 檢查者曾提供八個零容量卡的版型／揭示提案；本檔是對實際渲染圖片的逐張覆核，不冒稱與所有前期設計完全無關。
- 所有渲染均在分離的私有 preview 路徑完成，沒有呼叫付費／遠端供應商。主工作票由 root 認領，本次唯一 repo 寫入是此覆核記錄。
- 本次未修改來源、圖片、音訊、字幕、原生品質紀錄或 approvals；兩張卡的來源修正由 root 執行。canonical 的 paid STOP／未知 ASR reservation 及 provider 證據没有被本次渲染或覆核改動。

## 實際渲染與完整来源版本

原先一般終端 render 因工作階段消失而中斷，留下原生影格快取；其終止碼不可查證，因此不計為成功。確認舊程序停止後，使用隱藏的 detached 程序續跑。原生命令只執行本機免費 render：

```powershell
& '<home>/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe' '<home>/.codex/worktrees/ai-citation-completion-20261007/travel_scanㄐ/tools/video/cli.mjs' render --slug ai-citation-check --workdir '<home>/mokaair-work/ai-teaching-continuation-20261007/render-preview' --channel msedge
```

首版續跑於 `2026-10-07T09:24:58.492Z` 開始，`09:28:52.705Z` 完成；worker/native PID 為 3336/1040，exit code 0、signal null、stderr 0 bytes。stdout 記錄 37 個狀態重畫、30 個沿用、67 個總數，原生耗時 233 秒。完成後逐張目視 67 個狀態，並保存首版 review、manifest、timeline、contact sheet、thumbnail、run receipts 和兩張受影響原圖；保存收據另含完整 67 張原 still 的雜湊清單。

安全區修正後的第二次 render 於 `2026-10-07T09:48:30.699Z` 開始，`09:49:29.925Z` 完成；worker/native PID 24516/38616，exit code 0、signal null、stderr 0 bytes。stdout 的實際結果為 **2 個狀態重畫、65 個沿用，耗時 58 秒**。來源前後均為 `ba96bc7d5d1cc5d6fd20172064baefabd2bb319b00ba67387b02b4e90c5e3423`。最終 manifest 的 `visual_hash=471d44f874da92e5`、`theme_hash=387c6c9767343f5d`。

完整來源版本與實際證據如下，避免把前一版紀錄當作最後畫面：

1. 原稿：`a9b9eb260a2d61a6f430fdb74e2193a6327fb3267aa7c430b39105235f8d3cd2`，已保留 exact 原檔。
2. 首次 67 狀態稿：`c1e01a5a8797445bd147606ad8ae87427c9adb9aa0f57a959474d30a01b968b0`；root 的 applied proof 記錄八個版型轉換、31 個 reveal 行変更、spoken fields／TTS plans identical、143 raw clips、stale takes 0。原始 applied proof 和 exact 來源均保留。
3. 最終安全區稿：`ba96bc7d5d1cc5d6fd20172064baefabd2bb319b00ba67387b02b4e90c5e3423`，僅把 `link-vs-proof`／`not-found` 既有 verdict 移至標題第二行並移除 data.verdict。獨立讀取前後 JSON，逐項證明所有 143 行／36 景 ID、原有 line 物件、voice、reveal、template 與其他欄位相同；還原這兩處 data 後，完整來源物件與首版相等。兩個原有 verdict 字串皆精確保留。

root 的 safe-area-proof 另記錄 actual 143 WAV SHA 未變、TTS plans identical、paid calls 0。本次直接讀到 preview 原生 timeline 的 `speech_hash=399237f659e75fc5`、30 fps、18,596 body frames 和 67 states；最終 timeline SHA 與首版完全相同。這些一致性證據不代表音訊辨識通過。

實際 preview 圖片根目錄：

`<home>/mokaair-work/ai-teaching-continuation-20261007/render-preview/ai-citation-check`

| 實際檔案 | Bytes | SHA-256 |
| --- | ---: | --- |
| `<home>/.codex/worktrees/ai-citation-completion-20261007/travel_scanㄐ/docs/videos/ai-citation-check/video.json` | 24643 | ba96bc7d5d1cc5d6fd20172064baefabd2bb319b00ba67387b02b4e90c5e3423 |
| `<home>/mokaair-work/ai-teaching-continuation-20261007/render-preview/ai-citation-check/frames/manifest.json` | 44709 | 09eb29ba7b2efb51862fd46087631a8722fa809a0dc2b1e5677518518785e4f7 |
| `<home>/mokaair-work/ai-teaching-continuation-20261007/render-preview/ai-citation-check/timeline.json` | 47060 | 3ef9c3e53d35f4192ca8207220ce2b4f0809e10cada127c20ac8a68665d841b5 |
| `<home>/mokaair-work/ai-teaching-continuation-20261007/render-preview/ai-citation-check/thumbnail.jpg` | 75742 | a8a15e09aeb263ec3b8259af9e45e76989a1d8ed4bd8d5f73292e5a66a0b91b0 |
| `<home>/mokaair-work/ai-teaching-continuation-20261007/render-preview/ai-citation-check/contact-sheet.png` | 1373661 | 2223460712ce2d076fcbdef42b0b28b6fde8a74c0d351e7f83965921b3db9464 |
| `<home>/mokaair-work/ai-teaching-continuation-20261007/visual-candidate/original-video.json` | 24329 | a9b9eb260a2d61a6f430fdb74e2193a6327fb3267aa7c430b39105235f8d3cd2 |
| `<home>/mokaair-work/ai-teaching-continuation-20261007/visual-candidate/pre-safe-area-video.json` | 24669 | c1e01a5a8797445bd147606ad8ae87427c9adb9aa0f57a959474d30a01b968b0 |
| `<home>/mokaair-work/ai-teaching-continuation-20261007/visual-candidate/safe-area-proof.json` | 901 | cc426acac1ac07298c1bd5dd2146dd53eb7e7c1741784ed2263ef349f78b27e6 |
| `<home>/mokaair-work/ai-teaching-continuation-20261007/visual-candidate/proof-applied.json` | 1719 | 232bb9ae9c50bb91ac80e9f3635d3d7b974be6fe152e2406a072d484d7d50860 |
| `<home>/mokaair-work/ai-teaching-continuation-20261007/visual-candidate/proof-applied-before-safe-area.json` | 747 | 19c7156cd904686313be221d870b0c2b1eb8223d8ebdf74eef6130aaf5c3a467 |
| `<home>/mokaair-work/ai-teaching-continuation-20261007/render-preview/safety-resume-2026-10-07T09-48-30-699Z-pid-24516/command.json` | 818 | 5171191b44cb76779e53c8c78c98689d180782584c4bab4d56f4677e8bfb43ad |
| `<home>/mokaair-work/ai-teaching-continuation-20261007/render-preview/safety-resume-2026-10-07T09-48-30-699Z-pid-24516/pid.json` | 841 | 43ce564cf504bc11584a4b0ffc545612bd6d360abe1c41a583db32eb3d2ce4a7 |
| `<home>/mokaair-work/ai-teaching-continuation-20261007/render-preview/safety-resume-2026-10-07T09-48-30-699Z-pid-24516/stdout.log` | 789 | 6100f3b85e61c2db7546c7063e9fa3185f9bb53154c8561b7c0f02a3602135b0 |
| `<home>/mokaair-work/ai-teaching-continuation-20261007/render-preview/safety-resume-2026-10-07T09-48-30-699Z-pid-24516/stderr.log` | 0 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |
| `<home>/mokaair-work/ai-teaching-continuation-20261007/render-preview/safety-resume-2026-10-07T09-48-30-699Z-pid-24516/exit.json` | 1267 | 61be4fb7c891f586fd08c3abed73a2046a9f6e6c967e03439afffda7ad988c3f |
| `<home>/mokaair-work/ai-teaching-continuation-20261007/visual-review-first-render-20261007/receipt.json` | 28573 | 1526ff46025bd961a0d93c4bb99e62df25a56a078989a7a398f1e9e97232e695 |
| `<home>/mokaair-work/ai-teaching-continuation-20261007/visual-review-first-render-20261007/visual-review-20261007.md` | 19808 | eb81d921d807278a8081cb8fb88de532bb3534b44ef700022e0acc8468723527 |

## 已目視的內容與版面

67 張 still 已在首版以 1920×1080 原尺寸逐張開啟；最終再次逐檔讀取、驗證 65 張 SHA 完全相同，並以原尺寸開啟兩張新 still，再查看更新的整張 1920×5434 contact sheet。這不是用渲染 exit 0 或縮圖取代逐張檢查。manifest 另列 682 個 transition PNG；已逐檔確認存在且尺寸 1920×1080，但没有逐張目視或以播放器播放轉場。

- `mock-answer`、`mock-purpose`、`marker-trap`、`corrected` 的「教學示意／刻意寫錯／錯誤示意／示意段落／原示意錯句」標籤可讀，錯誤內容沒有脫離其標籤。没有偽造產品聊天畫面或暗示真實產品曾輸出這些錯句。
- `real-page` 的官方頁名、`auditable` 的英文引用、apostrophe、中文說明與 Anthropic 來源標示完整可讀。本次核對的是提供的來源文字，沒有重新開啟官方頁面；source.checked_on 仍為 2026-09-27，沒有改成此次渲染日期。
- `not-found`、`paraphrase`、`weaker-words`、`certainty-scale` 的支持／不支持、原文／錯誤轉述、可能／一定、降低／消除及條件差異清楚，有文字標籤輔助，未只靠顏色區分。表格欄列沒有錯置。
- 31 個新增 reveal 的前後 still 均增加相關訊息；聊天訊息、表格列、比較欄、步驟、引用翻譯與結尾問題／行動提示没有以相同畫面冒充新狀態。最終 `answer` 的四項完整狀態沒有超框。
- 六章進度、MOKAAIR、字型、底色與強調色一致；未發現登入、key、帳單、私人通知或個人帳號畫面。
- 原生 67 個 state hold 為 3.900–14.933 秒，最長為 `link-vs-proof` 的 448 frames，超過 15 秒為 0。時間以实际 timeline 的 frame 差／30 計算，沒有以影片播放驗證聲畫同步或閱讀節奏。

首版兩張卡的結論像素分別在 y=889–930、890–930，而下緣 15% 从 y=918 起；原始 13px 例外已保存於首版 review。最終兩張卡的結論移至可讀的標題第二行，對照面板仍保持完整、沒有標題／內文重疊。讀取最終全部 67 張 PNG，在 x=96–1823、y=918–1079 的区域以三個 RGB 色頻皆 >180 檢查浅色字形像素，結果全部為 0；這輔助確認白色文字的位置，不等同實際字幕播放器驗證。

| 受影響 Scene | 首版 Still／SHA-256 | 最終 Still／SHA-256 |
| --- | --- | --- |
| link-vs-proof | frames/3cbe9ebfa6234456.png / 234b0a544444472f1fd8329c0fab16cddd95c28841f7422295b24dc259e69bde | frames/ef3101e6750ab050.png / 265680ce77d9c490fa1a098bf4a8d06e98c62a9441acca2bd77e2650d45c09cf |
| not-found | frames/9fb64a5d888a1dc5.png / 7544779bbf57b52e04dd30a8464da0132847a78a1aed14c56faa532e0624c738 | frames/b2a97d16153b98a2.png / 25de3d046b9c041b027fd2744f86f1875ac33b5c0703313334c5e32b824df148 |

主縮圖為 1280×720、75,742 bytes；原尺寸和實際 320×180 記憶體縮小預覽都已目視。主標「有連結，也可能說反」可辨，示意副標可讀，右下角只有裝飾且沒有重要文字。主標長於 visuals.md 的六字建議，但小圖可讀；本次没有製作 A/B 版。縮圖 SHA 在安全區修正前後完全相同。

manifest 的 `thumbnail_locale_gaps` 為 en、ja、ko、zh-CN；原生 stdout 說明這四份翻譯没有提供縮圖文字，沿用主縮圖。本次仅檢查主縮圖，沒有聲稱存在四份語系縮圖。

## 審查限制

本次未播放完整 MP4、未聆聽旁白、未逐張查看 682 張 transition、未驗證 YouTube CC／播放器控制列重疊、未開啟文章 CTA 或重新查證外部頁面、未上傳 YouTube，也未核准音訊／final／publish。靜態畫面可讀及 hold ≤15 秒，不能推論實際播放的聲畫同步或整體節奏已通過。原生 ASR 與人工聆聽仍應依其实际收據另行判斷；這份視覺檢查沒有補造 approvals。

## 最終全部 67 個已目視狀態的雜湊與原生停留時間

路徑相對於上述 preview 根目錄；state 為 manifest 零起始索引、reveal 保留原生值。body timeline 未額外加品牌片頭，end frame 為區間終點。

| 序號 | Scene | State / Reveal | Body frames | Hold 秒 | Still 路徑 | Bytes | SHA-256 |
| ---: | --- | --- | --- | ---: | --- | ---: | --- |
| 1 | hook | 0 / 0 | 0–386 | 12.867 | frames/a0046de14cb4b0e4.png | 458838 | 8719a6f03670165e31e10b83f06ec42b6083b4acd1fc74fb137943272edc3502 |
| 2 | mock-answer | 0 / 0 | 386–612 | 7.533 | frames/bfbc4850e60b0c85.png | 453849 | 5b3d8d5c408f60add969f2949d1815caa328419822ef78c599cfc20f1cbd5253 |
| 3 | mock-answer | 1 / 1 | 612–926 | 10.467 | frames/57434c4684f7ee36.png | 464010 | b14700a190b5cf89f12eade0be47e877a4ad6518903121ac0de5afa121505bcb |
| 4 | mock-purpose | 0 / 0 | 926–1052 | 4.200 | frames/9b93b763d9600189.png | 471107 | 52118f7e2c455cb783c7423d152d07471a13d5f9ef8f871326c30ec7b9b19e33 |
| 5 | mock-purpose | 1 / 1 | 1052–1471 | 13.967 | frames/d8a0807c92da4b30.png | 491248 | b43456e417e03c8267df038dbfaddfc54e1c901c0c8ff36faab827d42a21a500 |
| 6 | why-tricky | 0 / 0 | 1471–1867 | 13.200 | frames/efdb78005a1674c9.png | 454945 | 73eb5032e1805b011276a55b60971c287a2a4f6c61d77d63522986557dfc4e32 |
| 7 | why-tricky | 1 / 1 | 1867–1994 | 4.233 | frames/a90bf4aa3e8e3029.png | 474489 | 43f94084cc195fa6c03a6a83d8fe331e7441258170ef27e481b471c564b2ce10 |
| 8 | different-mistakes | 0 / 0 | 1994–2181 | 6.233 | frames/2832db7872700f49.png | 479634 | 25ee2b7c4b451d99490d1d387f3371370a874aef5e4277133ca568508cccef51 |
| 9 | different-mistakes | 1 / 1 | 2181–2580 | 13.300 | frames/e5cf50db73021305.png | 490844 | b446c92e9a8585cbe47b05cf6f68ac4139eaf164624ef1ac0a574f4902d5d825 |
| 10 | three-questions | 0 / 0 | 2580–3007 | 14.233 | frames/5c6eabb84a18681a.png | 404874 | 5149e276cb3e366e69b0bb23e439130293b19d45e7a5ee8ae5b655d523ef7e67 |
| 11 | order-matters | 0 / 0 | 3007–3258 | 8.367 | frames/c2200e71f7cfd7f1.png | 453799 | 4b22346fa0a9d9598ac8caba47bd09b14fafac289cde408a3e89810246fe6311 |
| 12 | order-matters | 1 / 1 | 3258–3502 | 8.133 | frames/3b678c3129a67ba5.png | 469972 | dcf47db47c36a2a0feb47ceadf1afe0da1e4b7454652578e7067fd3da62070b3 |
| 13 | open-link | 0 / 0 | 3502–3712 | 7.000 | frames/ea5aa28e28ddbdb9.png | 420285 | 214e45b371f2f31e8bf32d44815c1d2d18d4f12687907d31010e449a3c69acf1 |
| 14 | open-link | 1 / 1 | 3712–3972 | 8.667 | frames/2915c9213daa0969.png | 423561 | c130a43e37af52b8577dde1e84734bbef4cad12740bd6f3994f755ca6cb3b6b0 |
| 15 | real-page | 0 / 0 | 3972–4382 | 13.667 | frames/a48ac34739ee4c98.png | 477687 | ea1bf3bae7380f6885333ba8701e03c9233a3c0591b9144de8dfc844783ba4ff |
| 16 | page-or-summary | 0 / 0 | 4382–4731 | 11.633 | frames/7782a8ca923fe093.png | 416184 | 34b17c3f4a09fe882d02c07de1c18141d5f656742bd3a987f35e60340d700c82 |
| 17 | page-or-summary | 1 / 1 | 4731–5038 | 10.233 | frames/4c2771e25ea5a8a9.png | 420673 | 8e63c90b69a01eac5813496947e4a83ec5324544492175fbed2d9ac90d9058a8 |
| 18 | redirect-check | 0 / 0 | 5038–5294 | 8.533 | frames/928208f320de4731.png | 415614 | 18edd080e089d554772be6f51323f30e1e4aa140d62dba56052ffec089f43bc0 |
| 19 | redirect-check | 1 / 1 | 5294–5533 | 7.967 | frames/545e1ebc29895f27.png | 416183 | ac297f9856bc767dee8c54ef4c12ac9ef4c9a1030033993377aa2508bc7931b8 |
| 20 | link-vs-proof | 0 / 0 | 5533–5981 | 14.933 | frames/ef3101e6750ab050.png | 427681 | 265680ce77d9c490fa1a098bf4a8d06e98c62a9441acca2bd77e2650d45c09cf |
| 21 | claim-split | 0 / 0 | 5981–6417 | 14.533 | frames/99a04763d8efcc83.png | 465554 | 6e48ec894cdd2da0cec352c579c37ec6318b5a4628d94153c932f4137834b162 |
| 22 | one-to-one | 0 / 0 | 6417–6657 | 8.000 | frames/a81e8687df69bec4.png | 416810 | efd8c5ba8da9a93128eb5b711b5ae3a81fc712ff72c2ff1d7d695fd62d29ac1a |
| 23 | one-to-one | 1 / 1 | 6657–6956 | 9.967 | frames/60c1d9738cb98a20.png | 419941 | 46a18f6a68a0a18c425058aad689a1c38feefa57b308058a84e8d336e6f86a47 |
| 24 | marker-trap | 0 / 0 | 6956–7114 | 5.267 | frames/0496aee32bd3baca.png | 437428 | f5bd004ce6dbc89ea24f9f4d373726e155acb6640843cc6e711558667bf567f8 |
| 25 | marker-trap | 1 / 1 | 7114–7477 | 12.100 | frames/189d0d118f1fff7c.png | 441716 | 742df6c2b8991ce939032f620ecc434d1d94c5ee3d1e10df4745ebb730652331 |
| 26 | auditable | 0 / 0 | 7477–7623 | 4.867 | frames/7e6ea1d1d1bb5555.png | 491872 | 976f45eeec593f6e40af054a4d32b458e038bd3747936ed3281e679306aa8619 |
| 27 | auditable | 1 / 1 | 7623–8036 | 13.767 | frames/5cd724616734c118.png | 500954 | 71839a93430b4cf7d4544535f7a1fe22279223bd972da1c7594c8dd19117bced |
| 28 | source-function | 0 / 0 | 8036–8163 | 4.233 | frames/85c5034a7cd55242.png | 443565 | cd778a323887c54d5be2860f6c36e8fff1a2014fc270e48996955079674f126f |
| 29 | source-function | 1 / 1 | 8163–8560 | 13.233 | frames/a15ba41ad1e843c7.png | 464922 | c3b26ff9d4de2afa4abf68f716b90d1c0617de37d9646cbec1ed5c854e6d7fa1 |
| 30 | not-found | 0 / 0 | 8560–8995 | 14.500 | frames/b2a97d16153b98a2.png | 438566 | 25de3d046b9c041b027fd2744f86f1875ac33b5c0703313334c5e32b824df148 |
| 31 | missing-proof | 0 / 0 | 8995–9244 | 8.300 | frames/a2a87a54963c64f5.png | 446804 | 88666d5884b184f6ea3e87ce40ed12490ed63f82920998204525d853d04ccede |
| 32 | missing-proof | 1 / 1 | 9244–9564 | 10.667 | frames/3f488d4d20af1fcc.png | 468786 | 492c2b84cfc4b6a7ece104df2cb55f94492e9c40ffbe7539e7073ee9fd08b9c4 |
| 33 | search-method | 0 / 0 | 9564–9889 | 10.833 | frames/2a0a2b3a7cbac827.png | 423208 | ad988f737eb3a3968667c8a5b3480bc02217b5f1cc74ffc8239bb3b2e41d9854 |
| 34 | search-method | 1 / 1 | 9889–10018 | 4.300 | frames/84b83d3c91c62ccd.png | 428926 | eae2cbe7afe2a3b3b1f9df912c5103321c7dd503a0fd676476d7a381f104a961 |
| 35 | paraphrase | 0 / 0 | 10018–10135 | 3.900 | frames/1e8f3d8dc666803f.png | 415033 | aa18aaef79f78596fa9bf000d0b6a04b339c229eae5dafbce33f58f59b5cb091 |
| 36 | paraphrase | 1 / 1 | 10135–10568 | 14.433 | frames/754beb1b2b8d9dea.png | 415378 | f557c46482348ae7c4a6023164fbf126f98144fbe96d10509a267f3e62716ba4 |
| 37 | contradiction | 0 / 0 | 10568–10827 | 8.633 | frames/540d47f6de6fe965.png | 414050 | c2c6aac4e4fe9661ce45f42c29291a5d1671c1741fae915e87b28cc54286fac7 |
| 38 | contradiction | 1 / 1 | 10827–11095 | 8.933 | frames/bd3f01e065ed0475.png | 421121 | 1671de5012bf643e6f1899fcae5a06023c5289c953446fb26e1e45ee9d2d7194 |
| 39 | context | 0 / 0 | 11095–11430 | 11.167 | frames/fd72142a829fc445.png | 457258 | b3dfcb239b3314ee9179fa0603e4ac624ad36fdf949c766bb1ce7657d7488389 |
| 40 | context | 1 / 1 | 11430–11557 | 4.233 | frames/ba7976bcc3cbe345.png | 477372 | 66d2b852bd739a73f5f493034c22ee1408711e8f15d8a1f7f88d4dfc94a15d15 |
| 41 | context-window | 0 / 0 | 11557–11812 | 8.500 | frames/d4fcbf9bfbfbdb8a.png | 456235 | 052bf14017a4b2f7153532c6c24861514a1f6d815d0a8ad24bd0115a4692c802 |
| 42 | context-window | 1 / 1 | 11812–12124 | 10.400 | frames/73a6545658ee0a27.png | 469029 | d88e05566d1c79503e42af6bfe0220341c9e7cd939345977aa783aa46c706e2b |
| 43 | certainty-scale | 0 / 0 | 12124–12483 | 11.967 | frames/a981230b8c544920.png | 467465 | 3e3ede24d4964fee4444564d6e30165d424241abf81cf9461446692a7be2b86d |
| 44 | certainty-scale | 1 / 1 | 12483–12620 | 4.567 | frames/7195c9f4690eb0a0.png | 476474 | b7b882889f4be9910e02f542ea15244f30230a1a21b67d6886de1958180811f0 |
| 45 | weaker-words | 0 / 0 | 12620–12903 | 9.433 | frames/e1a24f10adca2bdf.png | 458531 | 68f0a7c16b1c87422276e0c7703ed83ef83e4970a0c302c15a0559a7dfe90cb1 |
| 46 | weaker-words | 1 / 1 | 12903–13127 | 7.467 | frames/fbb112cfba2eff22.png | 469049 | 820272b373b1b92f727daf808071f7a498f22ca951247c77e4557aff296b75eb |
| 47 | weaker-words | 2 / 2 | 13127–13278 | 5.033 | frames/ffe1b48e541782cd.png | 482719 | 6a95169d351349ecced6ba91a040afa1ceb4a8a54ee60e1e031a24f769f8020f |
| 48 | date | 0 / 0 | 13278–13519 | 8.033 | frames/6f989cefc6f758ad.png | 406304 | 2c91f9ca987349a88d3c4bc5c26749a2e54f77cd3dd382c290852c4a95f3038e |
| 49 | date | 1 / 1 | 13519–13756 | 7.900 | frames/dcc82937a6728c36.png | 413725 | a33ddac5abb32633e967a2486919369e6372d257db6f71ca975fef51523687a5 |
| 50 | timeliness | 0 / 0 | 13756–14064 | 10.267 | frames/959ed96f9fafc7d8.png | 413585 | 4d839c9133458524483158bc022b6e6f8b8343d5a8cff2f2a88ae21cb302c825 |
| 51 | timeliness | 1 / 1 | 14064–14363 | 9.967 | frames/61ffa69daa34e2f2.png | 415010 | 02c7b7492f28383953303cbba820f4da17318316a2fde1a3e9b4de364e7b4214 |
| 52 | date-and-topic | 0 / 0 | 14363–14603 | 8.000 | frames/df1f6aabd5c5b847.png | 444969 | 081b8c4160e460b20caa615e88801cebe89a3bcf3295c6d90a9a33590d830b45 |
| 53 | date-and-topic | 1 / 1 | 14603–14849 | 8.200 | frames/e87b748528c071be.png | 461363 | 4e25a9810e6658544340463d3283b3fc19a49f63848d50943f65feed961aaaf7 |
| 54 | corrected | 0 / 0 | 14849–15279 | 14.333 | frames/12ea662b22e03f80.png | 455617 | 8eb5c5ea64f3fce3fe47c7e6303d7995c7b3a32c3d271a6db29d2f00a582e8c9 |
| 55 | correction-logic | 0 / 0 | 15279–15527 | 8.267 | frames/2c8e9775f5feb667.png | 410934 | 5748471e0394f8ab400a0195a8797d78a9a42272e2dfdc02fe86f2f19aab2198 |
| 56 | correction-logic | 1 / 1 | 15527–15777 | 8.333 | frames/5081c027f3c0c289.png | 413819 | 3f178f2a2c1fedd91f3db776ea3a85f1fb2a9451ec86539756179bcf85d2b4fa |
| 57 | copy-prompt | 0 / 0 | 15777–16052 | 9.167 | frames/f7855c49c7a3bc9d.png | 471201 | d4c68827a345f38918301a4a5dbe8bc1bc6b440fee4229c7616cd63f21f88bde |
| 58 | copy-prompt | 1 / 1 | 16052–16353 | 10.033 | frames/39764ef5a38e1d96.png | 487200 | 403de9a306828edeb746e09bebabe5bfddce39231c32ee2f4898cb24caf744d6 |
| 59 | fast-routine | 0 / 0 | 16353–16638 | 9.500 | frames/3ece0299f8394e69.png | 464902 | 401b973720ff6b6c9b84b1d000ccea176f5a2a2338ac20aea489b5c6eb8d3590 |
| 60 | fast-routine | 1 / 1 | 16638–16912 | 9.133 | frames/c485c1adb9f41f48.png | 473697 | 40fbdcb4ab4ecb36286dcdb85ffca95172db7fb61b36e472b34783da4dc4c962 |
| 61 | practice | 0 / 0 | 16912–17120 | 6.933 | frames/2cbb299df8a98a6b.png | 411600 | 39de8076cf70d0f043133947146743951f0fd259e03ece0adb7fb7e91e8cea22 |
| 62 | practice | 1 / 1 | 17120–17400 | 9.333 | frames/8ef2f5f963b47c63.png | 416766 | b01b8886083e642ef9307e0fdc70320011f19c3e13c4835b50ad17c6ab1aa120 |
| 63 | article | 0 / 0 | 17400–17755 | 11.833 | frames/854c1e2bc5f5eedb.png | 456283 | 7765eda8c0e10acfdf9f0edb1a8c9cb073101f23c722a9cf6d6ad86bb4245e69 |
| 64 | article | 1 / 1 | 17755–18020 | 8.833 | frames/e7df9f978d163e2a.png | 477224 | caa169635083b5884644edd607dea52b0cc82d90622cc23de8ecb30c2ff6ecb0 |
| 65 | answer | 0 / 0 | 18020–18245 | 7.500 | frames/3f6fdfc5a5ade983.png | 460919 | e56047623b318b2e20222340f6d583373f06d3e88f8fa3a5846ad8176dfaf97e |
| 66 | answer | 1 / 1 | 18245–18449 | 6.800 | frames/883c22bc448ef936.png | 479063 | 5cb123a6515cec0dd32448c357f66498a8711dbc4f170fe9b4d3bb11f75604e5 |
| 67 | answer | 2 / 2 | 18449–18596 | 4.900 | frames/92ed6a71fc76ebd0.png | 503650 | 4572050f3adf3f85cd822872add672092fb33b53a1b17089791b610dedb720a2 |

## 補充：完成草稿影片的九張實際影格抽樣

於 `2026-10-07T10:20:36.214377Z–10:20:41.641919Z`，以本機 ffmpeg 從完成的 `final.mp4` **實際解碼取出九張影格**，並逐張以原尺寸目視檢查。這次使用成片，不是重讀 renderer 的 still PNG；沒有重新渲染、合成或變更任何媒體。成片完整 SHA-256 為 `fdc4afbcee830e7990805c89dbf0424fc067efc62d6a295abd17f66354410ca5`，91,117,107 bytes。抽取前後均重新核對成片、最終來源、timeline 和 manifest 雜湊與上列版本一致。

ffprobe 實測影片為 1920×1080、30 fps、18,596 個 video frames／619.866667 秒；audio stream 為 619.900000 秒。本成片與原生 body frame grid 相同，沒有另加 branding offset。依實際 timeline 和 manifest 的 transition 長度選取 `link-vs-proof`／`not-found` 入場，以及 `auditable` 的中文解釋 reveal，分別取切換前一格、transition 中段及 transition 後第一格。抽取採 `select=eq(n\\,5532)+eq(n\\,5539)+eq(n\\,5545)+eq(n\\,7622)+eq(n\\,7627)+eq(n\\,7632)+eq(n\\,8559)+eq(n\\,8566)+eq(n\\,8572)`，未以粗略 seek 猜測時間。ffprobe／ffmpeg 實際 exit code 皆為 0，stderr 皆為 0 bytes。

樣本、完整 argv 和未修改的抽取收據位於：

`<home>/mokaair-work/ai-teaching-continuation-20261007/actual-movie-samples-20261007T102036Z`

- `extraction-receipt.json`：SHA-256 `be37bea3580a1fa13b60bf2d13a30bfd982ed7f5136830188e10d812a7b60352`。
- `inspection-receipt.json`：SHA-256 `6abb47edd8900d30464bb3bbf8d9efe31a92e1bf8f412127b88362627f7344d9`，5,947 bytes；分別保存抽取證據與其後實際目視結論，沒有把「已抽取」當作「已看過」。

| 樣本 | 場景 | 切換位置 | 零起算成片 frame | 秒 | 私有 PNG | SHA-256 |
| --- | --- | --- | ---: | ---: | --- | --- |
| 1 | link-vs-proof | before | 5532 | 184.400 | sample-01.png | 048c043722c5f70d5103085a143e07f3861f9815e652b67102ce403a5b456d05 |
| 2 | link-vs-proof | middle | 5539 | 184.633 | sample-02.png | e26432a521eba4cb1c1127eb271a3badbd7d589ecb0046df0562815c3efd954a |
| 3 | link-vs-proof | after | 5545 | 184.833 | sample-03.png | 29c5c1d58066b7e7b7131212adb17842ebf9ec6cb665c5b94506d45853340ba1 |
| 4 | auditable | before | 7622 | 254.067 | sample-04.png | 7193d446a6135f6a4ec8e37335cbc27f196b3a1213c02db80584edcff4a59349 |
| 5 | auditable | middle | 7627 | 254.233 | sample-05.png | 0f17f2538b58bcd0a832a0cd8ab87529d1c61c6507a208a135fbd589ad2c0202 |
| 6 | auditable | after | 7632 | 254.400 | sample-06.png | 525c3ab262364e127c2bef9f68abba66aae112099cda09d1e96b305f1315d68a |
| 7 | not-found | before | 8559 | 285.300 | sample-07.png | e88210b7e963570dd23eebf0148087e6fe9886f675821276e56ecbeff4054389 |
| 8 | not-found | middle | 8566 | 285.533 | sample-08.png | c3fa9928d9acb3bafbe30843e1533be24cc2a0cb4a02d78029ef999620223c25 |
| 9 | not-found | after | 8572 | 285.733 | sample-09.png | 57853e12de42152745c81ce0ddbaa99d7e1298e38607b3c13eb7a2afe5625fb1 |

三組抽樣均未見文字裁切、重疊、空白影格，或文字侵入下緣 15% 保留區。兩張 compare 的結論保留在標題第二行，左／右「已確認／還沒確認」及「有支持／沒有支持」的區分和否定內容完整。`auditable` 的官方英文引文在前、中、後均完整；中文「讓回覆可以被查核」出現時沒有覆蓋引文或來源標示。

此結論限定上述九張成片影格。抽樣未顯示燒入字幕或播放器 CC，故只確認畫面留出字幕區，**沒有驗證外部播放器實際字幕疊放**。沒有連續播放完整影片、看完每個過場影格、聽取音訊、核准聲畫同步、上傳、發布或站主驗收。
