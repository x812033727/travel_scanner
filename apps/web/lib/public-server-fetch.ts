import { headers } from "next/headers";
import { cache } from "react";
import { forwardedClientHeaders } from "@/lib/client-address";

/**
 * Request headers for a server-side read of a public API endpoint.
 *
 * Server rendering reaches the API directly rather than through the BFF, so without
 * this the visitor's address never arrives and every rendered page looks like traffic
 * from the web container itself. That matters in one direction only: the API counts
 * reads per source, and a bucket shared by every visitor at once is either useless or
 * an outage, depending on where the threshold sits.
 *
 * Public reads only -- no cookies, no authorization, no account state. The address and
 * user agent are the whole payload, and both are copied exactly as the BFF sends them
 * so one source is one source however it reached us.
 *
 * Not for fetches that set `next.revalidate`: a per-visitor header would split a shared
 * cache entry into one per reader, and a route that calls `headers()` cannot be rendered
 * statically at all.
 */
export const publicServerHeaders = cache(async (locale: string): Promise<Record<string, string>> => {
  const incoming = await headers();
  const forwarded: Record<string, string> = {
    Accept: "application/json",
    "X-Travel-Locale": locale,
  };
  Object.assign(forwarded, forwardedClientHeaders(incoming));
  const agent = incoming.get("user-agent")?.slice(0, 512);
  if (agent) forwarded["X-Travel-User-Agent"] = agent;
  return forwarded;
});
