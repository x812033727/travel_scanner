import { describe, expect, it } from "vitest";
import { fixtureCatalogue, fixtureSeries } from "@/components/gemini-series/fixture.test-data";
import { projectGeminiArticleContent } from "./gemini-series-content";
import type { GuideArticleState } from "./guides";
import { siteUrl } from "./seo";

const catalogue = fixtureCatalogue();
const hidden = catalogue.articles[50].slug;
const href = `${siteUrl}/zh-TW/life/${hidden}#section-3`;
function state(): GuideArticleState {
  return { kind: "life", slug: catalogue.hubSlug, locale: "zh-TW", status: "published", destination_id: null, destination_label: null,
    topics: [], valid_until: null, expired: false, published_locales: ["zh-TW"],
    article_links: [{ kind: "life", slug: hidden, title: "深入概念" }, { kind: "life", slug: "claude-code-tutorials", title: "Claude" }],
    document: { title: "Gemini 教學", description: "系列說明", version: 1, published_at: "2026-09-14", sources: [{ title: "隱藏", url: href, checked_on: "2026-09-14" }], blocks: [
      { type: "heading", level: 2, text: "先備知識" },
      { type: "rich_paragraph", inlines: [{ type: "text", text: "先讀 " }, { type: "link", text: "深入概念", url: href }, { type: "article", text: "再做練習", kind: "life", slug: hidden }] },
      { type: "link", text: "下一步", url: `${siteUrl}/zh-TW/life/${hidden}/?from=guide` },
      { type: "list", ordered: false, items: [`範例 ${href}`, `參考 /zh-TW/life/${hidden}`] },
      { type: "code", language: "text", label: "網址示例", code: href },
      { type: "heading", level: 2, text: "後續內容" },
      { type: "rich_paragraph", inlines: [{ type: "link", text: "GEMINI.md", url: `${siteUrl}/zh-TW/life/gemini-cli-gemini-md` }] },
    ] } };
}
describe("Gemini body visibility", () => {
  it("removes hidden destinations from body and serialized references while retaining prose and headings", () => {
    const source = state(); const before = JSON.stringify(source);
    const projected = projectGeminiArticleContent(source, catalogue, fixtureSeries());
    expect(JSON.stringify(projected)).not.toContain(hidden);
    expect(projected.document?.blocks[1]).toEqual({ type: "rich_paragraph", inlines: [{ type: "text", text: "先讀 " }, { type: "text", text: "深入概念" }, { type: "text", text: "再做練習" }] });
    expect(projected.document?.blocks.filter(block => block.type === "heading")).toEqual(source.document?.blocks.filter(block => block.type === "heading"));
    expect(JSON.stringify(projected)).toContain("gemini-cli-gemini-md");
    expect(projected.article_links).toHaveLength(1);
    expect(JSON.stringify(source)).toBe(before);
  });
  it("preserves full content after advanced enablement", () => {
    const source = state();
    expect(projectGeminiArticleContent(source, catalogue, fixtureSeries(true))).toBe(source);
  });
  it("does not rewrite another series, locale or unavailable article", () => {
    for (const source of [{ ...state(), slug: "claude-code-tutorials" }, { ...state(), locale: "en" }, { ...state(), document: null }]) {
      expect(projectGeminiArticleContent(source, catalogue, null)).toBe(source);
    }
  });
  it("removes directory links while the hub is unavailable", () => {
    const source = state();
    source.document!.blocks.push({ type: "link", text: "返回目錄", url: `${siteUrl}/zh-TW/life/${catalogue.hubSlug}` });
    expect(projectGeminiArticleContent(source, catalogue, null).document?.blocks.at(-1)).toEqual({ type: "paragraph", text: "返回目錄" });
  });
});
