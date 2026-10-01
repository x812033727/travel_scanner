# 五部合集的文件契約

此批只編寫原創製作企劃；不呼叫網站、不開拍、不產生付費素材、不上傳。故事與結局以站主於 2026-09-28 核定的五部企劃為準。數字代表規劃，不是已測得的成片時間或觀看成績。

各作品目錄只由被分派的作者編輯 `source.mjs`，`export default` 一個可 JSON 序列化物件。共用 `build.mjs` 產生給人閱讀與供產線使用的檔案。不要自行編輯生成檔。不得省略中間集數、用一樣的句子換人名，或將未發生的素材生成、試聽、發布標示通過。

## source.mjs 結構

```js
export default {
  series: {slug, title, premise, genre, lead, tone, note},
  setting: {
    world: {place, period, conflict_engine, factions: [{name,want,secret}], visual_language, narrator},
    rules: ["完整世界規則與不可撤銷代價"],
    characters: [{id,name,role,age,appearance,personality,want,fear,secret,speech,
      voice: {provider:"gemini",name:"...",style:"台灣國語；..."},
      relationships:[{with:"character-id",kind:"關係與改變"}],
      // 可省略：某幾集換的樣子與聲音，見「必須符合」的 looks 一條
      looks:[{id:"no-coat",from:28,to:37,appearance:"那幾集完整的英文外觀",voice_style:"可省略"}]}],
    locations:[{id,name,description}],
    mysteries:[{id,question,answer,planted:1,advanced:[4,8],revealed:12,reserved:false}],
    naming:["命名規則"], never:["禁止事項"], lexicon:{"人名":"讀音"},
    ending:"確定結局與代價", opening_30_seconds:[{seconds:"0–5",picture:"...",audio:"..."}]
  },
  chapters: [{number:1,title,theme,start_state,end_state,turn,stakes,question,episodes:[{
    number:1,title,logline,timeline:"present",hook,hook_type:"danger",
    conflict,turn,cliffhanger:{type:"reveal",text:"具體收尾"},
    setups:["m01"],payoffs:[],tension:[4,3,5,3,4],
    characters:["lead-id","other-id"],locations:["location-id"],theme,
    lead_arc:"mixed",satisfaction:[
      {beat:"opening",type:"reversal",text:"此集具體回報",planned_seconds:22},
      {beat:"second_half",type:"rescue",text:"第二個不同的具體回報",planned_seconds:120}],
    state:{time:"故事時間",knowledge:"各方知道或不知道甚麼",character_state:"傷勢、關係與狀態",evidence:"道具或證據持有者",carry_forward:"下集必須承接甚麼"},
    // 僅第 40 集設 true；收尾可用 reversal 兌現早期物件或關係，不另開懸案。
    closed_ending:false
  }]}],
  packaging:{titles:["三個已核定方向"],description:"不劇透結局的完整繁中介紹",tags:["..."],
    thumbnail_variants:[{id:"A",headline:"12字內",composition:"人物、物件、對比",episode:1,scene:"前三集實際存在的畫面",promise:"兌現點"}],
    audience:"...",visual_identity:"色彩、材質、場景辨識",music:"配樂進退",release_order:1,
    pinned_comment:"討論問題，不要求觀看或留言換獎勵"},
  continuity_notes:["跨集特別注意事項與創作補完理由"]
};
```

## 必須符合

- 正好四篇、每篇十集、全季 1–40 不缺漏；忠於已核定 40 集事件。
- 每集 hook 是可直接說的一句話，建議 20 個中文字內；不把整個分鏡段落塞進 hook。
- conflict、turn、收尾各有具體行動與因果；logline 不只重複標題。每集至少兩項具體 satisfaction，第一項規劃 30 秒內（只有計畫，之後需以 TTS/成片驗證）。
- hook_type: question|danger|image|line|reversal；lead_arc: wins|suffers|mixed。
- cliffhanger.type: danger|reveal|choice|reversal|emotion，相鄰集不同（包括篇章交界）；10/20/30/40 集使用 reveal 或 reversal。40 集為已完成的情感翻轉，不作續集預告。
- satisfaction.type: face_slap|identity_reveal|counter_kill|level_up|first_clear|betrayer_punished|villain_humbled|hidden_power|public_vindication|rescue|reversal。
- 每集 2–4 個具名出場角色、1–2 個主要場景；全部 ID 已在設定集登記。群眾、工作人員可以無台詞背景呈現。
- 8–12 條長線 mysteries；`planted`、`advanced`、`revealed` 與 episodes.setups/payoffs 對得上。setups 可以是首次埋下或 advanced 排程內的新線索；可以在 advanced 集數付出局部答案，但不可冒稱終局揭曉。文字說清回收了哪一部分，所有謎團在結尾已回收，沒有保留續作。
- 任意連續四集至少一項 payoffs，包括跨篇；不能連續兩集只有 suffers。tension 五個 1–5、不能全相同、末值至少 4（結局可以是情感濃度）。
- 每位角色英文 appearance 800 字元內，具備穩定髮型、衣著、輪廓與辨識物。產線把它原文接進每一集每一個鏡頭的生圖提示詞、不帶集數（`tools/video/media/look.mjs`、`keyframes.mjs`），所以只寫整部不變的樣子：不寫集數、時間先後（later、at first、after episode…）、場合條件或別的角色名字，validate.mjs 會擋集數與時間字眼。會出現、消失、易手或改變的衣物與道具不寫進去：連續幾集換了樣子寫進該角色的 looks，只是某一鏡多一樣東西才在 continuity_notes 逐集寫明、由鏡頭提示詞加上；幾乎每場都帶在身上、觀眾靠它認人的小物件可以留，離身那一拍寫進 continuity_notes。聲音是擬定 casting，未試聽，先使用現有 Gemini 名稱如 Sulafat、Kore、Aoede、Charon、Fenrir、Puck、Orus、Zephyr，正式開拍先核對主機聲音池。
- 角色在連續幾集換了樣子（脫下外套、剪斷紅繩、坐輪椅、病人服、婚紗只穿前三集）或換了說話方式，寫在該角色的 `looks`：`id` 小寫英數 2–24 字、同角色不重複；`from`／`to` 是含頭尾的集數（沒有 `to` 就到第 40 集），同一角色兩個 look 不能涵蓋同一集；`appearance` 是那幾集完整的英文外觀（規則同上一條，不是在基底上加減）；`voice_style` 可省略，給了就取代那幾集台詞的 `voice.style`。產線開始一集時用涵蓋它的 look 取代基底，設定圖畫一次、站主核准一次，之後沿用（`docs/videos/SERIES.md`「換裝與變化」）。同一場戲裡的變化（老了幾十歲）另立一個角色 id。validate.mjs 經由產線的 `documentProblem` 擋形狀錯的 look。
- setting 規則先補完已核定企劃留下的因果空隙，不能改掉人物、主要事件、結局。例如「第七個活人」必須明確成立；失憶仙俠需明確規定抹除範圍與紅繩毀後不再使用守淵之力的解法。
- 集名、標題候選、縮圖文字、說明欄、置頂留言都是公開文字：合輯每集是一個 YouTube 章節，40 個集名在說明欄一次列出，觀眾開片前就看得到（`tools/video/core/compilation.mjs`）。這些文字只給懸念，不給謎團答案、中段翻轉、篇末揭曉或結局；篇名照同樣標準。
- metadata、縮圖為文案與構圖規格，沒有現成圖片；完整台詞、TTS、影片、五語字幕檔另屬媒體製作，不能偽造完成。

## 五個目錄與作者分工

1. wedding-reckoning — 喜宴未散，清算開始；rebirth-revenge/female/no-romance。
2. seventh-passenger — 末班車上的第七個活人；custom/male/no-romance。
3. scapegoat-empress — 朕不是你們的替死鬼；empress-rise/female/no-romance。
4. city-owes-a-light — 這座城欠他一盞燈；urban-return/male/no-romance。
5. remembered-by-rival — 世人忘我，死敵記我；custom/dual-male/dual-male-leads-subtext。

共同值由 build.mjs 注入：total_minutes 120、target_minutes 3、planned_episodes 40、episodes_per_chapter 10、compilation true、open_ended false、visual_tier hybrid、style_preset cinematic-3d。建立請求 JSON 不含衍生的 chapters；文件檢查 job 另加 chapters:4。不會因本機建檔觸發工人。

## 獨立編輯查核紀錄

查核者不得審自己的作品。先讀完整 source 與 user 核定計畫，實質問題傳回作者修正後重新讀差異。只可編輯被指派的 `reviews/<slug>.json`，不可修改別人的 source。

格式：`{slug, reviewer, author, evidence_type:"independent-editorial-review", source_sha256, scope, limitations, documents, open_findings:[], resolved_findings:[]}`。

- `source_sha256` 用 `hash(await loadSource(slug))`（從本目錄 build.mjs 匯入），綁定實際審過的版本。
- `scope` 寫明已讀設定集、40 集與包裝；`limitations` 明說未看成片、未實測留存、未作全網同名或法律權利查核。
- documents 正好有 setting、outline、chapter-01、chapter-02、chapter-03、chapter-04 六個鍵；每個值照 `verifier-series-doc.md` 含 `{verdicts, similar_works, problems, notes}`。verdicts 鍵與既有 REQUIRED_VERDICTS 相同，值為「有」「弱」「無」。
- `resolved_findings` 每條含 `{issue,resolution,episodes}`；沒有具體問題就空陣列，不編造問題。
- notes 說實際閱讀判斷，不能只複製同一段「全部通過」。若有缺陷，open_findings 與 problems 留下，先修再過。
- 這不是正式站 judge 核准記錄，也不寫進送審文件當作已批准；現有線上裁決仍要走自己的規則。
