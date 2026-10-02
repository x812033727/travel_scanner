# 十部漫劇配音與製作細節覆核（2026-10-02）

本輪重查十部／400 集的聲音、分鏡、物件材質、角色知情與音源位置。
95 名角色維持跨集固定聲線，各劇旁白另選；這些都是 casting 候選，尚未實際試聽。
已修正設計與原文不符之處，補 55 個表演狀態、50 組聲音提示、23 個接戲試音場面。
原故事來源與舊審稿收據不改；本報告不核准付費生成或上架。

## 已修正的具體問題

| 作品／位置 | 修正與實作意義 |
| --- | --- |
| 婚禮／杜淑雲 | 設計中的淑改回台灣二聲 shú，與來源字典一致。[教育部](https://dict.concised.moe.edu.tw/dictView.jsp?ID=35368&la=0&powerMode=0) |
| 三針／沈亦微 | 微改成台灣二聲 wéi；原字典只提示姓氏，新增完整讀音補充，確實進到 TTS metadata。[教育部](https://dict.concised.moe.edu.tw/dictView.jsp?ID=43426&la=0&powerMode=0) |
| 列車 E13 | 紅廣播催門、白燈報號是同一聲線的不同台詞，各錄一段；不能把兩句視為同一檔案。 |
| 列車 E14／E19 | E14 三次問話指定完全同一 take；E19 由唐綺記錄編號，程望核對兩項證據後叫媽，避免主詞誤配。 |
| 死對頭 E1–2 | 早期追捕令是蓋印的紙本，改紙張／指節落石聲；E26 的繼承令牌另保留硬材質。 |
| 城市 E31 | 父女留訊與回訊改為訊息画外朗讀及鎖定畫面，避免拍成即時雙向電話。 |

## 聲音細節與試音材料

每部 `production-design.json`／`production-review.md` 記錄來源定位。
`performance_states` 規定受傷、煙嗆、虛弱、老化與情緒改變時的氣息和語尾，保留同一角色與 voice。
設定中原有 `looks[].voice_style` 仍依集数生效，沒有被新的基礎 casting 蓋掉。
無法說話的鶴亭以無可辨詞的呼吸／手寫及指定旁白處理；思思是 19 歲成年弱聲，不配成嬰兒。

`audio_cues` 明列錄音、廣播、訊息朗讀、敲擊、倒數、歌詞與音源視點。
同聲線不同台詞、同句不同表演、同一 take 重播分別處理；母親舊錄音及受損／修復衍生版保留來源關係。
必要線索不能被雨、車、火與配樂蓋住；配樂不能另造類似敲擊或倒數的假線索。
這些仍是聲音計畫，尚未自動生成或混入所有情節音效。

新版離線試音計畫包括平靜、低聲、反轉、孤立人名、字典別名／術語、實際逐集有效聲線、每個表演狀態及明確歸屬的原句。
來源敘述只當排戲語境；只有人工指定、可逐字對回來源且有說話者的台詞才送作故事片段。
無聲狀態沒有文字合成參數。所有材料都標 `not-synthesized`，校準句不得加入故事。
預設音色的年齡、性別、口音與辨識度須實聽選角，不能僅靠長段表演指令宣稱已符合角色。
[Gemini 官方語音文件](https://ai.google.dev/gemini-api/docs/speech-generation)

## 製作工具修正

- `pronunciation_hints` 使用設定的來源字典與已列明補充，只有當句命中詞才進 Gemini style。
  拼音／注音不是台詞，CC 原字不改；讀音更正會更新語音請求與時序雜湊。
  超過 400 字明確拒絕，避免靜默截斷必要指示。
- `audio_ref` 只引用前文未引用的原始 line，檢查 speaker、唸法與有效 voice。
  新來源合成後核對 WAV 格式並保存 SHA256；重播複製同一份 bytes，不另呼叫合成。
  各次重播仍有獨立 line id、停頓與 CC 落點。來源損壞或缺少雜湊會停止，不能暗中多付費重錄。
  重拍同一 take 的任一重播會重拍其來源一次並更新整組。
- 後台設定 Markdown 附錄加入角色姓名、中文讀音、聲音狀態、聲音線索、逐集 sound／voice_notes／cc_notes。
  單集 writer 只收到該集適用的聲音狀態及提示。

WAV 完整性檢查不代表人耳或 ASR 已驗收。後續仍須實際聽審、量時及觀看。

## 中文與後續語言

先完成 zh-TW、台灣口音與可開關 CC；正片不燒對白字幕。
中文主版核准後才做日／韓／英，各自選角、配音、量時與 CC，不把中文混音墊在外語人聲下面。
人聲、旁白、環境／音效、音樂分存，Veo 原生人聲排除。
四語多角色的完整產線仍有待實作及驗收，這次沒有生成任何外語音軌。

## 驗證與待驗收事項

```text
node tools/video/cli.mjs production-check
node tools/video/cli.mjs production-build --out test-results/ten-drama-voice-review-current
node --test tools/*.test.mjs "tools/video/**/*.test.mjs"
node tools/tasks.mjs check
```

離線設計檢查、兩批來源／產生檔驗證與聲音契約測試通過；整套工具 1,224 通過、0 失敗、2 個既有環境跳過，結果見 [offline-evidence.json](offline-evidence.json)。
修改到的五個片長審核綁定另經獨立增量覆核，沒有放寬任何片長門檻；原報告／收據保存在本目錄的 `duration-review-before.*`。
更嚴格的 Codex `--require-reviews` 仍指出婚禮／列車的舊全文審稿來源雜湊過期：
由已合併 PR #1095 的造型／聲音設定更新造成，不能將舊收據改 hash 冒充新的全文覆核。
另留 [source-review-delta.json](source-review-delta.json) 的獨立差異證據；新後台文件仍須正式待審程序。

實際聲線自然度、兒童聲年齡感、同場辨識、歌唱、情節 SFX、混音、對嘴、動畫小樣與整片觀看仍未驗收。
六部有未成年人物／兒童入鏡路徑待驗，不能宣稱 400 集已能直接用 Lite 全量製作。
百萬點閱是目標，不是這輪文字或工具檢查能保證的結果。

後台已追加十部的 v3 待審文件，共 60 份；v1／v2 共 120 份歷史文件保留原樣。
逐份正文與正常後台 serializer 的版本／雜湊皆符合，唯讀重放十部都為 unchanged。
同步結果與歷史保留檢查另記 [backend-verification.json](backend-verification.json)；未在登入瀏覽器驗畫面。
工具程式在草稿 [PR #1122](https://github.com/x812033727/travel_scanner/pull/1122)，本輪未部署 runtime、未試音、未生成或發布。
