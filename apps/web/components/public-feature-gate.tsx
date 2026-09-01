import { CircleOff, TriangleAlert } from "lucide-react";
import { getTranslations } from "next-intl/server";
import { SiteHeader } from "@/components/site-header";
import { Link } from "@/i18n/navigation";
import { featureEnabled, type SiteFeature } from "@/lib/site-features";
import { getSiteVisibility } from "@/lib/site-visibility.server";

const featureMessageKey: Record<SiteFeature, string> = {
  hotspots: "features.hotspots",
  trips: "features.trips",
  alerts: "features.alerts",
  flight_status: "features.flightStatus",
  airline_fares: "features.airlineFares",
  pricing: "features.pricing",
};

export async function PublicFeatureGate({
  feature,
  children,
}: {
  feature: SiteFeature;
  children: React.ReactNode;
}) {
  const visibility = await getSiteVisibility();
  if (featureEnabled(visibility, feature)) return children;

  const t = await getTranslations("availability");
  const unavailable = visibility.status === "unavailable";
  const Icon = unavailable ? TriangleAlert : CircleOff;
  const featureName = t(featureMessageKey[feature]);
  return (
    <>
      <SiteHeader />
      <main className="mx-auto max-w-3xl px-5 py-16 text-center md:px-8">
        <Icon aria-hidden className="mx-auto text-[var(--teal)]" size={42} />
        <h1 className="mt-5 text-3xl font-bold">
          {t(unavailable ? "unavailableTitle" : "closedTitle", { feature: featureName })}
        </h1>
        <p className="mx-auto mt-3 max-w-xl leading-7 text-[var(--muted)]">
          {t(unavailable ? "unavailableDescription" : "closedDescription")}
        </p>
        <Link href="/" className="mt-7 inline-flex rounded-xl bg-[var(--teal)] px-5 py-3 font-semibold text-white">
          {t("backHome")}
        </Link>
      </main>
    </>
  );
}
