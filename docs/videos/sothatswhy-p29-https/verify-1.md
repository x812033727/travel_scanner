# 查核報告 1（sothatswhy-p29-https）

- 查核者：Claude Opus 5.5（獨立查核代理，未參與撰稿）
- 日期：2026-11-12
- 方法：逐句讀 `video.json` 的 193 句台詞（p001–p193），加上 YouTube 標題、說明、標籤與縮圖文字（headline「多一個 S／差在哪？」、sub「密碼在路上，誰看得到」）。`claims.md` 的 C01–C25 只當線索，不採用它的引文；每個來源當天重新打開（curl GET，HTML 去標籤轉純文字後 grep 並讀上下文）：
  - RFC 8446（TLS 1.3，2018-08）：rfc-editor.org `.txt`（200，337,736 bytes），讀 §1 三項性質與攻擊者假設、§1.2、§2（Key Exchange、CertificateVerify、Finished、Application Data 的限制與伺服器先送資料的但書）、§2.3（IMPORTANT NOTE 全段）、§5.2（additional_data、解密失敗 MUST 斷線）、§5.3（序號與 nonce）、§5.4（填充）、§6.1（close_notify）、§8 開頭（0-RTT 防重送）、§9.2（server_name）、附錄 E.1（前向保密、端點身分保護）、E.2（順序與防重送）、E.3（流量分析）、E.5（重複購買）。
  - RFC 9849（TLS Encrypted Client Hello）：`.txt`（200，112,500 bytes），頁首 "March 2026"、"Category: Standards Track"，讀 §1 全段與 public_name 定義。rfc-editor.org/info/rfc9849 頁面是 JS 框架，讀不到發布日期欄位，日期以 RFC 本文頁首為準。
  - RFC 5280：`.txt`（200，352,580 bytes），讀 §6.1 開頭（(a)–(c) 鏈條件、trust anchor 是輸入、path validation 的目的）。
  - RFC 9110（HTTP Semantics，June 2022）：`.txt`（200，502,941 bytes），讀 §4.2.2 "secured" 定義、§4.3.4 憑證驗證。
  - Let's Encrypt〈How It Works〉（200，頁首 "Last updated: August 2, 2025"）、〈Chains of Trust〉（200），另開〈Multi-Perspective Validation〉2020-02-19 部落格（200，How It Works 的 "multiple network perspectives" 連到這篇），用來核對 p055 的「同時」。
  - certificate.transparency.dev〈How CT works〉（200）。
  - Chromium Blog〈An Update on the Lock Icon〉（200，頁首 "Tuesday, May 2, 2023"）。
  - Google Chrome 說明 answer/95617：英文版 `hl=en`（200）與繁中版 `hl=zh-Hant`（200），用繁中版核對 p090 的畫面用字。
  - MDN〈HTTPS〉詞彙頁（200）、〈How does the Internet work?〉（200；現行版多了交換器與 MAC 位址的段落，router／ISP／domain name 的句子仍在）。
- 打不開／沒讀到原文的：沒有打不開的來源。沒有在實機的繁中 Chrome 上看憑證錯誤頁（只用 Chrome 繁中說明頁的用字核對，見 S6）；RFC 9849 的 info 頁讀不到 metadata，日期以本文頁首為準。
- 結論統計（台詞 193 句）：**正確 192、需改 1、錯誤 0**。另外標題、說明、標籤、縮圖 4 項：正確 3、需改 1（說明）。另有 7 處選修建議（不影響結論，見文末）。
- 「HTTPS 不等於網站可信」這條紅線：片中 p057–p067、p071–p074、p170–p177 都講對了；唯一會讓小孩聽反的是 p184 的「也冒充不了！」（F01），以及說明欄把「只查網址」說成所有發證機構（F02）。
- 字數：下表建議句含標點計算（英文字母、空格各算一字），小問 ≤15、所長 ≤25。

## 一、需改的地方與理由

| # | 行 | 原句 | 結論 | 理由與讀到的原文 | 建議改法 |
| --- | --- | --- | --- | --- | --- |
| F01 | p184（小問） | 也冒充不了！ | 需改（跟 p066 的定義互相打架，會被聽成 HTTPS 擋得住冒牌網站） | TLS 擋住的是冒充**同一個網址**：RFC 9110 §4.3.4 "Certificate verification is used to prevent server impersonation by an on-path attacker or by an attacker that controls name resolution"，且 "a client MUST verify that the service's identity is an acceptable match for the URI's origin server"。片中 p066 剛把釣魚網站定義成「假裝成別人、騙你打密碼的網站」，p067 又說騙子的相似網址一樣領得到證件；Chromium Blog："nearly all phishing sites use HTTPS"、"the lock icon does not indicate website trustworthiness"。小孩聽到總結句「也冒充不了！」，很容易記成「有 HTTPS 就沒人能假裝」，正好是本集要拆掉的誤會。p185 雖接「寄給誰，要我自己看清楚」，但兩句連著聽仍互相矛盾。把冒充的範圍說成「那個網址」就一致 | 也冒充不了那個網址！（10 字） |
| F02 | YouTube 說明 | 發證件的機構只查你管不管得了網址 | 需改（把一家的做法說成所有發證機構） | 片中 p053 說的是「有一個免費發憑證的機構」，來源也只有 Let's Encrypt："the ACME client proves to the Certificate Authority (CA) that the web server controls a domain"、"proves to the Let's Encrypt CA that the operator controls one or more domains"。說明欄拿掉了「免費」「這一家」，變成所有憑證機構都只查網址控制權；有些機構另外核對組織身分（本次沒讀相關來源，claims.md C07 也寫明不說所有 CA 都只做這種驗證）。片中台詞本身沒有這個問題 | 「……（網站的證件、免費發證件的機構只查你管不管得了網址、一路簽到瀏覽器內建的根憑證、公開的登記帳本）……」其餘照留 |

## 二、逐段核對（正確的句子與依據）

### 開場：咖啡店與多一個 S（p001–p011）

| 段落／行 | 主張 | 結論 | 來源 | 依據摘要 |
| --- | --- | --- | --- | --- |
| p001–p007 | 咖啡店免費網路登入遊戲；媽媽說開頭要 HTTPS 才能打密碼；不就多一個 S | 正確 | — | 虛構情節；媽媽的規則在 p172–p177 補上「不夠」 |
| p008–p009 | 密碼在路上差很多；有些事它根本不管 | 正確 | RFC 8446 §1 | 「在路上」對應 "Data sent over the channel after establishment is only visible to the endpoints"；p009 在 p172 回收 |
| p010 | 小鎖頭很多人看錯 | 正確 | Chromium Blog | "only 11% of study participants correctly understood the precise meaning of the lock icon" |
| p011 | 到底差在哪 | 正確 | — | 問句 |

### 密碼要經過好多人的手（p012–p038）

| 段落／行 | 主張 | 結論 | 來源 | 依據摘要 |
| --- | --- | --- | --- | --- |
| p012–p013 | 是不是直接飛到遊戲公司（錯猜） | 正確 | — | 錯猜，p014 糾正 |
| p014–p016 | 先到咖啡店的無線網路機器，再交給網路公司，一站轉一站，經過好多台轉送的電腦 | 正確 | MDN Internet | "the commercial router in your home is likely a combination of a switch, a router, and a modem"；"An ISP is a company that manages some special routers … the message from our network is carried through the network of ISP networks to the destination network." 沒給台數 |
| p017–p022 | 那些機器看得到嗎；上課傳信，中間經過好幾個同學；咖啡店的機器、網路公司就是這些同學 | 正確（比喻） | MDN Internet | 經手的同學對應路由器與 ISP，比喻沒有教錯方向 |
| p023–p024 | 信沒封，每個經手的人都能打開看，甚至改幾個字 | 正確（比喻） | Chrome 說明 | 對應下一句的 "view and change" |
| p025–p026 | Chrome 說明：沒有私密連線的網站，別人可能看到、也可能改掉你傳的東西 | 正確 | Chrome 說明（Info or Not secure） | "The site doesn't use a private connection. Someone may be able to view and change the information you send and get through this site."；繁中版「網站未使用私人連線，其他人或許可以查看及變更你與該網站之間的資訊」。「可能」對應 may |
| p027–p029 | 同學人都很好；大部分是，可是沒辦法挑誰來傳 | 正確 | — | 口語橋接，沒說路上的機器真的在偷看 |
| p030–p031 | S 背後的規則叫 TLS；規格寫就算路上的人能完全控制網路，保護也要成立 | 正確 | MDN HTTPS；RFC 8446 §1 | MDN "It uses TLS to encrypt all communication"；RFC "These properties should be true even in the face of an attacker who has complete control of the network"。原文是 should，「也要成立」是設計目標的說法，恰當 |
| p032–p033 | S 是什麼意思 | 正確 | — | 問句 |
| p034–p035 | S 是「安全」；HTTPS 是網頁往來用 TLS 加密的版本 | 正確 | MDN HTTPS | "HTTPS (HyperText Transfer Protocol Secure) is an encrypted version of the HTTP protocol. It uses TLS to encrypt all communication between a client and a server." |
| p036 | 加密就是只有你和對方看得懂 | 正確 | RFC 8446 §1 | "only visible to the endpoints"；「看得懂」是內容，長度另在 p148 交代，不矛盾 |
| p037–p038 | 封起來就好了吧 | 正確 | — | 錯猜，p039 回答 |

### 對面真的是遊戲公司嗎（p039–p091）

| 段落／行 | 主張 | 結論 | 來源 | 依據摘要 |
| --- | --- | --- | --- | --- |
| p039–p041 | 封起來也要封給對的人；有人假裝遊戲公司收下，封再好也是交給他 | 正確 | RFC 9110 §4.3.4 | "prevent server impersonation by an on-path attacker" |
| p042–p043 | 出發前要先問「這個網址在哪裡」，回答也可能被動手腳 | 正確（簡化） | RFC 9110 §4.3.4；MDN Internet | "or by an attacker that controls name resolution"；MDN "we can alias an IP address with a human-readable name called a domain name"。不念 DNS，簡化合理 |
| p044–p045 | 怎麼知道對面真的是遊戲公司 | 正確 | — | 問句 |
| p046–p048 | 證件叫憑證，寫著網站名字，印著專屬印章的圖樣；那顆章只有網站拿著 | 正確（比喻，附註） | CT；RFC 5280 §6.1 | CT "A certificate ties together a domain and a public key"；"a binding of a cryptographic key (in this case a public key) to a web domain by a Certificate Authority"；RFC 5280 "verify the binding between a subject distinguished name or a subject alternative name and subject public key"。圖樣＝公開金鑰、章＝私鑰，對應正確。比喻的限度見 S1 |
| p049 | 瀏覽器先看證件上的名字跟網址列一樣嗎 | 正確（簡化） | RFC 9110 §4.3.4 | "a client MUST verify that the service's identity is an acceptable match for the URI's origin server"。一張證可列多個名字或萬用字元，「一樣」是小孩層次的說法 |
| p050–p051 | 證件誰發的；自己做一張 | 正確 | — | 問句 |
| p052 | 自己做的瀏覽器不收；要找專門發憑證的機構 | 正確（撰稿推論） | RFC 9110 §4.3.4；CT | "This process requires that a client be configured with a set of trust anchors"；CT "ensuring the each certificate in the chain was ultimately issued by a certificate authority that the browser trusts"。自簽憑證不在信任庫就驗不過；使用者手動安裝根憑證的例外不必講 |
| p053–p055 | 免費機構在官網寫怎麼查：例如在網站固定位置放指定檔案，再從好幾個地方同時連過來看 | 正確 | Let's Encrypt How It Works；LE 2020 MPIC | "Provisioning an HTTP resource under a well-known URI"；"it creates a file on a specified path"；"check that the challenges have been satisfied from multiple network perspectives"。「例如」對應原文 "For example"（另有 DNS 記錄）。「同時」：MPIC 文 "an attacker must successfully compromise three different network paths at the same time"，有據 |
| p056 | 像在自己座位的抽屜放指定小卡 | 正確（比喻） | — | 對應「證明你管得了這個位置」，沒有教錯 |
| p057–p058 | 它有查網站是不是好人嗎 | 正確 | — | 問句 |
| p059–p060 | 沒有，查的是你管不管得了這個網址，不是人好不好、內容能不能信 | 正確 | Let's Encrypt How It Works；Chromium Blog | "proves to the Let's Encrypt CA that the operator controls one or more domains"；"the lock icon does not indicate website trustworthiness"。「它」指 p053 那一家，範圍正確（說明欄的問題見 F02） |
| p061–p063 | 同學傳來送免費寶石的連結，也是 HTTPS | 正確 | — | 虛構情節 |
| p064–p065 | Chrome 團隊寫過：幾乎所有釣魚網站都用 HTTPS | 正確 | Chromium Blog | "nearly all phishing sites use HTTPS, and therefore also display the lock icon."「寫過」是過去式，沒有把 2023 年的話說成現況 |
| p066 | 釣魚網站是假裝成別人、騙你打密碼的網站 | 正確（給小孩的定義） | — | 合理定義；與 p184 的衝突見 F01 |
| p067 | 騙子替自己長得很像的網址一樣領得到證件 | 正確（撰稿推論） | Let's Encrypt；Chromium Blog | 驗證內容只有網域控制權，加上「nearly all phishing sites use HTTPS」，推論成立；沒點名哪家 CA |
| p068 | 瀏覽器很早就畫小鎖頭，代表連線有加密 | 正確 | Chromium Blog | "Browsers have shown a lock icon when a site loads over HTTPS since the early versions of Netscape in the 1990s."；"meant to indicate that the network connection is a secure channel" |
| p069–p070 | 我看到的就是這個鎖頭 | 正確 | — | 情節；平板沒指定瀏覽器（Chromium 原文：Android 一起換、iOS 移除，桌機換 tune），不衝突 |
| p071–p072 | 他們的研究：只有百分之十一的受試者真的懂鎖頭的意思 | 正確 | Chromium Blog | "our research in 2021 showed that only 11% of study participants correctly understood the precise meaning of the lock icon"。數字精確 |
| p073–p074 | 二〇二三年宣布把鎖頭換成別的圖示，免得以為有鎖就是好網站 | 正確 | Chromium Blog | 發文 2023-05-02；"we will be replacing the lock icon in Chrome with a variant of the tune icon"；"prevents the misunderstanding that the lock icon is associated with the trustworthiness of a page"。說「宣布」不說上線日（原文 "scheduled to launch in Chrome 117"），準確 |
| p075–p076 | 瀏覽器為什麼相信發證機構 | 正確 | — | 問句 |
| p077–p078 | 機構也有證件，蓋著上一層的章；一層一層往上，最上面叫根憑證 | 正確（簡化） | RFC 5280 §6.1；CT；LE Chains of Trust | "(a) for all x in {1, ..., n-1}, the subject of certificate x is the issuer of certificate x+1; (b) certificate 1 is issued by the trust anchor"；CT "root certificates … are used to create intermediate CA certificates … that are used to issue the web server certificates"；LE "We issue end-entity certificates to subscribers from the intermediates" |
| p079–p080 | 瀏覽器或手機系統內建一組根憑證；像本來就認得校長 | 正確（比喻） | CT；LE Chains of Trust | "root certificates" "distributed by user agents as "trust anchors""；"Root Programs and Trust Stores may decide to trust a Root CA…"。沒給數量 |
| p081–p082 | 機構發錯證件呢 | 正確 | — | 問句 |
| p083–p085 | 現在 Chrome 和 Safari 要求憑證登記在公開帳本；只能加、不能刪，誰都能翻 | 正確（簡化） | CT | "Some browsers, like Chrome and Safari, help enforce CT"；"Both Safari and Chrome user agents require at least 2 SCTs"；"Certificate logs are append-only ledgers … anyone can query them"；"Certificates can only be added to a log, not deleted, modified, or retroactively inserted." 瀏覽器實際要求的是 SCT（日誌承諾在 MMD 內收錄，通常 24 小時），說成「要登記」在小孩層次不錯；沒說「只有」這兩家，不排除其他瀏覽器 |
| p086–p087 | 網站主人可訂閱通知，有人用我的名字拿到憑證、登記進去後就收到通知 | 正確 | CT | "If you subscribe to a CT monitor for your domain, you get updates when precertificates and certificates for those domains are included in any of the logs checked by that monitor."「登記進去之後」照原文的順序；沒說能事先擋下 |
| p088–p089 | 檢查沒過會怎樣 | 正確 | — | 問句 |
| p090–p091 | 像 Chrome 會整頁警告「你的連線不是私人連線」；說明寫問題可能出在網站、網路或裝置 | 正確 | Chrome 說明（英／繁中） | 英文 "If you get a full-page error message saying "Your connection is not private," then there's a problem with the site, the network, or your device."；繁中版標題「修正「你的連線不是私人連線」錯誤」，內文「表示網站、網路或你的裝置發生問題」。用字與繁中官方說明一致（實機畫面見 S6） |

### 先調顏色，再封信（p092–p144）

| 段落／行 | 主張 | 結論 | 來源 | 依據摘要 |
| --- | --- | --- | --- | --- |
| p092–p094 | 找對人了，信要怎麼封 | 正確 | — | 問句 |
| p095–p097 | 寫信前先有只有彼此知道的秘密；可是大家都看得到 | 正確 | RFC 8446 §2 | "Key Exchange: Establish shared keying material" |
| p098–p102 | 調顏料：公開的顏色、各自偷偷加、交換、再加自己的，兩邊同色；傳信的只看過半成品調不出來 | 正確（比喻） | RFC 8446 §2 | "The combination of the ClientHello and the ServerHello determines the shared keys"；ServerHello 帶 "the server's ephemeral Diffie-Hellman share"。調顏料是常見的 Diffie-Hellman 示意，步驟對應正確；「調不出來」只對旁觀者成立，主動換顏色的人在 p115–p119 另外處理，比喻沒有教錯 |
| p103 | 這只是比喻，真的做法是數學 | 正確 | — | 明說比喻 |
| p104–p105 | 第一步交換這種資料，之後的往來全部封起來，連證件也是封好才送 | 正確 | RFC 8446 §2、§1.2 | "Everything after this phase is encrypted."；"All handshake messages after the ServerHello are now encrypted."；RFC 9849 §1 "TLS 1.3 … encrypts most of the handshake, including the server certificate"。把「先驗證、後交換」的誤會講清楚 |
| p106–p107 | 先錄下來以後再解呢 | 正確 | — | 問句 |
| p108–p110 | 顏色用完就丟；就算以後章被偷，只要這次的秘密已丟掉，以前錄下的也解不開 | 正確 | RFC 8446 附錄 E.1、§1.2 | "If the long-term keying material (in this case the signature keys in certificate-based authentication modes …) is compromised after the handshake is complete, this does not compromise the security of the session key …, as long as the session key itself has been erased."；"All public-key based key exchange mechanisms now provide forward secrecy."「章」＝簽章金鑰，對應精確；條件句照原文 |
| p111–p114 | 證件可以影印；所以網站還要當場蓋章；影印的人沒有那顆章 | 正確（比喻，附註） | RFC 8446 §2 | "CertificateVerify: A signature over the entire handshake using the private key corresponding to the public key in the Certificate message." 憑證是公開的，持有私鑰要另外證明，推論成立。比喻限度見 S1 |
| p115–p116 | 傳信的同學偷換顏色呢 | 正確 | — | 問句 |
| p117–p119 | 章蓋在整段來回上，包括顏色；瀏覽器拿圖樣來對；顏色換過就對不上，直接斷線 | 正確 | RFC 8446 §2、附錄 E.1 | 簽章涵蓋 "the entire handshake"（含帶 key_share 的 ClientHello／ServerHello）；E.1 "authenticated by the server's signature over the handshake transcript"；"A failure of the handshake or other protocol error triggers the termination of the connection"。用公開金鑰（圖樣）驗簽，對應正確 |
| p120–p121 | 最後再對一次帳：整段來回我看到的跟你一樣嗎；對上才寄真正的信 | 正確（簡化） | RFC 8446 §2 | "Finished: A MAC … over the entire handshake. This message provides key confirmation"；"Application Data MUST NOT be sent prior to sending the Finished message, except as specified in Section 2.3"。例外在 p135 講；伺服器可在收到用戶端 Finished 前先送資料（"the server may send Application Data prior to receiving the client's Authentication messages"）沒講，屬可接受的簡化 |
| p122–p123 | 每封信用那個顏色封；改一點點就打不開，規格要求斷線 | 正確（簡化） | RFC 8446 §5.2、§1 | "The output is either the plaintext or an error indicating that the decryption failed. There is no separate integrity check."；"If the decryption fails, the receiver MUST terminate the connection with a "bad_record_mac" alert."。實際用的是由共同秘密推導出的流量金鑰，「那個顏色」是簡化 |
| p124–p125 | 信封外寫著多長；這幾個字也算在封條裡，看得到改不了 | 正確 | RFC 8446 §5.2 | "additional_data = TLSCiphertext.opaque_type || TLSCiphertext.legacy_record_version || TLSCiphertext.length"。「改不了」＝改了會被發現 |
| p126–p128 | 把「我要買寶石」抄下來再寄一次 | 正確 | — | 問句 |
| p129 | 每封有編號，兩邊各自從零開始，寄一封加一 | 正確 | RFC 8446 §5.3 | "A 64-bit sequence number is maintained separately for reading and writing records. The appropriate sequence number is incremented by one after reading or writing each record. Each sequence number is set to zero at the beginning of a connection and whenever the key is changed"。換鑰歸零沒講，可接受 |
| p130 | 編號不寫在外面，混進封條裡 | 正確（撰稿推論，成立） | RFC 8446 §5.3、§5.2 | "The padded sequence number is XORed with either the static client_write_iv or server_write_iv"；"Note: This is a different construction from that in TLS 1.2, which specified a partially explicit nonce."；紀錄標頭只有類型、版本、長度 |
| p131–p132 | 舊信再送或順序調換，編號對不上，打不開 | 正確 | RFC 8446 附錄 E.2、§5.2 | "An attacker should not be able to cause the receiver to accept a record which it has already accepted or cause the receiver to accept record N+1 without having first processed record N."；nonce 不對則 AEAD 解密失敗 |
| p133–p134 | 所以每一封都不能重寄（小問） | 正確 | — | 小孩的過度推論，p135 立刻用例外修正 |
| p135–p136 | 有一個例外，規格用「重要提醒」標出來 | 正確 | RFC 8446 §2.3 | 原文 "IMPORTANT NOTE: The security properties for 0-RTT data are weaker than those for other kinds of TLS data." |
| p137–p138 | 以前連過，瀏覽器可以用上次留下的秘密讓第一封搶先送出，省一次來回 | 正確（簡化） | RFC 8446 §2.3、§1.2 | "When clients and servers share a PSK (either obtained externally or via a previous handshake), TLS 1.3 allows clients to send data on the first flight"；"saving a round trip at connection setup for some application data"。說「可以」不說「會」，恰當；外部 PSK 省略。與 p108 的可能混淆見 S4 |
| p139–p140 | 搶先的信不保證不被重送；抄下再寄可能讓買東西發生兩次 | 正確 | RFC 8446 §2.3、附錄 E.5 | "There are no guarantees of non-replay between connections."；"Duplication of actions which cause side effects (e.g., purchasing an item or transferring money) to be duplicated"。「可能」恰當（另見 S5） |
| p141–p142 | 那是一個洞；規格另寫幾種方法讓網站自己擋 | 正確 | RFC 8446 §2.3、§8 | "Section 8 describes mechanisms which the server can use to limit the impact of replay."；§8 "The first class of attack can be prevented by sharing state to guarantee that the 0-RTT data is accepted at most once. Servers SHOULD provide that level of replay safety" |
| p143–p144 | 寄完最後一封說我講完了；半路剪斷才分得出來 | 正確 | RFC 8446 §6.1 | "The client and the server must share knowledge that the connection is ending in order to avoid a truncation attack."；"If a transport-level close is received prior to a "close_notify", the receiver cannot know that all the data that was sent has been received." |

### 封條管不到的地方（p145–p179）

| 段落／行 | 主張 | 結論 | 來源 | 依據摘要 |
| --- | --- | --- | --- | --- |
| p145–p147 | 路上的人什麼都看不到了吧 | 正確 | — | 錯猜，p148 回答 |
| p148–p149 | 規格直說不隱藏長度；多厚、多久寄一封還是看得到 | 正確 | RFC 8446 §1、附錄 E.3 | "TLS does not hide the length of the data it transmits"；E.3 "based on observing the length and timing of encrypted packets" |
| p150–p151 | 看厚度能看出什麼 | 正確 | — | 問句 |
| p152–p153 | 看長度和時間有時猜得出在做什麼；選擇不多時特別容易，像固定影片的網站 | 正確 | RFC 8446 附錄 E.3 | "TLS is susceptible to a variety of traffic analysis attacks … This is particularly easy when there is a small set of possible messages to be distinguished, such as for a video server hosting a fixed corpus of content"；「有時」對應 susceptible，沒給成功率 |
| p154–p155 | 網站可以塞空白把信撐成一樣厚；要塞多少規格沒規定 | 正確（附註） | RFC 8446 §1、§5.4 | "endpoints are able to pad TLS records in order to obscure lengths"；"Selecting a padding policy that suggests when and how much to pad is a complex topic and is beyond the scope of this specification."（填充位元組是全零，「空白」可留）。原文是「兩端」都可以，見 S2 |
| p156–p157 | 他們知道我在跟哪個網站說話嗎 | 正確 | — | 問句 |
| p158–p160 | 很可能；連線開頭瀏覽器會說要找哪個網站，名字平常沒封；像信封外的收件人 | 正確 | RFC 9849 §1；RFC 8446 §9.2 | "The plaintext Server Name Indication (SNI) extension in ClientHello messages, which leaks the target domain for a given connection, is perhaps the most sensitive information left unencrypted in TLS 1.3."；RFC 8446 "all implementations MUST support the use of the "server_name" extension"。規格沒要求每次都送，「很可能」「平常」恰當 |
| p161 | 不能也封起來嗎 | 正確 | — | 問句 |
| p162–p163 | 二〇二六年三月一份新規格正式發布，把收件人名字也放進裡面一層信封 | 正確（簡化） | RFC 9849 頁首、§1 | 頁首 "March 2026"、"Category: Standards Track"；"Encrypted Client Hello (ECH) that allows clients to encrypt their ClientHello to the TLS server. This protects the SNI"。年月精確；只說發布、沒說普及。外層信封仍寫著服務商名字，見 S3 |
| p164–p165 | 它自己也寫光這樣不夠；送到哪一棟大樓路上還是看得到 | 正確 | RFC 9849 §1 | "ECH is not in itself sufficient to protect the identity of the server. The target domain may also be visible through other channels, such as plaintext client DNS queries or visible server IP addresses." |
| p166–p167 | 很多網站常住同一棟，所以信封上的名字才是最明白的線索 | 正確 | RFC 9849 §1 | "many TLS servers host multiple domains on the same IP address … In such environments, the SNI remains the primary explicit signal available to observers to determine the server's identity." |
| p168–p169 | 出發前那一問要是沒封，也會露出名字 | 正確 | RFC 9849 §1 | "plaintext client DNS queries"；加密 DNS 的名字沒念，可接受 |
| p170–p171 | 那送寶石的連結 | 正確 | — | 問句 |
| p172–p173 | 最要緊：封條只管路上；信到了對方手上，對方全部讀得到 | 正確 | RFC 8446 §1；Chrome 說明 | "only visible to the endpoints"；Chrome "Information you send or get through the site is private between you and the site." |
| p174 | 對方是騙子，HTTPS 也會把密碼好好送到騙子手上 | 正確（撰稿推論，成立） | RFC 8446 §1；Chromium Blog；Let's Encrypt | 端點看得到全部內容＋"nearly all phishing sites use HTTPS"＋發證只驗網域控制權，三者合起來推論成立；在小孩聽到的層次是真的，也正是本集的重點 |
| p175 | 那我要怎麼分 | 正確 | — | 問句 |
| p176–p177 | Chrome 說明提醒：就算安全連線也要看清楚網址列的名字 | 正確 | Chrome 說明（Default (Secure)） | "Even when connected to a site securely, always be careful when you share sensitive or personal information. Check the site name in the address bar to make sure you're on the site you want to visit."；繁中版「即使是安全連線……請查看網址列中的網站名稱」 |
| p178–p179 | 名字多了一個字母 | 正確 | — | 故事情節 |

### 收尾（p180–p193）

| 段落／行 | 主張 | 結論 | 來源 | 依據摘要 |
| --- | --- | --- | --- | --- |
| p180–p183 | 同學還是幫我傳，可是拆不開、改不掉 | 正確 | RFC 8446 §1 | Confidentiality 與 Integrity 兩項；「拆不開」指內容，長度與名字前面已交代 |
| p184 | 也冒充不了！ | 見 F01 | — | — |
| p185 | 寄給誰要我自己看清楚 | 正確 | Chrome 說明 | "Check the site name in the address bar" |
| p186–p187 | 所長意見：一路都是不認識的人在傳，信裡寫什麼卻不用靠他們守密 | 正確（意見） | RFC 8446 §1 | 對應 "complete control of the network" 的假設；說「信裡寫什麼」避開長度與名字，措辭精準 |
| p188–p193 | 去跟媽媽說連結是假的；下次先看名字；留言與訂閱 | 正確 | — | 情節與呼籲 |

### 標題、說明、標籤、縮圖

| 項目 | 結論 | 依據 |
| --- | --- | --- |
| 標題「網址多一個 S，資料在路上差了什麼？」 | 正確 | 問句，範圍限「在路上」 |
| 說明 | 需改（F02） | 其餘句子正確：咖啡店機器與網路公司（MDN）、根憑證與公開帳本（CT）、規格承認的例外（§2.3）、「HTTPS 只保護路上，不保證網站是好人，詐騙網站一樣有」（Chromium Blog）、比喻與 AI 插圖聲明、資料截至日 |
| 標籤 | 正確 | 與內容相符 |
| 縮圖「多一個 S 差在哪？」「密碼在路上，誰看得到」 | 正確 | 問句，沒有暗示 HTTPS＝安全網站 |

## 三、撰稿者標出的疑點

| 項目 | 結論 |
| --- | --- |
| C06 印章圖樣＝公開金鑰、章＝私鑰 | 對應正確；片中沒說章不能仿刻。限度：真實印章看了印文可以仿刻，蓋出的印文每張都一樣；數位簽章不能由公開金鑰推出私鑰，而且每次簽的內容不同。p117「章蓋在整段來回上」補上了後者，前者見 S1（選修） |
| C07 自己做的瀏覽器不收；免費機構的驗法 | 正確。「同時」有 LE 2020 MPIC 文 "at the same time" 支持；片中用「例如」「有一個」，範圍正確。說明欄擴大成所有機構，需改（F02） |
| C12 Chrome 與 Safari 要求登記 | 正確（簡化）。實際要求是至少兩張 SCT；小孩層次「要登記在公開帳本」不教錯；「登記進去之後」才收到通知，也沒說能事先擋下 |
| C13 整頁警告與三種原因 | 正確。繁中 Chrome 說明的用字正是「你的連線不是私人連線」；「像 Chrome」與「可能」保住範圍 |
| C14 調顏料、連證件也封好才送 | 正確。§2 "Everything after this phase is encrypted"、§1.2、RFC 9849 §1 "including the server certificate"。比喻已明說，旁觀者調不出、主動換色另有蓋章處理，沒有教錯機制 |
| C16 證件可影印、章蓋在整段來回上包括顏色 | 正確。CertificateVerify 簽 "the entire handshake"，涵蓋雙方 key_share |
| C19 編號不寫在外面 | 正確。§5.3 nonce＝序號 XOR iv，且明說與 TLS 1.2 的 partially explicit nonce 不同 |
| C23 SNI、ECH 2026 年 3 月、IP 與 DNS | 正確。RFC 9849 頁首 March 2026、Standards Track；四句原文都在 §1；片中沒說 ECH 已普及 |
| p174 HTTPS 也把密碼送到騙子手上 | 正確，推論成立，而且是本集最該留的一句 |
| 紅線：HTTPS 是否被說成可信／防詐 | 台詞只有 p184 有被聽反的風險（F01）；說明欄 F02 是範圍問題，不是可信度問題 |

## 建議修改

必改：

- F01 p184（小問）：也冒充不了！ → 也冒充不了那個網址！（10 字）
- F02 YouTube 說明：「發證件的機構只查你管不管得了網址」 → 「免費發證件的機構只查你管不管得了網址」（其餘照留）

選修（不影響本輪結論）：

- S1 印章比喻（p047、p114）：小孩可能追問「看到圖樣不能照著刻一顆嗎？」。台詞不必改；若要補一句，可在 p114 後讓所長說「這顆章，看圖樣也刻不出來。」（14 字），對應公開金鑰推不出私鑰。插圖避免畫成同一個印文貼在不同紙上。
- S2 p154：網站可以在信裡塞空白，把信撐成一樣厚； → 網站和瀏覽器都可以在信裡塞空白，把信撐成一樣厚；（24 字）。RFC 8446 §1 是 "endpoints are able to pad"，兩端都可以；原句沒有說錯，可留。
- S3 p163／ECH 插圖：RFC 9849 §1 "Usage of this mechanism reveals that a client is connecting to a particular service provider"，外層 ClientHello 仍帶 public_name（"The DNS name of the client-facing server"）。台詞「放進裡面一層信封」正確；插圖的外層信封不要畫成全空白，可以寫著一個「大樓管理處」之類的名字。
- S4 p137：p108 剛說「顏色用完就丟」，p137 又說「上次留下的秘密」，小孩可能以為兩者是同一個。可改 → 你跟網站以前連過，瀏覽器可以用上次另外留下的秘密，（25 字）。續連用的秘密是另外導出的（§2.3 "via a previous handshake"），不是那次調出的顏色；原句沒有說錯。
- S5 p140：§8 也規定用戶端 "MUST only send early data which they deem safe to be replayed"，瀏覽器本來就不該把「買東西」這類請求搶先送出。原句說「可能」、轉述的是 E.5 的攻擊類型，可留；若要更完整，可讓 p142 改成「所以規格要瀏覽器小心挑，也寫了方法讓網站擋。」（22 字）。
- S6 p090：繁中 Chrome 說明頁的用字已確認是「你的連線不是私人連線」；本次沒在實機繁中 Chrome 上開過憑證錯誤頁，上片前若有截圖或插圖帶字，再對一次實機畫面。
- S7 p083：CT 頁只舉 Chrome 與 Safari；片中沒說「只有」，可留。不必加其他瀏覽器（本次沒讀其來源）。
