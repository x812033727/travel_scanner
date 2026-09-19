import { beforeEach, describe, expect, it, vi } from "vitest";
import { disabledAdsense } from "@/lib/adsense";
import { fetchAdsenseConfig } from "@/lib/adsense-config";
import { ADS_TXT_FALLBACK_PUBLISHER_ID, adsTxtLine } from "./ads-txt";
import { dynamic, GET } from "./route";

vi.mock("@/lib/adsense-config", () => ({ fetchAdsenseConfig: vi.fn() }));

// Not the fallback account, so a line naming it can only have come from the configuration.
const configured = { enabled: true, publisher_id: "ca-pub-1234567890123456", slot_id: "1234567890", cmp_enabled: false };

async function served(): Promise<{ response: Response; text: string }> {
  const response = await GET();
  return { response, text: await response.text() };
}

describe("/ads.txt", () => {
  beforeEach(() => {
    vi.mocked(fetchAdsenseConfig).mockReset().mockResolvedValue(configured);
  });

  it("is read when a crawler asks, so a changed id needs no rebuild", () => {
    expect(dynamic).toBe("force-dynamic");
  });

  it("names the configured publisher in Google's line, with the stored ca- prefix dropped", async () => {
    const { response, text } = await served();
    expect(response.status).toBe(200);
    expect(response.headers.get("Content-Type")).toBe("text/plain; charset=utf-8");
    expect(text).toBe("google.com, pub-1234567890123456, DIRECT, f08c47fec0942fa0\n");
  });

  it("lets whatever sits between the crawler and this server keep the answer for an hour", async () => {
    expect((await GET()).headers.get("Cache-Control")).toBe("public, max-age=3600");
  });

  it.each([
    ["advertising is off or the API could not be reached", () => vi.mocked(fetchAdsenseConfig).mockResolvedValue(disabledAdsense)],
    ["the configured id is not Google's shape", () => vi.mocked(fetchAdsenseConfig).mockResolvedValue({ ...configured, publisher_id: "pub-1234567890123456" })],
    ["the read itself fails", () => vi.mocked(fetchAdsenseConfig).mockRejectedValue(new Error("hostile"))],
  ])("still names the verified account when %s, because silence would un-verify the site", async (_label, arrange) => {
    arrange();
    const { response, text } = await served();
    expect(response.status).toBe(200);
    expect(response.headers.get("Content-Type")).toBe("text/plain; charset=utf-8");
    expect(text).toBe(`${adsTxtLine(ADS_TXT_FALLBACK_PUBLISHER_ID)}\n`);
  });

  it("falls back to the account the checked-in file used to name, in Google's shape", () => {
    expect(ADS_TXT_FALLBACK_PUBLISHER_ID).toMatch(/^ca-pub-\d{16}$/);
    expect(adsTxtLine(ADS_TXT_FALLBACK_PUBLISHER_ID)).toBe("google.com, pub-4140966684432854, DIRECT, f08c47fec0942fa0");
  });
});
