import { readFile } from "node:fs/promises";
import { join } from "node:path";
import { ImageResponse } from "next/og";
import { NextResponse } from "next/server";
import type { Locale } from "@/i18n/routing";
import {
  ARTICLE_OG_HEIGHT,
  ARTICLE_OG_WIDTH,
  clampCardText,
  hasNonLatinScript,
  headlineFontSize,
  loadSubsetFont,
} from "@/lib/article-og";

const STATIC_OG_PATH = join(process.cwd(), "public", "og.png");

let fallbackOgBytes: Promise<Buffer> | null = null;
function readFallbackOg(): Promise<Buffer> {
  fallbackOgBytes ??= readFile(STATIC_OG_PATH);
  return fallbackOgBytes;
}

export type EditorialOgCardInput = {
  locale: Locale;
  title: string;
  description?: string | null;
  badge: string;
  meta?: string | null;
};

/**
 * Shared 1200x630 editorial Open Graph / Google Discover card renderer used by articles,
 * destination guides, and topic hubs.
 *
 * Falls back cleanly to the static brand `/og.png` when non-Latin text requires a subsetted
 * font that cannot be fetched in time, so social scrapers never receive tofu glyphs.
 */
export async function renderEditorialOgCard(input: EditorialOgCardInput): Promise<Response> {
  const title = clampCardText(input.title, 76);
  const description = input.description ? clampCardText(input.description, 128) : "";
  const badge = clampCardText(input.badge || "MOKAAIR", 32);
  const meta = input.meta ? clampCardText(input.meta, 40) : "";
  const cardText = `${title} ${description} ${badge} ${meta} Mokaair mokaair.com`;
  const needsCustomFont = hasNonLatinScript(cardText);
  const font = needsCustomFont ? await loadSubsetFont(input.locale, cardText) : null;

  if (needsCustomFont && !font) {
    try {
      const png = await readFallbackOg();
      return new NextResponse(new Uint8Array(png), {
        headers: {
          "Content-Type": "image/png",
          "Cache-Control": "public, max-age=300",
        },
      });
    } catch {
      return new NextResponse("unavailable", { status: 503 });
    }
  }

  const fontSize = headlineFontSize(title);
  const fontFamily = font ? `"${font.name}", sans-serif` : "sans-serif";

  return new ImageResponse(
    (
      <div
        style={{
          width: "100%",
          height: "100%",
          display: "flex",
          flexDirection: "column",
          justifyContent: "space-between",
          padding: "56px 64px",
          background: "linear-gradient(135deg, #092026 0%, #0f343d 55%, #164852 100%)",
          color: "#f8fafc",
          fontFamily,
        }}
      >
        <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", width: "100%" }}>
          <div style={{ display: "flex", alignItems: "center", gap: "16px" }}>
            <div
              style={{
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                padding: "10px 22px",
                borderRadius: "999px",
                background: "rgba(20, 184, 166, 0.2)",
                border: "2px solid rgba(45, 212, 191, 0.65)",
                color: "#99f6e4",
                fontSize: "24px",
                fontWeight: 700,
              }}
            >
              {badge}
            </div>
            {meta ? (
              <div style={{ display: "flex", color: "#94a3b8", fontSize: "22px", fontWeight: 700 }}>
                {meta}
              </div>
            ) : null}
          </div>
          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: "10px",
              color: "#5eead4",
              fontSize: "28px",
              fontWeight: 700,
              letterSpacing: "0.06em",
            }}
          >
            MOKAAIR
          </div>
        </div>

        <div style={{ display: "flex", flexDirection: "column", gap: "24px", maxWidth: "1060px" }}>
          <div
            style={{
              display: "flex",
              fontSize: `${fontSize}px`,
              fontWeight: 700,
              lineHeight: 1.24,
              color: "#ffffff",
            }}
          >
            {title}
          </div>
          {description ? (
            <div
              style={{
                display: "flex",
                fontSize: "26px",
                fontWeight: 700,
                lineHeight: 1.45,
                color: "#cbd5e1",
              }}
            >
              {description}
            </div>
          ) : null}
        </div>

        <div
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            width: "100%",
            borderTop: "1px solid rgba(148, 163, 184, 0.3)",
            paddingTop: "22px",
            color: "#94a3b8",
            fontSize: "22px",
            fontWeight: 700,
          }}
        >
          <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
            <div style={{ width: "12px", height: "12px", borderRadius: "999px", background: "#f97316" }} />
            <span>mokaair.com</span>
          </div>
          <span>{input.locale}</span>
        </div>
      </div>
    ),
    {
      width: ARTICLE_OG_WIDTH,
      height: ARTICLE_OG_HEIGHT,
      ...(font ? { fonts: [{ name: font.name, data: font.data, style: "normal", weight: 700 }] } : {}),
      headers: {
        "Cache-Control": "public, max-age=3600, s-maxage=86400, stale-while-revalidate=604800",
      },
    },
  );
}
