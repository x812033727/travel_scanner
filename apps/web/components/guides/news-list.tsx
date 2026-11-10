import { Link } from "@/i18n/navigation";
import { GuideImage } from "./guide-image";
import { guideHref, type GuideSummary } from "@/lib/guides";

/** Preserve event-date order when the first story gets more space. Missing artwork and
 * undated evergreen entries stay readable without invented assets or dates. */
export function NewsList({ articles, className = "mt-4", lead = false, titleTag: Title = "p" }: {
  articles: readonly GuideSummary[];
  className?: string;
  lead?: boolean;
  titleTag?: "h2" | "h3" | "h4" | "p";
}) {
  if (!articles.length) return null;
  return (
    <ol className={`${className} divide-y divide-[var(--line)]`} data-testid="news-list">
      {articles.map((article, index) => {
        const prominent = lead && index === 0;
        return (
          <li key={`${article.kind}:${article.slug}`} data-testid={prominent ? "news-lead" : undefined}
            className={prominent ? "mb-3 rounded-3xl border border-[var(--line)] bg-[var(--surface)]" : "py-6"}>
            <Link href={guideHref(article.kind, article.slug)} aria-label={article.title}
              className={`group grid min-w-0 gap-4 rounded-xl outline-offset-4 [overflow-wrap:anywhere] ${prominent
                ? `p-5 sm:p-7 ${article.hero ? "md:grid-cols-2 md:items-center md:gap-6" : ""}`
                : article.hero ? "grid-cols-[5.5rem_minmax(0,1fr)] sm:grid-cols-[10rem_minmax(0,1fr)] sm:gap-6" : ""}`}>
              {article.hero ? (
                <GuideImage src={article.hero.src} alt="" width={article.hero.width} height={article.hero.height}
                  loading={prominent ? "eager" : "lazy"} fetchPriority={prominent ? "high" : undefined} decoding="async"
                  className={`aspect-video w-full rounded-2xl object-contain ${prominent ? "order-2" : ""}`} />
              ) : null}
              <div className="min-w-0">
                <p className="flex flex-wrap items-center gap-x-3 gap-y-1 text-xs text-[var(--muted)]">
                  {article.topics[0] ? <span className="font-semibold text-[var(--teal)]">{article.topics[0].label}</span> : null}
                  {article.news_date ? <time dateTime={article.news_date} className="tabular-nums">{article.news_date}</time> : null}
                </p>
                <Title className={`mt-2 font-bold tracking-tight text-[var(--ink)] group-hover:text-[var(--teal)] group-hover:underline group-focus-visible:underline ${prominent ? "text-2xl leading-snug sm:text-3xl" : "text-lg leading-snug sm:text-xl"}`}>
                  {article.title}
                </Title>
                <p className={`mt-3 text-sm leading-7 text-[var(--muted)] ${prominent ? "line-clamp-4" : "line-clamp-2"}`}>{article.description}</p>
              </div>
            </Link>
          </li>
        );
      })}
    </ol>
  );
}
