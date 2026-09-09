import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { SiteInformationPage, siteInformationMetadata } from "./site-information-page";
import { getSitePageCopy } from "@/lib/site-pages.server";
import { sitePageLocales } from "@/lib/site-pages";

vi.mock("@/components/site-header", () => ({ SiteHeader: () => null }));
vi.mock("next-intl/server", () => ({ getTranslations: () => { throw new Error("General UI-text is not a publication channel"); } }));
afterEach(() => { cleanup(); vi.unstubAllGlobals(); });

describe("publication-only public information", () => {
  it.each(sitePageLocales)("uses immutable bundled status text in %s, never general UI overrides", async (locale) => {
    vi.stubGlobal("fetch", vi.fn(async () => new Response(JSON.stringify({ slug: "privacy", locale, status: "unpublished", document: null }))));
    const copy = await getSitePageCopy(locale);
    render(await SiteInformationPage({ slug: "privacy", locale }));
    expect(screen.getByRole("status").textContent).toBe(copy.unpublished);
    expect(await siteInformationMetadata("privacy", locale)).toMatchObject({ title: copy.privacy, description: copy.unpublished, robots: { index: false } });
  });

  it("never falls back to another locale's public labels", async () => {
    await expect(getSitePageCopy("invalid")).rejects.toThrow("Unsupported site-page locale");
  });

  it("renders only the published content and fixed factual labels", async () => {
    const document = { title: "Published title", description: "Published summary", blocks: [{ type: "paragraph", text: "Approved body" }], requirements: { operator: "Verified operator", contact: "", location: "", retention: "", legal: "" }, effective_date: "2026-09-09", version: 2, published_at: "2026-09-09T00:00:00Z" };
    vi.stubGlobal("fetch", vi.fn(async () => new Response(JSON.stringify({ slug: "privacy", locale: "en", status: "published", document }))));
    render(await SiteInformationPage({ slug: "privacy", locale: "en" }));
    expect(screen.getByText("Approved body")).toBeTruthy();
    expect(screen.getByText((await getSitePageCopy("en")).operator)).toBeTruthy();
    expect(await siteInformationMetadata("privacy", "en")).toMatchObject({ title: document.title, description: document.description });
  });
});
