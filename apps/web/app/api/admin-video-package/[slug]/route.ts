import { cookies } from "next/headers";
import { NextRequest, NextResponse } from "next/server";
import { forwardedClientHeaders } from "@/lib/client-address";

/**
 * A manual upload package as one zip: the API stores every review file the page names
 * (`file=<sha256>:<name>`, repeated) into an archive and streams it. Like /api/admin-video-files,
 * this route passes the bytes through, since the generic /api/travel proxy reads a response as
 * text and caps it at 10 MiB. The zip is built as it streams, so there are no byte ranges. The
 * API checks content.manage and names the archive in Content-Disposition.
 *
 * With `check=1` the route asks the API's `/package` instead and answers its JSON: whether the zip
 * can be made, and each file it would miss with why. The page asks this first, because a download
 * that fails at its first byte only shows the browser's "failed" (2026-11-04, daily-ai-20261103).
 */
type Context = { params: Promise<{ slug: string }> };
const SLUG = /^[a-z0-9](?:[a-z0-9-]{0,78}[a-z0-9])?$/;
const ENTRY = /^[0-9a-f]{64}:[A-Za-z0-9][A-Za-z0-9._-]{0,79}$/;
const MAX_ENTRIES = 64;
const PASSED_BACK = ["content-type", "content-disposition", "last-modified"];
const TIMEOUT_MS = 30_000;

function problem(status: number, code: string) {
  return NextResponse.json({ status, code }, { status, headers: { "Cache-Control": "no-store" } });
}

export async function GET(request: NextRequest, context: Context) {
  const { slug } = await context.params;
  if (!SLUG.test(slug)) return problem(404, "video_package_not_found");
  const entries = request.nextUrl.searchParams.getAll("file");
  if (entries.length === 0 || entries.length > MAX_ENTRIES || entries.some((entry) => !ENTRY.test(entry) || entry.includes(".."))) return problem(422, "video_package_entries_invalid");
  const jar = await cookies();
  const session = jar.get("travel_access")?.value;
  if (!session) return problem(401, "authentication_required");
  const stepUp = jar.get("admin_step_up")?.value;
  const headers = new Headers({
    Cookie: [`travel_access=${session}`, stepUp ? `admin_step_up=${stepUp}` : ""].filter(Boolean).join("; "),
  });
  for (const [name, value] of Object.entries(forwardedClientHeaders(request.headers))) headers.set(name, value);
  const query = new URLSearchParams(entries.map((entry) => ["file", entry]));
  const check = request.nextUrl.searchParams.get("check") === "1";
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), TIMEOUT_MS);
  let upstream: Response;
  try {
    const base = process.env.API_INTERNAL_URL || "http://localhost:8000";
    upstream = await fetch(`${base}/api/v1/admin/videos/${slug}/${check ? "package" : "package.zip"}?${query}`, {
      headers,
      cache: "no-store",
      redirect: "manual",
      signal: AbortSignal.any([controller.signal, request.signal]),
    });
  } catch {
    clearTimeout(timeout);
    return problem(502, "upstream_unavailable");
  }
  // The deadline covers the answer's headers; the archive streams for as long as the download runs.
  clearTimeout(timeout);
  const out = new Headers({ "Cache-Control": "private, no-store", "X-Content-Type-Options": "nosniff" });
  for (const name of PASSED_BACK) {
    const value = upstream.headers.get(name);
    if (value) out.set(name, value);
  }
  if (check && upstream.ok) {
    const answer: unknown = await upstream.json().catch(() => null);
    if (!answer || typeof answer !== "object") return problem(502, "upstream_unavailable");
    return NextResponse.json(answer, { headers: { "Cache-Control": "private, no-store" } });
  }
  if (!upstream.ok) {
    await upstream.body?.cancel();
    return problem(upstream.status, upstream.status === 401 || upstream.status === 403 ? "video_package_forbidden" : "video_package_unavailable");
  }
  return new Response(upstream.body, { status: upstream.status, headers: out });
}
