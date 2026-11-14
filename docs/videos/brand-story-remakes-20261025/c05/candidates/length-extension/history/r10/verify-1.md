# C05 金鳥蚊香｜R10獨立來源與書面配鏡查核

查核日：2026-10-25。查核者：`/root/c07_author`。本代理為R9獨立來源審查者，未撰寫或修改C05中文、prompt或研究，未讀任何blind/native敘事內容／答案。

**結論：SOURCE PASS／WRITTEN VISUAL PASS。** 116句、113插圖規劃及1原生結尾卡，共114景；不是生成圖、實聲或敘事panel驗收。

## 綁定輸入

| 檔案 | SHA-256 |
| --- | --- |
| video.json | `3cf768c449dc875e8fefbc04001879e0f6eacd3ad746de9a2146b4c844c6044c` |
| script.md | `ce4dff3e6d3dd9884448b46569cd63a86f1e124bd1211fbaf9aa2b52f7be8edc` |
| narration-only.json | `1578aa9ea4672daa034213b5c28848152002a557a013536aeff255e9179e34bc` |
| claims.json | `99325f782ccb4fc55901b009c1215805a231b2a5cc8bb44afc7325a21e1a2ee9` |
| claims.md | `e94a3dab479b1c8105f57b32843b67352bebcfc8ec7ff34c6a6b34df6ebc6229` |
| brief.md | `0694de8fa1a910344934b8c5084e53d3db219dcfa8453111f015d4c9309e30f6` |
| series.json | `a50d508be0af86d51636b5fd8437cd0eb0cf9dd4b085a92ff1e914f3266f9de7` |

新獨立收據：`reviews/source-r10-independent.json`，SHA-256 `1135935da4954d57484d9d99dd24746464c14d668086c939935f5d3b31675969`。
封存R9來源收據SHA `6c49ff1b3471dd03c1d16dde54bae7ff18e97588c7367d66464586de765c7e33`；verify SHA `20e9174afb30fa210849a056f22ab97257588993082c7538952d108d9ae1eb5b`。七份封存輸入、117句雜湊與115完整scene雜湊重核，原完整來源鏈保留。

## 直接差分核對

- 刪除c05r019的1888舶來粉／竹筒試作句與景；c07d02僅加後來，c07d03以這本書第五版承接書名。其餘114句、所有114留存prompt／camera／visual／emotion、原39組loops與非scene影片欄位完全同R9；章標只移到c05r020，留存句的章歸屬不變。
- 重新核NDL原書目／manifest：第五版，出版者上山英一郎，1897，作者欄空白；親讀原掃畫幅6前言p5的「明治三十年」（SHA `f579895cdb5861118d66983b94c7eaf93b5c489363ddc8d034e91c1528062a94`）。後來出版與1886／1887收成相容，沒有填成著者或說1880年代讀到1897版。
- 手冊段仍持續說這本書第五版、書裡、出版者、手冊、賣家立場；1897年仍在逐句來源scope。沒有把書中乾燥／製粉／保存寫成1887同一原料批或實際工廠流程。c07d18的形狀問題到c05r020是材料主題橋，後者另綁K_T線香製法回顧；未說手冊造成1890上市或1902量產，1958研究也未倒推1902或1955。
- 15組來源、62個當前不重複錨點、115個逐句引用、40份原件／抽文檔核hash與定位；所有留存source IDs／objects／anchors／claim kinds皆同R9。刪除1888句未留下懸空loop。
- brief／series有R10狀態、差分、字量與parent更新，未稱byteexact。原三份擴充研究、作者輸入及history未改；書面提示仍是匿名概念規劃，未驗收實際生成圖。

## 逐句來源結果

| 句ID | 結果 | 來源 |
| --- | --- | --- |
| c05r001 | PASS | K_T, K_F |
| c05r002 | PASS | K_T, K_F |
| c07o03 | PASS | EDITORIAL |
| c07o04 | PASS | K_F, NDL1897 |
| c07o05 | PASS | EDITORIAL |
| c07o06 | PASS | EDITORIAL |
| c07d01 | PASS | K_M |
| c05r013 | PASS | K_M |
| c05le001 | PASS | K_F |
| c05le002 | PASS | K_F |
| c07d02 | PASS | NDL1897 |
| c07d03 | PASS | NDL1897 |
| c07d19 | PASS | NDL1897 |
| c07d20 | PASS | NDL1897 |
| c07d04 | PASS | NDL1897 |
| c07d05 | PASS | NDL1897 |
| c07d06 | PASS | NDL1897 |
| c07d07 | PASS | NDL1897 |
| c07d08 | PASS | NDL1897 |
| c07d09 | PASS | NDL1897 |
| c07d10 | PASS | NDL1897 |
| c07d11 | PASS | NDL1897 |
| c07d12 | PASS | NDL1897 |
| c07d13 | PASS | NDL1897 |
| c07d14 | PASS | NDL1897 |
| c07d15 | PASS | NDL1897 |
| c07d16 | PASS | NDL1897 |
| c07d17 | PASS | NDL1897 |
| c07d18 | PASS | EDITORIAL |
| c05r020 | PASS | K_T, K_F |
| c05r021 | PASS | K_M, K_F, EDITORIAL |
| c05r023 | PASS | K_T, K_F |
| c05r024 | PASS | K_T, K_F |
| c05r025 | PASS | K_T, K_F |
| c05r026 | PASS | K_T, K_F, K_M, NM, NA |
| c07s02 | PASS | K_M, NM |
| c05r030 | PASS | K_M, NM, NA |
| c05r031 | PASS | K_M, NM, NA |
| c05r032 | PASS | K_M, NM, NA |
| c07s03 | PASS | NM, K_T |
| c05r036 | PASS | K_T, NM |
| c07s04 | PASS | K_M, NM |
| c05r049 | PASS | K_T, NM |
| c05r050 | PASS | K_T |
| c07s05 | PASS | CHEM2017 |
| c05le004 | PASS | NM_MACHINE |
| c05le005 | PASS | NM_MACHINE |
| c05r051 | PASS | K_T, NM_MACHINE, NM_COIL |
| c05r052 | PASS | K_T, NM_MACHINE, NM_COIL |
| c05r054 | PASS | K_T |
| c05r055 | PASS | K_T |
| c05r058 | PASS | K_S |
| c05r059 | PASS | K_S |
| c05r061 | PASS | K_S |
| c07s06 | PASS | K_S |
| c05r067 | PASS | K_T, K_40 |
| c05r068 | PASS | K_T, K_40 |
| c05r069 | PASS | K_T |
| c05r071 | PASS | K_T, K_40 |
| c05r073 | PASS | K_F |
| c05r074 | PASS | K_F |
| c05r076 | PASS | K_57, K_F |
| c07a01 | PASS | NSM_FULL |
| c07a02 | PASS | NSM_FULL |
| c07a03 | PASS | NSM_FULL |
| c07a04 | PASS | NSM_FULL, CHEM2017 |
| c07a05 | PASS | CHEM2017 |
| c07a11 | PASS | CHEM2017 |
| c07a06 | PASS | CHEM2017 |
| c07a07 | PASS | CHEM2017 |
| c07a08 | PASS | CHEM2017 |
| c07a09 | PASS | CHEM2017 |
| c07a10 | PASS | K_F, CHEM2017 |
| c05r091 | PASS | K_F |
| c05rx005 | PASS | K_F |
| c05rx007 | PASS | K_F |
| c07m01 | PASS | K_F |
| c05r092 | PASS | K_PROCESS_R5 |
| c5r5a01 | PASS | K_PROCESS_R5 |
| c5r5a02 | PASS | K_PROCESS_R5 |
| c5r5a03 | PASS | K_PROCESS_R5 |
| c5r5a04 | PASS | K_PROCESS_R5 |
| c5r5a05 | PASS | K_PROCESS_R5 |
| c05le010 | PASS | NM_MACHINE |
| c05le023 | PASS | K_PROCESS_R5 |
| c5r5a06 | PASS | K_PROCESS_R5 |
| c5r5a07 | PASS | K_PROCESS_R5 |
| c5r5a08 | PASS | K_PROCESS_R5 |
| c5r5a09 | PASS | K_PROCESS_R5 |
| c07m02 | PASS | K_PROCESS_R5, K_Q |
| c07m03 | PASS | K_Q |
| c05r080 | PASS | K_Q |
| c05r081 | PASS | K_Q |
| c05r082 | PASS | K_Q |
| c07u01 | PASS | K_Q |
| c07u02 | PASS | K_Q |
| c07u03 | PASS | K_Q |
| c07u06 | PASS | K_Q |
| c05r084 | PASS | K_Q, K_F |
| c05r085 | PASS | K_F |
| c05rx004 | PASS | K_Q, EDITORIAL |
| c05r088 | PASS | K_Q |
| c05r089 | PASS | K_Q |
| c05rx009 | PASS | K_F, EDITORIAL |
| c05rx010 | PASS | K_F |
| c05le012 | PASS | K_F |
| c07u04 | PASS | K_F |
| c05le013 | PASS | K_F |
| c05le014 | PASS | K_F |
| c05le015 | PASS | K_F |
| c07u05 | PASS | K_Q |
| c07u07 | PASS | K_Q |
| c07u08 | PASS | K_Q |
| c05r101 | PASS | K_F, NDL1897 |
| c05r102 | PASS | K_T, NM, K_Q |
| c05r103 | PASS | EDITORIAL, PROJECT |

## 保留HOLD

原生字量全片3306／開場152／開場後正文3154／有聲結尾99／扣結尾正文3055，較R9淨減26，僅規劃。沒有實際TTS秒數，正文720–840秒仍HOLD，不以算術範圍判時長PASS或FAIL。保留c05rx004原有非必要書面提示advisory，不為此改稿。未批准敘事panel、實圖／實聲／媒體、配音資格、字典讀音、owner或付費；無provider/backend/Git/spawn。
