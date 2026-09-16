import type { ArticleReference } from "@/lib/guide-series";
import type { GuideArticleState, GuideBlock, PublishedGuide } from "./guides";
import type { InlineNode } from "./content-blocks";
import type { GeminiCatalogue, VisibleGeminiSeries } from "./gemini-series-projection";
import { siteUrl } from "./seo";

/** Run before rendering/serializing content. Keep heading positions and readable link labels. */
export function projectGeminiArticleContent(state: GuideArticleState, catalogue: GeminiCatalogue, visible: VisibleGeminiSeries | null): GuideArticleState {
  if (state.kind !== "life" || state.locale !== catalogue.locale || !state.document
    || (state.slug !== catalogue.hubSlug && !catalogue.articles.some(article => article.slug === state.slug))) return state;
  const allowed = new Set(visible ? [visible.hubSlug, ...visible.articles.map(article => article.slug)] : []);
  const hidden = new Set([catalogue.hubSlug, ...catalogue.articles.map(article => article.slug)].filter(slug => !allowed.has(slug)));
  if (!hidden.size) return state;
  const hiddenUrl = (raw: string) => {
    try {
      const url = new URL(raw, siteUrl);
      if (url.origin !== new URL(siteUrl).origin) return false;
      const prefix = `/${catalogue.locale}/life/`;
      const pathname = decodeURIComponent(url.pathname).replace(/\/$/, "");
      return pathname.startsWith(prefix) && hidden.has(pathname.slice(prefix.length));
    } catch { return false; }
  };
  const cleanText = (text: string) => text.replace(/https?:\/\/[^\s<>"'`]+|\/[a-z]{2}-[A-Z]{2}\/life\/[a-z0-9-]+(?:[?#][^\s<>"'`]+)?/g, raw => {
    const url = raw.replace(/[)\]。,，；;]+$/, "");
    return hiddenUrl(url) ? "相關教學" + raw.slice(url.length) : raw;
  });
  const inline = (node: InlineNode): InlineNode => {
    if ((node.type === "link" && hiddenUrl(node.url)) || (node.type === "article" && node.kind === "life" && hidden.has(node.slug))) {
      return { type: "text", text: cleanText(node.text) };
    }
    return { ...node, text: cleanText(node.text) };
  };
  const blocks: GuideBlock[] = state.document.blocks.map(block => {
    if (block.type === "rich_paragraph") return { ...block, inlines: block.inlines.map(inline) };
    if (block.type === "link" && hiddenUrl(block.url)) return { type: "paragraph", text: cleanText(block.text) };
    if (block.type === "list") return { ...block, items: block.items.map(cleanText) };
    if (block.type === "table") return { ...block, header: block.header.map(cleanText), rows: block.rows.map(row => row.map(cleanText)), ...(block.caption ? { caption: cleanText(block.caption) } : {}) };
    if (block.type === "code") return { ...block, code: cleanText(block.code), label: cleanText(block.label) };
    if ("text" in block) return { ...block, text: cleanText(block.text) };
    return block;
  });
  const document: PublishedGuide = { ...state.document, title: cleanText(state.document.title), description: cleanText(state.document.description), blocks,
    sources: state.document.sources.filter(source => !hiddenUrl(source.url)) };
  const shown = (refs?: ArticleReference[]) => refs?.filter(ref => ref.kind !== "life" || !hidden.has(ref.slug));
  return { ...state, document, article_links: shown(state.article_links), related: shown(state.related), backlinks: shown(state.backlinks) };
}
