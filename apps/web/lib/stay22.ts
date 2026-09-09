/** External browsing only: never use widget content as an itinerary/quote API. */
export type Stay22MapContext = {
  destination_id: string;
  country_code: string;
  city_code: string;
  check_in?: string | null;
  check_out?: string | null;
  travelers?: { adults: number; children: number; rooms: number } | null;
  currency?: string;
};

const PILOTS = {
  tokyo: { country: "JP", city: "NRT", timezone: "Asia/Tokyo", bounds: [35.2, 36.0, 138.8, 140.1] },
  taipei: { country: "TW", city: "TPE", timezone: "Asia/Taipei", bounds: [24.8, 25.3, 121.3, 121.9] },
} as const;

function validDate(value: string | null | undefined): value is string {
  if (!value || !/^\d{4}-\d{2}-\d{2}$/.test(value)) return false;
  const parsed = new Date(`${value}T00:00:00Z`);
  return Number.isFinite(parsed.getTime()) && parsed.toISOString().slice(0, 10) === value;
}

function cityToday(now: Date, timeZone: string) {
  const parts = new Intl.DateTimeFormat("en", { timeZone, year: "numeric", month: "2-digit", day: "2-digit" }).formatToParts(now);
  return ["year", "month", "day"].map((type) => parts.find((part) => part.type === type)?.value).join("-");
}

export function buildStay22Map(
  context: Stay22MapContext | null | undefined,
  area: { latitude: number; longitude: number } | null | undefined,
  now = new Date(),
) {
  if (!context || !area || !Object.hasOwn(PILOTS, context.destination_id)) return null;
  const pilot = PILOTS[context.destination_id as keyof typeof PILOTS];
  if (context.country_code !== pilot.country || context.city_code !== pilot.city) return null;
  const { latitude, longitude } = area;
  const [south, north, west, east] = pilot.bounds;
  if (!Number.isFinite(latitude) || !Number.isFinite(longitude) || latitude < south || latitude > north || longitude < west || longitude > east) return null;
  const datesProvided = Number.isFinite(now.getTime()) && validDate(context.check_in) && validDate(context.check_out)
    && context.check_out > context.check_in && context.check_in >= cityToday(now, pilot.timezone);
  const party = context.travelers;
  const guestsProvided = Boolean(party && Number.isInteger(party.adults) && party.adults >= 1 && party.adults <= 9
    && Number.isInteger(party.children) && party.children >= 0 && party.children <= 9
    && Number.isInteger(party.rooms) && party.rooms >= 1 && party.rooms <= 4);
  // Explicit allowlist, not a spread of the trip/context. Never send private titles, IDs or POIs.
  const params = new URLSearchParams({
    aid: "mokaair", lat: latitude.toFixed(5), lng: longitude.toFixed(5),
    campaign: `mokaair_stays_${context.destination_id}`, currency: "TWD",
    showhotels: "true", priceper: "nightly", unitsystem: "metric",
    maincolor: "0F6F6C", fontcolor: "FFFFFF", zoom: "14", viewmode: "map", scroll: "disabled",
  });
  if (datesProvided) {
    params.set("checkin", context.check_in!);
    params.set("checkout", context.check_out!);
  }
  if (guestsProvided && party) {
    params.set("adults", String(party.adults));
    params.set("children", String(party.children));
    params.set("rooms", String(party.rooms));
  }
  return {
    url: `https://www.stay22.com/embed/gm?${params}`,
    datesProvided, guestsProvided, hasChildren: guestsProvided && Boolean(party?.children),
    checkIn: datesProvided ? context.check_in! : null,
    checkOut: datesProvided ? context.check_out! : null,
  };
}
