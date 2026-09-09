import "server-only";

import { cookies } from "next/headers";
import { normalizeAdminBootstrap, type AdminBootstrap } from "@/lib/admin-operations";

export type AdminBootstrapResult =
  | { status: "ready"; data: AdminBootstrap }
  | { status: "signed_out" }
  | { status: "forbidden" }
  | { status: "unavailable" };

export async function loadAdminBootstrap(): Promise<AdminBootstrapResult> {
  const jar = await cookies();
  const token = jar.get("travel_access")?.value;
  if (!token) return { status: "signed_out" };
  const base = (process.env.API_INTERNAL_URL || "http://localhost:8000").replace(/\/$/, "");
  try {
    const response = await fetch(`${base}/api/v1/admin/bootstrap`, {
      cache: "no-store",
      // This is an authorization probe, not a browser session call. Bearer mode
      // intentionally prevents the API from sliding a cookie the server layout
      // cannot relay; HeaderSessionProvider renews the active browser session.
      headers: { Accept: "application/json", Authorization: `Bearer ${token}` },
      signal: AbortSignal.timeout(6_000),
    });
    if (response.status === 401) return { status: "signed_out" };
    if (response.status === 403) return { status: "forbidden" };
    if (!response.ok) return { status: "unavailable" };
    const data = normalizeAdminBootstrap(await response.json());
    return data ? { status: "ready", data } : { status: "unavailable" };
  } catch {
    return { status: "unavailable" };
  }
}
