import type { Metadata } from "next";
import { hasLocale, NextIntlClientProvider } from "next-intl";
import { getMessages, getTranslations } from "next-intl/server";
import { headers } from "next/headers";
import { notFound } from "next/navigation";
import { LegacyUiLocalizer } from "@/components/legacy-ui-localizer";
import { AppBottomNav } from "@/components/app-bottom-nav";
import { SavedItemsProvider } from "@/components/saved-items-provider";
import { SiteFooter } from "@/components/site-footer";
import { SiteVisibilityProvider } from "@/components/site-visibility-provider";
import { UsageCatalogProvider } from "@/components/usage-catalog-provider";
import { AnalyticsProvider } from "@/components/analytics-provider";
import { routing } from "@/i18n/routing";
import { getSiteVisibility } from "@/lib/site-visibility.server";
import { TEXT_SIZE_BOOTSTRAP_SCRIPT } from "@/lib/text-size";
import { THEME_BOOTSTRAP_SCRIPT } from "@/lib/theme";
import { getUsageCatalog } from "@/lib/usage-catalog.server";
import "../globals.css";

type Props = Readonly<{
  children: React.ReactNode;
  params: Promise<{ locale: string }>;
}>;

const siteUrl = process.env.NEXT_PUBLIC_SITE_URL || "http://localhost:3000";

export function generateStaticParams() {
  return routing.locales.map((locale) => ({ locale }));
}

export async function generateMetadata({ params }: Pick<Props, "params">): Promise<Metadata> {
  const { locale } = await params;
  if (!hasLocale(routing.locales, locale)) notFound();
  const t = await getTranslations({ locale, namespace: "metadata" });
  const languages = Object.fromEntries(routing.locales.map((value) => [value, `${siteUrl}/${value}`]));
  return {
    metadataBase: new URL(siteUrl),
    title: t("title"),
    description: t("description"),
    alternates: { canonical: `${siteUrl}/${locale}`, languages },
    openGraph: {
      title: t("ogTitle"),
      description: t("ogDescription"),
      images: [{ url: "/og.png", width: 1200, height: 630, alt: t("ogTitle") }],
      locale: locale.replace("-", "_"),
      alternateLocale: routing.locales.filter((value) => value !== locale).map((value) => value.replace("-", "_")),
      type: "website",
    },
    twitter: {
      card: "summary_large_image",
      title: t("ogTitle"),
      description: t("ogDescription"),
      images: ["/og.png"],
    },
  };
}

export default async function LocaleLayout({ children, params }: Props) {
  const { locale } = await params;
  if (!hasLocale(routing.locales, locale)) notFound();
  const [messages, siteVisibility, usageCatalog, requestHeaders] = await Promise.all([
    getMessages(),
    getSiteVisibility(),
    getUsageCatalog(locale),
    headers(),
  ]);
  // Set by proxy.ts so the inline theme bootstrap can satisfy the nonce-based CSP.
  const nonce = requestHeaders.get("x-nonce") ?? undefined;
  return (
    <html lang={locale} data-theme-preference="system" suppressHydrationWarning>
      <head>
        {/* A plain script in <head>, not next/script: `beforeInteractive` queues this
            into `self.__next_s` after </head>, which is late enough that a reader on
            the largest text size watched the page paint at 16px and then jump to 20px
            (measured: the hero moved 30px down on a throttled phone). Parser-blocking
            in the head is the whole point of a bootstrap. */}
        <script nonce={nonce} dangerouslySetInnerHTML={{ __html: `${THEME_BOOTSTRAP_SCRIPT};${TEXT_SIZE_BOOTSTRAP_SCRIPT}` }} />
      </head>
      <body>
        <NextIntlClientProvider messages={messages}>
          <SiteVisibilityProvider state={siteVisibility}>
            <UsageCatalogProvider state={usageCatalog}>
              <AnalyticsProvider>
                <LegacyUiLocalizer />
                <SavedItemsProvider>
                  <div className="public-app-shell">
                    {children}
                    {/* Inside the shell, so the 5rem the shell already reserves for the
                        fixed bottom navigation sits below the footer rather than over it. */}
                    <SiteFooter year={new Date().getFullYear()} />
                  </div>
                  <AppBottomNav />
                </SavedItemsProvider>
              </AnalyticsProvider>
            </UsageCatalogProvider>
          </SiteVisibilityProvider>
        </NextIntlClientProvider>
      </body>
    </html>
  );
}
