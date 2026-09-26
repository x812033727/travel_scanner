import { NextRequest, NextResponse } from "next/server";
import { limitedRequestBody } from "@/lib/request-body";
import { problem } from "../../speech/forward";

/**
 * The video pipeline's media stages (docs/videos/DRAMA.md) reach apps/api/app/video_media
 * through here with a video tool token; nginx exposes only this web app. Generated files are
 * 10-40 MB clips, so the download route streams the API's body and passes byte ranges through
 * instead of buffering (the speech forwarder reads whole answers, which is fine for JSON and
 * a narration line, not for video). Only the token is forwarded, never cookies.
 */
type Context = { params: Promise<{ path: string[] }> };
type Method = "GET" | "POST" | "PUT";
export type Route = { kind: "json" | "upload" | "download"; maxBytes: number; timeoutMs: number };

const TOKEN = /^Bearer mkv_[A-Za-z0-9_-]{36,76}$/;
const SLUG = /^[a-z0-9](?:[a-z0-9-]{0,78}[a-z0-9])?$/;
const SHA256 = /^[0-9a-f]{64}$/;
const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/;
const RANGE = /^bytes=\d*-\d*$/;
// A part of an upload (PART_BYTES in apps/api/app/video_reviews/storage.py), under nginx's 6 MB.
export const PART_MAX_BYTES = 4 * 1024 * 1024;
const JSON_MAX_BYTES = 256 * 1024;
// A poll may run the vendor download inside the API; nginx allows 300 s for /api/.
const JOB_TIMEOUT_MS = 240_000;
const JUDGE_TIMEOUT_MS = 180_000;
const SUBMIT_TIMEOUT_MS = 90_000;
const SHORT_TIMEOUT_MS = 30_000;
const UPLOAD_TIMEOUT_MS = 60_000;
const JSON_HEADERS = ["content-type", "retry-after", "www-authenticate"];
const FILE_HEADERS = ["content-type", "content-length", "content-range", "accept-ranges", "etag", "last-modified"];

/** Which media route a path and method are, or null for anything else. */
export function mediaRoute(path: string[], method: Method): Route | null {
  const [head, ...rest] = path;
  const json = (timeoutMs: number): Route => ({ kind: "json", maxBytes: JSON_MAX_BYTES, timeoutMs });
  if (head === "status" && rest.length === 0 && method === "GET") return json(SHORT_TIMEOUT_MS);
  if ((head === "images" || head === "clips" || head === "music") && rest.length === 0 && method === "POST") return json(SUBMIT_TIMEOUT_MS);
  if (head === "judge" && rest.length === 0 && method === "POST") return json(JUDGE_TIMEOUT_MS);
  if (head === "jobs" && rest.length === 1 && UUID.test(rest[0]) && method === "GET") return json(JOB_TIMEOUT_MS);
  if (head === "files" && rest.length === 2 && SLUG.test(rest[0]) && SHA256.test(rest[1])) {
    if (method === "PUT") return { kind: "upload", maxBytes: PART_MAX_BYTES, timeoutMs: UPLOAD_TIMEOUT_MS };
    if (method === "GET") return { kind: "download", maxBytes: 0, timeoutMs: SHORT_TIMEOUT_MS };
  }
  return null;
}

/** The part, parts and size of an upload, digits only; null when any is missing or malformed. */
function partQuery(request: NextRequest): URLSearchParams | null {
  const query = new URLSearchParams();
  for (const name of ["part", "parts", "size"]) {
    const value = request.nextUrl.searchParams.get(name);
    if (!value || !/^\d{1,12}$/.test(value)) return null;
    query.set(name, value);
  }
  return query;
}

function passBack(upstream: Response, names: string[], extra: Record<string, string> = {}) {
  const headers = new Headers({ "Cache-Control": "no-store", ...extra });
  for (const name of names) {
    const value = upstream.headers.get(name);
    if (value) headers.set(name, value);
  }
  return headers;
}

async function forward(request: NextRequest, context: Context, method: Method) {
  const authorization = request.headers.get("authorization") ?? "";
  if (!TOKEN.test(authorization)) return problem(401, "video_tool_token_invalid", "a video tool token is required");
  const { path } = await context.params;
  const route = mediaRoute(path, method);
  if (!route) return problem(404, "video_media_route_unknown", "no such video media route");
  const query = route.kind === "upload" ? partQuery(request) : new URLSearchParams();
  if (!query) return problem(422, "video_media_bad_part", "an upload needs part, parts and size");
  let body: ArrayBuffer | undefined;
  if (method !== "GET") {
    try {
      body = (await limitedRequestBody(request, route.maxBytes)) ?? new ArrayBuffer(0);
    } catch {
      return problem(413, "video_media_request_too_large", "the request is too large; send files in parts");
    }
  }
  const headers = new Headers({ Authorization: authorization, Accept: route.kind === "download" ? "*/*" : "application/json" });
  if (body) headers.set("Content-Type", route.kind === "upload" ? "application/octet-stream" : "application/json");
  const range = request.headers.get("range");
  if (route.kind === "download" && range && RANGE.test(range)) headers.set("Range", range);
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), route.timeoutMs);
  let upstream: Response;
  try {
    const base = process.env.API_INTERNAL_URL || "http://localhost:8000";
    const suffix = query.size ? `?${query}` : "";
    upstream = await fetch(`${base}/api/v1/video/media/${path.join("/")}${suffix}`, {
      method,
      headers,
      body,
      cache: "no-store",
      redirect: "manual",
      signal: route.kind === "download" ? AbortSignal.any([controller.signal, request.signal]) : controller.signal,
    });
  } catch {
    clearTimeout(timeout);
    return problem(502, "upstream_unavailable", "the API is not answering");
  }
  if (route.kind !== "download") {
    try {
      return new NextResponse(await upstream.arrayBuffer(), { status: upstream.status, headers: passBack(upstream, JSON_HEADERS) });
    } catch {
      return problem(502, "upstream_unavailable", "the API is not answering");
    } finally {
      clearTimeout(timeout);
    }
  }
  // The deadline covers the answer's headers; the body streams for as long as the tool reads.
  clearTimeout(timeout);
  const out = passBack(upstream, FILE_HEADERS, { "X-Content-Type-Options": "nosniff" });
  if (!upstream.ok) {
    // An error answer is small JSON: pass it through, buffered, so the tool sees the code.
    return new NextResponse(await upstream.arrayBuffer(), { status: upstream.status, headers: passBack(upstream, JSON_HEADERS) });
  }
  out.set("Cache-Control", "private, no-store");
  return new Response(upstream.body, { status: upstream.status, headers: out });
}

export function GET(request: NextRequest, context: Context) {
  return forward(request, context, "GET");
}

export function POST(request: NextRequest, context: Context) {
  return forward(request, context, "POST");
}

export function PUT(request: NextRequest, context: Context) {
  return forward(request, context, "PUT");
}
