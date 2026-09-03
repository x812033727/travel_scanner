import { randomBytes } from "node:crypto";
import { NextRequest, NextResponse } from "next/server";
import { normalizeLocale } from "@/i18n/routing";
import { safeNextPath } from "@/lib/navigation";
import {
  apiUrl,
  authHeaders,
  encodeFlowCookie,
  flowCookieName,
  isOAuthProvider,
} from "../../_shared";

export async function GET(
  request: NextRequest,
  context: { params: Promise<{ provider: string }> },
) {
  const { provider } = await context.params;
  if (!isOAuthProvider(provider)) return NextResponse.json({ error: "not_found" }, { status: 404 });
  const intent = request.nextUrl.searchParams.get("intent") === "link" ? "link" : "login";
  const locale = normalizeLocale(request.nextUrl.searchParams.get("locale"));
  const next = safeNextPath(request.nextUrl.searchParams.get("next"));
  const binding = randomBytes(32).toString("base64url");
  let upstream: Response;
  try {
    const headers = authHeaders(request);
    if (intent !== "link") headers.delete("Authorization");
    upstream = await fetch(apiUrl(`auth/oauth/${provider}/start`), {
      method: "POST",
      headers,
      body: JSON.stringify({ intent, locale, next_path: next, browser_binding: binding }),
      cache: "no-store",
      signal: AbortSignal.timeout(10_000),
    });
  } catch {
    return NextResponse.redirect(new URL(`/${locale}/login?oauth_error=oauth_provider_unavailable`, request.url));
  }
  const payload = await upstream.json().catch(() => ({})) as {
    authorization_url?: string;
    flow_id?: string;
    state?: string;
    expires_in?: number;
    code?: string;
  };
  if (!upstream.ok || !payload.authorization_url || !payload.flow_id || !payload.state) {
    const target = intent === "link" ? `/${locale}/account` : `/${locale}/login`;
    const url = new URL(target, request.url);
    url.searchParams.set("oauth_error", payload.code || "oauth_provider_unavailable");
    return NextResponse.redirect(url);
  }
  const response = NextResponse.redirect(payload.authorization_url);
  const secureCookie = process.env.NODE_ENV === "production" || request.nextUrl.protocol === "https:";
  response.cookies.set(
    flowCookieName(provider),
    encodeFlowCookie({
      flowId: payload.flow_id,
      state: payload.state,
      binding,
      locale,
      next,
      intent,
    }),
    {
      httpOnly: true,
      secure: secureCookie,
      sameSite: provider === "apple" && secureCookie ? "none" : "lax",
      path: `/api/auth/oauth/${provider}`,
      maxAge: Math.min(payload.expires_in || 600, 1800),
    },
  );
  return response;
}
