/**
 * Section copy for the destination index and the city guides.
 *
 * A locale-keyed module rather than a new `messages/` namespace, following
 * lib/stay22-script-copy.ts and lib/discovery-copy.ts. Adding a namespace would mean editing the
 * allowlists that tools/check-i18n.mjs cross-checks -- lib/ui-text.ts and, on the other side of
 * the repository, apps/api/app/ui_text/schemas.py -- which is a lot of blast radius for section
 * headings. Only the two page-title keys live in messages/metadata.json, because
 * app/[locale]/metadata.test.ts reads them from there.
 */
const en = {
  indexTitle: "Destinations",
  indexIntro:
    "Guides to the cities Mokaair covers: how long to stay, which areas to base yourself in, and what other travellers look up most.",
  guideEyebrow: "Destination guide",
  factsDays: "Suggested stay",
  daysUnit: "days",
  factsTimezone: "Time zone",
  factsCurrency: "Currency",
  areasTitle: "Where to stay",
  seeTitle: "What to see",
  eatTitle: "Where to eat",
  planTitle: "Plan this trip",
  nearbyTitle: "Nearby",
  browsePlaces: "Browse every reviewed place",
  browseFood: "Open the food guide",
  planTrip: "Compare flights and stays",
  stays: "Hotels for this destination",
  emptyPlaces: "Reviewed places for this destination are not listed yet.",
  emptyFood: "Reviewed merchants for this destination are not listed yet.",
  partOf: "Part of",
  extensions: "Extended destinations",
  breadcrumb: "Destinations",
};

type Copy = Record<keyof typeof en, string>;

const copies: Record<string, Copy> = {
  en,
  "zh-TW": {
    indexTitle: "目的地",
    indexIntro: "Mokaair 收錄城市的旅行指南：建議待幾天、住哪一區比較順、以及其他旅人最常查的地方。",
    guideEyebrow: "目的地指南",
    factsDays: "建議天數",
    daysUnit: "天",
    factsTimezone: "時區",
    factsCurrency: "貨幣",
    areasTitle: "住哪一區",
    seeTitle: "看什麼",
    eatTitle: "吃什麼",
    planTitle: "規劃這趟行程",
    nearbyTitle: "鄰近目的地",
    browsePlaces: "瀏覽所有已審核景點",
    browseFood: "打開美食指南",
    planTrip: "比較機票與住宿",
    stays: "這個目的地的住宿",
    emptyPlaces: "這個目的地還沒有已審核的景點。",
    emptyFood: "這個目的地還沒有已審核的店家。",
    partOf: "屬於",
    extensions: "延伸目的地",
    breadcrumb: "目的地",
  },
  "zh-CN": {
    indexTitle: "目的地",
    indexIntro: "Mokaair 收录城市的旅行指南：建议待几天、住哪一区比较顺，以及其他旅人最常查的地方。",
    guideEyebrow: "目的地指南",
    factsDays: "建议天数",
    daysUnit: "天",
    factsTimezone: "时区",
    factsCurrency: "货币",
    areasTitle: "住哪一区",
    seeTitle: "看什么",
    eatTitle: "吃什么",
    planTitle: "规划这趟行程",
    nearbyTitle: "邻近目的地",
    browsePlaces: "浏览所有已审核景点",
    browseFood: "打开美食指南",
    planTrip: "比较机票与住宿",
    stays: "这个目的地的住宿",
    emptyPlaces: "这个目的地还没有已审核的景点。",
    emptyFood: "这个目的地还没有已审核的商家。",
    partOf: "属于",
    extensions: "延伸目的地",
    breadcrumb: "目的地",
  },
  ja: {
    indexTitle: "旅行先",
    indexIntro:
      "Mokaair が扱う都市のガイドです。滞在日数の目安、拠点にしやすいエリア、他の旅行者がよく調べている場所をまとめています。",
    guideEyebrow: "旅行先ガイド",
    factsDays: "滞在日数の目安",
    daysUnit: "日",
    factsTimezone: "タイムゾーン",
    factsCurrency: "通貨",
    areasTitle: "どのエリアに泊まるか",
    seeTitle: "見どころ",
    eatTitle: "食べる",
    planTitle: "この旅程を組む",
    nearbyTitle: "近隣の旅行先",
    browsePlaces: "確認済みのスポットをすべて見る",
    browseFood: "グルメガイドを開く",
    planTrip: "航空券と宿を比較する",
    stays: "この旅行先の宿",
    emptyPlaces: "この旅行先の確認済みスポットはまだありません。",
    emptyFood: "この旅行先の確認済み店舗はまだありません。",
    partOf: "所属",
    extensions: "拡張エリア",
    breadcrumb: "旅行先",
  },
  ko: {
    indexTitle: "여행지",
    indexIntro:
      "Mokaair가 다루는 도시 가이드입니다. 며칠이 적당한지, 어느 지역에 묵는 게 편한지, 다른 여행자들이 가장 많이 찾아보는 곳을 정리했습니다.",
    guideEyebrow: "여행지 가이드",
    factsDays: "권장 일수",
    daysUnit: "일",
    factsTimezone: "시간대",
    factsCurrency: "통화",
    areasTitle: "어느 지역에 묵을까",
    seeTitle: "무엇을 볼까",
    eatTitle: "무엇을 먹을까",
    planTitle: "이 여행 계획하기",
    nearbyTitle: "가까운 여행지",
    browsePlaces: "검증된 장소 전체 보기",
    browseFood: "맛집 가이드 열기",
    planTrip: "항공권과 숙소 비교하기",
    stays: "이 여행지의 숙소",
    emptyPlaces: "이 여행지의 검증된 장소가 아직 없습니다.",
    emptyFood: "이 여행지의 검증된 매장이 아직 없습니다.",
    partOf: "소속",
    extensions: "확장 여행지",
    breadcrumb: "여행지",
  },
};

export function destinationsCopy(locale: string): Copy {
  return copies[locale] ?? en;
}
