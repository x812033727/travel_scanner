import { NextRequest, NextResponse } from "next/server";
import { forwardedClientAddress } from "@/app/api/travel/[...path]/proxy-security";

const locales = new Set(["en", "ja", "ko", "zh-TW", "zh-CN"]);

export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ locale: string; guideId: string }> },
) {
  const { locale, guideId } = await params;
  if (!locales.has(locale) || !/^[0-9a-f-]{36}$/i.test(guideId)) {
    return NextResponse.json({ code: "hotspot_guide_not_found" }, { status: 404 });
  }
  const base = process.env.API_INTERNAL_URL || "http://localhost:8000";
  const headers = new Headers({ "X-Travel-Locale": locale });
  // Only the session token travels upstream, never the browser's whole cookie jar; the client
  // address uses the same right-most-proxy rule as the main API proxy so it cannot be spoofed.
  const token = request.cookies.get("travel_access")?.value;
  if (token) headers.set("Authorization", `Bearer ${token}`);
  const userAgent = request.headers.get("user-agent")?.slice(0, 512);
  if (userAgent) headers.set("User-Agent", userAgent);
  const clientAddress = forwardedClientAddress(request.headers);
  if (clientAddress) headers.set("X-Travel-Client-IP", clientAddress);
  let response: Response;
  try {
    response = await fetch(`${base}/api/v1/hotspots/guides/${guideId}/open`, {
      method: "POST",
      headers,
      cache: "no-store",
    });
  } catch {
    return NextResponse.json({ code: "upstream_unavailable" }, { status: 502 });
  }
  if (!response.ok) {
    return NextResponse.json({ code: "hotspot_guide_not_found" }, { status: response.status });
  }
  const payload = await response.json() as { url?: unknown };
  if (typeof payload.url !== "string") {
    return NextResponse.json({ code: "unsafe_upstream_redirect" }, { status: 502 });
  }
  let target: URL;
  try {
    target = new URL(payload.url);
  } catch {
    return NextResponse.json({ code: "unsafe_upstream_redirect" }, { status: 502 });
  }
  if (target.protocol !== "https:" || target.username || target.password) {
    return NextResponse.json({ code: "unsafe_upstream_redirect" }, { status: 502 });
  }
  return NextResponse.redirect(target, 307);
}
