# C10 OXO｜開場共圖文字計畫獨立查核

查核者：/root/c09_c10_visual_source；未參與作者稿、研究或共圖計畫。

**SOURCE PASS／WRITTEN VISUAL PASS。** 只核文字來源、書面畫面與共圖程序；不是實圖QA、runtime採用、13分鐘實測或owner批准。

## 當前綁定

| 檔案 | SHA-256 |
| --- | --- |
| video.json | 637c8cce6426341d8612b2443089556cbfc2b67d415d1d726bc559999a2d307f |
| script.md | 91719c5b7d3915393a97d5681256973927cc312e4e1b961d6247b9c68ca76c48 |
| narration-only.json | c1e723ca73cd7c3a8c883feb491745f7f498cc384a1bc76493236f3b7524a77c |
| claims.json | e76dd9ef35d4eacbf79b8c7b5a81ccd1f2cafae595da064fa0b7230f64c364b3 |
| image-reuse-plan.json | 6fc61e8c4b91fe6152eeb3c8ee427de5e695c2e6fcb08998de86ec67c7a87c68 |

R7原來源收據：history/before-teaser-image-plan/reviews/source-r7-independent.json；SHA 3ddf8ae9f2afcf5d2fd5bffe1ea378cf57f0ddae4f21d7074ec5ac1b8db7d64f。舊verify SHA dabdcb9f8bf958d6de39e796d00b3665ead4d175bad15319ecebc316a6ce83b4。全部82封存檔、75現保護檔（含2份i18n準備檔）、357個歷史raw/cache/protected bytes、73 source nodes及184現行evidence instances皆實核SHA／excerpt／完整物件。原始四檔亦按batch紀錄核同。

118句、所有facts/source/evidence/limits/material_refs、旁白ID、scene順序、loops、emotion、metadata、voice、look、字幕與分類不變。114完整claim、112完整scene可繼承；只四景prompt/camera及必要written_visual投影改變。claims頂層僅revision/scope/input-hash更新，script與claims.md舊prefix逐bytes保留。新default builder六輸出僅memory攔寫重播逐bytes同值，未跑歷史producer。

## 新書面畫面與原件

h06 ↔ o06：匿名手懸在未成形clay與金屬削皮器上方，camera pull back；teaser不展示做成的握柄，body由Stowell後來回憶的原句交代動作。親讀Gastropod原HTML153及Cooper Hewitt原PDF27（printed52–53），Betsey參與及不同prototype材料界線不動。

h07 ↔ r5-s04：黑柄削皮器以短鏈連carrot bowl，匿名手尚未試用，camera tilt down；不畫顧客反應、購買或銷售結果。親讀PBS原DOCX，Stowell將Lechters、展會後銷慢及chain-to-bowl試用置於同一回憶；不採另一來源chain-to-table當此事件細節。clay prototype、館藏物件、展會samples及retail工具仍各自分清，不冒同一實體。

## 原生純本機驗綁

resolveLook／shotCast／shotAppearancePrompt／composeShotPrompt／Stage.imageKey等實算兩pair完整image input相等，MiniMax image-01、1920×1080、1K、seed1、offset0、takes1、空cast/reference/correction及同look；selection v0。literal HTTP只shot_id場景欄不同，judge context仍各別，不能推定judge stamps相同。

| pair | composed SHA-256 | native image key |
| --- | --- | --- |
| clay-pre-action-shared-still | 91145ec4ed21a1aeaa08ca42cf9345023ce0eed3c4b70fb49b8d7550212c2278 | f81d8106c2586e61 |
| shop-trial-pre-action-shared-still | 66df03ab0a1b11989af0d5f82e8cb6a2ea21ecdf61dfaa6c807824b8a27adb45 | 7652b5e24753d7c0 |

新舊native screenplay／runtime／backend-script逐bytes同SHA 1fa2d25a0161b8ed0e4638fbaf8d982cc1dbf5717e9300cd2d121e43b0a29082。narrative f1c1a609840063ff、speech3899ca6484b93ccf（現runtime字典亦同）、look/mix/subtitles不變；pictures改642c2e38f5e1a565。既有native record SHA ade38a1b35362b8189ffae1a78ac42d4dd979fda35b9723538065aaec1de27e9，僅選四hash欄做narrativeReviewMatches新舊皆true，未讀投票或重judge。

## 實資產仍待驗

現live media/cache.json與keyframes/manifest.json均缺；無provider/backend/producer呼叫。每個第二teaser命令前先核已接受payoff cache與實檔SHA、exact current request。missing/cache miss即停，不能派購探cache。兩端judge／retake／trim選擇不同即停pair；最終manifest與實檔須同SHA才能render。actual_same_asset_verified=false；實圖、成片與無重購ledger均未驗。

## 逐句來源結果

以下118句保留R7原分類、歸屬與來源；完整source-node／limits及逐物件證明見新JSON。

| 句ID | 結果 | 材料／來源 |
| --- | --- | --- |
| c10h01 | PLAN | N01；S1 |
| c10h02 | ATTRIBUTED | A09, N01；S3, S1 |
| c10h03 | PLAN | N02；S2 |
| c10h04 | PLAN | N01；S1 |
| c10h05 | PLAN | N01；S1 |
| c10h06 | PLAN | N06；C1, I4 |
| c10h07 | PLAN | N26；S4 |
| c10h08 | PLAN | N01, N26；S1, S4 |
| c10h09 | PLAN | N01, N05, N26；S1, S2, S4 |
| c10o01 | ATTRIBUTED | N01；S1 |
| c10o02 | ATTRIBUTED | N01；S1 |
| c10o03 | ATTRIBUTED | N02；S2 |
| c10o04 | ATTRIBUTED | N02；S2 |
| c10o05 | PLAN | N06；C1, I4 |
| c10o06 | ATTRIBUTED | N06；C1, I4 |
| c10o07 | ATTRIBUTED | N06；C1, I4 |
| c10o08 | PLAN | N06；C1, I4 |
| c10o09 | PLAN | N06；C1, I4 |
| c10o11 | PLAN | C10X15；X05_TEACHER_PACKET |
| c10o12a | ATTRIBUTED | A01；I4 |
| c10o12b | ATTRIBUTED | A01；I4 |
| c10o13 | ATTRIBUTED | N04, N05, N24；S7, S2, I5 |
| c10o14 | ATTRIBUTED | N05；S2 |
| c10o15 | ATTRIBUTED | N24；I5 |
| c10o16 | ATTRIBUTED | N05；S2 |
| c10o17 | PLAN | N05, N09；S2, I4 |
| c10v5o02 | ATTRIBUTED | A10；X02_HANDLES |
| c10v5o03 | ATTRIBUTED | A10；X02_HANDLES |
| c10o19 | ATTRIBUTED | N07；C1 |
| c10o20 | ATTRIBUTED | N07；C1 |
| c10v5o01 | ATTRIBUTED | C10X15；X05_TEACHER_PACKET |
| c10o22 | PLAN | N08, N09；M6, M5, I4 |
| c10r01 | ATTRIBUTED | N08；M6, M5 |
| c10r02 | ATTRIBUTED | N08；M6, M5 |
| c10r03 | PLAN | N08；M6, M5 |
| c10r05 | ATTRIBUTED | N09；I4 |
| c10r08 | PLAN | N09, N12；I4, P0 |
| c10r09 | PLAN | N09；I4 |
| c10r10 | PLAN | N09, N12；I4, P0 |
| c10r11 | ATTRIBUTED | N09；I4 |
| c10r13 | PLAN | N09；I4 |
| c10r14 | PLAN | N09, N12；I4, P0 |
| c10r16 | PLAN | N10, N12；I4, P0 |
| c10v5b01 | ATTRIBUTED | C10X01；X02_HANDLES |
| c10v5b02 | ATTRIBUTED | A11；X02_HANDLES |
| c10v5b03 | ATTRIBUTED | C10X02；X02_HANDLES |
| c10v5b05 | PLAN | ； |
| c10r18 | ATTRIBUTED | N10；I4 |
| c10r19 | ATTRIBUTED | N10；I4 |
| c10r21 | PLAN | N10, N12；I4, P0 |
| c10m01 | ATTRIBUTED | N11, N12；P0 |
| c10m01a | ATTRIBUTED | A08；P0 |
| c10m02 | ATTRIBUTED | N12；P0 |
| c10m03 | ATTRIBUTED | N12；P0 |
| c10m05 | PLAN | N12；P0 |
| c10m06 | PLAN | N12, N17, N18；P0, C3, M4 |
| c10m08 | ATTRIBUTED | N17；C3, M4 |
| c10m09 | ATTRIBUTED | N17, N18；C3, M4 |
| c10m10a | ATTRIBUTED | A02；S4 |
| c10m11 | PLAN | A03, N17, N18；C3, M4 |
| c10m13 | PLAN | N20；S4 |
| c10m14 | ATTRIBUTED | N20；S4 |
| c10m15 | PLAN | N20；S4 |
| c10m17 | ATTRIBUTED | N20；S4 |
| c10m18 | PLAN | N20；S4 |
| c10m19 | PLAN | N13, N17；P0, C3, M4 |
| c10a01 | ATTRIBUTED | N13；P0 |
| c10a02 | ATTRIBUTED | N13；P0 |
| c10a03 | PLAN | N13；P0 |
| c10a05 | ATTRIBUTED | N13；P0 |
| c10a07 | PLAN | N14；P0 |
| c10a08 | ATTRIBUTED | N14；P0 |
| c10a10 | PLAN | N14；P0 |
| c10a11 | ATTRIBUTED | N14；P0 |
| c10a12 | ATTRIBUTED | N14；P0 |
| c10a15 | PLAN | N15；P0 |
| c10a16 | ATTRIBUTED | N15；P0 |
| c10a18 | PLAN | N15；P0 |
| c10a18x | ATTRIBUTED | N15；P0 |
| c10a18a | ATTRIBUTED | N15；P0 |
| c10a18b | PLAN | N15；P0 |
| c10v5p01 | ATTRIBUTED | C10X03；X16_BLADE_PROTOTYPE |
| c10v5p02 | ATTRIBUTED | C10X03；X16_BLADE_PROTOTYPE |
| c10v5p03 | ATTRIBUTED | C10X03；X16_BLADE_PROTOTYPE |
| c10v5f01 | PLAN | C10X04； |
| c10v5f02 | ATTRIBUTED | C10X04；X09_PBS_TRANSCRIPT |
| c10v5f03 | ATTRIBUTED | C10X04；X09_PBS_TRANSCRIPT |
| c10v5f04 | ATTRIBUTED | C10X05；X09_PBS_TRANSCRIPT |
| c10v5f05 | PLAN | ； |
| c10v5f06 | ATTRIBUTED | C10X06；X09_PBS_TRANSCRIPT |
| c10v5f07 | ATTRIBUTED | C10X06；X09_PBS_TRANSCRIPT |
| c10v5f08 | ATTRIBUTED | C10X07；X09_PBS_TRANSCRIPT |
| c10v5f09 | PLAN | ； |
| c10v5s01 | ATTRIBUTED | C10X07；X09_PBS_TRANSCRIPT |
| c10v5s02 | ATTRIBUTED | C10X07；X09_PBS_TRANSCRIPT |
| c10v5s03 | ATTRIBUTED | C10X08；X09_PBS_TRANSCRIPT |
| c10v5s04 | ATTRIBUTED | C10X08；X09_PBS_TRANSCRIPT |
| c10l06 | PLAN | N26；S4 |
| c10l07 | PLAN | N26；S4 |
| c10v5s05 | ATTRIBUTED | C10X08；X09_PBS_TRANSCRIPT |
| c10v5s06 | ATTRIBUTED | C10X09；X02_HANDLES |
| c10v5s07 | ATTRIBUTED | C10X09；X02_HANDLES |
| c10v5u01 | ATTRIBUTED | C10X10；X20_INTERACTION_ESSAY |
| c10v5u02 | ATTRIBUTED | C10X10；X20_INTERACTION_ESSAY |
| c10v5u03 | ATTRIBUTED | C10X11；X20_INTERACTION_ESSAY |
| c10v5u04 | ATTRIBUTED | C10X11, C10X12；X20_INTERACTION_ESSAY |
| c10v5u06 | PLAN | ； |
| c10v5u07 | ATTRIBUTED | C10X12；X20_INTERACTION_ESSAY |
| c10v5u08 | ATTRIBUTED | C10X12；X20_INTERACTION_ESSAY |
| c10v5u09 | PLAN | ； |
| c10v5u10 | ATTRIBUTED | C10X13；X20_INTERACTION_ESSAY |
| c10v5u11 | ATTRIBUTED | C10X13；X20_INTERACTION_ESSAY |
| c10v5u12 | ATTRIBUTED | C10X14；X20_INTERACTION_ESSAY |
| c10v5u13 | ATTRIBUTED | C10X14；X20_INTERACTION_ESSAY |
| c10v5u14 | ATTRIBUTED | C10X14；X20_INTERACTION_ESSAY |
| c10l19 | PLAN | N01, N05, N26；S1, S2, S4 |
| c10l20 | PLAN | ； |
| c10l21 | PLAN | ； |

本輪必修：無。只寫本獨立報告與verify；未改runtime、media、approval、字典、backend或Git。
