import { cookies } from "next/headers";
import { NextRequest, NextResponse } from "next/server";

type Context = { params: Promise<{ path: string[] }> };

async function proxy(request: NextRequest, context: Context) {
  const { path } = await context.params;
  const endpoint = path.join("/");
  const base = process.env.API_INTERNAL_URL || "http://localhost:8000";
  const url = `${base}/api/v1/${endpoint}${request.nextUrl.search}`;
  const jar = await cookies();
  const token = jar.get("travel_access")?.value;
  const headers = new Headers();
  const contentType = request.headers.get("content-type");
  if (contentType) headers.set("Content-Type", contentType);
  if (token) headers.set("Authorization", `Bearer ${token}`);
  for (const name of ["idempotency-key", "last-event-id"]) {
    const value = request.headers.get(name);
    if (value) headers.set(name, value);
  }
  const upstream = await fetch(url, {
    method: request.method,
    headers,
    body: request.method === "GET" || request.method === "HEAD" ? undefined : await request.text(),
    cache: "no-store",
    redirect: "manual",
  });
  const redirectLocation = upstream.headers.get("location");
  if (upstream.status >= 300 && upstream.status < 400 && redirectLocation) {
    return new Response(null, {
      status: upstream.status,
      headers: { Location: redirectLocation },
    });
  }
  if (upstream.headers.get("content-type")?.includes("text/event-stream")) {
    return new Response(upstream.body, { status: upstream.status, headers: { "Content-Type": "text/event-stream", "Cache-Control": "no-cache", "X-Accel-Buffering": "no" } });
  }
  const text = await upstream.text();
  let payload: unknown = text;
  try { payload = text ? JSON.parse(text) : null; } catch { /* preserve text */ }
  if (payload && typeof payload === "object" && "access_token" in payload && typeof payload.access_token === "string") {
    const accessToken = payload.access_token;
    delete payload.access_token;
    const response = NextResponse.json(payload, { status: upstream.status });
    response.cookies.set("travel_access", accessToken, { httpOnly: true, secure: process.env.NODE_ENV === "production", sameSite: "lax", path: "/", maxAge: 60 * 60 * 24 * 7 });
    return response;
  }
  const response = upstream.status === 204
    ? new NextResponse(null, { status: 204 })
    : typeof payload === "string"
      ? new NextResponse(payload, { status: upstream.status })
      : NextResponse.json(payload, { status: upstream.status });
  if (endpoint === "auth/logout") response.cookies.delete("travel_access");
  return response;
}

export const GET = proxy;
export const POST = proxy;
export const PUT = proxy;
export const DELETE = proxy;
