export type HotelUnavailableStay = {
  start_date: string;
  end_date: string;
  reason: string;
  source_url: string;
};

export type HotelOperatingRules = {
  unavailable_stays: HotelUnavailableStay[];
  last_checkout_date?: string | null;
  last_checkout_reason?: string | null;
  last_checkout_source_url?: string | null;
};

export type HotelOperationError =
  | "invalidJson" | "invalidRules" | "emptyRules" | "invalidDates"
  | "invalidReason" | "invalidSource" | "overlappingDates" | "tooManyRanges";

function record(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

export function isHotelOperationDate(value: unknown): value is string {
  if (typeof value !== "string" || !/^\d{4}-\d{2}-\d{2}$/.test(value) || value.startsWith("0000-")) return false;
  const date = new Date(`${value}T00:00:00.000Z`);
  return Number.isFinite(date.getTime()) && date.toISOString().slice(0, 10) === value;
}

function validReason(value: unknown) {
  return typeof value === "string" && value.trim().length > 0 && value.trim().length <= 1000;
}

function validSource(value: unknown) {
  if (typeof value !== "string") return false;
  try {
    const url = new URL(value);
    return url.protocol === "https:" && !!url.hostname && !url.username && !url.password;
  } catch {
    return false;
  }
}

export function hotelOperatingRulesError(value: unknown): HotelOperationError | null {
  if (value == null) return null;
  if (!record(value) || (value.unavailable_stays !== undefined && !Array.isArray(value.unavailable_stays))) return "invalidRules";
  const ranges = (value.unavailable_stays ?? []) as unknown[];
  if (ranges.length > 50) return "tooManyRanges";
  const sorted: HotelUnavailableStay[] = [];
  for (const range of ranges) {
    if (!record(range)) return "invalidRules";
    if (!isHotelOperationDate(range.start_date) || !isHotelOperationDate(range.end_date) || range.start_date >= range.end_date) return "invalidDates";
    if (!validReason(range.reason)) return "invalidReason";
    if (!validSource(range.source_url)) return "invalidSource";
    sorted.push(range as HotelUnavailableStay);
  }
  sorted.sort((a, b) => a.start_date.localeCompare(b.start_date));
  if (sorted.some((range, index) => index > 0 && range.start_date < sorted[index - 1].end_date)) return "overlappingDates";
  const cutoff = value.last_checkout_date != null || value.last_checkout_reason != null || value.last_checkout_source_url != null;
  if (cutoff) {
    if (!isHotelOperationDate(value.last_checkout_date)) return "invalidDates";
    if (!validReason(value.last_checkout_reason)) return "invalidReason";
    if (!validSource(value.last_checkout_source_url)) return "invalidSource";
  }
  return !ranges.length && !cutoff ? "emptyRules" : null;
}

export function evaluateHotelOperatingStay(
  rules: HotelOperatingRules | null | undefined,
  checkIn?: string,
  checkOut?: string,
): "allowed" | "dates_required" | "unavailable" | "invalid" {
  if (!rules) return "allowed";
  if (hotelOperatingRulesError(rules)) return "invalid";
  if (!checkIn || !checkOut) return "dates_required";
  if (!isHotelOperationDate(checkIn) || !isHotelOperationDate(checkOut) || checkOut <= checkIn) return "invalid";
  if (rules.last_checkout_date && checkOut > rules.last_checkout_date) return "unavailable";
  return (rules.unavailable_stays ?? []).some((range) => checkIn < range.end_date && checkOut > range.start_date)
    ? "unavailable" : "allowed";
}

/** The JSON editor remains the only draft; date controls never retain a competing copy. */
export function readHotelOperationDraft(json: string): {
  rules: HotelOperatingRules | null;
  error: HotelOperationError | null;
  editable: boolean;
} {
  let product: unknown;
  try { product = JSON.parse(json); } catch { return { rules: null, error: "invalidJson", editable: false }; }
  if (!record(product) || (product.facts !== undefined && !record(product.facts))) return { rules: null, error: "invalidJson", editable: false };
  const value = (product.facts as Record<string, unknown> | undefined)?.hotel_operating_rules;
  if (value == null) return { rules: null, error: null, editable: true };
  const error = hotelOperatingRulesError(value);
  if (!record(value) || (value.unavailable_stays !== undefined && !Array.isArray(value.unavailable_stays))) return { rules: null, error: "invalidRules", editable: false };
  const ranges = (value.unavailable_stays ?? []) as unknown[];
  if (ranges.some((range) => !record(range))) return { rules: null, error: "invalidRules", editable: false };
  const text = (value: unknown) => typeof value === "string" ? value : "";
  return {
    editable: true,
    error,
    rules: {
      ...value,
      unavailable_stays: ranges.map((range) => {
        const row = range as Record<string, unknown>;
        return { ...row, start_date: text(row.start_date), end_date: text(row.end_date), reason: text(row.reason), source_url: text(row.source_url) };
      }),
      ...(value.last_checkout_date != null ? { last_checkout_date: text(value.last_checkout_date) } : {}),
      ...(value.last_checkout_reason != null ? { last_checkout_reason: text(value.last_checkout_reason) } : {}),
      ...(value.last_checkout_source_url != null ? { last_checkout_source_url: text(value.last_checkout_source_url) } : {}),
    },
  };
}

export function writeHotelOperationDraft(json: string, rules: HotelOperatingRules | null): string {
  const product = JSON.parse(json) as Record<string, unknown>;
  const hasCutoff = rules?.last_checkout_date != null || rules?.last_checkout_reason != null || rules?.last_checkout_source_url != null;
  return JSON.stringify({
    ...product,
    facts: {
      ...(product.facts as Record<string, unknown> | undefined),
      hotel_operating_rules: rules && (rules.unavailable_stays.length || hasCutoff) ? rules : null,
    },
  }, null, 2);
}
