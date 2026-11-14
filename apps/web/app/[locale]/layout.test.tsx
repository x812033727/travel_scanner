import { beforeEach, describe, expect, it, vi } from "vitest";
import { isValidElement, type ReactNode } from "react";

const { incoming, jar, adsConfig, passthrough } = vi.hoisted(() => ({
  incoming: vi.fn(),
  jar: vi.fn(),
  adsConfig: vi.fn(async () => ({ enabled: false, publisher_id: null as string | null, slot_id: null as string | null, cmp_enabled: false })),
  // vi.mock factories are hoisted above ordinary consts, so this has to be hoisted too.
  passthrough: (name: string) => ({ [name]: (props: Record<string, unknown>) => props.children }),
}));
vi.mock("next/headers", () => ({ headers: incoming, cookies: jar }));
vi.mock("next/navigation", () => ({ notFound: () => { throw new Error("not found"); } }));
vi.mock("next-intl", () => ({
  hasLocale: (locales: string[], locale: string) => locales.includes(locale),
  ...passthrough("NextIntlClientProvider"),
}));
vi.mock("next-intl/server", () => ({
  getMessages: async () => ({}),
  getTranslations: async () => (key: string) => key,
}));
vi.mock("@/lib/adsense-config", () => ({ fetchAdsenseConfig: adsConfig }));
vi.mock("@/lib/community/server", () => ({ getCommunityState: async () => ({ enabled: false }) }));
vi.mock("@/lib/site-visibility.server", () => ({ getSiteVisibility: async () => ({}) }));
vi.mock("@/lib/usage-catalog.server", () => ({ getUsageCatalog: async () => ({}) }));
// Named so the tree walk below can find them by identity.
vi.mock("@/components/header-session", () => passthrough("HeaderSessionProvider"));
vi.mock("@/components/saved-items-provider", () => passthrough("SavedItemsProvider"));
vi.mock("@/components/theme-provider", () => passthrough("ThemeProvider"));
vi.mock("@/components/site-visibility-provider", () => passthrough("SiteVisibilityProvider"));
vi.mock("@/components/usage-catalog-provider", () => passthrough("UsageCatalogProvider"));
vi.mock("@/components/community/provider", () => passthrough("CommunityProvider"));
vi.mock("@/components/analytics-provider", () => passthrough("AnalyticsProvider"));
vi.mock("@/components/legacy-ui-localizer", () => ({ LegacyUiLocalizer: () => null }));
vi.mock("@/components/travelpayouts-drive", () => ({ TravelpayoutsDrive: () => null }));
vi.mock("@/components/app-bottom-nav", () => ({ AppBottomNav: () => null }));
vi.mock("@/components/site-footer", () => ({ SiteFooter: () => null }));
vi.mock("@/components/ads/adsense-loader", () => ({ AdsenseLoader: () => null }));

import LocaleLayout, { generateMetadata } from "./layout";
import { ADS_TXT_FALLBACK_PUBLISHER_ID } from "@/app/ads.txt/ads-txt";
import { HeaderSessionProvider } from "@/components/header-session";
import { SavedItemsProvider } from "@/components/saved-items-provider";
import { AdsenseLoader } from "@/components/ads/adsense-loader";

/** Every element of this type anywhere in the returned tree. */
function findAll(node: ReactNode, type: unknown): Record<string, unknown>[] {
  if (Array.isArray(node)) return node.flatMap((child) => findAll(child, type));
  if (!isValidElement(node)) return [];
  const props = node.props as Record<string, unknown>;
  const here = node.type === type ? [props] : [];
  return [...here, ...findAll(props.children as ReactNode, type)];
}

const enabledAds = {
  enabled: true, publisher_id: "ca-pub-4140966684432854", slot_id: "1234567890", cmp_enabled: false,
};
const params = Promise.resolve({ locale: "zh-TW" });

describe("the shared locale document", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    incoming.mockResolvedValue(new Headers({ "x-travel-pathname": "/zh-TW/guides/howto/tokyo-esim" }));
    jar.mockResolvedValue({ has: () => true });
    adsConfig.mockResolvedValue({ enabled: false, publisher_id: null, slot_id: null, cmp_enabled: false });
  });

  it("asks about the reader on an ordinary page", async () => {
    const tree = await LocaleLayout({ children: null, params });
    expect(findAll(tree, HeaderSessionProvider)[0].hasSession).toBe(true);
    expect(findAll(tree, SavedItemsProvider)[0].hasSession).toBe(true);
    expect(findAll(tree, AdsenseLoader)).toHaveLength(0);
  });

  it("asks nothing about the reader in a document that loads Google's ad tag", async () => {
    // This is the privacy property docs/travel-guides.md states: both of these providers
    // fetch /auth/me (`components/header-session.tsx:85` returns early without a session),
    // and a third-party script sharing this document can read whatever they put on the page.
    // Not mounting them with a session means the answer never exists here to be read.
    const tree = await LocaleLayout({ children: null, params, ads: enabledAds });
    expect(findAll(tree, HeaderSessionProvider)[0].hasSession).toBe(false);
    expect(findAll(tree, SavedItemsProvider)[0].hasSession).toBe(false);
    expect(findAll(tree, AdsenseLoader)).toHaveLength(1);
  });

  it("still asks when an ad configuration is present but switched off", async () => {
    // Only advertising actually being served costs the reader their header state.
    const tree = await LocaleLayout({
      children: null, params, ads: { ...enabledAds, enabled: false },
    });
    expect(findAll(tree, HeaderSessionProvider)[0].hasSession).toBe(true);
    expect(findAll(tree, SavedItemsProvider)[0].hasSession).toBe(true);
    expect(findAll(tree, AdsenseLoader)).toHaveLength(0);
  });

  it("has nothing to suppress when the reader carries no session cookie", async () => {
    jar.mockResolvedValue({ has: () => false });
    const tree = await LocaleLayout({ children: null, params, ads: enabledAds });
    expect(findAll(tree, HeaderSessionProvider)[0].hasSession).toBe(false);
  });

  it("emits google-adsense-account meta on public mokaair.com routes and omits it on private or non-production hosts", async () => {
    incoming.mockResolvedValueOnce(new Headers({ host: "mokaair.com", "x-travel-pathname": "/zh-TW" }));
    const homeMeta = await generateMetadata({ params });
    expect(homeMeta.other).toEqual({ "google-adsense-account": ADS_TXT_FALLBACK_PUBLISHER_ID });

    adsConfig.mockResolvedValueOnce({
      enabled: true,
      publisher_id: "ca-pub-9999999999999999",
      slot_id: "1234567890",
      cmp_enabled: true,
    });
    incoming.mockResolvedValueOnce(new Headers({ host: "mokaair.com", "x-travel-pathname": "/zh-TW/life/ai-notes" }));
    const articleMeta = await generateMetadata({ params });
    expect(articleMeta.other).toEqual({ "google-adsense-account": "ca-pub-9999999999999999" });

    incoming.mockResolvedValueOnce(new Headers({ host: "mokaair.com", "x-travel-pathname": "/zh-TW/admin/settings" }));
    const adminMeta = await generateMetadata({ params });
    expect(adminMeta.other).toBeUndefined();

    incoming.mockResolvedValueOnce(new Headers({ host: "localhost:3000", "x-travel-pathname": "/zh-TW" }));
    const localMeta = await generateMetadata({ params });
    expect(localMeta.other).toBeUndefined();
  });
});
