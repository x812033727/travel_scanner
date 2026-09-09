const en = {
  title: "Hotels & booking platforms", subtitle: "Explore reviewed hotel links. Choose a hotel first, then its booking platform — no map required.",
  publicPage: "Public hotel directory", home: "Home", trips: "My trips", privacy: "Privacy", back: "Back to travel planning",
  disclosure: "This page uses Stay22's official script, including automatic partner-link conversion and Spark / Nova recommendations. We may earn a commission. Prices, availability and booking terms are confirmed on the external platform.",
  dataNotice: "Loading this page may share its public content and browser/device information with Stay22. No personal itinerary settings are loaded here. This third-party script runs on this website; this is not an isolated browser security origin.",
  dateNotice: "Set and confirm your dates, guests, rooms and cancellation terms on the booking platform. No private trip dates are transferred to this page.",
  originalNotice: "Reviewed original links are shown below. Stay22 may convert supported links; loading the script does not verify attribution. If conversion is unavailable, the original link remains usable.",
  scriptUnavailable: "Stay22 could not load. Original hotel links remain available; commission tracking is not confirmed.",
  loading: "Loading reviewed hotels…", empty: "No reviewed hotels are available for this destination yet.", error: "Unable to load hotels. Your page is unchanged; please try again.", retry: "Try again",
  open: "View booking platforms", close: "Close", platformLoading: "Loading reviewed platform links…", platformError: "Unable to load platform links. Please try again, or reload to use the latest site setting.",
  noLinks: "No currently reviewed exact hotel links are available. We do not substitute a search page for this hotel.",
  platform: "Open {platform}", official: "Hotel website", newTab: "Opens in a new tab", reload: "Reload page",
};
type Copy = Record<keyof typeof en, string>;
const copies: Record<string, Copy> = {
  en,
  "zh-TW": {
    title: "住宿與預訂平台", subtitle: "瀏覽已審核的飯店連結，先選飯店、再選訂房平台，不必先開地圖。", publicPage: "公開住宿目錄", home: "首頁", trips: "我的旅行", privacy: "隱私政策", back: "返回行程規劃",
    disclosure: "本頁使用 Stay22 官方 Script，包含合作連結自動轉換及 Spark／Nova 推薦；我們可能獲得佣金。實際價格、供應與訂房條款以外站為準。",
    dataNotice: "載入本頁可能將公開內容與瀏覽器／裝置資訊提供給 Stay22；這裡不載入私人行程設定。第三方程式在本站執行，此頁不是獨立的瀏覽器安全網域。",
    dateNotice: "請到訂房平台設定並確認日期、人數、房數及取消條件；本頁不帶入私人旅程日期。",
    originalNotice: "以下為已審核的原始連結，Stay22 可能轉換支援平台的連結。載入程式不代表已驗證分潤歸屬；無法轉換時仍可使用原連結。",
    scriptUnavailable: "Stay22 程式未能載入；原始飯店連結仍可使用，但無法確認分潤追蹤。",
    loading: "正在載入已審核飯店…", empty: "這個目的地尚無可顯示的已審核飯店。", error: "暫時無法載入飯店，原頁面仍保留，請稍後重試。", retry: "重試", open: "查看預訂平台", close: "關閉", platformLoading: "正在載入已審核平台連結…", platformError: "暫時無法載入平台連結。請重試，或重新整理以使用最新設定。", noLinks: "目前沒有審核有效的精確飯店連結，不會以搜尋頁冒充這間飯店。", platform: "前往 {platform}", official: "飯店官網", newTab: "另開新分頁", reload: "重新整理頁面",
  },
  "zh-CN": {
    title: "住宿与预订平台", subtitle: "浏览已审核的酒店链接，先选酒店、再选预订平台，无需先打开地图。", publicPage: "公开住宿目录", home: "首页", trips: "我的旅行", privacy: "隐私政策", back: "返回行程规划",
    disclosure: "本页使用 Stay22 官方 Script，包括合作链接自动转换和 Spark／Nova 推荐；我们可能获得佣金。实际价格、供应及预订条款以外站为准。", dataNotice: "加载本页可能向 Stay22 提供公开内容及浏览器／设备信息；这里不加载私人行程设置。第三方程序在本站执行，本页不是独立的浏览器安全域。", dateNotice: "请在预订平台设置并确认日期、人数、房数及取消条件；本页不带入私人旅行日期。", originalNotice: "下方是已审核的原始链接，Stay22 可能转换支持平台的链接。加载程序不等于分佣归属已验证；无法转换时仍可使用原链接。", scriptUnavailable: "Stay22 程序无法加载；原始酒店链接仍可使用，但无法确认分佣追踪。", loading: "正在加载已审核酒店…", empty: "这个目的地暂无可显示的已审核酒店。", error: "暂时无法加载酒店，原页面仍保留，请稍后重试。", retry: "重试", open: "查看预订平台", close: "关闭", platformLoading: "正在加载已审核的平台链接…", platformError: "暂时无法加载平台链接。请重试，或刷新以使用最新设置。", noLinks: "目前没有审核有效的精确酒店链接，不会以搜索页面替代。", platform: "前往 {platform}", official: "酒店官网", newTab: "在新标签页打开", reload: "刷新页面",
  },
  ja: {
    title: "ホテル・予約サイト", subtitle: "確認済みのホテルを選び、予約サイトへ。地図を開く必要はありません。", publicPage: "公開ホテル一覧", home: "ホーム", trips: "旅行一覧", privacy: "プライバシー", back: "旅行プランに戻る",
    disclosure: "このページでは Stay22 公式 Script のリンク変換と Spark／Nova 提案を使用し、当サイトが紹介料を受け取る場合があります。料金、空室、予約条件は外部サイトでご確認ください。", dataNotice: "読み込み時に公開内容とブラウザー・端末情報が Stay22 に提供される場合があります。個人の旅行設定は読み込みません。第三者プログラムは当サイトで実行され、独立したセキュリティオリジンではありません。", dateNotice: "日付、人数、部屋数、キャンセル条件は予約サイトで設定・確認してください。個人の旅行日付は引き継ぎません。", originalNotice: "確認済みの元リンクを表示します。Stay22 が対応リンクを変換する場合がありますが、紹介料の帰属確認を意味しません。変換できない場合も元リンクを使用できます。", scriptUnavailable: "Stay22 を読み込めません。元のホテルリンクは利用できますが、紹介料の追跡は確認できません。", loading: "確認済みホテルを読み込み中…", empty: "この目的地には表示できる確認済みホテルがありません。", error: "ホテルを読み込めません。もう一度お試しください。", retry: "再試行", open: "予約サイトを見る", close: "閉じる", platformLoading: "確認済みリンクを読み込み中…", platformError: "リンクを読み込めません。再試行するか、ページを再読み込みしてください。", noLinks: "有効な確認済みホテルリンクがありません。検索ページで代用しません。", platform: "{platform} を開く", official: "ホテル公式サイト", newTab: "新しいタブで開く", reload: "再読み込み",
  },
  ko: {
    title: "숙소 및 예약 플랫폼", subtitle: "검토된 호텔을 고른 후 예약 플랫폼을 선택하세요. 지도를 먼저 열 필요가 없습니다.", publicPage: "공개 숙소 목록", home: "홈", trips: "내 여행", privacy: "개인정보 정책", back: "여행 계획으로 돌아가기",
    disclosure: "이 페이지는 Stay22 공식 Script의 링크 변환과 Spark／Nova 추천을 사용하며 수수료를 받을 수 있습니다. 가격, 객실 및 예약 조건은 외부 사이트에서 확인하세요.", dataNotice: "로딩 시 공개 콘텐츠와 브라우저·기기 정보가 Stay22에 제공될 수 있습니다. 개인 여행 설정은 불러오지 않습니다. 제3자 프로그램은 이 사이트에서 실행되며 별도 보안 출처가 아닙니다.", dateNotice: "예약 플랫폼에서 날짜, 인원, 객실 수 및 취소 조건을 설정하고 확인하세요. 개인 여행 날짜는 전달하지 않습니다.", originalNotice: "검토된 원본 링크가 표시됩니다. Stay22가 지원 링크를 변환할 수 있지만 수수료 귀속 검증을 의미하지 않습니다. 변환하지 못해도 원본 링크를 사용할 수 있습니다.", scriptUnavailable: "Stay22를 불러오지 못했습니다. 원본 호텔 링크는 사용할 수 있지만 수수료 추적은 확인되지 않았습니다.", loading: "검토된 호텔을 불러오는 중…", empty: "이 목적지에는 표시할 검토된 호텔이 없습니다.", error: "호텔을 불러오지 못했습니다. 다시 시도하세요.", retry: "재시도", open: "예약 플랫폼 보기", close: "닫기", platformLoading: "검토된 링크를 불러오는 중…", platformError: "링크를 불러오지 못했습니다. 다시 시도하거나 페이지를 새로 고치세요.", noLinks: "유효한 검토된 호텔 링크가 없습니다. 검색 페이지로 대체하지 않습니다.", platform: "{platform} 열기", official: "호텔 공식 사이트", newTab: "새 탭에서 열기", reload: "새로 고침",
  },
};
export function stay22ScriptCopy(locale: string): Copy { return copies[locale] || en; }
