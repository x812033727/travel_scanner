# S56 R7 獨立史料、主張及書面畫面覆核 — PASS

2026-10-20 UTC。我未撰寫 R7；在收到 [R7 作者五檔凍結交接](r7-author-fix.md)後才讀本版創作檔。**本版的史料、逐句主張與書面畫面關卡 PASS。**R6 的 [來源 PASS](r6-source-independent.md)只涵蓋舊雜湊；本票重新核對 R7 的 18 句修改，不是敘事盲評、TTS 聽審、實際插圖或成片驗收。

## 凍結檔案與原文

| 檔案 | 本次獨立重算 SHA-256 |
| --- | --- |
| `brief.md` | `09f731c13f1037c963aa5774b936a43e1a187b5c4ae8d09ba158581a705f1a52` |
| `research.md` | `59549e98e6ae258cedfc5b43e6684ecaa1102284d0dee13b0beef6443e4a6fb7` |
| `claims.md` | `aa0923707ae19afe2a64906d5e7d208bd675fb0ad364897c76e1d2ec44c07165` |
| `video.json` | `451fd61d81b93ba3290d314c5b3b408d4a1b59a7c40287d3d03ad5e6df315f8a` |
| `script.md` | `1612cbe85e9add3f1c4b9b4be490a3fe9a6ef23588f080ed4f16d135369d1e2d` |

五值與作者交接一致。重新下載 [Foster 固定版](https://github.com/GITenberg/A-Letter-from-the-Fire-Being-an-account-of-the-Great-Chicago-Fire_66472/blob/60c777551301c30942acf749d4bb37ca32752353/66472-0.txt)全文，SHA-256 `59d5d0740ecf20583374d499ab3aff481c000d45d20685b548490b90fc3062ee`；[Loesch 固定版](https://github.com/GITenberg/Personal-Experiences-During-the-Chicago-Fire-1871_66433/blob/08931a6f2629fd4b8be37b1ec548857d48d17eb9/66433-0.txt)全文，SHA-256 `d1e6575eb2af0a36a99aacfc9c94817f38e460db81746cd4cc95199e18d1f011`。Foster 的文字是 1871 年信件之 1923 年家人抄本印刷版；Loesch 的是 1925 年親歷回憶。

R6 音檢私有存檔 `r6-audio-archive/round1/check.json` 的逐句 `intended` 與目前 170 個口說 ID 相較，**恰有下列 18 句變動**，與作者表列的 R6 原句及 R7 現句逐字相同，沒有未列出的口說修改。該存檔不是完整 R6 `video.json` 快照，故不宣稱全檔逐位元 R6→R7 差分。相較仍留存的 R4 `video.json` 快照，現稿共通場景的 `data` 欄只有先前 R6 已覆核的 `s56151–s56153` 不同；R7 這 18 句所屬畫面提示與字卡未見新增改動。

## 18 句逐句史料與畫面核對

| ID | 獨立判斷 |
| --- | --- |
| `s56004` | Foster 過 South Branch 後站在這岸望向舊火 [F357–366](https://github.com/GITenberg/A-Letter-from-the-Fire-Being-an-account-of-the-Great-Chicago-Fire_66472/blob/60c777551301c30942acf749d4bb37ca32752353/66472-0.txt#L357-L366)；對岸大火與他看河的提示一致。 |
| `s56038` | Loesch 寫鋪街的松木塊及上覆焦油 [L105–117](https://github.com/GITenberg/Personal-Experiences-During-the-Chicago-Fire-1871_66433/blob/08931a6f2629fd4b8be37b1ec548857d48d17eb9/66433-0.txt#L105-L117)；提示畫木路塊，不混成電子「介面」。 |
| `s56052` | Foster 在信裡寫自己到場不久有三十輛蒸汽消防車，隨即描述風中燃燒木塊落到別處 [F293–308](https://github.com/GITenberg/A-Letter-from-the-Fire-Being-an-account-of-the-Great-Chicago-Fire_66472/blob/60c777551301c30942acf749d4bb37ca32752353/66472-0.txt#L293-L308)。新句的「他在家書中數到」保留當事人歸屬；消防員與遠處煙屋頂提示沒有把三十輛畫成精確重建。 |
| `s56053` | 風帶火星與燃燒木塊落下見 [F299–308](https://github.com/GITenberg/A-Letter-from-the-Fire-Being-an-account-of-the-Great-Chicago-Fire_66472/blob/60c777551301c30942acf749d4bb37ca32752353/66472-0.txt#L299-L308)；仰望火屑提示吻合，沒有實際「火牆」或武器。 |
| `s56057` | 教堂屋頂離主火約三百碼，木塊先落而屋頂起火 [F310–315](https://github.com/GITenberg/A-Letter-from-the-Fire-Being-an-account-of-the-Great-Chicago-Fire_66472/blob/60c777551301c30942acf749d4bb37ca32752353/66472-0.txt#L310-L315)。新問句和遠處屋頂火提示未說主火已到。 |
| `s56071` | Foster 說人們以為火不能越過約八十碼水面 [F360–366](https://github.com/GITenberg/A-Letter-from-the-Fire-Being-an-account-of-the-Great-Chicago-Fire_66472/blob/60c777551301c30942acf749d4bb37ca32752353/66472-0.txt#L360-L366)。新句用「在信中估計／約」限定數字；既有 `big` 字卡「約 80 碼／福斯特信中估計／主火隔著南支河水面」仍與口說同一主張，沒有把它改成實測寬度。 |
| `s56073` | 他在自己這岸背後約四百碼發現另起的火 [F364–368](https://github.com/GITenberg/A-Letter-from-the-Fire-Being-an-account-of-the-Great-Chicago-Fire_66472/blob/60c777551301c30942acf749d4bb37ca32752353/66472-0.txt#L364-L368)；提示只畫回頭看遠煙，未指定某塊火屑的飛行路徑。 |
| `s56078` | 他走去看新火，見木造小屋迅速燒起 [F368–373](https://github.com/GITenberg/A-Letter-from-the-Fire-Being-an-account-of-the-Great-Chicago-Fire_66472/blob/60c777551301c30942acf749d4bb37ca32752353/66472-0.txt#L368-L373)；東岸木屋提示相符。 |
| `s56079` | Foster 寫舊火後來也「jumped the river」並與新火連在一起 [F364–369](https://github.com/GITenberg/A-Letter-from-the-Fire-Being-an-account-of-the-Great-Chicago-Fire_66472/blob/60c777551301c30942acf749d4bb37ca32752353/66472-0.txt#L364-L369)。新句分清西岸大火、東岸新火；提示為兩處火前線相遇，沒有畫確定越河火屑。 |
| `s56080` | 「那處火旁有小木屋，火很快蔓延」對應 [F368–374](https://github.com/GITenberg/A-Letter-from-the-Fire-Being-an-account-of-the-Great-Chicago-Fire_66472/blob/60c777551301c30942acf749d4bb37ca32752353/66472-0.txt#L368-L374)；與 `s56079` 共一景的兩火相接提示是結果示意，沒有與此句衝突。 |
| `s56086` | Foster 在前行時撲滅由火星點著的篷布、人行道等小火 [F373–379](https://github.com/GITenberg/A-Letter-from-the-Fire-Being-an-account-of-the-Great-Chicago-Fire_66472/blob/60c777551301c30942acf749d4bb37ca32752353/66472-0.txt#L373-L379)；提示只畫他潑水救小篷布。 |
| `s56094` | 信中稱該商業區建築有磚、石、鐵或大理石 [F378–381](https://github.com/GITenberg/A-Letter-from-the-Fire-Being-an-account-of-the-Great-Chicago-Fire_66472/blob/60c777551301c30942acf749d4bb37ca32752353/66472-0.txt#L378-L381)。新句明指福斯特；畫面只概示磚石街，不假裝精確記錄材料或「石頭燃燒」。 |
| `s56095` | Foster 自述當時確信火不會穿過這片建築，甚至未料燒到旅館 [F380–386](https://github.com/GITenberg/A-Letter-from-the-Fire-Being-an-account-of-the-Great-Chicago-Fire_66472/blob/60c777551301c30942acf749d4bb37ca32752353/66472-0.txt#L380-L386)；新句保留其**當時判斷**，石牆提示沒有畫「石材本身可燃」。 |
| `s56099` | 他打包大箱，先留小物待威脅迫近再放入，後又出門看火 [F388–400](https://github.com/GITenberg/A-Letter-from-the-Fire-Being-an-account-of-the-Great-Chicago-Fire_66472/blob/60c777551301c30942acf749d4bb37ca32752353/66472-0.txt#L388-L400)；新句「還留在」與旅館房內箱子提示都未說他丟棄。 |
| `s56132` | Loesch 把那幕與乾燥、受熱、焦油街面和落下的燃燒木塊連起來 [L394–400](https://github.com/GITenberg/Personal-Experiences-During-the-Chicago-Fire-1871_66433/blob/08931a6f2629fd4b8be37b1ec548857d48d17eb9/66433-0.txt#L394-L400)，焦油木街面另見 [L105–117](https://github.com/GITenberg/Personal-Experiences-During-the-Chicago-Fire-1871_66433/blob/08931a6f2629fd4b8be37b1ec548857d48d17eb9/66433-0.txt#L105-L117)。新句說「他認為」且沒有宣稱列盡所有原因；木路塊及火屑提示維持個人回憶的範圍。 |
| `s56156` | Loesch 返回借住處，屋前／南方為乾草地 [L578–584](https://github.com/GITenberg/Personal-Experiences-During-the-Chicago-Fire-1871_66433/blob/08931a6f2629fd4b8be37b1ec548857d48d17eb9/66433-0.txt#L578-L584)；問句與屋旁乾草地提示相符，未再暗示返程方位。 |
| `s56167` | 原擬用井水浸濕布料，必要時跑過草火；大雨先於草火落下 [L589–609](https://github.com/GITenberg/Personal-Experiences-During-the-Chicago-Fire-1871_66433/blob/08931a6f2629fd4b8be37b1ec548857d48d17eb9/66433-0.txt#L589-L609)。新句明說這是**未用的備案**，提示只畫備好的水鍋與落雨。 |
| `s56176` | Foster 過南支河後在同岸發現新火，後來另過橋，原以為安全的北側又起火 [F357–369](https://github.com/GITenberg/A-Letter-from-the-Fire-Being-an-account-of-the-Great-Chicago-Fire_66472/blob/60c777551301c30942acf749d4bb37ca32752353/66472-0.txt#L357-L369)、[F447–460](https://github.com/GITenberg/A-Letter-from-the-Fire-Being-an-account-of-the-Great-Chicago-Fire_66472/blob/60c777551301c30942acf749d4bb37ca32752353/66472-0.txt#L447-L460)。片尾句只總結過河未必已脫險；河邊人物提示是示意，沒有新造具體事件。 |

## 機械結果與下一關

現稿 **170** 個唯一、遞增口說 ID；`claims.md` **170** 列逐一與 `video.json` 的 ID／全文相同，每列有來源。**258** 個引用連結皆指向兩個固定 commit 且行號有效；`script.md` 與 `screenplay(video.json)` 逐位元相同。**137** 景（134 插圖景、3 字卡）、**7** 章、**17** 個有效且前設早於回收的伏筆。程式算得 `narrative_hash=0af74e3174cb3b72`、`speech_hash=9c38a82ff422307e`，與作者交接一致。

`node tools/video/cli.mjs lint --slug curio-s56 --json` 回 **0 errors／0 warnings**，`git diff --check HEAD -- docs/videos/curio-s56` 通過。文字估計在 250 字元／分鐘時開場 **59.33 秒**、正文 **778.97 秒**；325 時開場 **48.33 秒**、正文 **631.80 秒**。符合 30–60 秒開場及至少 8 分鐘正文的**稿面規劃**。R7 的實際 TTS 尚未生成，不能用 R6 實測 54.37 秒或 R6 的 21 個音檢旗標作 R7 放行；開場文字估計離 60 秒僅 0.67 秒，後續須用新語音重測。

來源與書面畫面關卡可交棒給兩位未接觸前情的獨立敘事讀者，之後再依新雜湊重做政策與音訊關卡。本票沒有代替那些票，也沒有動用付費媒體。
