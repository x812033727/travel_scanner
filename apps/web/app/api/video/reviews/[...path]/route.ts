import { NextRequest, NextResponse } from "next/server";
import { limitedRequestBody } from "@/lib/request-body";
import { problem } from "../../speech/forward";

/**
 * The local video pipeline reports a video, uploads its previews and submits reviews for
 * /admin/videos through here, with its video tool token; the API is not exposed by nginx.
 * Only the three routes the pipeline uses are forwarded, and only the token, never cookies.
 */
type Context = { params: Promise<{ path: string[] }> };
const TOKEN = /^Bearer mkv_[A-Za-z0-9_-]{36,76}$/;
const SLUG = /^[a-z0-9](?:[a-z0-9-]{0,78}[a-z0-9])?$/;
const SHA256 = /^[0-9a-f]{64}$/;
// A preview goes up in parts of 4 MiB (PART_BYTES in apps/api/app/video_reviews/storage.py),
// under nginx's 6 MB request cap and the API's 5 MiB.
export const PART_MAX_BYTES = 4 * 1024 * 1024;
const JSON_MAX_BYTES = 512 * 1024;
const TIMEOUT_MS = 60_000;
const PASSED_BACK = ["content-type", "retry-after", "www-authenticate"];

type Route = { kind: "project" | "review" | "file"; maxBytes: number };

/** Which pipeline route a path and method are, or null for anything else. */
export function reviewRoute(path: string[], method: string): Route | null {
  const [slug, ...rest] = path;
  if (!slug || !SLUG.test(slug)) return null;
  if (rest.length === 0 && (method === "GET" || method === "PUT")) return { kind: "project", maxBytes: JSON_MAX_BYTES };
  if (rest.length === 1 && rest[0] === "reviews" && method === "POST") return { kind: "review", maxBytes: JSON_MAX_BYTES };
  if (rest.length === 2 && rest[0] === "files" && SHA256.test(rest[1]) && method === "PUT") return { kind: "file", maxBytes: PART_MAX_BYTES };
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

async function forward(request: NextRequest, context: Context, method: "GET" | "PUT" | "POST") {
  const authorization = request.headers.get("authorization") ?? "";
  if (!TOKEN.test(authorization)) return problem(401, "video_tool_token_invalid", "a video tool token is required");
  const { path } = await context.params;
  const route = reviewRoute(path, method);
  if (!route) return problem(404, "video_review_route_unknown", "no such video review route");
  const query = route.kind === "file" ? partQuery(request) : new URLSearchParams();
  if (!query) return problem(422, "video_review_bad_part", "an upload needs part, parts and size");
  let body: ArrayBuffer | undefined;
  if (method !== "GET") {
    try {
      body = (await limitedRequestBody(request, route.maxBytes)) ?? new ArrayBuffer(0);
    } catch {
      return problem(413, "video_review_part_too_large", "the request is too large; send the file in parts");
    }
  }
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), TIMEOUT_MS);
  try {
    const base = process.env.API_INTERNAL_URL || "http://localhost:8000";
    const suffix = query.size ? `?${query}` : "";
    const upstream = await fetch(`${base}/api/v1/video/reviews/${path.join("/")}${suffix}`, {
      method,
      headers: {
        Authorization: authorization,
        Accept: "application/json",
        ...(body ? { "Content-Type": route.kind === "file" ? "application/octet-stream" : "application/json" } : {}),
      },
      body,
      cache: "no-store",
      signal: controller.signal,
    });
    const headers = new Headers({ "Cache-Control": "no-store" });
    for (const name of PASSED_BACK) {
      const value = upstream.headers.get(name);
      if (value) headers.set(name, value);
    }
    return new NextResponse(await upstream.arrayBuffer(), { status: upstream.status, headers });
  } catch {
    return problem(502, "upstream_unavailable", "the API is not answering");
  } finally {
    clearTimeout(timeout);
  }
}

export function GET(request: NextRequest, context: Context) {
  return forward(request, context, "GET");
}

export function PUT(request: NextRequest, context: Context) {
  return forward(request, context, "PUT");
}

export function POST(request: NextRequest, context: Context) {
  return forward(request, context, "POST");
}
