import { afterEach, describe, expect, it, vi } from "vitest";
import { generateMetadata } from "./destination-services-page";

vi.mock("next-intl/server", () => ({
  getTranslations: async () => (key: string) => key,
}));

afterEach(() => {
  vi.unstubAllGlobals();
});

/** The catalog lookup only supplies the city's display name; an unreachable API falls back
 *  to the id, which is all these assertions need. */
function withCatalog(items: { id: string; city: string }[] | null) {
  vi.stubGlobal(
    "fetch",
    vi.fn(async () =>
      items
        ? ({ ok: true, json: async () => ({ items }) } as unknown as Response)
        : ({ ok: false, json: async () => ({}) } as unknown as Response),
    ),
  );
}

describe("destination services metadata", () => {
  it("tells crawlers not to index the page, but to follow it", async () => {
    // Every city gets the same template with its name in the title and nothing else, so
    // Search Console collected 23 of these as duplicates whose declared canonical Google
    // overrode. `follow` keeps the outbound lodging links, which are the page's purpose.
    withCatalog([{ id: "hiroshima", city: "廣島" }]);
    const meta = await generateMetadata({
      params: Promise.resolve({ locale: "zh-TW" as const, destinationId: "hiroshima" }),
    });
    expect(meta.robots).toEqual({ index: false, follow: true });
  });

  it("says the same thing for every city and locale", async () => {
    withCatalog(null);
    for (const [locale, destinationId] of [
      ["ja", "sapporo"],
      ["en", "kaohsiung"],
      ["ko", "nagoya"],
    ] as const) {
      const meta = await generateMetadata({ params: Promise.resolve({ locale, destinationId }) });
      expect(meta.robots).toEqual({ index: false, follow: true });
    }
  });
});
