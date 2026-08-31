import { NewTripForm } from "@/components/new-trip-form";
import { SiteHeader } from "@/components/site-header";

export default function NewTripPage() {
  return <><SiteHeader /><main className="mx-auto max-w-6xl px-5 pb-20 pt-4 md:px-8"><NewTripForm /></main></>;
}
