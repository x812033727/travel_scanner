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

1. 影片的 publish 上傳包須已核准。後台可以從原 API 表單、失敗進度卡，或尚未連 OAuth 的
   頻道提示進入「VPS 獨立上傳」；後者先選影片。
2. 已有 YouTube 影片時填原影片網址。網站或 VPS 已記錄 ID 的影片不會再次傳 MP4。
   API 曾開始上傳但還沒有 ID 時，必須先到 Studio 核對並填原影片網址。
3. 按「送到 VPS（私人）」。目前表單的標題與完整說明會隨請求固定；字幕、縮圖、標籤、
   翻譯、類別、目標觀眾與合成內容選項來自核准的上傳包。
4. **「準備／傳送素材」期間保留頁面。** 每次請求最多傳 4 MiB；離開、網路中斷或
   網站重啟後可以按「繼續傳送到 VPS」，從 VPS 已收到的位置接續。
5. 顯示「VPS 已排入佇列」後，可以關閉網頁。VPS 會獨立完成私人影片、詳細資料、縮圖、
   每份字幕與每組翻譯。新影片、既有影片都只接受私人狀態。
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

## 在獨立 VPS 準備容器

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
容器 UID 1000 可讀。一般操作員不需讀取服務密鑰，Google 帳密不出現在這些檔案中。
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

## 網站連線設定

在主網站 **API 容器** 加入環境變數，並唯讀掛入密鑰檔。API 容器的實際 UID 必須有讀取權限。
把同一份密鑰用營運者既有的機密管理流程送到網站主機，不經前端、聊天訊息或 Git：

```dotenv
MOKAAIR_VPS_UPLOADER_URL=http://10.42.0.2:8789
MOKAAIR_VPS_UPLOADER_SECRET_FILE=/run/secrets/youtube-uploader
MOKAAIR_VPS_UPLOADER_CHANNEL_ID=UC_replace_with_your_channel_id
```

`10.42.0.2` 是範例，需替換成實際私人 VPN 位址。容器內的 `127.0.0.1` 指容器自己，不能
直接拿來連另一台 VPS。若服務與網站同機，可由營運者把兩者接入共同的私人 Docker network，
URL 使用服務名稱；不要因此公開 HTTP port。此功能不需資料庫 migration。
上述設定不會經 `/admin/settings` 編輯，也不會回傳給瀏覽器。

省略 `MOKAAIR_VPS_UPLOADER_URL` 即停用網站入口的提交功能。已存在於 VPS 的工作不會因
網站移除設定而停止，因此有未完成工作時必須先在後台處理，或停止獨立容器。
VPS 啟用時，網站 API 上傳會先檢查同一影片有沒有 VPS 工作；VPS 連不上時拒絕開始另一筆，
避免在不知道遠端狀態的情況下建立重複影片。

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
| file_hash_mismatch | 核對素材與磁碟；不略過完整 SHA-256 驗證 |

工作 SQLite 紀錄每一步、已知影片 ID、素材雜湊與傳送位移。服務重啟時，原先 running 的
工作轉 needs_action；不假設上次點擊成功，也不自動重送影片。已確認完成的步驟不重做。
同一資料目錄用 SQLite 的持續 exclusive lock 防止啟動第二個 daemon；不可把同一頻道
拆成多個互不共享紀錄的 uploader。

取消工作不刪素材。本版沒有自動清理機制，營運者需監看 volume 用量；停止服務後才可備份，
備份需包含整個資料目錄與工作資料庫，並當作登入機密加密保管。復原到相同版本、相同頻道，
確認沒有另一個執行中的實例後啟動；檢查所有 needs_action 工作再繼續。
暫停全部工作可執行 `docker compose --env-file ops/youtube-uploader/.env -f ops/youtube-uploader/compose.yml stop`。
一般停止與升級不要使用 `down -v`；刪除 volume 會失去工作 ID 與登入資料，破壞去重依據。

## 通訊契約

以下服務端路徑除 `/health` 外全部要求 `Authorization: Bearer <service secret>`。
瀏覽器只呼叫網站 BFF；不會知道 secret，也不會直接存取 VPS。

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
2026-09-28 已在 commit `0b105dc3` 通過獨立 workflow 的測試、Docker build 與無帳號啟動：
[CI 執行紀錄](https://github.com/x812033727/travel_scanner/actions/runs/36383247014)。
這份紀錄不包含真實 Google 登入或影片上傳；後續修正仍需對應版本的 CI。

### 啟用前真人驗收（未執行）

取得站主對指定 VPS、部署版本、登入與測試影片的授權後：

- 在專用測試頻道或已核准的私人測試影片驗證每個 DOM 步驟；確認沒有公開或排程。
- 完整跑一次 MP4、標題、含章節的完整說明、觀眾／合成內容設定、標籤、類別、縮圖、字幕與翻譯。
- 離開後台再重開；重新讀取 Studio 持久化內容，核對網站記錄的 ID 為同一支影片。
- 在素材傳送中重啟網站；在 Studio 工作中重啟 uploader；確認位移復原、人工確認與不重複上傳。
- 驗證登入逾時、Google 驗證要求、公開影片拒絕、不同頻道拒絕、兩筆排隊與舊字幕更新。
- 選擇器若需調整，將真實觀察整理成不含登入機密的 fixture，再重跑回歸測試。

參考：[Studio 上傳流程](https://support.google.com/youtube/answer/57407?hl=en)、
[字幕上傳](https://support.google.com/youtube/answer/2734796?hl=en)、
[Playwright persistent context](https://playwright.dev/docs/api/class-browsertype#browser-type-launch-persistent-context)。
