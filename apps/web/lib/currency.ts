import { activeLocale } from "@/lib/locale-format";

// Mirrors the Currency literal in apps/api/app/auth/schemas.py: every currency
// destinations.ts assigns to a published destination, plus USD for anywhere
// else. Keep the two lists in step — the API rejects anything outside its own.
export const currencies = ["TWD", "JPY", "KRW", "THB", "SGD", "HKD", "VND", "USD"] as const;
export type Currency = (typeof currencies)[number];
export const defaultCurrency: Currency = "TWD";

export function isCurrency(value: unknown): value is Currency {
  return typeof value === "string" && currencies.includes(value as Currency);
}

export function normalizeCurrency(value: string | null | undefined): Currency {
  return isCurrency(value) ? value : defaultCurrency;
}

// Intl already knows every one of these in all five UI languages, so the names
// stay out of the message catalogs and never drift from the codes.
export function currencyName(currency: Currency) {
  try {
    return new Intl.DisplayNames(activeLocale(), { type: "currency" }).of(currency) || currency;
  } catch {
    return currency;
  }
}
