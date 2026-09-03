import { NextRequest, NextResponse } from "next/server";

const locales = new Set(["en", "ja", "ko", "zh-TW", "zh-CN"]);

export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ locale: string; hotspotId: string }> },
) {
  const { locale, hotspotId } = await params;
  if (!locales.has(locale) || !/^[0-9a-f-]{36}$/i.test(hotspotId)) {
    return NextResponse.json({ code: "hotspot_source_not_found" }, { status: 404 });
  }
  const base = process.env.API_INTERNAL_URL || "http://localhost:8000";
  const headers = new Headers({ "X-Travel-Locale": locale });
  // Only the session token travels upstream, never the browser's whole cookie jar.
  const token = request.cookies.get("travel_access")?.value;
  if (token) headers.set("Authorization", `Bearer ${token}`);
  let response: Response;
  try {
    response = await fetch(`${base}/api/v1/hotspots/${hotspotId}/source`, {
      headers,
      cache: "no-store",
    });
  } catch {
    return NextResponse.json({ code: "upstream_unavailable" }, { status: 502 });
  }
  if (!response.ok) {
    return NextResponse.json({ code: "hotspot_source_not_found" }, { status: response.status });
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
