import { describe, expect, it } from "vitest";
import enAuth from "./messages/en/auth.json";
import enHotspots from "./messages/en/hotspots.json";
import enMetadata from "./messages/en/metadata.json";
import jaAuth from "./messages/ja/auth.json";
import jaHotspots from "./messages/ja/hotspots.json";
import jaMetadata from "./messages/ja/metadata.json";
import koAuth from "./messages/ko/auth.json";
import koHotspots from "./messages/ko/hotspots.json";
import koMetadata from "./messages/ko/metadata.json";
import zhCNAuth from "./messages/zh-CN/auth.json";
import zhCNHotspots from "./messages/zh-CN/hotspots.json";
import zhCNMetadata from "./messages/zh-CN/metadata.json";
import zhTWAuth from "./messages/zh-TW/auth.json";
import zhTWHotspots from "./messages/zh-TW/hotspots.json";
import zhTWMetadata from "./messages/zh-TW/metadata.json";

const publicBrandCatalogs = [
  enAuth, enHotspots, enMetadata,
  jaAuth, jaHotspots, jaMetadata,
  koAuth, koHotspots, koMetadata,
  zhCNAuth, zhCNHotspots, zhCNMetadata,
  zhTWAuth, zhTWHotspots, zhTWMetadata,
];

function relativeLuminance(hex: string): number {
  const channels = hex.match(/[a-f\d]{2}/gi)?.map((value) => Number.parseInt(value, 16) / 255) ?? [];
  const [red = 0, green = 0, blue = 0] = channels.map((value) =>
    value <= 0.04045 ? value / 12.92 : ((value + 0.055) / 1.055) ** 2.4,
  );
  return 0.2126 * red + 0.7152 * green + 0.0722 * blue;
}

function contrastRatio(foreground: string, background: string): number {
  const lighter = Math.max(relativeLuminance(foreground), relativeLuminance(background));
  const darker = Math.min(relativeLuminance(foreground), relativeLuminance(background));
  return (lighter + 0.05) / (darker + 0.05);
}

describe("Mokaair public branding", () => {
  it("uses Mokaair in all localized brand catalogs", () => {
    for (const catalog of publicBrandCatalogs) {
      const serialized = JSON.stringify(catalog);
      expect(serialized).toContain("Mokaair");
      expect(serialized).not.toContain("Travel Scanner");
    }
  });

  it("keeps the product name as one word with a capital M", () => {
    for (const metadata of [enMetadata, jaMetadata, koMetadata, zhCNMetadata, zhTWMetadata]) {
      expect(metadata.title).toContain("Mokaair");
      expect(metadata.title).not.toContain("Moka air");
    }
  });

  it("keeps both wordmark colors readable on the cream brand background", () => {
    expect(contrastRatio("#6B4A3A", "#F7F1E8")).toBeGreaterThanOrEqual(4.5);
    expect(contrastRatio("#0D6B68", "#F7F1E8")).toBeGreaterThanOrEqual(4.5);
  });
});
