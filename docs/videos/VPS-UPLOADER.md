# VPS 獨立 YouTube Studio 上傳服務

## 交付範圍與目前狀態

後台 `/admin/videos` 的「VPS 獨立上傳」把核准素材送到獨立服務，再由該服務的
Chromium 操作 YouTube Studio。服務使用 Node 24、Playwright、SQLite 與自己的瀏覽器
資料目錄，可用本目錄的 Docker Compose 單獨部署，不需要主網站的資料庫或 Google OAuth。
網站需要可連到服務的私人網路，以及共同的服務密鑰。

**這是待真實帳號驗收的 Studio 操作器。** 自動化測試涵蓋佇列、檔案傳送、後台與合成 DOM；
合成 DOM 不代表目前線上 Studio 畫面。此版本未部署到正式 VPS，未登入真實 Google 帳號，
也未實際上傳影片。啟用前必須完成下方的私人影片驗收，不能把容器健康檢查當作上傳成功。

此路線不呼叫 YouTube Data API，因此不會消耗該 API 的單位配額；YouTube 本身的頻道上傳限制、
帳號驗證與自動存取規則仍適用。它不是官方上傳 API，也不保證無人值守或無限上傳。
[YouTube 條款](https://www.youtube.com/static?template=terms) 對自動存取有書面許可要求，
營運者啟用前須確認自己的使用方式符合規定。
[API 稽核與擴額](https://developers.google.com/youtube/v3/guides/quota_and_compliance_audits)
仍是官方 API 的擴額途徑。

## 操作流程

### 網頁設定入口

在 `/admin/videos?tab=settings#youtube-vps-settings` 的「VPS 上傳服務」卡設定
啟用狀態、服務網址、頻道 ID、服務密鑰與遠端桌面網址。只有具有
`settings.manage` 權限的管理員可儲存與測試連線；影片審閱者可查看設定狀態。
服務仍須先由營運者部署，網頁不會安裝 Docker 或建立上傳服務。

密鑰只寫入加密儲存，不會回傳到網頁；留白保留原密鑰。設定保存後即由 API
採用，無須為這些連線欄位重建容器。尚無網頁設定時才沿用原環境變數；網頁
明確停用後不會再回退到環境變數。過期版本的儲存會被拒絕，避免覆寫另一位
管理員的修改。更換服務網址必須提供新密鑰，不會把舊密鑰自動送往新主機。

「測試連線」只確認服務回應與頻道設定相符，不能證明 Google 已登入。
儲存設定及測試連線都會寫入網站紀錄，須在正式操作授權內進行；測試的是已儲存的設定。
「開啟遠端桌面登入」使用另外設定的登入網址，由站主在 VPS 專用瀏覽器
完成登入與驗證；本機 Studio 的登入不會轉移到 VPS。遠端桌面仍須經安全
連線存取，網址不可包含密碼或權杖。

服務 `/status` 的 `active_jobs` 包含準備、排隊、執行及等待人工接手的工作。
變更連線、頻道、密鑰或停用之前必須確認原服務沒有未完成工作；服務連不上
或舊版沒有這項計數時，設定切換會被拒絕，避免漏掉原服務的上傳紀錄。

1. 影片的 publish 上傳包須已核准。後台可以從原 API 表單、失敗進度卡，或尚未連 OAuth 的
   頻道提示進入「VPS 獨立上傳」；後者先選影片。
2. 已有 YouTube 影片時填原影片網址。網站或 VPS 已記錄 ID 的影片不會再次傳 MP4。
   API 曾開始上傳但還沒有 ID 時，必須先到 Studio 核對並填原影片網址。
3. 按「送到 VPS（私人）」。目前表單的標題與完整說明會隨請求固定；字幕、縮圖、標籤、
   翻譯、類別、目標觀眾與合成內容選項來自核准的上傳包。
4. **「準備／傳送素材」期間保留頁面。** 每次請求最多傳 4 MiB；離開、網路中斷或
   網站重啟後可以按「繼續傳送到 VPS」，從 VPS 已收到的位置接續。
5. 顯示「VPS 已排入佇列」後，可以關閉網頁。VPS 會獨立完成私人影片、詳細資料、縮圖、
   每份字幕、每組翻譯與每條已核准的配音音軌（見下方「配音音軌」）。新影片、既有影片都只接受私人狀態。
6. 遇到登入、驗證、頻道不符或 Studio 欄位變動，工作停在「需要你接手」。進遠端桌面
   檢查後回後台按繼續。程式不填 Google 密碼、不解驗證碼，也不繞過登入阻擋。
7. 完成後重新打開進度會把影片 ID 記錄到網站；若寫回失敗可按「記錄影片連結」。
   網頁關閉時 VPS 能完成工作，但網站資料在下次讀取並成功記錄後才更新。
8. 公開或排程發布由站主在 Studio 操作。本服務沒有公開影片或設定公開時間的動作。

同一頻道只有一個瀏覽器 worker；有一筆工作等待人工處理時，後面的工作也等待，避免搶走
站主正在處理的畫面。取消等待中的工作保留已知影片 ID 與素材，不會刪除 YouTube 影片。
開始傳 MP4 後若來不及取得 ID 就中斷，必須填回既有影片網址才能繼續，不能盲目重新上傳。
若此時上傳包已重新審核，可填原影片網址後取消舊工作，避免重跑舊資料。
舊工作完成或取消後，出現新版核准包時會顯示「將新版核准包送到 VPS」。

## 配音音軌（`dub_<locale>` 步驟）

**YouTube Data API 做不到這件事。** 2026-10-10 查 Data API v3 的 discovery document
（revision `20261006`）：只有 `captions.insert`／`captions.update` 收媒體檔，沒有 audioTracks
資源，也沒有任何上傳或管理音軌的方法。網站的 API 同步因此只能送標題、說明與字幕，永遠送不了
配音；配音只能經 Studio「語言」頁放上去。這個步驟就是由本服務去按那一頁的按鈕。2026-10-09
站主發現十六條按過「已上傳」的配音其實不在 YouTube 上，才有這個步驟。

步驟順序是：`video` → `details` → `thumbnail` → `captions_<locale>` → `localization_<locale>` →
`dub_<locale>` → `verify`。

- **素材**：已核准的 `languages` 審核裡狀態是 ready 的配音，網站以角色 `dub_<locale>`
  （語系小寫、連字號改底線：`dub_en`、`dub_ja`、`dub_ko`、`dub_zh_cn`）連同審核紀錄的
  SHA-256、大小與內容類型交給服務，來源綁定與核准規則和 `captions_<locale>` 完全相同。
  略過（skipped）的配音沒有檔案；`languages` 審核未核准時整個上傳包被拒絕，什麼都不送。
  原旁白語言不收配音。服務依內容類型決定副檔名：`audio/mp4` → `.m4a`、`audio/mpeg` → `.mp3`、
  `audio/wav`／`audio/x-wav` → `.wav`；單檔上限 1 GiB，一份 manifest 最多 12 個檔案。
- **Studio 操作**：先確認影片是私人 → 開 `/video/<id>/translations` → 找該語言的列
  （沒有就「Add language」加上）→ 配音格（selector `dubCell`）→ 按「Add」→ 把檔案放進
  對話框的檔案欄位（selector `dubFile`）→ 等「Publish」可按 → 按「Publish」→ 等對話框關閉、
  該格顯示 Published。這裡的 Publish 發布的是音軌，不是影片的瀏覽權限；最後的 `verify`
  會再確認影片仍是私人。
- **不重複**：該格已顯示 Published 時整步略過，不刪除、不取代、不再傳一次。換掉一條音軌
  要先刪除，那是站主的決定。
- **停下來的情況**：找不到配音格或找到多個、格子裡不是「Add」（例如上次中斷留下的草稿）
  → `studio_changed`；格子出現自動配音字樣 → `dub_needs_review`（先由站主刪除自動配音）；
  按了 Publish 但該格沒有顯示 Published → `save_unconfirmed`；影片不是私人 →
  `private_required`。停下時和其他步驟一樣記錄 `needs_action`、代碼與 `current_step`，
  站主進遠端桌面看畫面後再按繼續。本服務目前沒有自動截圖，任何步驟都沒有。
- **中斷後續跑**：`dub_<locale>` 與它的收據在同一次寫入裡記為完成。服務在 Studio 已發布、
  紀錄還沒寫下時中斷的話，續跑會重讀那一列，看到 Published 就不再傳第二次。
- **收據**：工作檢視（`GET /projects/:slug`、`GET /jobs/:id`）多一個 `dubs` 陣列，每條
  `{ locale, sha256, state }`：`placed` 是這筆工作親手放上去的；`present` 是 Studio 那一列
  本來就有已發布的配音，服務沒有送檔（無法證明那條就是這個 SHA-256，包括上面的中斷續跑）；
  `pending` 是步驟還沒完成。
- **還沒接上的事**：收據目前不會自動核准 `languages` 審核。現在仍是站主核准那張卡之後，
  上傳包才帶配音；讓收據取代站主的按鈕是另一個決定。後台進度清單也還沒有 `dub_<locale>`
  步驟的文字。
- **只收私人影片**：和其他步驟一樣，已公開的影片會停在 `private_required`，所以已上架影片
  缺的配音目前不能走這條路補。
- **`dubCell`、`dubFile` 和其他 selector 一樣是暫定的**，「Add」「Publish」「Published」
  「Add language」等英文字樣與對話框流程也是，只在合成 DOM 上測過，沒看過真實 Studio。

頻道要先具備兩個一次性設定，都是站主的事（[`DUBS.md`](DUBS.md) §站主要做的事）：
「進階功能」已啟用；「允許自動配音」取消，否則英文會先被自動配音佔住，上傳自己的英文音軌前
要先刪掉它。

## 在獨立 VPS 準備容器

### mokaair.com 同機部署

站主已指定 mokaair.com 正式主機。2026-09-28 的唯讀預檢顯示 4 vCPU、約 16 GiB RAM
（當時約 13 GiB 可用）、約 91 GiB 磁碟可用，Docker 與 Compose 已安裝，8789／6080
未使用。這是當時的容量，正式執行前仍須重做預檢。目前尚未部署或登入 Google。

採用兩個 Compose project：網站原有 project，以及獨立的 `mokaair-studio-uploader`。
`docker-compose.prod.yml` 讓 API 額外加入 internal 的 `uploader_rpc` 網路，並唯讀掛入
`/etc/mokaair-uploader/api`。網站其他容器不加入這個網路。上傳服務用
`compose.mokaair.yml` 接上同一網路，另保留自己的對外網路連 YouTube。
網站一般更新會重建 API，服務名稱與密鑰掛載仍存在；不需要修改主機部署腳本。

待站主核准的執行順序：

1. 核對包含 #890／#893 uploader 與 #1046 網頁設定的實際合併版本及其檢查，
   依 `deploy` skill 預檢、備份與部署網站。首次安裝時保持網頁設定尚未啟用，且
   `MOKAAIR_VPS_UPLOADER_URL` 未設定；若已有連線或工作，先按下方停用／切換流程處理，
   不能只移除環境變數。網站部署會建立 RPC 網路。
2. 首次建立服務密鑰與 VNC 密碼，另保留 API UID 10001 能讀的同值密鑰檔，供舊版環境
   變數回退使用；網頁設定保存後改讀加密的 DB 密鑰。
   下列初始化只適用於尚無這些檔案的主機；已有檔案時停止，不覆寫或輪換：

   ```sh
   set -eu
   test ! -e /etc/mokaair-uploader/service-secret
   test ! -e /etc/mokaair-uploader/vnc-password
   test ! -e /etc/mokaair-uploader/api/service-secret
   install -d -m 0700 /etc/mokaair-uploader
   install -d -m 0700 -o 10001 -g 10001 /etc/mokaair-uploader/api
   (umask 077; openssl rand -hex 32 > /etc/mokaair-uploader/service-secret)
   (umask 077; openssl rand -hex 4 > /etc/mokaair-uploader/vnc-password)
   chown 1000:1000 /etc/mokaair-uploader/service-secret /etc/mokaair-uploader/vnc-password
   chmod 0400 /etc/mokaair-uploader/service-secret /etc/mokaair-uploader/vnc-password
   install -m 0400 -o 10001 -g 10001 /etc/mokaair-uploader/service-secret /etc/mokaair-uploader/api/service-secret
   ```

3. 從範例建立 `ops/youtube-uploader/.env`（維持 0600），設定確定的 UC 頻道 ID，保留
   `UPLOADER_PRIVATE_BIND_IP=127.0.0.1` 及 `UPLOADER_API_NETWORK=travel_scanner_uploader_rpc`。
   從已核對合併版本的 repo 根目錄執行：

   ```sh
   docker compose --env-file ops/youtube-uploader/.env -f ops/youtube-uploader/compose.yml -f ops/youtube-uploader/compose.mokaair.yml build
   docker compose --env-file ops/youtube-uploader/.env -f ops/youtube-uploader/compose.yml -f ops/youtube-uploader/compose.mokaair.yml up -d --no-build
   curl --fail http://127.0.0.1:8789/health
   ```

4. 容器啟動驗證後，經站主核准，由 `settings.manage` 管理員在網頁設定卡填入
   `http://mokaair-studio-uploader:8789`、已確認的 UC 頻道 ID、同一份服務密鑰及安全的
   遠端桌面網址，再啟用並儲存。不是填密鑰檔路徑，也不是填 Google 或 VNC 密碼。
   保存後 API 立即使用 DB 設定，無須為這些欄位重建容器；舊版環境配置見下節。
5. 按「測試連線」，由 API 使用已保存的密鑰驗證 authenticated `/status` 與頻道設定。
   若仍採舊版環境配置，另驗 API UID 10001 對唯讀密鑰檔的讀取權限。
   只回報通過與否，不輸出密鑰、完整環境變數或瀏覽器狀態；成功不代表 Google 已登入。
6. 站主經 SSH 隧道登入專用瀏覽器，核對頻道，再指定一支私人測試影片進行下方驗收。

同機模式的啟停／升級都須帶上上述兩個 `-f`，保留獨立 volume。不要對網站執行
`docker compose down`：它會嘗試刪除 uploader 使用中的共享網路；正常網站部署使用 `up`。
正常回退須先讓原服務完成空佇列驗證及網站停用，再停止 uploader，詳見下方
「停用、切換與緊急停止」。Google 登入與真實上傳仍須獨立驗收，健康檢查不足以啟用自動上傳。

### 另一台獨立 VPS

以下是交付給營運者的指令，**本次沒有在正式主機執行**。建議預留 4 GiB RAM、2 vCPU，
以及至少容納待傳影片總量兩倍的磁碟；這是起始規格，尚未經真實大檔負載測試。
需要 Linux、Docker Engine 與 Compose plugin、可連 YouTube 的網路，以及站主 SSH 存取。

在已核對版本的 repo 根目錄，準備 secret 檔（密鑰不可放在 Git 或命令列參數）：

```sh
sudo install -d -m 0700 /etc/mokaair-uploader
sudo sh -c 'umask 077; openssl rand -hex 32 > /etc/mokaair-uploader/service-secret'
sudo sh -c 'umask 077; openssl rand -hex 4 > /etc/mokaair-uploader/vnc-password'
sudo chown 1000:1000 /etc/mokaair-uploader/service-secret /etc/mokaair-uploader/vnc-password
sudo chmod 0400 /etc/mokaair-uploader/service-secret /etc/mokaair-uploader/vnc-password
cp ops/youtube-uploader/.env.example ops/youtube-uploader/.env
```

編輯 `.env` 的頻道 ID、兩個 secret **路徑**；不得把密鑰內容填進 `.env`。
容器以 UID 1000 執行；Compose 的本機 file secrets 依來源檔權限掛載，所以檔案必須讓
容器 UID 1000 可讀。網站設定使用同一份服務密鑰；Google 帳密不出現在這些檔案中。
VNC 傳統密碼只使用前 8 個字元，主要存取保護是 SSH 隧道。

```sh
docker compose --env-file ops/youtube-uploader/.env -f ops/youtube-uploader/compose.yml build
docker compose --env-file ops/youtube-uploader/.env -f ops/youtube-uploader/compose.yml up -d
docker compose --env-file ops/youtube-uploader/.env -f ops/youtube-uploader/compose.yml ps
curl --fail http://127.0.0.1:8789/health
```

預設 HTTP 8789 與遠端桌面 6080 都只發佈在 VPS 的 `127.0.0.1`。
要讓另一台主機的網站存取，先建立私人 VPN（例如 WireGuard），再設定
`UPLOADER_PRIVATE_BIND_IP` 為 VPS 的 VPN IP，且防火牆僅允許網站主機。
不要設定 `0.0.0.0` 或公網 IP。Bearer 密鑰不能透過公網明文 HTTP 傳送；若使用 HTTPS
反向代理，需額外限制來源且禁止記錄 Authorization header。noVNC 維持 loopback。

## 站主登入

在站主電腦開 SSH 隧道（把 `your-vps` 換成自己的主機）：

```sh
ssh -N -L 6080:127.0.0.1:6080 your-vps
```

瀏覽 `http://127.0.0.1:6080/vnc.html`，輸入自己設定的 VNC 密碼，在 VPS 的獨立 Chromium
登入 YouTube Studio。站主親自處理登入、二階段驗證與帳號警告，切換到指定頻道，並把
Studio 介面語言設為 English。Playwright 的 locale 不會覆蓋已登入 Google 帳戶的語言設定。
Google 若拒絕自動化瀏覽器登入，停止此路線並使用手動模式；不要停用帳號保護或搬移 Cookie。

瀏覽器登入狀態只儲存在 `uploader-data` volume 的 `browser/`，與站主本機 Chrome、主網站
OAuth 完全分開。保護整個 volume；不要把它打包到一般附件、測試輸出、PR 或公開備份。

## 網站連線設定與舊版環境回退

目前以「VPS 上傳服務」網頁設定卡為主，保存後即時生效，密鑰加密存入 DB。
只有尚未保存網頁設定時，才使用以下舊版環境變數回退；只執行過連線測試、尚未保存設定的
診斷紀錄不會中止回退。網頁明確停用後仍以 DB 為準，不會重新採用環境變數。

保留舊版環境配置時，在主網站 **API 容器** 加入下列環境變數，並唯讀掛入密鑰檔；
API 容器的實際 UID 必須有讀取權限。檔案經既有機密管理流程提供，不經聊天訊息或 Git。
這條舊路線變更環境或掛載後才需要依已核准步驟重建 API：

```dotenv
MOKAAIR_VPS_UPLOADER_URL=http://10.42.0.2:8789
MOKAAIR_VPS_UPLOADER_SECRET_FILE=/run/secrets/youtube-uploader
MOKAAIR_VPS_UPLOADER_CHANNEL_ID=UC_replace_with_your_channel_id
```

同機舊版配置改用 `MOKAAIR_VPS_UPLOADER_URL=http://mokaair-studio-uploader:8789` 與
`MOKAAIR_VPS_UPLOADER_SECRET_FILE=/run/mokaair-uploader/service-secret`，對應既有 API 掛載。
`10.42.0.2` 是範例，需替換成實際私人 VPN 位址。容器內的 `127.0.0.1` 指容器自己，不能
直接拿來連另一台 VPS。若服務與網站同機，可由營運者把兩者接入共同的私人 Docker network，
URL 使用服務名稱；不要因此公開 HTTP port。此功能不需資料庫 migration。
網頁設定入口是 `/admin/videos?tab=settings#youtube-vps-settings`，不是通用 `/admin/settings`。
URL、頻道與來源會顯示在設定卡；服務密鑰只供有權管理員輸入，不會由 API 回傳。

只有仍採環境回退時，省略 `MOKAAIR_VPS_UPLOADER_URL` 才會停用網站入口；已有 DB 設定時，
移除環境變數不會改變啟用狀態。停用網站入口也不會停止 VPS 已有工作，必須依下節處理。
VPS 啟用時，網站 API 上傳會先檢查同一影片有沒有 VPS 工作；VPS 連不上時拒絕開始另一筆，
避免在不知道遠端狀態的情況下建立重複影片。

### 停用、切換與緊急停止

以下操作都須在站主核准的版本與操作範圍內進行，並保留 Google 登入及真人上傳驗收門檻。

正常停用或更換連線、頻道、密鑰時：

1. 與操作人員協調停止提交新工作，先完成或經核准取消原服務的待處理工作，保留影片 ID
   與素材；等待人工接手的工作也算 active。上傳已開始卻尚無 ID 時先到 Studio 核對，
   不因取消而建立第二次 MP4 上傳。
2. **保持原服務可達**，再於網頁設定卡停用或儲存核准的新連線。保存時會認證原服務並要求
   `active_jobs == 0`；原服務不可達、未提供計數或仍有工作時即拒絕。過期版本須重新讀取、
   核對後再存，不能盲目覆寫；更換 URL 須提供新服務密鑰。
3. 保存成功並重讀確認後，只有停用或切換到另一服務時，才按核准步驟停止舊 uploader、
   保留 volume。同一服務校正頻道或輪換密鑰，則依已核准計畫測試已保存的連線，確認認證與
   頻道相符；不預設停止目前有效的服務。

DB 停用即時生效，不回退到環境變數。確認原工作與影片 ID 已核對、舊服務已停止後，才可按
另行批准的步驟恢復原 API 上傳。既有環境配置也可經設定卡保存停用，採用同一個空佇列守門。

如緊急情況必須先停止服務，先保留工作資料、已知影片 ID 與登入 profile，再按核准步驟停止。
此時網站設定仍可能顯示啟用，後續停用／切換會因無法認證原服務空佇列而拒絕。保留現場，
待核准的復原流程能確認原佇列後再處理；不直接修改 DB、不清除 volume、不重傳或改走另一
上傳路線來繞過守門。單純移除網站環境 URL 不能解除 DB 設定或已存在的工作。

同機停止必須保留兩份 Compose 檔：

```sh
docker compose --env-file ops/youtube-uploader/.env -f ops/youtube-uploader/compose.yml -f ops/youtube-uploader/compose.mokaair.yml stop
```

只有「另一台獨立 VPS」配置才使用單份檔案：

```sh
docker compose --env-file ops/youtube-uploader/.env -f ops/youtube-uploader/compose.yml stop
```

## Studio 介面變更與復原

操作器只透過 DOM 控制項，不使用 Studio 私有 API。找不到控制項或找到多個時會停止。
預設控制項在 `services/youtube-uploader/src/studio.mjs` 的 `DEFAULT_SELECTORS`。
**這些選擇器尚未在站主真實 Studio 驗收。** 維護者先用遠端桌面核對畫面，必要時更新
操作器與測試；單純 selector 變動可掛入 JSON 檔並設定 `UPLOADER_SELECTORS_FILE`。
JSON 僅接受該常數列出的鍵，例如 `{ "title": "#title-textarea #textbox" }`。
修改 selector 不能替代流程驗收，英文按鈕名稱或精靈步驟改變仍需要更新程式。

| 狀態 / 代碼 | 處理方式 |
| --- | --- |
| staging | 保留原工作，按繼續傳送；不要建立新工作 |
| login_required / verification_required | 在安全遠端桌面由站主登入或驗證 |
| channel_unconfirmed | 核對設定的 UC 頻道 ID 與目前 Studio 頻道 |
| private_required | 核對原影片；服務不會把公開影片自行改成私人 |
| interrupted / video_id_required | 核對是否已有影片，必要時貼原影片網址，再繼續 |
| studio_changed / save_unconfirmed | 先檢查畫面與更新操作器，不要連續盲按重試 |
| dub_needs_review | 該語言已有自動配音；站主在 Studio 刪除後再繼續，並確認「允許自動配音」已取消 |
| file_hash_mismatch | 核對素材與磁碟；不略過完整 SHA-256 驗證 |

工作 SQLite 紀錄每一步、已知影片 ID、素材雜湊與傳送位移。服務重啟時，原先 running 的
工作轉 needs_action；不假設上次點擊成功，也不自動重送影片。已確認完成的步驟不重做。
同一資料目錄用 SQLite 的持續 exclusive lock 防止啟動第二個 daemon；不可把同一頻道
拆成多個互不共享紀錄的 uploader。

取消工作不刪素材。本版沒有自動清理機制，營運者需監看 volume 用量；停止服務後才可備份，
備份需包含整個資料目錄與工作資料庫，並當作登入機密加密保管。復原到相同版本、相同頻道，
確認沒有另一個執行中的實例後啟動；檢查所有 needs_action 工作再繼續。
停止服務的順序與同機／獨立 VPS 命令見「停用、切換與緊急停止」。
一般停止與升級不要使用 `down -v`；刪除 volume 會失去工作 ID 與登入資料，破壞去重依據。

## 通訊契約

以下服務端路徑除 `/health` 外全部要求 `Authorization: Bearer <service secret>`。
瀏覽器只呼叫網站 BFF，不會直接存取 VPS。設定卡可提交管理員輸入的服務密鑰，
但網站不會回傳已儲存的密鑰；上傳操作由 API 帶密鑰呼叫服務 RPC。

| 路徑 | 用途 |
| --- | --- |
| GET /health | HTTP 存活；不證明 Google 登入或 Studio 版面相容 |
| GET /status | 指定頻道與 worker 狀態 |
| GET /projects/:slug | 該專案最新工作；回覆不含密鑰、標題、Cookie 或瀏覽器網址 |
| PUT /jobs/:sha256 | 建立 immutable manifest；相同 ID / 內容回傳原工作 |
| PUT /jobs/:id/files/:sha256?offset=N | 依位移追加至核准大小，完成時驗完整雜湊 |
| POST /jobs/:id/queue | 每份檔案長度與雜湊通過後排入 |
| POST /jobs/:id/resume | 人工處理後續跑；可帶已核對的 video_id |
| POST /jobs/:id/cancel | 取消等待；保留素材與已知影片 ID |

網站工作 ID 為 `sha256(slug + ':' + approved metadata sha256)`。工作建立後的標題與說明
固定在該 manifest；更改後台表單不會改寫進行中的工作。新核准版本可帶原影片 ID 建立另一筆，
但原工作 active 時會拒絕。素材只接受核准的本機 review-store 檔案，不接受任意下載 URL。
manifest 的檔案角色是 `final`、`thumbnail`、`captions_<locale>` 與 `dub_<locale>`；工作檢視
除了 `steps`、`files`，另有 `dubs`（每條配音的語系、SHA-256 與 `placed`／`present`／`pending`）。

## 驗證

```sh
cd services/youtube-uploader
npm ci
npx playwright install chromium
npm test
```

網站測試：

```sh
cd apps/api
uv run pytest tests/test_video_youtube_vps.py tests/test_video_youtube.py tests/test_video_youtube_sync.py -q
uv run ruff check app/video_youtube tests/test_video_youtube_vps.py
uv run mypy app/video_youtube tests/test_video_youtube_vps.py
```

```sh
npm run test:web -- components/admin-video-vps-upload.test.tsx components/admin-video-manual-upload.test.tsx components/admin-video-youtube.test.tsx
npm run check:i18n
npm run typecheck:web
```

`.github/workflows/youtube-uploader.yml` 額外跑 Node/Chromium fixture tests、獨立 Docker build，
以及無 Google 帳號的 Xvfb/noVNC/HTTP 啟動檢查。主 CI 執行網站與 API 的檢查。
2026-09-28 已在 commit `24424d4a` 通過獨立 workflow 的測試、Docker Compose build 與無帳號啟動：
[CI 執行紀錄](https://github.com/x812033727/travel_scanner/actions/runs/36386376526)。
新增的同機檢查會以 API UID 10001 讀取唯讀密鑰、核對 Docker DNS 與 authenticated status，
並重建 client 後再測一次。CI 使用拋棄式網路、假密鑰與無登入瀏覽器。
這份歷史紀錄不包含同機檢查、真實 Google 登入或影片上傳；同機改動仍須對應版本的 CI。

### 啟用前真人驗收（未執行）

取得站主對指定 VPS、部署版本、登入與測試影片的授權後：

- 在專用測試頻道或已核准的私人測試影片驗證每個 DOM 步驟；確認沒有公開或排程。
- 完整跑一次 MP4、標題、含章節的完整說明、觀眾／合成內容設定、標籤、類別、縮圖、字幕與翻譯。
- 離開後台再重開；重新讀取 Studio 持久化內容，核對網站記錄的 ID 為同一支影片。
- 在素材傳送中重啟網站；在 Studio 工作中重啟 uploader；確認位移復原、人工確認與不重複上傳。
- 驗證登入逾時、Google 驗證要求、公開影片拒絕、不同頻道拒絕、兩筆排隊與舊字幕更新。
- 配音音軌：先用**一支私人影片、一個配音語系**驗收，再擴到其他語系。逐項記錄版本與結果：
  - 頻道已啟用「進階功能」，且「允許自動配音」已取消（英文尤其要確認該列沒有自動配音）。
  - Studio 收不收 `.m4a`；不收就改用 `--format mp3` 重做配音再驗一次。
  - 影片還是私人時能不能加音軌。
  - 音軌的「Publish」會不會動到影片的瀏覽權限（預期不會；`verify` 會擋下變成非私人的影片）。
  - `dubCell`、`dubFile`、「Add」「Publish」「Published」是否與真實畫面相符；檔案處理多久後
    Publish 才可按。
  - 重跑同一工作不會出現第二條音軌；Studio 工作中重啟 uploader 後續跑也不會。
  - 收據 `dubs` 的語系與 SHA-256 和核准的 `languages` 審核一致，並在播放器實際切到該音軌聽過。
- 選擇器若需調整，將真實觀察整理成不含登入機密的 fixture，再重跑回歸測試。

參考：[Studio 上傳流程](https://support.google.com/youtube/answer/57407?hl=en)、
[字幕上傳](https://support.google.com/youtube/answer/2734796?hl=en)、
[Playwright persistent context](https://playwright.dev/docs/api/class-browsertype#browser-type-launch-persistent-context)。
