export default {
 id:'A21',
 hook_visual_reuse:[
  {setup:4,recovery:35,setup_paragraph:'H03',recovery_paragraphs:['E01'],reason:'同一稅務法庭案卷與匿名書記官圖；首次只預告審理，E01 才展開第一回合。'},
  {setup:5,recovery:55,setup_paragraph:'H04',recovery_paragraphs:['T01'],reason:'同一高院讀卷示意圖；H04 不放結果，T01 才接新讀法。'},
  {setup:6,recovery:67,setup_paragraph:'H04',recovery_paragraphs:['N01'],reason:'同一上訴法院三份文件圖；不畫三人互動，末章才給勝負。'}
 ],
 source_aliases:['S1','S2','S3','S4','S5','S6'],
 claims:{C01:[0],C02:[1],C03:[2],C04:[3],C05:[0],C06:[0],C07:[0],C08:[0],C09:[0],C10:[1,2],C11:[1,3],C12:[1,2,3],C13:[1,3],C14:[1],C15:[1],C16:[1],C17:[1],C18:[1],C19:[1,2],C20:[2,3],C21:[2],C22:[3],C23:[3],C24:[3],C25:[3],C26:[3],C27:[3],C28:[4],C29:[5],C30:[1],C31:[1],C32:[1],C33:[3]},
 claim_section_end:'## 四、可聽的Loops',
 boundaries:[
  '本集只說 2004 年秋改配方之後、案件內的 Regular Pringles；更早配方、Dippers 與其他系列不在範圍。',
  '1966-07-29 為專利申請日，1970-03-03 為核准日；核准文本中的生切片／馬鈴薯麵團是製法選項，不是早期商業配方證據。',
  '2007 稅務法庭、2008 高等法院、2009 上訴法院為三個不同裁判層級；示意人物與空白文件不冒充真人或庭審原件。',
  '42% 只指案件中的配方近似比例，沒有 50% 的法定門檻；不推廣為當今產品配方或一般稅務建議。',
  '2009 過往最多約一億英鎊、其後每年約兩千萬英鎊，均為判決記載的 HMRC 律師估額；沒有欠稅則是美聯社報導中的公司說法。兩者不互代。',
  '2025 Sensations Poppadoms 案只是後續引用此案方法，不是品客再審。',
  '內部來源取得狀態只留 source-map／審查證據，不能出現在觀眾卡片；旁白原文不因分鏡改寫。'
 ],
 loops:[
  {setup:['H01','H02'],payoff:['O02','O03','O04','O05','E03'],purpose:'圓筒先解運送與保存，再成為相似性論點之一；不說包裝造成訴訟。'},
  {setup:['H03'],payoff:['E01','E07'],purpose:'2007 法庭預告回收第一回合與稅率結果。'},
  {setup:['H04'],payoff:['T01','T02','T03','T04'],purpose:'2008 換讀法回收高院解釋與暫時勝訴。'},
  {setup:['H04','H05'],payoff:['N01'],purpose:'2009 三回合問題在末章第一段回答。'},
  {setup:['O07'],payoff:['I03','I06','E06','T02','N03','N03a','N04','N05'],purpose:'麵團中的馬鈴薯角色，逐步走到 made from 的法律判斷。'},
  {setup:['I08'],payoff:['N06','N07'],purpose:'稅款估額與是否欠繳分別作答，不把兩者合成債務。'},
  {setup:['E08'],payoff:['T02','T03'],purpose:'用馬鈴薯做成的讀法帶來高院轉折。'},
  {setup:['T05','T06','T07'],payoff:['N01','N02'],purpose:'上訴法院先檢查原法庭有無法律錯誤，再給最終結果。'}
 ],
 look_plans:[{id:'generic_package_designer',purpose:'包裝與製法以匿名設計員示意；不指定發明人肖像。'},{id:'generic_legal_reader',purpose:'三個法院層級使用不同書桌、文件與鏡位，僅匿名解說，不重建任何特定法官或律師。'}],
 claim_overrides:{C22:'T06 only replaces the ambiguous pronoun with 稅務機關, identifying HMRC as the appellant seeking restoration of the tribunal ruling. Same 2009 judgment source, no new factual proposition. Independent review of this adapted wording is pending.'},
 adaptation:[{
  paragraph_id:'T06',
  before:'這回他們要說服上訴法院，高等法院把這句話讀得太窄，而最初稅務法庭的判斷應該恢復。',
  after:'這回，稅務機關要說服上訴法院，高等法院把這句話讀得太窄，而最初稅務法庭的判斷應該恢復。',
  reason:'T05 ends with P&G defending its High Court win; name the tax authority explicitly in T06 so the following appeal argument cannot be misread as P&G seeking to reverse that win. Original v3 fullscript and first storyboard remain preserved.',
  source_cids:['C22'],
  active_worker_source_indices_zero_based:[3],
  review_status:'AUTHOR_CLARIFICATION_PENDING_INDEPENDENT_RECHECK'
 }]
};
