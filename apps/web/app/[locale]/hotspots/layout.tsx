import { PublicFeatureGate } from "@/components/public-feature-gate";

export default function HotspotsLayout({ children }: { children: React.ReactNode }) {
  return <PublicFeatureGate feature="hotspots">{children}</PublicFeatureGate>;
}
