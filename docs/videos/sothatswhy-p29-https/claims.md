# 主張與來源（sothatswhy-p29-https）

對應 [`brief.md`](brief.md) 的「查核清單」。每一條列出片中怎麼說、來源原文與注意事項，並標出它是
**官方規格**、**官方說明**、**教材**、**撰稿推論**，還是**比喻／示意**。撰稿只能用「可用說法」裡的數字與說法；逐行查核見 `verify-1.md`（第一版 193 句）與 `verify-2.md`（盲評改寫後）。

**行號**以現行 `video.json` 為準（p001–p178，2026-11-13 照頻道新規則刪小問的捧場句後重編；`script.md` 是它的可讀版）。2026-11-13 之前的行號是 p001–p192（2026-11-12 盲評改寫後），`verify-1.md`、`verify-2.md` 用的是那時或更早的行號；下面這段講的是 2026-11-12 那次改寫。第一版的行號在改寫時失效：舊 p024「每個經手的人都能打開看，甚至改幾個字再傳下去。」與舊 p185「寄給誰，要我自己看清楚！」刪掉，舊 p025–p184 全部往前移一號，p179 是新加的句子，收尾重寫。下面每一列的行號與引用的台詞都已對過現行 `video.json`。

2026-11-12 撰稿時當天重讀每一個來源（引文是原句）：
- RFC 8446、RFC 9849、RFC 5280、RFC 9110：rfc-editor.org 純文字正式版，curl GET 200（337,736／112,500／352,580／502,941 bytes），逐段讀。
- Let's Encrypt〈How It Works〉（頁首 Last updated: August 2, 2025）與〈Chains of Trust〉、certificate.transparency.dev〈How CT works〉：curl GET 200，HTML 轉純文字。
- Chromium Blog 2023-05-02〈An Update on the Lock Icon〉：curl GET 200，取 post-body 全文。
- Google Chrome 說明〈Check if a site's connection is secure〉（support.google.com/chrome/answer/95617，2026-11-12 版）：curl GET 200。
- MDN〈HTTPS〉詞彙頁、〈How does the Internet work?〉：curl GET 200。
- Google Chrome 說明〈Manage warnings about unsafe sites〉（support.google.com/chrome/answer/99020，`hl=en`）：2026-11-12 改寫 p165 後 curl GET 200，HTML 轉純文字（C24）。
- 素材審視 `material-20261111-round3` 的 T53-001～011 與 `pool/batches/wave53-tech.json` 只當線索；這裡每一條都重開來源。方括號數字對應文末〈來源〉。

**A55 的舊來源怎麼處理**（企劃要求重讀或不用）：
- Chromium 2023〈An Update on the Lock Icon〉：**重讀，有用**（C09、C10）。
- Chromium 2018〈A secure web is here to stay〉：重讀（2026-11-12 curl 200），內容是 Chrome 68 把 HTTP 標成「Not secure」與 2018 年的加密比例；**片中沒有用**（跟「多一個 S 差在哪」無關，年份與比例只會增加數字）。
- Let's Encrypt 2015〈Our First Certificate Is Now Live〉：重讀（200，2015-09-14 發出第一張憑證）；**片中沒有用**（歷史岔題）。
- Google 2025〈HTTPS by default〉：security.googleblog.com 的網址現在轉到 blog.google，curl 只拿到頁面框架、讀不到正文；**不用**。
- RFC 8446（A55 唯一講機制的來源）：重讀全文相關段落，見各條。

**本集刻意不做的事**：不念 SNI、ECH、DNS、IP、0-RTT、close_notify、CertificateVerify、Finished、AEAD 這些名字（片中都用信件比喻的話說）；只念 HTTPS 和 TLS。
不講數學、不講公式（調顏料明說是比喻）；不講 TLS 1.2 以前的握手；不講用戶端憑證、PSK 細節、OV/EV 憑證；不說哪些網站開了「搶先送出」（0-RTT）；
**不說 ECH 已經普及**（沒有部署比例的來源）；不說瀏覽器現在一定畫鎖頭（Chrome 2023 年宣布換掉，片中照實說）。

**簡化清單**（協定簡化要明列，企劃要求）：
1. 握手只講三件事：先交換金鑰（調顏料）、伺服器用私鑰簽整段握手（蓋章）、雙方 Finished（對帳）。省掉 EncryptedExtensions、CertificateRequest、HelloRetryRequest、PSK 與用戶端驗證。
2. 憑證鏈只講「一層蓋一層到內建的根」，不講撤銷、名稱限制、路徑建構。
3. 「封條」＝ AEAD 加密與驗證合一；「編號混進封條」＝序號與 IV 混成 nonce。
4. 「這次調出的顏色用完就丟」＝暫時性 (EC)DHE 金鑰與前向保密，只在憑證模式下成立（PSK-only 不在範圍）。
5. 「出發前那一問」（p037 問「查詢處」）＝ DNS 查詢；「信最後送到哪一台網站的機器」＝伺服器的 IP 位址（一個位址背後不一定只有一台機器，見 C23）；「信封外面的收件人」＝ ClientHello 的 SNI。

## C01 資料要經過不是你的機器：咖啡店的無線網路機器、網路公司、一站轉一站的轉送電腦【教材】

- **可用說法**：p005、p011–p013、p018–p019
- **來源**：[11]
- **原文**：MDN [11]：「we divide computers into separate local networks and connect these networks using a device called a router」「the commercial router in your home is likely a combination of a switch, a router, and a modem」「An ISP is a company that manages some special routers that are all linked together and can also access other ISPs' routers. So the message from our network is carried through the network of ISP networks to the destination network.」
- **注意**：MDN 說的是家裡的路由器；咖啡店的無線網路機器是同一種東西（Chrome 說明 [9] 也提到 cafe 的 public Wi-Fi）。「好多台」不給數字。

## C02 沒有加密的連線：別人可能看到、也可能改掉你傳的東西【官方說明】

- **可用說法**：p020–p022（p020 小問「信沒封起來的話……」，p021–p022 所長轉述 Chrome 說明）
- **來源**：[9]
- **原文**：Chrome 說明 [9]，Info or Not secure：「The site doesn't use a private connection. Someone may be able to view and change the information you send and get through this site.」
- **注意**：「可能」照原文的 may。p021「沒有私人連線的網站」是 private connection 的說法，跟繁中版說明的用字（「網站未使用私人連線」，verify-1／verify-2 讀過）和 p082 的整頁警告「你的連線不是私人連線」一致；第一版寫「私密」，verify-2 G01 改掉。第一版另有一句比喻「打開看，甚至改幾個字再傳下去」，已刪，「看得到、改得掉」只由 p022 轉述的說明交代。

## C03 TLS 的規格假設路上的人可以完全控制網路【官方規格】

- **可用說法**：p024–p026
- **來源**：[1] §1
- **原文**：「These properties should be true even in the face of an attacker who has complete control of the network, as described in [RFC3552].」
- **注意**：p024「大部分是。可是你沒辦法挑，誰來幫你傳。」是撰稿的口語橋接；不說路上的機器真的在偷看。

## C04 HTTPS 的 S 是 Secure；HTTPS 是用 TLS 加密的 HTTP；加密＝只有你和對方看得懂【教材＋官方規格】

- **可用說法**：p025、p029–p031
- **來源**：[10]、[1] §1、[4] §4.2.2
- **原文**：MDN [10]：「HTTPS (HyperText Transfer Protocol Secure) is an encrypted version of the HTTP protocol. It uses TLS to encrypt all communication between a client and a server.」
  RFC 8446 [1] §1 Confidentiality：「Data sent over the channel after establishment is only visible to the endpoints.」
  RFC 9110 [4] §4.2.2：「"secured" specifically means that the server has been authenticated as acting on behalf of the identified authority and all HTTP communication with that server has confidentiality and integrity protection」
- **注意**：p031 的定義對應 RFC 8446「only visible to the endpoints」；長度不隱藏在 C22 講，兩者不矛盾（看得懂的是內容）。

## C05 封起來也要封給對的人：路上的人可以冒充網站；出發前問查詢處「這個網址在哪裡」，那一問的回答也可能被動手腳【官方規格】【比喻：查詢處】

- **可用說法**：p034–p038，回呼在 p155
- **來源**：[4] §4.3.4；[11]（網域名稱是 IP 位址的別名）
- **原文**：RFC 9110 [4] §4.3.4：「Certificate verification is used to prevent server impersonation by an on-path attacker or by an attacker that controls name resolution. This process requires that a client be configured with a set of trust anchors.」
  MDN [11]：「we can alias an IP address with a human-readable name called a domain name」。
- **注意**：p037「平板先問查詢處『這個網址在哪裡』」：「查詢處」＝幫你把網域名稱查成 IP 位址的地方（DNS 解析），是**比喻**；問的其實是網域名稱不是整個網址、有快取時不必每次問，都屬**簡化**。片中不念 DNS。查詢處沒有被說成可信的權威：p038 馬上說「那一問的回答，也可能被路上的人動手腳」，對應 RFC 9110「an attacker that controls name resolution」。p155 的回呼（「還記得出發前，問『這個網址在哪裡』那一問嗎？」）沒提查詢處，仍接得上。

## C06 憑證：寫著網站的名字，綁著一把只有網站自己有的鑰匙（片中：專屬印章的圖樣）；瀏覽器檢查名字跟網址列一樣【官方規格＋官方說明】【比喻】

- **可用說法**：p039–p044
- **來源**：[7]、[3] §6.1、[4] §4.3.4
- **原文**：CT [7] step 1：「A certificate ties together a domain and a public key.」；Web PKI 段：「A certificate is, essentially, a binding of a cryptographic key (in this case a public key) to a web domain by a Certificate Authority (CA).」
  RFC 5280 [3] §6.1：「The primary goal of path validation is to verify the binding between a subject distinguished name or a subject alternative name and subject public key」。
  RFC 9110 [4] §4.3.4：「a client MUST verify that the service's identity is an acceptable match for the URI's origin server」。
- **比喻的限度**：公開金鑰＝「印章的圖樣」（誰都能拿來對），私鑰＝「那顆章」（只有網站拿著）。真的印章可以仿刻，數位簽章在沒有私鑰時造不出來；片中說「影印的人沒有那顆章」，不說章不能仿。

## C07 自己做的證件瀏覽器不收；憑證機構（以免費發證的機構為例）只驗證你控制這個網域：在網站固定位置放指定檔案，從多個網路位置同時檢查【官方說明】

- **可用說法**：p045–p051
- **來源**：[5]；[4] §4.3.4（要有信任錨）；[7]（鏈要接到瀏覽器信任的根）
- **原文**：Let's Encrypt [5]：「the ACME client proves to the Certificate Authority (CA) that the web server controls a domain」「Provisioning a DNS record under example.com, or Provisioning an HTTP resource under a well-known URI on http://example.com/」「it's the CA's job to check that the challenges have been satisfied from multiple network perspectives」。
- **注意**：「自己做的，瀏覽器不收」是**撰稿推論**：RFC 9110 要求用戶端用設定好的信任錨驗證，CT [7]「ensuring the each certificate in the chain was ultimately issued by a certificate authority that the browser trusts」；自簽憑證不在信任庫裡就驗不過。片中說「例如」，因為還有 DNS 記錄等其他方法；這是 Let's Encrypt 一家的做法，不說所有 CA 都只做這種驗證（OV/EV 未讀）。p051 抽屜小卡是**比喻**。

## C08 發證只查「你管不管得了這個網址」，不查網站好不好、內容能不能信；騙子替自己的相似網址一樣領得到證件【官方說明＋撰稿推論】

- **可用說法**：p052–p055、p062
- **來源**：[5]、[8]
- **原文**：Let's Encrypt [5]：「proves to the Let's Encrypt CA that the operator controls one or more domains」；Chromium [8]：「we know that the lock icon does not indicate website trustworthiness」「nearly all phishing sites use HTTPS, and therefore also display the lock icon」。
- **注意**：p062 是從 [5] 的驗證內容（只驗網域控制）和 [8]「幾乎所有釣魚網站都用 HTTPS」推出來的；片中沒有說哪一家 CA 發給了哪個詐騙網站。

## C09 幾乎所有釣魚網站都用 HTTPS；釣魚網站的定義【官方說明】

- **可用說法**：p059–p061
- **來源**：[8]
- **原文**：「This misunderstanding is not harmless — nearly all phishing sites use HTTPS, and therefore also display the lock icon.」
- **注意**：這句寫於 2023-05-02，片中沒有說年份（初稿有，年份太多，刪了）；p061「釣魚網站，就是假裝成別人、騙你打密碼的網站。」是撰稿給八歲小孩的定義。

## C10 瀏覽器很早就畫鎖頭表示 HTTPS；只有 11% 受試者真的懂鎖頭的意思；2023 年 Chrome 宣布把鎖頭換成別的圖示，免得被誤會成網站可信【官方說明】

- **可用說法**：p008（開場只問）、p063–p067
- **來源**：[8]
- **原文**：「Browsers have shown a lock icon when a site loads over HTTPS since the early versions of Netscape in the 1990s.」「The lock icon is meant to indicate that the network connection is a secure channel between the browser and site」「our research in 2021 showed that only 11% of study participants correctly understood the precise meaning of the lock icon」「we will be replacing the lock icon in Chrome with a variant of the tune icon」「Replacing the lock icon with a neutral indicator prevents the misunderstanding that the lock icon is associated with the trustworthiness of a page」「The new icon is scheduled to launch in Chrome 117, which releases in early September 2023」。
- **注意**：片中說「宣布」，不說哪一天上線（原文是 scheduled）。小問的平板畫的是鎖頭：插圖不指定瀏覽器；Chromium 原文也說 iOS 上移除、Android 一起換。研究年份（2021）片中不念，只說「他們的研究」。

## C11 憑證鏈：機構的證件由上一層簽，一層接一層到根憑證；瀏覽器或系統內建一組根憑證，決定要信它們【官方規格＋官方說明】【比喻：校長的章】

- **可用說法**：p068–p073
- **來源**：[3] §6.1、[7]、[6]
- **原文**：RFC 5280 [3] §6.1：「(a) for all x in {1, ..., n-1}, the subject of certificate x is the issuer of certificate x+1; (b) certificate 1 is issued by the trust anchor; (c) certificate n is the certificate to be validated」「The trust anchor is an input to the algorithm.」
  CT [7]：「These private keys are associated with what are called "root certificates" which are distributed by user agents as "trust anchors"」「These root certificates and their private keys are used to create intermediate CA certificates … that are used to issue the web server certificates」。
  Let's Encrypt [6]：「Our root key material is kept safely offline. We issue end-entity certificates to subscribers from the intermediates」「Root Programs and Trust Stores may decide to trust a Root CA beyond that date, or terminate trust in it before that date.」
- **注意**：「一組」不給數量。「瀏覽器或手機系統」對應 user agents 與 Trust Stores；哪些根被信任由信任庫決定（[6]），RFC 不規定清單。

## C12 憑證要登記在公開、只增不刪、誰都能查的帳本；Chrome 與 Safari 要求；網域主人可訂閱通知【官方說明】（約 20 秒，企劃要求）

- **可用說法**：p074–p079
- **來源**：[7]、[5]
- **原文**：CT [7]：「Some browsers, like Chrome and Safari, help enforce CT.」「Certificate logs are append-only ledgers of certificates. Because they're distributed and independent, anyone can query them」「Both Safari and Chrome user agents require at least 2 SCTs, depending on certificate lifetimes.」「If you subscribe to a CT monitor for your domain, you get updates when precertificates and certificates for those domains are included in any of the logs checked by that monitor.」「Monitors work with website operators to help them understand if an unauthorized certificate has been issued for a domain.」
  Let's Encrypt [5]：「The CA will also submit the certificate to numerous public Certificate Transparency (CT) logs.」
- **注意**：**簡化**：瀏覽器要求的是至少兩張 SCT（日誌承諾收錄的時間戳記），片中說「要登記在公開的帳本上」。「至少兩張」與 SCT 不念。p075「現在 Chrome、Safari 這些瀏覽器要求」是「像 Chrome、Safari 這樣的瀏覽器」，對應原文的 like：只舉例，不說只有它們，也不說所有瀏覽器都要求。CT 網站是 Google 主導的開放專案頁，不是標準文件。

## C13 檢查沒過：Chrome 會整頁顯示「你的連線不是私人連線」；問題可能出在網站、網路或裝置【官方說明】

- **可用說法**：p080–p083
- **來源**：[9]
- **原文**：「If you get a full-page error message saying "Your connection is not private," then there's a problem with the site, the network, or your device.」
- **注意**：企劃列為缺的證據（目前瀏覽器怎麼顯示憑證錯誤）。Chrome 說明頁沒有逐條寫「憑證哪裡不對就出現這頁」，所以 p082 說「像 Chrome，會整頁跳出警告」並照原文說原因可能在三處，不說每一種憑證錯誤都長這樣，也不講其他瀏覽器。「你的連線不是私人連線」是英文訊息的中文說法；**播出前在繁中 Chrome 上確認畫面上的實際用字**，不同就改成實際用字。

## C14 寫信前先交換金鑰（調顏料比喻）；之後的往來全部加密，連憑證也是加密後才送【官方規格】【比喻】

- **可用說法**：p086–p096
- **來源**：[1] §2、§1.2
- **原文**：§2：「Key Exchange: Establish shared keying material and select the cryptographic parameters. Everything after this phase is encrypted.」「The combination of the ClientHello and the ServerHello determines the shared keys.」（ClientHello 帶 key_share，ServerHello 帶伺服器的 key_share）
  §1.2：「All handshake messages after the ServerHello are now encrypted.」；Figure 1 中 {Certificate*} 用握手金鑰保護。
- **比喻的限度**：調顏料是常見的 Diffie-Hellman 示意，**不在 RFC 裡**；片中 p094 明說「這只是比喻，真的做法是數學」。「半成品調不出來」對應 DH 的困難問題，片中不說為什麼。第二章先講憑證、第三章才說憑證是加密後才送：p096 的「連剛剛那張證件，也是封好才送」就是把順序講清楚，避免觀眾以為先驗證再交換金鑰。

## C15 前向保密：這次的秘密用完就丟；就算以後網站的長期金鑰（章）被偷，只要這次的秘密已刪除，以前錄下的也解不開【官方規格】

- **可用說法**：p097–p101
- **來源**：[1] 附錄 E.1、§1.2
- **原文**：E.1：「Forward secret with respect to long-term keys: If the long-term keying material (in this case the signature keys in certificate-based authentication modes …) is compromised after the handshake is complete, this does not compromise the security of the session key (see [DOW92]), as long as the session key itself has been erased.」§1.2：「All public-key based key exchange mechanisms now provide forward secrecy.」
- **注意**：「只要這次的秘密已經丟掉」照原文的條件句。PSK-only 模式不成立（E.1 末句），本集不講 PSK。搶先送出的信（C20）也不具前向保密，片中沒說，不矛盾（片中沒說它有）。

## C16 憑證可以被轉寄；伺服器要用私鑰對整段握手簽名（當場蓋章，蓋在整段來回上，包括顏色）；對不上就中止連線【官方規格】【比喻】

- **可用說法**：p102–p110
- **來源**：[1] §2、附錄 E.1
- **原文**：§2：「CertificateVerify: A signature over the entire handshake using the private key corresponding to the public key in the Certificate message.」「A failure of the handshake or other protocol error triggers the termination of the connection」。
  E.1：「authenticated by the server's signature over the handshake transcript」。
- **注意**：p102–p103「證件，可以影印吧？」與 p105「影印的人，沒有那顆章」對應憑證是公開文件、誰都能轉寄（T53-002 的說法；原文沒有「轉寄」這個字，是**撰稿推論**：Certificate 訊息本身不證明持有私鑰，所以才需要 CertificateVerify）。p108「整段來回上，包括顏色」＝簽名涵蓋含 key_share 的 ClientHello／ServerHello。

## C17 最後雙方再對一次帳（Finished）；對上了才開始寄真正的信【官方規格】

- **可用說法**：p111–p112
- **來源**：[1] §2
- **原文**：「Finished: A MAC (Message Authentication Code) over the entire handshake. This message provides key confirmation, binds the endpoint's identity to the exchanged keys」「Application Data MUST NOT be sent prior to sending the Finished message, except as specified in Section 2.3.」
- **注意**：例外（§2.3 的 0-RTT）就是 C20，片中在 p124 起講，所以「才開始寄真正的信」不是絕對句。另：伺服器可以在收到用戶端 Finished 前先送資料（§2 末），**簡化**不講。

## C18 每封信都封起來；改一點就打不開，規格要求斷線；信封上寫的長度也算在封條裡【官方規格】

- **可用說法**：p113–p116（p084–p085 的「那信要怎麼封，才不會被同學拆開？」在 p113 回收）
- **來源**：[1] §5.2、§1.2
- **原文**：§5.2：「Each encrypted record consists of a plaintext header followed by an encrypted body, which itself contains a type and optional padding.」「the additional data input is the record header. I.e., additional_data = TLSCiphertext.opaque_type || TLSCiphertext.legacy_record_version || TLSCiphertext.length」「The output is either the plaintext or an error indicating that the decryption failed. There is no separate integrity check.」「If the decryption fails, the receiver MUST terminate the connection with a "bad_record_mac" alert.」
  §1 Integrity：「Data sent over the channel after establishment cannot be modified by attackers without detection.」
- **注意**：p115「信封外面還寫著這封信有多長」＝明文紀錄標頭的 length 欄，p116「看得到，改不了」＝它算在 additional_data 裡（改了解密就失敗）。p113「用那個只有你們知道的顏色封起來」＝用握手導出的流量金鑰，**簡化**（實際上金鑰由共同秘密再推導，兩個方向各一把）。

## C19 編號：兩個方向各自從 0 數、每筆加一；編號混進封條、不寫在外面；重送或調換順序就打不開【官方規格】

- **可用說法**：p117–p123
- **來源**：[1] §5.3、附錄 E.2、§5.2
- **原文**：§5.3：「A 64-bit sequence number is maintained separately for reading and writing records. The appropriate sequence number is incremented by one after reading or writing each record. Each sequence number is set to zero at the beginning of a connection and whenever the key is changed」「The 64-bit record sequence number is encoded in network byte order and padded to the left with zeros to iv_length. The padded sequence number is XORed with either the static client_write_iv or server_write_iv」。
  E.2：「Order protection/non-replayability: An attacker should not be able to cause the receiver to accept a record which it has already accepted or cause the receiver to accept record N+1 without having first processed record N.」
- **注意**：「編號不寫在外面」是**撰稿推論**：TLS 1.3 的紀錄標頭只有類型、版本、長度（§5.2 的 additional_data），nonce 由序號隱含算出；§5.3 註明與 TLS 1.2「partially explicit nonce」不同。換鑰時歸零、64 位元片中不講。（舊稿小問的「所以每一封，都不能重寄！」2026-11-13 刪掉，C20 的例外照舊從 p124 起講。）

## C20 規格自己用「IMPORTANT NOTE」標出的例外：以前連過時，用上次留下的秘密讓第一封搶先送出、省一次來回；不保證跨連線不被重送；可能讓購買重複；規格另寫方法讓伺服器自己限制【官方規格】

- **可用說法**：p124–p130
- **來源**：[1] §1.2、§2.3、附錄 E.5、§8
- **原文**：§1.2：「A zero round-trip time (0-RTT) mode was added, saving a round trip at connection setup for some application data, at the cost of certain security properties.」
  §2.3：「When clients and servers share a PSK (either obtained externally or via a previous handshake), TLS 1.3 allows clients to send data on the first flight ("early data").」「IMPORTANT NOTE: The security properties for 0-RTT data are weaker than those for other kinds of TLS data. … There are no guarantees of non-replay between connections.」「Section 8 describes mechanisms which the server can use to limit the impact of replay.」
  E.5：「Duplication of actions which cause side effects (e.g., purchasing an item or transferring money) to be duplicated」。
- **注意**：不說哪些網站或瀏覽器開了 0-RTT；同一連線內不會重複處理（§2.3）片中不講。「以前連過」也包括外部共享的 PSK，**簡化**成以前連過。

## C21 寄完要說「我講完了」，半路被剪斷才分得出來【官方規格】（一句，企劃要求）

- **可用說法**：p131–p132
- **來源**：[1] §6.1
- **原文**：「The client and the server must share knowledge that the connection is ending in order to avoid a truncation attack.」「close_notify: This alert notifies the recipient that the sender will not send any more messages on this connection.」「If a transport-level close is received prior to a "close_notify", the receiver cannot know that all the data that was sent has been received.」

## C22 長度不隱藏；看長度與時間的流量分析能推出資訊，選擇少時特別容易（如固定片庫的影片網站）；可填充，但規格不規定填多少【官方規格】

- **可用說法**：p133–p142（p135 回呼 p115 的長度）
- **來源**：[1] §1、附錄 E.3、§5.4
- **原文**：§1：「TLS does not hide the length of the data it transmits, though endpoints are able to pad TLS records in order to obscure lengths and improve protection against traffic analysis techniques.」
  E.3：「TLS is susceptible to a variety of traffic analysis attacks based on observing the length and timing of encrypted packets … This is particularly easy when there is a small set of possible messages to be distinguished, such as for a video server hosting a fixed corpus of content, but still provides usable information even in more complicated scenarios.」
  §5.4：「Selecting a padding policy that suggests when and how much to pad is a complex topic and is beyond the scope of this specification.」
- **注意**：盲評改寫後，片中不再直接說「規格寫它不隱藏資料的長度」：p135「還看得到一些。還記得信封外面寫的長度嗎？」回頭指向 p115「信封外面還寫著這封信有多長」，也就是 §5.2 明文紀錄標頭裡的 length 欄（C18），路上看得到；p136「信有多厚、多久寄一封，路上的人還是看得到」仍由 §1 與 E.3 支持，p139「規格提醒：看長度和時間……」把 E.3 交代成規格的話，p142「要塞多少，規格沒有規定」是 §5.4。標頭寫的是含填充的長度，所以 p141 塞空白「撐成一樣厚」接得上。p139「有時就猜得出」照原文的 susceptible／usable information，不給成功率。

## C23 網站的名字在連線開頭沒有加密（SNI）；2026 年 3 月發布的 ECH 規格把它也加密；但 ECH 自己說光這樣不夠：信最後送到哪一台網站的機器（伺服器的 IP 位址）、出發前那一問（明文 DNS 查詢）仍可能露出；很多網站共用同一台（同一個 IP），所以名字是最主要的明確線索【官方規格】【比喻：網站的機器】

- **可用說法**：p143–p156
- **來源**：[2] §1、[1] §9.2
- **原文**：RFC 9849 [2]（頁首 March 2026，Standards Track）§1：「The plaintext Server Name Indication (SNI) extension in ClientHello messages, which leaks the target domain for a given connection, is perhaps the most sensitive information left unencrypted in TLS 1.3.」「This document specifies a new TLS extension called Encrypted Client Hello (ECH) that allows clients to encrypt their ClientHello to the TLS server.」「ECH is not in itself sufficient to protect the identity of the server. The target domain may also be visible through other channels, such as plaintext client DNS queries or visible server IP addresses.」「many TLS servers host multiple domains on the same IP address. Private origins may also be deployed behind a common provider, such as a reverse proxy. In such environments, the SNI remains the primary explicit signal available to observers to determine the server's identity.」
  RFC 8446 [1] §9.2：「all implementations MUST support the use of the "server_name" extension with applications capable of using it. Servers MAY require clients to send a valid "server_name" extension.」
- **注意**：p145「很可能」：一般 TLS 1.3 連線會帶 SNI，但規格沒有要求每次都送，所以不說「一定」。**ECH 普及率沒有來源**（企劃列為缺的證據）：片中只說規格何時發布，不說現在多少瀏覽器或網站在用；也不說「現在網域名稱都藏起來了」。p150「裡面一層信封」對應 ECH 的內外兩個 ClientHello，**簡化**。p152「信最後送到哪一台網站的機器，路上還是看得到」＝ visible server IP addresses，p153「不過很多網站常常共用同一台」＝ multiple domains on the same IP address；**簡化**：路上看得到的是位址不是實體機器，一個位址背後也不一定只有一台（原文的 common provider、reverse proxy），片中只講共用主機那一種，要表達的事（光看送到哪裡分不出是哪個網站，所以 p154 名字才是最明白的線索）跟原文一致。第一版的比喻是「哪一棟大樓」「住同一棟」，盲評改寫換成機器，插圖也換成 `server-cabinet`、`chief-same-machine`。「很多」「常常」對應 many，不給比例。p156「那一問要是沒封，也會露出名字」對應 plaintext DNS queries；加密 DNS 的名字不講。

## C24 加密只保護路上；資料到了對方手上對方全部讀得到；對方是騙子，HTTPS 也把資料送到騙子手上；要看清楚網址列上的名字，長得很像的名字封條管不到、要靠自己看【官方規格＋官方說明＋撰稿推論】

- **可用說法**：p157–p165（p007「可是也有些事，它根本不管。」在 p158 回收；p056–p058 的寶石連結在 p157–p157 問、p164 回收）
- **來源**：[1] §1、[9]、[8]、[5]、[12]
- **原文**：RFC 8446 §1：「Data sent over the channel after establishment is only visible to the endpoints.」
  Chrome 說明 [9]，Default (Secure)：「Information you send or get through the site is private between you and the site. Even when connected to a site securely, always be careful when you share sensitive or personal information. Check the site name in the address bar to make sure you're on the site you want to visit.」
  Chromium [8]：「nearly all phishing sites use HTTPS」。
  Chrome 說明 [12]：「Phishing and malware detection is turned on by default in Chrome. When you encounter phishing, malware, unwanted software, or social engineering sites, you may get a red warning that says "Dangerous site."」「To protect you from unsafe websites, Google Safe Browsing maintains a list of websites that might put you at risk for malware, abusive extensions, phishing, malicious and intrusive ads, and social engineering attacks.」
- **注意**：p160「對方是騙子，HTTPS 也會把密碼，好好送到騙子手上。」是 C08、C09 與「only visible to the endpoints」合起來的**撰稿推論**。p162–p163 轉述 [9] 的 Check the site name。p164「名字多了一個字母！」是故事情節，不是事實主張；插圖不畫網址字樣。
  p165「沒錯，這種封條管不到，要靠你自己看。」是**撰稿推論**，範圍限在「封條」（HTTPS／TLS）：發證只驗網域控制（[5]，C08），騙子替自己相似的網址一樣領得到證件，幾乎所有釣魚網站都用 HTTPS（[8]），連上了封條照樣成立，所以名字像不像不是封條會檢查的事，[9] 才要你自己看網址列上的名字。不說「只能靠你自己」：[12] 寫 Chrome 預設開著釣魚與惡意網站偵測，遇到（Safe Browsing 名單上的）釣魚網站可能跳出紅色「Dangerous site」警告；這是封條以外的另一項功能，不保證每個相似網址都會被擋，片中不講。第一版的「這種只能靠你自己看」被 verify-2 G02 指出說得太滿，已改。原本收尾的「寄給誰，要我自己看清楚！」（已刪）的意思移到這一句與 p175「下次打密碼，我先看名字！」。

## C25 收尾：小問的答案、所長的意見【回收，意見標成意見】

- **可用說法**：p166–p172（p173–p175 小問去跟媽媽說、下次先看名字，回收 C24；p176–p178 留言題與訂閱）。
  p166 所長只問「那多一個 S，你的密碼在路上差了什麼？」，範圍限在路上。
  p167–p170 小問用自己的話說：「原來如此！就像剛剛那封封好的信，同學照樣傳，卻讀不到，也冒充不了那個網址！」——同學照樣傳（C01）、讀不到（C04；指信的內容，長度與名字看得到已在 C22、C23 交代）、也冒充不了那個網址（C05、C06、C16；RFC 9110 §4.3.4 擋的是路上的人冒充**同一個網址**，不是長得很像的網址，p165 剛講過）。
  改寫的經過：第一版寫過「抄了也沒用」，因為搶先送出的例外（C20）會跟它矛盾，改成「也冒充不了」；verify-1 F01 指出會被聽成 HTTPS 擋得住冒牌網站，改成「也冒充不了那個網址」；盲評改寫拿掉「改不掉」（完整性在 p114 已講，C18）與「寄給誰，要我自己看清楚！」（意思移到 p165 與 p175，C24）。
  p171–p172「說得好。我覺得最妙的是，這個封條你每天都在用，卻從來沒有看清楚它。」是所長的**意見**（明說「我覺得」）。「每天都在用」不是統計主張，片中不給 HTTPS 普及率；「沒有看清楚它」：封條（加密）本身看不到，鎖頭只是瀏覽器畫的標示（[8]「The lock icon is meant to indicate that the network connection is a secure channel between the browser and site」，C10），而且觀眾看過鎖頭（p063 所長指出網址旁的小鎖頭，tablet-lock 那一景畫的就是它），所以說「看清楚」不說「看見」（verify-2 S3）。第一版的意見「一路上都是不認識的人在傳，信裡寫什麼，卻不用靠他們守密」已換掉。

## 故事與比喻（不是事實主張）

- 小問在咖啡店用免費網路登入遊戲、媽媽叫她看 https、同學傳來「送免費寶石」的連結：**虛構情節**。
- 上課傳信、查詢處（出發前那一問）、抽屜小卡、校長的章、調顏料、蓋章、對帳、封條、編號、信封厚度、信封上的收件人、網站的機器：**比喻**，各自的限度寫在 C05、C06、C07、C11、C14、C16、C18、C19、C23。

## 來源

1. IETF RFC 8446, *The Transport Layer Security (TLS) Protocol Version 1.3*（E. Rescorla, 2018-08；§1、§1.2、§2、§2.3、§5.2–5.4、§6.1、§8、§9.2、附錄 E.1–E.3、E.5），https://www.rfc-editor.org/rfc/rfc8446 （讀的是 .txt 正式版）
2. IETF RFC 9849, *TLS Encrypted Client Hello*（Rescorla、Oku、Sullivan、Wood, 2026-03；§1），https://www.rfc-editor.org/rfc/rfc9849
3. IETF RFC 5280, *Internet X.509 Public Key Infrastructure Certificate and CRL Profile*（2008-05；§6.1），https://www.rfc-editor.org/rfc/rfc5280
4. IETF RFC 9110, *HTTP Semantics*（2022-06；§4.2.2、§4.3.4），https://www.rfc-editor.org/rfc/rfc9110
5. Let's Encrypt〈How It Works〉（Last updated: August 2, 2025），https://letsencrypt.org/how-it-works/
6. Let's Encrypt〈Chains of Trust〉，https://letsencrypt.org/certificates/
7. Certificate Transparency〈How CT works〉，https://certificate.transparency.dev/howctworks/
8. Chromium Blog〈An Update on the Lock Icon〉（2023-05-02），https://blog.chromium.org/2023/05/an-update-on-lock-icon.html
9. Google Chrome 說明〈Check if a site's connection is secure〉，https://support.google.com/chrome/answer/95617?hl=en
10. MDN Web Docs〈HTTPS〉（Glossary），https://developer.mozilla.org/en-US/docs/Glossary/HTTPS
11. MDN Web Docs〈How does the Internet work?〉，https://developer.mozilla.org/en-US/docs/Learn_web_development/Howto/Web_mechanics/How_does_the_Internet_work
12. Google Chrome 說明〈Manage warnings about unsafe sites〉，https://support.google.com/chrome/answer/99020?hl=en

重讀但片中沒有用的：Chromium Blog〈A secure web is here to stay〉（2018-02-08）、Let's Encrypt〈Our First Certificate Is Now Live〉（2015-09-14）。讀不到、沒有用的：Google〈HTTPS by default〉（2025-10，轉址後只拿到頁面框架）。
