import type { Metadata } from "next";
import { PublicFeatureGate } from "@/components/public-feature-gate";
import { featureEnabled } from "@/lib/site-features";
import { getSiteVisibility } from "@/lib/site-visibility.server";

// The gate answers 200 with this route's ordinary metadata when the feature is closed or
// the settings API cannot be read, so a crawl during a backend blip would index the
// "unavailable" page. The gate is a component and cannot contribute metadata itself.
export async function generateMetadata(): Promise<Metadata> {
  return featureEnabled(await getSiteVisibility(), "pricing") ? {} : { robots: { index: false } };
}

export default function PricingLayout({ children }: { children: React.ReactNode }) {
  return <PublicFeatureGate feature="pricing">{children}</PublicFeatureGate>;
}
