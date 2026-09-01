import { AdminFoodsPanel } from "@/components/admin-foods-panel";
import { AdminNav } from "@/components/admin-nav";
import { SiteHeader } from "@/components/site-header";
import { getTranslations } from "next-intl/server";

export default async function AdminFoodsPage() {
  const t = await getTranslations("foodAdmin");
  return <><SiteHeader /><main className="mx-auto max-w-7xl px-5 pb-16 pt-8 md:px-8"><p className="text-sm font-semibold tracking-[.14em] text-[var(--teal)]">{t("eyebrow")}</p><h1 className="mt-2 text-4xl font-bold">{t("title")}</h1><p className="mt-3 max-w-3xl leading-7 text-[var(--muted)]">{t("description")}</p><AdminNav current="foods" /><AdminFoodsPanel /></main></>;
}
