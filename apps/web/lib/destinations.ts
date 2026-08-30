export type CountryKey = "JP" | "KR" | "TH";

export type DestinationCity = {
  id: string;
  country: CountryKey;
  name: string;
  airport: string;
  airportName: string;
  summary: string;
  recommendedStay: string;
  areas: string[];
  tags: string[];
  timezone: string;
  currency: string;
};

export const countries = [
  { key: "JP" as const, label: "日本", caption: "城市、文化與四季自然" },
  { key: "KR" as const, label: "韓國", caption: "美食、購物與海岸城市" },
  { key: "TH" as const, label: "泰國", caption: "度假、夜市與療癒慢旅" },
];

export const destinations: DestinationCity[] = [
  { id: "tokyo", country: "JP", name: "東京", airport: "NRT", airportName: "成田／羽田", summary: "交通選擇最完整，適合第一次自由行", recommendedStay: "4–6 天", areas: ["新宿", "上野／淺草", "東京站／銀座", "澀谷"], tags: ["購物", "文化", "親子"], timezone: "Asia/Tokyo", currency: "JPY" },
  { id: "osaka-kyoto", country: "JP", name: "大阪／京都", airport: "KIX", airportName: "關西國際機場", summary: "一次搭配大阪美食與京都文化", recommendedStay: "5–7 天", areas: ["難波／心齋橋", "梅田", "京都站", "四條河原町"], tags: ["美食", "文化", "購物"], timezone: "Asia/Tokyo", currency: "JPY" },
  { id: "fukuoka", country: "JP", name: "福岡", airport: "FUK", airportName: "福岡機場", summary: "機場近市區，三至五日也能從容玩", recommendedStay: "3–5 天", areas: ["博多站", "天神", "中洲", "大濠公園"], tags: ["美食", "短天數", "近郊"], timezone: "Asia/Tokyo", currency: "JPY" },
  { id: "sapporo", country: "JP", name: "札幌", airport: "CTS", airportName: "新千歲機場", summary: "四季自然、溫泉與北海道美食", recommendedStay: "5–7 天", areas: ["札幌站", "大通", "薄野", "中島公園"], tags: ["自然", "溫泉", "美食"], timezone: "Asia/Tokyo", currency: "JPY" },
  { id: "okinawa", country: "JP", name: "沖繩", airport: "OKA", airportName: "那霸機場", summary: "海島與親子自駕的放慢旅程", recommendedStay: "4–6 天", areas: ["國際通", "那霸新都心", "北谷", "恩納"], tags: ["海灘", "親子", "自駕"], timezone: "Asia/Tokyo", currency: "JPY" },
  { id: "nagoya", country: "JP", name: "名古屋", airport: "NGO", airportName: "中部國際機場", summary: "串聯中部城市、主題樂園與美食", recommendedStay: "4–6 天", areas: ["名古屋站", "榮", "伏見", "金山"], tags: ["親子", "美食", "近郊"], timezone: "Asia/Tokyo", currency: "JPY" },
  { id: "seoul", country: "KR", name: "首爾", airport: "ICN", airportName: "仁川／金浦", summary: "購物、美食與展覽密度高", recommendedStay: "4–6 天", areas: ["明洞", "弘大", "東大門", "江南"], tags: ["購物", "美食", "夜生活"], timezone: "Asia/Seoul", currency: "KRW" },
  { id: "busan", country: "KR", name: "釜山", airport: "PUS", airportName: "金海國際機場", summary: "海景、市場與城市慢遊", recommendedStay: "4–5 天", areas: ["西面", "南浦洞", "海雲台", "廣安里"], tags: ["海灘", "美食", "夜景"], timezone: "Asia/Seoul", currency: "KRW" },
  { id: "jeju", country: "KR", name: "濟州", airport: "CJU", airportName: "濟州國際機場", summary: "海岸、咖啡與自然步道", recommendedStay: "4–6 天", areas: ["濟州市", "涯月", "中文觀光區", "西歸浦"], tags: ["自然", "海灘", "自駕"], timezone: "Asia/Seoul", currency: "KRW" },
  { id: "bangkok", country: "TH", name: "曼谷", airport: "BKK", airportName: "蘇凡納布／廊曼", summary: "美食、購物、寺廟與按摩一次滿足", recommendedStay: "4–6 天", areas: ["暹羅", "Asok／素坤逸", "Silom", "河濱"], tags: ["美食", "購物", "SPA"], timezone: "Asia/Bangkok", currency: "THB" },
  { id: "chiang-mai", country: "TH", name: "清邁", airport: "CNX", airportName: "清邁國際機場", summary: "古城、咖啡、手作與近郊自然", recommendedStay: "4–6 天", areas: ["古城", "尼曼區", "湄平河畔", "夜市周邊"], tags: ["文化", "自然", "慢旅"], timezone: "Asia/Bangkok", currency: "THB" },
  { id: "phuket", country: "TH", name: "普吉", airport: "HKT", airportName: "普吉國際機場", summary: "海灘、跳島、度假村與夜生活", recommendedStay: "5–7 天", areas: ["普吉老城", "芭東", "卡塔", "卡隆"], tags: ["海灘", "跳島", "夜生活"], timezone: "Asia/Bangkok", currency: "THB" },
  { id: "krabi", country: "TH", name: "喀比", airport: "KBV", airportName: "喀比國際機場", summary: "島嶼、石灰岩海岸與悠閒度假", recommendedStay: "4–6 天", areas: ["奧南", "喀比鎮", "萊雷", "克隆芒"], tags: ["海灘", "自然", "慢旅"], timezone: "Asia/Bangkok", currency: "THB" },
];

export const interests = [
  { code: "food", label: "美食" },
  { code: "shopping", label: "購物" },
  { code: "culture", label: "文化" },
  { code: "nature", label: "自然" },
  { code: "family", label: "親子" },
  { code: "nightlife", label: "夜生活" },
  { code: "spa", label: "溫泉／SPA" },
  { code: "beach", label: "海灘／跳島" },
];

export function citiesForCountry(country: CountryKey) {
  return destinations.filter((destination) => destination.country === country);
}

export function destinationByAirport(airport?: string | null) {
  return destinations.find((destination) => destination.airport === airport);
}

export function interestLabel(code: string) {
  return interests.find((interest) => interest.code === code)?.label || code;
}
