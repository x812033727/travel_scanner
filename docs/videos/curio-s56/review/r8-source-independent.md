# S56 R8 獨立史料、主張及書面畫面覆核 — PASS

2026-10-20 UTC。我未撰寫 R8；在收到 [作者單句修稿凍結](r8-author-fix.md)後才讀取當前稿件。**R8 精確五檔雜湊的史料、逐句主張與書面畫面關卡 PASS。**這不是新稿敘事盲評、政策、實際語音或生成插圖驗收。

| 檔案 | 本次重算 SHA-256 |
| --- | --- |
| `brief.md` | `09f731c13f1037c963aa5774b936a43e1a187b5c4ae8d09ba158581a705f1a52` |
| `research.md` | `59549e98e6ae258cedfc5b43e6684ecaa1102284d0dee13b0beef6443e4a6fb7` |
| `claims.md` | `5c735e7abb3e4fbf26c6db522efd04cff49c99ca2d6fce0a9e65d6196d2be045` |
| `video.json` | `543054261039a1ecb8c38bccc93b3a48cd77a02a361a2f1f57084ef772470690` |
| `script.md` | `4ffefbfd2310bdca453a331001c2c61c385f4ef43d7ca85316079a17d8924b00` |

五值與 R8 作者交接相同。重新下載 [Loesch 1925 年固定版回憶](https://github.com/GITenberg/Personal-Experiences-During-the-Chicago-Fire-1871_66433/blob/08931a6f2629fd4b8be37b1ec548857d48d17eb9/66433-0.txt)，全文 SHA-256 `d1e6575eb2af0a36a99aacfc9c94817f38e460db81746cd4cc95199e18d1f011`，與 `research.md` 相同；Foster 固定版 SHA-256 `59d5d0740ecf20583374d499ab3aff481c000d45d20685b548490b90fc3062ee` 已在 [R7 獨立覆核](r7-source-independent.md)重取核對，R8 對其來源與口說未改。

## 唯一改句的來源與畫面

`s56132` 現為「**洛許認為，剛才看見的燃燒木塊，是幾個街區同時起火的可能原因之一。**」Loesch 先記自己看到空中燃燒餘燼，隨後三個街區連街面、人行道幾乎一瞬間起火 [L380–393](https://github.com/GITenberg/Personal-Experiences-During-the-Chicago-Fire-1871_66433/blob/08931a6f2629fd4b8be37b1ec548857d48d17eb9/66433-0.txt#L380-L393)。他接著把乾燥、長時間高熱與焦油鋪面連到**街面燃燒**，再說落下的燃燒木塊**加上前述因素**可解釋數個街區的建築幾乎同時起火 [L394–400](https://github.com/GITenberg/Personal-Experiences-During-the-Chicago-Fire-1871_66433/blob/08931a6f2629fd4b8be37b1ec548857d48d17eb9/66433-0.txt#L394-L400)。更早他也明記看到被風吹來、長達兩英尺以上的燃燒木塊 [L322–327](https://github.com/GITenberg/Personal-Experiences-During-the-Chicago-Fire-1871_66433/blob/08931a6f2629fd4b8be37b1ec548857d48d17eb9/66433-0.txt#L322-L327)。新句用「洛許認為」和「可能原因之一」限定為個人解釋、非單一已證實火因；`s56133` 緊接著說這是回憶與判斷，而非真有炸藥爆炸。

故事中 `s56120` 已說並畫被風吹來的燃燒木塊；`s56129–s56131` 再說並畫多個街區、街面與人行道起火。因此新 `s56132` 的「剛才看見」能回指已呈現的景，而不是把乾燥、焦油與木塊清單重講一次。`s56132` 原有提示是深色背心男子檢視塗焦油木路塊，旁有飛落火星；它只作回憶中木路面與飛火因素的插圖示意，未畫精確木塊軌跡或爆炸。主張列的固定來源與畫面限制和口說句相容。這只判定**史料與書面畫面**；回呼是否使敘事 `no_recap` 過關，須由無前情讀者另行盲評。

為核對窄差分，我在記憶體中把 R8 `video.json` 和 `claims.md` 各唯一一處新句換回 [R7 凍結舊句](r7-author-fix.md)，重算 SHA-256 分別精確得到 R7 `451fd61d81b93ba3290d314c5b3b408d4a1b59a7c40287d3d03ad5e6df315f8a` 和 `aa0923707ae19afe2a64906d5e7d208bd675fb0ad364897c76e1d2ec44c07165`；由還原的 JSON 執行 `screenplay()`，又精確得到 R7 劇本 `1612cbe85e9add3f1c4b9b4be490a3fe9a6ef23588f080ed4f16d135369d1e2d`。所以 R7→R8 的這三檔差分確實只有所述單句與生成劇本的相應改動；`brief.md`、`research.md` 位元未變。

## 機械結果與交接

R8 有 **170** 個唯一遞增口說 ID，`claims.md` **170** 列的 ID／全文逐一相同，每列有來源；**258** 個引用都指向兩份固定 commit 的有效行號。`script.md` 與 `screenplay(video.json)` 逐位元一致。**137** 景（134 插圖景、3 字卡）、**7** 章、**17** 個有效且前設早於回收的伏筆；`narrative_hash=442f1009de84b004`、`speech_hash=68467aa7d587dcc8`。`node tools/video/cli.mjs lint --slug curio-s56 --json` 是 **0 errors／0 warnings**；`git diff --check HEAD -- docs/videos/curio-s56` 通過。

文字估計在 250 字元／分鐘下開場 **59.33 秒**、正文 **779.67 秒**；325 時開場 **48.33 秒**、正文 **632.37 秒**，符合 30–60 秒開場及至少 8 分鐘正文的稿面規劃。R8 尚無實測 TTS；開場估計離上限僅 0.67 秒，音訊關卡必須重新量測。本來源票可交給兩位未接觸前情的讀者評 R8 敘事，不能沿用 R7 `no_recap` 雙否票，也不能沿用 R6 音訊或政策核准。
