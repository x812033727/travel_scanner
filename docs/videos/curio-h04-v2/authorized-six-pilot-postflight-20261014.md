# H04 v2｜授權六圖中的兩鏡小樣後檢（2026-10-14）

**結論：兩張 MiniMax 圖與兩次正常判圖已完成，沒有重抽；兩張現圖都未正式採用。** `tent-opening-question` 只保留為美術方向候選，`model-paper-card` 因來源與場景錯誤退件。這不是完整 storyboard、50% 可用插畫或成片核准。本輪的原圖、裁圖、manifest、帳本及付費前快照留在外部 `<home>/mokaair-work/videos/curio-h04-v2/`，付費前快照目錄為 `review/authorized-six-pilot-20261014T052257Z/`。

## 綁定與音訊

- 正式 `video.json` SHA-256 `6c7cd3d3a48c7fa03ba01122fb72601548867eb0faa09fc2ecde0dc507fa34dd`；`pictures_hash=615be7c0e501c98c`。來源圖卡及兩鏡規格見[付費前預檢](./formal-sourcecard-pilot-preflight-20261014.md)。
- 場景結構變動使 `narrative_hash=5152905cd2a5ac0b`；新獨立盲審 11/11 PASS，外部 `review/narrative.json` 記為第 23 輪。預檢曾估計台詞不變便可沿用舊審查，實際沒有這樣做。
- `tts --refresh-evidence` 只重建時間軸，0 次新合成、99 次快取沿用；付費前後 100 句逐句音訊 SHA 與樣本數比對均相同。正式 `timeline.json` SHA-256 `12b18320ed0e246b25ace3ea844f55bbc91f17374e95bc87c85fe1d2bd9b6790`，`approvals.json` 已讀回同一 SHA 的 audio 核准，時間為 2026-10-14T05:21:52.675Z。這項核准只涵蓋音訊。

## 四項判定分開記

| 鏡頭與預定時窗 | 原圖／實際選圖 SHA-256 | 正常 judge | 人工實看與獨立冷看靜圖 | 本版採用 |
| --- | --- | --- | --- | --- |
| `tent-opening-question`，143 格 | `3f5e7367f571f3ff4a6f7b4ec7bb1b83629eac0e7724817672895700fee0edf2`／`37f10d595db128c3ca70a0d304ea90e9d024b75bd505f3e06b83ef87c6ba2f17` | PASS，9.29；judge 自己指出斜角、規整掀起的布片不符正面窄裂口 | 2D 形式可當插畫方向；布片形態比來源允許的提問更具體，且畫面沒有「情境插畫／非證物復原」標示。冷看只驗靜圖，未驗剪接。 | **暫不可採用，僅美術候選** |
| `model-paper-card`，231 格 | `103223e67786440246ce2f2a4e37a20aa5d6ec8f6622f2d64a9e2f2ef392d914`／`e1747b612f94183d523e5135ea1297c083cebf458442016a2bba783b104d643a` | PASS，9.29；judge 的 details 題已指出帳篷與樹木 | 實圖有黃色帳篷、針葉樹和大片雪板，偏向具體事故現場，超出只解釋 2021 年抽象模型的來源界線；獨立冷看同意退件。 | **人工退件** |

機器 manifest 對兩張都記 `needs_review=false`，只表示其判圖流程通過，**不是人工畫面採用**。沒有改寫 judge 分數、門檻或舊收據。獨立冷看只看選圖靜格；正常速度的有聲剪接與播放器字幕均未驗。

## 帳本與下一關

- 付費前帳本 US$2.879、215 張 image、213 次 judge、reserved 0；本輪增加 2 張 image（每張 US$0.0035）及 2 次 judge（每次 US$0.01），合計 **US$0.027**。付費後 US$2.906、217 image、215 judge、reserved 0；`media/ledger.json` SHA-256 `6e5124c45c346dbac212a31293d1a4463ecf816df0c062b44402d81f25142127`。當前 `keyframes/manifest.json` SHA-256 `33eac1b08869c5f8f16f8627043804d863fb6eb8f134d01913733f8e954af304`。
- 現行分鏡按核准音檔分配 7,935/15,827 格 `shot`，即 **50.1358% 計畫時窗**，僅比門檻多 21 格。`model-paper-card` 的 231 格現圖已退件；不能把未通過的圖算作完成的插畫比例。來源標示在單一 `shot` 中也尚無經驗證的正式呈現方案。
- 本輪授權每鏡一張已用完，停止 H04 這個小樣分支的付費生成；不重抽、不擴批、不送 storyboard 核准。後續若重設來源安全的鏡頭，須重新核算 50% 與雜湊、實看新圖和字幕，再走正式關卡。沒有完整渲染、CC、QA、MP4、上傳包或站主成片驗收。
