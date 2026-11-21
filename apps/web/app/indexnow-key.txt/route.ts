import { NextResponse } from "next/server";

/**
 * `/indexnow-key.txt` -- proves domain ownership for IndexNow instant indexing notifications
 * sent to Bing, Yahoo Taiwan, Naver, DuckDuckGo, and ChatGPT Search.
 *
 * Served dynamically from `INDEXNOW_KEY` (same runtime pattern as `/ads.txt` and `/llms.txt`)
 * so rotating or enabling the key needs no Docker image rebuild. Returns 404 when unconfigured.
 */
export const dynamic = "force-dynamic";

const INDEXNOW_KEY_PATTERN = /^[A-Za-z0-9-]{8,128}$/;

const HEADERS = {
  "Content-Type": "text/plain; charset=utf-8",
  "Cache-Control": "public, max-age=3600",
} as const;

function configuredIndexNowKey(): string | null {
  const raw = (process.env.INDEXNOW_KEY ?? "").trim();
  return INDEXNOW_KEY_PATTERN.test(raw) ? raw : null;
}

export async function GET(): Promise<Response> {
  const key = configuredIndexNowKey();
  if (!key) return new NextResponse("not found", { status: 404 });
  return new Response(key, { status: 200, headers: HEADERS });
}

export async function HEAD(): Promise<Response> {
  const key = configuredIndexNowKey();
  if (!key) return new NextResponse(null, { status: 404 });
  return new Response(null, { status: 200, headers: HEADERS });
}
