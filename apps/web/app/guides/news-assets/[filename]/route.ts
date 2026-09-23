import { NextRequest } from "next/server";

const SAFE_FILENAME = /^[a-z0-9][a-z0-9.-]{0,159}\.(?:webp|svg)$/;

type Context = { params: Promise<{ filename: string }> };

async function assetResponse(request: NextRequest, context: Context, head: boolean) {
  const { filename } = await context.params;
  if (!SAFE_FILENAME.test(filename)) return new Response(null, { status: 404 });
  const target = new URL(`/api/travel/news-assets/${encodeURIComponent(filename)}`, request.url);
  const upstream = await fetch(target, { cache: "no-store", signal: request.signal });
  const contentType = upstream.headers.get("content-type") || "";
  if (upstream.ok && !["image/webp", "image/svg+xml"].includes(contentType.split(";", 1)[0])) {
    return new Response(null, { status: 502 });
  }
  return new Response(head ? null : upstream.body, {
    status: upstream.status,
    headers: {
      "Content-Type": contentType,
      "Cache-Control": upstream.headers.get("cache-control") || "no-store",
      "ETag": upstream.headers.get("etag") || "",
      "X-Content-Type-Options": "nosniff",
    },
  });
}

export async function GET(request: NextRequest, context: Context) {
  return assetResponse(request, context, false);
}

export async function HEAD(request: NextRequest, context: Context) {
  return assetResponse(request, context, true);
}
