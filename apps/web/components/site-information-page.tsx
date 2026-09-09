import type { Metadata } from "next";
import { getTranslations } from "next-intl/server";
import { SiteHeader } from "@/components/site-header";
import { SitePageContent } from "@/components/site-page-content";
import { getSitePage } from "@/lib/site-pages.server";
import { requirementKeys, type SitePageSlug } from "@/lib/site-pages";

export async function siteInformationMetadata(slug: SitePageSlug, locale: string): Promise<Metadata> {
  const [state, t] = await Promise.all([getSitePage(slug, locale), getTranslations({ locale, namespace: "admin.sitePages" })]);
  return {
    title: state.document?.title || t(slug),
    description: state.document?.description || t(state.status === "unavailable" ? "unavailable" : "unpublished"),
    robots: state.status === "published" ? undefined : { index: false },
  };
}

export async function SiteInformationPage({ slug, locale }: { slug: SitePageSlug; locale: string }) {
  const [state, t] = await Promise.all([getSitePage(slug, locale), getTranslations({ locale, namespace: "admin.sitePages" })]);
  const labels = Object.fromEntries([...requirementKeys, "effectiveDate"].map((key) => [key, t(key)])) as Record<typeof requirementKeys[number] | "effectiveDate", string>;
  return <><SiteHeader /><main className="mx-auto max-w-3xl px-5 py-10 md:py-14">
    {state.document ? <SitePageContent document={state.document} labels={labels} /> : <>
      <h1 className="text-3xl font-bold">{t(slug)}</h1>
      <p role={state.status === "unavailable" ? "alert" : "status"} className="mt-5 leading-8 text-[var(--muted)]">{t(state.status === "unavailable" ? "unavailable" : "unpublished")}</p>
    </>}
  </main></>;
}
