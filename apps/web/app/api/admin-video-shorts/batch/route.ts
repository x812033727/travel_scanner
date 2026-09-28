import { cookies } from "next/headers";
import { NextRequest, NextResponse } from "next/server";
import { forwardedClientHeaders } from "@/lib/client-address";

/**
 * The Shorts the owner uploads to YouTube Studio themselves, as one archive
 * (docs/videos/SHORTS.md, the section on what happens before the API audit passes). The API puts
 * the files of the coming days together, each under the name the site later looks for on the
 * channel, and this route passes the bytes through with the admin's session: the generic
 * /api/travel proxy reads a response as text and caps it at 10 MiB. The API checks
 * content.manage and names the file in Content-Disposition.
 */
const PASSED_BACK = ["content-type", "content-length", "content-disposition", "last-modified", "etag"];
// The API copies the files into the archive before it answers, which takes longer than a header.
const TIMEOUT_MS = 120_000;

function problem(status: number, code: string) {
  return NextResponse.json({ status, code }, { status, headers: { "Cache-Control": "no-store" } });
}

export async function GET(request: NextRequest) {
  const jar = await cookies();
  const session = jar.get("travel_access")?.value;
  if (!session) return problem(401, "authentication_required");
  const stepUp = jar.get("admin_step_up")?.value;
  const headers = new Headers({
    Cookie: [`travel_access=${session}`, stepUp ? `admin_step_up=${stepUp}` : ""].filter(Boolean).join("; "),
  });
  for (const [name, value] of Object.entries(forwardedClientHeaders(request.headers))) headers.set(name, value);
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), TIMEOUT_MS);
  let upstream: Response;
  try {
    const base = process.env.API_INTERNAL_URL || "http://localhost:8000";
    upstream = await fetch(`${base}/api/v1/admin/video-shorts/uploads/batch.zip`, {
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
  if (!upstream.ok) {
    await upstream.body?.cancel();
    // A refusal of the caller is not the batch being empty, and neither is the API being away.
    const refused = upstream.status === 401 || upstream.status === 403;
    return problem(upstream.status, refused ? "video_shorts_batch_forbidden" : upstream.status === 404 ? "video_shorts_nothing_to_upload" : "video_shorts_batch_unavailable");
  }
  return new Response(upstream.body, { status: upstream.status, headers: out });
}
