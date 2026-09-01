import { defaultLocale, normalizeLocale, type Locale } from "@/i18n/routing";

export function activeLocale(): Locale {
  if (typeof document === "undefined") return defaultLocale;
  return normalizeLocale(document.documentElement.lang);
}

export function formatCurrency(value: number, currency = "TWD") {
  return new Intl.NumberFormat(activeLocale(), {
    style: "currency",
    currency,
    maximumFractionDigits: 0,
  }).format(value);
}

export function formatDateTime(value: string | number | Date, options?: Intl.DateTimeFormatOptions) {
  return new Intl.DateTimeFormat(activeLocale(), options || { dateStyle: "medium", timeStyle: "short" }).format(new Date(value));
}

export function formatNumber(value: number) {
  return new Intl.NumberFormat(activeLocale()).format(value);
}
