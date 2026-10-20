# S48 R10｜獨立史料及書面畫面差分：PASS

2026-10-20 UTC。獨立對照 [R10 作者凍結](../verify-13.md)、[R9 獨立來源／書面畫面 PASS](r9-source-independent.md)、Git HEAD 的精確 R9 五檔，以及兩份固定原文。本次只裁決 `atl058` 新口播的史料、逐句主張及**書面**畫面；沒有改作者五檔、生成媒體或做敘事盲讀。

| R10 精確輸入 | SHA-256 |
| --- | --- |
| `brief.md` | `7b4bc4b3f6970ac20ef9c2b9269d8a17cafacc87f2ccaf076806772b2e56ca8a` |
| `research.md` | `3d769826eff0fbfb939b35506e9eafb4166868a6c0709cb4bf234af4922dd19f` |
| `claims.md` | `5b0714fafe2d0537d03309aac08d1dff8de0656337223689b7033866a5ccbbf7` |
| `video.json` | `ae0c8fd27d8abf7cc3d1dc192640336d12e5a5919db28d7b658671db35821e10` |
| `script.md` | `182581f1a2f5c5eba79e3513bc0d6a8c79a6789360d6c86847068460cf515cdd` |

原始位元組另核：[Russell 固定全文](https://github.com/GITenberg/The-Atlantic-Telegraph_40948/blob/ba499c6bc32adef8c8a91a306dcb2d54bf7e898d/40948-0.txt) `/tmp/s48-russell-atlantic-telegraph.txt` SHA-256 `558efcc342df669e7387ffff818c104690e7ec910de49e795f996abf147ea750`；[Field 固定全文](https://github.com/GITenberg/The-Story-of-the-Atlantic-Telegraph_34765/blob/6b50b44d3cd2f3f1831e2c1a8fa052f53c51a4cd/34765.txt) `/tmp/s48-field-atlantic-telegraph.txt` SHA-256 `bee659b24ace56a5e1f7104a6a306e9325ccd9c864fc373ad35b0863c5a8c675`。Field 所涉 1866 年口播與引文層級未變。

## `atl058` 史料裁決

`atl023–024` 先講第一截鐵絲刺入絕緣層、進入方式當時無法判定；Russell [R3033–3044](https://github.com/GITenberg/The-Atlantic-Telegraph_40948/blob/ba499c6bc32adef8c8a91a306dcb2d54bf7e898d/40948-0.txt#L3033-L3044)記其形狀、刺入及「無人能說明如何進水槽」，意外帶入只是當時一般看法。`atl032–034` 再講第二截穿到核心及船上猜疑；[R3572–3584](https://github.com/GITenberg/The-Atlantic-Telegraph_40948/blob/ba499c6bc32adef8c8a91a306dcb2d54bf7e898d/40948-0.txt#L3572-L3584)顯示當時對蓄意破壞的強烈懷疑，並非調查確定了下手者或刺入機制。故 R10「兩截鐵絲都不能證明有人動手」保留兩次破口的證據界線。

緊接的 `atl057` 明說是羅素翻看**船上儲放線圈**的護線鐵絲，並沒有把後來的脆線當作兩個破口的逐件鑑定。[R3735–3758](https://github.com/GITenberg/The-Atlantic-Telegraph_40948/blob/ba499c6bc32adef8c8a91a306dcb2d54bf7e898d/40948-0.txt#L3735-L3758)另記一截從船上電纜突出、碰觸即脆斷的鐵絲，作者因此考慮機械意外可留下貌似人為的痕跡，船上多數最後傾向意外；[R4094–4105](https://github.com/GITenberg/The-Atlantic-Telegraph_40948/blob/ba499c6bc32adef8c8a91a306dcb2d54bf7e898d/40948-0.txt#L4094-L4105)記在電纜線圈中發現保護鐵絲有的鬆脫或斷裂、扭轉後有的堅韌有的很脆，並明說這**加強**意外說。R10「材料脆斷的發現讓意外較可信」只述證據使某種解釋較可信；後半「但鐵絲怎麼刺入仍不明」阻止將材料觀察說成已查定兩截各自刺入的原因。因此新句沒有誇大兩次鐵絲刺入，也沒有把人為或意外定為已證實結論。

## 精確差分、對齊及書面畫面

以 Git HEAD 的 R9 `video.json` 還原 `atl058.lines[0].text` 後，整個 JSON 物件與 R10 逐欄相等：**只改該句口播**。`claims.md` 相對 R9 只改首段版本狀態與 `atl058` 同文，`brief.md`／`research.md` 位元組仍是 R9；`script.md` 與 `screenplay(doc)` 逐位元相同。`video.json` 保有 100 景、99 個正文 `shot`、三句片尾，共 **102 個唯一口播 ID**；`claims.md` 的 **99/99 正文列**及三句片尾均按 ID、順序、字面對齊。99/99 個非空 `shot.data.prompt` 與 R9 逐字相同；23/23 條 `loops` 全同，setup／payoff ID 均存在且順序正確。

`atl057` 的原提示詞畫船艙儲線圈旁彎折兩小段護線材；`atl058` 原提示詞畫記者、單截斷線與空白筆記本。兩景沒有指示繪製破口樣本的鑑定結果、海底撈出的脆線或已證實的破壞者；新口播沒有造成畫面矛盾。這只是**書面提示詞**裁決，不是生成插畫驗收。

`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s48 --json` 回報 **0 errors／0 warnings、102 lines**；`git diff --check -- docs/videos/curio-s48` 通過。`estimateTimeline(doc, 325)` 估濃縮開場 **45.27 秒**、其後正文至片尾前 **531.70 秒（8:51.70）**，是靜態估值，非 R10 TTS 實長。

**裁決：史料文字 PASS；書面畫面 PASS。** 只綁上表精確 R10 五檔。仍須兩位全新隔離讀者對 R10 敘事盲讀，之後按精確新版重做全稿政策與網站劇本流程、只重合成改句並完整音檢至零旗標。R9 的敘事／政策／站台結果及音訊 HOLD 不自動移轉為 R10 放行；沒有音訊、插畫、配樂或成片驗收。
