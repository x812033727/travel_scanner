import { PublicFeatureGate } from "@/components/public-feature-gate";

export default function TripsLayout({ children }: { children: React.ReactNode }) {
  return <PublicFeatureGate feature="trips">{children}</PublicFeatureGate>;
}
