import { cookies } from "next/headers";
import { NextRequest, NextResponse } from "next/server";
import { forwardedClientHeaders } from "@/lib/client-address";

/**
 * A preview on /admin/videos (a 720p cut, the narration, the contact sheet), streamed from the
 * API with the admin's session. The generic /api/travel proxy reads a response as text and caps
 * it at 10 MiB, which breaks video; this route passes the bytes and the byte ranges through so
 * the player can seek without downloading the whole file. The API checks content.read.
 */
type Context = { params: Promise<{ slug: string; sha256: string }> };
const SLUG = /^[a-z0-9](?:[a-z0-9-]{0,78}[a-z0-9])?$/;
const SHA256 = /^[0-9a-f]{64}$/;
const RANGE = /^bytes=\d*-\d*$/;
const PASSED_BACK = ["content-type", "content-length", "content-range", "accept-ranges", "last-modified", "etag"];
const TIMEOUT_MS = 30_000;

function problem(status: number, code: string) {
  return NextResponse.json({ status, code }, { status, headers: { "Cache-Control": "no-store" } });
}

export async function GET(request: NextRequest, context: Context) {
  const { slug, sha256 } = await context.params;
  if (!SLUG.test(slug) || !SHA256.test(sha256)) return problem(404, "video_review_file_not_found");
  const jar = await cookies();
  const session = jar.get("travel_access")?.value;
  if (!session) return problem(401, "authentication_required");
  const stepUp = jar.get("admin_step_up")?.value;
  const headers = new Headers({
    Cookie: [`travel_access=${session}`, stepUp ? `admin_step_up=${stepUp}` : ""].filter(Boolean).join("; "),
  });
  const range = request.headers.get("range");
  if (range && RANGE.test(range)) headers.set("Range", range);
  for (const [name, value] of Object.entries(forwardedClientHeaders(request.headers))) headers.set(name, value);
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), TIMEOUT_MS);
  let upstream: Response;
  try {
    const base = process.env.API_INTERNAL_URL || "http://localhost:8000";
    upstream = await fetch(`${base}/api/v1/admin/videos/${slug}/files/${sha256}`, {
      headers,
      cache: "no-store",
      redirect: "manual",
      signal: AbortSignal.any([controller.signal, request.signal]),
    });
  } catch {
    clearTimeout(timeout);
    return problem(502, "upstream_unavailable");
  }
  // The deadline covers the answer's headers; the body streams for as long as the player reads.
  clearTimeout(timeout);
  const out = new Headers({ "Cache-Control": "private, no-store", "X-Content-Type-Options": "nosniff" });
  for (const name of PASSED_BACK) {
    const value = upstream.headers.get(name);
    if (value) out.set(name, value);
  }
  if (!upstream.ok) {
    await upstream.body?.cancel();
    return problem(upstream.status, "video_review_file_unavailable");
  }
  return new Response(upstream.body, { status: upstream.status, headers: out });
}
