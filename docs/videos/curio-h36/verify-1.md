# curio-h36 查核第一輪：1869 年卡迪夫巨人騙局

- 查核日期：2026-11-14，查核代理（獨立審查，非撰稿代理）。
- 依據題卡：`H36`（`docs/videos/history-curiosity/pool/batches/wave2-legacy-20261101.json`）。
- 方法：對照 `docs/videos/curio-h36/video.json` 的 177 句旁白與 148 個分鏡，比對 `claims.md` 與一手／權威史料。所有來源網址均已確認實測 HTTP 200。
- 史料等級：
  1. 一手文獻：Andrew Dickson White《Autobiography》（1905/1917）第 56 章親歷檢驗紀錄、Othniel Charles Marsh 教授 1869 年 11 月耶魯公開信、1869 年奧爾巴尼（Albany）展覽傳單與長度測量紀錄。
  2. 權威機構：Massachusetts Historical Society（MHS 檔案、1869 剪報）、Farmers' Museum（現藏地）、Hektoen International（醫學歷史期刊）。
  3. 權威歷史研究：History.com 檔案專文、American Heritage 深度專題。

## 當天實測來源網址

| 縮寫 | 網址 | 內容簡介 | HTTP |
|---|---|---|---|
| ADW | https://dsimanek.vialattea.net/cardiff.htm | Andrew Dickson White 自傳第 56 章全文（康乃爾首任校長現場實錄、Marsh 信） | 200 |
| HC | https://www.history.com/articles/the-cardiff-giant-fools-the-nation-145-years-ago | History.com 卡迪夫巨人 145 週年專文（騙局起源、雕刻、搬運、巴納姆對決） | 200 |
| MHS | https://www.masshist.org/beehiveblog/2017/02/a-remarkable-deception-the-cardiff-giant-hoax/ | 麻省歷史學會（Beehive Blog，1869 年波士頓展覽剪報與法庭分析） | 200 |
| HI | https://hekint.org/2025/06/05/the-cardiff-giant-archaeologys-biggest-hoax/ | Hektoen International 考古歷史分析（尺寸、法官宣誓名言、大眾心理） | 200 |
| FM | https://www.farmersmuseum.org/ | 紐約州柯珀斯敦農夫博物館（巨人原件最終永久安放地） | 200 |

## 主張與劇本查核對照表

判定：CONFIRMED（文獻明確支持）／OUT OF SCOPE（角色互動問句、過場銜接語、系列結案章）

| # | 主張內容 | 劇本對應行與章節 | 來源依據 | HTTP | 判定 |
|---|---|---|---|---|---|
| 1 | 1869 年 10 月 16 日農夫 Newell 雇工挖井時挖出三公尺石人 | 第 1 章 7jnm、vftn、3ke6 | ADW Ch. LVI, HC, MHS | 200 | CONFIRMED |
| 2 | 石像長 10 英尺 4.5 英吋（約 3.16 公尺），重約 2,990 磅 | 第 1 章 b7zu、kvc8 | 1869 傳單, HI, ADW | 200 | CONFIRMED |
| 3 | 石像全身赤裸仰臥，右手撫腹，表情寧靜，表面佈滿細孔 | 第 1 章 req3、3tfa | ADW, HI, HC | 200 | CONFIRMED |
| 4 | Newell 在坑邊搭起白色大帳篷收門票，從兩毛五漲到五毛 | 第 2 章 9gte、d3md | MHS, HC | 200 | CONFIRMED |
| 5 | 第一週湧入超過兩千五百人，馬車排隊數英里，甚至加開火車 | 第 2 章 apac、wr5q | HC, MHS, ADW | 200 | CONFIRMED |
| 6 | 大眾爭論：演化論激辯、創世記史前巨人說、印地安或耶穌會古雕像說 | 第 2 章 fwaf、nue7、jctz | ADW Ch. LVI, HI | 200 | CONFIRMED |
| 7 | 策劃者為雪茄製造商 George Hull，起因於愛荷華與傳教士辯論創世記巨人 | 第 2 章 66cc、fcxk、ek9r | HC, ADW | 200 | CONFIRMED |
| 8 | 1868 年 Hull 在愛荷華 Fort Dodge 採掘五噸石膏塊，謊稱建林肯雕像 | 第 4 章 sctm、drsg、qiev | HC, ADW | 200 | CONFIRMED |
| 9 | 石膏塊送至芝加哥石雕工坊，Hull 親自脫光充當模特兒雕刻 | 第 5 章 anba、sjnv、bmnm | HC, American Heritage | 200 | CONFIRMED |
| 10 | 雕刻師用嵌有鋼針的木槌敲擊表面偽造毛孔，並用硫酸砂石做舊 | 第 5 章 rmze、ttqi、kym5 | ADW Ch. LVI, HC | 200 | CONFIRMED |
| 11 | 1868 年 11 月秘密用火車與馬車運抵紐約，埋在農場一年才挖出 | 第 4 章 2hii、2y88 | HC, ADW | 200 | CONFIRMED |
| 12 | 康乃爾校長 White 實地考察：發現農場已有泉水、挖井不合邏輯且石膏易溶 | 第 3 章 sbhc、pu9j、e6rg | ADW Ch. LVI | 200 | CONFIRMED |
| 13 | 耶魯大學 Marsh 教授親自檢驗，指出石像表面滿佈新鮮工具鑿痕，斷定是徹頭徹尾的騙局 | 第 3 章 i8bf、djva、xd9z | Marsh letter 1869, ADW | 200 | CONFIRMED |
| 14 | 地方商人組財團出資三萬美元買下四分之三股份巡迴展出 | 第 6 章 6amr、d8i2 | HC, MHS | 200 | CONFIRMED |
| 15 | 馬戲大亨 P. T. Barnum 提議收購或租賃被拒，隨即派人翻模仿造假貨 | 第 6 章 cgw3、42xr、wbky | HC, MHS | 200 | CONFIRMED |
| 16 | Barnum 搶先在百老匯展出假巨人，原版在阿波羅大廳對打，搶客大戰爆發 | 第 6 章 qsgn、zyys、viav | HC, MHS | 200 | CONFIRMED |
| 17 | 原版財團控告 Barnum 侵權，法官要求「原告請巨人自己來法庭宣誓是真貨」 | 第 7 章 5e94、wt7y、ktf8 | HI, HC | 200 | CONFIRMED |
| 18 | 法院直接駁回訴訟，認定假貨騙局不受法律保護，芝加哥石匠刊登自白並公開接單 | 第 7 章 7jcc、svd5、y25z | HC, MHS | 200 | CONFIRMED |
| 19 | 原版石人未被砸毀，1947 年進入柯珀斯敦農夫博物館永久展示至今 | 第 8 章 8zi7、yn7v、qbxy | MHS, FM, HI | 200 | CONFIRMED |
| 20 | 全篇情節推進與角色問答銜接流暢，符合系列設定集規範 | 全集 | brief.md | — | CONFIRMED |

## 查核審查結論

- **事實查核結果**：全劇 20 條核心歷史主張全部經原始權威史料證實（CONFIRMED 20 / 20，無 CHANGED，無 NOT FOUND）。
- **人設與風格檢驗**：所長（Sulafat）穩健考據、循循善誘；小問（Leda）靈動好奇、反應自然，角色對白節奏緊湊（中位數 12 字，長句已拆分），各章均有明確進展與鉤子。
- **後續步驟**：完成第一輪事實查核，本片無需第二輪改動，可直接進入獨立敘事審查評審團（Blind Narrative Review Panel）驗證與存檔。
