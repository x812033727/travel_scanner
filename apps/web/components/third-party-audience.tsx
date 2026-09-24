"use client";

import { useEffect } from "react";
import { useHeaderSession } from "@/components/header-session";
import { setThirdPartyAudience } from "@/lib/third-party-audience";

/**
 * Tells the third-party scripts who is reading (see `lib/third-party-audience.ts`).
 *
 * `unknownRole` is for a document that deliberately never asks `/auth/me` (an article page
 * carrying ads, `app/[locale]/layout.tsx`): with a session cookie present the reader might be
 * an administrator, and nothing here can find out, so the scripts stay out.
 */
export function ThirdPartyAudience({ unknownRole = false }: { unknownRole?: boolean }) {
  const { status, user } = useHeaderSession();

  useEffect(() => {
    if (unknownRole || (status === "authenticated" && user?.is_admin)) setThirdPartyAudience("blocked");
    else if (status === "signed_out" || status === "authenticated") setThirdPartyAudience("allowed");
    else setThirdPartyAudience("pending");
  }, [status, unknownRole, user?.is_admin]);

  return null;
}
