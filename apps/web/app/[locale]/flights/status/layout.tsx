import { PublicFeatureGate } from "@/components/public-feature-gate";

export default function FlightStatusLayout({ children }: { children: React.ReactNode }) {
  return <PublicFeatureGate feature="flight_status">{children}</PublicFeatureGate>;
}
