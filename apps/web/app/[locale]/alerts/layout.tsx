import { PublicFeatureGate } from "@/components/public-feature-gate";

export default function AlertsLayout({ children }: { children: React.ReactNode }) {
  return <PublicFeatureGate feature="alerts">{children}</PublicFeatureGate>;
}
