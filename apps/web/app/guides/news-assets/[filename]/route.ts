import { NextRequest } from "next/server";
import { forwardedClientHeaders } from "@/lib/client-address";

/**
 * The artwork the hourly news pipeline generates (hero, social card, diagram), served under
 * the site's own path so an article's plain `<img>` never leaves the origin.
 *
 * The bytes live in the API (`/api/v1/news-assets/<file>`, app/news_automation/router.py),
 * reached at `API_INTERNAL_URL` like every other server-side read. The upstream used to be
 * derived from `request.url`, which behind nginx is an https URL on this server's
 * plain-HTTP port: the fetch failed with ERR_SSL_WRONG_VERSION_NUMBER and every news image
 * answered 500.
 */

const SAFE_FILENAME = /^[a-z0-9][a-z0-9.-]{0,159}\.(?:webp|svg)$/;
const IMAGE_TYPES = new Set(["image/webp", "image/svg+xml"]);
// The API serves nothing larger (MAX_PUBLIC_ASSET_BYTES in app/news_automation/assets.py).
const MAX_ASSET_BYTES = 5 * 1024 * 1024;
const UPSTREAM_TIMEOUT_MS = 15_000;

type Context = { params: Promise<{ filename: string }> };

function empty(status: number) {
  return new Response(null, {
    status,
    headers: { "Cache-Control": "no-store", "X-Content-Type-Options": "nosniff" },
  });
}

/** Lets go of a body this route will not read; a stream that already failed has nothing to free. */
async function discard(response: Response) {
  await response.body?.cancel().catch(() => undefined);
}

/** The whole body, or null as soon as it is longer than `maxBytes`, however it was labelled. */
async function boundedBody(response: Response, maxBytes: number): Promise<Uint8Array<ArrayBuffer> | null> {
  if (Number(response.headers.get("content-length") || 0) > maxBytes) {
    await discard(response);
    return null;
  }
  if (!response.body) return new Uint8Array();
  const reader = response.body.getReader();
  const chunks: Uint8Array[] = [];
  let size = 0;
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    size += value.byteLength;
    if (size > maxBytes) {
      await reader.cancel();
      return null;
    }
    chunks.push(value);
  }
  const body = new Uint8Array(size);
  let offset = 0;
  for (const chunk of chunks) {
    body.set(chunk, offset);
    offset += chunk.byteLength;
  }
  return body;
}

async function assetResponse(request: NextRequest, context: Context, head: boolean) {
  const { filename } = await context.params;
  if (!SAFE_FILENAME.test(filename)) return empty(404);
  const base = process.env.API_INTERNAL_URL || "http://localhost:8000";
  // The API meters public reads per visitor; without the forwarded address every image
  // would count as the web container's own traffic.
  const headers = new Headers(forwardedClientHeaders(request.headers));
  const userAgent = request.headers.get("user-agent")?.slice(0, 512);
  if (userAgent) headers.set("X-Travel-User-Agent", userAgent);
  let upstream: Response;
  try {
    // Always a GET: the API route answers GET only, so a HEAD goes through the same checks
    // and its body is dropped below.
    upstream = await fetch(`${base}/api/v1/news-assets/${encodeURIComponent(filename)}`, {
      headers,
      cache: "no-store",
      redirect: "manual",
      signal: AbortSignal.any([AbortSignal.timeout(UPSTREAM_TIMEOUT_MS), request.signal]),
    });
  } catch {
    return empty(502);
  }
  if (!upstream.ok) {
    await discard(upstream);
    // A missing or withdrawn asset is the API's 404 and stays one; a redirect is not
    // something this route follows.
    return empty(upstream.status >= 400 ? upstream.status : 502);
  }
  const contentType = upstream.headers.get("content-type")?.split(";", 1)[0]?.trim().toLowerCase() || "";
  if (!IMAGE_TYPES.has(contentType)) {
    await discard(upstream);
    return empty(502);
  }
  let body: Uint8Array<ArrayBuffer> | null;
  try {
    body = await boundedBody(upstream, MAX_ASSET_BYTES);
  } catch {
    return empty(502);
  }
  if (!body) return empty(502);
  const out = new Headers({
    "Content-Type": contentType,
    "Cache-Control": upstream.headers.get("cache-control") || "no-store",
    "X-Content-Type-Options": "nosniff",
  });
  const etag = upstream.headers.get("etag");
  if (etag) out.set("ETag", etag);
  return new Response(head ? null : body, { status: upstream.status, headers: out });
}

export async function GET(request: NextRequest, context: Context) {
  return assetResponse(request, context, false);
}

export async function HEAD(request: NextRequest, context: Context) {
  return assetResponse(request, context, true);
}
