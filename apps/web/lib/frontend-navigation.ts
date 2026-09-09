import type { SiteFeature } from "./site-features";

export const frontendDestinations: ReadonlyArray<{key: "explore" | "collections" | "trips" | "my"; href: string; feature?: SiteFeature}> = [
  { key: "explore", href: "/explore" },
  { key: "collections", href: "/explore/collections" },
  { key: "trips", href: "/trips", feature: "trips" as SiteFeature },
  { key: "my", href: "/my" },
] as const;

export function frontendActive(key: string, pathname: string) {
  const path = pathname.replace(/^\/(?:en|ja|ko|zh-TW|zh-CN)(?=\/|$)/, "") || "/";
  if (key === "collections") return path.startsWith("/explore/collections") || path.startsWith("/community/collections");
  if (key === "trips") return path === "/trips" || path.startsWith("/trips/");
  if (key === "my") return ["/my", "/account", "/login", "/register", "/alerts", "/search", "/flights", "/labs", "/pricing", "/community"].some((prefix) => path === prefix || path.startsWith(prefix + "/")) && !path.startsWith("/community/collections");
  return path === "/" || ["/explore", "/hotspots", "/foods", "/destinations"].some((prefix) => path === prefix || path.startsWith(prefix + "/")) && !path.startsWith("/explore/collections");
}

const en = {
  logout: "Sign out", deleteTrip: "Delete trip", uncertain: "The connection was interrupted and this item may already be in your trip. Check the trip before adding it again.",
  explore: "Explore", collections: "Saved", trips: "My trips", my: "My space",
  tools: "Travel tools", display: "Display & language", search: "Flights & stays", advanced: "More preferences", basics: "Where, when & who", searchTitle: "Find a trip that fits", searchHelp: "Start with the basics. Accommodation and interests are optional. Recommendations are estimates; check current prices in the next step.",
  continue: "Continue planning", more: "More options", plan: "Add to trip", hotel: "Set as main hotel", hotelWarning: "This replaces the main hotel and updates the hotel anchors for every day. It does not make a reservation.", mealWarning: "This replaces the restaurant for the selected meal. Review the day and meal before confirming.",
  chooseTrip: "Choose a trip", chooseMerchant: "Choose a restaurant", chooseDay: "Choose a day", day: "Day", destinationMatch: "Same destination", otherTrips: "Other trips", unavailable: "This item cannot be added yet. You can still save it.", noMerchant: "No verified restaurant is available for this dish yet. Save it and choose a restaurant later.",
  confirm: "Confirm and add", confirmHotel: "Confirm main hotel", added: "Added to your trip", openTrip: "Open trip", create: "Create a trip", empty: "Create a trip, then return here to confirm this item.", loading: "Loading…", retry: "Try again", cancel: "Cancel", login: "Sign in to continue", error: "Could not complete this action. Please try again.", conflict: "This trip has changed. Reload its latest version and confirm again.", selected: "Selected item", lunch: "Lunch", dinner: "Dinner", meal: "Meal", noTrips: "No trips yet", query: "Find travel options", account: "Account settings",
};
type Copy = typeof en;
const copies: Record<string, Copy> = {
  en,
  "zh-TW": {
    logout: "登出", deleteTrip: "刪除旅程", uncertain: "連線中斷，這筆內容可能已加入。請先開啟旅程確認，不會在這裡再次送出。",
    explore: "探索", collections: "收藏", trips: "我的旅程", my: "我的", tools: "旅行工具", display: "外觀與語言", search: "機票與住宿", advanced: "更多偏好條件", basics: "去哪裡、什麼時候、和誰", searchTitle: "找到適合你的旅行", searchHelp: "先選基本條件，住宿與興趣可以晚點決定。推薦費用是估算，下一步再查目前報價。", continue: "繼續規劃", more: "更多操作", plan: "加入旅程", hotel: "設為主要飯店", hotelWarning: "這會替換主要飯店，並同步每一天的飯店起訖卡；不代表完成訂房。", mealWarning: "這會更換所選餐次的餐廳，請確認日期與午餐／晚餐。", chooseTrip: "選擇旅程", chooseMerchant: "選擇實際用餐店家", chooseDay: "選擇日期", day: "第幾天", destinationMatch: "相同目的地", otherTrips: "其他旅程", unavailable: "這筆內容暫時無法加入旅程，仍可先收藏。", noMerchant: "這道料理目前沒有可安排的已驗證店家，可以先收藏，之後再選餐廳。", confirm: "確認加入", confirmHotel: "確認更換主要飯店", added: "已加入旅程", openTrip: "開啟旅程", create: "建立旅程", empty: "先建立旅程，完成後會回到這裡確認加入的內容。", loading: "載入中…", retry: "重新載入", cancel: "取消", login: "登入後繼續", error: "操作未完成，請再試一次。", conflict: "旅程已被更新，請載入最新內容後重新確認。", selected: "準備加入的內容", lunch: "午餐", dinner: "晚餐", meal: "餐次", noTrips: "還沒有旅程", query: "尋找旅行方案", account: "帳號設定",
  },
  "zh-CN": {
    logout: "退出登录", deleteTrip: "删除旅程", uncertain: "连接中断，这条内容可能已加入。请先打开旅程确认，不会在这里再次提交。",
    explore: "探索", collections: "收藏", trips: "我的旅程", my: "我的", tools: "旅行工具", display: "外观与语言", search: "机票与住宿", advanced: "更多偏好条件", basics: "去哪里、什么时候、和谁", searchTitle: "找到适合你的旅行", searchHelp: "先选基本条件，住宿与兴趣可以稍后决定。推荐费用是估算，下一步再查当前报价。", continue: "继续规划", more: "更多操作", plan: "加入旅程", hotel: "设为主要酒店", hotelWarning: "这会替换主要酒店，并同步每天的酒店起讫卡；不代表完成预订。", mealWarning: "这会更换所选餐次的餐厅，请确认日期与午餐／晚餐。", chooseTrip: "选择旅程", chooseMerchant: "选择实际用餐店家", chooseDay: "选择日期", day: "第几天", destinationMatch: "相同目的地", otherTrips: "其他旅程", unavailable: "这条内容暂时无法加入旅程，仍可先收藏。", noMerchant: "这道菜目前没有可安排的已验证店家，可以先收藏，之后再选餐厅。", confirm: "确认加入", confirmHotel: "确认更换主要酒店", added: "已加入旅程", openTrip: "打开旅程", create: "创建旅程", empty: "先创建旅程，完成后会回到这里确认加入的内容。", loading: "加载中…", retry: "重新加载", cancel: "取消", login: "登录后继续", error: "操作未完成，请再试一次。", conflict: "旅程已被更新，请加载最新内容后重新确认。", selected: "准备加入的内容", lunch: "午餐", dinner: "晚餐", meal: "餐次", noTrips: "还没有旅程", query: "寻找旅行方案", account: "账号设置",
  },
  ja: {
    logout: "ログアウト", deleteTrip: "旅行を削除", uncertain: "通信が中断しました。すでに追加されている可能性があるため、再追加する前に旅行をご確認ください。",
    explore: "見つける", collections: "保存", trips: "マイ旅行", my: "マイページ", tools: "旅行ツール", display: "表示と言語", search: "航空券と宿泊", advanced: "その他の希望条件", basics: "行き先・日程・人数", searchTitle: "あなたに合う旅を探す", searchHelp: "まず基本条件から。宿泊や興味は後から選べます。おすすめの費用は概算です。次の手順で現在の料金を確認できます。", continue: "計画を続ける", more: "その他の操作", plan: "旅行に追加", hotel: "メインホテルに設定", hotelWarning: "メインホテルを変更し、毎日の出発・到着ホテルを更新します。予約は行いません。", mealWarning: "選択した食事のレストランを変更します。日付と昼食・夕食をご確認ください。", chooseTrip: "旅行を選択", chooseMerchant: "レストランを選択", chooseDay: "日付を選択", day: "日目", destinationMatch: "同じ目的地", otherTrips: "その他の旅行", unavailable: "この情報はまだ旅行に追加できません。保存は可能です。", noMerchant: "この料理には手配可能な確認済み店舗がありません。保存して後で選べます。", confirm: "確認して追加", confirmHotel: "ホテル変更を確認", added: "旅行に追加しました", openTrip: "旅行を開く", create: "旅行を作成", empty: "旅行を作成すると、この画面に戻って追加内容を確認できます。", loading: "読み込み中…", retry: "再試行", cancel: "キャンセル", login: "ログインして続ける", error: "操作を完了できませんでした。もう一度お試しください。", conflict: "旅行が更新されています。最新情報を読み込み、再度確認してください。", selected: "追加する内容", lunch: "昼食", dinner: "夕食", meal: "食事", noTrips: "旅行がありません", query: "旅行プランを探す", account: "アカウント設定",
  },
  ko: {
    logout: "로그아웃", deleteTrip: "여행 삭제", uncertain: "연결이 끊겼습니다. 이미 추가되었을 수 있으므로 다시 추가하기 전에 여행을 확인하세요.",
    explore: "둘러보기", collections: "저장", trips: "내 여행", my: "마이", tools: "여행 도구", display: "화면 및 언어", search: "항공편 및 숙소", advanced: "추가 선호 조건", basics: "목적지·날짜·인원", searchTitle: "나에게 맞는 여행 찾기", searchHelp: "기본 조건부터 선택하세요. 숙소와 관심사는 나중에 정할 수 있습니다. 추천 비용은 예상 금액이며 다음 단계에서 현재 가격을 확인합니다.", continue: "계속 계획하기", more: "더 보기", plan: "여행에 추가", hotel: "주요 호텔로 설정", hotelWarning: "주요 호텔을 변경하고 매일 출발·도착 호텔을 업데이트합니다. 예약이 완료되는 것은 아닙니다.", mealWarning: "선택한 식사의 식당을 변경합니다. 날짜와 점심·저녁을 확인하세요.", chooseTrip: "여행 선택", chooseMerchant: "실제 방문할 식당 선택", chooseDay: "날짜 선택", day: "일차", destinationMatch: "같은 목적지", otherTrips: "다른 여행", unavailable: "아직 여행에 추가할 수 없는 항목입니다. 저장은 가능합니다.", noMerchant: "이 요리에는 아직 추가 가능한 검증된 식당이 없습니다. 저장한 후 나중에 식당을 선택하세요.", confirm: "확인 후 추가", confirmHotel: "주요 호텔 변경 확인", added: "여행에 추가했어요", openTrip: "여행 열기", create: "여행 만들기", empty: "여행을 만들면 이 화면으로 돌아와 추가할 내용을 확인합니다.", loading: "불러오는 중…", retry: "다시 시도", cancel: "취소", login: "로그인 후 계속", error: "작업을 완료하지 못했습니다. 다시 시도하세요.", conflict: "여행이 변경되었습니다. 최신 정보를 불러온 후 다시 확인하세요.", selected: "추가할 항목", lunch: "점심", dinner: "저녁", meal: "식사", noTrips: "아직 여행이 없어요", query: "여행 옵션 찾기", account: "계정 설정",
  },
};
export function frontendCopy(locale: string): Copy { return copies[locale] || en; }
