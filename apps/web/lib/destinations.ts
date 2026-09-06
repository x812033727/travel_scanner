export type CountryKey = "JP" | "KR" | "TH" | "TW" | "SG" | "HK" | "VN";

/**
 * A destination as the workbench, the search page and the home page show it.
 *
 * The API (`GET /destinations`) is the source of truth and answers with the reader's
 * locale already applied. The list below is the offline copy the same surfaces fall
 * back to when the API cannot be reached; its display text lives in the
 * `search.catalog` messages, keyed by destination id, so all five locales sit in one
 * place. Areas stay in the destination's own script: they are place names.
 */
export type DestinationCity = {
  id: string;
  country: CountryKey;
  name: string;
  airport: string;
  summary: string;
  recommendedDays: { min: number; max: number };
  areas: string[];
  /** Descriptive codes; `SECONDARY_CITY_TAG` marks a second-tier city in the picker. */
  tags: string[];
  timezone: string;
  currency: string;
};

export type DestinationSeed = Omit<DestinationCity, "name" | "summary">;

/** A `search.catalog` translator: `useTranslations("search.catalog")` or its server twin. */
export type CatalogTranslator = {
  (key: string, values?: Record<string, string | number>): string;
  has?: (key: string) => boolean;
};

export const SECONDARY_CITY_TAG = "secondary";

export const countryKeys: CountryKey[] = ["JP", "KR", "TH", "TW", "SG", "HK", "VN"];

export const destinationSeeds: DestinationSeed[] = [
  { id: "tokyo", country: "JP", airport: "NRT", recommendedDays: { min: 4, max: 6 }, areas: ["新宿", "上野／淺草", "東京站／銀座", "澀谷"], tags: ["shopping", "culture", "family"], timezone: "Asia/Tokyo", currency: "JPY" },
  { id: "osaka-kyoto", country: "JP", airport: "KIX", recommendedDays: { min: 5, max: 7 }, areas: ["難波／心齋橋", "梅田", "京都站", "四條河原町"], tags: ["food", "culture", "shopping"], timezone: "Asia/Tokyo", currency: "JPY" },
  { id: "fukuoka", country: "JP", airport: "FUK", recommendedDays: { min: 3, max: 5 }, areas: ["博多站", "天神", "中洲", "大濠公園"], tags: ["food", "short_stay", "day_trips"], timezone: "Asia/Tokyo", currency: "JPY" },
  { id: "sapporo", country: "JP", airport: "CTS", recommendedDays: { min: 5, max: 7 }, areas: ["札幌站", "大通", "薄野", "中島公園"], tags: ["nature", "spa", "food"], timezone: "Asia/Tokyo", currency: "JPY" },
  { id: "okinawa", country: "JP", airport: "OKA", recommendedDays: { min: 4, max: 6 }, areas: ["國際通", "那霸新都心", "北谷", "恩納"], tags: ["beach", "family", "self_drive"], timezone: "Asia/Tokyo", currency: "JPY" },
  { id: "nagoya", country: "JP", airport: "NGO", recommendedDays: { min: 4, max: 6 }, areas: ["名古屋站", "榮", "伏見", "金山"], tags: ["family", "food", "day_trips"], timezone: "Asia/Tokyo", currency: "JPY" },
  { id: "seoul", country: "KR", airport: "ICN", recommendedDays: { min: 4, max: 6 }, areas: ["明洞", "弘大", "東大門", "江南"], tags: ["shopping", "food", "nightlife"], timezone: "Asia/Seoul", currency: "KRW" },
  { id: "busan", country: "KR", airport: "PUS", recommendedDays: { min: 4, max: 5 }, areas: ["西面", "南浦洞", "海雲台", "廣安里"], tags: ["beach", "food", "night_views"], timezone: "Asia/Seoul", currency: "KRW" },
  { id: "jeju", country: "KR", airport: "CJU", recommendedDays: { min: 4, max: 6 }, areas: ["濟州市", "涯月", "中文觀光區", "西歸浦"], tags: ["nature", "beach", "self_drive"], timezone: "Asia/Seoul", currency: "KRW" },
  { id: "bangkok", country: "TH", airport: "BKK", recommendedDays: { min: 4, max: 6 }, areas: ["暹羅", "Asok／素坤逸", "Silom", "河濱"], tags: ["food", "shopping", "spa"], timezone: "Asia/Bangkok", currency: "THB" },
  { id: "chiang-mai", country: "TH", airport: "CNX", recommendedDays: { min: 4, max: 6 }, areas: ["古城", "尼曼區", "湄平河畔", "夜市周邊"], tags: ["culture", "nature", "slow_travel"], timezone: "Asia/Bangkok", currency: "THB" },
  { id: "phuket", country: "TH", airport: "HKT", recommendedDays: { min: 5, max: 7 }, areas: ["普吉老城", "芭東", "卡塔", "卡隆"], tags: ["beach", "islands", "nightlife"], timezone: "Asia/Bangkok", currency: "THB" },
  { id: "krabi", country: "TH", airport: "KBV", recommendedDays: { min: 4, max: 6 }, areas: ["奧南", "喀比鎮", "萊雷", "克隆芒"], tags: ["beach", "nature", "slow_travel"], timezone: "Asia/Bangkok", currency: "THB" },
  { id: "taipei", country: "TW", airport: "TPE", recommendedDays: { min: 3, max: 5 }, areas: ["台北車站", "西門町", "信義區", "中山"], tags: ["food", "culture", "night_views"], timezone: "Asia/Taipei", currency: "TWD" },
  { id: "singapore", country: "SG", airport: "SIN", recommendedDays: { min: 4, max: 5 }, areas: ["濱海灣", "烏節路", "牛車水", "武吉士"], tags: ["family", "food", "culture"], timezone: "Asia/Singapore", currency: "SGD" },
  { id: "hong-kong", country: "HK", airport: "HKG", recommendedDays: { min: 3, max: 5 }, areas: ["中環／上環", "尖沙咀", "銅鑼灣", "旺角"], tags: ["food", "shopping", "night_views"], timezone: "Asia/Hong_Kong", currency: "HKD" },
  { id: "hanoi", country: "VN", airport: "HAN", recommendedDays: { min: 4, max: 5 }, areas: ["還劍湖", "老城區", "西湖", "巴亭"], tags: ["culture", "food", "slow_travel"], timezone: "Asia/Ho_Chi_Minh", currency: "VND" },
  { id: "ho-chi-minh-city", country: "VN", airport: "SGN", recommendedDays: { min: 4, max: 5 }, areas: ["第一郡", "第三郡", "濱城市場", "草田"], tags: ["food", "culture", "nightlife"], timezone: "Asia/Ho_Chi_Minh", currency: "VND" },
  { id: "da-nang", country: "VN", airport: "DAD", recommendedDays: { min: 4, max: 6 }, areas: ["美溪海灘", "漢江", "山茶半島", "會安古城"], tags: ["beach", "nature", "culture"], timezone: "Asia/Ho_Chi_Minh", currency: "VND" },
];

export const interestCodes = [
  "deep_travel",
  "food",
  "shopping",
  "culture",
  "nature",
  "family",
  "nightlife",
  "spa",
  "beach",
] as const;

export type InterestCode = (typeof interestCodes)[number];

// Shop types the planner can favour. They only mean anything alongside the
// "shopping" interest, which is why the form hides them until it is chosen.
export const shopThemeCodes = [
  "drugstore",
  "electronics",
  "department-store",
  "outlet",
  "souvenir",
  "vintage",
  "anime-hobby",
  "market-street",
] as const;

export type ShopThemeCode = (typeof shopThemeCodes)[number];

export function localizeDestination(seed: DestinationSeed, t: CatalogTranslator): DestinationCity {
  return { ...seed, name: t(`cities.${seed.id}.name`), summary: t(`cities.${seed.id}.summary`) };
}

export function localizeDestinations(t: CatalogTranslator): DestinationCity[] {
  return destinationSeeds.map((seed) => localizeDestination(seed, t));
}

export function citiesForCountry(country: CountryKey, t: CatalogTranslator): DestinationCity[] {
  return destinationSeeds.filter((seed) => seed.country === country).map((seed) => localizeDestination(seed, t));
}

export function destinationByAirport(airport: string | null | undefined, t: CatalogTranslator): DestinationCity | undefined {
  const seed = destinationSeeds.find((candidate) => candidate.airport === airport);
  return seed ? localizeDestination(seed, t) : undefined;
}

/** The interest's label in the reader's language; an unknown code is shown as is. */
export function interestLabel(code: string, t: CatalogTranslator): string {
  if (!(interestCodes as readonly string[]).includes(code)) return code;
  return t(`interests.${code}`);
}

/** The shop type's label; an unknown code is shown as is. */
export function shopThemeLabel(code: string, t: CatalogTranslator): string {
  if (!(shopThemeCodes as readonly string[]).includes(code)) return code;
  return t(`shopThemes.${code}`);
}
