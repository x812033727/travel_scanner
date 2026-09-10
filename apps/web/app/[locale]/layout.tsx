import type { Metadata } from "next";
import { hasLocale, NextIntlClientProvider } from "next-intl";
import { getMessages, getTranslations } from "next-intl/server";
import { cookies, headers } from "next/headers";
import { notFound } from "next/navigation";
import { LegacyUiLocalizer } from "@/components/legacy-ui-localizer";
import { AppBottomNav } from "@/components/app-bottom-nav";
import { HeaderSessionProvider } from "@/components/header-session";
import { SavedItemsProvider } from "@/components/saved-items-provider";
import { SiteFooter } from "@/components/site-footer";
import { ThemeProvider } from "@/components/theme-provider";
import { SiteVisibilityProvider } from "@/components/site-visibility-provider";
import { UsageCatalogProvider } from "@/components/usage-catalog-provider";
import { CommunityProvider } from "@/components/community/provider";
import { getCommunityState } from "@/lib/community/server";
import { AnalyticsProvider } from "@/components/analytics-provider";
import { TravelpayoutsDrive } from "@/components/travelpayouts-drive";
import { routing } from "@/i18n/routing";
import { alternatesFor, routePathFromRequest, siteUrl } from "@/lib/seo";
import { getSiteVisibility } from "@/lib/site-visibility.server";
import { NAVIGATION_HISTORY_BOOTSTRAP_SCRIPT } from "@/lib/navigation-history";
import { TEXT_SIZE_BOOTSTRAP_SCRIPT } from "@/lib/text-size";
import { THEME_BOOTSTRAP_SCRIPT } from "@/lib/theme";
import { isTravelpayoutsDriveOrigin } from "@/lib/travelpayouts-drive";
import { getUsageCatalog } from "@/lib/usage-catalog.server";
import "../globals.css";

type Props = Readonly<{
  children: React.ReactNode;
  params: Promise<{ locale: string }>;
}>;

const travelpayoutsDriveEnabled = isTravelpayoutsDriveOrigin(siteUrl);

export function generateStaticParams() {
  return routing.locales.map((locale) => ({ locale }));
}

export async function generateMetadata({ params }: Pick<Props, "params">): Promise<Metadata> {
  const { locale } = await params;
  if (!hasLocale(routing.locales, locale)) notFound();
  const [t, requestHeaders] = await Promise.all([
    getTranslations({ locale, namespace: "metadata" }),
    headers(),
  ]);
  // Every page inherits this `alternates` unless it sets its own, so a fixed value here made
  // all forty-odd routes canonicalize to the locale home page. proxy.ts puts the real path in
  // this header; a page wanting a different canonical still overrides the whole field.
  const path = routePathFromRequest(requestHeaders.get("x-travel-pathname"));
  const home = path === "/";
  return {
    metadataBase: new URL(siteUrl),
    title: t("title"),
    description: t("description"),
    alternates: alternatesFor(locale, path),
    openGraph: {
      // Only the home page carries the site-level social copy. Everywhere else these are left
      // out on purpose: Next's postProcessMetadata fills og:title and og:description from the
      // page's own resolved title, which is what a share card should say. Naming them here
      // would hand every page the site-wide pair instead.
      ...(home ? { title: t("ogTitle"), description: t("ogDescription") } : {}),
      images: [{ url: "/og.png", width: 1200, height: 630, alt: t("ogTitle") }],
      locale: locale.replace("-", "_"),
      alternateLocale: routing.locales.filter((value) => value !== locale).map((value) => value.replace("-", "_")),
      type: "website",
    },
    twitter: {
      card: "summary_large_image",
      ...(home ? { title: t("ogTitle"), description: t("ogDescription") } : {}),
      images: ["/og.png"],
    },
  };
}

export default async function LocaleLayout({ children, params }: Props) {
  const { locale } = await params;
  if (!hasLocale(routing.locales, locale)) notFound();
  const [messages, siteVisibility, usageCatalog, requestHeaders, jar, community] = await Promise.all([
    getMessages(),
    getSiteVisibility(),
    getUsageCatalog(locale),
    headers(),
    cookies(),
    getCommunityState(),
  ]);
  // Nobody carrying a session cookie means nobody to ask about. Both providers below
  // used to find that out by sending a request that could only come back 401, on every
  // page a signed-out reader opened.
  const hasSession = jar.has("travel_access");
  // Set by proxy.ts so the static inline bootstraps satisfy the nonce-based CSP.
  const nonce = requestHeaders.get("x-nonce") ?? undefined;
  return (
    <html lang={locale} data-theme-preference="system" suppressHydrationWarning>
      <head>
        {/* A plain script in <head>, not next/script: `beforeInteractive` queues this
            into `self.__next_s` after </head>, which is late enough that a reader on
            the largest text size watched the page paint at 16px and then jump to 20px
            (measured: the hero moved 30px down on a throttled phone). Parser-blocking
            in the head is the whole point of a bootstrap. */}
        {/* History dispatch must also be registered before the router hydrates. */}
        <script nonce={nonce} dangerouslySetInnerHTML={{ __html: `${NAVIGATION_HISTORY_BOOTSTRAP_SCRIPT};${THEME_BOOTSTRAP_SCRIPT};${TEXT_SIZE_BOOTSTRAP_SCRIPT}` }} />
      </head>
      <body>
        <NextIntlClientProvider messages={messages}>
          <ThemeProvider>
          <SiteVisibilityProvider state={siteVisibility}>
            <UsageCatalogProvider state={usageCatalog}>
              <AnalyticsProvider>
                <TravelpayoutsDrive enabled={travelpayoutsDriveEnabled} />
                <LegacyUiLocalizer />
                {/* One /auth/me for the whole page. It used to be asked three times —
                    by the header, the currency switcher and the account panel — and a
                    signed-out reader got three 401s for one fact. */}
                {/* Keyed, so signing in or out remounts both providers instead of
                    leaving the previous session's answers in client state. */}
                <HeaderSessionProvider key={hasSession ? "session" : "anonymous"} hasSession={hasSession}>
                  <CommunityProvider state={community}>
                  <SavedItemsProvider hasSession={hasSession}>
                    <div className="public-app-shell">
                      {children}
                      {/* Inside the shell, so the 5rem the shell already reserves for the
                          fixed bottom navigation sits below the footer rather than over it. */}
                      <SiteFooter year={new Date().getFullYear()} />
                    </div>
                    <AppBottomNav />
                  </SavedItemsProvider>
                  </CommunityProvider>
                </HeaderSessionProvider>
              </AnalyticsProvider>
            </UsageCatalogProvider>
          </SiteVisibilityProvider>
          </ThemeProvider>
        </NextIntlClientProvider>
      </body>
    </html>
  );
}
