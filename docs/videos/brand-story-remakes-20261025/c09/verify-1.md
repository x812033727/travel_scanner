# C09 Patagonia｜開場共圖文字計畫獨立查核

查核者：/root/c09_c10_visual_source；未參與作者稿與計畫。

**SOURCE PASS／WRITTEN VISUAL PASS。** 僅文字稿、書面畫面及共圖程序；不是實圖QA、runtime採用、13分鐘實測或owner批准。

## 當前綁定

| 檔案 | SHA-256 |
| --- | --- |
| video.json | 1912082c8c1ecc0d2bab399903bde0e6f2a203cc3aac7487519ec3bbc26cc222 |
| script.md | 186602e9f7511c10c5f4bf43ea2206c9a1a0bd787381e31412ae8765735a9946 |
| narration-only.json | 18c5843875be1525341d3b0f24992baafc227f7b975487a8369e2517a6383d25 |
| claims.json | 8f9b5d2936b0a18cb729cdac3052103fe6edcf0719830a68eac1214cfc48f686 |
| image-reuse-plan.json | 8485f2ecc10fb5a168bfb25c0579bce0814faec5264ea0e4b786e0225acf10c3 |

R7原來源收據：history/before-teaser-image-plan/reviews/source-length-r7-independent.json；SHA 5e69a7c502aa8fd8f2c8fdb80e578281637de5fc102eb4c4db9cdbb5f2ff0815。舊verify SHA 416a1d8e63230b944a8f0fa43c6ad3cfd18a8619a1c326b222328e6f111053ba。封存159檔、現保護152檔（85 i18n）、原始四檔、5組raw/cache、S8 PDF及既存四頁proof、142錨點皆逐實檔SHA核同。

逐物件只差006/088 prompt及088 camera；claims只加兩筆written_visual，101完整claim不變，103 facts/source/evidence物件不動。所有旁白、ID、scene順序、loops、emotion、metadata、voice、look、字幕及分類不動。script與claims.md原prefix逐bytes相同，僅尾加無聲註解。新default builder五輸出在memory攔寫重播逐bytes同值，未跑歷史producer。

## 新畫面與原生驗綁

006 ↔ 088：匿名攀登者、granite ledge、閉合袋及繩索，camera tilt up。袋不露岩釘／楔塊，不在teaser揭無錘或完成結果；回收章由原旁白給答案。共用示意素材不聲稱1973照片或同一歷史實袋。親讀AAJ S8原HTML及PDF59–60，1973事件／1974刊載、人工攀登、hammerless≠free／solo界線不動。

原生resolveLook／composeShotPrompt／Stage.imageKey等純函數：image-affecting params相等；composed SHA 59d3b8c894bdc31f8bdc92a721f3e8d7ad1008f2b659ca6887c77eda54998551；base54ff8953f25502f9；selection v1 key56004e358e0d7e9d。MiniMax image-01、1920×1080、1K、seed1/takes1、空cast/references/corrections與同look。literal HTTP只有shot_id場景欄不同，judge仍需各自接受。

原生新舊screenplay／runtime／backend-script逐bytes同SHA 02f091cae8f4e6179364155ef489b8ae59839efd969b695d21971d7b1ab5e3de。narrative22e4b5a76555fa87、speech e5fd2a0eb8489dbd不變；pictures改881022278d73ca13。native narrativeReviewMatches新舊皆true，只核既有record四個hash欄，未讀投票或重judge。

## 實資產仍待驗

現live media/cache.json及keyframes/manifest.json皆缺，未派送任何命令。第二teaser命令前先核已接受payoff cache及實檔SHA；missing/cache miss即停，不派購探cache。兩端judge／retake／trim不同則停pair，最終manifest及實檔必須同SHA才可render。actual_same_asset_verified=false；實圖、成片與無重購ledger均未驗。

## 逐句來源結果

103原句完整繼承經hash驗綁的R7逐句分類、來源及限定；本次新JSON保留完整basis與所有錨點。

| 句ID | 結果 | 來源／錨點 |
| --- | --- | --- |
| c09r5001 | CONFIRMED | S1、S2；S1:004, S2:029 |
| c09r5002 | ATTRIBUTED | S2；S2:029 |
| c09r5003 | PLAN | S2、S3；S2:025, S3:001 |
| c09r5004 | ATTRIBUTED | S2；S2:036, S2:043 |
| c09r5005 | PLAN | S2；S2:035, S2:036 |
| c09r5006 | PLAN | S8；S8:011, S8:012 |
| c09r5007 | PLAN | S2、S8；S2:043, S8:011, S8:019 |
| c09r5008 | PLAN | S2、S8；S2:030, S8:021 |
| c09r5009 | ATTRIBUTED | S4；S4:033 |
| c09r5010 | ATTRIBUTED | S4；S4:033 |
| c09r5011 | ATTRIBUTED | S4；S4:028 |
| c09r5012 | ATTRIBUTED | S4；S4:031 |
| c09r5013 | ATTRIBUTED | S4；S4:031 |
| c09r5014 | PLAN | S4；S4:033 |
| c09r5015 | ATTRIBUTED | S4；S4:033 |
| c09r5016 | ATTRIBUTED | S4；S4:033 |
| c09r5017 | PLAN | S4；S4:035 |
| c09r5018 | ATTRIBUTED | S4；S4:035 |
| c09r5019 | PLAN | S4；S4:035 |
| c09r5020 | ATTRIBUTED | S4；S4:035 |
| c09r5021 | ATTRIBUTED | S4；S4:035 |
| c09r5022 | ATTRIBUTED | S4；S4:035 |
| c09r5023 | PLAN | S4；S4:045 |
| c09r5024 | ATTRIBUTED | S4；S4:045 |
| c09r5025 | PLAN | S4；S4:045 |
| c09r5026 | ATTRIBUTED | S4；S4:045 |
| c09r5027 | PLAN | S1、S2；S1:004, S1:005, S2:027 |
| c09r5028 | CONFIRMED | S1；S1:002, S1:009 |
| c09r5029 | CONFIRMED | S1；S1:009 |
| c09r5030 | CONFIRMED | S1；S1:010 |
| c09r5031 | CONFIRMED | S1；S1:004 |
| c09r5032 | PLAN | S1；S1:018 |
| c09r5033 | CONFIRMED | S1；S1:018 |
| c09r5034 | CONFIRMED | S1；S1:018 |
| c09r5035 | PLAN | S1；S1:019, S1:021 |
| c09r5036 | CONFIRMED | S1；S1:019, S1:021 |
| c09r5038 | PLAN | S4；S4:008 |
| c09r5039 | ATTRIBUTED | S4；S4:008 |
| c09r5040 | ATTRIBUTED | S4；S4:008 |
| c09r5041 | PLAN | S2、S4；S2:029, S4:008 |
| c09r5043 | ATTRIBUTED | S2；S2:029 |
| c09r5044 | PLAN | S4；S4:008 |
| c09r5045 | ATTRIBUTED | S4；S4:008 |
| c09r5046 | ATTRIBUTED | S4；S4:008 |
| c09r5047 | PLAN | S2、S4；S2:030, S2:036, S4:010 |
| c09r5049 | ATTRIBUTED | S4；S4:007 |
| c09r5050 | ATTRIBUTED | S4；S4:007 |
| c09r5051 | ATTRIBUTED | S4；S4:006 |
| c09r5052 | PLAN | S4；S4:010 |
| c09r5053 | ATTRIBUTED | S2、S4；S2:030, S4:010 |
| c09r5054 | ATTRIBUTED | S4；S4:010 |
| c09r5055 | ATTRIBUTED | S4；S4:010 |
| c09r5056 | ATTRIBUTED | S4；S4:010 |
| c09r5057 | PLAN | S2；S2:030 |
| c09r5058 | ATTRIBUTED | S2；S2:030 |
| c09r5059 | ATTRIBUTED | S2；S2:030 |
| c09r5060 | ATTRIBUTED | S2；S2:030 |
| c09r5061 | PLAN | S2；S2:030 |
| c09r5062 | ATTRIBUTED | S2；S2:030 |
| c09r5063 | ATTRIBUTED | S2；S2:034 |
| c09r5064 | PLAN | S3；S3:005, S3:006, S3:007 |
| c09r5065 | ATTRIBUTED | S3；S3:001, S3:005 |
| c09r5066 | ATTRIBUTED | S3；S3:005 |
| c09r5067 | ATTRIBUTED | S3；S3:005 |
| c09r5068 | PLAN | S3、S4、S8；S3:005, S4:009, S8:011, S8:019 |
| c09r5069 | ATTRIBUTED | S3；S3:007 |
| c09r5070 | ATTRIBUTED | S3；S3:007 |
| c09r5074 | ATTRIBUTED | S3；S3:004 |
| c09r5075 | PLAN | S3、S8；S3:005, S8:011 |
| c09r5076 | ATTRIBUTED | S8；S8:002, S8:005, S8:011 |
| c09r5077 | ATTRIBUTED | S8；S8:005 |
| c09r5078 | PLAN | S8；S8:005, S8:007 |
| c09r5079 | ATTRIBUTED | S8；S8:005, S8:006 |
| c09r5080 | ATTRIBUTED | S8；S8:007 |
| c09r5081 | ATTRIBUTED | S8；S8:008 |
| c09r5082 | PLAN | S4、S8；S4:010, S8:008 |
| c09r5083 | ATTRIBUTED | S8；S8:008 |
| c09r5084 | ATTRIBUTED | S8；S8:010 |
| c09r5086 | ATTRIBUTED | S4、S8；S4:009, S8:011 |
| c09r5087 | ATTRIBUTED | S8；S8:011 |
| c09r5088 | ATTRIBUTED | S4、S8；S4:009, S8:017, S8:018 |
| c09r5089 | ATTRIBUTED | S8；S8:012 |
| c09r5090 | PLAN | S8；S8:012, S8:014 |
| c09r5091 | ATTRIBUTED | S8；S8:014 |
| c09r5092 | ATTRIBUTED | S8；S8:015 |
| c09r5093 | PLAN | S8；S8:014, S8:015 |
| c09r5094 | ATTRIBUTED | S8；S8:014, S8:015 |
| c09r5095 | ATTRIBUTED | S8；S8:016, S8:018 |
| c09r5097 | PLAN | S8；S8:015, S8:018 |
| c09r5098 | ATTRIBUTED | S8；S8:018 |
| c09r5099 | ATTRIBUTED | S8；S8:018, S8:019 |
| c09r5100 | PLAN | S8；S8:019 |
| c09r5101 | ATTRIBUTED | S8；S8:019 |
| c09r5102 | ATTRIBUTED | S8；S8:019 |
| c09r5103 | ATTRIBUTED | S8；S8:019 |
| c09r5104 | PLAN | S8；S8:019 |
| c09r5105 | ATTRIBUTED | S8；S8:019 |
| c09r5106 | ATTRIBUTED | S8；S8:019 |
| c09r5107 | PLAN | S8；S8:020 |
| c09r5108 | ATTRIBUTED | S8；S8:020 |
| c09r5109 | ATTRIBUTED | S8；S8:021 |
| c09r5111 | PLAN | S8；S8:014, S8:015 |
| c09r5112 | PLAN | S8；S8:019 |

5030仍是流程概述並保留外傾例外；5111／CTA仍是假設性觀眾問題，不冒Chouinard出版、授權或披露意願史實。

本輪必修：無。未改任何runtime、media、approval、字典、backend或Git。
