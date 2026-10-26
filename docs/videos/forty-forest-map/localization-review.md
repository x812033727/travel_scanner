# ForTy 八語與繁中交付進度

最新事實：正式官方v4主片與EN、JA、KO、VI四個已驗M4A已送後臺，繁中及這四語的實際對時CC／完整標題說明也已送達並讀回。外語三部件交付4／8；新final pending、原生QA false10／11；正式八語batch／package與overall仍未完成。詳細SHA見[主結果](production-result.md)與[安全收據索引](receipts/official-v4-20261026/README.md)。

| 語言 | 實際文字／音訊 | 當前CC與標題說明下載 | 保留限制 |
| --- | --- | --- | --- |
| zh-TW | 原版92句MASTER PASS；非外語計數 | 97 narration cues／SRT+VTT+TXT均已交 | 新QAfalse10，不能以舊QA11取代 |
| en | current92／92、0flags、89fit；新品牌版M4A已交 | 98 current-dub cues／0CPS提示；完整TXT已交 | 非全八語ready |
| ja | current92／92、0flags、89fit；新品牌版M4A已交 | 121 current-dub cues／0CPS；完整TXT已交 | 原retake／縮句／改詞歷史保留 |
| ko | current92／92、0flags、89fit；新品牌版M4A已交 | 114 current-dub cues／1CPS；完整TXT已交 | dkq3 owner-exception reword3獨立記錄，未改回round2 |
| es | 92句審稿；較早502未知request仍held，無current checked交付 | narration-fallback初稿／stale hard error／9CPS；不送ready資產 | 9a36與journal3935不得replay或清除 |
| pt | 原文retake1一次v3恢復真exit3；0local raw變更，計費未知 | narration-fallback初稿／stale hard error／8CPS；未交 | 新held3cc1/b9d12；R1=1、shorten2、reword0不變 |
| id | 92句審稿文字；無已驗M4A | narration-fallback初稿／1CPS；未交 | 必須真合成、音檢及獨審 |
| vi | current92／92、0flags、89fit；新品牌版M4A已交 | 101 current-dub cues／16CPS；完整TXT已交 | 原兩次原文retake與四句等義reword保留 |
| th | 92句審稿文字；無已驗M4A | narration-fallback初稿／0CPS；未交 | 初稿不等於已驗交付 |

九語原生CC都是真實目前presentation重建，5已交語各完整92來源ID；全部35CPS（已交17）與ES／PT兩個stale錯誤原樣保留。沒有把其他四語初稿當ready，也沒有重新送native final夾帶未音檢fitted dub。章節00:00／00:27／02:05／02:57／04:38／07:03／08:26只套一次正常官方位移。

四條新M4A用已驗舊body raw／cache零TTS包上官方5＋21秒，正常native cachedcheck再核完整intended／currentWAV／cache裁決，獨審368句與currentM4A／fit／meter。這不是新ASR、第二次Jev或全M4A人工聽完；現有ASR與失敗歷史沒有清除。原四份BODY音檢與交付檔仍是歷史版本，見[舊文件封存](history/before-official-v4-doc-refresh-20261026/README.md)。

EN最高tempo1.21、JA1.19、KO1.14、VI1.10；皆0skip／keep-fitted。KO原兩輪retake／兩輪標準reword後一flag，經站主持續委派採dkq3單句owner-exception reword3，6개→여섯 범주、保留唯一最大值，新合成1句26字且其他91raw不變；當時byte-scope不是ASR PASS，之後真nativePASS才採用。VI兩輪原文retake＋一輪四句reword、JA及EN原先縮句／改詞／重錄的全部失敗與上限保留，未因重封裝重置。

PT v3開始06:50:04.672149Z、結束06:50:36.418431Z／PID258624／exit3，stage無完成；native失敗文字是Mokaair HTTP502，上游provider結果與計費未知，0localWAV不能稱0charges。原driver270e與root更正bdd531分開保留；新holdad19及舊holdE8ac archive全留。即使07:50時間到了也不能重送3cc1或較早ES9a36，須真實每request結果／usage或可恢復答案及另行有界授權。[PT摘要](receipts/official-v4-20261026/PT-v3-unknown-provider-outcome.summary.json)沒有rawjournal或provider憑證。

原版b293的server final56c69為真approved12角色／QA11；新品牌版95bd為pending37角色／QA10。兩者與所有oldpayload／choices／決策分開保留。交付核驗限server組裝SHA／size加登入後角色metadata，不聲稱remote binary重下載。所有八語預設、推薦決策與後臺增量交付授權仍有效；未上傳公開YouTube／merge／deploy。

獨立翻譯及預算審查仍見[localization/](localization/)，來源與教學數字、否定、六類／250總量、年份及未親測限制未變。[production-decision.md](production-decision.md)保留原始推薦採用；[機器進度](production-progress.json)記錄未完成項。
