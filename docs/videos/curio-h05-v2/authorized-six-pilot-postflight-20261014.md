# H05 v2｜年代順序訂正、音訊重綁與兩鏡小樣後檢（2026-10-14）

**結論：新版敘事及音訊已對現行雜湊核准；兩張 MiniMax 圖各做一次與一次正常判圖，現圖均未正式採用。** `arrival-cabin` 只是美術方向候選，`aircraft-search` 退件；不得因此送完整 storyboard、擴批或稱成片完成。付費前快照在外部 `<home>/mokaair-work/videos/curio-h05-v2/_receipts/authorized-six-pilot-20261014T052351Z/`，原圖、manifest、帳本留在同一 v2 工作目錄。

## 更正付費前預檢的時間順序

[森林來源卡預檢](./forest-tail-siximage-preflight-20261014.md)記錄的是修改場景模板後、尚未重排年代的歷史版本。獨立盲審指出原本 `h5v063`–`h5v065` 先提 2020 年研究，卻放在 1980 年發現贖鈔的段落；故將既有 `zone-and-bank`、`distance-not-drift` 兩景移到 `h5v084`「二〇二〇年，凱伊與梅爾策發表河岸鈔票的研究」之後。新版時窗為 `h5v084` 11737–11908 格，接 `h5v063`–`065` 11908–12279 格。這是**播放順序變動**，不是新錄音。

正式 `video.json` SHA-256 `4fe70670b67e58478e1ea5abbe3f38b6bf573075cc310670994603126ac6dd76`、`script.md` SHA-256 `be7c2f06022092038ea52901aeb0b7f376a858c669d6308a7da0edc0266aca57`；`narrative_hash=d4db5dc99dea1f24`，獨立盲審第 21 輪 **11/11 PASS**。先前一次命令的證據字串格式不合要求，機械面板曾記第 20 輪 false；補齊 `[句 ID]` 與原句後才記下第 21 輪通過，不把格式錯誤說成第二次內容退件。原始新盲評與送入工具的答案在外部 `_receipts/narrative-chronology-20261014T051642Z/`。

`speech_hash` 隨順序變為 `1587d40bdeae59dd`；108 句逐句 WAV SHA 與樣本數在重排前後 **0 個改變**，`tts --refresh-evidence` 使用 102 筆快取、0 次合成。合併旁白 WAV 因播放順序而改變，不能沿用舊總檔 SHA。總長仍為 16,204 格／30 fps。正式 `timeline.json` SHA-256 `f8d106653941b3b90c9d3d6d6adf50f8bbb653bffde941073b43ce721e414468`；站主於後台聽審後，`review-pull` 在 `approvals.json` 讀回相同 SHA 的 audio 核准，時間為 2026-10-14T05:23:05.428Z。此核准只涵蓋新順序旁白。

## 兩張指定 MiniMax 圖

| 鏡頭與時窗 | 實際選圖 SHA-256 | 正常 judge | 人工實看與獨立冷看靜圖 | 本版採用 |
| --- | --- | --- | --- | --- |
| `arrival-cabin`，4918–5109 格（191 格） | `a2e978f2169281468e2b16673ae4dd82f4bbed2ebbf4735e28c455c2862968a6` | PASS，10/10 | 深色 1970 年代手繪空座與窗可作風格參考；獨立冷看指出座墊上的黃色塊讀起來像遺留物，來源並未支持。 | **暫不可採用，僅美術候選** |
| `aircraft-search`，5109–5287 格（178 格） | `0796e02c3a441e077070bb6737605b30933e482f76786402f2e0084089f306cb` | **FAIL，9.71**；`subject=0` | 實圖滿載乘客，走道另有人，窗外很亮；與夜間、乘客已離開後的空機艙搜查氛圍矛盾，也憑空具體化當時人物。 | **人工退件** |

兩鏡及相鄰來源卡尚未做正式正常速度有聲剪接；獨立冷看只驗靜圖。沒有修改正常判圖分數或門檻。`aircraft-search` 的高總分不能掩蓋必答 subject 題失敗；`arrival-cabin` 的機器 PASS 也不能代替人工來源審查。

## 帳本、比例及後續

- 付費前 US$0.189、14 image、14 judge；本輪 2 張 image 各 US$0.0035、2 次 judge 各 US$0.01，新增 **US$0.027**。付費後 US$0.216、16 image、16 judge、reserved 0；`media/ledger.json` SHA-256 `a0e126405bc555014288a633f5df75ae90a256c965d1632425521702b4116189`。`keyframes/manifest.json` SHA-256 `063869be88bc32e6e25d10a179928cc5ba8cf24744e88772dfa02eba0b119978`，其中第二鏡 `needs_review=true`。
- 目前 **規劃** 57 個 `shot` 共 8,888/16,204 格，即 54.8507%；這是模板時窗，並非已取得可用圖的比例。兩鏡現圖均未正式採用；森林來源 SVG 與片尾來源欄／CC 調整仍需完整聲畫驗證。
- 已用完本次 H05 兩鏡各一張的授權，無同鏡重抽。依重複的重大人物／來源缺陷停在小樣；保留原件與負面判圖，不送 storyboard，不做全量圖片。尚無完整渲染、正式 CC、QA、MP4、上傳包或站主成片驗收。
