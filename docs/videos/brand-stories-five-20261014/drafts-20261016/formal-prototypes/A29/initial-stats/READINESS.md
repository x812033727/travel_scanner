# A29 正式章節轉換原型：可重建，尚不能直接匯入製作

## 結論

這是一份 **Temp 本機格式原型**。六章 JSON、逐字對照、官方合併輸出與真實 lint 結果已完成；沒有寫入主機、修改儲存庫、呼叫模型、生成媒體、寫審核 PASS 或生產 auto.json。

- 凍結稿 **65 段、2,201 編輯計數字**，轉成 **105 個有 ID 的文字片段、83 鏡**；逐段字串、UTF-16 偏移及整篇串接均完全一致。原段 ID 保存在 `mapping.json`，不把 loops 表當旁白。
- 原 **72 個插畫畫面、11 張數字／來源卡、34 個 CID、8 組懸念、三組共用圖** 全保留。插畫 prompt／camera 原字串不改，`look` 只有 `cute-mystery`，`image-01` 與繁中 `burn_in:false` 保留。
- 實跑已部署程式 `story.mjs` SHA `f9825a7ce9649111d3e49ab33a2846a8be61111dd2cb2df40db3b68b974676f3` 的 `advanceStory(..., 'script passes lint')`。初版將數字卡轉 `stats`，**正式 lint 有 11 個真錯誤**：品牌故事的 drama 格式不允許 stats。沒有刪卡、偷改為插畫、掩掉錯誤或把結果稱為通過。
- 直接呼叫現有 `shotProblems`／`storyProblems` 的窄項檢查各 0 errors，cute gate 0 errors，host lexicon 未知詞 0；這些不取代完整 lint。完整 lint 在 schema 錯誤後提早返回，因此它的 warnings=0 不表示其餘全部已檢查。
- 36 個讀取的原始檔 SHA 全部不變；原型輸出也在第二次檢查時逐一比對不變。

## 已核對的最小數字卡選項（尚未套用）

既有 `title` renderer 能原樣輸出三段文字，不需新增正式程式：

```json
{
  "template": "title",
  "data": {
    "title": "原 card.text：數字／金額",
    "subtitle": "原 card.scope：年份／分母／法律主體",
    "tag": "原 card.source：出處"
  }
}
```

`renderer-readiness.json` 對 **11 張卡**逐張保存原卡與這個建議 data，實呼叫既有 `TEMPLATE_SPECS.title.check`／`slideHtml`：schema 0 errors、產生 HTML 含全部三段原字串。**未產生像素圖片、未做字體與版面 QA，也未修改本原型六章**。

實作限制：`title` 三欄僅要求非空文字，沒有硬字數上限。title 初始 112px，最大寬 1,600px／高 400px；subtitle 46px，最大寬 1,500px／高 150px；兩者會縮到初始大小 60% 以內的下限。tag 36px，不自動縮字。必須再做實際 renderer 版面檢查，不能由 HTML 完整推論畫面已完整。

`chapter` 不適合此用途：spec 是 `title` 加可選一至兩位數 `number`，renderer 雖另讀 `subtitle`，卻不讀 `source`／`tag`，還會以章節狀態補章號。直接把來源塞 `source` 會丟失可見出處。

程式位置：`tools/video/templates/templates.mjs:84,318`；`theme.css:95`；`render/browser.mjs:61`。現有 `stats` 的 `source` 本身沒有另訂字數上限，48 字上限是 bullets／compare／steps／table 的 source helper，不能錯套到這些 title 欄位。

## 欄位映射

| 凍結分鏡 | 原型正式形狀／對照 | 保留方式與限制 |
|---|---|---|
| chapter.id/title | chapter.key/title | 六章次序與章名不變 |
| A29-SNNN | `<chapter>-NNN` | scene ID 需小寫連字號；雙向表記原 ID |
| narration_refs | lines `a29`＋四位 base36 | ID 4–8 小寫英數；每片段文字原樣，未加 say、cue 或 pause |
| paragraph_id/start/end | `mapping.lines` | 原段逐字重建、不重複、不漏字、順序固定 |
| illustrated_still | shot、visual=still | prompt/camera 完全相同，不加畫風／negative／人物綁定 |
| number_or_source_card | 初版 stats | value=text、label=scope、source=source；真 lint 拒絕，保留作失敗證據 |
| source CID 與來源 | 94 個 UNCHECKED claim rows＋完整 sidecar | 原段可能跨鏡，所以 claim 保留完整原段作上下文，並在該片段所在 scene 引用；這不是新增旁白 |
| 多來源 CID | native source=null；sidecar 保留全部候選索引、原 boundary | 12 列不自行選單一不完整出處，待獨立／實際查核 |
| CID→must_verify | 新的候選 fact index 對照 | 既有 10 項 must_verify 原值／順序不動；新 binding 待獨立覆核；T05 的兩項跨 fact 留 null（t8/t9） |
| loop 多段 payoff | native 單一終點＋完整 payoff window | setup 取原 setup 段末片段，payoff 取完整回收段落組末片段；完整原段列表、視覺回收與所有 line IDs 在 sidecar，不臆造回收 |
| image_asset_key/reuse_binding | `mapping.images/image_reuse` | 原生 shot schema 不接受此額外欄位；保留精確來源綁定要求，未假裝已有檔案 |
| worker row／series | 官方 storySeriesFile／storyCast／storyBrief | 使用 compiled stories.json 的 exact A29，含已審 reviewer_only 與 caveats；非只用未編譯 row |
| 5 秒片頭／21 秒片尾 | 外部 bookends 計畫 | 未偽造無旁白 scene；官方 defaultIntroAt=after_first_chapter；實際資產 hash、末 16 秒連結目標未設 |

所有 claim 的 verdict 均為 **UNCHECKED**。compiled plan 的既有 reviewer_only 是保留輸入資料，不等於本原型完成查核。沒有新 report、verify-1、敘事收據或腳本核准。

## 真正匯入的缺口

1. `video-story-import`／`episode_values` 只將企劃列放入 episode.beats；沒有作者章稿 payload。`draftStory` 建立空 `story.chapters`，`advanceStory` 會對 missing／written=0 章呼叫 writer。**匯入現有五集 stories.json 不會使用此完整稿。**
2. `readChapterAnswer` 是模型答案正規化器，不是作者包安裝器；它只收 shot（最後章可 outro）。hook 雖能讀取也會丟 claim ID／verdict／note；其他五章遇 stats 被拒。就算日後採 title adapter 解決 video schema，這個 parser 仍會拒絕 title。不能為了跳過 writer 任意設生產 written counters。
3. 安全採用作者稿需要單獨審核的、確定 slug／source／row／series／six chapters 哈希的安裝流程，在工作者未取件、無待決 runreceipt、STOP／lease 等現有守門下完成。需把 actual checked/listened/verified/narrative 保持待查，保留舊證據。**這次沒有設計新的主機寫入命令，也沒有宣稱已有該入口。**
4. 三組共圖在相同 prompt／camera／look／reference／seed／size 時得到相同原生 image request key；但 keyframe judge／retake 是每個 scene 各自選結果，可能選到不同 seed。sidecar asset key 不是執行期約束，仍要在實際製作時核對三組 selected file SHA 相同。不能只以同 prompt 當已共圖。
5. 原 row 的兩個 generic cast 原樣保留，凍結分鏡只指定匿名示意人物、沒有 data.characters 綁定。這會留下未使用 cast／可能產 look sheets 的取捨，應在正式採用前明確決定；本原型不擅刪 plan.cast 或把一般人物當真人。

相關未結工作已有 `tasks/open/2026-10-14-five-curio-style-brand-story-video.md`，明列正式 worker chapters 尚未完成。這次只讀搜尋沒有發現獨立的作者章稿安裝票；由 parent 在既有工作範圍記錄／拆票，避免本代理修改 repo 或重複開票。

## 時間與節奏：均非實測

- 凍結計數：2,201；官方 `spokenUnits`：2,187。差值是 **14 個 U+3007「〇」**被官方 CJK regex 漏算，並非刪字。`renderer-readiness.json` 列八個受影響原段。
- 凍結全文純口述估 528.24–574.17 秒（250–230 字／分），加既有 26 秒首尾為 554.24–600.17 秒。正文包含 hook，不含 branding。
- 原型官方 `estimateTimeline` 為 **616.767 秒正文**；hook 46.133 秒、最長鏡 9.4 秒。該值含每片段預設 300ms、前 82 鏡各 700ms、最後 1,500ms 與 frame rounding。105 片段不等於原本 65 段的說話分句，不能把 616.767 秒當成實測或保證節奏自然。
- 沒有自行加入停頓。既有分鏡要求聲音連續、切鏡只是視覺分割；正式採用要確認原生分句／鏡間停頓如何不製造不必要的斷句。不可拿預設空隙湊片長。真 TTS、發音／聽感及至少 8 分鐘正文仍待驗證。

## 檔案與檢查證據

- `chapters/{hook,origin,idea,engine,turn,now}.json`：六章候選形狀，包含尚未解決的 stats 格式。
- `series.json`／`worker-row.json`／`series-input.json`：原計畫與官方轉換結果。
- `mapping.json`：完整文字、主張、來源、懸念、卡與圖像對照。
- `synthetic/docroot/docs/videos/story-five-lego-legoland/{video.json,script.md,claims.md}`：官方程式實際合併。
- `compose-lint-evidence.json` SHA `a04b40638557078b0676aa6a535a82810b13065aa640d06bd4d2292bca96d8a1`：11 個真錯誤、0 外部呼叫。
- `renderer-readiness.json` SHA `2a891aa11551b67444f632f56615a6c387c68c50835a400c29fcbcfb205c4a00`：11 卡 title 選項的 HTML 保字檢查，沒有像素 QA。
- `input-pins.json`／`output-pins.json`：原件與第一輪輸出 SHA；後加的診斷及本報告另由 handoff-pins 記錄。

**可用範圍：供 parent 選擇 title adapter、核 source/fact/loop 對照及設計有守門的初始安裝；不可直接交工作者製作、不得視為六章查核／敘事／pilot PASS。**
