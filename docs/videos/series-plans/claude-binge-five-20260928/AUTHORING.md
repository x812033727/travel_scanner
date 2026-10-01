# 作者契約：一部作品的 `source.mjs`

每部作品一個目錄，只編輯 `source.mjs`（`export default` 一個可 JSON 序列化的物件）；其餘檔案由 `node build.mjs <slug>` 產生，不要手改。一部的來源太長時可以拆成幾個模組（例如 `setting.mjs`、`chapter-1.mjs`…`chapter-4.mjs`、`packaging.mjs`），由 `source.mjs` 匯入後組成同一個物件；一次寫入的量控制在一篇十集以內，免得撞到單次輸出上限。寫完跑 `node validate.mjs <slug> --source-only`，零錯誤才算完成；警告要看過，能改就改。所有中文用台灣的繁體與用語；人名讀起來要像台灣國語裡自然的名字。

## 結構

```js
export default {
  series: {
    slug, title,                       // slug 與目錄同名；title 是作品名（不是 YouTube 標題）
    logline,                           // 一句話賣點，≤ 60 字
    premise,                           // 故事前提，200–600 字：誰、出了什麼事、她／他有什麼、要什麼、誰擋著
    note,                              // 給產線的備註 ≤ 2000 字：不做的事、尺度、畫面基調
    genre,                             // rebirth-revenge | system-game | urban-return | empress-rise | custom
    lead,                              // female | male | dual-male
    tone,                              // no-romance | hetero-leads | dual-male-leads-subtext
    aspects,                           // [] 或 world/bonds/structure/mood 的子集合
  },
  setting: {
    world: {
      era,                             // 時代與地理一段話（哪一年、哪座城、什麼規模）
      places: [{ id, name, description }],   // ≥ 3；id 小寫英數 2–24 字；description 寫固定辨識物，讓每集畫面一致
      factions: [{ name, wants, hides }],    // ≥ 2：每個勢力想要什麼、隱瞞什麼
    },
    rules: [text],                     // ≥ 4 條硬規則與代價：能力怎麼用、用了付什麼、什麼不可逆
    characters: [{                     // 6–12 人；主角排第一（雙男主兩個都是 role: "lead"）
      id, name, role,                  // role: lead | support | antagonist
      age,                             // 「27 歲，安養院夜班照服員」這種一句
      appearance,                      // 英文、≤ 800 字元、ASCII：年齡、體型、臉、髮型、衣著顏色、一個標誌物；每集逐字沿用
      voice: { provider: "gemini", name, style },  // name 是 Gemini 內建聲音（Sulafat 留給旁白）；style 台灣國語的語氣指示
      personality, want, fear, secret, speech,     // speech 是口頭禪或說話習慣，一句話
      relationships: [{ with: id, kind }],
      looks: [{ id, from, to, appearance, sheet_prompt, voice_style }],  // 可省略：某幾集換的樣子與聲音，見「換裝與變化」
    }],
    mysteries: [{ id: "m01", question, answer, planted, advanced: [], revealed, reserved: false }],
                                       // 8–12 條；planted/advanced/revealed 都是集數；answer 是確定答案
    tone, imagery,                     // 語氣（一段）；畫面（攝影機愛什麼、色彩、絕不拍什麼）
    naming: [text], never: [text],     // 命名規則 ≥ 2；不做的事 ≥ 3
    lexicon: { "名詞": "讀法或 null" },  // 每個角色的 name 都要有一筆；多音字、罕見字給讀法
    ending,                            // 確定的結局一段：主線怎麼收、反派下場、代價、最後一個畫面
    cold_open: [{ seconds: "0–5", picture, audio }],  // 第 1 集前 30 秒，≥ 4 拍：第一句就是鉤子
  },
  chapters: [{                         // 正好 4 篇，每篇 10 集
    number, title, theme, stakes, question, start_state, end_state, turn,
    episodes: [{
      number, title, logline, timeline: "present" | "past",
      hook,                            // 一句能直接說出口的台詞或旁白，≤ 28 字（不含標點），全劇不重複
      hook_type,                       // question | danger | image | line | reversal
      conflict,                        // 本集要解決的衝突，具體動作與因果
      turn,                            // 中段轉折：誰的認知被改變
      cliffhanger: { type, text },     // type: danger | reveal | choice | reversal | emotion；相鄰集不同型（跨篇也算）；第 10/20/30/40 集用 reveal 或 reversal
      satisfaction: [{ beat, type, text }],  // ≥ 2；beat: opening|first_half|midpoint|second_half|ending，第一個在 opening 或 first_half；
                                       // type 是爽點 id；text 寫觀眾看到的那個畫面或那句話（≥ 8 字）
      lead_arc,                        // wins | suffers | mixed；不能連兩集 suffers
      setups: ["m01"], payoffs: [],    // 謎團 id；埋下要在該謎團的 planted 或 advanced 集，回收要在 advanced 或 revealed 集；任何連續 4 集至少一個 payoffs
      tension: [4, 3, 5, 3, 5],        // 五拍各 1–5，不能全同，最後 ≥ 4
      characters: [id],                // 2–4 個具名角色
      locations: [id],                 // 1–2 個場景
      theme,                           // 主題句
      carry,                           // 下一集必須繼承的事：情報分布、傷勢、道具在誰手上
      world_flip: true,                // 只有一集（第 18–22 集之間）：翻轉世界觀那一集
    }],
  }],
  packaging: {
    titles: [3 個],                    // 依題材的標題公式，≤ 100 字，不含角括號；三個是 A/B 測試的三個方向
    description,                      // 說明欄本文 ≤ 1200 位元組：前兩行說這是什麼、給誰看；不劇透結局
    tags: [],                          // 含 漫劇、AI漫劇、一口氣看完；合計 ≤ 500 字元
    thumbnails: [{ id: "A", headline: "≤12字", tag: "≤6字或 null", composition, episode: 1–3, scene, promise }],  // 3 組
    audience, visual_identity, music, pinned_comment,
    why_million: [text],               // ≥ 3 條：為什麼這部有機會破百萬（鉤子、搜尋詞、留存設計、分享點）
  },
  continuity_notes: [text],            // ≥ 3 條跨集注意事項
};
```

爽點 id：`face_slap` 打臉、`identity_reveal` 身份揭露、`counter_kill` 反殺、`level_up` 升級、`first_clear` 首殺／首通、`betrayer_punished` 背叛者遭報、`villain_humbled` 反派低頭、`hidden_power` 藏拙露鋒、`public_vindication` 當眾平反、`rescue` 及時救場、`reversal` 反轉。

## 每一集怎麼寫才緊湊（這是產線量的東西）

- 第一句就是鉤子：沒有片頭卡、沒有「上回說到」、沒有氣氛鋪陳。鉤子是一句話或一個畫面，說得出口、≤ 28 字。
- 10 秒內衝突成立，30 秒內第一個爽點；每 20–30 秒一個情緒節點（一句刺人的話、一個眼神、一個反轉、一個威脅）。
- 爽點與麻煩交替：爽完立刻來更大的麻煩。每集至少兩個爽點，類型盡量不同。
- 最後 5–10 秒就是懸念，之後沒有任何總結、感想、「下集」。
- 每集 2–4 個具名角色、1–2 個場景、一或兩個事件的轉折；不重述前情。
- 主角不能連兩集只挨打；每篇賭注高過上一篇；第 18–22 集之間一次翻轉世界觀的揭露，讓觀眾重新理解前面看過的東西。
- 每篇最後一集的懸念要改變觀眾對本篇某件事的理解（reveal 或 reversal）。
- 情感線只用動作與物件，不點明（`tone` 說什麼就照什麼）。
- 對白短而利：旁白負責速度，角色負責刀。

## 集名與包裝是公開的，不能說破

合輯每一集是 YouTube 的一個章節，章節名就是「第 N 集〈集名〉」，40 個集名在說明欄一次列出，觀眾開片前就看得到（`tools/video/core/compilation.mjs`）。標題候選、縮圖文字、說明欄、置頂留言也都公開。所以這些文字只給懸念，不給任何謎團的答案、第 18–22 集的翻轉、篇末的揭曉或結局；說破答案的句子留在集內的台詞。篇名目前不公開，也照同樣的標準寫。

## 固定外觀（appearance）只寫不變的樣子

產線把 `appearance` 原文接進每一集每一個鏡頭的生圖提示詞，不帶集數（`tools/video/media/look.mjs` 的 `sheetPrompt`、`tools/video/media/keyframes.mjs` 的 `shotPrompt`），一部作品每位角色只有一張設定圖。所以：

- 只寫整部都不變的：年齡、體型、臉、髮型、基本衣著、不離身的辨識物。
- 不寫集數、時間先後（later、at first、after episode…）、場合條件（in hospital、only during…）、別的角色名字；`validate.mjs` 會擋集數與時間字眼，其餘靠覆核。
- 會出現、消失、易手或改變的衣物與道具（外套、徽章、輪椅、病人服、信物…）不寫進去；寫進下一節的 `looks`，或（只是某一鏡多一樣東西時）在 `continuity_notes` 逐集寫清楚在誰身上、哪一集換手或消失，由該集的鏡頭提示詞加上去。
- 例外：幾乎每場都帶在身上、觀眾靠它認人的小物件（念珠、手錶）可以留，只寫物件本身、不寫動作條件；離身的那一拍寫進 `continuity_notes`，那幾拍用構圖避開。

## 換裝與變化（`looks`）

角色在連續幾集換了樣子（脫下制服、坐輪椅、穿病人服、婚紗只穿前三集）或換了說話方式（中風後），寫在那個角色底下的 `looks`。產線開始一集時，涵蓋這一集的 look 取代基底的 `appearance`（與給了的 `sheet_prompt`、`voice_style`），設定圖畫一次、站主核准一次，它涵蓋的其他集沿用（`docs/videos/SERIES.md`「換裝與變化」）。

- `id`：小寫英數 2–24 字，同一角色內不重複，例如 `no-coat`、`wheelchair`。
- `from`、`to`：集數，含頭尾；沒有 `to` 就到第 40 集。同一角色的兩個 look 不能涵蓋同一集。
- `appearance`：那幾集**完整的**外觀，規則同基底（英文、ASCII、≤ 800 字元、不寫集數與時間字眼）；不是「基底再加什麼」，生圖模型每一鏡都整段讀它。
- `sheet_prompt`、`voice_style`：可省略；`voice_style` 是那幾集台詞的 Gemini 語氣指示，取代基底的 `voice.style`。
- 同一集之內的變化（同一場戲裡老了幾十歲）不是 look：另立一個角色（例如 `lin-old`），那一集兩個都列進 `characters`。
- `validate.mjs` 用產線送設定集前的同一個檢查（`documentProblem`）擋形狀錯的 look。

## 原創與尺度

世界、人名、勢力、系統、物件、情節一律原創；不得使用任何既有作品讓讀者認得出的東西，也不用真實企業、政府、軍隊、朝代人物、真實遊戲。不說教、不血腥、不性暗示、不羞辱女性。旁白台灣國語，字幕繁中。
