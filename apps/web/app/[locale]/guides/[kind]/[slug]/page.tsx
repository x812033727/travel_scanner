import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { getTranslations } from "next-intl/server";
import { GuideArticle } from "@/components/guides/article";
import { SiteHeader } from "@/components/site-header";
import { StructuredData } from "@/components/structured-data";
import { Link } from "@/i18n/navigation";
import { localeLabels, type Locale } from "@/i18n/routing";
import { guideHref, isGuideKind } from "@/lib/guides";
import { getGuideArticle } from "@/lib/guides.server";
import { localeUrl } from "@/lib/seo";
import { breadcrumbs } from "@/lib/structured-data";

type Params = { locale: Locale; kind: string; slug: string };

async function resolve(params: Promise<Params>) {
  const { locale, kind, slug } = await params;
  if (!isGuideKind(kind)) notFound();
  return { locale, kind, slug };
}

export async function generateMetadata({ params }: { params: Promise<Params> }): Promise<Metadata> {
  const { locale, kind, slug } = await resolve(params);
  const [state, t] = await Promise.all([
    getGuideArticle(kind, slug, locale),
    getTranslations({ locale, namespace: "common" }),
  ]);
  const path = guideHref(kind, slug);
  if (state.status !== "published" || !state.document) {
    return {
      title: t("guides.unavailableTitle"),
      description: t(state.status === "unpublished" ? "guides.notTranslated" : "guides.unavailable"),
      robots: { index: false },
      alternates: { canonical: localeUrl(locale, path) },
    };
  }
  // Each locale publishes independently, so the root layout's all-five alternate set would
  // advertise translations that do not exist. Declare only the ones actually published.
  const languages = Object.fromEntries(state.published_locales.map((value) => [value, localeUrl(value, path)]));
  return {
    title: state.document.title,
    description: state.document.description,
    alternates: {
      canonical: localeUrl(locale, path),
      languages: {
        ...languages,
        ...(state.published_locales.includes("en") ? { "x-default": localeUrl("en", path) } : {}),
      },
    },
  };
}

export default async function GuideArticlePage({ params }: { params: Promise<Params> }) {
  const { locale, kind, slug } = await resolve(params);
  const [state, t, nav] = await Promise.all([
    getGuideArticle(kind, slug, locale),
    getTranslations({ locale, namespace: "common" }),
    getTranslations({ locale, namespace: "navigation" }),
  ]);
  const heading = kind === "intel" ? t("guides.intelTitle") : t("guides.howtoTitle");

  if (state.status !== "published" || !state.document) {
    const others = state.published_locales.filter((value) => value !== locale);
    return (
      <>
        <SiteHeader />
        <main className="mx-auto max-w-3xl px-5 py-10 md:py-14">
          <h1 className="text-3xl font-bold">{t("guides.unavailableTitle")}</h1>
          <p role={state.status === "unavailable" ? "alert" : "status"} className="mt-5 leading-8 text-[var(--muted)]">
            {t(state.status === "unpublished" ? "guides.notTranslated" : "guides.unavailable")}
          </p>
          {others.length ? (
            <ul className="mt-5 flex flex-wrap gap-3">
              {others.map((value) => (
                <li key={value}>
                  <a className="inline-flex min-h-11 items-center text-[var(--teal)] underline" href={`/${value}${guideHref(kind, slug)}`} hrefLang={value}>
                    {localeLabels[value]}
                  </a>
                </li>
              ))}
            </ul>
          ) : null}
          <p className="mt-6">
            <Link className="inline-flex min-h-11 items-center text-[var(--teal)] underline" href={`/guides/${kind}`}>
              {heading}
            </Link>
          </p>
        </main>
      </>
    );
  }

  return (
    <>
      <SiteHeader />
      <StructuredData
        data={[
          breadcrumbs(locale, [
            { name: nav("home"), path: "/" },
            { name: t("guides.hubTitle"), path: "/guides" },
            { name: heading, path: `/guides/${kind}` },
            { name: state.document.title, path: guideHref(kind, slug) },
          ]),
          // Honest because this page renders the article it describes: a real headline, a
          // real body and a real publication date. No image is claimed; there is none.
          {
            "@context": "https://schema.org",
            "@type": "Article",
            headline: state.document.title,
            description: state.document.description,
            inLanguage: locale,
            datePublished: state.document.published_at,
            mainEntityOfPage: localeUrl(locale, guideHref(kind, slug)),
            author: { "@type": "Organization", name: "Mokaair" },
            publisher: { "@type": "Organization", name: "Mokaair" },
          },
        ]}
      />
      <main className="mx-auto max-w-3xl px-5 py-10 md:py-14">
        <GuideArticle
          state={{ ...state, document: state.document }}
          labels={{
            intel: t("guides.intel"), howto: t("guides.howto"),
            published: t("guides.published"), updated: t("guides.updated"),
            expiredNotice: t("guides.expiredNotice"), validUntil: t("guides.validUntil"),
            sources: t("guides.sources"), checkedOn: t("guides.checkedOn"),
            destination: t("guides.destination"), otherLanguages: t("guides.otherLanguages"),
          }}
        />
        <p className="mt-10">
          <Link className="inline-flex min-h-11 items-center text-[var(--teal)] underline" href={`/guides/${kind}`}>
            {heading}
          </Link>
        </p>
      </main>
    </>
  );
}
