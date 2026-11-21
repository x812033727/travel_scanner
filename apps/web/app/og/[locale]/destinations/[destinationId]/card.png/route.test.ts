// @vitest-environment node
import { beforeEach, describe, expect, it, vi } from "vitest";
import { GET } from "./route";

const mocks = vi.hoisted(() => ({
  getDestination: vi.fn(),
  loadSubsetFont: vi.fn(),
}));

vi.mock("@/lib/destinations.server", () => ({
  getDestination: mocks.getDestination,
}));
vi.mock("@/lib/article-og", async (original) => ({
  ...await original<typeof import("@/lib/article-og")>(),
  loadSubsetFont: mocks.loadSubsetFont,
}));

beforeEach(() => {
  mocks.getDestination.mockReset();
  mocks.loadSubsetFont.mockReset().mockResolvedValue(null);
});

describe("/og/[locale]/destinations/[destinationId]/card.png", () => {
  it("renders a PNG card for a known public destination", async () => {
    mocks.getDestination.mockResolvedValue({
      id: "tokyo",
      city: "Tokyo",
      country: "Japan",
      localName: null,
      reason: "Dense rail transit and neighborhoods for every style of trip.",
    });

    const response = await GET(new Request("https://mokaair.com/og/en/destinations/tokyo/card.png"), {
      params: Promise.resolve({ locale: "en", destinationId: "tokyo" }),
    });

    expect(response.status).toBe(200);
    expect(response.headers.get("Content-Type")).toContain("image/png");
    const bytes = new Uint8Array(await response.arrayBuffer());
    expect(bytes.slice(0, 4)).toEqual(new Uint8Array([0x89, 0x50, 0x4e, 0x47]));
  });

  it("returns 404 for unknown locales or destinations", async () => {
    const unknown = await GET(new Request("https://mokaair.com/og/en/destinations/atlantis/card.png"), {
      params: Promise.resolve({ locale: "en", destinationId: "atlantis" }),
    });
    expect(unknown.status).toBe(404);

    const badLocale = await GET(new Request("https://mokaair.com/og/fr/destinations/tokyo/card.png"), {
      params: Promise.resolve({ locale: "fr", destinationId: "tokyo" }),
    });
    expect(badLocale.status).toBe(404);
  });
});
