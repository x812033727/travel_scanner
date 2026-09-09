import type { Locale } from "@/i18n/routing";

const en = {
  title: "Hotels", intro: "Manage hotel records, review each booking platform, and configure hotel services in one workspace.",
  partnersTitle: "Partners and brands", partnersIntro: "Shared brand approval applies across hotels and other travel services. Product and booking-link reviews remain separate.",
  catalog: "Hotel catalog", review: "Review and platforms", affiliates: "Affiliate offers", imports: "Import and coverage", settings: "Hotel settings",
  products: "Hotel records", platforms: "Booking platforms", destinations: "Destination offers", import: "CSV import", coverage: "Coverage", providers: "Provider configuration",
  partners: "Manage shared partners", other: "Other travel services", shared: "Shared publishing and destination gates are read-only here. Changing hotel settings never enables another service, a city, or the Airalo feed.",
  hotelOnly: "Only hotel rows are accepted. Existing source keys cannot be reassigned from another service. Importing never approves hotel records, booking links, or brands.",
  draft: "Unsaved hotel configuration is retained while switching tabs.", total: "Hotels", pending: "Pending review", approved: "Approved", unavailable: "Disabled",
  conflict: "Hotel settings changed elsewhere. Your draft is retained; reload the latest settings before editing again.", reload: "Reload latest settings", discard: "Discard this hotel settings draft and load the latest saved settings?",
  leave: "Hotel settings have unsaved changes. Leave this page?",
  missingOptions: "No booking links recorded", showAllHotels: "Show all hotels",
};
type Copy = { [K in keyof typeof en]: string };
const copies: Record<Locale, Copy> = {
  en,
  "zh-TW": {
    title: "飯店", intro: "集中管理飯店目錄、各訂房平台審核與飯店服務設定。",
    partnersTitle: "合作夥伴與品牌", partnersIntro: "品牌核准由飯店及其他旅遊服務共用；飯店資料、訂房連結仍需各自審核。",
    catalog: "飯店目錄", review: "審核與平台", affiliates: "聯盟連結", imports: "匯入與覆蓋率", settings: "飯店設定",
    products: "飯店資料", platforms: "訂房平台", destinations: "目的地連結", import: "CSV 匯入", coverage: "覆蓋率", providers: "供應商設定",
    partners: "管理共用合作夥伴", other: "其他旅遊服務", shared: "全站公開與城市開關在此僅供查看。修改飯店設定不會啟用其他服務、城市或 Airalo 資料源。",
    hotelOnly: "僅接受飯店資料，既有來源識別碼不得覆蓋其他服務。匯入不會自動核准飯店、訂房連結或品牌。",
    draft: "尚未儲存的飯店設定會在切換頁籤時保留。", total: "飯店總數", pending: "待審核", approved: "已核准", unavailable: "已停用",
    conflict: "飯店設定已由其他管理員更新。你的草稿仍保留，請重新載入最新設定後再編輯。", reload: "重新載入最新設定", discard: "放棄這份飯店設定草稿，並載入最新已儲存設定？",
    leave: "飯店設定尚未儲存，確定要離開此頁？",
    missingOptions: "尚無訂房連結", showAllHotels: "顯示全部飯店",
  },
  "zh-CN": {
    title: "酒店", intro: "集中管理酒店目录、各预订平台审核与酒店服务设置。",
    partnersTitle: "合作伙伴与品牌", partnersIntro: "品牌批准由酒店及其他旅游服务共用；酒店资料、预订链接仍需各自审核。",
    catalog: "酒店目录", review: "审核与平台", affiliates: "联盟链接", imports: "导入与覆盖率", settings: "酒店设置",
    products: "酒店资料", platforms: "预订平台", destinations: "目的地链接", import: "CSV 导入", coverage: "覆盖率", providers: "供应商设置",
    partners: "管理共用合作伙伴", other: "其他旅游服务", shared: "全站公开与城市开关在此仅供查看。修改酒店设置不会启用其他服务、城市或 Airalo 数据源。",
    hotelOnly: "仅接受酒店资料，现有来源标识不得覆盖其他服务。导入不会自动批准酒店、预订链接或品牌。",
    draft: "切换标签页时保留尚未保存的酒店设置。", total: "酒店总数", pending: "待审核", approved: "已批准", unavailable: "已停用",
    conflict: "酒店设置已由其他管理员更新。你的草稿仍保留，请重新加载最新设置后再编辑。", reload: "重新加载最新设置", discard: "放弃这份酒店设置草稿并加载最新已保存设置？",
    leave: "酒店设置尚未保存，确定离开此页？",
    missingOptions: "暂无预订链接", showAllHotels: "显示全部酒店",
  },
  ja: {
    title: "ホテル", intro: "ホテル一覧、予約サイトごとの審査、ホテルサービス設定を一か所で管理します。",
    partnersTitle: "提携先とブランド", partnersIntro: "ブランド承認はホテルと他の旅行サービスで共通です。ホテル情報と予約リンクは個別に審査します。",
    catalog: "ホテル一覧", review: "審査と予約サイト", affiliates: "アフィリエイト", imports: "取込とカバレッジ", settings: "ホテル設定",
    products: "ホテル情報", platforms: "予約サイト", destinations: "目的地リンク", import: "CSV 取込", coverage: "カバレッジ", providers: "プロバイダー設定",
    partners: "共通の提携先を管理", other: "他の旅行サービス", shared: "全体の公開設定と都市設定は参照のみです。ホテル設定を変更しても他のサービス、都市、Airalo は有効になりません。",
    hotelOnly: "ホテルの行のみ取り込めます。他サービスの識別子は上書きできません。取込ではホテル、予約リンク、ブランドを自動承認しません。",
    draft: "タブを切り替えても未保存のホテル設定は保持されます。", total: "ホテル数", pending: "審査待ち", approved: "承認済み", unavailable: "無効",
    conflict: "ホテル設定が他で更新されました。下書きは保持されています。最新の設定を読み込んでから再編集してください。", reload: "最新の設定を再読み込み", discard: "このホテル設定の下書きを破棄して最新の設定を読み込みますか？",
    leave: "ホテル設定に未保存の変更があります。このページを離れますか？",
    missingOptions: "予約リンク未登録", showAllHotels: "すべてのホテルを表示",
  },
  ko: {
    title: "호텔", intro: "호텔 목록, 예약 플랫폼별 검토와 호텔 서비스 설정을 한곳에서 관리합니다.",
    partnersTitle: "파트너 및 브랜드", partnersIntro: "브랜드 승인은 호텔 및 다른 여행 서비스가 공유합니다. 호텔 정보와 예약 링크는 각각 검토합니다.",
    catalog: "호텔 목록", review: "검토 및 플랫폼", affiliates: "제휴 링크", imports: "가져오기 및 범위", settings: "호텔 설정",
    products: "호텔 정보", platforms: "예약 플랫폼", destinations: "목적지 링크", import: "CSV 가져오기", coverage: "지원 범위", providers: "공급자 설정",
    partners: "공유 파트너 관리", other: "다른 여행 서비스", shared: "전체 공개 및 도시 설정은 여기서 읽기 전용입니다. 호텔 설정을 변경해도 다른 서비스, 도시 또는 Airalo는 활성화되지 않습니다.",
    hotelOnly: "호텔 행만 허용됩니다. 다른 서비스의 기존 식별자는 덮어쓸 수 없습니다. 가져오기로 호텔, 예약 링크 또는 브랜드가 자동 승인되지 않습니다.",
    draft: "탭을 전환해도 저장하지 않은 호텔 설정이 유지됩니다.", total: "호텔 수", pending: "검토 대기", approved: "승인됨", unavailable: "비활성",
    conflict: "다른 관리자가 호텔 설정을 변경했습니다. 초안은 유지됩니다. 최신 설정을 불러온 후 다시 편집하세요.", reload: "최신 설정 다시 불러오기", discard: "호텔 설정 초안을 버리고 최신 저장 설정을 불러올까요?",
    leave: "호텔 설정에 저장하지 않은 변경이 있습니다. 이 페이지를 나갈까요?",
    missingOptions: "등록된 예약 링크 없음", showAllHotels: "모든 호텔 보기",
  },
};
export function adminHotelsCopy(locale: string): Copy {
  return copies[locale as Locale] ?? en;
}
