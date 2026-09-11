"use client";

import { CircleAlert } from "lucide-react";
import { useTranslations } from "next-intl";
import { useEffect, useState } from "react";
import { Link } from "@/i18n/navigation";
import { api } from "@/lib/api";
import { useSiteVisibility } from "@/components/site-visibility-provider";
import { featureEnabled } from "@/lib/site-features";

type UsageSummary = { available_uses: number };

/**
 * Shown in place of a charged action that came back with `insufficient_uses`.
 * The old behaviour sent the member to /pricing, where the purchase button is
 * disabled; this keeps them on the page, tells them the balance, and links to
 * the two pages that can actually explain it.
 */
export function UsageInsufficientNotice({ chargeLabel }: { chargeLabel: string }) {
  const t = useTranslations("usage");
  const [available, setAvailable] = useState<number | null | undefined>(undefined);
  // Linking to a page the owner has switched off is the other half of the dead end:
  // "go and buy more" pointing at "temporarily closed" leaves nothing to do.
  const visibility = useSiteVisibility();
  const canSeePlans = featureEnabled(visibility, "pricing");

  useEffect(() => {
    let active = true;
    api<UsageSummary>("/usage")
      .then((summary) => { if (active) setAvailable(summary.available_uses); })
      .catch(() => { if (active) setAvailable(null); });
    return () => { active = false; };
  }, []);

  return (
    <section role="alert" className="rounded-2xl border border-amber-200 bg-amber-50 p-5 text-amber-900">
      <p className="flex items-center gap-2 font-bold"><CircleAlert size={18} aria-hidden />{t("insufficientTitle")}</p>
      <p className="mt-2 text-sm leading-6">
        {available === undefined
          ? t("insufficientBodyUnknown", { uses: chargeLabel })
          : available === null
            ? t("insufficientBodyUnknown", { uses: chargeLabel })
            : t("insufficientBody", { uses: chargeLabel, available })}
        {" "}{canSeePlans ? t("insufficientPurchase") : t("purchaseUnavailable")}
      </p>
      <div className="mt-4 flex flex-wrap gap-3 text-sm font-semibold">
        <Link href="/account" className="rounded-xl bg-white px-4 py-2 text-amber-900 shadow-sm">{t("viewHistory")}</Link>
        {canSeePlans
          ? <Link href="/pricing" className="rounded-xl px-4 py-2 underline underline-offset-4">{t("viewPlans")}</Link>
          : <Link href="/contact" className="rounded-xl px-4 py-2 underline underline-offset-4">{t("contactUs")}</Link>}
      </div>
    </section>
  );
}
