import type { Metadata } from "next";
import { PublicFeatureGate } from "@/components/public-feature-gate";

// Everything under here belongs to one signed-in reader. Pages below add their own title
// and description; neither sets `robots`, so this one survives the shallow merge.
export const metadata: Metadata = { robots: { index: false, follow: true } };

export default function AlertsLayout({ children }: { children: React.ReactNode }) {
  return <PublicFeatureGate feature="alerts">{children}</PublicFeatureGate>;
}
