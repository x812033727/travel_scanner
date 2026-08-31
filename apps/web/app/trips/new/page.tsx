import { NewTripAuthGate } from "@/components/new-trip-auth-gate";
import { SiteHeader } from "@/components/site-header";

export default function NewTripPage() {
  return <><SiteHeader /><main className="mx-auto max-w-6xl px-5 pb-20 pt-4 md:px-8"><NewTripAuthGate /></main></>;
}
