/** Local read-only publication fixture. It never imports into the application database. */
import { spawn } from "node:child_process";
import { createServer } from "node:http";
import { createRequire } from "node:module";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { inflateRawSync } from "node:zlib";

const root = new URL("../../../", import.meta.url);
const read = (path: string) => JSON.parse(readFileSync(new URL(path, root), "utf8"));
type Inline = { type: string; slug?: string; kind?: string; text?: string };
type Block = { type: string; text?: string; code?: string; inlines?: Inline[] };
type Pack = { slug: string; locales: { "zh-TW": { title: string; description: string; hero: unknown; sources: unknown[]; blocks: Block[] } } };
export const catalogue = read("api/app/guides/series_data/claude-code.json") as {
  slug: string; hub: string; groups: { id: string; title: string }[];
  paths: { id: string; title: string; slugs: string[] }[];
  entries: { slug: string; number: number; group: string; level: string; platforms: string[]; aliases: string[]; prerequisites: string[]; related: string[] }[];
};
export const packs = new Map<string, Pack>([catalogue.hub, ...catalogue.entries.map(e => e.slug)]
  .map(slug => [slug, read(`api/app/guides/content/${slug}.json`) as Pack]));
const reference = (slug: string) => ({ kind: "life", slug, title: packs.get(slug)!.locales["zh-TW"].title });
const entries = catalogue.entries.map(entry => ({
  ...entry, ...reference(entry.slug), description: packs.get(entry.slug)!.locales["zh-TW"].description,
  minutes: Math.max(1, Math.ceil(packs.get(entry.slug)!.locales["zh-TW"].blocks.reduce((n, b) => n + (b.text?.length ?? b.inlines?.reduce((v, i) => v + (i.text?.length ?? 0), 0) ?? 0), 0) / 450)),
}));
export const hubPath = `/zh-TW/life/${catalogue.hub}`;

export async function startPracticePreview() {
  const archive = readFileSync(new URL("web/public/tutorials/claude-code/complete.zip", root));
  const files = new Map<string, Buffer>();
  let offset = 0;
  while (archive.readUInt32LE(offset) === 0x04034b50) {
    const size = archive.readUInt32LE(offset + 18);
    const length = archive.readUInt16LE(offset + 26);
    const start = offset + 30 + length + archive.readUInt16LE(offset + 28);
    const name = archive.subarray(offset + 30, offset + 30 + length).toString("utf8");
    files.set(name.replace(/^complete\//, "/"), inflateRawSync(archive.subarray(start, start + size)));
    offset = start + size;
  }
  const server = createServer((req, res) => {
    const pathname = new URL(req.url || "/", "http://localhost").pathname;
    const key = pathname === "/" ? "/index.html" : pathname;
    const file = files.get(key);
    res.statusCode = file ? 200 : 404;
    res.setHeader("Content-Type", key.endsWith(".js") ? "text/javascript; charset=utf-8" : key.endsWith(".css") ? "text/css; charset=utf-8" : "text/html; charset=utf-8");
    res.end(file ?? "Not found");
  });
  await new Promise<void>(resolve => server.listen(0, "127.0.0.1", resolve));
  return { origin: `http://127.0.0.1:${(server.address() as { port: number }).port}`, stop: () => new Promise<void>(resolve => { server.closeAllConnections(); server.close(() => resolve()); }) };
}

export async function startSeriesPreview() {
  const state = { seriesAvailable: true };
  const upstream = createServer((req, res) => {
    req.resume();
    const url = new URL(req.url || "/", "http://127.0.0.1");
    let result: unknown = {};
    if (req.method !== "GET") { res.statusCode = 405; res.end(); return; }
    if (url.pathname === `/api/v1/guides/series/${catalogue.slug}`) {
      if (!state.seriesAvailable) res.statusCode = 503;
      result = state.seriesAvailable ? { slug: catalogue.slug, locale: "zh-TW", hub: reference(catalogue.hub), groups: catalogue.groups, paths: catalogue.paths, entries } : { detail: "Local fixture unavailable" };
    } else if (url.pathname.startsWith("/api/v1/guides/life/")) {
      const slug = url.pathname.split("/").at(-1)!;
      const pack = packs.get(slug);
      const locale = url.searchParams.get("locale") || "zh-TW";
      const visible = pack && locale === "zh-TW";
      const index = catalogue.entries.findIndex(e => e.slug === slug);
      const entry = catalogue.entries[index];
      result = { slug, kind: "life", locale, status: visible ? "published" : "unpublished", destination_id: null, destination_label: null,
        topics: [{ slug: "ai", label: "AI" }, { slug: "tutorial", label: "教學" }], valid_until: null, expired: false,
        published_locales: pack ? ["zh-TW"] : [],
        document: visible ? { ...pack.locales["zh-TW"], version: 1, published_at: "2026-09-14T00:00:00Z", modified_at: null } : null,
        article_links: visible ? Array.from(new Set(pack.locales["zh-TW"].blocks.flatMap(b => b.inlines?.filter(i => i.type === "article" && i.kind === "life" && packs.has(i.slug!)).map(i => i.slug!) ?? []))).map(reference) : [],
        series: visible ? { slug: catalogue.slug, hub: reference(catalogue.hub), current: index < 0 ? null : entries[index],
          previous: index > 0 ? reference(entries[index - 1].slug) : null,
          next: index >= 0 && index < entries.length - 1 ? reference(entries[index + 1].slug) : null,
          prerequisites: entry?.prerequisites.map(reference) ?? [], related: entry?.related.map(reference) ?? [] } : null,
      };
    } else if (url.pathname === "/api/v1/guides/topics") result = { topics: [{ slug: "ai", label: "AI", section: "life" }, { slug: "tutorial", label: "教學", section: "life" }] };
    else if (url.pathname === "/api/v1/guides") result = { articles: Array.from(packs.values()).slice(0, 12).map(pack => ({ ...reference(pack.slug), locale: "zh-TW", description: pack.locales["zh-TW"].description, hero: pack.locales["zh-TW"].hero, topics: [], destination_id: null, destination_label: null, valid_until: null, expired: false, published_at: "2026-09-14T00:00:00Z" })), next_cursor: null };
    else if (url.pathname === "/api/v1/runtime/site-visibility") result = Object.fromEntries(["hotspots", "trips", "alerts", "flight_status", "airline_fares", "pricing"].map(key => [`${key}_enabled`, true]));
    else if (url.pathname === "/api/v1/ads/config") result = { enabled: false, publisher_id: null, slot_id: null, cmp_enabled: false };
    else if (url.pathname === "/api/v1/analytics/config") result = { first_party_enabled: false, ga4_enabled: false };
    else if (["/api/v1/community/status", "/api/v1/discovery/status"].includes(url.pathname)) result = { enabled: false };
    else if (url.pathname.startsWith("/api/v1/runtime/ui-text")) result = { locale: "zh-TW", version: "local-preview", entries: {} };
    else if (url.pathname === "/api/v1/auth/me") { res.statusCode = 401; result = { detail: "anonymous preview" }; }
    res.setHeader("Content-Type", "application/json");
    res.setHeader("Cache-Control", "no-store");
    res.end(JSON.stringify(result));
  });
  await new Promise<void>(resolve => upstream.listen(0, "127.0.0.1", resolve));
  const probe = createServer();
  await new Promise<void>(resolve => probe.listen(0, "127.0.0.1", resolve));
  const port = (probe.address() as { port: number }).port;
  await new Promise<void>(resolve => probe.close(() => resolve()));
  const origin = `http://127.0.0.1:${port}`;
  const server = spawn(process.execPath, [createRequire(import.meta.url).resolve("next/dist/bin/next"), "start", "--hostname", "127.0.0.1", "--port", String(port)], {
    cwd: fileURLToPath(new URL("web/", root)), windowsHide: true, stdio: ["ignore", "pipe", "pipe"],
    env: { ...process.env, NODE_ENV: "production", API_INTERNAL_URL: `http://127.0.0.1:${(upstream.address() as { port: number }).port}`, NEXT_TELEMETRY_DISABLED: "1" },
  });
  let logs = "";
  server.stdout.on("data", chunk => { logs = (logs + chunk).slice(-10000); });
  server.stderr.on("data", chunk => { logs = (logs + chunk).slice(-10000); });
  const stop = async () => {
    server.kill();
    await new Promise<void>(resolve => { upstream.closeAllConnections(); upstream.close(() => resolve()); });
  };
  try {
    for (let attempt = 0; attempt < 60; attempt++) {
      try { if ((await fetch(origin + hubPath, { signal: AbortSignal.timeout(1000) })).ok) return { origin, state, stop, logs: () => logs }; } catch { /* bounded startup probe */ }
      if (server.exitCode !== null) throw new Error(logs);
      await new Promise(resolve => setTimeout(resolve, 500));
    }
    throw new Error(`Preview failed to start: ${logs}`);
  } catch (error) { await stop(); throw error; }
}
