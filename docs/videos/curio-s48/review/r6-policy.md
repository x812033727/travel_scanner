# S48 R6｜全稿 Jev 政策與站台劇本卡

2026-10-20 16:00 UTC。先核對 R6 [獨立來源／書面畫面 PASS](r6-source-independent.md) 與[正式雙盲敘事 PASS](r6-official-panel.md)所綁的五檔 SHA。站台起初沒有 S48 row；執行 `review-push --slug curio-s48 --report-only` 後，重新讀取並確認 `category=explainer`、`format=drama`、審核卡 **0** 件。這次登記沒有送審卡，也沒有取得核准。

| 精確輸入或回條 | SHA-256 |
| --- | --- |
| `brief.md` | `7b4bc4b3f6970ac20ef9c2b9269d8a17cafacc87f2ccaf076806772b2e56ca8a` |
| `research.md` | `3d769826eff0fbfb939b35506e9eafb4166868a6c0709cb4bf234af4922dd19f` |
| `video.json` | `5d8245536c1271f6cd99b930155beb3c9532e1e0b4e1247690531282ceee9bfe` |
| `script.md` | `ddf43a0f76cef45f378d3d34c4a1050d7391eaf11bf2faf8f8f3f3f0833e3c5f` |
| `claims.md` | `4324f4a9980a2a1aaab7e85c91115c7ad43f3a9c55c79f8ab042129b76e7d3b9` |
| `policyRequest({ doc, brief })` JSON | `713cd38e2a78fe7a4ef2224062e6f9643baee4e49652da2dcf8eb10c4bd2f4b1` |
| [匿名 Jev 回條](r6-policy.json) | `3f42b9f0b98cf3cfa1e0ee11a530e17fb1051d26f58a911e713d22c1d08e4db1` |

五檔 hash 守衛、站台分類與零卡檢查通過後，對**完整** R6 旁白做了**一次** Jev `policyRequest`，不截短、不重試：正文 3,096 個 Unicode 字元，低於 60,000 上限。`questions=explainer`；Jev **PASS**：立場 **0.73**、示範不適用、建議 **0.01**、業配 **0.13**。私有原樣回條在 `/workspace/.video-work/curio-s48/review/policy-pre-tts-r6.json`；送出前的防重送紀錄在同目錄的 `policy-pre-tts-r6.attempt.json`。公開匿名回條只留檔案／請求雜湊、字數、評分與結論，不含網站權杖或請求正文。

政策通過後執行 `review-push --slug curio-s48 --gate script`。站台再次讀回 **1** 張劇本卡，`content_sha256=ddf43a0f76cef45f378d3d34c4a1050d7391eaf11bf2faf8f8f3f3f0833e3c5f`、`hand_pushed=true`、`status=pending`、`decided_at=null`；這是等待站主在 `/admin/videos` 決定，**不是網站核准**。大綱卡未提交或核准；Jev PASS 也不代替該決定、語音、插畫、配樂或成片關卡。
