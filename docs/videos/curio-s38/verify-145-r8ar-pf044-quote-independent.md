# S38 R8ar PF044 引文卡：獨立來源／書面畫面覆核

2026-10-22 UTC；不同作者 reviewer policy_duration_incremental_review。**PASS**：這是書面來源卡覆核，不是三張失敗原圖變成KEEP。pf044 累計3 actual、0 remaining，禁止第四張；本次未改media／manifest或付費。

## 固定原文

直接重開 `/tmp/curio-s38-pepys-4200.txt` L65917–65934 並驗 SHA `3cd43a3c39ee72eb9c4a3657f1fcb1723afba291cedac176c65a39289483be5d`，與research固定GITenberg commit68fcf49f70ee793b989a6fd0464264d55beb4451相符。D2c L65925–27原文為：`houses were burned by these drops and flakes of fire, three or four, nay, five or six houses, one from another.`

卡上「相隔三四間，甚至五六間」保留其距離描寫的近似數與遞進；副文「飛散的火星，點燃另一處房屋」概括火滴／火片跳燒，未新增每處精確間距、唯一機制或全市統計。kicker清楚標佩皮斯日記・中文譯文；這是有歸屬的原文節譯，不假裝可驗證的現場測量或中文原稿。符合原旁白「那些火星甚至讓相隔好幾間的房屋接連著火。」

## 相容與比例

- verify144精確old/new只涉及pf044 template/data，由shot改big引用卡；當前卡內容與new完全一致。112句仍逐字存在正式script與claims；原pf044口播未更改。此覆核未作任何口播改寫。
- 112 scenes中98 shot、13 big、1 outro；排除outro的正文插圖98/111=88.29%，高於70%。最長連續非shot為3；pf044前pf043、後pf045均shot，新增卡不造成長串卡片。
- 獨立重跑 `node tools/video/cli.mjs lint --slug curio-s38`：0 errors／0 warnings，112 lines。script正式重產後全文匹配當前112句。
- 引文卡沒有新生成文件／申請表／精確現場布局，並非以原創卡通充作證據。史料層次仍為Pepys近時代第一人稱日記及後來轉錄，不升格為每位倫敦人的經驗。

## SHA-256綁定

- `video.json`：`fde1ddb2bba417d7e96747fdb3dec68adb42a7b502c988e11f1724e518ea7136`
- `script.md`：`d435a49db4895bd356e63a899b974701012a9d66346f136afc02e3bfa2785542`
- `claims.md`：`b1a86f5161280e48027cfb6ba1716a8a9eaf0136326a0b4120477507a3c6b02e`
- `research.md`：`f838518cf2c4ab23de91021ae6024d9431f907866c14301466ca0a06bb3ecdfe`
- `verify-144-r8ar-pf044-quote-author.json`：`28b10e1663aa3c35602be141e23e77b8563735b16ab5ae9479711644d1b53bf2`
