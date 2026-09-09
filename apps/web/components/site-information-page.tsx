import type { Metadata } from "next";
import { SiteHeader } from "@/components/site-header";
import { SitePageContent } from "@/components/site-page-content";
import { getSitePage, getSitePageCopy } from "@/lib/site-pages.server";
import { requirementKeys, type SitePageSlug } from "@/lib/site-pages";

export async function siteInformationMetadata(slug: SitePageSlug, locale: string): Promise<Metadata> {
  const [state, copy] = await Promise.all([getSitePage(slug, locale), getSitePageCopy(locale)]);
  return {
    title: state.document?.title || copy[slug],
    description: state.document?.description || copy[state.status === "unavailable" ? "unavailable" : "unpublished"],
    robots: state.status === "published" ? undefined : { index: false },
  };
}

export async function SiteInformationPage({ slug, locale }: { slug: SitePageSlug; locale: string }) {
  const [state, copy] = await Promise.all([getSitePage(slug, locale), getSitePageCopy(locale)]);
  const labels = Object.fromEntries([...requirementKeys, "effectiveDate"].map((key) => [key, copy[key as keyof typeof copy]])) as Record<typeof requirementKeys[number] | "effectiveDate", string>;
  return <><SiteHeader /><main className="mx-auto max-w-3xl px-5 py-10 md:py-14">
    {state.document ? <SitePageContent document={state.document} labels={labels} /> : <>
      <h1 className="text-3xl font-bold">{copy[slug]}</h1>
      <p role={state.status === "unavailable" ? "alert" : "status"} className="mt-5 leading-8 text-[var(--muted)]">{copy[state.status === "unavailable" ? "unavailable" : "unpublished"]}</p>
    </>}
  </main></>;
}
