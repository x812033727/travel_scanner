import React from "react";
import { vi } from "vitest";
import account from "./messages/zh-TW/account.json";
import auth from "./messages/zh-TW/auth.json";
import common from "./messages/zh-TW/common.json";
import navigation from "./messages/zh-TW/navigation.json";
import search from "./messages/zh-TW/search.json";
import trips from "./messages/zh-TW/trips.json";

const catalogs: Record<string, Record<string, string>> = { account, auth, common, navigation, search, trips };

function translator(namespace: string) {
  return (key: string, values?: Record<string, string | number>) => {
    let value = catalogs[namespace]?.[key] || key;
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
  getTranslations: async (namespace: string) => translator(namespace),
}));

vi.mock("@/i18n/navigation", () => ({
  Link: ({ href, children, ...props }: React.AnchorHTMLAttributes<HTMLAnchorElement> & { href: string }) =>
    React.createElement("a", { href, ...props }, children),
  usePathname: () => "/",
  useRouter: () => ({ push: vi.fn(), replace: vi.fn(), refresh: vi.fn() }),
}));
