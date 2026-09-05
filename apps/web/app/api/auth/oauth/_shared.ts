import { NextRequest, NextResponse } from "next/server";
import { locales, normalizeLocale, type Locale } from "@/i18n/routing";
import { safeNextPath } from "@/lib/navigation";
import { limitedRequestBody, RequestBodyError } from "@/lib/request-body";
import { forwardedClientAddress } from "@/app/api/travel/[...path]/proxy-security";

// An OAuth form_post callback carries a code, a state and possibly an error string —
// a few hundred bytes. The route is unauthenticated, so it must never buffer an
// arbitrarily large body the way `request.formData()` does.
const MAX_CALLBACK_BODY_BYTES = 16 * 1024;

export const oauthProviders = ["google", "line", "apple"] as const;
export type OAuthProvider = (typeof oauthProviders)[number];

type FlowCookie = {
  flowId: string;
  state: string;
  binding: string;
  locale: Locale;
  next: string;
  intent: "login" | "link";
};

export function isOAuthProvider(value: string): value is OAuthProvider {
  return oauthProviders.includes(value as OAuthProvider);
}

export function flowCookieName(provider: OAuthProvider) {
  return `travel_oauth_${provider}`;
}

export function encodeFlowCookie(value: FlowCookie) {
  return Buffer.from(JSON.stringify(value)).toString("base64url");
}

export function decodeFlowCookie(value: string | undefined): FlowCookie | null {
  if (!value) return null;
  try {
    const parsed = JSON.parse(Buffer.from(value, "base64url").toString("utf8")) as FlowCookie;
    if (!parsed.flowId || !parsed.state || !parsed.binding || !parsed.locale) return null;
    return parsed;
  } catch {
    return null;
  }
}

export function apiUrl(path: string) {
  const base = process.env.API_INTERNAL_URL || "http://localhost:8000";
  return `${base}/api/v1/${path}`;
}

export function authHeaders(request: NextRequest) {
  const headers = new Headers({ "Content-Type": "application/json" });
  const token = request.cookies.get("travel_access")?.value;
  if (token) headers.set("Authorization", `Bearer ${token}`);
  const sourceAddress = forwardedClientAddress(request.headers);
  if (sourceAddress) headers.set("X-Travel-Client-IP", sourceAddress);
  return headers;
}

export function localizedPath(locale: Locale, nextPath: string) {
  const safe = safeNextPath(nextPath);
  if (locales.some((item) => safe === `/${item}` || safe.startsWith(`/${item}/`))) return safe;
  return safe === "/" ? `/${locale}` : `/${locale}${safe}`;
}

const safeErrorCodes = new Set([
  "oauth_cancelled",
  "oauth_state_invalid",
  "oauth_nonce_invalid",
  "oauth_token_invalid",
  "oauth_email_required",
  "oauth_account_exists",
  "oauth_identity_conflict",
  "oauth_identity_revoked",
  "oauth_provider_unavailable",
  "oauth_link_session_invalid",
  "registration_closed",
  "admin_email_reserved",
]);

export function errorRedirect(
  request: NextRequest,
  flow: FlowCookie | null,
  code: string,
) {
  const locale = normalizeLocale(flow?.locale || request.cookies.get("travel_locale")?.value);
  const next = safeNextPath(flow?.next || "/");
  const target = flow?.intent === "link" ? `/${locale}/account` : `/${locale}/login`;
  const url = new URL(target, request.nextUrl.origin);
  url.searchParams.set("oauth_error", safeErrorCodes.has(code) ? code : "oauth_token_invalid");
  url.searchParams.set("next", next);
  const response = NextResponse.redirect(url);
  for (const provider of oauthProviders) response.cookies.delete(flowCookieName(provider));
  return response;
}

export async function callback(request: NextRequest, providerValue: string) {
  if (!isOAuthProvider(providerValue)) return NextResponse.json({ error: "not_found" }, { status: 404 });
  const flow = decodeFlowCookie(request.cookies.get(flowCookieName(providerValue))?.value);
  let code: string | null;
  let state: string | null;
  let providerError: string | null;
  if (request.method === "POST") {
    let body: ArrayBuffer | undefined;
    try {
      body = await limitedRequestBody(request, MAX_CALLBACK_BODY_BYTES);
    } catch (error) {
      if (error instanceof RequestBodyError) {
        return errorRedirect(request, flow, "oauth_token_invalid");
      }
      throw error;
    }
    // form_post responses are application/x-www-form-urlencoded per the OAuth spec.
    const form = new URLSearchParams(new TextDecoder().decode(body ?? new ArrayBuffer(0)));
    code = form.get("code");
    state = form.get("state");
    providerError = form.get("error");
  } else {
    code = request.nextUrl.searchParams.get("code");
    state = request.nextUrl.searchParams.get("state");
    providerError = request.nextUrl.searchParams.get("error");
  }
  if (providerError) return errorRedirect(request, flow, "oauth_cancelled");
  if (!flow || !code || !state || state !== flow.state) {
    return errorRedirect(request, flow, "oauth_state_invalid");
  }
  let upstream: Response;
  try {
    upstream = await fetch(apiUrl(`auth/oauth/${providerValue}/exchange`), {
      method: "POST",
      headers: (() => {
        const headers = authHeaders(request);
        if (flow.intent !== "link") headers.delete("Authorization");
        return headers;
      })(),
      body: JSON.stringify({
        flow_id: flow.flowId,
        state,
        code,
        browser_binding: flow.binding,
      }),
      cache: "no-store",
      signal: AbortSignal.timeout(20_000),
    });
  } catch {
    return errorRedirect(request, flow, "oauth_provider_unavailable");
  }
  const payload = await upstream.json().catch(() => ({})) as {
    access_token?: string;
    expires_in?: number;
    code?: string;
    new_account?: boolean;
    user?: { preferred_locale?: string };
  };
  if (!upstream.ok || !payload.access_token) {
    return errorRedirect(request, flow, payload.code || "oauth_token_invalid");
  }
  const locale = normalizeLocale(payload.user?.preferred_locale || flow.locale);
  const response = NextResponse.redirect(
    new URL(localizedPath(locale, flow.next), request.nextUrl.origin),
  );
  const secureCookie = process.env.NODE_ENV === "production" || request.nextUrl.protocol === "https:";
  response.cookies.set("travel_access", payload.access_token, {
    httpOnly: true,
    secure: secureCookie,
    sameSite: "lax",
    path: "/",
    maxAge: Math.min(payload.expires_in || 3600, 60 * 60 * 24 * 30),
  });
  response.cookies.set("travel_locale", locale, {
    secure: secureCookie,
    sameSite: "lax",
    path: "/",
    maxAge: 60 * 60 * 24 * 365,
  });
  if (payload.new_account) {
    response.cookies.set("travel_oauth_registered", "1", {
      secure: secureCookie,
      sameSite: "lax",
      path: "/",
      maxAge: 300,
    });
  }
  response.cookies.delete(flowCookieName(providerValue));
  return response;
}
