import { hasLocale } from "next-intl";
import { getRequestConfig } from "next-intl/server";
import { notFound } from "next/navigation";
import { applyUiTextOverrides } from "../lib/ui-text";
import { getUiTextOverrides } from "../lib/ui-text.server";
import { routing } from "./routing";

const namespaces = ["common", "metadata", "navigation", "auth", "search", "trips", "alerts", "pricing", "usage", "account", "admin", "availability", "errors", "legacy", "hotspots", "hotspotAdmin", "hotspotThemes", "restaurants", "foods", "foodAdmin", "catalogReview", "newTrip", "stayAreas"] as const;

export default getRequestConfig(async ({ requestLocale }) => {
  const requested = await requestLocale;
  if (!hasLocale(routing.locales, requested)) notFound();
  const entries = await Promise.all(namespaces.map(async (namespace) => {
    const messages = (await import(`../messages/${requested}/${namespace}.json`)).default;
    return [namespace, messages] as const;
  }));
  // Administrator overrides are layered here, so getTranslations, generateMetadata and the
  // single NextIntlClientProvider all see one merged catalog and no component changes.
  // The merge is copy-on-write; see lib/ui-text.ts and docs/ui-text-overrides.md.
  const overrides = await getUiTextOverrides(requested);
  const merged = applyUiTextOverrides(Object.fromEntries(entries), overrides.entries);
  return { locale: requested, messages: merged.messages };
});
