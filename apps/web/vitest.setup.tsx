import React from "react";
import { vi } from "vitest";
import account from "./messages/zh-TW/account.json";
import admin from "./messages/zh-TW/admin.json";
import auth from "./messages/zh-TW/auth.json";
import availability from "./messages/zh-TW/availability.json";
import common from "./messages/zh-TW/common.json";
import navigation from "./messages/zh-TW/navigation.json";
import pricing from "./messages/zh-TW/pricing.json";
import search from "./messages/zh-TW/search.json";
import trips from "./messages/zh-TW/trips.json";
import usage from "./messages/zh-TW/usage.json";
import hotspots from "./messages/zh-TW/hotspots.json";
import hotspotAdmin from "./messages/zh-TW/hotspotAdmin.json";
import restaurants from "./messages/zh-TW/restaurants.json";
import foods from "./messages/zh-TW/foods.json";
import foodAdmin from "./messages/zh-TW/foodAdmin.json";
import newTrip from "./messages/zh-TW/newTrip.json";

const catalogs: Record<string, unknown> = { account, admin, auth, availability, common, navigation, pricing, search, trips, usage, hotspots, hotspotAdmin, restaurants, foods, foodAdmin, newTrip };

function message(namespace: string, key: string): string | undefined {
  let current: unknown = catalogs;
  for (const part of [...namespace.split("."), ...key.split(".")]) {
    if (typeof current !== "object" || current === null) return undefined;
    current = (current as Record<string, unknown>)[part];
  }
  return typeof current === "string" ? current : undefined;
}

function translator(namespace: string) {
  return (key: string, values?: Record<string, string | number>) => {
    let value = message(namespace, key) || key;
    for (const [name, replacement] of Object.entries(values || {})) {
      value = value.replaceAll(`{${name}}`, String(replacement));
    }
    return value;
  };
}

vi.mock("next-intl", () => ({
  useLocale: () => "zh-TW",
  useTranslations: (namespace: string) => translator(namespace),
}));

vi.mock("next-intl/server", () => ({
  getTranslations: async (input: string | { namespace: string }) => translator(typeof input === "string" ? input : input.namespace),
}));

vi.mock("@/i18n/navigation", () => ({
  Link: ({ href, children, ...props }: React.AnchorHTMLAttributes<HTMLAnchorElement> & { href: string }) =>
    React.createElement("a", { href, ...props }, children),
  usePathname: () => "/",
  useRouter: () => ({ push: vi.fn(), replace: vi.fn(), refresh: vi.fn() }),
}));
