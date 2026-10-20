# S50 R6｜七句音檢 HOLD 後的作者限縮修稿

2026-10-20 UTC。R5 [真實音檢](r5-audio.md)完整查核 119/119 句，兩輪限縮重錄後仍有 `fire015/020/032/039/062/078/099` 七句旗標；R5 音訊為 **HOLD**。R6 只改這七句口播及對應主張列，將 `fire061→062` 伏筆描述與地名同步；另將未改口播的 `fire019` 主張註解收窄，釐清佩皮斯日記沒有記珍妮站在窗邊的確切位置。這是**作者候選**，不替代新版獨立史料、書面畫面、兩位新讀者盲評、政策或真實音檢。

| ID | R6 新旁白 | 固定來源與讀音修正 |
| --- | --- | --- |
| `fire015` | 烈焰在橋邊停下，轉進泰晤士街，迎面是一排緊挨著的屋子。 | Vincent [V L2174–2206](https://github.com/textcreationpartnership/A64990/blob/e15ce8bba340e6089deec4ff85b486842e568434/A64990.xml#L2174-L2206)說火在橋邊受阻，轉進泰晤士街；以「烈焰」避開單字「火／或」同音。街屋緊密僅作環境，沒有指定哪戶被燒。 |
| `fire020` | 九月二日凌晨約三點，女僕珍妮叫醒佩皮斯，說城裡有場大火。 | Pepys [D L65788–65804](https://github.com/GITenberg/The-Diary-of-Samuel-Pepys---Complete_4200/blob/68fcf49f70ee793b989a6fd0464264d55beb4451/4200.txt#L65788-L65804)明說 Jane 叫醒並報火，**佩皮斯之後才走到她的窗邊**；R5「從窗邊叫醒」會使珍妮站位看似被記載，也使「窗／床」模糊，故刪去。 |
| `fire032` | 佩皮斯坐船經過倫敦橋，才看見熟人的房屋已經燒掉。 | Pepys [D L65820–65835](https://github.com/GITenberg/The-Diary-of-Samuel-Pepys---Complete_4200/blob/68fcf49f70ee793b989a6fd0464264d55beb4451/4200.txt#L65820-L65835)記乘船 `through bridge`，並見 Michell 家已燒；明說主詞與船行以避開「船過／穿過」、「他／她」的轉寫混淆。 |
| `fire039` | 河岸的貨物也能助燃，火勢不必只靠相連的房屋蔓延。 | Vincent [V L2191–2206](https://github.com/textcreationpartnership/A64990/blob/e15ce8bba340e6089deec4ff85b486842e568434/A64990.xml#L2191-L2206)寫泰晤士街的可燃物；Pepys [D L65835–65877](https://github.com/GITenberg/The-Diary-of-Samuel-Pepys---Complete_4200/blob/68fcf49f70ee793b989a6fd0464264d55beb4451/4200.txt#L65835-L65877)記油、酒等。這是助燃機制，不稱逐戶延燒曾被目擊；去掉聽不清的「一戶火」。 |
| `fire062` | 倫敦塔旁堆滿家當，人潮堵得連小門都過不去。 | Pepys [D L65956–65989](https://github.com/GITenberg/The-Diary-of-Samuel-Pepys---Complete_4200/blob/68fcf49f70ee793b989a6fd0464264d55beb4451/4200.txt#L65956-L65989)記 Tower Hill 堆物、postern 因人群無法通行；「倫敦塔旁」避開「塔丘／卡車」。既有 Tower Hill 畫面提示詞仍相符。 |
| `fire078` | 房屋損失再大，也不能把它說成整座城都燒光。 | 1667 刊本 [A L153–170](https://github.com/textcreationpartnership/A63385/blob/4ac29739d661a1c7f2a34f51ffb8a1811176f146/A63385.xml#L153-L170)在燒毀總數旁列城牆內未燒 75 英畝 3 roods；此句只限制推論，不再念一次 `fire077` 的數字，避開「未燒／未銷」和「整城／整層」。 |
| `fire099` | 屋主回答：不可能，風根本吹不動那堆餘燼。 | 1667 刊本 [A L465–480](https://github.com/textcreationpartnership/A63385/blob/4ac29739d661a1c7f2a34f51ffb8a1811176f146/A63385.xml#L465-L480)將無風可擾煤燼的說法歸於屋主 Farryner；以前句的屋主身分接答，避開專名「法里納／法麗娜」同音，仍只作其事後證詞。 |

R5→R6 的 `video.json` 只有七個 `lines[0].text` 與 `fire061→062` 的一個 `what` 改動；119 個 ID、景序、113 個 `shot.data.prompt`、卡片、縮圖、頻道旁白設定、配樂設定、YouTube 說明與連結均未動。`claims.md` 只有七列口播及各自註解、加 `fire019` 的來源界線註解改動；`script.md` 由 CLI 重生。`brief.md`、`research.md` 逐位元未改。固定原文字節 SHA：Pepys `3cd43a3c39ee72eb9c4a3657f1fcb1723afba291cedac176c65a39289483be5d`、A `0a4b379b932fc331c9ff10bd217e6d8b2cc513388a3fd73d7f64f0b35447595e`、Vincent `36798f66f98c32482b09209d7acb0ed204bacae744b5eae7c40532ca7a093f29`。

| R6 精確內容檔 | SHA-256 |
| --- | --- |
| `brief.md` | `bac9d05082626689833057f30718c0f9d6d798562460335c8bcb834216ed1a3b` |
| `research.md` | `27f9df563ab8376d2f6ee10837772821534515fd29b86b7e83e259eb56023a95` |
| `claims.md` | `1006cfea670965d23618cd5de939f7ce70ad3d9731289ea72102916faaa3fc7a` |
| `video.json` | `f231e8bd4118adb40d5c49974dd24747b8bb0cfb1de8528d4735127ca291e892` |
| `script.md` | `a988c497ac8cc46cc4a80a7e3f268aff62c4ad9dfcd89f5bc8b87c505f1989b7` |

作者本地核對：119/119 口播、`claims.md` 和 `screenplay(doc)` ID／順序／字面一致；113/113 個 `shot` 提示詞非空，29/29 條伏筆 setup 在 payoff 前，`lint --slug curio-s50 --json` **0 errors／1 warning**（原 R5 片尾沒有口頭訂閱提醒；畫面 CTA 仍在）。預估 250／300／325 CPM 時，濃縮開場分別 **48.23／41.40／38.97 秒**，正文 **10:44.73／9:14.00／8:41.53**；最快仍過 8 分鐘，這些不是 R6 配音實長。`git diff --check` 通過。R5 的實測音長與 R5 政策、站台劇本卡均綁舊稿，不能移作 R6 放行。Gazette 與 London Museum 在本環境仍是 P17 衍生查核，不能宣稱已直接重開官網。

**下一關：**另一位工作者按上表精確五檔與固定原文獨立核七句及書面畫面；兩名此前未讀 R6 的隔離讀者只看新 `script.md` 按固定 13 題盲評。若同版兩關通過，再重做完整 Jev 政策與站台劇本流程，只合成改動句並作全片 119 句零旗標音檢。未製作插畫、配樂或成片。
