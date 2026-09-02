import { cookies } from "next/headers";
import { NextRequest, NextResponse } from "next/server";
import {
  forwardedClientAddress,
  isAllowedMutationOrigin,
  observedRequestOrigin,
  safeRedirectLocation,
  validateProxyPath,
} from "./proxy-security";

type Context = { params: Promise<{ path: string[] }> };
const MAX_REQUEST_BYTES = Number(process.env.API_PROXY_MAX_BODY_BYTES || 5 * 1024 * 1024);
const MAX_RESPONSE_BYTES = Number(process.env.API_PROXY_MAX_RESPONSE_BYTES || 10 * 1024 * 1024);
const UPSTREAM_TIMEOUT_MS = Number(process.env.API_PROXY_TIMEOUT_MS || 15_000);
const SUPPORTED_LOCALES = new Set(["en", "ja", "ko", "zh-TW", "zh-CN"]);

function problem(status: number, code: string, detail: string) {
  return NextResponse.json(
    { title: "請求未完成", status, code, detail },
    { status, headers: { "Cache-Control": "no-store" } },
  );
}

async function limitedResponseText(response: Response): Promise<string> {
  const declared = Number(response.headers.get("content-length") || 0);
  if (Number.isFinite(declared) && declared > MAX_RESPONSE_BYTES) {
    throw new Error("upstream_response_too_large");
  }
  if (!response.body) return "";
  const reader = response.body.getReader();
  const chunks: Uint8Array[] = [];
  let size = 0;
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    size += value.byteLength;
    if (size > MAX_RESPONSE_BYTES) {
      await reader.cancel();
      throw new Error("upstream_response_too_large");
    }
    chunks.push(value);
  }
  const result = new Uint8Array(size);
  let offset = 0;
  for (const chunk of chunks) {
    result.set(chunk, offset);
    offset += chunk.byteLength;
  }
  return new TextDecoder().decode(result);
}

async function proxy(request: NextRequest, context: Context) {
  const { path } = await context.params;
  const endpoint = validateProxyPath(path);
  if (!endpoint) return problem(400, "invalid_proxy_path", "API 路徑格式不正確");
  const requestOrigin = observedRequestOrigin(request.headers, request.nextUrl.origin);
  if (!isAllowedMutationOrigin(
    request.method,
    request.headers.get("origin"),
    requestOrigin,
    process.env.NEXT_PUBLIC_SITE_URL,
  )) {
    return problem(403, "cross_site_request_blocked", "不允許跨網站修改資料");
  }
  const base = process.env.API_INTERNAL_URL || "http://localhost:8000";
  const url = `${base}/api/v1/${endpoint}${request.nextUrl.search}`;
  const jar = await cookies();
  const token = jar.get("travel_access")?.value;
  const localeCookie = jar.get("travel_locale")?.value;
  const headers = new Headers();
  const contentType = request.headers.get("content-type");
  if (contentType) headers.set("Content-Type", contentType);
  if (token) headers.set("Authorization", `Bearer ${token}`);
  headers.set("X-Travel-Locale", SUPPORTED_LOCALES.has(localeCookie || "") ? localeCookie! : "zh-TW");
  for (const name of ["idempotency-key", "last-event-id"]) {
    const value = request.headers.get(name);
    if (value) headers.set(name, value);
  }
  const sourceAddress = forwardedClientAddress(request.headers);
  if (sourceAddress) headers.set("X-Travel-Client-IP", sourceAddress);
  const userAgent = request.headers.get("user-agent")?.slice(0, 512);
  if (userAgent) headers.set("X-Travel-User-Agent", userAgent);
  for (const name of ["sec-gpc", "dnt"]) {
    const value = request.headers.get(name);
    if (value === "1") headers.set(name, "1");
  }
  const trustedCountryHeader = process.env.ANALYTICS_COUNTRY_HEADER?.trim().toLowerCase();
  if (trustedCountryHeader) {
    const country = request.headers.get(trustedCountryHeader)?.trim().toUpperCase();
    if (country && /^[A-Z]{2}$/.test(country)) headers.set("X-Travel-Country", country);
  }
  let body: ArrayBuffer | undefined;
  if (request.method !== "GET" && request.method !== "HEAD") {
    const declared = Number(request.headers.get("content-length") || 0);
    if (Number.isFinite(declared) && declared > MAX_REQUEST_BYTES) {
      return problem(413, "request_too_large", "請求內容超過允許大小");
    }
    body = await request.arrayBuffer();
    if (body.byteLength > MAX_REQUEST_BYTES) {
      return problem(413, "request_too_large", "請求內容超過允許大小");
    }
  }
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), UPSTREAM_TIMEOUT_MS);
  let upstream: Response;
  try {
    upstream = await fetch(url, {
      method: request.method,
      headers,
      body,
      cache: "no-store",
      redirect: "manual",
      signal: controller.signal,
    });
  } catch {
    return problem(502, "upstream_unavailable", "API 服務目前無法回應");
  } finally {
    clearTimeout(timeout);
  }
  const redirectLocation = upstream.headers.get("location");
  if (upstream.status >= 300 && upstream.status < 400 && redirectLocation) {
    const location = safeRedirectLocation(redirectLocation, request.nextUrl.origin);
    if (!location) return problem(502, "unsafe_upstream_redirect", "API 回傳了不安全的轉址");
    return new Response(null, {
      status: upstream.status,
      headers: { Location: location, "Cache-Control": "no-store" },
    });
  }
  if (upstream.headers.get("content-type")?.includes("text/event-stream")) {
    return new Response(upstream.body, { status: upstream.status, headers: { "Content-Type": "text/event-stream", "Cache-Control": "no-cache", "X-Accel-Buffering": "no" } });
  }
  let text: string;
  try {
    text = await limitedResponseText(upstream);
  } catch {
    return problem(502, "upstream_response_too_large", "API 回應超過允許大小");
  }
  let payload: unknown = text;
  try { payload = text ? JSON.parse(text) : null; } catch { /* preserve text */ }
  if (payload && typeof payload === "object" && "access_token" in payload && typeof payload.access_token === "string") {
    const accessToken = payload.access_token;
    const expiresInValue = "expires_in" in payload ? payload.expires_in : undefined;
    const expiresIn = typeof expiresInValue === "number" && expiresInValue > 0
      ? Math.min(expiresInValue, 60 * 60 * 24 * 30)
      : 60 * 60;
    delete payload.access_token;
    const response = NextResponse.json(payload, { status: upstream.status });
    response.headers.set("Cache-Control", "no-store");
    response.cookies.set("travel_access", accessToken, { httpOnly: true, secure: process.env.NODE_ENV === "production", sameSite: "lax", path: "/", maxAge: expiresIn });
    const preferredLocale = "user" in payload && payload.user && typeof payload.user === "object" && "preferred_locale" in payload.user
      ? payload.user.preferred_locale
      : undefined;
    if (typeof preferredLocale === "string" && SUPPORTED_LOCALES.has(preferredLocale)) {
      response.cookies.set("travel_locale", preferredLocale, { sameSite: "lax", path: "/", maxAge: 31_536_000 });
    }
    return response;
  }
  const response = upstream.status === 204
    ? new NextResponse(null, { status: 204 })
    : typeof payload === "string"
      ? new NextResponse(payload, { status: upstream.status })
      : NextResponse.json(payload, { status: upstream.status });
  response.headers.set("Cache-Control", "no-store");
  if (endpoint === "auth/logout" || (endpoint === "auth/me" && upstream.status === 401)) {
    response.cookies.delete("travel_access");
  }
  return response;
}

export const GET = proxy;
export const POST = proxy;
export const PUT = proxy;
export const PATCH = proxy;
export const DELETE = proxy;
