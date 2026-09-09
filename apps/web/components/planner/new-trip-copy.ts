const copy = {
  "zh-TW": {
    title: "先選一座城市，開始你的旅行", subtitle: "只要城市與日期，就能開啟空白行程。",
    cityHelp: "從城市清單挑選，或直接輸入；不會自動搜尋地圖。", datePrompt: "選擇旅行日期", editDates: "調整日期", closeCalendar: "收起日曆",
    advanced: "進階偏好（選填）", nameHelp: "依城市與天數自動命名，也可以自行修改。", autoName: "使用自動名稱",
    submit: "開始安排", creating: "正在建立…", notice: "先建立可編輯的空白行程；不會自動呼叫 AI 或計算路線。",
    travelersHelp: "預設 2 位成人、0 位兒童、1 間房，隨時可修改。", invalidTravelers: "請確認成人、兒童與房間數在可選範圍內。", invalidNumbers: "請檢查偏好數值，不能低於欄位允許的範圍。",
  },
  "zh-CN": {
    title: "先选一座城市，开始你的旅行", subtitle: "只需城市与日期，就能开启空白行程。",
    cityHelp: "从城市列表选择，或直接输入；不会自动搜索地图。", datePrompt: "选择旅行日期", editDates: "调整日期", closeCalendar: "收起日历",
    advanced: "高级偏好（选填）", nameHelp: "按城市与天数自动命名，也可以自行修改。", autoName: "使用自动名称",
    submit: "开始安排", creating: "正在创建…", notice: "先创建可编辑的空白行程；不会自动调用 AI 或计算路线。",
    travelersHelp: "默认 2 位成人、0 位儿童、1 间房，随时可修改。", invalidTravelers: "请确认成人、儿童与房间数在可选范围内。", invalidNumbers: "请检查偏好数值，不能低于字段允许的范围。",
  },
  en: {
    title: "Pick a city. Make it your trip.", subtitle: "A city and dates are all you need to open a blank itinerary.",
    cityHelp: "Choose a city from the list, or type one. No map search runs automatically.", datePrompt: "Choose travel dates", editDates: "Edit dates", closeCalendar: "Close calendar",
    advanced: "More preferences (optional)", nameHelp: "Named from your city and dates. Make it your own whenever you like.", autoName: "Use automatic name",
    submit: "Start planning", creating: "Creating…", notice: "Start with an editable blank itinerary. No AI generation or route calculation runs automatically.",
    travelersHelp: "Starts with 2 adults, 0 children and 1 room. You can change these now.", invalidTravelers: "Choose valid numbers of adults, children and rooms.", invalidNumbers: "Check the preference values; they cannot be below the allowed limits.",
  },
  ja: {
    title: "行きたい街から、旅をはじめよう", subtitle: "都市と日付だけで、空白の旅程を作成できます。",
    cityHelp: "一覧から都市を選ぶか、直接入力してください。地図検索は自動実行されません。", datePrompt: "旅行の日付を選ぶ", editDates: "日付を変更", closeCalendar: "カレンダーを閉じる",
    advanced: "詳しい希望（任意）", nameHelp: "都市と日数から自動で名前を付けます。自由に変更できます。", autoName: "自動の名前を使う",
    submit: "旅の計画をはじめる", creating: "作成中…", notice: "編集できる空白の旅程を作成します。AI 生成や経路計算は自動実行されません。",
    travelersHelp: "初期設定は大人 2 人、子ども 0 人、1 室です。変更できます。", invalidTravelers: "大人、子ども、部屋の数を選択可能な範囲で設定してください。", invalidNumbers: "希望条件の数値が指定範囲を下回っていないか確認してください。",
  },
  ko: {
    title: "도시를 고르고, 나만의 여행을 시작하세요", subtitle: "도시와 날짜만 있으면 빈 일정을 만들 수 있어요.",
    cityHelp: "목록에서 도시를 고르거나 직접 입력하세요. 지도 검색은 자동으로 실행되지 않습니다.", datePrompt: "여행 날짜 선택", editDates: "날짜 변경", closeCalendar: "달력 닫기",
    advanced: "상세 선호 사항 (선택)", nameHelp: "도시와 일수로 이름을 정해 드려요. 자유롭게 바꿀 수 있습니다.", autoName: "자동 이름 사용",
    submit: "일정 시작하기", creating: "만드는 중…", notice: "수정할 수 있는 빈 일정을 만듭니다. AI 생성이나 경로 계산은 자동으로 실행되지 않습니다.",
    travelersHelp: "성인 2명, 어린이 0명, 객실 1개로 시작하며 지금 변경할 수 있습니다.", invalidTravelers: "성인, 어린이와 객실 수를 선택 가능한 범위로 설정하세요.", invalidNumbers: "선호 사항의 숫자가 허용된 최솟값보다 작은지 확인하세요.",
  },
} as const;

export function newTripCopy(locale: string) {
  return copy[locale as keyof typeof copy] ?? copy.en;
}

export function automaticTripName(locale: string, city: string, days: number) {
  if (!city) return "";
  if (locale === "ja") return days ? `${city}・${days}日間` : `${city}の旅`;
  if (locale === "ko") return days ? `${city} ${days}일 여행` : `${city} 여행`;
  if (locale === "zh-TW" || locale === "zh-CN") return days ? `${city}・${days} 天` : `${city}旅行`;
  return days ? `${city} · ${days}-day trip` : `${city} trip`;
}
