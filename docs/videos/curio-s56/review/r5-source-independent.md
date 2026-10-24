# S56 R5 獨立史料、主張與書面畫面覆核 — HOLD

2026-10-20 UTC。我未參與 S56 R5 寫作，從固定版重新抓取兩份原文並核對 R4→R5 的差異。**史料／書面畫面關卡 HOLD**：`s56152–s56153` 把洛許的返抵避難所寫成確定「繼續往北退」，而所列來源沒有交代他當時的行走方向；`s56166` 把 Loesch 1925 年回憶中的約一點半鐘點改成無歸屬的旁白確定句。其餘 R5 改動及機械對照通過。此票不是盲讀敘事、實際生成畫面或語音驗收。

## 凍結輸入及來源

| 檔案 | 我重新計算的 SHA-256；與作者 R5 交接一致 |
| --- | --- |
| `brief.md` | `404156118c92079b8dd36e89e28025e18582dd365ef36721b840da0390de27a0` |
| `research.md` | `59549e98e6ae258cedfc5b43e6684ecaa1102284d0dee13b0beef6443e4a6fb7` |
| `claims.md` | `5accac0eac72bb257e0da9e60895c3007fc345f6b4576b614c6a674ec5eecf16` |
| `video.json` | `01589b2c33986b92b4fa62504b186e023c2ea0425d82ed5a19a802ad35206cdc` |
| `script.md` | `8556a4a41665cc2c3b660710016669dcee2aa5bd94bf4f13d3868ddfb3194753` |

從固定 Git commit 的 `raw.githubusercontent.com` **重新下載**全文：Foster [1871-10-31 家書之 1923 抄本版](https://github.com/GITenberg/A-Letter-from-the-Fire-Being-an-account-of-the-Great-Chicago-Fire_66472/blob/60c777551301c30942acf749d4bb37ca32752353/66472-0.txt) SHA-256 `59d5d0740ecf20583374d499ab3aff481c000d45d20685b548490b90fc3062ee`；Loesch [1925 回憶錄](https://github.com/GITenberg/Personal-Experiences-During-the-Chicago-Fire-1871_66433/blob/08931a6f2629fd4b8be37b1ec548857d48d17eb9/66433-0.txt) SHA-256 `d1e6575eb2af0a36a99aacfc9c94817f38e460db81746cd4cc95199e18d1f011`。兩者皆與 `research.md` 固定值一致。R4 未改的台詞與畫面由 [R4 獨立史料覆核](r4-source-independent.md)承接；我另核 R5 全部逐句 ID、文字、引文連結與 R5 變動的來源內容。

## 必修項目

1. **`s56152–s56153` 的方向及 `s56152` 畫面。** R5 旁白說「洛許若繼續往北退」及「洛許往已暫住的地方退，那裡在更北的草地旁」。Loesch 原文說星期一約 6 時**已**搭車北行至 Fullerton/Racine 借住 [L516–522](https://github.com/GITenberg/Personal-Experiences-During-the-Chicago-Fire-1871_66433/blob/08931a6f2629fd4b8be37b1ec548857d48d17eb9/66433-0.txt#L516-L522)，白天在 North 與 Fullerton 之間走動 [L537–545](https://github.com/GITenberg/Personal-Experiences-During-the-Chicago-Fire-1871_66433/blob/08931a6f2629fd4b8be37b1ec548857d48d17eb9/66433-0.txt#L537-L545)，日落前**回到**暫住處 [L578–584](https://github.com/GITenberg/Personal-Experiences-During-the-Chicago-Fire-1871_66433/blob/08931a6f2629fd4b8be37b1ec548857d48d17eb9/66433-0.txt#L578-L584)。文字沒有交代他白天行走的最後方位，不能肯定這次「繼續往北退」；`claims.md` 的 `s56152–s56153` 引文也未包含早晨到 Fullerton/Racine 的定位段。`s56152` 畫面把他畫成朝「北方空地」與攜物難民同鏡移動，但同一原文說那些難民**多數往西**過 Webster Avenue 橋 [L560–575](https://github.com/GITenberg/Personal-Experiences-During-the-Chicago-Fire-1871_66433/blob/08931a6f2629fd4b8be37b1ec548857d48d17eb9/66433-0.txt#L560-L575)，容易合併兩條逃生路線。請以「回到已借住的屋子，屋前有乾草地」之類有據的動作改寫，對應改畫面和引用；若保留 `s56154`，應避免連說兩次「回到暫住處」。
2. **`s56166` 的鐘點歸屬。** R4 `s56167` 明說「洛許回憶約一點半」，R5 刪掉這個歸屬，現在 `s56166` 直接宣告「星期二凌晨約一點半，大雨……」。這時間是 Loesch 1925 年的回憶 [L601–613](https://github.com/GITenberg/Personal-Experiences-During-the-Chicago-Fire-1871_66433/blob/08931a6f2629fd4b8be37b1ec548857d48d17eb9/66433-0.txt#L601-L613)，不是本集找到的 1871 官方逐分紀錄；`research.md` 也要求精確時刻標明回憶性質。請在口說句加上「洛許回憶／記得」等歸屬。大雨先於草火、浸布備案未用，則與 [L578–613](https://github.com/GITenberg/Personal-Experiences-During-the-Chicago-Fire-1871_66433/blob/08931a6f2629fd4b8be37b1ec548857d48d17eb9/66433-0.txt#L578-L613) 相符；目前雨景未宣稱全城同分鐘熄滅。

## 其餘 R4→R5 變動

JSON 逐欄差異只有刪景 `s56016`、`s56017`、`s56089`，刪句 `s56059`，換開場章名，及 `s56015`、`s56091–s56092`、`s56152`、`s56166–s56167` 台詞；頂層資料與保留場景的 `data` 畫面欄位均未變。開場新章名是 Foster 過南支河後停看對岸 [F349–365](https://github.com/GITenberg/A-Letter-from-the-Fire-Being-an-account-of-the-Great-Chicago-Fire_66472/blob/60c777551301c30942acf749d4bb37ca32752353/66472-0.txt#L349-L365)；`s56015` 家書日期及收信人由 [F161–171](https://github.com/GITenberg/A-Letter-from-the-Fire-Being-an-account-of-the-Great-Chicago-Fire_66472/blob/60c777551301c30942acf749d4bb37ca32752353/66472-0.txt#L161-L171)、[F204–208](https://github.com/GITenberg/A-Letter-from-the-Fire-Being-an-account-of-the-Great-Chicago-Fire_66472/blob/60c777551301c30942acf749d4bb37ca32752353/66472-0.txt#L204-L208) 支持，畫面沒有冒充原信。教堂屋頂、消防員爬屋頂的保留動作見 [F310–327](https://github.com/GITenberg/A-Letter-from-the-Fire-Being-an-account-of-the-Great-Chicago-Fire_66472/blob/60c777551301c30942acf749d4bb37ca32752353/66472-0.txt#L310-L327)；刪掉的 `s56059` 是重述。`s56091–s56092` 的旅館距離／商業區疑問及後章磚、石、鐵、大理石與最終失守，符合 [F376–412](https://github.com/GITenberg/A-Letter-from-the-Fire-Being-an-account-of-the-Great-Chicago-Fire_66472/blob/60c777551301c30942acf749d4bb37ca32752353/66472-0.txt#L376-L412)，未畫石材本身燃燒。刪掉的 `s56089–s56090` 只收掉提前重述。`s56167` 的浸布備案未使用是雨先到後的合理窄結論。

## 機械結果及關卡界線

`script.md` 與程式 `screenplay(video.json)` 逐位元相同。`video.json` 有 **171** 個唯一遞增口說 ID、**138** 景（**135** 插圖景、**3** 字卡）、**7** 章、**17** 個 loop；`claims.md` **171** 列依序與口說 ID 和全文相同，每列至少一個來源。**258** 個來源連結全指向兩個固定 commit 的指定全文，行號區間有效。`node tools/video/cli.mjs lint --slug curio-s56 --json` 為 **0 errors／0 warnings**，`git diff --check HEAD -- docs/videos/curio-s56` 通過。估時計時器在 250 字元／分鐘下開場 **59.57 秒**、正文 **774.93 秒（12:55）**；在 325 下開場 **48.50 秒**、正文 **629.00 秒（10:29）**，皆落在 30–60 秒開場和正文至少 8 分鐘的規劃條件內。這是文字估計，R5 尚無相符的實測語音。

作者修正後需重新凍結五檔雜湊，由未撰稿者對修處重新核對；後續兩位無前情讀者及付費媒體關卡各自獨立。
