import { hasLocale } from "next-intl";
import { getRequestConfig } from "next-intl/server";
import { notFound } from "next/navigation";
import { routing } from "./routing";

const namespaces = ["common", "metadata", "navigation", "auth", "search", "trips", "alerts", "pricing", "usage", "account", "admin", "availability", "errors", "legacy"] as const;

export default getRequestConfig(async ({ requestLocale }) => {
  const requested = await requestLocale;
  if (!hasLocale(routing.locales, requested)) notFound();
  const entries = await Promise.all(namespaces.map(async (namespace) => {
    const messages = (await import(`../messages/${requested}/${namespace}.json`)).default;
    return [namespace, messages] as const;
  }));
  return { locale: requested, messages: Object.fromEntries(entries) };
});
