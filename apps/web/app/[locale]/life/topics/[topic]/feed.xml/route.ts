import { NextResponse } from "next/server";
import { isLocale } from "@/i18n/routing";
import { guideHref, guideTopicHref, isNewsTopic } from "@/lib/guides";
import { getGuideList, getGuideTopicList } from "@/lib/guides.server";
import { localeUrl, siteUrl } from "@/lib/seo";
import { TOPIC_FEED_SIZE, topicFeedPath } from "@/lib/topic-feed";

export const dynamic = "force-dynamic";
type Context = { params: Promise<{ locale: string; topic: string }> };

// XML 1.0 accepts fewer characters than HTML. Preserve valid non-BMP text while
// discarding control characters and lone surrogates before escaping markup.
function escape(value: string): string {
  return Array.from(value).filter((char) => {
    const code = char.codePointAt(0)!;
    return code === 9 || code === 10 || code === 13 || (code >= 0x20 && code <= 0xd7ff)
      || (code >= 0xe000 && code <= 0xfffd) || (code >= 0x10000 && code <= 0x10ffff);
  }).join("").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}

function unavailable() {
  return new NextResponse("feed temporarily unavailable", {
    status: 503,
    headers: { "Retry-After": "600", "Content-Type": "text/plain; charset=utf-8", "Cache-Control": "no-store" },
  });
}

export async function GET(_request: Request, { params }: Context): Promise<NextResponse> {
  const { locale, topic } = await params;
  if (!isLocale(locale) || !isNewsTopic("life", topic)) return new NextResponse("Not found", { status: 404 });
  try {
    const [list, vocabulary] = await Promise.all([
      getGuideList(locale, { section: "life", topic, sort: "latest" }, TOPIC_FEED_SIZE),
      getGuideTopicList(locale, "life"),
    ]);
    if (!list.available || !vocabulary.available) return unavailable();
    const selected = vocabulary.topics.find((item) => item.slug === topic);
    if (!selected) return new NextResponse("Not found", { status: 404 });
    const today = new Date().toISOString().slice(0, 10);
    // The public API owns publication/locale visibility. Keep its expiry rule at
    // this boundary too, without turning source-read failures into empty feeds.
    const articles = list.articles.filter((article) => article.kind === "life" && (!article.valid_until || article.valid_until >= today))
      .slice(0, TOPIC_FEED_SIZE);
    const dated = articles.map((article) => ({ article, timestamp: Date.parse(article.published_at) }));
    if (dated.some(({ timestamp }) => !Number.isFinite(timestamp))) return unavailable();
    dated.sort((a, b) => b.timestamp - a.timestamp || a.article.slug.localeCompare(b.article.slug));
    const self = localeUrl(locale, topicFeedPath(topic));
    const hub = localeUrl(locale, guideTopicHref("life", topic));
    // With no entries, this dates the generated representation, not a fabricated
    // article. Populated feeds use actual publication dates, never polling time.
    const updated = dated.length ? new Date(dated[0].timestamp).toISOString() : new Date().toISOString();
    const entries = dated.map(({ article, timestamp }) => {
      const url = localeUrl(locale, guideHref(article.kind, article.slug));
      const published = new Date(timestamp).toISOString();
      return ["  <entry>", `    <id>${escape(url)}</id>`, `    <title type="text">${escape(article.title)}</title>`,
        `    <link rel="alternate" type="text/html" hreflang="${locale}" href="${escape(url)}"/>`,
        `    <published>${published}</published>`, `    <updated>${published}</updated>`,
        article.description ? `    <summary type="text">${escape(article.description)}</summary>` : "", "  </entry>"].filter(Boolean).join("\n");
    });
    const body = ['<?xml version="1.0" encoding="UTF-8"?>', `<feed xmlns="http://www.w3.org/2005/Atom" xml:lang="${locale}">`,
      `  <id>${escape(self)}</id>`, `  <title type="text">Mokaair — ${escape(selected.label)}</title>`,
      `  <link rel="self" type="application/atom+xml" href="${escape(self)}"/>`,
      `  <link rel="alternate" type="text/html" hreflang="${locale}" href="${escape(hub)}"/>`,
      `  <author><name>Mokaair</name><uri>${escape(siteUrl)}</uri></author>`,
      `  <updated>${updated}</updated>`, ...entries, "</feed>", ""].join("\n");
    return new NextResponse(body, { headers: { "Content-Type": "application/atom+xml; charset=utf-8", "Content-Language": locale, "Cache-Control": "max-age=0, must-revalidate" } });
  } catch { return unavailable(); }
}
