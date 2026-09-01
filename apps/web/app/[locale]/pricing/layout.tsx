import { PublicFeatureGate } from "@/components/public-feature-gate";

export default function PricingLayout({ children }: { children: React.ReactNode }) {
  return <PublicFeatureGate feature="pricing">{children}</PublicFeatureGate>;
}
