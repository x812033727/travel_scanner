import { defaultLocale, normalizeLocale, type Locale } from "@/i18n/routing";

export function activeLocale(): Locale {
  if (typeof document === "undefined") return defaultLocale;
  return normalizeLocale(document.documentElement.lang);
}

export function formatCurrency(value: number, currency = "TWD") {
  const formatted = new Intl.NumberFormat(activeLocale(), {
    style: "currency",
    currency,
    maximumFractionDigits: 0,
  }).format(value);
  // Intl renders TWD as a bare "$" in Chinese locales and as "TWD" in ja/ko,
  // which on a price-comparison site reads as USD or as a code; pin NT$.
  return currency === "TWD" ? formatted.replace(/^(-?)(?:NT\$|TWD\s?|\$)/, "$1NT$$") : formatted;
}

export function formatDateTime(value: string | number | Date, options?: Intl.DateTimeFormatOptions) {
  return new Intl.DateTimeFormat(activeLocale(), options || { dateStyle: "medium", timeStyle: "short" }).format(new Date(value));
}

export function formatNumber(value: number) {
  return new Intl.NumberFormat(activeLocale()).format(value);
}
