import { describe, expect, it } from "vitest";
import base from "./guide-series.json";
import curriculum from "../../../docs/gemini-series/advanced/curriculum.json";
import contract from "../../../docs/gemini-series/advanced/platform/catalogue-contract.json";
import { filterVisibleGeminiLessons, projectGeminiSeries, visibleGeminiHref, visibleGeminiMember, visibleGeminiNavigation, type GeminiCatalogue } from "./gemini-series-projection";

function full(): GeminiCatalogue {
  return {
    ...structuredClone(base),
    articles: [...structuredClone(base.articles), ...curriculum.articles.map(article => ({
      ...article, stage: 2, minutes: article.estimatedReadingMinutes, labMinutes: article.estimatedLabMinutes,
    }))],
    paths: [...structuredClone(base.paths), ...curriculum.routes.map(route => ({ ...route, stage: 2, description: route.title }))],
  };
}

describe("Gemini server projection contract", () => {
  it("preserves 50 base lessons, eight groups and five routes while dropping every advanced URL", () => {
    const source = full();
    source.articles[49].related = [48, 51, 86];
    source.commands = [...source.commands, { command: "hidden-batch-command", description: "draft", kind: "CLI 指令", article: 85, anchor: "section-3" }];
    const visible = projectGeminiSeries(source);
    expect(visible.articles).toHaveLength(50);
    expect(visible.groups).toHaveLength(8);
    expect(visible.paths).toHaveLength(5);
    expect(visible.articles[49].related).toEqual([48]);
    const serialized = JSON.stringify(visible);
    for (const article of curriculum.articles) expect(serialized).not.toContain(article.slug);
    for (const route of curriculum.routes) expect(serialized).not.toContain(route.id);
    expect(serialized).not.toContain("hidden-batch-command");
  });

  it("projects all frozen 86 identities and eleven paths when explicitly enabled", () => {
    const visible = projectGeminiSeries(full(), true);
    expect(visible.articles.map(({ number, slug }) => ({ number, slug }))).toEqual(contract.articles.map(({ number, slug }) => ({ number, slug })));
    expect(visible.paths.map(route => route.id)).toEqual(contract.paths.map(route => route.id));
    expect(visible.articles).toHaveLength(86);
    expect(visible.paths).toHaveLength(11);
    expect(visible.articles.slice(50).every(article => article.stage === 2 && article.labMinutes && article.track)).toBe(true);
  });

  it("does not mutate the input or forward undeclared nested draft metadata", () => {
    const source = full();
    Object.assign(source, { editorialSecret: { slug: "hidden-draft-url" } });
    Object.assign(source.articles[0], { allDrafts: curriculum.articles });
    Object.assign(source.groups[0], { draftLinks: ["hidden-draft-url"] });
    const before = JSON.stringify(source);
    const projected = projectGeminiSeries(source);
    expect(JSON.stringify(source)).toBe(before);
    expect(JSON.stringify(projected)).not.toContain("hidden-draft-url");
    expect(JSON.stringify(projected)).not.toContain("acceptance");
    expect(projected.articles[0].platforms).not.toBe(source.articles[0].platforms);
  });

  it("hides missing-stage advanced lessons and refuses a forged base stage", () => {
    const source = full();
    delete source.articles[50].stage;
    expect(projectGeminiSeries(source).articles).toHaveLength(50);
    source.articles[50].stage = 1;
    expect(() => projectGeminiSeries(source)).toThrow(/stage/);
  });

  it("rejects duplicate identities and incomplete visible advanced metadata", () => {
    const duplicate = full();
    duplicate.articles = [...duplicate.articles, duplicate.articles[0]];
    expect(() => projectGeminiSeries(duplicate)).toThrow(/Duplicate/);
    const missing = full();
    missing.articles[50].track = "unknown";
    expect(() => projectGeminiSeries(missing, true)).toThrow(/track/);
    expect(projectGeminiSeries(missing).articles).toHaveLength(50);
  });

  it("never exposes a partial advanced rollout or silently missing base lesson", () => {
    const source = full();
    source.articles = source.articles.filter(lesson => lesson.number !== 86);
    expect(projectGeminiSeries(source).articles).toHaveLength(50);
    expect(() => projectGeminiSeries(source, true)).toThrow(/Incomplete/);
    source.articles = source.articles.filter(lesson => lesson.number !== 36);
    expect(() => projectGeminiSeries(source)).toThrow(/Incomplete/);
    expect(projectGeminiSeries(base, true).articles).toHaveLength(50);
  });

  it("uses the same visible set for every next/previous, prerequisite and related destination", () => {
    for (const enabled of [false, true]) {
      const visible = projectGeminiSeries(full(), enabled);
      visible.articles.forEach((lesson, index) => {
        const nav = visibleGeminiNavigation(visible, lesson.number)!;
        expect(nav.previous?.number).toBe(visible.articles[index-1]?.number);
        expect(nav.next?.number).toBe(visible.articles[index+1]?.number);
        expect([...nav.prerequisites, ...nav.related].every(entry => visible.articles.includes(entry))).toBe(true);
      });
      expect(visibleGeminiNavigation(visible, 999)).toBeUndefined();
    }
    expect(visibleGeminiNavigation(projectGeminiSeries(full()), 50)?.next).toBeUndefined();
    expect(visibleGeminiNavigation(projectGeminiSeries(full(), true), 50)?.next?.number).toBe(51);
  });

  it.each(["GEMINI.md", "/memory", "SKILL.md", "RAG", "Batch", "快取", "引用", "手機"])("finds the advanced keyword %s from visible metadata", query => {
    expect(filterVisibleGeminiLessons(projectGeminiSeries(full(), true), { query }).length).toBeGreaterThan(0);
  });

  it("intersects stage, path, group, track and normalized search without revealing hidden routes", () => {
    const visible = projectGeminiSeries(full(), true);
    expect(filterVisibleGeminiLessons(visible, { stage: 2 })).toHaveLength(36);
    expect(filterVisibleGeminiLessons(visible, { stage: 1 })).toHaveLength(50);
    expect(filterVisibleGeminiLessons(visible, { stage: 2, track: "api" })).toHaveLength(6);
    expect(filterVisibleGeminiLessons(visible, { stage: 2, track: "api", group: "H", query: "Ｂａｔｃｈ" }).map(a => a.number)).toContain(85);
    for (const route of visible.paths) expect(filterVisibleGeminiLessons(visible, { path: route.id })).toHaveLength(route.articles.length);
    expect(filterVisibleGeminiLessons(projectGeminiSeries(full()), { path: curriculum.routes[0].id })).toEqual([]);
    expect(filterVisibleGeminiLessons(visible, { query: "nonexistent-example-xyz" })).toEqual([]);
  });

  it("refuses hidden hrefs, wrong kinds/locales and absent members", () => {
    const visible = projectGeminiSeries(full());
    expect(visibleGeminiHref(visible, curriculum.articles[0].slug)).toBeUndefined();
    expect(visibleGeminiHref(visible, visible.hubSlug)).toBe("/zh-TW/life/gemini-guide");
    expect(visibleGeminiHref(visible, base.articles[35].slug, "section-3")).toBe("/zh-TW/life/gemini-cli-gemini-md#section-3");
    expect(visibleGeminiMember(visible, base.articles[0].slug, "en", "life")).toBeUndefined();
    expect(visibleGeminiMember(visible, base.articles[0].slug, "zh-TW", "howto")).toBeUndefined();
    expect(visibleGeminiMember(visible, curriculum.articles[0].slug, "zh-TW", "life")).toBeUndefined();
  });
});
