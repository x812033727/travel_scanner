import { defaultLocale, normalizeLocale, type Locale } from "@/i18n/routing";

export function activeLocale(): Locale {
  if (typeof document === "undefined") return defaultLocale;
  return normalizeLocale(document.documentElement.lang);
}

// Intl renders TWD as a bare "$" in Chinese locales and as "TWD" in ja/ko,
// which on a price-comparison site reads as USD or as a code; pin NT$.
function pinNewTaiwanDollar(formatted: string, currency: string) {
  return currency === "TWD" ? formatted.replace(/^(-?)(?:NT\$|TWD\s?|\$)/, "$1NT$$") : formatted;
}

export function formatCurrency(value: number, currency = "TWD") {
  return pinNewTaiwanDollar(
    new Intl.NumberFormat(activeLocale(), {
      style: "currency",
      currency,
      maximumFractionDigits: 0,
    }).format(value),
    currency,
  );
}

// formatCurrency rounds every price to whole units, which is right for the
// search results it was written for but wrong for a ledger the traveller types
// themselves. Here Intl decides the decimals from the currency: two for TWD and
// USD, none for JPY, KRW and VND.
export function formatMoney(value: number, currency = "TWD") {
  return pinNewTaiwanDollar(
    new Intl.NumberFormat(activeLocale(), { style: "currency", currency }).format(value),
    currency,
  );
}

export function formatDateTime(value: string | number | Date, options?: Intl.DateTimeFormatOptions) {
  return new Intl.DateTimeFormat(activeLocale(), options || { dateStyle: "medium", timeStyle: "short" }).format(new Date(value));
}

export function formatNumber(value: number) {
  return new Intl.NumberFormat(activeLocale()).format(value);
}
