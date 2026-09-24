"use client";

import { usePathname } from "next/navigation";
import Script from "next/script";
import { useSyncExternalStore } from "react";
import { isPrivateRoute } from "@/lib/private-routes";
import { TRAVELPAYOUTS_DRIVE_SCRIPT_URL } from "@/lib/travelpayouts-drive";

const optimizerBypassAttributes = {
  nowprocket: "",
  "data-noptimize": "1",
  "data-cfasync": "false",
  "data-wpfc-render": "false",
  "seraph-accel-crit": "1",
  "data-no-defer": "1",
  "data-cmp-ab": "2",
};

function privacyOptOut(): boolean {
  return navigator.doNotTrack === "1"
    || (navigator as Navigator & { globalPrivacyControl?: boolean }).globalPrivacyControl === true;
}

function subscribeToPrivacySignals() {
  // DNT and GPC are fixed browser preferences for the lifetime of this page.
  return () => undefined;
}

export function TravelpayoutsDrive({ enabled }: { enabled: boolean }) {
  const pathname = usePathname();
  const mayLoad = useSyncExternalStore(
    subscribeToPrivacySignals,
    () => enabled && !privacyOptOut(),
    () => false,
  );

  // Never on a private page: a share link's token or a trip is readable by any script in the
  // document. `PrivateRouteIsolation` covers arriving there after the script already ran.
  if (!mayLoad || isPrivateRoute(pathname)) return null;

  return (
    <Script
      id="travelpayouts-drive"
      src={TRAVELPAYOUTS_DRIVE_SCRIPT_URL}
      strategy="afterInteractive"
      {...optimizerBypassAttributes}
    />
  );
}
