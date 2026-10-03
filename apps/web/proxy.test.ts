import { readdirSync } from "node:fs";
import path from "node:path";
import { unstable_doesMiddlewareMatch } from "next/experimental/testing/server";
import { describe, expect, it, vi } from "vitest";
import { config } from "./proxy";

// Only the exported matcher is under test; next-intl's middleware does not load outside Next.
vi.mock("next-intl/middleware", () => ({ default: () => () => undefined }));

const runs = (url: string) => unstable_doesMiddlewareMatch({ config, url });

/**
 * One file per extension under public/, so a new kind of static file cannot slip past this.
 * Case-sensitive on purpose: the matcher is, so `.JPG` would need its own entry there.
 */
function publicSamples(): string[] {
  const root = path.join(import.meta.dirname, "public");
  const byExtension = new Map<string, string>();
  for (const entry of readdirSync(root, { recursive: true, withFileTypes: true })) {
    if (!entry.isFile()) continue;
    const extension = path.extname(entry.name);
    if (!byExtension.has(extension)) {
      const file = path.relative(root, path.join(entry.parentPath, entry.name));
      byExtension.set(extension, `/${file.split(path.sep).join("/")}`);
    }
  }
  return [...byExtension.values()];
}

describe("proxy matcher", () => {
  it("runs on every document, including a dotted path that only exists as a 404", () => {
    for (const url of [
      "/", "/zh-TW", "/en/explore", "/zh-TW/admin/users",
      // The [...rest] 404 document mounts the whole provider tree and the third-party
      // scripts, so it needs the nonce and the enforced script-src as much as any page.
      "/zh-TW/no-such.page", "/en/guides/travel/v1.2", "/no-such.page",
    ]) {
      expect(runs(url), url).toBe(true);
    }
  });

  it("skips the API, Next's own assets and every static file the site serves", () => {
    const files = [
      ...publicSamples(),
      // app/ metadata files and dotted route handlers: next-intl must never prefix these.
      "/favicon.ico", "/icon.svg", "/apple-icon.png", "/robots.txt", "/manifest.webmanifest",
      "/ads.txt", "/llms.txt", "/feed.xml", "/sitemap.xml", "/sitemaps/sitemap/travel-zh-TW-0.xml",
      "/guides/news-assets/0123456789abcdef-hero.webp",
      // Apple fetches its association files here, one of them with no extension at all.
      "/.well-known/apple-app-site-association", "/.well-known/apple-developer-domain-association.txt",
    ];
    expect(files.length).toBeGreaterThan(15);
    for (const url of [...files, "/api/travel/auth/me", "/_next/static/chunks/main.js", "/_next/image", "/_vercel/insights/view"]) {
      expect(runs(url), url).toBe(false);
    }
  });
});
