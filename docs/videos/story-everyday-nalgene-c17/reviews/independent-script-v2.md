# C17 Nalgene｜v2 逐句來源與配鏡獨立覆核

**結論：旁白來源 69/69 PASS；配鏡文字 67/69 PASS、2/69 HOLD。整體暫緩站主劇本／逐鏡關卡。** 本收據只審文字與配對畫面，未生成圖片、配音或成片；69 句正文的實際 TTS 時長與插圖時間占比尚未量測。這也不是兩位只讀旁白盲讀。

## 綁定版本

- 作者草稿 PR #1703，讀回 head `c50e59e3cdf3c9270a65f50e0c7b09f307eaa9bd`。
- `script.md` SHA-256 `5B1ADE1DA22D04131627C6EC2E6A62BA222428F58D1765D1ABAABD3D6E2357A9`。
- `script-source-notes.md` SHA-256 `E89AE30074A09BA68A2D0C29760691CCFBBA82C3F89883AEBD45501471C1E8EB`。
- `visual-plan.md` SHA-256 `7DC6C943FC8967AFD0B448A8AB460A354AEF4A754DCBF2ECFFB6460DDDA5CEB7`。
- `visual-plan.json` SHA-256 `5193C8DB8144F1028B7CB85B1F19BE80316A62694391D58291DEF00FD0634A85`。
- 程式比對：劇本 69 個 ID 與 JSON 69 鏡一一對應，61 鏡 image、8 鏡 card；JSON 旁白與劇本欄、JSON prompt／card_text 與分鏡 Markdown 欄均 69/69 逐字相同。

## 逐句來源：PASS

逐句讀 H01–H07、O01–O12、I01–I11、E01–E11、T01–T13、N01–N15 與作者來源欄，再直接重開原發行者材料。H01–H03、O04、I05 等為明示泛用情境，不冒充特定歷史現場；其餘事實句在下列界線內有直接依據。

| 台詞群 | 直接讀回的材料與判斷 |
| --- | --- |
| H04、O01–O03、O09–O12 | [Nalgene／Thermo Fisher 2019 年新聞稿](https://india.newsroom.thermofisher.com/press-releases?item=123305)正文將 1949 年界定為 Nalge 在 Rochester 的實驗室器皿起點；稿首「1949 水瓶」的宣傳導語沒有被旁白寫成戶外瓶當年上市。 |
| O06–I11、E01–E09 | [品牌事後回顧](https://nalgene.com/our-story/)稱 1960 年代自家科學家帶實驗瓶健行；[2019 年新聞稿](https://india.newsroom.thermofisher.com/press-releases?item=123305)記載當地戶外使用擴散、1970 年代中期消費品部門與後來運動、校園場景。旁白 I01、I03 明示公司回顧，不指名首位發現者或單趟行程。E01 說「七〇年代中期」而不定首賣年份。 |
| H06、E11、T01–T12 | [Nalgene 2008 年原公告轉刊](https://www.chemicalonline.com/doc/nalgene-tto-phase-out-production-of-consumer-0001)標 `SOURCE: Nalgene`；原文是未來數月逐步停產 Outdoor 含 BPA 的聚碳酸酯容器，同時保留公司當時的安全立場及已上市 Everyday／Tritan 款。旁白沒有改寫成當日全部停產、召回或醫學致害結論。 |
| T13、N01–N08 | [2020 年 Nalgene／Thermo Fisher 發表稿](https://india.newsroom.thermofisher.com/2020-08-06-Nalgene-Outdoor-Is-First-to-Market-with-Reusable-Water-Bottle-Made-from-50-Transformed-Trash)記載初始 32 oz 寬口 Sustain、Tritan Renew，腳註明示 ISCC 質量平衡分配；[Thermo Fisher 技術表](https://documents.thermofisher.com/TFS-Assets/LPD/Reference-Materials/nalgene-sustain-bottles-green-facts.pdf)與[Eastman 2020 報告印刷頁 30–32](https://www.eastman.com/content/dam/eastman/corporate/en/media-center/resources/eastman-sustainability-report-2020.pdf)明確把它解釋為供應鏈帳目分配。N05 是隨即被 N06–N07 糾正的可能誤會，沒有把每只瓶子物理切半當事實。 |
| N09–N15 | [Nalgene 現行 FAQ](https://nalgene.com/faq/)稱「目前多數」採 Tritan Renew；N09 留了 2026 年查閱時點，不回推舊瓶。N10–N13 是前述來源界線內的回收，N14–N15 是留言／訂閱邀請。 |

所有起源、性能與產品變化來源主要是品牌、母公司及樹脂供應商材料；審查只認為**台詞符合其可讀原件與歸屬**，不把行銷的全球第一、減碳或醫學安全口號升格為獨立實證。

## 配鏡：兩處 HOLD

| ID | 現有畫面與旁白差異 | 窄修建議 |
| --- | --- | --- |
| E06 | 旁白只問「它離開山路後，下一個會出現在哪裡？」；畫面卻同時畫出室內運動場與校園桌面，提前給出 E07 才回答的兩個地點。 | 改成通往**未顯示目的地**的室內門或岔路，讓 E07 再出現運動與校園。MD 與 JSON 同步。 |
| T04 | 旁白特別說 2008 年是**停產計畫的宣布**，不能當成舊瓶已消失；現有畫面把瓶子沿時間線「逐漸淡出」，仍像在陳述執行結果。 | 改成無字公告旁的**虛線未來箭頭／尚未落實的計畫**，瓶子保持可見；不要畫已下架的結果。MD 與 JSON 同步。 |

其餘 67 鏡的圖像／字卡方向與同 ID 旁白相符。尤其 T03 限定 Outdoor 含 BPA 聚碳酸酯款，N04 的 50% 卡已帶「認證回收來源分配」，N05–N08 未畫每瓶物理對半。概念畫面不能生成商標、可讀字、當年實物照片感或特定真人；成圖仍需逐張驗收。字卡張數 8/69 不是時間占比 70% 的證明。

**下一步**：作者只改 E06、T04 的 MD／JSON 配鏡，保持旁白與來源註記不變；同一獨立審查者重新核對差分及四份新雜湊。兩位只讀旁白盲讀也須綁定最終旁白字節。之後才可提交站主劇本與逐鏡採用關卡；這份收據不含任何付費核准。
