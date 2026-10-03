# 喜宴未散，清算開始｜繁中試音與 15 鏡剪輯計畫

## 故事前提

重生回簽字前的知棠，在婚禮中央桌拒絕交出表決權；撕展示副本而完整原件仍留桌，退回新娘婚戒。原始來源與完整 15 鏡在 edit-plan.json；voice-only.video.json 僅供 11 句繁中 TTS 測時，不可直接 assemble 成完整 pilot。

## 角色

沈知棠 28 歲，Kore；顧承川 31 歲，Puck；第三人稱旁白 Erinome。角色外觀、聲線與所有命名造型沿用 source/production-design 經既有 productionSetting 的結果。前世褲裝、現世婚紗加頭紗；詳見 series.json 與逐鏡 character_looks。

## 站主觀點

先做繁中台灣口音、繁中 CC 與畫面；日／韓／英必須等完整繁中全片及完整可開關 CC 交由站主本人確認後才啟動；中文 pilot、代理審查或自動品管通過均不能代替此關卡。本輪只做 zh-TW，不生成或花費任何外語 TTS／CC／配音。只用正常句速驗證聲音與行為，不為湊 planned 60 秒加假旁白、重複台詞或假發聲。原始劇情、完整副本取得與其他人物揭密次序不動。

## 執行狀態

此資料夾由前製代理交付可驗證工作稿；前製代理沒有呼叫 TTS 或生成媒體。實際試錄由主代理另行執行，最新結果以 repo 外的 WAV／時間軸／收據為準。聲音稿故意只含 10 個有聲 scene；S06/S07/S11/S12/S15 的無聲動作鏡保留在 edit-plan.json，等待真實逐句 WAV 後另行對時剪輯。不可把 voice-only 產出的 timeline.json 當作完整動畫時間軸。

## 檔案分工與已知工具限制

- `voice-only.video.json`：現有 `validateVideo`／`lint` 可接受的 10 個有聲 scene、11 句 zh-TW；只供 TTS 和逐句聽校。不是完整 15 鏡影片，不對它跑付費 clips／assemble。
- `edit-plan.json`：完整 15 鏡、planned 60 秒，原片各 8 秒；S06／S07／S11／S12／S15 是獨立無對白動作鏡，不產 TTS、不產對白 CC。這是 editorial schema，不是 `video.json`。
- `id-map.json`：保留原始 `WR-E01-Lxxx` 到隨機 8 字元 runtime line id 的固定映射；往後改措辭也不更換 id。shot ids 轉小寫，以符合既有 scene schema。
- `series.json`：本地的 source-bound cast、named look catalogue 與 clip profile，讓試音稿的 lint 能核對人物與 8 秒素材限制。沒有修改全域 production profile，也沒有啟用全域 drama worker。

現有 `core/schema.mjs` 強制每個 scene 有非空 `lines[]`，`core/timeline.mjs` 按台詞迭代建立 scene；因此不能以 `lines: []` 保存獨立的無聲鏡。`pause_after_ms` 只延長同一個有聲 scene，不能新建 S06 等動作鏡。把「撕紙聲」或空白當台詞、讓 TTS 再念一遍、塞假發聲都會破壞聲音／CC，這份交接沒有這樣做。共享 schema／timeline 正有其他工作，本輪不改工具，也不輸出聲稱可 lint 的完整 15 鏡 `video.json`。

聲音稿每句保留正常的 300 ms 句後停頓；現有 pipeline 另在 scene 尾加 700 ms、最後一個 scene 尾加 1500 ms。這些是聲音檢閱軌的既有排法，**不是 planned 60 秒畫面剪輯**。三個試音章節只是讓現有 lint 的章節契約成立，沒有生成或加入片頭／章節卡。真正逐句 WAV 已去掉這些組軌用 padding，請直接量其 sample count。

角色的 `appearance`、`voice` 與完整 `shot_looks` 透過既有 `productionSetting` 自原始設定與 `production-design.json` 產生，再逐字帶入；沒有改臉、年齡、角色 id 或造型描述。S09 越肩構圖實際看得到知棠的肩與頭紗，所以除承川也列知棠及 `zhitang-bride-veiled`。試音稿必填的 `look.preset/style` 是前製視覺候選，不等於已核准或生成的風格樣片。

## 繁中試錄指令

從 repo 根目錄執行；`--workdir` 是 repo 外的媒體根目錄，實際會再加上 `wedding-reckoning-pilot-voice-zh-tw/`。TTS 與 check-audio 都接受 `--file`，不用把試音稿冒充正式集數搬到 `docs/videos/<slug>/video.json`。

```bash
node tools/video/cli.mjs lint --file docs/videos/series-plans/competition-20261002/pilot/voice-only.video.json --json
node tools/video/cli.mjs tts --file docs/videos/series-plans/competition-20261002/pilot/voice-only.video.json --workdir /workspace/wedding-competition-media --dry-run
```

主代理核對 dry-run、既有額度與本輪範圍後，去掉 `--dry-run` 才是真正付費試錄。只重做被標記的 line ids，保存 cache 與 WAV SHA-256，未知結果先查 job／cache，不能盲目重送。

```bash
node tools/video/cli.mjs check-audio --file docs/videos/series-plans/competition-20261002/pilot/voice-only.video.json --workdir /workspace/wedding-competition-media
```

以上 `/workspace/wedding-competition-media` 是指令示例，並非聲稱媒體已在此處。若主代理採不同 media root，所有後續步驟保持同一個 root；不碰金鑰檔、不將 token 寫入命令或版本庫。`check-audio` 的辨字結果不等於台灣口音、表演、音色和聽感已由人驗收。

## 固定台詞映射

聲音窗仍為 planned；本表不是 SRT，也不是實際 WAV 時長。日韓英原草稿仍保留在上層 `opening-lines.json`，本地沒有外語 TTS 或 CC 輸出。

| original id | runtime id | speaker | planned 聲音窗（秒） | zh-TW |
| --- | --- | --- | --- | --- |
| WR-E01-L001 | `afd1ed57` | narrator | 0.2–4.8 | 上一世，她簽了字，再也沒能走出這扇門。 |
| WR-E01-L002 | `0c782990` | chengchuan | 5.2–9.5 | 字簽了，妳也就沒用了。 |
| WR-E01-L003 | `0945b87f` | narrator | 10.2–14.8 | 再睜眼，她回到婚禮，還沒簽字。 |
| WR-E01-L004 | `c1ee7ed5` | chengchuan | 15.1–17.8 | 棠棠，簽了就好。 |
| WR-E01-L005 | `677ac0bc` | zhitang | 18.2–20.8 | 這份授權，我不簽。 |
| WR-E01-L006 | `a390c745` | zhitang | 26.1–29.8 | 媽媽的公司，不拿來陪嫁。 |
| WR-E01-L007 | `6a480238` | chengchuan | 30.2–34.6 | 不簽，這婚就別結了。 |
| WR-E01-L008 | `548a5cb2` | zhitang | 35.2–38.5 | 那婚禮就到這裡。 |
| WR-E01-L009 | `087d01cb` | zhitang | 47.2–51.4 | 撕掉的，只是展示副本。 |
| WR-E01-L010 | `b9acfedc` | zhitang | 52.1–54.4 | 原件留在這裡。 |
| WR-E01-L011 | `e24854f2` | zhitang | 54.6–57 | 表決權，我不交。 |

## 實測後的剪輯交接

1. 對每個 `audio/<runtime id>.wav` 量 sample rate、sample count、聲音本體時長，保存檔案雜湊與語音／台詞版本。使用真實 WAV；`estimateTimeline`、planned window、TTS request 數都不是實測時長。
2. 依 `edit-plan.json` 的 planned 15 鏡先排 timed animatic，放入已接受的逐句乾聲；五個無對白動作鏡保留撕紙、歸盒、推盒等表演與環境音。animatic 可用核定靜畫檢查節奏，但要明標前製預覽，不冒稱動畫素材已完成。
3. 實測每句是否落入可演的窗口，尤其 L001、L003 與 30 秒內的 L005／L006。超窗先精簡同義措辭並重錄該 id，或在 8 秒動態原片內調剪輯；不能加速、慢放或凍結。修改後重驗前世 → 婚禮、拒簽撕的是展示副本、原件仍在中央桌，以及 S01/S08 同臉換裝。
4. 僅在真實逐句聲音放入已接受的 15 鏡剪輯後，寫每句 `actual_edit_voice_window_s` 與逐鏡實際出入點。依這一份時間軸產 zh-TW SRT/VTT，不使用 voice-only 的 timeline 直接對 60 秒畫面出字幕。關 CC 仍需理解授權、退戒與原件保留；原件／展示副本字樣是道具，不把台詞燒進畫面。
5. 正式生成前另核對 drama 開關、clip provider／model／1080p／8 秒及本片權限與預算。資料夾內寫著 Veo profile 不表示遠端 Omni 預設已被改掉，聲音已配對也不表示動畫可直接跑。只在本片授權範圍內處理，不以試拍啟用其他作品自動製作。
6. 中文 pilot 驗收後才放量做中文全片。日／韓／英唯一啟動條件是**完整繁中全片及繁中 CC 交由站主本人確認**；本地 `series.json` 與 `edit-plan.json` 的 gate 均為 pending，不能由 pilot 通過或代理判定代替。

## 離線驗證

已執行既有 CLI lint：0 errors；只留「原創故事沒有外部事實來源」通用警告，沒有捏造網頁來源壓掉它。已核對 15 鏡 planned 連續覆蓋 0–60 秒、每次原片 8 秒、5 鏡無台詞、11 句 zh-TW 與上層逐字一致、runtime ids 唯一合法、speaker／voice 和人物 look 來源一致。詳細結果見 `validation.json`。這些檢查不證明 TTS、視覺生成、母語聽校或實際 CC 已驗收；最新媒體狀態由主代理的 repo 外產物記錄。
