# S58 R5｜雙盲敘事與史料畫面窄修作者凍結

2026-10-21 UTC。**R5 作者候選，尚非史料、敘事、原生插圖或站台核准 PASS。** R4 的[獨立來源／書面畫面 HOLD](r4-source-independent.md)與[正式雙盲 OR 合併 HOLD](r4-merge/summary.md)已先封存：兩位讀者各 11／13、合併 11／13，`chapters_link` 和 `no_recap` 未過；官方 CLI `passed:false` 且五份 R4 創作檔在執行前後 SHA 一致。R5 是依這些阻擋所做的新候選，所有 R1–R4 原票和紀錄均保留。

| R5 凍結檔 | SHA-256 |
| --- | --- |
| `research.md` | `1f6adc58345a10655a0bfdf66c87d5337cbd87c8271f41cb4878204bf4e5d5d0` |
| `brief.md` | `fbffce22c2eff5052a4050b06b121e3fc8a62b7ab350ecfd6a150f5788214362` |
| `claims.md` | `67ed990038429d6186487e1f16504ebf3e982d2b8d7c591c75b7c58faf8cceef` |
| `video.json` | `1be17b85b1b41cb1f5e0f9fe21d18c758ef096447cb4c776c5dcba1ba79dda22` |
| `script.md` | `ce03aeae00241c3e178897ea35a4469c697abaddbb268061fd0574eed0dc35e0` |

## 相對 R4 的修訂

- **章節銜接與避免重述：**`s58055` 現問倖存器材過佔領區第一步怎麼避搜查，`s58056` 以村民衣物直接回答；`s58079` 只保留抵 Tours 日期，`s58080` 不再重說抵達，而從他已有的透明薄膜樣本推向當地紙郵務。`s58107` 的一鳥載片問題在新章首 `s58108` 直接答 **十八片**；後面依序只說一次每片十二或十六頁、平均三千則、一鳥逾五萬則與整組不足一克。`s58114` 把最高容量與實際送達分開，不再重念五萬。
- **酒桶位置：**`s58071` 口播與單人提示詞改為進 Arcis 稅卡前把酒桶留在小村，沒有畫酒桶在稅卡接受檢查；符合固定 Dagron [D231–260](https://github.com/GITenberg/La-poste-par-pigeons-voyageurs--Souvenir-du-si-ge-de-Paris_19588/blob/d2a6e7f42a608005416d925c4fbf1f85d4dbe966/19588-8.txt#L231-L260)。
- **一次一動作：**`s58089` 只畫一位工人把透明薄膜放上攝影桌，舊紙為靜止背景。`s58108` 的一人提示詞配合十八片答句，畫多片細小薄膜而不要求模型寫出精確數目。
- **一月材料的證據界線：**研究檔 P11、主張列與 `s58140–s58142` 明確區分「Dagron 以鴿郵向巴黎兩位聯絡人求助、請他們搭首個離城氣球寄出」與「一月二十四日材料到波爾多」；固定 [D394–404](https://github.com/GITenberg/La-poste-par-pigeons-voyageurs--Souvenir-du-si-ge-de-Paris_19588/blob/d2a6e7f42a608005416d925c4fbf1f85d4dbe966/19588-8.txt#L394-L404)未記實際回運載具。`s58141` 畫一人為無字請求封蠟，不再畫飛行員把材料裝上球；`s58142` 口播不宣稱實際搭球，提示詞也不畫載運。

## 作者檢查與下一關

`video.json` 為 **147 景、142 個 `shot`、5 個 `big`**（插圖占 96.6%），與 `claims.md`、衍生 `script.md` **147／147** 場景 ID、口播逐字對齊，連號。濃縮開場 183 漢字、六章正文 2697 漢字；按較快每分鐘 325 漢字估 **8.30 分鐘正文**，實際時長須日後以 TTS timeline 驗證。20 組 `loops` 已配置，R5 `s58107` 的答案錨點改為 `s58108`。`NODE_USE_ENV_PROXY=1 NODE_NO_WARNINGS=1 node tools/video/cli.mjs lint --slug curio-s58 --json` 為 **0 error／0 warning**；`script --slug` 已重產劇本，`npm run test:docs-videos` **236／236 pass**，`npm run check:tasks` exit 0（只列其他任務既有警告）。

請新的非作者覆核者按此五檔 SHA 檢查 R4 HOLD 四處及新序列的逐句主張／書面提示詞；再由兩位無前情讀者只看 R5 劇本重做 13 題盲讀和正式 OR 合併。未做 TTS、插圖、配樂、合成、網站核准或 YouTube 上架。
