import type { Locale } from "@/i18n/routing";

const en = {
  channel: "Affiliate channel", travelpayouts: "Travelpayouts", klook: "Klook direct affiliate",
  independent: "Approval, evidence and activation are managed separately for each channel. Existing approvals are not transferred.",
  noApi: "Affiliate booking links do not grant access to prices or availability. Confirm final prices and booking conditions on Klook; no pricing API is used here.",
  evidence: "Approval evidence for this channel", evidenceHint: "Provide the approval evidence from the selected partner account. Saving an approval does not approve individual product links.",
  configure: "Configure Klook affiliate account", affiliateId: "Klook Affiliate ID",
  networkMissing: "Travelpayouts is not configured. This does not prevent independently approved direct affiliate links or ordinary hotel links.",
  discover: "Continue exploring this destination", discoveryHint: "Reviewed destination links, not individual products. Choose dates and check prices and availability on the external platform.",
  exact: "Reviewed products", tour: "Day trips and experiences", duration: "Duration (minutes)",
  browserVerified: "I verified this exact product or destination in the browser", browserEvidence: "Verified Klook page URL", browserHint: "Use only after personally opening this page and checking its identity. This records your review and does not bypass URL or account safety checks.",
};
type Copy = { [K in keyof typeof en]: string };
const copies: Record<Locale, Copy> = {
  en,
  "zh-TW": {
    channel: "分潤管道", travelpayouts: "Travelpayouts", klook: "Klook 直接分潤",
    independent: "各管道的核准、證明與啟用狀態分開管理，不會沿用另一管道的核准。",
    noApi: "分潤連結不代表已取得房價或供應量權限。最終價格與預訂條件請至 Klook 確認；此處不使用報價 API。",
    evidence: "此管道的核准證明", evidenceHint: "請提供所選合作帳號的核准證明。儲存品牌核准不會自動核准各商品連結。",
    configure: "設定 Klook 分潤帳號", affiliateId: "Klook Affiliate ID",
    networkMissing: "尚未設定 Travelpayouts；不影響各自完成核准的直接分潤連結或一般飯店連結。",
    discover: "繼續探索這個目的地", discoveryHint: "以下是已審核的目的地入口，不是特定商品。日期、價格與供應狀況請至外部平台確認。",
    exact: "已審核商品", tour: "一日遊與體驗", duration: "時長（分鐘）",
    browserVerified: "我已在瀏覽器核對這個商品或目的地", browserEvidence: "已核對的 Klook 頁面網址", browserHint: "僅在親自開啟頁面並確認身分後勾選。系統會記錄你的審核，不會略過網址或帳號安全檢查。",
  },
  "zh-CN": {
    channel: "分佣渠道", travelpayouts: "Travelpayouts", klook: "Klook 直接分佣",
    independent: "各渠道的批准、证明与启用状态分别管理，不会沿用另一渠道的批准。",
    noApi: "分佣链接不代表已获得房价或供应量权限。最终价格与预订条件请到 Klook 确认；此处不使用报价 API。",
    evidence: "此渠道的批准证明", evidenceHint: "请提供所选合作账号的批准证明。保存品牌批准不会自动批准各商品链接。",
    configure: "设置 Klook 分佣账号", affiliateId: "Klook Affiliate ID",
    networkMissing: "尚未设置 Travelpayouts；不影响各自完成批准的直接分佣链接或普通酒店链接。",
    discover: "继续探索这个目的地", discoveryHint: "以下是已审核的目的地入口，不是特定商品。日期、价格与供应情况请到外部平台确认。",
    exact: "已审核商品", tour: "一日游与体验", duration: "时长（分钟）",
    browserVerified: "我已在浏览器核对这个商品或目的地", browserEvidence: "已核对的 Klook 页面网址", browserHint: "仅在亲自打开页面并确认身份后勾选。系统会记录你的审核，不会跳过网址或账号安全检查。",
  },
  ja: {
    channel: "提携経路", travelpayouts: "Travelpayouts", klook: "Klook 直接提携",
    independent: "承認、証拠、有効化は経路ごとに管理します。他の経路の承認は引き継ぎません。",
    noApi: "提携リンクの承認に料金・空き状況 API の権限は含まれません。最終料金と予約条件は Klook で確認してください。ここでは料金 API を使用しません。",
    evidence: "この経路の承認証拠", evidenceHint: "選択した提携アカウントの承認証拠を入力してください。ブランド承認で個別商品リンクが自動承認されることはありません。",
    configure: "Klook 提携アカウントを設定", affiliateId: "Klook Affiliate ID",
    networkMissing: "Travelpayouts は未設定です。独立して承認された直接提携リンクや通常のホテルリンクは利用できます。",
    discover: "この目的地をさらに探す", discoveryHint: "審査済みの目的地リンクであり、特定商品ではありません。日付、料金、空き状況は外部サイトで確認してください。",
    exact: "審査済み商品", tour: "日帰りツアーと体験", duration: "所要時間（分）",
    browserVerified: "ブラウザーでこの商品または目的地を確認しました", browserEvidence: "確認済みの Klook ページ URL", browserHint: "実際にページを開き、対象を確認した場合のみ選択してください。審査者を記録し、URL やアカウントの安全性検証は省略しません。",
  },
  ko: {
    channel: "제휴 경로", travelpayouts: "Travelpayouts", klook: "Klook 직접 제휴",
    independent: "승인, 증빙 및 활성화는 경로별로 관리하며 다른 경로의 승인을 이전하지 않습니다.",
    noApi: "제휴 링크는 가격이나 예약 가능 여부 API 권한을 부여하지 않습니다. 최종 가격과 예약 조건은 Klook에서 확인하세요. 여기서는 가격 API를 사용하지 않습니다.",
    evidence: "이 경로의 승인 증빙", evidenceHint: "선택한 제휴 계정의 승인 증빙을 입력하세요. 브랜드 승인은 개별 상품 링크를 자동 승인하지 않습니다.",
    configure: "Klook 제휴 계정 설정", affiliateId: "Klook Affiliate ID",
    networkMissing: "Travelpayouts가 설정되지 않았습니다. 별도로 승인된 직접 제휴 링크와 일반 호텔 링크에는 영향을 주지 않습니다.",
    discover: "이 여행지 더 살펴보기", discoveryHint: "검토된 여행지 링크이며 특정 상품이 아닙니다. 날짜, 가격 및 예약 가능 여부는 외부 플랫폼에서 확인하세요.",
    exact: "검토된 상품", tour: "당일 투어와 체험", duration: "소요 시간(분)",
    browserVerified: "브라우저에서 이 상품 또는 여행지를 확인했습니다", browserEvidence: "확인한 Klook 페이지 URL", browserHint: "직접 페이지를 열어 해당 상품이나 여행지가 맞는지 확인한 후에만 선택하세요. 검토자를 기록하며 URL 및 계정 안전 검사를 우회하지 않습니다.",
  },
};
export function klookAffiliateCopy(locale: string): Copy {
  return copies[locale as Locale] || copies.en;
}
