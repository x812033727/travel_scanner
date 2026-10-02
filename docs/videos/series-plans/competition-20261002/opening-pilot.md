# 《喜宴未散，清算開始》E1 前 60 秒優化開場

狀態：**新改寫台詞／planned 前製草稿；未 TTS、未生成畫面、未測時、未經母語聽校。** 本文件與 `opening-lines.json` 是競賽選片後的開場提案，不是原始 `source.mjs` 引句或已核准的 `video.json`。未修改來源劇情或製作設計，也未發出付費生成請求。

目標是讓觀眾先看到「簽字後被拋棄」的死局，再在 planned 30 秒內看到她停筆、撕展示副本、保住自己的決定權。planned 30–60 秒由退婚戒承擔拒絕的代價，再用原件仍在桌上收住；不靠提前揭密增加刺激。

## 來源與本次調整

來源為 `../binge-five-20260928/wedding-reckoning/source.mjs` 的 `setting.rules`、`setting.opening_30_seconds`、E1「這次不簽」，以及同目錄 `production-design.json` 的 `opening_30s`、角色聲線、look states、E1 與音訊限制。來源物件雜湊為 `37328fa1c643e0edfcd1d138a158410653b36d6e02739ce7a9c555b26bc5bb9c`。

- 保留前世南主門／火光 → 現世婚禮重生 → 拒簽撕展示副本。開場旁白只說知棠親歷的死亡與重生，沒有新兇手、新證據或全知情報。
- 將既有「看原件、拿副本、撕紙」拆成獨立鏡頭。撕紙時雙手只操作展示副本，原件留桌；不用同一鏡頭再要求第三隻手按原件。
- 在婚禮威脅後拍拿戒、歸盒、退盒三個動作，明確區分顧家準備的新娘婚戒與後續她自費購買的男方婚戒。戒指未交換、未戴上，婚禮與登記均未完成。
- 完整未簽原件含附件，始終留婚宴廳中央簽署席的遠端；碎展示副本留近端。拍頁碼／取得另存完整副本仍留 E1 後半，原件封存留 E2、向許聞交付副本留 E3。
- 知夏、未送禮袋、母親聲音、錄音筆、舅舅、新調查者均不入本段。E1 後續事件仍按原稿發生，不刪掉，也不提前揭露。

## 拍攝與剪輯契約

沿用倉庫既有 profile：Gemini `veo-3.1-lite-generate-preview`、1080p、16:9、24 fps，每次原片 8 秒；實際供應能力、價格與服務可用性由開拍前檢查核對。每片一個主動作、一種攝影意圖，剪取 2–8 秒動態有效素材。下表為 **planned edit windows**，15 片原始素材合計 planned 120 秒，不含重試；不能因此宣稱已取得 60 秒成片。

不使用 `referenceImages` 或 extension。可先準備核定首格／末格；臉部與逐鏡服裝由人工及既有品管核對。靜態 animatic 只用來預演，不當成正式動態鏡頭。缺秒時改稿或重剪，不凍結、慢播或插無意義停頓。

現世知棠全段使用 `zhitang-bride-veiled`；前世只用 `zhitang--base` 褲裝。承川固定 `chengchuan--base`。知棠 28 歲、承川 31 歲；入鏡賓客僅成年背景人物且沒有新增對白。知棠在畫面左、承川右，中央桌軸線不跨。每個 look 的完整外觀沿用已登錄資料，同臉、同髮型、同一只銀色方錶，不在掌上、桌上或另一人物身上複製配件。

| shot id | planned 秒 | 單一主動作 | 逐鏡 look | 台詞 id |
| --- | --- | --- | --- | --- |
| S01 | 00–05 | 固定中近景可辨完整臉、褲裝肩胸與握筆手；手指收緊一次。 | zhitang → zhitang--base | L001 |
| S02 | 05–10 | 承川嘴角的笑意收起。 | chengchuan → chengchuan--base | L002 |
| S03 | 10–15 | 握筆手輕抖後穩住，筆尖不接觸紙。 | zhitang → zhitang-bride-veiled | L003 |
| S04 | 15–18 | 左手食指沿原件一個既有頁碼滑過。 | zhitang → zhitang-bride-veiled | L004 |
| S05 | 18–21 | 知棠將筆放到原件旁的桌面。 | zhitang → zhitang-bride-veiled | L005 |
| S06 | 21–23 | 知棠拿起薄的展示副本。 | zhitang → zhitang-bride-veiled | 無台詞 |
| S07 | 23–26 | 雙手把展示副本撕開一次。 | zhitang → zhitang-bride-veiled | 無台詞 |
| S08 | 26–30 | 完整臉部、婚紗與頭紗可辨；將碎展示副本放回桌面近端。 | zhitang → zhitang-bride-veiled | L006 |
| S09 | 30–35 | 承川收起現世的禮貌笑容。 | chengchuan → chengchuan--base | L007 |
| S10 | 35–39 | 從托盤拿起新娘婚戒。 | zhitang → zhitang-bride-veiled | L008 |
| S11 | 39–43 | 將新娘婚戒放回戒盒。 | zhitang → zhitang-bride-veiled | 無台詞 |
| S12 | 43–47 | 將裝著戒指的盒子推到承川側桌位。 | zhitang → zhitang-bride-veiled | 無台詞 |
| S13 | 47–52 | 食指輕點碎頁上的展示副本字角一次。 | zhitang → zhitang-bride-veiled | L009 |
| S14 | 52–57 | 左手掌輕按完整原件邊緣。 | zhitang → zhitang-bride-veiled | L010、L011 |
| S15 | 57–60 | 承川目光從戒盒轉向未簽原件。 | chengchuan → chengchuan--base | 無台詞 |

完整構圖、鏡頭意圖與文件位置見 `opening-lines.json` 的 `shots`。S01–S02 門已關閉，只看知棠親歷的門內外，不生成加鎖或縱火操作。S01 固定中近景同框保留知棠完整臉部、象牙白褲裝的肩胸與握筆手，讓 S08 現世婚紗加頭紗的臉有可核對的前世畫面；只做握筆收緊，不增加鏡頭、預算或傷勢。S03 用剪輯硬切完成重生，不要求模型在一片內把褲裝變婚紗。S04 指過既有頁碼只是認出文件，沒有拍照、換頁、取得副本或發現新證據。

S07 的撕紙音落在無台詞窗，婚宴鋼琴同時停止；S08 開口前撕聲已收尾。S11 戒指入盒留短促碰聲，S12 推盒用桌面摩擦與室內底聲承接，不能以音效尖峰製造台詞聽不清的假衝擊。S15 的目光回到未簽原件只留下他仍在意授權的懸念，不提前播 E1 結尾「附件別給外人看」。

## 四語逐句草稿

全 id 固定前綴 `WR-E01-`；下表省略前綴方便閱讀。聲音窗是供試錄安排的 **planned reservation**，不是字幕時碼。每語各自測時、母語聽校後才能產 SRT/VTT；不可複用繁中的時間碼。文字也不是對嘴驗收結果。

`zhitang` 沿用 Gemini **Kore**、`chengchuan` 沿用 **Puck**。`narrator` 用來源 `setting.world.narrator` 提案的 **Erinome**；它是產線保留的 `speaker: narrator`，不新增到 `characters[]`，不能與角色共用聲線。三者全是候選 casting，尚未試聽。日韓英先試同一角色聲音身份，不合口音／年齡時另留 casting 版本，不能把名稱相同當作已驗收。

| line id / speaker | planned 聲音窗（秒） | 繁中 zh-TW | 日文 ja | 韓文 ko | 英文 en |
| --- | --- | --- | --- | --- | --- |
| L001 / narrator | 0.2–4.8 | 上一世，她簽了字，再也沒能走出這扇門。 | 前世、この署名が彼女を死に追いやった。 | 전생에 그녀는 서명 한 번에 목숨을 잃었다. | In her past life, that signature led to her death. |
| L002 / chengchuan | 5.2–9.5 | 字簽了，妳也就沒用了。 | 署名した時点で、お前の役目は終わった。 | 서명했으니, 네 쓸모도 끝났어. | Once you signed, you were no use to me. |
| L003 / narrator | 10.2–14.8 | 再睜眼，她回到婚禮，還沒簽字。 | 気づけば、署名前の結婚式に戻っていた。 | 눈을 뜨니, 서명하기 전 결혼식으로 돌아와 있었다. | She was back at her wedding, before she had signed. |
| L004 / chengchuan | 15.1–17.8 | 棠棠，簽了就好。 | ジータン、署名するだけだよ。 | 즈탕, 서명만 하면 돼. | Just sign it, Zhitang. |
| L005 / zhitang | 18.2–20.8 | 這份授權，我不簽。 | この委任状には署名しない。 | 이 위임장엔 서명 안 해. | I will not sign this authorization. |
| L006 / zhitang | 26.1–29.8 | 媽媽的公司，不拿來陪嫁。 | 母の会社は、嫁入り道具じゃない。 | 엄마 회사는 혼수가 아니야. | My mother’s company is not my dowry. |
| L007 / chengchuan | 30.2–34.6 | 不簽，這婚就別結了。 | 署名しないなら、この結婚はなしだ。 | 서명 안 할 거면, 결혼도 없던 일이야. | If you will not sign, the wedding is off. |
| L008 / zhitang | 35.2–38.5 | 那婚禮就到這裡。 | じゃあ、式はここで終わりね。 | 그럼 결혼식도 여기까지야. | Then this wedding is over. |
| L009 / zhitang | 47.2–51.4 | 撕掉的，只是展示副本。 | 破ったのは、展示用の写しだけ。 | 찢은 건 전시용 사본뿐이야. | I only tore the display copy. |
| L010 / zhitang | 52.1–54.4 | 原件留在這裡。 | 原本はここに置く。 | 원본은 여기 둘 거야. | The original stays here. |
| L011 / zhitang | 54.6–57 | 表決權，我不交。 | 議決権は渡さない。 | 의결권은 안 넘겨. | My voting rights stay mine. |

情緒、用語護欄、候選人名讀法與固定術語均逐條放在 JSON。知棠拒絕時收住呼吸、用正常台灣句速，不靠吼叫；承川的前世冷淡與現世親暱必須仍聽得出同一人。日文現世催簽用親近語氣，前世蔑視才用較冷的「お前」；韓文兩人對話使用親近關係的非敬語，旁白採敘述語氣；英文保持短句，不把授權誇成賣掉整家公司。四語這些安排都須母語聽校才能鎖版。

繁中「展示副本」、日文「展示用の写し」、韓文「전시용 사본」、英文「display copy」只指不含附件的展示份。`L010` 的「原件／原本／원본／original」指畫面中完整未簽原件，不能指被撕的那份。`L011` 的「表決權／議決権／의결권／voting rights」不能譯成公司所有權。

## Veo prompt 例句

以下是逐鏡 prompt 草稿，**未送出生成**。每例獨立請求 8 秒，`prompt` 管單格構圖、`motion` 只指定一個動作、`camera` 固定一種意圖。角色外觀應由核定 look 完整帶入；文件上的「展示副本」及頁碼由後製在實體道具表面追蹤合成，逐格校字，不相信模型生字。對白、旁白與翻譯全部為可關閉 CC。

**S01／前世門內，planned 剪 5 秒**

```json
{
  "character_looks": {"zhitang": "zhitang--base"},
  "prompt": "Locked medium close-up inside the already closed south main door of the old warehouse. The approved adult East Asian woman, age 28, has her entire identifiable face, the shoulders and chest of her ivory tailored trouser suit, and her pen-holding hand clearly visible together in one frame. Preserve her approved facial identity for comparison with the present-time bridal face in S08. Her hand already holds one intact metal signing pen near the closed door. Flickering firelight is reflected on the pen and the cold door frame; flames never touch her body. No wedding gown, veil, or new injury.",
  "motion": "Her fingers tighten once around the pen.",
  "camera": "Locked medium close-up keeping her full face, trouser-suit shoulders and chest, and pen-holding hand visible together."
}
```

**S07／撕展示副本，planned 剪 3 秒**

```json
{
  "character_looks": {"zhitang": "zhitang-bride-veiled"},
  "prompt": "Oblique overhead close-up at the central wedding signing table. The approved adult bride, age 28, wears the same ivory wedding gown and veil. Both hands already hold the thin unsigned display copy above the near edge. One separate complete unsigned original with its attachments lies intact at the far edge, fully visible and untouched. Exactly two hands, one display copy, one original. Leave the paper label area blank for tracked prop typography in post.",
  "motion": "She tears the thin display copy once with both hands.",
  "camera": "Locked oblique overhead close-up."
}
```

**S12／退回新娘戒盒，planned 剪 4 秒**

```json
{
  "character_looks": {"zhitang": "zhitang-bride-veiled"},
  "prompt": "Medium close-up of the central signing table, keeping the bride on frame left and the groom's table position on frame right. The bride's ring is already inside its open ring box. Torn display pages remain near the bride; the complete unsigned original remains at the far edge. No ring is worn on her fingers. Approved wedding gown and veil remain unchanged.",
  "motion": "The bride slides the open ring box to the groom's side of the table.",
  "camera": "Locked medium close-up."
}
```

Veo 原生音訊棄用；角色乾聲、旁白、音效／環境、音樂各存獨立 stem。不能把「不要原生說話」寫進 prompt 就宣稱配音已對嘴。此版使用手部、越肩、反應鏡承接對白；若生成可見嘴型，須另驗同步或重構鏡頭。

## Pilot 驗收與修改出口

1. **先實錄 zh-TW。** 試錄以上三聲線與 11 句，量每句與呼吸；中文初版正常句速若超窗，先精簡或調剪輯。重排後再確認前 5 秒鉤子與 30 秒內拒簽撕紙，沒有量測就維持 pending。
2. **拍前做 timed animatic。** 配上實際中文音訊，關 CC 也要辨識前世 → 婚禮、她拒簽的是授權、撕的是展示副本、完整原件未毀。若不清楚，先修構圖／台詞，不先加解說字卡。
3. **優先驗證 S06–S08 與 S10–S12，再組全段。** 審兩手接觸、紙張阻力與撕後狀態、戒指實際進盒及推盒重量；逐格查原件不被撕、不變多份、戒指不瞬移。每片只有一個主動作，剪接前後物件位置相合。
4. **造型／年齡／方位。** 用 S01 的完整臉部／象牙白褲裝肩胸，對照 S08 的現世完整臉部／婚紗加頭紗，實際核對同一張臉；兩鏡都須清楚可辨，不能用手袖特寫代替換裝同臉驗收。S01 保持固定中近景、握筆收緊一個主動作，無新增傷勢；28／31 歲成年人。人物左右、門方位、銀方錶唯一性、原件與碎頁桌位均連續。沒有妹妹禮袋、母聲或新增證據。
5. **中文聲音與 CC。** 單聲道和手機外放能分旁白／知棠／承川；撕紙和音樂不蓋關鍵字。CC 可關，開啟時人名、說話者、否定與道具詞正確，跟隨實際音軌；聲音描述也只進 CC。
6. **再做 ja／ko／en。** 先母語校稿，再各自試音／正常速度測時／對齊／CC 和播放器驗收。維持同一核定畫面主版；先修語句、再在允許窗口內調節，不硬加速。漫劇多角色配音目前仍屬 `planned-not-implemented-for-drama`，本逐句表不冒充已可自動四語交付。
7. **通過才放量。** 保存所採臉部、look、聲線、台詞及鏡頭版本；記每次生成 job 與成本，遵守既有重試／預算上限。這份稿本不構成無上限重拍授權。通過實測小樣也不等於全片、四語或 YouTube 上架已完成。

目前驗收表：zh-TW TTS／聽校／CC pending；ja／ko／en TTS／母語聽校／CC pending；15 片動態素材與 60 秒實際剪輯未生成；對嘴未驗收。製作媒體應輸出至 repo 外，版本化台詞與檢查紀錄可留此資料夾。
