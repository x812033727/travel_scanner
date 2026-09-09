import { cookies } from "next/headers";
import { NextRequest, NextResponse } from "next/server";
import { RequestBodyError, limitedRequestBody } from "@/lib/request-body";
import { hotelClickoutErrorPage } from "@/lib/hotel-clickout-error";
import {
  forwardedClientAddress,
  isAllowedMutationOrigin,
  observedRequestOrigin,
  safeRedirectLocation,
  validateProxyPath,
} from "./proxy-security";
import { preserveRequestId } from "./request-id";
import { forwardedAnalyticsSession, renewedSession, stepUpSession, upstreamLocale } from "./proxy-context";

type Context = { params: Promise<{ path: string[] }> };
const MAX_REQUEST_BYTES = Number(process.env.API_PROXY_MAX_BODY_BYTES || 5 * 1024 * 1024);
const MAX_RESPONSE_BYTES = Number(process.env.API_PROXY_MAX_RESPONSE_BYTES || 10 * 1024 * 1024);
const UPSTREAM_TIMEOUT_MS = Number(process.env.API_PROXY_TIMEOUT_MS || 15_000);
function upstreamTimeout(endpoint: string): number {
  if (endpoint === "community/translations") return Math.max(UPSTREAM_TIMEOUT_MS, 45_000);
  if (/^community\/media\/[0-9a-f-]+\/complete$/.test(endpoint)) return Math.max(UPSTREAM_TIMEOUT_MS, 60_000);
  return UPSTREAM_TIMEOUT_MS;
}
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
  const query = new URLSearchParams(request.nextUrl.search);
  const isHotelClickout = /^travel-services\/[a-f0-9-]+\/hotel-links\/[a-z_]+\/clickout$/.test(endpoint);
  const isOptionClickout = /^travel-services\/[a-f0-9-]+\/booking-options\/[a-f0-9-]+\/clickout$/.test(endpoint);
  const isServiceClickout = isHotelClickout || isOptionClickout || /^affiliates\/(?:offers|destination-offers)\/[a-f0-9-]+\/clickout$/.test(endpoint);
  const formLocale = isServiceClickout ? query.get("locale") : null;
  if (isServiceClickout) query.delete("locale");
  // First-party error recovery context must never reach the API/affiliate URL.
  if (isOptionClickout) query.delete("return_to");
  const url = `${base}/api/v1/${endpoint}${query.size ? `?${query}` : ""}`;
  const jar = await cookies();
  const token = jar.get("travel_access")?.value;
  const stepUpToken = jar.get("admin_step_up")?.value;
  const localeCookie = jar.get("travel_locale")?.value;
  const headers = new Headers();
  const contentType = request.headers.get("content-type");
  if (contentType) headers.set("Content-Type", contentType);
  // Sent as a cookie rather than a bearer header on purpose. The API only slides a
  // session forward for cookie callers — bearer clients are expected to manage their own
  // tokens — so forwarding it as Authorization meant the renewal never ran and every
  // session died exactly one token lifetime after sign-in.
  const upstreamCookies = [token ? `travel_access=${token}` : "", stepUpToken ? `admin_step_up=${stepUpToken}` : ""].filter(Boolean);
  if (upstreamCookies.length) headers.set("Cookie", upstreamCookies.join("; "));
  headers.set("X-Travel-Locale", upstreamLocale(request.headers.get("x-travel-locale") || formLocale, localeCookie));
  for (const name of ["idempotency-key", "last-event-id"]) {
    const value = request.headers.get(name);
    if (value) headers.set(name, value);
  }
  const requestId = request.headers.get("x-request-id");
  if (requestId && /^[A-Za-z0-9._:-]{1,128}$/.test(requestId)) {
    headers.set("X-Request-ID", requestId);
  }
  const sourceAddress = forwardedClientAddress(request.headers);
  if (sourceAddress) headers.set("X-Travel-Client-IP", sourceAddress);
  const userAgent = request.headers.get("user-agent")?.slice(0, 512);
  if (userAgent) headers.set("X-Travel-User-Agent", userAgent);
  const analyticsSession = forwardedAnalyticsSession(request.headers.get("x-travel-analytics-session"));
  if (analyticsSession) headers.set("X-Travel-Analytics-Session", analyticsSession);
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
  const browserClickout = isOptionClickout && request.method === "POST" && request.headers.get("accept")?.includes("text/html");
  const failure = (status: number, code: string, detail: string) => browserClickout
    ? hotelClickoutErrorPage({
      requestUrl: request.url, referrer: request.headers.get("referer"),
      locale: headers.get("X-Travel-Locale") || "zh-TW", body, contentType, status,
    })
    : problem(status, code, detail);
  if (request.method !== "GET" && request.method !== "HEAD") {
    try {
      // Counts the stream as it arrives, so a chunked or mislabelled upload cannot be buffered in
      // full before the limit applies.
      body = await limitedRequestBody(request, isOptionClickout ? Math.min(4096, MAX_REQUEST_BYTES) : MAX_REQUEST_BYTES);
    } catch (error) {
      if (error instanceof RequestBodyError && error.reason === "invalid_length") {
        return failure(400, "invalid_content_length", "Content-Length 標頭無效");
      }
      return failure(413, "request_too_large", "請求內容超過允許大小");
    }
  }
  const controller = new AbortController();
  const verifyOffer = isHotelClickout || /^admin\/travel-services\/(offers|products|destination-offers)\/[a-f0-9-]+\/(?:booking-options\/[a-f0-9-]+\/)?review$/.test(endpoint) || endpoint === "admin/travel-services/destination-offers/batch-review";
  const quoteSearch = /^travel-services\/[a-f0-9-]+\/hotel-quotes$/.test(endpoint);
  const timeout = setTimeout(() => controller.abort(), verifyOffer ? Math.max(45_000, UPSTREAM_TIMEOUT_MS) : quoteSearch ? Math.max(30_000, UPSTREAM_TIMEOUT_MS) : upstreamTimeout(endpoint));
  let upstream: Response;
  try {
    upstream = await fetch(url, {
      method: request.method,
      headers,
      body,
      cache: "no-store",
      redirect: "manual",
      signal: AbortSignal.any([controller.signal, request.signal]),
    });
  } catch {
    clearTimeout(timeout);
    return failure(502, "upstream_unavailable", "API 服務目前無法回應");
  }
  const redirectLocation = upstream.headers.get("location");
  if (upstream.status >= 300 && upstream.status < 400 && redirectLocation) {
    clearTimeout(timeout);
    const location = safeRedirectLocation(redirectLocation, request.nextUrl.origin);
    if (!location) return failure(502, "unsafe_upstream_redirect", "API 回傳了不安全的轉址");
    return preserveRequestId(new Response(null, {
      status: upstream.status,
      headers: { Location: location, "Cache-Control": "no-store", "Referrer-Policy": "no-referrer" },
    }), upstream);
  }
  if (upstream.headers.get("content-type")?.includes("text/event-stream")) {
    // Server-sent events stay open by design, so the upstream deadline only covered the headers.
    clearTimeout(timeout);
    return preserveRequestId(new Response(upstream.body, { status: upstream.status, headers: { "Content-Type": "text/event-stream", "Cache-Control": "private, no-store", "X-Accel-Buffering": "no" } }), upstream);
  }
  let text: string;
  try {
    // The same deadline now also bounds reading the response body, not just the headers.
    text = await limitedResponseText(upstream);
  } catch {
    if (controller.signal.aborted) return failure(504, "upstream_timeout", "API 服務回應逾時");
    return failure(502, "upstream_response_too_large", "API 回應超過允許大小");
  } finally {
    clearTimeout(timeout);
  }
  if (browserClickout) {
    // A successful booking clickout is a redirect, never provider JSON/HTML.
    return preserveRequestId(failure(upstream.status, "hotel_link_unavailable", "訂房連結目前無法開啟"), upstream);
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
    return preserveRequestId(response, upstream);
  }
  const elevated = endpoint === "admin/step-up" && upstream.ok ? stepUpSession(upstream) : null;
  const response = upstream.status === 204
    ? new NextResponse(null, { status: 204 })
    : typeof payload === "string"
      ? new NextResponse(payload, { status: upstream.status })
      : NextResponse.json(payload, { status: upstream.status });
  response.headers.set("Cache-Control", "no-store");
  if (elevated) {
    response.cookies.set("admin_step_up", elevated.token, {
      httpOnly: true,
      secure: process.env.NODE_ENV === "production",
      sameSite: "strict",
      path: "/api/travel/admin",
      maxAge: elevated.maxAge,
    });
  }
  if (endpoint === "auth/logout" || (endpoint === "auth/me" && upstream.status === 401) ||
      (["auth/reset-password", "auth/delete-account"].includes(endpoint) && upstream.ok)) {
    response.cookies.delete("travel_access");
    response.cookies.set("admin_step_up", "", {
      httpOnly: true,
      secure: process.env.NODE_ENV === "production",
      sameSite: "strict",
      path: "/api/travel/admin",
      maxAge: 0,
    });
  } else {
    // This proxy owns the browser cookie, so a session the API just slid forward only
    // reaches the browser if the new token is re-issued here.
    const renewed = renewedSession(upstream);
    if (renewed) {
      response.cookies.set("travel_access", renewed.token, {
        httpOnly: true,
        secure: process.env.NODE_ENV === "production",
        sameSite: "lax",
        path: "/",
        maxAge: renewed.maxAge,
      });
    }
  }
  return preserveRequestId(response, upstream);
}

export const GET = proxy;
export const POST = proxy;
export const PUT = proxy;
export const PATCH = proxy;
export const DELETE = proxy;
