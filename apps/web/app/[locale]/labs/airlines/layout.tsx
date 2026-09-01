import { PublicFeatureGate } from "@/components/public-feature-gate";

export default function AirlineFaresLayout({ children }: { children: React.ReactNode }) {
  return <PublicFeatureGate feature="airline_fares">{children}</PublicFeatureGate>;
}
