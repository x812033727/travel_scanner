import { ArrowUpRight } from "lucide-react";
import { useLocale } from "next-intl";
import { getPathname } from "@/i18n/navigation";
import type { Locale } from "@/i18n/routing";
import { guideHref, visibleGuideHero, type GuideSummary } from "@/lib/guides";
import { GuideImage } from "./guide-image";

/** The picture and its link belong to this guide, even when the adjacent news has no photo. */
export function ChannelGuide({ articles, news, label }: {
  articles: readonly GuideSummary[];
  news: readonly GuideSummary[];
  label: string;
}) {
  const locale = useLocale() as Locale;
  const pick = articles.find((article) =>
    !article.news_date && visibleGuideHero(article.hero) && !news.some((story) => story.slug === article.slug),
  );
  if (!pick?.hero) return null;
  const { hero } = pick;
  return (
    <aside aria-label={label} className="min-w-0">
      <a href={getPathname({ locale, href: guideHref(pick.kind, pick.slug) })} aria-label={pick.title}
        className="group grid h-full min-w-0 grid-cols-[5.5rem_minmax(0,1fr)] items-center gap-3 rounded-xl border border-[var(--line)] bg-[var(--surface)] p-2.5 text-[var(--ink)] transition-colors hover:border-[var(--teal)] sm:grid-cols-[7rem_minmax(0,1fr)] md:block md:p-3">
        <GuideImage src={hero.src} alt={hero.alt} width={hero.width} height={hero.height} decoding="async"
          className="aspect-video w-full rounded-md bg-[var(--paper)] object-contain" />
        <div className="min-w-0 md:mt-2.5">
          <span className="flex items-center justify-between gap-2 text-xs font-semibold text-[var(--teal-dark)]">
            {label}<ArrowUpRight size={16} aria-hidden className="shrink-0" />
          </span>
          <p className="mt-1 text-sm font-bold leading-snug underline-offset-4 [overflow-wrap:anywhere] group-hover:underline group-focus-visible:underline md:text-base">{pick.title}</p>
        </div>
      </a>
    </aside>
  );
}
